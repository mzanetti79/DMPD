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
            self.inputCounter = ROOT.TH1F("WCounter", "WCounter", 10, 0, 10)
    
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
        event.Muon = event.selectedMuons[0]
        return True
    
    def selectW(self, event):
        if not event.Muon:
            return False
        theW = event.Muon.p4() + event.met.p4()
        if theW.mt() < self.cfg_ana.mt_low or theW.mt() > self.cfg_ana.mt_high:
            return False
        theW.charge = event.Muon.charge()
        theW.deltaEta = abs(event.Muon.eta())
        theW.deltaPhi = deltaPhi(event.Muon.phi(), event.met.phi())
        theW.deltaR = deltaR(event.Muon.eta(), event.Muon.phi(), 0, event.met.phi())
        event.W = theW
        return True
    
    def makeFakeMET(self,event):
        if not event.Muon:
            return False
        # Make ject in the event and adding muon px, py
        event.fakeMEt = copy.deepcopy(event.met)
        px, py = event.met.px() + event.Muon.px(), event.met.py() + event.Muon.py()
        event.fakeMEt.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px,py)))
        
        event.fakeMEtNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px() + event.Muon.px(), event.metNoPU.py() + event.Muon.py()
        event.fakeMEtNoPU.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px,py)))
        
        return True
                
    def selectFakeMet(self, event):
        if event.fakeMEt.pt() < self.cfg_ana.fakemet_pt:
            return False
#        if event.Category == 1 and deltaPhi(event.fatJets[0].phi(), event.fakeMEt.phi()) > self.cfg_ana.deltaPhi1met:
#            return True
#        if (event.Category == 2 or event.Category == 3) and deltaPhi(event.JetPostCuts[0].phi(), event.fakeMEt.phi()) > self.cfg_ana.deltaPhi1met:
#            return True
        return True
    
    def process(self, event):
        # Select exactly one muon
        event.isWCR = False
        event.Muon = None
        event.W = None
        
        # Exactly one muon
        if not len(event.selectedMuons) == 1:
            return True
        self.inputCounter.Fill(3)
        # Select the muon
        if not self.selectMuon(event):
            return True
        self.inputCounter.Fill(4)
        # Build W candidate
        if not self.selectW(event):
            return True
        self.inputCounter.Fill(5)
        # Build and cut fake MET
        if not self.makeFakeMET(event) or not self.selectFakeMet(event):
            return True
        self.inputCounter.Fill(6)
        # Vetoes
        #if not self.vetoGamma(event):
        #    return True
        #self.inputCounter.Fill(7)
        
        event.candidate = event.W
        event.isWCR = True
        return True
        
