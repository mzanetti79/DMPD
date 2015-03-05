from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import math
import ROOT
import sys

class PreselectionAnalyzer( Analyzer ):
    '''Preselect the events by requiring 1 or 2 jet(s)
       Cat 1: one fat, double b-tagged jet
       Cat 2: two resolved, b-tagged jets
       Cat 3: one single b-tagged jet'''
        
    def selectJets(self, event):
        # Veto events with more than 2 jets with Pt>jetveto_pt and |Eta|<jetveto_eta
        if len(event.cleanJets) < 1:
            return False
        event.JetPostCuts = [x for x in event.cleanJets if x.pt() > self.cfg_ana.jetveto_pt and abs(x.eta()) < self.cfg_ana.jetveto_eta]
        if len(event.JetPostCuts) < 1 or len(event.JetPostCuts) > 2:
            return False
        return True
       
    #def fatJetCategory(self, event):
        #if event.fatJets[0].pt() > self.cfg_ana.jet1_pt and abs(event.fatJets[0].eta()) < self.cfg_ana.jet1_eta and event.fatJets[0].chargedHadronEnergyFraction() > self.cfg_ana.jet1_chf_min and event.fatJets[0].neutralHadronEnergyFraction() < self.cfg_ana.jet1_nhf_max and event.fatJets[0].neutralEmEnergyFraction() < self.cfg_ana.jet1_phf_max:
            #return 1
        #else:
            #return 0
    
    def slimJetCategory(self, event):
        if event.JetPostCuts[0].pt() < self.cfg_ana.jet1_pt                               or \
           abs(event.JetPostCuts[0].eta()) > self.cfg_ana.jet1_eta                        or \
           event.JetPostCuts[0].chargedHadronEnergyFraction() < self.cfg_ana.jet1_chf_min or \
           event.JetPostCuts[0].neutralHadronEnergyFraction() > self.cfg_ana.jet1_nhf_max or \
           event.JetPostCuts[0].neutralEmEnergyFraction() > self.cfg_ana.jet1_phf_max:
            return 0
        if len(event.JetPostCuts) == 2                                  and \
           event.JetPostCuts[1].pt() > self.cfg_ana.jet2_pt             and \
           abs(event.JetPostCuts[1].eta()) > self.cfg_ana.jet2_eta      and \
           deltaPhi(event.JetPostCuts[0].phi(), event.JetPostCuts[1].phi()) < self.cfg_ana.deltaPhi12:
            return 2
        else:
            return 3
        sys.exit("E R R O R! It should never get here! - PreselectionAnalyzer")

    def vetoElectron(self, event):
        if len(event.selectedElectrons) != 0:
            return False
        return True

    def vetoTau(self, event):
        if len(event.selectedTaus) != 0:
            return False
        return True

    def process(self, event):

        event.JetPostCuts = []
        event.Category = 0
                
        if not self.vetoElectron(event):
            return False
        if not self.vetoTau(event):
            return False
        if not self.selectJets(event):
            return False
        
        event.Category = self.slimJetCategory(event)
            
        if event.Category == 0:
            return False
        
        return True
    