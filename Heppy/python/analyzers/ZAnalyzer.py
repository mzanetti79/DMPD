from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT

class ZAnalyzer( Analyzer ):
    '''Analyze and select Z->ll events'''

    def beginLoop(self,setup):
        super(ZAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            self.ZCRCounter = ROOT.TH1F("ZCRCounter", "ZCRCounter", 10, 0, 10)
            self.ZCRCounter.GetXaxis().SetBinLabel(1, "All events")
            self.ZCRCounter.GetXaxis().SetBinLabel(2, "Trigger")
            self.ZCRCounter.GetXaxis().SetBinLabel(3, "#Jets > 1")
            self.ZCRCounter.GetXaxis().SetBinLabel(4, "Jet cuts")
            self.ZCRCounter.GetXaxis().SetBinLabel(5, "Lep #geq 2")
            self.ZCRCounter.GetXaxis().SetBinLabel(6, "Lep1 cuts")
            self.ZCRCounter.GetXaxis().SetBinLabel(7, "Lep2 cuts")
            self.ZCRCounter.GetXaxis().SetBinLabel(8, "Z cand")
            self.ZCRCounter.GetXaxis().SetBinLabel(9, "MEt cut")
            
            
#    def vetoGamma(self, event):
#        # VETO PHOTONS - selectedPhotons must pass the 'veto' SelectionCuts
#        if len(event.selectedPhotons) != 0:
#            return False
#        return True
    
    def selectElectron1(self, event):
        # The leading electron has to satisfy the following conditions
        if not len(event.selectedElectrons) >= 1:
            return False
        if not event.selectedElectrons[0].pt() > self.cfg_ana.ele1_pt: 
            return False
        if not event.selectedElectrons[0].electronID(self.cfg_ana.ele1_id):
            return False
        event.electron1 = event.selectedElectrons[0]
        return True
        
    def selectElectron2(self, event):
        # Select the second electron, as the first one after the leading with opposite sign satisfying the following conditions
        if not len(event.selectedElectrons) >= 2:
            return False
        for e in event.selectedElectrons:
            if e.charge() == event.electron1.charge():
                continue
            if not e.pt() > self.cfg_ana.ele2_pt: 
                return False
            if not e.electronID(self.cfg_ana.ele2_id):
                return False
            event.electron2 = e
        return True
    
    
    def selectMuon1(self, event):
        # The leading muons has to satisfy the following conditions
        if not len(event.selectedMuons) >= 1:
            return False
        if not event.selectedMuons[0].pt() > self.cfg_ana.mu1_pt: 
            return False
        if not event.selectedMuons[0].muonID(self.cfg_ana.mu1_id):
            return False
        event.muon1 = event.selectedMuons[0]
        return True
        
    def selectMuon2(self, event):
        # Select the second muon, as the first one after the leading with opposite sign satisfying the following conditions
        if not len(event.selectedMuons) >= 2:
            return False
        for m in event.selectedMuons:
            if m.charge() == event.muon1.charge():
                continue
            if not m.pt() > self.cfg_ana.mu2_pt: 
                return False
            if not m.muonID(self.cfg_ana.mu2_id):
                return False
            event.muon2 = m
        return True
    
    
    def selectZ(self, event):
        event.isZtoEE = False
        event.isZtoMM = False
        
        if hasattr(event, "muon1") and hasattr(event, "muon2"):
            event.isZtoMM = True
            event.Leptons.append(event.muon1)
            event.Leptons.append(event.muon2)
        elif hasattr(event, "electron1") and hasattr(event, "electron2"):
            event.isZtoEE = True
            event.Leptons.append(event.electron1)
            event.Leptons.append(event.electron2)
        else:
            return False
            
        theZ = event.Leptons[0].p4() + event.Leptons[1].p4()
        if theZ.mass() < self.cfg_ana.mass_low or theZ.mass() > self.cfg_ana.mass_high:
            return False
        theZ.charge = event.Leptons[0].charge() + event.Leptons[1].charge()
        theZ.deltaR = deltaR(event.Leptons[0].eta(), event.Leptons[0].phi(), event.Leptons[1].eta(), event.Leptons[1].phi())
        theZ.deltaEta = abs(event.Leptons[0].eta() - event.Leptons[1].eta())
        theZ.deltaPhi = deltaPhi(event.Leptons[0].phi(), event.Leptons[1].phi())
        theZ.deltaPhi_met = deltaPhi(theZ.phi(), event.met.phi())
        theZ.deltaPhi_jet1 = deltaPhi(theZ.phi(), event.Jets[0].phi())
        event.Z = theZ
        
        return True

    def makeFakeMET(self,event):
        if not hasattr(event, "Z"):
            return False
        # Make ject in the event and adding Z px, py
        event.fakemet = copy.deepcopy(event.met)
        px, py = event.met.px()+event.Z.px(), event.met.py()+event.Z.py()
        event.fakemet.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        event.fakemetNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px()+event.Z.px(), event.metNoPU.py()+event.Z.py()
        event.fakemetNoPU.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        return True

    def selectFakeMET(self, event):
        if event.fakemet.pt() < self.cfg_ana.fakemet_pt:
            return False
        return True
         
    def process(self, event):
        event.isZCR = False
        event.Leptons = []
        
        # Leptons >= 2
        if not len(event.inclusiveLeptons)>=2:
            return True
        self.ZCRCounter.Fill(4)
        # Select first lepton
        if not self.selectMuon1(event) and not self.selectElectron1(event):
            return True
        self.ZCRCounter.Fill(5)
        # Select second lepton
        if not self.selectMuon2(event) and not self.selectElectron2(event):
            return True
        self.ZCRCounter.Fill(6)
        # Build Z candidate
        if not self.selectZ(event):
            return True
        self.ZCRCounter.Fill(7)
        # Build and cut fake MET
        if not self.makeFakeMET(event) or not self.selectFakeMET(event):
            return True
        self.ZCRCounter.Fill(8)
        # Vetoes
        #if not self.vetoGamma(event):
        #    return True
        #self.ZCRCounter.Fill(9)
        
        event.isZCR = True
        
        return True

