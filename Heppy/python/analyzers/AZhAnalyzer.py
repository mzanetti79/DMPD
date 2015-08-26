from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT
from array import array

class AZhAnalyzer( Analyzer ):
    '''Analyzer for the Z' -> Zh -> (ll/nunu)bb analysis'''

    def beginLoop(self, setup):
        super(AZhAnalyzer, self).beginLoop(setup)
        self.Hist = {}
        
        Z2LLlabels = ["Trigger", "Lep #geq 2", "Lep Id", "Lep Iso", "Z cand", "Z mass", "Z p_{T}", "Jet p_{T}", "h mass", "b-tag 1", "b-tag 2"]
        Z2NNlabels = ["Trigger", "e/#mu veto", "Jet p_{T}", "#slash{E}_{T}", "#Delta #varphi > 2.5", "h mass", "b-tag 1", "b-tag 2"]
        HEEPlabels = ["isEcalDriven", "#Delta #eta_{in}^{seed}", "#Delta #varphi_{in}", "H/E", "E^{2x5}/E^{5x5}", "Lost Hits", "|d_{xy}|"]
        pTbins = [0., 5., 10., 15., 20., 25., 30., 35., 40., 45., 50., 60., 70., 80., 90., 100., 110., 120., 130., 150., 175., 200., 225., 250., 300., 350., 400., 500., 750., 1000., 1250., 1500., 2000., 2500.]
        dRbins = [0., 0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.75, 1.0]
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd("Counters")
            self.Hist["Z2EECounter"] = ROOT.TH1F("ZtoEECounter", "", len(Z2LLlabels), 0, len(Z2LLlabels))
            self.Hist["Z2MMCounter"] = ROOT.TH1F("ZtoMMCounter", "", len(Z2LLlabels), 0, len(Z2LLlabels))
            self.Hist["Z2NNCounter"] = ROOT.TH1F("ZtoNNCounter", "", len(Z2NNlabels), 0, len(Z2NNlabels))
            for i, l in enumerate(Z2LLlabels):
                self.Hist["Z2EECounter"].GetXaxis().SetBinLabel(i+1, l)
                self.Hist["Z2MMCounter"].GetXaxis().SetBinLabel(i+1, l)
            for i, l in enumerate(Z2NNlabels):
                self.Hist["Z2NNCounter"].GetXaxis().SetBinLabel(i+1, l)
            setup.services["outputfile"].file.cd("..")
            #
            setup.services["outputfile"].file.mkdir("Leptons")
            setup.services["outputfile"].file.cd("Leptons")
            self.Hist["ElecBarrelHEEP"] = ROOT.TH1F("ElecBarrelHEEP", ";;Events", len(HEEPlabels), 0, len(HEEPlabels))
            self.Hist["ElecEndcapHEEP"] = ROOT.TH1F("ElecEndcapHEEP", ";;Events", len(HEEPlabels), 0, len(HEEPlabels))
            for i, l in enumerate(HEEPlabels):
                self.Hist["ElecBarrelHEEP"].GetXaxis().SetBinLabel(i+1, l)
                self.Hist["ElecEndcapHEEP"].GetXaxis().SetBinLabel(i+1, l)
            self.Hist["ElecEndcapHEEP"].GetXaxis().SetBinLabel(5, "#sigma_{i#eta i#eta}")
            for i, n in enumerate(["ElecPt", "MuonPt"]):
                self.Hist[n] = ROOT.TH1F(n, ";Lepton p_{T} (GeV);Events", len(pTbins)-1, array('f', pTbins))
            for i, n in enumerate(["ElecEta", "MuonEta"]):
                self.Hist[n] = ROOT.TH1F(n, ";Lepton #eta;Events", 60, -3., 3.)
            for i, n in enumerate(["ElecZdR", "MuonZdR"]):
                self.Hist[n] = ROOT.TH1F(n, ";gen #Delta R;Events", len(dRbins)-1, array('f', dRbins))
            setup.services["outputfile"].file.cd("..")
            #
            setup.services["outputfile"].file.mkdir("Eff")
            setup.services["outputfile"].file.cd("Eff")
            self.Hist["EffElecBarrelHEEP"] = ROOT.TH1F("EffElecBarrelHEEP", ";;Efficiency", len(HEEPlabels), 0, len(HEEPlabels))
            self.Hist["EffElecEndcapHEEP"] = ROOT.TH1F("EffElecEndcapHEEP", ";;Efficiency", len(HEEPlabels), 0, len(HEEPlabels))
            for i, l in enumerate(HEEPlabels):
                self.Hist["EffElecBarrelHEEP"].GetXaxis().SetBinLabel(i+1, l)
                self.Hist["EffElecEndcapHEEP"].GetXaxis().SetBinLabel(i+1, l)
            self.Hist["EffElecEndcapHEEP"].GetXaxis().SetBinLabel(5, "#sigma_{i#eta i#eta}")
            for i, n in enumerate(["EffElecPt_HEEP", "EffMuonPt_Highpt"]):
                self.Hist[n] = ROOT.TH1F(n, ";Lepton p_{T} (GeV);Efficiency", len(pTbins)-1, array('f', pTbins))
            for i, n in enumerate(["EffElecEta_HEEP", "EffMuonEta_Highpt"]):
                self.Hist[n] = ROOT.TH1F(n, ";Lepton #eta;Efficiency", 60, -3., 3.)
            for i, n in enumerate(["EffElecZdR", "EffElecZdR_Loose", "EffElecZdR_Loose_pfIso", "EffElecZdR_Loose_miniIso", "EffElecZdR_Tight", "EffElecZdR_HEEP", "EffElecZdR_HEEP_pfIso", "EffElecZdR_HEEP_miniIso", "EffMuonZdR", "EffMuonZdR_TrackerTracker", "EffMuonZdR_TrackerTracker_pfIso", "EffMuonZdR_TrackerTracker_miniIso", "EffMuonZdR_LooseLoose", "EffMuonZdR_LooseLoose_pfIso", "EffMuonZdR_LooseLoose_miniIso", "EffMuonZdR_HighptTracker", "EffMuonZdR_HighptTracker_pfIso", "EffMuonZdR_HighptTracker_miniIso", "EffMuonZdR_HighptLoose", "EffMuonZdR_HighptLoose_pfIso", "EffMuonZdR_HighptLoose_miniIso", "EffMuonZdR_HighptHighpt", "EffMuonZdR_TightTight"]):
                self.Hist[n] = ROOT.TH1F(n, ";gen #Delta R;Efficiency", len(dRbins)-1, array('f', dRbins))
            # Set Sumw2
            for n, h in self.Hist.iteritems():
                h.Sumw2()

            
    def endLoop(self, setup):
        for n, h in self.Hist.iteritems():
            if n.startswith("Eff"): h.Divide(self.Hist[ n.split("_", 1)[0].replace("Eff", "") ])
