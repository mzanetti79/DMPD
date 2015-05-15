from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT

class WAnalyzer( Analyzer ):
    '''Analyze and select W->mu nu events'''
    
    def beginLoop(self,setup):
        super(WAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            WCRLabels = ["Trigger", "#Jets > 1", "Jet cuts", "#Muons > 1", "Muon cuts", "W cand", "MEt cut"]
            self.WCRCounter = ROOT.TH1F("WCRCounter", "WCRCounter", 8, 0, 8)
            for i, l in enumerate(WCRLabels):
                self.WCRCounter.GetXaxis().SetBinLabel(i+1, l)

    
    #def selectW(self, event):
        ## Select exactly one muon
        #if len(event.selectedMuons) == 0:
          #return False
        #theW = event.selectedMuons[0].p4() + event.met.p4()
        #if theW.mt() < self.cfg_ana.mt_low or theW.mt() > self.cfg_ana.mt_high:
          #return False
        #event.W = theW
        #return True
    
#    def vetoGamma(self, event):
#        # VETO PHOTONS - selectedPhotons must pass the 'veto' SelectionCuts
#        if len(event.selectedPhotons) != 0:
#            return False
#        return True
#    
    
    
    def selectMuon(self, event):
        # The leading muons has to satisfy the following conditions
        if not len(event.selectedMuons) >= 1:
            return False
        if not event.selectedMuons[0].pt() > self.cfg_ana.mu_pt: 
            return False
        if not event.selectedMuons[0].muonID(self.cfg_ana.mu_id):
            return False
        if not event.selectedMuons[0].relIso04 < self.cfg_ana.mu_iso:
            return False
        event.muon1 = event.selectedMuons[0]
        return True
    
    def selectW(self, event):
        if not hasattr(event, "muon1"):
            return False
        theW = event.selectedMuons[0].p4() + event.met.p4()
        theW.deltaPhi_met = deltaPhi(event.selectedMuons[0].phi(), event.met.phi())
        theW.mT = math.sqrt( 2.*event.selectedMuons[0].et()*event.met.pt()*(1.-math.cos(theW.deltaPhi_met)) )        
        if theW.mT < self.cfg_ana.mt_low or theW.mT > self.cfg_ana.mt_high:
            return False
        theW.charge = event.selectedMuons[0].charge()
        theW.deltaEta = abs(event.selectedMuons[0].eta())
        theW.deltaPhi = deltaPhi(event.selectedMuons[0].phi(), event.met.phi())
        theW.deltaR = deltaR(event.selectedMuons[0].eta(), event.selectedMuons[0].phi(), 0, event.met.phi())
        event.W = theW
        return True
    
    def makeFakeMET(self,event):
        if not hasattr(event, "muon1"):
            return False
        # Make ject in the event and adding muon px, py
        event.fakemet = copy.deepcopy(event.met)
        px, py = event.met.px() + event.selectedMuons[0].px(), event.met.py() + event.selectedMuons[0].py()
        event.fakemet.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px,py)))
        
        event.fakemetNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px() + event.selectedMuons[0].px(), event.metNoPU.py() + event.selectedMuons[0].py()
        event.fakemetNoPU.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px,py)))
        
        return True
                
    def selectFakeMET(self, event):
        if event.fakemet.pt() < self.cfg_ana.fakemet_pt:
            return False
        return True
    
    def process(self, event):
        # Select exactly one muon
        event.isWCR = False
        
        # Exactly one muon
        if not len(event.selectedMuons) == 1:
            return True
        self.WCRCounter.Fill(3)
        # Select the muon
        if not self.selectMuon(event):
            return True
        self.WCRCounter.Fill(4)
        # Build W candidate
        if not self.selectW(event):
            return True
        self.WCRCounter.Fill(5)
        # Build and cut fake MET
        if not self.makeFakeMET(event) or not self.selectFakeMET(event):
            return True
        self.WCRCounter.Fill(6)
        # Vetoes
        #if not self.vetoGamma(event):
        #    return True
        #self.WCRCounter.Fill(7)
        
        event.isWCR = True
        return True
        
