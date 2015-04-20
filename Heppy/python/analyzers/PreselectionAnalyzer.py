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
        for j in event.Jets + event.cleanJets + event.cleanFatJets:
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
            f.nSubJets = len(subJets)
            if len(subJets) >= 1:
                f.subJet1 = subJets[0]
            if len(subJets) >= 2:
                f.subJet2 = subJets[1]
        #########
        
        if not event.cleanFatJets[0].nSubJets >=2 or not event.cleanFatJets[0].subJet1.btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatjet_tag1 or not event.cleanFatJets[0].subJet2.btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatjet_tag2: 
            return False
        
        # Higgs candidate
        event.cleanFatJets[0].setMass(event.cleanFatJets[0].userFloat("ak8PFJetsCHSPrunedLinks"))
        theH = event.cleanFatJets[0].p4()
        theH.charge = event.cleanFatJets[0].charge()
        theH.deltaR = deltaR(event.cleanFatJets[0].subJet1.eta(), event.cleanFatJets[0].subJet1.phi(), event.cleanFatJets[0].subJet2.eta(), event.cleanFatJets[0].subJet2.phi()) if hasattr(event.cleanFatJets[0], "subJet2") else -1.
        theH.deltaEta = abs(event.cleanFatJets[0].subJet1.eta() - event.cleanFatJets[0].subJet2.eta()) if hasattr(event.cleanFatJets[0], "subJet2") else -9.
        theH.deltaPhi = deltaPhi(event.cleanFatJets[0].subJet1.phi(), event.cleanFatJets[0].subJet2.phi()) if hasattr(event.cleanFatJets[0], "subJet2") else -9.
        theH.deltaPhi_met = deltaPhi(theH.phi(), event.met.phi())
        theH.deltaPhi_jet1 = deltaPhi(theH.phi(), event.cleanFatJets[0].phi())
        event.H = theH
        
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
        
        # Higgs candidate
        theH = event.cleanJets[0].p4() + event.cleanJets[1].p4()
        theH.charge = event.cleanJets[0].charge() + event.cleanJets[1].charge()
        theH.deltaR = deltaR(event.cleanJets[0].eta(), event.cleanJets[0].phi(), event.cleanJets[1].eta(), event.cleanJets[1].phi())
        theH.deltaEta = abs(event.cleanJets[0].eta() - event.cleanJets[1].eta())
        theH.deltaPhi = deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi())
        theH.deltaPhi_met = deltaPhi(theH.phi(), event.met.phi())
        theH.deltaPhi_jet1 = deltaPhi(theH.phi(), event.cleanJets[0].phi())
        event.H = theH
        
        return True
    
    
    def selectMonoJet(self, event):
        if not len(event.cleanJets) >= 1:
            return False
        if not event.cleanJets[0].pt() > self.cfg_ana.jet1_pt:
            return False
        #if not event.cleanJets[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.jet1_tag:
        #    return False
        
        # Higgs candidate
        theH = event.cleanJets[0].p4()
        theH.charge = event.cleanJets[0].charge()
        theH.deltaR = -1.
        theH.deltaEta = -9.
        theH.deltaPhi = -9.
        theH.deltaPhi_met = -9.
        theH.deltaPhi_jet1 = -9.
        event.H = theH
        
        return True
    
    
    def process(self, event):
        event.Category = 0
        
        self.inputCounter.Fill(0)
        # Trigger
        self.inputCounter.Fill(1)
        
        # Check if there is at least one jet
        if len(event.cleanJets) < 1:
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
    
