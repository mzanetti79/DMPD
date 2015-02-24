from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import math
import ROOT

class SRAnalyzer( Analyzer ):
    '''Select Signal Region
    '''

    def process(self, event):
        # Leptin veto
        if len(event.selectedMuons) != 0 or len(event.selectedElectrons) != 0 or len(event.selectedTaus) != 0 or len(event.selectedPhotons) != 0:
          return False
        # Select MET
        if event.met.pt() < self.cfg_ana.met_pt:
          return False
        # Select the first jet
        if len(event.cleanJets) < 1:
          return False
        elif len(event.cleanJets) == 1:
          if event.cleanJets[0].pt() > self.cfg_ana.jet1_pt:
            event.nJets = 1
        # select second jet, if present
        if len(event.cleanJets) == 2:
          if event.cleanJets[1].pt() > self.cfg_ana.jet2_pt and deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi()) < self.cfg_ana.deltaPhi12:
            event.nJets = 2
            return True
        # veto on other jets
        return False