#        name = h.split("_", 1)[0].replace("Eff", "")
#        self.Hist["EffElecBarrelHEEP"].Divide(self.Hist["ElecBarrelHEEP"])
#        self.Hist["EffElecEndcapHEEP"].Divide(self.Hist["ElecEndcapHEEP"])
#        self.Hist["EffElecPt_HEEP"].Divide(self.Hist["ElecPt"])
#        self.Hist["EffElecEta_HEEP"].Divide(self.Hist["ElecEta"])
#        self.Hist["EffElecZdR"].Divide(self.Hist["ElecZdR"])
#        self.Hist["EffElecZdR_Loose"].Divide(self.Hist["ElecZdR"])
#        self.Hist["EffElecZdR_Tight"].Divide(self.Hist["ElecZdR"])
#        self.Hist["EffElecZdR_HEEP"].Divide(self.Hist["ElecZdR"])
#        self.Hist["EffElecZdR_HEEP_pfIso"].Divide(self.Hist["ElecZdR"])
#        self.Hist["EffElecZdR_HEEP_miniIso"].Divide(self.Hist["ElecZdR"])
#        self.Hist["EffMuonPt_Highpt"].Divide(self.Hist["MuonPt"])
#        self.Hist["EffMuonEta_Highpt"].Divide(self.Hist["MuonEta"])
#        self.Hist["EffMuonZdR"].Divide(self.Hist["MuonZdR"])
#        self.Hist["EffMuonZdR_Tracker_Tracker"].Divide(self.Hist["MuonZdR"])
#        self.Hist["EffMuonZdR_Loose_Loose"].Divide(self.Hist["MuonZdR"])
#        self.Hist["EffMuonZdR_Highpt_Tracker"].Divide(self.Hist["MuonZdR"])
#        self.Hist["EffMuonZdR_Highpt_Loose"].Divide(self.Hist["MuonZdR"])
#        self.Hist["EffMuonZdR_Highpt_Highpt"].Divide(self.Hist["MuonZdR"])
#        self.Hist["EffMuonZdR_Tight_Tight"].Divide(self.Hist["MuonZdR"])
        
        
        
    def fillGenPlots(self, event):
        if hasattr(event, "genleps") and len(event.genleps) >= 2:
            i1, i2 = [0, 1] if event.genleps[0].pt() > event.genleps[1].pt() else [1, 0]
            l1, l2 = -1, -1
            genZdR = deltaR(event.genleps[i1].eta(), event.genleps[i1].phi(), event.genleps[i2].eta(), event.genleps[i2].phi())
            # Electrons
            if abs(event.genleps[0].pdgId())==11:
                for i, l in enumerate(event.inclusiveLeptons):
                    if l.isElectron() and deltaR(l.eta(), l.phi(), event.genleps[i1].eta(), event.genleps[i1].phi())<0.1 and abs(1-l.pt()/event.genleps[i1].pt()) < 0.3: l1 = i
                    elif l.isElectron() and deltaR(l.eta(), l.phi(), event.genleps[i2].eta(), event.genleps[i2].phi())<0.1 and abs(1-l.pt()/event.genleps[i2].pt()) < 0.3: l2 = i
                if l1 >= 0 and l2 >= 0 and event.genleps[i1].pt() > self.cfg_ana.elec1pt and event.genleps[i2].pt() > self.cfg_ana.elec2pt:
                    pfIso = event.inclusiveLeptons[l1].relIso04<0.20 and event.inclusiveLeptons[l2].relIso04<0.20
                    miniIso = event.inclusiveLeptons[l1].miniRelIso<0.1 and event.inclusiveLeptons[l2].miniRelIso<0.1
                    self.Hist["ElecPt"].Fill(event.genleps[i1].pt())
                    self.Hist["ElecPt"].Fill(event.genleps[i2].pt())
                    self.Hist["ElecEta"].Fill(event.genleps[i1].eta())
                    self.Hist["ElecEta"].Fill(event.genleps[i2].eta())
                    self.Hist["ElecZdR"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].isHEEP:
                        self.Hist["EffElecPt_HEEP"].Fill(event.genleps[i1].pt())
                        self.Hist["EffElecEta_HEEP"].Fill(event.genleps[i1].eta())
                    if event.inclusiveLeptons[l2].isHEEP:
                        self.Hist["EffElecPt_HEEP"].Fill(event.genleps[i2].pt())
                        self.Hist["EffElecEta_HEEP"].Fill(event.genleps[i2].eta())
                    # deltaR
                    self.Hist["EffElecZdR"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].isHEEP and event.inclusiveLeptons[l2].isHEEP:
                        self.Hist["EffElecZdR_HEEP"].Fill(genZdR)
                        if pfIso: self.Hist["EffElecZdR_HEEP_pfIso"].Fill(genZdR)
                        if miniIso: self.Hist["EffElecZdR_HEEP_miniIso"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].electronID('POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Loose') and event.inclusiveLeptons[l2].electronID('POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Loose'):
                        self.Hist["EffElecZdR_Loose"].Fill(genZdR)
                        if pfIso: self.Hist["EffElecZdR_Loose_pfIso"].Fill(genZdR)
                        if miniIso: self.Hist["EffElecZdR_Loose_miniIso"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].electronID('POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Tight') and event.inclusiveLeptons[l2].electronID('POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Tight'):
                        self.Hist["EffElecZdR_Tight"].Fill(genZdR)
                    
                
            # Muons
            if abs(event.genleps[0].pdgId())==13:
                for i, l in enumerate(event.inclusiveLeptons):
                    if l.isMuon() and deltaR(l.eta(), l.phi(), event.genleps[i1].eta(), event.genleps[i1].phi())<0.1 and abs(1-l.pt()/event.genleps[i1].pt()) < 0.3: l1 = i
                    elif l.isMuon() and deltaR(l.eta(), l.phi(), event.genleps[i2].eta(), event.genleps[i2].phi())<0.1 and abs(1-l.pt()/event.genleps[i2].pt()) < 0.3: l2 = i
                if l1 >= 0 and l2 >= 0 and event.genleps[i1].pt() > self.cfg_ana.muon1pt and event.genleps[i2].pt() > self.cfg_ana.muon2pt:
                    pfIso = event.inclusiveLeptons[l1].relIso04<0.20 and event.inclusiveLeptons[l2].relIso04<0.20
                    miniIso = event.inclusiveLeptons[l1].miniRelIso<0.1 and event.inclusiveLeptons[l2].miniRelIso<0.1
                    self.Hist["MuonPt"].Fill(event.genleps[i1].pt())
                    self.Hist["MuonPt"].Fill(event.genleps[i2].pt())
                    self.Hist["MuonEta"].Fill(event.genleps[i1].eta())
                    self.Hist["MuonEta"].Fill(event.genleps[i2].eta())
                    self.Hist["MuonZdR"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].muonID("POG_ID_HighPt"):
                        self.Hist["EffMuonPt_Highpt"].Fill(event.genleps[i1].pt())
                        self.Hist["EffMuonEta_Highpt"].Fill(event.genleps[i1].eta())
                    if event.inclusiveLeptons[l2].muonID("POG_ID_HighPt"):
                        self.Hist["EffMuonPt_Highpt"].Fill(event.genleps[i2].pt())
                        self.Hist["EffMuonEta_Highpt"].Fill(event.genleps[i2].eta())
                    # deltaR
                    self.Hist["EffMuonZdR"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].isTrackerMuon() and event.inclusiveLeptons[l2].isTrackerMuon():
                        self.Hist["EffMuonZdR_TrackerTracker"].Fill(genZdR)
                        if pfIso: self.Hist["EffMuonZdR_TrackerTracker_pfIso"].Fill(genZdR)
                        if miniIso: self.Hist["EffMuonZdR_TrackerTracker_miniIso"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].muonID("POG_ID_Loose") and event.inclusiveLeptons[l2].muonID("POG_ID_Loose"):
                        self.Hist["EffMuonZdR_LooseLoose"].Fill(genZdR)
                        if pfIso: self.Hist["EffMuonZdR_LooseLoose_pfIso"].Fill(genZdR)
                        if miniIso: self.Hist["EffMuonZdR_LooseLoose_miniIso"].Fill(genZdR)
                    if (event.inclusiveLeptons[l1].muonID("POG_ID_HighPt") or event.inclusiveLeptons[l2].muonID("POG_ID_HighPt")) and event.inclusiveLeptons[l1].isTrackerMuon() and event.inclusiveLeptons[l2].isTrackerMuon():
                        self.Hist["EffMuonZdR_HighptTracker"].Fill(genZdR)
                        if pfIso: self.Hist["EffMuonZdR_HighptTracker_pfIso"].Fill(genZdR)
                        if miniIso: self.Hist["EffMuonZdR_HighptTracker_miniIso"].Fill(genZdR)
                    if (event.inclusiveLeptons[l1].muonID("POG_ID_HighPt") or event.inclusiveLeptons[l2].muonID("POG_ID_HighPt")) and event.inclusiveLeptons[l1].muonID("POG_ID_Loose") and event.inclusiveLeptons[l2].muonID("POG_ID_Loose"):
                        self.Hist["EffMuonZdR_HighptLoose"].Fill(genZdR)
                        if pfIso: self.Hist["EffMuonZdR_HighptLoose_pfIso"].Fill(genZdR)
                        if miniIso: self.Hist["EffMuonZdR_HighptLoose_miniIso"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].muonID("POG_ID_HighPt") and event.inclusiveLeptons[l2].muonID("POG_ID_HighPt"): self.Hist["EffMuonZdR_HighptHighpt"].Fill(genZdR)
                    if event.inclusiveLeptons[l1].muonID("POG_ID_Tight") and event.inclusiveLeptons[l2].muonID("POG_ID_Tight"): self.Hist["EffMuonZdR_TightTight"].Fill(genZdR)

    
    
    def addFakeMet(self, event, particles):
        # Copy regular met
        event.fakemet = copy.deepcopy(event.met)
        px, py = event.met.px(), event.met.py()
        for i, p in enumerate(particles):
            if not p:
                continue
            else:
                px += p.px()
                py += p.py()
        
        event.fakemet.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px, py)))
        return True
    
    
    
    def isHEEP(self, e, doPlot=True):
        e.isHEEP = False
        if not e.isElectron() or not e.et() > 35.: return False
        
        # Plot
        if doPlot:
            if abs(e.superCluster().eta()) < 1.4442:
                for i in range(self.Hist["ElecBarrelHEEP"].GetNbinsX()): self.Hist["ElecBarrelHEEP"].AddBinContent(i+1)
                if e.ecalDrivenSeed(): self.Hist["EffElecBarrelHEEP"].AddBinContent(1)
                if abs(e.deltaEtaSeedClusterTrackAtVtx()) < 0.004: self.Hist["EffElecBarrelHEEP"].AddBinContent(2)
                if abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: self.Hist["EffElecBarrelHEEP"].AddBinContent(3)
                if e.hadronicOverEm() < 1./e.energy() + 0.05: self.Hist["EffElecBarrelHEEP"].AddBinContent(4)
                if (e.e2x5Max()/e.e5x5() > 0.94 or e.e1x5()/e.e5x5() > 0.83): self.Hist["EffElecBarrelHEEP"].AddBinContent(5)
                if e.lostInner() <= 1: self.Hist["EffElecBarrelHEEP"].AddBinContent(6)
                if abs(e.dxy()) < 0.02: self.Hist["EffElecBarrelHEEP"].AddBinContent(7)
            elif abs(e.superCluster().eta()) > 1.566 and abs(e.superCluster().eta()) < 2.5:
                for i in range(self.Hist["ElecEndcapHEEP"].GetNbinsX()): self.Hist["ElecEndcapHEEP"].AddBinContent(i+1)
                if e.ecalDrivenSeed(): self.Hist["EffElecEndcapHEEP"].AddBinContent(1)
                if abs(e.deltaEtaSeedClusterTrackAtVtx()) < 0.006: self.Hist["EffElecEndcapHEEP"].AddBinContent(2)
                if abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: self.Hist["EffElecEndcapHEEP"].AddBinContent(3)
                if e.hadronicOverEm() < 5./e.energy() + 0.05: self.Hist["EffElecEndcapHEEP"].AddBinContent(4)
                if e.sigmaIetaIeta() < 0.03: self.Hist["EffElecEndcapHEEP"].AddBinContent(5)
                if e.lostInner() <= 1: self.Hist["EffElecEndcapHEEP"].AddBinContent(6)
                if abs(e.dxy()) < 0.05: self.Hist["EffElecEndcapHEEP"].AddBinContent(7)
        
        
        if abs(e.superCluster().eta()) < 1.4442:
            if not e.ecalDrivenSeed(): return False
            if not abs(e.deltaEtaSeedClusterTrackAtVtx()) < 0.004: return False
            if not abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: return False
            if not e.hadronicOverEm() < 1./e.energy() + 0.05: return False
            if not (e.e2x5Max()/e.e5x5() > 0.94 or e.e1x5()/e.e5x5() > 0.83): return False
            if not e.lostInner() <= 1: return False
            if not abs(e.dxy()) < 0.02: return False
        elif abs(e.superCluster().eta()) > 1.566 and abs(e.superCluster().eta()) < 2.5:
            if not e.ecalDrivenSeed(): return False
            if not abs(e.deltaEtaSeedClusterTrackAtVtx()) < 0.006: return False
            if not abs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06: return False
            if not e.hadronicOverEm() < 5./e.energy() + 0.05: return False
            if not e.sigmaIetaIeta() < 0.03: return False
            if not e.lostInner() <= 1: return False
            if not abs(e.dxy()) < 0.05: return False
        else:
            return False
        
        e.isHEEP = True
        return True
    
    
    def process(self, event):
        event.isAZh = False
        event.isZ2EE = False
        event.isZ2MM = False
        event.isZ2NN = False
        event.highptFatJets = [] #ROOT.pat.Jet()
        event.Z = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
        event.A = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
        event.fakemet = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
        
         # All
        self.Hist["Z2EECounter"].AddBinContent(0)
        self.Hist["Z2MMCounter"].AddBinContent(0)
        self.Hist["Z2NNCounter"].AddBinContent(0)
        
        ### Preliminary operations ###
        # Attach electron HEEP Id
        for i, l in enumerate(event.inclusiveLeptons): self.isHEEP(l)
        self.fillGenPlots(event)
        
        # Trigger
        if event.HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v: self.Hist["Z2EECounter"].AddBinContent(1)
        if event.HLT_BIT_HLT_Mu45_eta2p1_v: self.Hist["Z2MMCounter"].AddBinContent(1)
        if event.HLT_BIT_HLT_PFMET170_NoiseCleaned_v: self.Hist["Z2NNCounter"].AddBinContent(1)
        
        #########################
        #    Part 1: Leptons    #
        #########################
        
        
        
        # Lepton collections
        if len([x for x in event.inclusiveLeptons if x.isElectron()]) >= 2 and event.inclusiveLeptons[0].pt() > self.cfg_ana.elec1pt and event.inclusiveLeptons[1].pt() > self.cfg_ana.elec2pt: self.Hist["Z2EECounter"].AddBinContent(2)
        elif len([x for x in event.inclusiveLeptons if x.isMuon()]) >= 2 and event.inclusiveLeptons[0].pt() > self.cfg_ana.muon1pt and event.inclusiveLeptons[1].pt() > self.cfg_ana.muon2pt: self.Hist["Z2MMCounter"].AddBinContent(2)
        
        # Id
        event.highptIdElectrons = [x for x in event.inclusiveLeptons if x.isElectron() and self.isHEEP(x)] # and self.isHEEP(x) and x.miniRelIso<0.1  and x.electronID('POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Loose')
        event.highptIdMuons = [x for x in event.inclusiveLeptons if x.isMuon() and x.isTrackerMuon()] #x.isTrackerMuon() and x.miniRelIso<0.1  and x.muonID("POG_ID_Loose")
        
        if len(event.highptIdElectrons) >= 2 and event.highptIdElectrons[0].pt() > self.cfg_ana.elec1pt and event.highptIdElectrons[1].pt() > self.cfg_ana.elec2pt: self.Hist["Z2EECounter"].AddBinContent(3)
        if len(event.highptIdMuons) >= 2 and event.highptIdMuons[0].pt() > self.cfg_ana.muon1pt and event.highptIdMuons[1].pt() > self.cfg_ana.muon2pt: self.Hist["Z2MMCounter"].AddBinContent(3)
        
        # Iso
        event.highptIdIsoElectrons = [x for x in event.highptIdElectrons if x.miniRelIso<0.1]
        event.highptIdIsoMuons = [x for x in event.highptIdMuons if x.miniRelIso<0.1]
        
        if len(event.highptIdIsoElectrons) >= 2 and event.highptIdIsoElectrons[0].pt() > self.cfg_ana.elec1pt and event.highptIdIsoElectrons[1].pt() > self.cfg_ana.elec2pt: self.Hist["Z2EECounter"].AddBinContent(4)
        if len(event.highptIdIsoMuons) >= 2 and event.highptIdIsoMuons[0].pt() > self.cfg_ana.muon1pt and event.highptIdIsoMuons[1].pt() > self.cfg_ana.muon2pt: self.Hist["Z2MMCounter"].AddBinContent(4)
        
        #for i, m in enumerate(event.highptMuons):
        #    if m.muonID("POG_ID_HighPt"): m.setP4( m.tunePMuonBestTrack().get().p4() )
        
        event.highptLeptons = []
        event.highptIdIsoElectrons.sort(key = lambda l : l.pt(), reverse = True)
        event.highptIdIsoMuons.sort(key = lambda l : l.pt(), reverse = True)
        
        
        # Categorization
        if len(event.highptIdIsoElectrons) >= 2 and event.highptIdIsoElectrons[0].pt() > self.cfg_ana.elec1pt and event.highptIdIsoElectrons[1].pt() > self.cfg_ana.elec2pt:
            event.highptLeptons = event.highptIdIsoElectrons
            self.Hist["Z2EECounter"].AddBinContent(5)
            event.isZ2EE = True
        elif len(event.highptIdIsoMuons) >= 2 and event.highptIdIsoMuons[0].pt() > self.cfg_ana.muon1pt and event.highptIdIsoMuons[1].pt() > self.cfg_ana.muon2pt:
            event.highptLeptons = event.highptIdIsoMuons
            self.Hist["Z2MMCounter"].AddBinContent(5)
            event.isZ2MM = True
        elif len(event.highptIdIsoElectrons) + len(event.highptIdIsoMuons) == 0:
            self.Hist["Z2NNCounter"].AddBinContent(2)
            event.isZ2NN = True
        else:
            return True
        event.isZ2LL = event.isZ2EE or event.isZ2MM
        
        # Z candidate
        if event.isZ2LL:
            event.Z = event.highptLeptons[0].p4() + event.highptLeptons[1].p4()
            event.Z.charge = event.highptLeptons[0].charge() + event.highptLeptons[1].charge()
            event.Z.deltaR = deltaR(event.highptLeptons[0].eta(), event.highptLeptons[0].phi(), event.highptLeptons[1].eta(), event.highptLeptons[1].phi())
            event.Z.deltaEta = abs(event.highptLeptons[0].eta() - event.highptLeptons[1].eta())
            event.Z.deltaPhi = deltaPhi(event.highptLeptons[0].phi(), event.highptLeptons[1].phi())
            # Z candidate
            if event.Z.mass() < 50. or event.highptLeptons[0].charge() != event.highptLeptons[1].charge():
                return True
            if event.isZ2EE: self.Hist["Z2EECounter"].AddBinContent(6)
            if event.isZ2MM: self.Hist["Z2MMCounter"].AddBinContent(6)
            # Z mass
            if event.Z.mass() < 70 or event.Z.mass() > 110:
                return True
            # Z pt
            if event.isZ2EE: self.Hist["Z2EECounter"].AddBinContent(7)
            if event.isZ2MM: self.Hist["Z2MMCounter"].AddBinContent(7)
            if event.Z.pt() < self.cfg_ana.Z_pt:
                return True
            if event.isZ2EE: self.Hist["Z2EECounter"].AddBinContent(8)
            if event.isZ2MM: self.Hist["Z2MMCounter"].AddBinContent(8)
        
        event.isAZh = True
        
        #########################
        #    Part 2: Jets       #
        #########################
        
        for i, j in enumerate(event.cleanJetsAK8):
            if j.pt() >= self.cfg_ana.fatjet_pt:
                if not event.isZ2LL or (event.isZ2LL and ( deltaR(event.highptLeptons[0].eta(), event.highptLeptons[0].phi(), j.eta(), j.phi()) > 0.8 and deltaR(event.highptLeptons[1].eta(), event.highptLeptons[1].phi(), j.eta(), j.phi()) > 0.8 ) ):
                    event.highptFatJets.append(j)
        event.highptFatJets.sort(key = lambda j : j.pt(), reverse = True) #j.userFloat(self.cfg_ana.jetAlgo)

        if len(event.highptFatJets) < 1:
            return True
        
        if event.isZ2EE: self.Hist["Z2EECounter"].AddBinContent(9)
        if event.isZ2MM: self.Hist["Z2MMCounter"].AddBinContent(9)
        if event.isZ2NN: self.Hist["Z2NNCounter"].AddBinContent(3)
        
        
        #########################
        #   Part 3: Candidates  #
        #########################
        
        # h candidate with pseudo-kin fit
        kH = event.highptFatJets[0].p4()
        k = 125.0/event.highptFatJets[0].mass() if event.highptFatJets[0].mass() > 0 else 0. #.userFloat("ak8PFJetsCHSSoftDropMass")
        kH = ROOT.reco.Particle.LorentzVector(event.highptFatJets[0].px()*k, event.highptFatJets[0].py()*k, event.highptFatJets[0].pz()*k, event.highptFatJets[0].energy()*k)
        
        # A/Z' candidate
        if event.isZ2LL:
            event.A = event.Z + event.highptFatJets[0].p4()
            event.A.mT = event.A.mass()
            event.A.mC = event.A.mass()
            event.A.mK = (event.Z + kH).mass()
            event.A.deltaR = deltaR(event.Z.eta(), event.Z.phi(), event.highptFatJets[0].eta(), event.highptFatJets[0].phi())
            event.A.deltaEta = abs(event.Z.eta() - event.highptFatJets[0].eta())
            event.A.deltaPhi = deltaPhi(event.Z.phi(), event.highptFatJets[0].phi())
        elif len(event.highptLeptons) == 1:
            event.A = event.highptLeptons[0].p4() + event.met.p4() + event.highptFatJets[0].p4()
            pz = 0.
            a = 80.4**2 - event.highptLeptons[0].mass()**2 + 2.*event.highptLeptons[0].px()*event.met.px() + 2.*event.highptLeptons[0].py()*event.met.py()
            A = 4*( event.highptLeptons[0].energy()**2 - event.highptLeptons[0].pz()**2 )
            B = -4*a*event.highptLeptons[0].pz()
            C = 4*event.highptLeptons[0].energy()**2 * (event.met.px()**2  + event.met.py()**2) - a**2
            D = B**2 - 4*A*C
            if D>0:
                pz = min((-B+math.sqrt(D))/(2*A), (-B-math.sqrt(D))/(2*A))
            else:
                pz = -B/(2*A)
            kmet = event.met.p4()
            kmet.SetPz(pz)
            event.A.mT = (event.highptLeptons[0].p4() + kmet + event.highptFatJets[0].p4()).mass()
            cmet = event.met.p4()
            cmet.SetPz(event.highptLeptons[0].pz())
            event.A.mC = (event.highptLeptons[0].p4() + cmet + event.highptFatJets[0].p4()).mass()
            event.A.mK = (event.highptLeptons[0].p4() + kmet + kH).mass()
        else:
            event.A = event.met.p4() + event.highptFatJets[0].p4()
            event.A.mT = math.sqrt( 2.*event.highptFatJets[0].energy()*event.met.pt()*(1.-math.cos( deltaPhi(event.highptFatJets[0].phi(), event.met.phi()) )) )
            cmet = event.met.p4()
            cmet.SetPz( -event.highptFatJets[0].pz() )
            event.A.mC = (cmet + event.highptFatJets[0].p4()).mass()
            event.A.mK = math.sqrt( 2.*kH.energy()*event.met.pt()*(1.-math.cos( deltaPhi(kH.phi(), event.met.phi()) )) )
        
        if event.isZ2LL:
            self.addFakeMet(event, [event.highptLeptons[0], event.highptLeptons[1]])
        else:
            self.addFakeMet(event, [])
        
        if (event.isZ2LL and event.Z.pt() < self.cfg_ana.Z_pt) or (event.isZ2NN and event.met.pt() < self.cfg_ana.met_pt):
            return True
        
        
        # Fill tree
        event.isAZh = True
        
        # ---------- Estimate cuts ----------
        
        if event.isZ2LL: 
            if event.highptFatJets[0].userFloat(self.cfg_ana.jetAlgo) > 95 and event.highptFatJets[0].userFloat(self.cfg_ana.jetAlgo) < 130:
                self.Hist["Z2EECounter"].AddBinContent(10) if event.isZ2EE else self.Hist["Z2MMCounter"].AddBinContent(10)
                if event.highptFatJets[0].subjets('SoftDrop')[0].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.605:
                    self.Hist["Z2EECounter"].AddBinContent(11) if event.isZ2EE else self.Hist["Z2MMCounter"].AddBinContent(11)
                    if event.highptFatJets[0].subjets('SoftDrop')[1].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.605: 
                        self.Hist["Z2EECounter"].AddBinContent(12) if event.isZ2EE else self.Hist["Z2MMCounter"].AddBinContent(12)
        if event.isZ2NN: 
            if event.met.pt() > 200:
                self.Hist["Z2NNCounter"].AddBinContent(4)
                if event.highptFatJets[0].deltaPhi_met>2.5:
                    if event.highptFatJets[0].userFloat(self.cfg_ana.jetAlgo) > 95 and event.highptFatJets[0].userFloat(self.cfg_ana.jetAlgo) < 130:
                        self.Hist["Z2NNCounter"].AddBinContent(5)
                        if event.highptFatJets[0].subjets('SoftDrop')[0].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.605:
                            self.Hist["Z2NNCounter"].AddBinContent(6)
                            if event.highptFatJets[0].subjets('SoftDrop')[1].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.605: 
                                self.Hist["Z2NNCounter"].AddBinContent(7)
        return True

