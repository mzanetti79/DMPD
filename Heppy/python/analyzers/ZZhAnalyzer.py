from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT

class ZZhAnalyzer( Analyzer ):
    '''Analyzer for the Z' -> Zh -> llbb analysis'''

    def beginLoop(self,setup):
        super(ZZhAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            ZZhLabels = ["Trigger", "#Lep #geq 2", "Z cand", "Jet p_{T}", "Z p_{T}", "Z mass", "h mass", "#slash{E}_{T}", "b-tag 1", "b-tag 2"]
            self.ZZhCounter = ROOT.TH1F("ZZhCounter", "ZZhCounter", len(ZZhLabels), 0, len(ZZhLabels))
            for i, l in enumerate(ZZhLabels):
                self.ZZhCounter.GetXaxis().SetBinLabel(i+1, l) 
        
        
    def process(self, event):
        event.isZZh = False
        
#        self.genAnalysis(event)
        
        self.ZZhCounter.Fill(-1) # All
        self.ZZhCounter.Fill(0) # Trigger
        # Leptons >= 2
        if not len(event.inclusiveLeptons)>=2:
            return True
        self.ZZhCounter.Fill(1) # Lep > 2
        # Select first lepton
        if not hasattr(event, "Z"):
            return True
        self.ZZhCounter.Fill(2) # Z cand
        if len(event.cleanJetsAK8)<1 or event.cleanJetsAK8[0].pt() < self.cfg_ana.fatjet_pt:
            return True
        self.ZZhCounter.Fill(3) # Jet pT
        if event.Z.pt() < self.cfg_ana.Z_pt:
            return True
        self.ZZhCounter.Fill(4) # Z pT
        # Fill tree
        event.isZZh = True
        
        
        # Build candidates
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
        event.h = theH
        
        # Zprime candidate
        theA = event.Z + event.h
        theA.charge = event.Z.charge + event.h.charge
        theA.deltaR = deltaR(event.Z.eta(), event.Z.phi(), event.h.eta(), event.h.phi())
        theA.deltaEta = abs(event.Z.eta() - event.h.eta())
        theA.deltaPhi = deltaPhi(event.Z.phi(), event.h.phi())
        theA.deltaPhi_met = deltaPhi(theA.phi(), event.met.phi())
        theA.deltaPhi_jet1 = deltaPhi(theA.phi(), event.h.phi())
        event.A = theA
        
#        for j in event.cleanJetsAK8:
#            j.deltaPhi_met = deltaPhi(j.phi(), event.met.phi())
#            j.deltaPhi_jet1 = deltaPhi(j.phi(), event.cleanJetsAK8[0].phi())
        
        
        
        
        # Estimate cuts
        if event.Z.mass() > self.cfg_ana.Zmass_low and event.Z.mass() < self.cfg_ana.Zmass_high:
            self.ZZhCounter.Fill(5) # Z mass
            if event.cleanJetsAK8[0].userFloat("ak8PFJetsCHSPrunedLinks") > self.cfg_ana.fatJetMass_low and event.cleanJetsAK8[0].userFloat("ak8PFJetsCHSPrunedLinks") < self.cfg_ana.fatJetMass_high:
                self.ZZhCounter.Fill(6) # h mass
                if event.met.pt() < self.cfg_ana.met_pt:
                    self.ZZhCounter.Fill(7) # MET
                    #if event.cleanJetsAK8[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag:
                    if event.cleanJetsAK8[0].nSubJets >= 1 and event.cleanJetsAK8[0].subJet1.btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag_1:
                        self.ZZhCounter.Fill(8) # b-Jet1
                        if event.cleanJetsAK8[0].nSubJets >= 2 and event.cleanJetsAK8[0].subJet2.btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag_2: 
                            self.ZZhCounter.Fill(9) # b-Jet2

        return True

