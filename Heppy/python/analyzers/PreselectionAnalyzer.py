from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT
import os, sys

class PreselectionAnalyzer( Analyzer ):
    '''
    '''
    
    def beginLoop(self,setup):
        super(PreselectionAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.mkdir("Counters")
            setup.services["outputfile"].file.cd("Counters")
            Labels = ["All", "SR", "ZCR", "WCR", "TCR", "GCR"]
            self.Counter = ROOT.TH1F("Counter", "Counter", len(Labels), 0, len(Labels))
            self.Counter.Sumw2()
            for i, l in enumerate(Labels):
                self.Counter.GetXaxis().SetBinLabel(i+1, l)   
    
        # Jet Mass Recalibration
        if self.cfg_ana.recalibrateMass:
            path = os.path.expandvars(self.cfg_ana.jecPath)
            globalTag = self.cfg_ana.mcGT if self.cfg_comp.isMC else self.cfg_ana.dataGT
            jetFlavour = self.cfg_ana.recalibrationType
            self.vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
            #self.L1JetPar  = ROOT.JetCorrectorParameters("%s/%s_L1FastJet_%s.txt" % (path,globalTag,jetFlavour),"");
            self.L2JetPar  = ROOT.JetCorrectorParameters("%s/%s_L2Relative_%s.txt" % (path,globalTag,jetFlavour),"");
            self.L3JetPar  = ROOT.JetCorrectorParameters("%s/%s_L3Absolute_%s.txt" % (path,globalTag,jetFlavour),"");
            #self.vPar.push_back(self.L1JetPar);
            self.vPar.push_back(self.L2JetPar);
            self.vPar.push_back(self.L3JetPar);
            # Add residuals if needed
            if not self.cfg_comp.isMC: 
                self.ResJetPar = ROOT.JetCorrectorParameters("%s/%s_L2L3Residual_%s.txt" % (path,globalTag,jetFlavour))
                self.vPar.push_back(self.ResJetPar);
            #Step3 (Construct a FactorizedJetCorrector object) 
            self.JetCorrector = ROOT.FactorizedJetCorrector(self.vPar)
        
        if self.cfg_ana.addJECUncertainties:
            path = os.path.expandvars(self.cfg_ana.jecPath)
            globalTag = self.cfg_ana.mcGT if self.cfg_comp.isMC else self.cfg_ana.dataGT
            jetFlavour = self.cfg_ana.recalibrationType
            self.JetUncertainty = ROOT.JetCorrectionUncertainty("%s/%s_Uncertainty_%s.txt" % (path,globalTag,jetFlavour))
            
    
    def isHEEP(self, event, e):
        if not e.isElectron(): return False
        if not e.pt() > 35.: return False
        
        if abs(e.superCluster().eta()) < 1.4442:
            if not e.ecalDrivenSeed(): return False
            if not abs(e.deltaEtaSeedClusterTrackAtVtx() - e.superCluster().eta() + e.superCluster().seed().eta()) < 0.004: return False
            if not abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: return False
            if not e.hadronicOverEm() < 1./e.superCluster().energy() + 0.05: return False
            if not (e.full5x5_e2x5Max()/e.full5x5_e5x5() > 0.94 or e.full5x5_e1x5()/e.full5x5_e5x5() > 0.83): return False
            if not e.gsfTrack().hitPattern().numberOfHits(1) <= 1: return False
            if not abs(e.gsfTrack().dxy(event.goodVertices[0].position())) < 0.02: return False
        elif abs(e.superCluster().eta()) > 1.566 and abs(e.superCluster().eta()) < 2.5:
            if not e.ecalDrivenSeed(): return False
            if not abs(e.deltaEtaSeedClusterTrackAtVtx() - e.superCluster().eta() + e.superCluster().seed().eta()) < 0.006: return False
            if not abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: return False
            if not e.hadronicOverEm() < 5./e.superCluster().energy() + 0.05: return False
            if not full5x5sigmaIetaIeta < 0.03: return False
            if not e.gsfTrack().hitPattern().numberOfHits(1) <= 1: return False
            if not abs(e.gsfTrack().dxy(event.goodVertices[0].position())) < 0.05: return False
        else:
            return False
    
    
    def isCustomTracker(self, event, m):
        m.isCustomTracker = False
        if not m.isMuon(): return False

        if not m.isTrackerMuon(): return False
        if not m.numberOfMatchedStations() > 1: return False
        if not m.bestTrack().ptError()/m.bestTrack().pt() < 0.3: return False
        if not abs(m.bestTrack().dxy(event.goodVertices[0].position())) < 0.2: return False
        if not abs(m.bestTrack().dz(event.goodVertices[0].position())) < 0.5: return False
        if not m.innerTrack().isNonnull(): return False
        if not m.innerTrack().hitPattern().numberOfValidPixelHits() > 0: return False
        if not m.innerTrack().hitPattern().trackerLayersWithMeasurement() > 5: return False
        
        return True
    
    
    def addCorrectedJetMass(self, event, jet):
        if self.cfg_ana.recalibrateMass:
            self.JetCorrector.setJetPt(jet.pt() * jet.rawFactor())
            self.JetCorrector.setJetEta(jet.eta())
            self.JetCorrector.setJetE(jet.energy() * jet.rawFactor());
            self.JetCorrector.setJetA(jet.jetArea())
            self.JetCorrector.setRho(event.rho)
            self.JetCorrector.setNPV( len(event.vertices) )
            corr = self.JetCorrector.getCorrection()
        else:
            corr = 1.

        jet.addUserFloat("ak8PFJetsCHSPrunedMassCorr", corr*jet.userFloat("ak8PFJetsCHSPrunedMass"))
        jet.addUserFloat("ak8PFJetsCHSSoftDropMassCorr", corr*jet.userFloat("ak8PFJetsCHSSoftDropMass"))
    
    def addJECUnc(self, event, jet):
        if self.cfg_ana.addJECUncertainties and self.cfg_comp.isMC:
            self.JetUncertainty.setJetEta(jet.eta())
            self.JetUncertainty.setJetPt(jet.pt())
            jet.JECUnc = self.JetUncertainty.getUncertainty(True) 
            corr = 1./jet.rawFactor()
            corrUp = corr * max(0, 1+jet.JECUnc)
            corrDown = corr * max(0, 1-jet.JECUnc)
        else:
            corr, corrUp, corrDown = 1, 1, 1
        
        jet.ptJESUp = jet.pt() * corrUp * jet.rawFactor()
        jet.ptJESDown = jet.pt() * corrDown * jet.rawFactor()
    
    ##########
    
    def addLeptonVariables(self, event):
        for i, l in enumerate(event.inclusiveLeptons):
            l.isHEEP = self.isHEEP(event, l)
            l.isCustomTracker = self.isCustomTracker(event, l)
    
    def addJetVariables(self, event):
        for i, j in enumerate(event.xcleanJets):#+event.xcleanJetsJERUp+event.xcleanJetsJERDown:
            j.deltaPhi_met = abs(deltaPhi(j.phi(), event.fakemet.phi()))
            j.deltaPhi_jet1 = abs(deltaPhi(j.phi(), event.xcleanJets[0].phi()))
            if j.deltaPhi_met < event.minDeltaPhi: event.minDeltaPhi = j.deltaPhi_met
            self.addJECUnc(event, j)
            
        for i, j in enumerate(event.xcleanJetsAK8):#+event.xcleanJetsAK8JERUp+event.xcleanJetsAK8JERDown):
            j.deltaPhi_met = abs(deltaPhi(j.phi(), event.fakemet.phi()))
            j.deltaPhi_jet1 = abs(deltaPhi(j.phi(), event.xcleanJetsAK8[0].phi()))
            j.dR_subjets = -1.
            if len(j.subjets('SoftDrop')) >= 2:
                j.dR_subjets = deltaR(j.subjets('SoftDrop')[0].eta(), j.subjets('SoftDrop')[0].phi(), j.subjets('SoftDrop')[1].eta(), j.subjets('SoftDrop')[1].phi())
            self.addCorrectedJetMass(event, j)
            self.addJECUnc(event, j)
    
    
    
    
    
    def addFakeMet(self, event, particles):
        # Copy regular met
        event.fakemet = copy.deepcopy(event.met)
        px, py = event.met.px(), event.met.py()
        
        for p in particles:
            if not p:
                continue
            else:
                px += p.px()
                py += p.py()
        
        event.fakemet.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px, py)))
                
        return True
    
    def createZ(self, event, leptons):
        theZ = leptons[0].p4() + leptons[1].p4()
        theZ.charge = leptons[0].charge() + leptons[1].charge()
        theZ.deltaR = deltaR(leptons[0].eta(), leptons[0].phi(), leptons[1].eta(), leptons[1].phi())
        theZ.deltaEta = abs(leptons[0].eta() - leptons[1].eta())
        theZ.deltaPhi = abs(deltaPhi(leptons[0].phi(), leptons[1].phi()))
        #theZ.deltaPhi_met = abs(deltaPhi(theZ.phi(), event.met.phi()))
        event.theZ = theZ
        # Recoil correction variables
        recoilX = - event.met.px() - event.theZ.px()
        recoilY = - event.met.py() - event.theZ.py()
        event.Upara = (recoilX*event.theZ.px() + recoilY*event.theZ.py())/event.theZ.pt()
        event.Uperp = (recoilX*event.theZ.py() - recoilY*event.theZ.px())/event.theZ.pt()        
        return True
    
    def createW(self, event, lepton):
        theW = lepton.p4() + event.met.p4()
        theW.charge = lepton.charge()
        theW.deltaR = deltaR(lepton.eta(), lepton.phi(), 0, event.met.phi())
        theW.deltaEta = abs(lepton.eta())
        theW.deltaPhi = abs(deltaPhi(lepton.phi(), event.met.phi()))
        theW.deltaPhi_met = abs(deltaPhi(lepton.phi(), event.met.phi()))
        theW.mT = math.sqrt( 2.*lepton.et()*event.met.pt()*(1.-math.cos(deltaPhi(lepton.phi(), event.met.phi())) ) )
        event.theW = theW
        # Recoil correction variables
        recoilX = - event.met.px() - lepton.px()
        recoilY = - event.met.py() - lepton.py()
        event.Upara = (recoilX*lepton.px() + recoilY*lepton.py())/lepton.pt()
        event.Uperp = (recoilX*lepton.py() - recoilY*lepton.px())/lepton.pt()      
        
        # W' -> WH -> lnubb
        if len( event.cleanJetsAK8)>0:
            pz = 0.
            a = 80.4**2 - lepton.mass()**2 + 2.*lepton.px()*event.met.px() + 2.*lepton.py()*event.met.py()
            A = 4*( lepton.energy()**2 - lepton.pz()**2 )
            B = -4*a*lepton.pz()
            C = 4*lepton.energy()**2 * (event.met.px()**2  + event.met.py()**2) - a**2
            D = B**2 - 4*A*C
            if D>0:
                pz = min((-B+math.sqrt(D))/(2*A), (-B-math.sqrt(D))/(2*A))
            else:
                pz = -B/(2*A)
            kmet = event.met.p4()
            kmet.SetPz(pz)
            kH = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
            
            event.X = lepton.p4() + kmet +  event.cleanJetsAK8[0].p4()
            event.X.mT = (lepton.p4() + kmet +  event.cleanJetsAK8[0].p4()).mass()
            cmet = event.met.p4()
            cmet.SetPz(lepton.pz())
            event.X.mC = (lepton.p4() + cmet +  event.cleanJetsAK8[0].p4()).mass()
            event.X.mK = (lepton.p4() + kmet + kH).mass()
            event.X.deltaR = deltaR(kmet.eta(), kmet.phi(),  event.cleanJetsAK8[0].eta(),  event.cleanJetsAK8[0].phi())
            event.X.deltaEta = abs(kmet.eta() -  event.cleanJetsAK8[0].eta())
            event.X.deltaPhi = abs(deltaPhi(kmet.phi(),  event.cleanJetsAK8[0].phi()))
            event.X.charge = lepton.charge()
        else:
            event.X = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
        return True
    
    
    def createX(self, event):
        event.theX = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
        return True
    
    def process(self, event):
        event.isSR = False
        event.isZCR = False
        event.isWCR = False
        event.isTCR = False
        event.isGCR = False
        event.isSSR = False
        event.isZtoEE = False
        event.isZtoMM = False
        event.isWtoEN = False
        event.isWtoMN = False
               
        # Inclusive lepton collections
        event.inclusiveElectrons = [x for x in event.inclusiveLeptons if x.isElectron()]
        event.inclusiveMuons = [x for x in event.inclusiveLeptons if x.isMuon()]
        
        # Build clean collections
        event.xcleanLeptons = event.selectedMuons + event.selectedElectrons
        event.xcleanTaus    = event.selectedTaus
        event.xcleanPhotons = event.selectedPhotons
        event.xcleanJets    = event.cleanJets
        event.xcleanJetsAK8 = event.cleanJetsAK8
        
        # nJetsNotFatJet variables
        event.nJetsNoFatJet30 = -1
        event.nJetsNoFatJet50 = -1
        event.nJetsNoFatJet100 = -1
        if len(event.xcleanJetsAK8) > 0:
            for i, j in enumerate(event.xcleanJets):
                if deltaR(event.xcleanJetsAK8[0].eta(), event.xcleanJetsAK8[0].phi(), j.eta(), j.phi()) > 1.2:
                    if j.pt() > 30.:
                        event.nJetsNoFatJet30 += 1
                    if j.pt() > 50.:
                        event.nJetsNoFatJet50 += 1
                    if j.pt() > 100.:
                        event.nJetsNoFatJet100 += 1
        else:
            event.nJetsNoFatJet30 = event.nJetsNoFatJet50 = event.nJetsNoFatJet100 = len(event.xcleanJets)
        
        event.minDeltaPhi = 3.15
        
        
        
        
        for i in event.xcleanLeptons:
            setattr(i,'trigMatch',    False)
            setattr(i,'trigMatchPt',  -999.)
            setattr(i,'trigMatchEta', -999.)
            setattr(i,'trigMatchPhi', -999.)
            if hasattr(i,'matchedTrgObj') and (i.matchedTrgObj is not None):
                i.trigMatch    = True
                i.trigMatchPt  = i.matchedTrgObj.pt()
                i.trigMatchEta = i.matchedTrgObj.eta()
                i.trigMatchPhi = i.matchedTrgObj.phi()

