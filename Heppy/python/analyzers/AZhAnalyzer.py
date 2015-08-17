from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT
from array import array

class AZhAnalyzer( Analyzer ):
    '''Analyzer for the Z' -> Zh -> (ll/nunu)bb analysis'''

    def beginLoop(self, setup):
        super(AZhAnalyzer, self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd("Counters")
            Z2LLlabels = ["Trigger", "#Lep #geq 2", "Z cand", "Jet p_{T}", "Z p_{T}", "Z mass", "h mass", "b-tag 1", "b-tag 2"]
            Z2NNlabels = ["Trigger", "e/#mu veto", "Jet p_{T}", "#slash{E}_{T}", "#Delta #varphi > 2.5", "h mass", "b-tag 1", "b-tag 2"]
            self.Z2EECounter = ROOT.TH1F("ZtoEECounter", "", len(Z2LLlabels), 0, len(Z2LLlabels))
            self.Z2MMCounter = ROOT.TH1F("ZtoMMCounter", "", len(Z2LLlabels), 0, len(Z2LLlabels))
            self.Z2NNCounter = ROOT.TH1F("ZtoNNCounter", "", len(Z2NNlabels), 0, len(Z2NNlabels))
            for i, l in enumerate(Z2LLlabels):
                self.Z2EECounter.GetXaxis().SetBinLabel(i+1, l)
                self.Z2MMCounter.GetXaxis().SetBinLabel(i+1, l)
            for i, l in enumerate(Z2NNlabels):
                self.Z2NNCounter.GetXaxis().SetBinLabel(i+1, l)
            setup.services["outputfile"].file.cd("..")
            setup.services["outputfile"].file.mkdir("Eff")
            setup.services["outputfile"].file.cd("Eff")
            pTbins = [0., 5., 10., 15., 20., 25., 30., 35., 40., 45., 50., 60., 70., 80., 90., 100., 110., 120., 130., 150., 175., 200., 225., 250., 300., 350., 400., 500.]
            self.DenElec1 = ROOT.TH1F("DenElec1", "", len(pTbins)-1, array('f', pTbins))
            self.EffElec1 = ROOT.TH1F("EffElec1", "", len(pTbins)-1, array('f', pTbins))
            self.DenElec2 = ROOT.TH1F("DenElec2", "", len(pTbins)-1, array('f', pTbins))
            self.EffElec2 = ROOT.TH1F("EffElec2", "", len(pTbins)-1, array('f', pTbins))
            self.DenMuon1 = ROOT.TH1F("DenMuon1", "", len(pTbins)-1, array('f', pTbins))
            self.EffMuon1 = ROOT.TH1F("EffMuon1", "", len(pTbins)-1, array('f', pTbins))
            self.DenMuon2 = ROOT.TH1F("DenMuon2", "", len(pTbins)-1, array('f', pTbins))
            self.EffMuon2 = ROOT.TH1F("EffMuon2", "", len(pTbins)-1, array('f', pTbins))
            dRbins = [0., 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.75, 1.0]
            self.DenElecZdR = ROOT.TH1F("DenElecZdR", "", len(dRbins)-1, array('f', dRbins))
            self.EffElecZdR_HEEP = ROOT.TH1F("EffElecZdR_HEEP", "", len(dRbins)-1, array('f', dRbins))
            self.EffElecZdR_HEEPpfIso = ROOT.TH1F("EffElecZdR_HEEPpfIso", "", len(dRbins)-1, array('f', dRbins))
            self.EffElecZdR_HEEPminiIso = ROOT.TH1F("EffElecZdR_HEEPminiIso", "", len(dRbins)-1, array('f', dRbins))
            self.EffElecZdR_Loose = ROOT.TH1F("EffElecZdR_Loose", "", len(dRbins)-1, array('f', dRbins))
            self.DenMuonZdR = ROOT.TH1F("DenMuonZdR", "", len(dRbins)-1, array('f', dRbins))
            self.EffMuonZdR_Tracker_Tracker = ROOT.TH1F("EffMuonZdR_Tracker_Tracker", "", len(dRbins)-1, array('f', dRbins))
            self.EffMuonZdR_HighPt_Tracker = ROOT.TH1F("EffMuonZdR_HighPt_Tracker", "", len(dRbins)-1, array('f', dRbins))
            self.EffMuonZdR_HighPt_HighPt = ROOT.TH1F("EffMuonZdR_HighPt_HighPt", "", len(dRbins)-1, array('f', dRbins))
            self.EffMuonZdR_Loose_Loose = ROOT.TH1F("EffMuonZdR_Loose_Loose", "", len(dRbins)-1, array('f', dRbins))
            self.EffMuonZdR_Tight_Tight = ROOT.TH1F("EffMuonZdR_Tight_Tight", "", len(dRbins)-1, array('f', dRbins))
            
    def endLoop(self, setup):
        self.EffElec1.Divide(self.DenElec1)
        self.EffElec2.Divide(self.DenElec2)
        self.EffMuon1.Divide(self.DenMuon1)
        self.EffMuon2.Divide(self.DenMuon2)
        self.EffElecZdR_HEEP.Divide(self.DenElecZdR)
        self.EffElecZdR_HEEPpfIso.Divide(self.DenElecZdR)
        self.EffElecZdR_HEEPminiIso.Divide(self.DenElecZdR)
        self.EffElecZdR_Loose.Divide(self.DenElecZdR)
        self.EffMuonZdR_Tracker_Tracker.Divide(self.DenMuonZdR)
        self.EffMuonZdR_HighPt_Tracker.Divide(self.DenMuonZdR)
        self.EffMuonZdR_HighPt_HighPt.Divide(self.DenMuonZdR)
        self.EffMuonZdR_Loose_Loose.Divide(self.DenMuonZdR)
        self.EffMuonZdR_Tight_Tight.Divide(self.DenMuonZdR)
        
        
        
    def fillGenPlots(self, event):
        if hasattr(event, "genleps") and len(event.genleps) >= 2:
            i1, i2 = [0, 1] if event.genleps[0].pt() > event.genleps[1].pt() else [1, 0]
            genZdR = deltaR(event.genleps[i1].eta(), event.genleps[i1].phi(), event.genleps[i2].eta(), event.genleps[i2].phi())
            
            # Electrons
            if abs(event.genleps[0].pdgId())==11:
                self.DenElec1.Fill(event.genleps[i1].pt())
                self.DenElec2.Fill(event.genleps[i2].pt())
                for i, l in enumerate(event.highptElectrons):
                    if deltaR(l.eta(), l.phi(), event.genleps[i1].eta(), event.genleps[i1].phi())<0.2 and abs(1-l.pt()/event.genleps[i1].pt()) < 0.3 and l.isHEEP: self.EffElec1.Fill(event.genleps[i1].pt())
                    if deltaR(l.eta(), l.phi(), event.genleps[i2].eta(), event.genleps[i2].phi())<0.2 and abs(1-l.pt()/event.genleps[i2].pt()) < 0.3 and l.isHEEP: self.EffElec2.Fill(event.genleps[i2].pt())
                        
                # deltaR
                self.DenElecZdR.Fill(genZdR)
                if len(event.highptElectrons) >= 2:
                    self.EffElecZdR_HEEP.Fill(genZdR)
                    if event.highptElectrons[0].miniRelIso<0.02 and event.highptElectrons[1].miniRelIso<0.02: self.EffElecZdR_HEEPminiIso.Fill(genZdR)
                    if event.highptElectrons[0].relIso03<0.15 and event.highptElectrons[1].relIso03<0.15: self.EffElecZdR_HEEPpfIso.Fill(genZdR)
                if len(event.selectedElectrons) >= 2: self.EffElecZdR_Loose.Fill(genZdR)
                
            # Muons
            if abs(event.genleps[0].pdgId())==13:
                self.DenMuon1.Fill(event.genleps[i1].pt())
                self.DenMuon2.Fill(event.genleps[i2].pt())
                for i, l in enumerate(event.highptMuons):
                    if deltaR(l.eta(), l.phi(), event.genleps[i1].eta(), event.genleps[i1].phi())<0.1 and abs(1-l.pt()/event.genleps[i1].pt()) < 0.3 and l.muonID("POG_ID_HighPt"): self.EffMuon1.Fill(event.genleps[i1].pt())
                    if deltaR(l.eta(), l.phi(), event.genleps[i2].eta(), event.genleps[i2].phi())<0.1 and abs(1-l.pt()/event.genleps[i2].pt()) < 0.3 and l.muonID("POG_ID_HighPt"): self.EffMuon2.Fill(event.genleps[i2].pt())
                        
                # deltaR
                self.DenMuonZdR.Fill(genZdR)
                if len(event.highptMuons) >= 2:
                    if event.highptMuons[0].miniRelIso<0.02 and event.highptMuons[1].miniRelIso<0.02: self.EffMuonZdR_Tracker_Tracker.Fill(genZdR)
                    if event.highptMuons[0].muonID("POG_ID_HighPt") and event.highptMuons[0].miniRelIso<0.02 and event.highptMuons[1].miniRelIso<0.02: self.EffMuonZdR_HighPt_Tracker.Fill(genZdR)
                    if event.highptMuons[0].muonID("POG_ID_HighPt") and event.highptMuons[0].miniRelIso<0.02 and event.highptMuons[1].muonID("POG_ID_HighPt") and event.highptMuons[1].miniRelIso<0.02: self.EffMuonZdR_HighPt_HighPt.Fill(genZdR)
                    if event.highptMuons[0].muonID("POG_ID_Loose") and event.highptMuons[0].relIso04<0.20 and event.highptMuons[1].muonID("POG_ID_Loose") and event.highptMuons[1].relIso04<0.20: self.EffMuonZdR_Loose_Loose.Fill(genZdR)
                    if event.highptMuons[0].muonID("POG_ID_Tight") and event.highptMuons[0].relIso04<0.12 and event.highptMuons[1].muonID("POG_ID_Tight") and event.highptMuons[1].relIso04<0.12: self.EffMuonZdR_Tight_Tight.Fill(genZdR)
    
    
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
        e.isHEEP = False
        if not e.pt() > 35.: return False
        
        if hasattr(e.gsfTrack(),"trackerExpectedHitsInner"):
		        nMissingHits = e.gsfTrack().trackerExpectedHitsInner().numberOfLostHits()
        else:
		        nMissingHits = e.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS)
        
        if abs(e.superCluster().eta()) < 1.4442:
            if not e.ecalDriven(): return False
            if not abs(e.deltaEtaSuperClusterTrackAtVtx()) < 0.004: return False
            if not abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: return False
            if not e.hadronicOverEm() < 2./e.energy() + 0.05: return False
            #if not e.sigmaIetaIeta() < 0: return False
            if not e.e2x5Max()/e.e5x5() > 0.94 or e.e1x5()/e.e5x5() > 0.83: return False
            if not nMissingHits <= 1: return False
            if not abs(e.dxy()) < 0.02: return False
        elif abs(e.superCluster().eta()) > 1.566 and abs(e.superCluster().eta()) < 2.5:
            if not e.ecalDriven(): return False
            if not abs(e.deltaEtaSuperClusterTrackAtVtx()) < 0.006: return False
            if not abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: return False
            if not e.hadronicOverEm() < 12.5/e.energy() + 0.05: return False
            if not e.sigmaIetaIeta() < 0.03: return False
            #if not e.e2x5Max()/e.e5x5() > 0.94 or e.e1x5()/e.e5x5() > 0: return False
            if not nMissingHits <= 1: return False
            if not abs(e.dxy()) < 0.05: return False
        else: return False
        e.isHEEP = True
        return True
    
    
    def process(self, event):
        event.isAZh = False
        event.isZ2EE = False
        event.isZ2MM = False
        event.isZ2NN = False
         # All
        self.Z2EECounter.Fill(-1)
        self.Z2MMCounter.Fill(-1)
        self.Z2NNCounter.Fill(-1)
        
         # Trigger
        self.Z2EECounter.Fill(0)
        self.Z2MMCounter.Fill(0)
        self.Z2NNCounter.Fill(0)
        
        #########################
        #    Part 1: Leptons    #
        #########################
        
        # Separate inclusive lepton collections
        event.highptElectrons = [x for x in event.inclusiveLeptons if x.isElectron() and self.isHEEP(x)]
        event.highptMuons = [x for x in event.inclusiveLeptons if x.isMuon() and x.isTrackerMuon()]
        event.highptLeptons = []
        
        self.fillGenPlots(event)
        
        # Categorization
        if len(event.highptElectrons) >= 2 and event.highptElectrons[0].pt() > self.cfg_ana.elec1pt and event.highptElectrons[1].pt() > self.cfg_ana.elec2pt:
            event.isZ2EE = True
        elif len(event.highptMuons) >= 2 and event.highptMuons[0].pt() > self.cfg_ana.muon1pt and event.highptMuons[1].pt() > self.cfg_ana.muon2pt:
            event.isZ2MM = True
        elif len(event.selectedMuons) + len(event.selectedElectrons) == 0:
            event.isZ2NN = True
        else:
            return True
        
        event.isZ2LL = event.isZ2EE or event.isZ2MM
        
        if event.isZ2EE: self.Z2EECounter.Fill(1) # Lep > 2
        if event.isZ2MM: self.Z2MMCounter.Fill(1) # Lep > 2
        if event.isZ2NN: self.Z2NNCounter.Fill(1) # Lep veto
        
        # Build Z candidate
        if event.isZ2EE: # and event.highptElectrons[0].charge() != event.highptElectrons[1].charge():
            event.highptLeptons = event.highptElectrons
        elif event.isZ2MM: # and event.highptMuons[0].charge() != event.highptMuons[1].charge():
            event.highptLeptons = event.highptMuons
        elif event.isZ2NN:
            event.highptLeptons = []
        else:
            return True
        
        # Z cand
        if event.isZ2EE: self.Z2EECounter.Fill(2)
        if event.isZ2MM: self.Z2MMCounter.Fill(2)
        
        
        #########################
        #    Part 2: Jets       #
        #########################
        
        if len(event.cleanJetsAK8)>=1 and event.cleanJetsAK8[0].pt() > self.cfg_ana.fatjet_pt: #FIXME
            #return True
            if event.isZ2EE: self.Z2EECounter.Fill(4)
            if event.isZ2MM: self.Z2MMCounter.Fill(4)
            if event.isZ2NN: self.Z2NNCounter.Fill(3)
        else:
            event.cleanJetsAK8.append( ROOT.pat.Jet() )
        
        #########################
        #   Part 3: Candidates  #
        #########################
        
        # Z candidate
        if event.isZ2LL:
            event.Z = event.highptLeptons[0].p4() + event.highptLeptons[1].p4()
            event.Z.charge = event.highptLeptons[0].charge() + event.highptLeptons[1].charge()
            event.Z.deltaR = deltaR(event.highptLeptons[0].eta(), event.highptLeptons[0].phi(), event.highptLeptons[1].eta(), event.highptLeptons[1].phi())
            event.Z.deltaEta = abs(event.highptLeptons[0].eta() - event.highptLeptons[1].eta())
            event.Z.deltaPhi = deltaPhi(event.highptLeptons[0].phi(), event.highptLeptons[1].phi())
        else:
            event.Z = event.met.p4()
        
        
        # h candidate with pseudo-kin fit
        kH = event.cleanJetsAK8[0].p4()
        k = 125.0/event.cleanJetsAK8[0].mass() if event.cleanJetsAK8[0].mass() > 0 else 0. #.userFloat("ak8PFJetsCHSSoftDropMass")
        kH = ROOT.reco.Particle.LorentzVector(event.cleanJetsAK8[0].px()*k, event.cleanJetsAK8[0].py()*k, event.cleanJetsAK8[0].pz()*k, event.cleanJetsAK8[0].energy()*k)
        
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
        
        if event.isZ2LL:
            self.addFakeMet(event, [event.highptLeptons[0], event.highptLeptons[1]])
        else:
            self.addFakeMet(event, [])
        
        if ((event.isZ2LL and event.Z.pt()) < self.cfg_ana.Z_pt) or ((event.isZ2NN and event.met.pt() < self.cfg_ana.met_pt)):
            return True
        
        
        # Fill tree
        event.isAZh = True
        
        if len(event.cleanJetsAK8) < 1 or event.cleanJetsAK8[0].pt() < self.cfg_ana.fatjet_pt: #FIXME
            event.cleanJetsAK8.pop()
            return True
        
        # ---------- Estimate cuts ----------
        if event.isZ2LL: 
            if event.Z.pt() > 200:
                self.Z2EECounter.Fill(4) if event.isZ2EE else self.Z2MMCounter.Fill(4)
                if event.Z.mass() > 75 and event.Z.mass() < 105:
                    self.Z2EECounter.Fill(5) if event.isZ2EE else self.Z2MMCounter.Fill(5)
                    if event.cleanJetsAK8[0].userFloat("ak8PFJetsCHSSoftDropMass") > 90 and event.cleanJetsAK8[0].userFloat("ak8PFJetsCHSSoftDropMass") < 150:
                        self.Z2EECounter.Fill(6) if event.isZ2EE else self.Z2MMCounter.Fill(6)
                        if event.cleanJetsAK8[0].subjets('SoftDrop')[0].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.605:
                            self.Z2EECounter.Fill(7) if event.isZ2EE else self.Z2MMCounter.Fill(7)
                            if event.cleanJetsAK8[0].subjets('SoftDrop')[1].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.605: 
                                self.Z2EECounter.Fill(8) if event.isZ2EE else self.Z2MMCounter.Fill(8)
        if event.isZ2NN: 
            if event.met.pt() > 200:
                self.Z2NNCounter.Fill(3)
                if event.cleanJetsAK8[0].deltaPhi_met>2.5:
                    if event.cleanJetsAK8[0].userFloat("ak8PFJetsCHSSoftDropMass") > 90 and event.cleanJetsAK8[0].userFloat("ak8PFJetsCHSSoftDropMass") < 150:
                        self.Z2NNCounter.Fill(4)
                        if event.cleanJetsAK8[0].subjets('SoftDrop')[0].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.605:
                            self.Z2NNCounter.Fill(5)
                            if event.cleanJetsAK8[0].subjets('SoftDrop')[1].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.605: 
                                self.Z2NNCounter.Fill(6)
        return True

