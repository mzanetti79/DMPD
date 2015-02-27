from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import math
import ROOT

class SRAnalyzer( Analyzer ):
    '''Select Signal Region
    '''

    #def process(self, event):
        ## Leptin veto
        #if len(event.selectedMuons) != 0 or len(event.selectedElectrons) != 0 or len(event.selectedTaus) != 0 or len(event.selectedPhotons) != 0:
          #return False
        ## Select MET
        #if event.met.pt() < self.cfg_ana.met_pt:
          #return False
        ## Select the first jet
        #if len(event.cleanJets) < 1:
          #return False
        #elif len(event.cleanJets) == 1:
          #if event.cleanJets[0].pt() > self.cfg_ana.jet1_pt:
            #event.nJets = 1
        ## select second jet, if present
        #if len(event.cleanJets) == 2:
          #if event.cleanJets[1].pt() > self.cfg_ana.jet2_pt and deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi()) < self.cfg_ana.deltaPhi12:
            #event.nJets = 2
            #return True
        ## veto on other jets
        #return False

    def selectJets(self, event):
        if len(event.cleanJets) < 1:
          return False
        # Veto events with more than 2 jets
        JetPostCuts = [x for x in event.cleanJets if x.pt() > self.cfg_ana.jetveto_pt and abs(x.eta()) < self.cfg_ana.jetveto_eta]
        if len(JetPostCuts) > 2: 
            return False    
        # Count how many jets pass the selection
        event.nSRJets = 0
        if event.cleanJets[0].pt() > self.cfg_ana.jet1_pt and abs(event.cleanJets[0].eta()) < self.cfg_ana.jet1_eta :
            event.nSRJets = 1
            # select second jet, if present
            if len(event.cleanJets) > 1 and event.cleanJets[1].pt() > self.cfg_ana.jet2_pt and abs(event.cleanJets[1].eta()) < self.cfg_ana.jet2_eta and deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi()) < self.cfg_ana.deltaPhi12:
                event.nSRJets = 2        
        if event.nSRJets < 1:
            return False
        return True

    def vetoLeptonsGamma(self, event):
        if len(event.selectedMuons) != 0 or len(event.selectedElectrons) != 0 or len(event.selectedTaus) != 0 or len(event.selectedPhotons) != 0:
            return False
        return True

    def selectMet(self, event):
        if event.met.pt() < self.cfg_ana.met_pt:
          return False
        return True

    def process(self, event):
        if not self.vetoLeptonsGamma(event):
            return False
        if not self.selectJets(event):
            return False
        return True