#        event.xcleanJetsJERUp      = event.cleanJetsJERUp
#        event.xcleanJetsAK8JERUp   = event.cleanJetsAK8JERUp
#        event.xcleanJetsJERDown    = event.cleanJetsJERDown
#        event.xcleanJetsAK8JERDown = event.cleanJetsAK8JERDown
        
#        # Swap MET (met) and rawMET (uncorrected) collections
#        event.rawmet = copy.deepcopy(event.met)
#        
#        # MINIAOD v2 (Run 2015D)
#        px_ = event.met.uncorPx()
#        py_ = event.met.uncorPy()
#        pt_ = math.hypot(px_, py_)
#        event.rawmet.setP4(ROOT.reco.Particle.LorentzVector(px_, py_, 0, pt_))
        
        
        
        self.Counter.Fill(-1, event.weight)
        
        
        ########################################
        ###            Preselections         ###
        ########################################
        
        if not event.passedVertexAnalyzer:
            return False
        
        # Check if there is at least one jet
        #if len(event.cleanJets) < 1:# and len(event.cleanJetsAK8) < 1:
        #    return False
        #self.Counter.Fill(1)
        
        self.Counter.AddBinContent(1, event.weight)
        
        ########################################
        ### Count Leptons and select Regions ###
        ########################################
        
        
        
        ### Two leptons
        if len(event.selectedLeptons) >= 2:
            ####   W(mnu) Control Region   ###
            #if len(event.selectedMuons) >= 1:
                #self.addFakeMet(event, [event.selectedMuons[0]])
                #self.createW(event, event.selectedMuons[0])
                #event.xcleanLeptons = event.selectedMuons + event.selectedElectrons + event.otherLeptons
                #self.Counter.AddBinContent(4, event.weight)
                #event.isWtoMN = True
                #event.isWCR = True
                
            ####   W(enu) Control Region   ###
            #elif len(event.selectedElectrons) >= 1:
                #self.addFakeMet(event, [event.selectedElectrons[0]])
                #self.createW(event, event.selectedElectrons[0])
                #event.xcleanLeptons = event.selectedElectrons + event.selectedMuons + event.otherLeptons
                #self.Counter.AddBinContent(4, event.weight)
                #event.isWtoEN = True
                #event.isWCR = True
                
            ### ============================== ###
            
            ###   Z(mm) Control Region   ###
            if len(event.selectedMuons) >= 2 and event.selectedMuons[0].charge() != event.selectedMuons[1].charge():
                self.addFakeMet(event, [event.selectedMuons[0], event.selectedMuons[1]])
                self.createZ(event, [event.selectedMuons[0], event.selectedMuons[1]])
                event.xcleanLeptons = event.selectedMuons
                self.Counter.AddBinContent(3, event.weight)
                event.isZtoMM = True
                event.isZCR = True
                
            ###   Z(ee) Control Region   ###
            elif len(event.selectedElectrons) >= 2 and event.selectedElectrons[0].charge() != event.selectedElectrons[1].charge():
                self.addFakeMet(event, [event.selectedElectrons[0], event.selectedElectrons[1]])
                self.createZ(event, [event.selectedElectrons[0], event.selectedElectrons[1]])
                event.xcleanLeptons = event.selectedElectrons
                self.Counter.AddBinContent(3, event.weight)
                event.isZtoEE = True
                event.isZCR = True
                
            ###   TTbar Control Region   ###
            elif len(event.selectedElectrons) >= 1 and len(event.selectedMuons) >= 1 and event.selectedElectrons[0].charge() != event.selectedMuons[0].charge():
                self.addFakeMet(event, [event.selectedElectrons[0], event.selectedMuons[0]])
                event.xcleanLeptons =  [event.selectedMuons[0]] + [event.selectedElectrons[0]]
                #event.xcleanLeptons.sort(key = lambda l : l.pt(), reverse = True)
                self.Counter.AddBinContent(5, event.weight)
                event.isTCR = True
                
            else :
                return False # protection against events with, e.g., 1 e and 1 mu with same charge
                
        
        ### One lepton
        elif len(event.selectedLeptons) == 1:
            ###   W(mnu) Control Region   ###
            if len(event.selectedMuons) == 1:
                self.addFakeMet(event, [event.selectedMuons[0]])
                self.createW(event, event.selectedMuons[0])
                event.xcleanLeptons = event.selectedMuons
                #event.xcleanLeptons = event.selectedMuons + [x for x in event.otherLeptons if x.isMuon()]
                self.Counter.AddBinContent(4, event.weight)
                event.isWtoMN = True
                event.isWCR = True

                event.mtophad = -1
                if len(event.xcleanJets) > 1:
                    tophad = event.xcleanJets[0].p4() + event.xcleanJets[1].p4()
                    if len(event.xcleanJets) >= 3:
                        tophad = tophad + event.xcleanJets[2].p4()
                    event.mtophad = tophad.M()
            
            ###   W(enu) Control Region   ###
            elif len(event.selectedElectrons) == 1:
                self.addFakeMet(event, [event.selectedElectrons[0]])
                self.createW(event, event.selectedElectrons[0])
                event.xcleanLeptons = event.selectedElectrons
                #event.xcleanLeptons = event.selectedElectrons + [x for x in event.otherLeptons if x.isElectron()]
                self.Counter.AddBinContent(4, event.weight)
                event.isWtoEN = True
                event.isWCR = True
        
                event.mtophad = -1
                if len(event.xcleanJets) > 1:
                    tophad = event.xcleanJets[0].p4() + event.xcleanJets[1].p4()
                    if len(event.xcleanJets) >= 3:
                        tophad = tophad + event.xcleanJets[2].p4()
                    event.mtophad = tophad.M()
        
            else :
                return False # protection (useless here)
        
        #### One photon
        #elif len(event.selectedPhotons) >= 1:
            #self.addFakeMet(event, [event.selectedPhotons[0]])
            #self.Counter.AddBinContent(6, event.weight)
            #event.isGCR = True
        
        ### No leptons nor photons
        else:
            self.addFakeMet(event, [])
            self.createX(event)
            self.Counter.AddBinContent(2, event.weight)
            event.isSR = True
            
        # Add jet variables (after fakemet computation)
        self.addJetVariables(event)
        
        
        ########################################
        ###             Same-sign            ###
        ########################################
        
        if (len(event.inclusiveMuons) >= 1 and event.inclusiveMuons[0].pt() > 10) or (len(event.selectedElectrons) >= 1 and event.selectedElectrons[0].pt() > 25.): event.isSSR = True
            
        
        return True
    
