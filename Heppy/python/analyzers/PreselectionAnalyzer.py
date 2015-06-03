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
        
            
    def selectFatJet(self, event):
        if not len(event.cleanJetsAK8) >= 1:
            return False
        if not event.cleanJetsAK8[0].pt() > self.cfg_ana.fatjet_pt: 
            return False
        
        
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
        
        # FatJet selections
        if not nSubJetTags >= 2:
            return False
        if not event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) > self.cfg_ana.fatjet_mass:
            return False
        if not hasattr(event.cleanJetsAK8[0], "tau21") or not event.cleanJetsAK8[0].tau21 > self.cfg_ana.fatjet_tau21:
            return False
        
        
        # Higgs candidate
        #prunedJet = copy.deepcopy(event.cleanJetsAK8[0]) # Copy fatJet...
        #prunedJet.setMass(prunedJet.userFloat("ak8PFJetsCHSPrunedLinks")) # ... and set the mass to the pruned mass
        theH = event.cleanJetsAK8[0].p4()
        theH.charge = event.cleanJetsAK8[0].charge()
        theH.deltaR = deltaR(event.cleanJetsAK8[0].subJet1.eta(), event.cleanJetsAK8[0].subJet1.phi(), event.cleanJetsAK8[0].subJet2.eta(), event.cleanJetsAK8[0].subJet2.phi()) if hasattr(event.cleanJetsAK8[0], "subJet2") else -1.
        theH.deltaEta = abs(event.cleanJetsAK8[0].subJet1.eta() - event.cleanJetsAK8[0].subJet2.eta()) if hasattr(event.cleanJetsAK8[0], "subJet2") else -9.
        theH.deltaPhi = deltaPhi(event.cleanJetsAK8[0].subJet1.phi(), event.cleanJetsAK8[0].subJet2.phi()) if hasattr(event.cleanJetsAK8[0], "subJet2") else -9.
        theH.deltaPhi_met = deltaPhi(theH.phi(), event.met.phi())
        theH.deltaPhi_jet1 = deltaPhi(theH.phi(), event.cleanJetsAK8[0].phi())
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
        
        self.Counter.Fill(-1)
        # Trigger
        self.Counter.Fill(0)
        
        # Check if there is at least one jet
        if len(event.cleanJets) < 1:
            return False
        self.Counter.Fill(1)
        
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
    
