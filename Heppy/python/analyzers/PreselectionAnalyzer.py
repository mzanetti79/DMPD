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
            setup.services["outputfile"].file.cd()
            Labels = ["Trigger"]
            self.Counter = ROOT.TH1F("Counter", "Counter", 8, 0, 8)
            for i, l in enumerate(Labels):
                self.Counter.GetXaxis().SetBinLabel(i+1, l)
    
    
    def addJetVariables(self, event):
        for i, j in enumerate(event.xcleanJets):#+event.xcleanJetsJERUp+event.xcleanJetsJERDown:
            j.deltaPhi_met = abs(deltaPhi(j.phi(), event.met.phi()))
            j.deltaPhi_jet1 = abs(deltaPhi(j.phi(), event.xcleanJets[0].phi()))
        for i, j in enumerate(event.xcleanJetsAK8):#+event.xcleanJetsAK8JERUp+event.xcleanJetsAK8JERDown):
            j.deltaPhi_met = abs(deltaPhi(j.phi(), event.met.phi()))
            j.deltaPhi_jet1 = abs(deltaPhi(j.phi(), event.xcleanJetsAK8[0].phi()))
            j.dR_subjets = -1.
            if len(j.subjets('SoftDrop')) >= 2:
                j.dR_subjets = deltaR(j.subjets('SoftDrop')[0].eta(), j.subjets('SoftDrop')[0].phi(), j.subjets('SoftDrop')[1].eta(), j.subjets('SoftDrop')[1].phi())
        
        
        
#    def addJESUncertainty(self, event):
#        path = "%s/src/CMGTools/RootTools/data/jec" % os.environ['CMSSW_BASE'];
#        globalTag = "GR_70_V2_AN1"
#        jetFlavour = "AK4PFchs"
#        JetUncertainty = ROOT.JetCorrectionUncertainty("%s/%s_Uncertainty_%s.txt" % (path,globalTag,jetFlavour));
#        for i, j in enumerate(event.xcleanJets):
#            JetUncertainty.setJetEta(j.eta())
#            JetUncertainty.setJetPt(j.pt())
#            j.jetEnergyCorrUncertainty = JetUncertainty.getUncertainty(True) 
#        jetFlavour = "AK8PFchs"
#        JetUncertainty = ROOT.JetCorrectionUncertainty("%s/%s_Uncertainty_%s.txt" % (path,globalTag,jetFlavour));
#        for i, j in enumerate(event.xcleanJetsAK8):
#            JetUncertainty.setJetEta(j.eta())
#            JetUncertainty.setJetPt(j.pt())
#            j.jetEnergyCorrUncertainty = JetUncertainty.getUncertainty(True) 
    
    
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
    
    
    
    def createZ(self, event, leptons):
        theZ = leptons[0].p4() + leptons[1].p4()
        theZ.charge = leptons[0].charge() + leptons[1].charge()
        theZ.deltaR = deltaR(leptons[0].eta(), leptons[0].phi(), leptons[1].eta(), leptons[1].phi())
        theZ.deltaEta = abs(leptons[0].eta() - leptons[1].eta())
        theZ.deltaPhi = deltaPhi(leptons[0].phi(), leptons[1].phi())
        #theZ.deltaPhi_met = deltaPhi(theZ.phi(), event.met.phi())
        event.theZ = theZ
        return True
    
    def createW(self, event, lepton):
        theW = lepton.p4() + event.met.p4()
        theW.charge = lepton.charge()
        theW.deltaR = deltaR(lepton.eta(), lepton.phi(), 0, event.met.phi())
        theW.deltaEta = abs(lepton.eta())
        theW.deltaPhi = deltaPhi(lepton.phi(), event.met.phi())
        theW.deltaPhi_met = deltaPhi(lepton.phi(), event.met.phi())
        theW.mT = math.sqrt( 2.*lepton.et()*event.met.pt()*(1.-math.cos(theW.deltaPhi_met)) )
        event.theW = theW
        return True
    
    
    
    def process(self, event):
        event.isSR = False
        event.isZCR = False
        event.isWCR = False
        event.isTCR = False
        event.isGCR = False
        event.isZtoEE = False
        event.isZtoMM = False
        event.isWtoEN = False
        event.isWtoMN = False
        
        if self.cfg_comp.isMC: 
            event.eventWeight = abs(event.LHE_originalWeight)/event.LHE_originalWeight
        else:
            event.eventWeight = 1.
        
        # Build clean collections
        event.xcleanLeptons = event.selectedMuons + event.selectedElectrons
        event.xcleanTaus    = event.selectedTaus
        event.xcleanPhotons = event.selectedPhotons
        event.xcleanJets    = event.cleanJets
        event.xcleanJetsAK8 = event.cleanJetsAK8
