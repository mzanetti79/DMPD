from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import copy
import math
import ROOT

class WAnalyzer( Analyzer ):
    '''Analyze and select W->mu nu events
    '''
    
    def selectW(self, event):
        # Select exactly one muon
        if len(event.selectedMuons) == 0:
          return False
        theW = event.selectedMuons[0].p4() + event.met.p4()
        if theW.mt() < self.cfg_ana.mt_low or theW.mt() > self.cfg_ana.mt_high:
          return False
        event.W = theW
        return True
    
    def makeFakeMET(self,event):
        # Make ject in the event and adding muon px, py
        event.fakeMEt = copy.deepcopy(event.met)
        px, py = event.met.px()-event.selectedMuons[0].px(), event.met.py()-event.selectedMuons[0].py()
        event.fakeMEt.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        event.fakeMEtNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px()-event.selectedMuons[0].px(), event.metNoPU.py()-event.selectedMuons[0].py()
        event.fakeMEtNoPU.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        if event.fakeMEt.pt() < self.cfg_ana.met_pt:
          return False
        return True
        
    
    def process(self, event):
        # Select exactly one muon
        if not self.selectW(event):
          return False
        if not self.makeFakeMET(event):
          return False
        return True

