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
            ZZhLabels = ["Trigger", "Jet p_{T}", "#Lep #geq 2", "Z cand", "Z p_{T}", "Z mass", "b-tag 1", "b-tag 2", "h mass", "#slash{E}_{T}"]
            self.ZZhCounter = ROOT.TH1F("ZZhCounter", "ZZhCounter", len(ZZhLabels), 0, len(ZZhLabels))
            for i, l in enumerate(ZZhLabels):
                self.ZZhCounter.GetXaxis().SetBinLabel(i+1, l)
            
#            self.ZZhGenAmass = ROOT.TH1F("ZZhGenAmass", ";m_{Z'} [GeV]", 1000, 0., 5000.)
#            self.ZZhGenApt = ROOT.TH1F("ZZhGenApt", ";Z' p_{T} [GeV]", 250, 0., 250.)
#            self.ZZhGenAeta = ROOT.TH1F("ZZhGenAeta", ";Z' #eta", 50, -5, 5.)
#            self.ZZhGenZdecay = ROOT.TH1F("ZZhGenZdecay", ";Z daughter pdgId", 25, 0.5, 25.5)
#            self.ZZhGenZmass = ROOT.TH1F("ZZhGenZmass", ";m_{Z} [GeV]", 100, 0., 200.)
#            self.ZZhGenZpt = ROOT.TH1F("ZZhGenZpt", ";Z p_{T} [GeV]", 250, 0., 2500.)
#            self.ZZhGenZeta = ROOT.TH1F("ZZhGenZeta", ";Z #eta", 50, -5, 5.)
#            self.ZZhGenZdR = ROOT.TH1F("ZZhGenZdR", ";Leptons #Delta R", 50, 0, 5.)
#            self.ZZhGenHdecay = ROOT.TH1F("ZZhGenHdecay", ";H daughter pdgId", 25, 0.5, 25.5)
#            self.ZZhGenHmass = ROOT.TH1F("ZZhGenHmass", ";m_{H} [GeV]", 1000, 100., 150.)
#            self.ZZhGenHpt = ROOT.TH1F("ZZhGenHpt", ";H p_{T} [GeV]", 250, 0., 2500.)
#            self.ZZhGenHeta = ROOT.TH1F("ZZhGenHeta", ";H #eta", 50, -5, 5.)
#            self.ZZhGenHdR = ROOT.TH1F("ZZhGenHdR", ";b-quarks #Delta R", 50, 0, 5.)
#            self.ZZhGenLepton1pt = ROOT.TH1F("ZZhGenLepton1pt", ";Lepton 1 p_{T} [GeV]", 100, 0., 2500.)
#            self.ZZhGenLepton1eta = ROOT.TH1F("ZZhGenLepton1eta", ";Lepton 1 #eta", 50, -5, 5.)
#            self.ZZhGenLepton2pt = ROOT.TH1F("ZZhGenLepton2pt", ";Lepton 2 p_{T} [GeV]", 100, 0., 2500.)
#            self.ZZhGenLepton2eta = ROOT.TH1F("ZZhGenLepton2eta", ";Lepton 2 #eta", 50, -5, 5.)
#            self.ZZhGenBquark1pt = ROOT.TH1F("ZZhGenBquark1pt", ";b-quark 1 p_{T} [GeV]", 100, 0., 2500.)
#            self.ZZhGenBquark1eta = ROOT.TH1F("ZZhGenBquark1eta", ";b-quark 1 #eta", 50, -5, 5.)
#            self.ZZhGenBquark2pt = ROOT.TH1F("ZZhGenBquark2pt", ";b-quark 2 p_{T} [GeV]", 100, 0., 2500.)
#            self.ZZhGenBquark2eta = ROOT.TH1F("ZZhGenBquark2eta", ";b-quark 2 #eta", 50, -5, 5.)
#            
#    
#    def genAnalysis(self, event):
#        if not hasattr(event, "genParticles"):
#            return False
#        # Z'
#        for g in event.genParticles:
#            if g.pdgId() == 1023:
#                self.ZZhGenAmass.Fill(g.mass())
#                self.ZZhGenApt.Fill(g.pt())
#                self.ZZhGenAeta.Fill(g.eta())
#        # Z
#        if hasattr(event, "genVBosons"):
#            if len(event.genVBosons) > 0 and event.genVBosons[0].pdgId() == 23:
#                self.ZZhGenZmass.Fill(event.genVBosons[0].mass())
#                self.ZZhGenZpt.Fill(event.genVBosons[0].pt())
#                self.ZZhGenZeta.Fill(event.genVBosons[0].eta())
#        # Higgs
#        if hasattr(event, "genHiggsBosons"):
#            if len(event.genHiggsBosons) > 0:
#                self.ZZhGenHmass.Fill(event.genHiggsBosons[0].mass())
#                self.ZZhGenHpt.Fill(event.genHiggsBosons[0].pt())
#                self.ZZhGenHeta.Fill(event.genHiggsBosons[0].eta())
#        # Leptons from Z
#        if hasattr(event, "genleps"):
#            if len(event.genleps) >= 1:
#                self.ZZhGenZdecay.Fill(abs(event.genleps[0].pdgId()))
#                self.ZZhGenZdR.Fill(deltaR(event.genleps[0].eta(), event.genleps[0].phi(), event.genleps[1].eta(), event.genleps[1].phi()))
#                i1, i2 = [0, 1] if event.genleps[0].pt() > event.genleps[1].pt() else [1, 0]
#                self.ZZhGenLepton1pt.Fill(event.genleps[i1].pt())
#                self.ZZhGenLepton1eta.Fill(event.genleps[i1].eta())
#                self.ZZhGenLepton2pt.Fill(event.genleps[i2].pt())
#                self.ZZhGenLepton2eta.Fill(event.genleps[i2].eta())
#        # b-quarks from Higgs
#        if hasattr(event, "genbquarksFromH"):
#            if len(event.genbquarksFromH) >= 1:
#                self.ZZhGenHdecay.Fill(abs(event.genbquarksFromH[0].pdgId()))
#                self.ZZhGenHdR.Fill(deltaR(event.genbquarksFromH[0].eta(), event.genbquarksFromH[0].phi(), event.genbquarksFromH[1].eta(), event.genbquarksFromH[1].phi()))
#                i1, i2 = [0, 1] if event.genbquarksFromH[0].pt() > event.genbquarksFromH[1].pt() else [1, 0]
#                self.ZZhGenBquark1pt.Fill(event.genbquarksFromH[i1].pt())
#                self.ZZhGenBquark1eta.Fill(event.genbquarksFromH[i1].eta())
#                self.ZZhGenBquark2pt.Fill(event.genbquarksFromH[i2].pt())
#                self.ZZhGenBquark2eta.Fill(event.genbquarksFromH[i2].eta())
        
        
        
    def process(self, event):
        event.isZZh = False
        
        self.genAnalysis(event)
        
        self.ZZhCounter.Fill(-1) # All
        #self.ZZhCounter.Fill(0) # Trigger
        if len(event.cleanFatJets)<1 or event.cleanFatJets[0].pt() < self.cfg_ana.fatjet_pt:
            return True
        self.ZZhCounter.Fill(1) # Jet pT
        # Leptons >= 2
        if not len(event.inclusiveLeptons)>=2:
            return True
        self.ZZhCounter.Fill(2) # Lep > 2
        # Select first lepton
        if not hasattr(event, "Z"):
            return True
        self.ZZhCounter.Fill(3) # Z cand
        if event.Z.pt() < self.cfg_ana.Z_pt:
            return True
        self.ZZhCounter.Fill(4) # Z pT
        # Fill tree
        event.isZZh = True
        
        
        # Build candidates
        # Higgs candidate
        #prunedJet = copy.deepcopy(event.cleanFatJets[0]) # Copy fatJet...
        #prunedJet.setMass(prunedJet.userFloat("ak8PFJetsCHSPrunedLinks")) # ... and set the mass to the pruned mass
        theH = event.cleanFatJets[0]
        theH.charge = event.cleanFatJets[0].charge()
        theH.deltaR = deltaR(event.cleanFatJets[0].subJet1.eta(), event.cleanFatJets[0].subJet1.phi(), event.cleanFatJets[0].subJet2.eta(), event.cleanFatJets[0].subJet2.phi()) if hasattr(event.cleanFatJets[0], "subJet2") else -1.
        theH.deltaEta = abs(event.cleanFatJets[0].subJet1.eta() - event.cleanFatJets[0].subJet2.eta()) if hasattr(event.cleanFatJets[0], "subJet2") else -9.
        theH.deltaPhi = deltaPhi(event.cleanFatJets[0].subJet1.phi(), event.cleanFatJets[0].subJet2.phi()) if hasattr(event.cleanFatJets[0], "subJet2") else -9.
        theH.deltaPhi_met = deltaPhi(theH.phi(), event.met.phi())
        theH.deltaPhi_jet1 = deltaPhi(theH.phi(), event.cleanFatJets[0].phi())
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
        
