from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import math
import ROOT

class SRAnalyzer( Analyzer ):
    '''Select Signal Region
    '''

    def vetoMuon(self, event):
        # VETO MUONS - selectedMuons must pass the 'veto' SelectionCuts
        if len(event.selectedMuons) != 0:
            return False
        return True

    def vetoGamma(self, event):
        # VETO PHOTONS - selectedPhotons must pass the 'veto' SelectionCuts
        if len(event.selectedPhotons) != 0:
            return False
        return True

    def selectMet(self, event):
        if event.met.pt() < self.cfg_ana.met_pt:
            return False
        if event.Category == 1 and deltaPhi(event.fatJets[0].phi(), event.met.phi()) > self.cfg_ana.deltaPhi1met:
            return True
        if (event.Category == 2 or event.Category == 3) and deltaPhi(event.JetPostCuts[0].phi(), event.met.phi()) > self.cfg_ana.deltaPhi1met:
            return True
        return False
        
    def process(self, event):
        
        event.isSR = False
        if self.vetoMuon(event) and self.vetoGamma(event) and self.selectMet(event):
            event.isSR = True
            return True
