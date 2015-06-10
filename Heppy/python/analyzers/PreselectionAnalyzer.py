from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
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
            Labels = ["Trigger", "#Jets > 1", "Jet cuts"]
            self.Counter = ROOT.TH1F("Counter", "Counter", 8, 0, 8)
            for i, l in enumerate(Labels):
                self.Counter.GetXaxis().SetBinLabel(i+1, l)
    
    
    def fillJetVariables(self, event):
        for j in event.Jets + event.cleanJets + event.cleanJetsAK8:
            j.deltaPhi_met = deltaPhi(j.phi(), event.met.phi())
            j.deltaPhi_jet1 = deltaPhi(j.phi(), event.Jets[0].phi())
    
    def fillFatJetVariables(self, event):
        # Add n-subjettiness
        for i, j in enumerate(event.cleanJetsAK8):
            j.tau21 = j.userFloat("NjettinessAK8:tau2")/j.userFloat("NjettinessAK8:tau1") if not j.userFloat("NjettinessAK8:tau1") == 0 else -1.
        
        # Count b-tagged subjets
        for i, j in enumerate(event.cleanJetsAK8):
            nSubJetTags = 0
            subJets = j.subjets('SoftDrop')
            for iw, wsub in enumerate(subJets):
                if iw == 0:
                    j.flavour1 = wsub.hadronFlavour()
                    j.CSV1 = wsub.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')
                    if j.CSV1 > self.cfg_ana.fatjet_tag1:
                        nSubJetTags += 1
                elif iw == 1:
                    j.flavour2 = wsub.hadronFlavour()
                    j.CSV2 = wsub.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')
                    if j.CSV2 > self.cfg_ana.fatjet_tag2:
                        nSubJetTags += 1
            j.nSubJetTags = nSubJetTags
            
    def selectFatJet(self, event):
        if not len(event.cleanJetsAK8) >= 1:
            return False
        if not event.cleanJetsAK8[0].pt() > self.cfg_ana.fatjet_pt: 
            return False
        
        # FatJet selections
        if not event.cleanJetsAK8[0].nSubJetTags >= 2:
            return False
        if not event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) > self.cfg_ana.fatjet_mass:
            return False
        if not hasattr(event.cleanJetsAK8[0], "tau21") or not event.cleanJetsAK8[0].tau21 > self.cfg_ana.fatjet_tau21:
            return False
        
        # Add subjets to the event
        event.SubJets = event.cleanJetsAK8[0].subjets('SoftDrop')
        
        # Higgs candidate
        theV = event.cleanJetsAK8[0].p4()
        theV.charge = event.cleanJetsAK8[0].charge()
        theV.deltaR = deltaR(event.SubJets[0].eta(), event.SubJets[0].phi(), event.SubJets[1].eta(), event.SubJets[1].phi())
        theV.deltaEta = abs(event.SubJets[0].eta() - event.SubJets[1].eta())
        theV.deltaPhi = deltaPhi(event.SubJets[0].phi(), event.SubJets[1].phi())
        theV.deltaPhi_met = deltaPhi(theV.phi(), event.met.phi())
        theV.deltaPhi_jet1 = deltaPhi(theV.phi(), event.cleanJetsAK8[0].phi())
        event.V = theV
        
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
        theV = event.cleanJets[0].p4() + event.cleanJets[1].p4()
        theV.charge = event.cleanJets[0].charge() + event.cleanJets[1].charge()
        theV.deltaR = deltaR(event.cleanJets[0].eta(), event.cleanJets[0].phi(), event.cleanJets[1].eta(), event.cleanJets[1].phi())
        theV.deltaEta = abs(event.cleanJets[0].eta() - event.cleanJets[1].eta())
        theV.deltaPhi = deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi())
        theV.deltaPhi_met = deltaPhi(theV.phi(), event.met.phi())
        theV.deltaPhi_jet1 = deltaPhi(theV.phi(), event.cleanJets[0].phi())
        event.V = theV
        
        return True
    
    
    def selectMonoJet(self, event):
        if not len(event.cleanJets) >= 1:
            return False
        if not event.cleanJets[0].pt() > self.cfg_ana.jet1_pt:
            return False
        #if not event.cleanJets[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.jet1_tag:
        #    return False
        
        # Higgs candidate
        theV = event.cleanJets[0].p4()
        theV.charge = event.cleanJets[0].charge()
        theV.deltaR = -1.
        theV.deltaEta = -9.
        theV.deltaPhi = -9.
        theV.deltaPhi_met = -9.
        theV.deltaPhi_jet1 = -9.
        event.V = theV
        
        return True
    
    
    def process(self, event):
        event.Category = 0
        
        self.Counter.Fill(-1)
        # Trigger
        self.Counter.Fill(0)
        
        # Check if there is at least one jet
        if len(event.cleanJets) < 1:
            return False
        self.Counter.Fill(1)
        
        # Make some interesting things available (tau21, sub-jet b-tagging...)
        self.fillFatJetVariables(event)
        
        # Categorization
        
        # Category 1
        if self.cfg_ana.enableFatJets and self.selectFatJet(event):
            event.Category = 1
        # Category 2
        elif self.selectResolvedJet(event):
            event.Category = 2
        # Category 3
        elif self.selectMonoJet(event):
            event.Category = 3
        else:
            return False
        self.Counter.Fill(2)
        
        # Create final jet list (standard or fat)
        event.Jets = []
        if event.Category == 1:
            event.Jets = event.cleanJetsAK8
        else:
            event.Jets = event.cleanJets
        
        self.fillJetVariables(event)
        
        return True
    
