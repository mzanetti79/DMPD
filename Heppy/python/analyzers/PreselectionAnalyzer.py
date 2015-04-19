from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import math
import ROOT
import sys

class PreselectionAnalyzer( Analyzer ):
    '''Preselect the events by requiring 1 or 2 jet(s)
       Cat 1: one fat, double b-tagged jet
       Cat 2: two resolved, b-tagged jets
       Cat 3: one single b-tagged jet'''
    
    def beginLoop(self,setup):
        super(PreselectionAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            self.inputCounter = ROOT.TH1F("Counter", "Counter", 10, 0, 10)
            self.inputCounter.GetXaxis().SetBinLabel(1, "All events")
            self.inputCounter.GetXaxis().SetBinLabel(2, "Trigger")
            self.inputCounter.GetXaxis().SetBinLabel(3, "#Jets > 1")
            self.inputCounter.GetXaxis().SetBinLabel(4, "Jet cuts")


       
    def fillJetVariables(self, event):
        for j in event.Jets:
            j.deltaPhi_met = deltaPhi(j.phi(), event.met.phi())
            j.deltaPhi_jet1 = deltaPhi(j.phi(), event.Jets[0].phi())
    
    
    def selectFatJet(self, event):
        if not len(event.cleanFatJets) >= 1:
            return False
        if not event.cleanFatJets[0].pt() > self.cfg_ana.fatjet_pt: 
            return False
        
        #########
        # FIXME dirty hack: count the number of ak4 b-tagged jet close instead
        # Count number of b-tagged subjets
        nSubJetTags = 0
        for f in event.cleanFatJets:
            subJets = []
            for j in event.cleanJets:
                if deltaR(f.eta(), f.phi(), j.eta(), j.phi())<0.8:
                    subJets.append(j)
            subJets.sort(key = lambda x : x.btag('combinedInclusiveSecondaryVertexV2BJetTags'), reverse = True)
            f.subJetCSV_1 = -99.
            f.subJetCSV_2 = -99.
            if len(subJets) >= 1:
                f.subJetCSV_1 = subJets[0].btag('combinedInclusiveSecondaryVertexV2BJetTags')
            if len(subJets) >= 2:
                f.subJetCSV_2 = subJets[1].btag('combinedInclusiveSecondaryVertexV2BJetTags')
        #########
        
        if not event.cleanFatJets[0].subJetCSV_1 > self.cfg_ana.fatjet_tag1 or not event.cleanFatJets[0].subJetCSV_2 > self.cfg_ana.fatjet_tag2: 
            return False
        return True


    def selectResolvedJet(self, event):
        if not len(event.cleanJets) >= 2:
            return False
        if not event.cleanJets[0].pt() > self.cfg_ana.jet1_pt: 
            return False
#        if not event.cleanJets[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.jet1_tag: 
#            return False
        if not event.cleanJets[1].pt() > self.cfg_ana.jet2_pt: 
            return False
#        if not event.cleanJets[1].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.jet2_tag: 
#            return False
        return True
    
    
    def selectMonoJet(self, event):
        if not len(event.cleanJets) >= 1:
            return False
        if not event.cleanJets[0].pt() > self.cfg_ana.jet1_pt:
            return False
        #if not event.cleanJets[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.jet1_tag:
        #    return False
        return True
    
    
    def process(self, event):
        event.Category = 0
        
        self.inputCounter.Fill(0)
        # Trigger
        self.inputCounter.Fill(1)
        
        # Check if there is at least one jet
        if len(event.cleanJets) < 1 and len(event.cleanFatJets) < 1:
            return False
        self.inputCounter.Fill(2)
        
        # Categorization
        # Category 1
        if self.selectFatJet(event):
            event.Category = 1
        # Category 2
        elif self.selectResolvedJet(event):
            event.Category = 2
        # Category 3
        elif self.selectMonoJet(event):
            event.Category = 3
        else:
            return False
        self.inputCounter.Fill(3)
        
        # Create final jet list (standard or fat)
        event.Jets = []
        if event.Category == 1:
            event.Jets = event.cleanFatJets
        else:
            event.Jets = event.cleanJets
        
        self.fillJetVariables(event)
        
        return True
    
