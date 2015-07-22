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
        if len(event.cleanJetsAK8)<1 or event.cleanJetsAK8[0].pt() < self.cfg_ana.fatjet_pt or len(event.cleanJetsAK8[0].subjets('SoftDrop')) < 2:
            return True
        self.ZZhCounter.Fill(3) # Jet pT
        if event.Z.pt() < self.cfg_ana.Z_pt:
            return True
        self.ZZhCounter.Fill(4) # Z pT
        # Fill tree
        event.isZZh = True
        
        
        # Build candidates
        if not hasattr(event, "SubJets"): event.SubJets = event.cleanJetsAK8[0].subjets('SoftDrop')
        
        # Higgs candidate
        theH = event.cleanJetsAK8[0].p4()
        theH.charge = event.cleanJetsAK8[0].charge()
        theH.deltaR = deltaR(event.SubJets[0].eta(), event.SubJets[0].phi(), event.SubJets[1].eta(), event.SubJets[1].phi())
        theH.deltaEta = abs(event.SubJets[0].eta() - event.SubJets[1].eta())
        theH.deltaPhi = deltaPhi(event.SubJets[0].phi(), event.SubJets[1].phi())
        theH.deltaPhi_met = deltaPhi(theH.phi(), event.met.phi())
        theH.deltaPhi_jet1 = deltaPhi(theH.phi(), event.cleanJetsAK8[0].phi())
        event.H = theH
        
        # Zprime candidate
        theA = event.Z + event.H
        theA.charge = event.Z.charge + event.H.charge
        theA.deltaR = deltaR(event.Z.eta(), event.Z.phi(), event.H.eta(), event.H.phi())
        theA.deltaEta = abs(event.Z.eta() - event.H.eta())
        theA.deltaPhi = deltaPhi(event.Z.phi(), event.H.phi())
        theA.deltaPhi_met = deltaPhi(theA.phi(), event.met.phi())
        theA.deltaPhi_jet1 = deltaPhi(theA.phi(), event.H.phi())
        event.A = theA
        
        for j in event.cleanJetsAK8:
            j.deltaPhi_met = deltaPhi(j.phi(), event.met.phi())
            j.deltaPhi_jet1 = deltaPhi(j.phi(), event.cleanJetsAK8[0].phi())
        
        # Estimate cuts
        if event.Z.mass() > self.cfg_ana.Zmass_low and event.Z.mass() < self.cfg_ana.Zmass_high:
            self.ZZhCounter.Fill(5) # Z mass
            if event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) > self.cfg_ana.fatjet_mass_low and event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) < self.cfg_ana.fatjet_mass_high:
                self.ZZhCounter.Fill(6) # h mass
                if event.met.pt() < self.cfg_ana.met_pt:
                    self.ZZhCounter.Fill(7) # MET
                    #if event.cleanJetsAK8[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag:
                    if event.cleanJetsAK8[0].subjets('SoftDrop')[0].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatjet_btag_1:
                        self.ZZhCounter.Fill(8) # b-Jet1
                        if event.cleanJetsAK8[0].subjets('SoftDrop')[1].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatjet_btag_2: 
                            self.ZZhCounter.Fill(9) # b-Jet2

        return True

