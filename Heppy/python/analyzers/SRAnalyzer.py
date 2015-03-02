from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import math
import ROOT

class SRAnalyzer( Analyzer ):
    '''Select Signal Region; three categories are made:
    Cat 1: one fat, double b-tagged jet
    Cat 2: two resolved, b-tagged jets
    Cat 3: one single b-tagged jet
    '''

    def vetoLeptonsGamma(self, event):
        if len(event.selectedMuons) != 0 or len(event.selectedElectrons) != 0 or len(event.selectedTaus) != 0 or len(event.selectedPhotons) != 0:
            return False
        return True

    def selectMet(self, event):
        if event.met.pt() < self.cfg_ana.met_pt:
          return False
        return True
    
    def selectJets(self, event):
        if len(event.cleanJets) < 1:
            return False
        # Veto events with more than 2 jets
        event.JetPostCuts = [x for x in event.cleanJets if x.pt() > self.cfg_ana.jetveto_pt and abs(x.eta()) < self.cfg_ana.jetveto_eta]
        if len(event.JetPostCuts) > 2: 
            return False
    
    ### Category 1: one fat, double b-tagged jet
    def selectCategory1(self, event):
        if len(event.fatJets) < 1 or event.fatJets[0].pt() < self.cfg_ana.jet1_pt or abs(event.fatJets[0].eta()) < self.cfg_ana.jet1_eta:
            return False
        event.Category = 1
        return True
    
    ### Category 2: two resolved, b-tagged jet
    def selectCategory2(self, event):
        if event.JetPostCuts[0].pt() < self.cfg_ana.jet1_pt or abs(event.JetPostCuts[0].eta()) < self.cfg_ana.jet1_eta:
            return False # We shouldn't be here
        if event.JetPostCuts[1].pt() < self.cfg_ana.jet2_pt or abs(event.JetPostCuts[1].eta()) < self.cfg_ana.jet2_eta:
            if deltaPhi(event.JetPostCuts[0].phi(), event.JetPostCuts[1].phi()) > self.cfg_ana.deltaPhi12:
                return False
        event.Category = 2
        return True
    
    ### Category 3: one single b-tagged jet
    def selectCategory3(self, event):
        if event.JetPostCuts[0].pt() < self.cfg_ana.jet1_pt or abs(event.JetPostCuts[0].eta()) < self.cfg_ana.jet1_eta:
            if len(event.JetPostCuts) > 1:
                return False
        event.Category = 3
        return True
    
    
    def process(self, event):
        
        event.isSR = False
        event.Category = 0
        if self.selectMet(event) and self.vetoLeptonsGamma(event) and self.selectJets(event):
            event.isSR = True
            ### Category 1: one fat, double b-tagged jet
            #if self.selectCategory1(event):
            #    event.Category = 1
            ### Category 2: two resolved, b-tagged jet
            if self.selectCategory2(event):
                event.Category = 2
            ### Category 3: one single b-tagged jet
            elif self.selectCategory3(event):
                event.Category = 3
            return True
            