#        event.xcleanJetsJERUp      = event.cleanJetsJERUp
#        event.xcleanJetsAK8JERUp   = event.cleanJetsAK8JERUp
#        event.xcleanJetsJERDown    = event.cleanJetsJERDown
#        event.xcleanJetsAK8JERDown = event.cleanJetsAK8JERDown
        
        self.addJetVariables(event)
        #self.addJESUncertainty(event)
        
        self.Counter.Fill(-1, event.eventWeight)
        # Trigger
        self.Counter.Fill(0, event.eventWeight)
        
        # Check if there is at least one jet
        #if len(event.cleanJets) < 1:# and len(event.cleanJetsAK8) < 1:
        #    return False
        #self.Counter.Fill(1)
        
        
        ########################################
        ### Count Leptons and select Regions ###
        ########################################
        
        
        ### Two leptons
        if len(event.selectedLeptons) >= 2:
            ###   TTbar Control Region   ###
            if len(event.selectedElectrons) == 1 and len(event.selectedMuons) == 1 and event.selectedElectrons[0].charge() != event.selectedMuons[0].charge():
                self.addFakeMet(event, [event.selectedElectrons[0], event.selectedMuons[0]])
                event.xcleanLeptons.sort(key = lambda l : l.pt(), reverse = True)
                event.isTCR = True
            
            ###   Z(ee) Control Region   ###
            elif len(event.selectedElectrons) >= 2 and event.selectedElectrons[0].charge() != event.selectedElectrons[1].charge():
                self.addFakeMet(event, [event.selectedElectrons[0], event.selectedElectrons[1]])
                self.createZ(event, [event.selectedElectrons[0], event.selectedElectrons[1]])
                event.xcleanLeptons = event.selectedElectrons
                event.isZtoEE = True
                event.isZCR = True
            
            ###   Z(mm) Control Region   ###
            elif len(event.selectedMuons) >= 2 and event.selectedMuons[0].charge() != event.selectedMuons[1].charge():
                self.addFakeMet(event, [event.selectedMuons[0], event.selectedMuons[1]])
                self.createZ(event, [event.selectedMuons[0], event.selectedMuons[1]])
                event.xcleanLeptons = event.selectedMuons
                event.isZtoMM = True
                event.isZCR = True
        
        ### One lepton
        elif len(event.selectedLeptons) == 1:
            ###   W(enu) Control Region   ###
            if len(event.selectedElectrons) == 1:
                self.addFakeMet(event, [event.selectedElectrons[0]])
                self.createW(event, event.selectedElectrons[0])
                event.xcleanLeptons = event.selectedElectrons
                event.isWtoEN = True
                event.isWCR = True
            
            ###   W(mnu) Control Region   ###
            elif len(event.selectedMuons) == 1:
                self.addFakeMet(event, [event.selectedMuons[0]])
                self.createW(event, event.selectedMuons[0])
                event.xcleanLeptons = event.selectedMuons
                event.isWtoMN = True
                event.isWCR = True
        
        ### One photon
        elif len(event.selectedPhotons) >= 1:
            self.addFakeMet(event, [event.selectedPhotons[0]])
            event.isGCR = True
        
        ### No leptons nor photons
        else:
            self.addFakeMet(event, [])
            event.isSR = True
        
        
        return True
    