#        for j in event.cleanFatJets:
#            j.deltaPhi_met = deltaPhi(j.phi(), event.met.phi())
#            j.deltaPhi_jet1 = deltaPhi(j.phi(), event.cleanFatJets[0].phi())
        
        
        
        
        # Estimate cuts
        if event.Z.mass() > self.cfg_ana.Zmass_low and event.Z.mass() < self.cfg_ana.Zmass_high:
            self.ZZhCounter.Fill(5) # Z mass
            #if event.cleanFatJets[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag:
            if event.cleanFatJets[0].nSubJets >= 1 and event.cleanFatJets[0].subJet1.btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag_1:
                self.ZZhCounter.Fill(6) # b-Jet1
                if event.cleanFatJets[0].nSubJets >= 2 and event.cleanFatJets[0].subJet2.btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.fatJet_btag_2: 
                    self.ZZhCounter.Fill(7) # b-Jet2
                    if event.cleanFatJets[0].userFloat("ak8PFJetsCHSPrunedLinks") > self.cfg_ana.fatJetMass_low and event.cleanFatJets[0].userFloat("ak8PFJetsCHSPrunedLinks") < self.cfg_ana.fatJetMass_high:
                        self.ZZhCounter.Fill(8) # h mass
                        if event.met.pt() < self.cfg_ana.met_pt:
                            self.ZZhCounter.Fill(9) # MET

        return True

