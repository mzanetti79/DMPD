from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import math
import ROOT

class PreselectionAnalyzer( Analyzer ):
    '''Preselect the events by requiring >= 1 jet and met
    '''

    def selectJet(self, event):
        if len(event.cleanJets) < 1:
            return False
        if event.cleanJets[0].pt() < self.cfg_ana.jet_pt :
            return False
        return True

    def selectMet(self, event):
        if event.met.pt() < self.cfg_ana.met_pt:
            return False
        return True

    def vetoTau(self, event):
        # VETO TAUS

    def vetoEle(self, event):
        # VETO ELECTRONS

    def process(self, event):
        if not self.selectJet(event):
            return False
        return True