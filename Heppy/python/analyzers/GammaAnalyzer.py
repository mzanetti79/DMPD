from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import copy
import math
import ROOT

class GammaAnalyzer( Analyzer ):
    '''Analyze and select gamma+jets events
    selectG: selects at least one photon above pt threshold
    '''
    
    def selectGamma(self, event):
      # Select at least one photon
      if len(event.selectedPhotons) < 1: return False
      if event.selectedPhotons[0] < self.cfg_ana.photon_pt:
        return False
      event.Gamma = event.selectedPhotons[0]
      return True
    
    def makeFakeMET(self,event):
        # Make ject in the event and adding photon px, py
        event.fakeMEt = copy.deepcopy(event.met)
        px, py = event.met.px()-event.Gamma.px(), event.met.py()-event.Gamma.py()
        event.fakeMEt.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        event.fakeMEtNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px()-event.Gamma.px(), event.metNoPU.py()-event.Gamma.py()
        event.fakeMEtNoPU.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        if event.fakeMEt.pt() < self.cfg_ana.met_pt:
          return False
        return True
        
        
    def process(self, event):
        if not self.selectGamma(event):
          return False
        if not self.makeFakeMET(event):
          return False
        return True

