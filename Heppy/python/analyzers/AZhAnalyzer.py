from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT

class AZhAnalyzer( Analyzer ):
    '''Analyzer for the Z' -> Zh -> (ll/nunu)bb analysis'''

    def beginLoop(self,setup):
        super(AZhAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            Z2LLlabels = ["Trigger", "#Lep #geq 2", "Z cand", "Jet p_{T}", "Z p_{T}", "Z mass", "h mass", "b-tag 1", "b-tag 2"]
            Z2NNlabels = ["Trigger", "e/#mu veto", "Jet p_{T}", "#slash{E}_{T}", "#delta #varphi > 2.5", "h mass", "b-tag 1", "b-tag 2"]
            self.Z2LLCounter = ROOT.TH1F("ZtoLLCounter", "", len(Z2LLlabels), 0, len(Z2LLlabels))
            self.Z2NNCounter = ROOT.TH1F("ZtoNNCounter", "", len(Z2NNlabels), 0, len(Z2NNlabels))
            for i, l in enumerate(Z2LLlabels):
                self.Z2LLCounter.GetXaxis().SetBinLabel(i+1, l)
            for i, l in enumerate(Z2NNlabels):
                self.Z2NNCounter.GetXaxis().SetBinLabel(i+1, l)
    
    def addFakeMet(self, event, particles):
        # Copy regular met
        event.fakemet = copy.deepcopy(event.met)
        px, py = event.met.px(), event.met.py()
        for i, p in enumerate(particles):
            if not p:
                continue
            else:
                px += p.px()
                py += p.py()
        
        event.fakemet.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px, py)))
        return True
    
    def isHEEP(self, e):
        if not e.pt() > 35.: return False
        if abs(e.superCluster().eta()) < 1.4442:
            if not e.ecalDriven(): return False
            if not abs(e.deltaEtaSuperClusterTrackAtVtx()) < 0.004: return False
            if not abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: return False
            if not e.hadronicOverEm() < 1./e.energy() + 0.05: return False
            #if not e.sigmaIetaIeta() < 0: return False
            if not e.e2x5()/e.e5x5() > 0.94 or e.e1x5()/e.e5x5() > 0.83: return False
            if not e.gsfTrack().trackerExpectedHitsInner().numberOfLostHits() <= 1: return False
            if not abs(e.dxy()) < 0.02: return False
        elif abs(e.superCluster().eta()) > 1.566 and abs(e.superCluster().eta()) < 2.5:
            if not e.ecalDriven(): return False
            if not abs(e.deltaEtaSuperClusterTrackAtVtx()) < 0.006: return False
            if not abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: return False
            if not e.hadronicOverEm() < 5./e.energy() + 0.05: return False
            if not e.sigmaIetaIeta() < 0.03: return False
            #if not e.e2x5()/e.e5x5() > 0.94 or e.e1x5()/e.e5x5() > 0: return False
            if not e.gsfTrack().trackerExpectedHitsInner().numberOfLostHits() <= 1: return False
            if not abs(e.dxy()) < 0.05: return False
        else: return False
        return True
    
    
    def process(self, event):
        event.isAZh = False
        event.isZ2EE = False
        event.isZ2MM = False
        event.isZ2NN = False
        
        self.Z2LLCounter.Fill(-1) # All
        self.Z2NNCounter.Fill(-1)
        
        
        self.Z2LLCounter.Fill(0) # Trigger
        self.Z2NNCounter.Fill(0)
        
        #########################
        #    Part 1: Leptons    #
        #########################
        
        # Separate inclusive lepton collections
        event.highptElectrons = [x for x in event.inclusiveLeptons if x.isElectron() and isHEEP(x)]
        event.highptMuons = [x for x in event.inclusiveLeptons if x.isMuon() and x.muonID("POG_ID_HighPt")]
        event.highptLeptons = []
        
        # Categoriazation
        if len(event.highptElectrons) >= 2 and event.highptElectrons[0].pt() > self.cfg_ana.elec1pt and event.highptElectrons[1].pt() > self.cfg_ana.elec2pt:
            event.isZ2EE = True
        elif len(event.highptMuons) >= 2 and event.highptMuons[0].pt() > self.cfg_ana.muon1pt and event.highptMuons[1].pt() > self.cfg_ana.muon2pt:
            event.isZ2MM = True
        elif len(event.selectedMuons) + len(event.selectedElectrons) == 0:
            event.isZ2NN = True
        else:
            return True
        
        event.isZ2LL = event.isZ2EE or event.isZ2MM
        
        if event.isZ2LL: self.Z2LLCounter.Fill(1) # Lep > 2
        if event.isZ2NN: self.Z2NNCounter.Fill(1) # Lep veto
        
        # Build Z candidate
        if event.isZ2EE and event.highptElectrons[0].charge() != event.highptElectrons[1].charge():
            event.highptLeptons = event.highptElectrons
        elif event.isZ2MM and event.highptMuons[0].charge() != event.highptMuons[1].charge():
            event.highptLeptons = event.highptMuons
        elif event.isZ2NN:
            event.highptLeptons = []
        else:
            return True
        
        if event.isZ2LL: self.Z2LLCounter.Fill(2) # Z cand
        
        #########################
        #    Part 2: Jets       #
        #########################
        
        if len(event.cleanJetsAK8)<1 or event.cleanJetsAK8[0].pt() < self.cfg_ana.fatjet_pt:
            return True
        
        if event.isZ2LL: self.Z2LLCounter.Fill(3) # Jet pT
        if event.isZ2NN: self.Z2NNCounter.Fill(2) # Jet pT
        
        #########################
        #   Part 3: Candidates  #
        #########################
        
        # Z candidate
        if len(event.highptLeptons) >= 2:
            event.Z = event.highptLeptons[0].p4() + event.highptLeptons[1].p4()
            event.Z.charge = event.highptLeptons[0].charge() + event.highptLeptons[1].charge()
            event.Z.deltaR = deltaR(event.highptLeptons[0].eta(), event.highptLeptons[0].phi(), event.highptLeptons[1].eta(), event.highptLeptons[1].phi())
            event.Z.deltaEta = abs(event.highptLeptons[0].eta() - event.highptLeptons[1].eta())
            event.Z.deltaPhi = deltaPhi(event.highptLeptons[0].phi(), event.highptLeptons[1].phi())
        
        # h candidate with pseudo-kin fit
        kH = event.cleanJetsAK8[0].p4()
        k = 125.0/event.cleanJetsAK8[0].mass()#.userFloat("ak8PFJetsCHSSoftDropMass")
        kH.SetE( event.cleanJetsAK8[0].energy()*k )
        kH.SetPx( event.cleanJetsAK8[0].px()*k )
        kH.SetPy( event.cleanJetsAK8[0].py()*k )
        kH.SetPz( event.cleanJetsAK8[0].pz()*k )
        
        # A/Z' candidate
        if event.isZ2LL:
            event.A = event.Z + event.cleanJetsAK8[0].p4()
            event.A.mT = event.A.mass()
            event.A.mC = event.A.mass()
            event.A.mK = (event.Z + kH).mass()
        elif len(event.highptLeptons) == 1:
            event.A = event.highptLeptons[0].p4() + event.met.p4() + event.cleanJetsAK8[0].p4()
            pz = 0.
            a = 80.4**2 - event.highptLeptons[0].mass()**2 + 2.*event.highptLeptons[0].px()*event.met.px() + 2.*event.highptLeptons[0].py()*event.met.py()
            A = 4*( event.highptLeptons[0].energy()**2 - event.highptLeptons[0].pz()**2 )
            B = -4*a*event.highptLeptons[0].pz()
            C = 4*event.highptLeptons[0].energy()**2 * (event.met.px()**2  + event.met.py()**2) - a**2
            D = B**2 - 4*A*C
            if D>0:
                pz = min((-B+math.sqrt(D))/(2*A), (-B-math.sqrt(D))/(2*A))
            else:
                pz = -B/(2*A)
            kmet = event.met.p4()
            kmet.SetPz(pz)
            event.A.mT = (event.highptLeptons[0].p4() + kmet + event.cleanJetsAK8[0].p4()).mass()
            cmet = event.met.p4()
            cmet.SetPz(event.highptLeptons[0].pz())
            event.A.mC = (event.highptLeptons[0].p4() + cmet + event.cleanJetsAK8[0].p4()).mass()
            event.A.mK = (event.highptLeptons[0].p4() + kmet + kH).mass()
        else:
            event.A = event.met.p4() + event.cleanJetsAK8[0].p4()
            event.A.mT = math.sqrt( 2.*event.cleanJetsAK8[0].energy()*event.met.pt()*(1.-math.cos( deltaPhi(event.cleanJetsAK8[0].phi(), event.met.phi()) )) )
            cmet = event.met.p4()
            cmet.SetPz( -event.cleanJetsAK8[0].pz() )
            event.A.mC = (cmet + event.cleanJetsAK8[0].p4()).mass()
            event.A.mK = math.sqrt( 2.*kH.energy()*event.met.pt()*(1.-math.cos( deltaPhi(kH.phi(), event.met.phi()) )) )
        
        # Fill tree
        event.isAZh = True
        
        
        
        # ---------- Estimate cuts ----------
        if event.isZ2LL: 
            if event.Z.pt() > 200:
                self.Z2LLCounter.Fill(4)
                if event.Z.mass() > 75 and event.Z.mass() < 105:
                    self.Z2LLCounter.Fill(5)
                    if event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) > self.cfg_ana.fatjet_mass_low and event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) < self.cfg_ana.fatjet_mass_high:
                        self.Z2LLCounter.Fill(6)
                            #if event.cleanJetsAK8[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag:
                            if event.cleanJetsAK8[0].subjets('SoftDrop')[0].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatjet_btag_1:
                                self.Z2LLCounter.Fill(7)
                                # b-Jet2
                                if event.cleanJetsAK8[0].subjets('SoftDrop')[1].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatjet_btag_2: 
                                    self.Z2LLCounter.Fill(8)
        if event.isZ2NN: 
            if event.met.pt() > 200:
                self.Z2NNCounter.Fill(3)
                if event.cleanJetsAK8[0].deltaPhi_met>2.5:
                    if event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) > self.cfg_ana.fatjet_mass_low and event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) < self.cfg_ana.fatjet_mass_high:
                        self.Z2NNCounter.Fill(4)
                            #if event.cleanJetsAK8[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag:
                            if event.cleanJetsAK8[0].subjets('SoftDrop')[0].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatjet_btag_1:
                                self.Z2NNCounter.Fill(5)
                                # b-Jet2
                                if event.cleanJetsAK8[0].subjets('SoftDrop')[1].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatjet_btag_2: 
                                    self.Z2NNCounter.Fill(6)
        return True

