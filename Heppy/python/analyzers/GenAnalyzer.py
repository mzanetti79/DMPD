from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT
import sys

class GenAnalyzer( Analyzer ):
    '''Make plots at generation level'''
    
    def beginLoop(self,setup):
        super(GenAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            setup.services["outputfile"].file.mkdir("Gen")
            setup.services["outputfile"].file.cd("Gen")
            
            self.GenPhi1mass = ROOT.TH1F("GenPhi1mass", ";#Phi mass [GeV]", 1000, 0., 5000.)
            self.GenPhi1pt = ROOT.TH1F("GenPhi1pt", ";#Phi p_{T} [GeV]", 500, 0., 500.)
            self.GenPhi1eta = ROOT.TH1F("GenPhi1eta", ";#Phi #eta", 50, -5, 5.)
            self.GenChi1mass = ROOT.TH1F("GenChi1mass", ";#chi_{1} mass [GeV]", 1000, 0., 100.)
            self.GenChi1pt = ROOT.TH1F("GenChi1pt", ";#chi_{1} p_{T} [GeV]", 500, 0., 500.)
            self.GenChi1eta = ROOT.TH1F("GenChi1eta", ";#chi_{1} #eta", 50, -5, 5.)
            self.GenChi2mass = ROOT.TH1F("GenChi2mass", ";#chi_{2} mass [GeV]", 1000, 0., 100.)
            self.GenChi2pt = ROOT.TH1F("GenChi2pt", ";#chi_{2} p_{T} [GeV]", 500, 0., 500.)
            self.GenChi2eta = ROOT.TH1F("GenChi2eta", ";#chi_{2} #eta", 50, -5, 5.)
            self.GenChi12dR = ROOT.TH1F("GenChi12dR", ";#chi_{1, 2} #Delta R", 50, 0, 5.)
            
            self.GenZdecay = ROOT.TH1F("GenZdecay", ";Z daughter pdgId", 25, 0.5, 25.5)
            self.GenZmass = ROOT.TH1F("GenZmass", ";m_{Z} [GeV]", 100, 0., 200.)
            self.GenZpt = ROOT.TH1F("GenZpt", ";Z p_{T} [GeV]", 250, 0., 2500.)
            self.GenZeta = ROOT.TH1F("GenZeta", ";Z #eta", 50, -5, 5.)
            self.GenZdR = ROOT.TH1F("GenZdR", ";Leptons #Delta R", 50, 0, 5.)
            self.GenHdecay = ROOT.TH1F("GenHdecay", ";H daughter pdgId", 25, 0.5, 25.5)
            self.GenHmass = ROOT.TH1F("GenHmass", ";m_{H} [GeV]", 1000, 100., 150.)
            self.GenHpt = ROOT.TH1F("GenHpt", ";H p_{T} [GeV]", 250, 0., 2500.)
            self.GenHeta = ROOT.TH1F("GenHeta", ";H #eta", 50, -5, 5.)
            self.GenHdR = ROOT.TH1F("GenHdR", ";b-quarks #Delta R", 50, 0, 5.)
            self.GenHdPhi = ROOT.TH1F("GenHdPhi", ";b-quarks #Delta #varphi", 50, 0, 3.15)
            self.GenLepton1pt = ROOT.TH1F("GenLepton1pt", ";Lepton 1 p_{T} [GeV]", 250, 0., 2500.)
            self.GenLepton1eta = ROOT.TH1F("GenLepton1eta", ";Lepton 1 #eta", 50, -5, 5.)
            self.GenLepton2pt = ROOT.TH1F("GenLepton2pt", ";Lepton 2 p_{T} [GeV]", 250, 0., 2500.)
            self.GenLepton2eta = ROOT.TH1F("GenLepton2eta", ";Lepton 2 #eta", 50, -5, 5.)
            self.GenBquark1pt = ROOT.TH1F("GenBquark1pt", ";b-quark 1 p_{T} [GeV]", 250, 0., 2500.)
            self.GenBquark1eta = ROOT.TH1F("GenBquark1eta", ";b-quark 1 #eta", 50, -5, 5.)
            self.GenBquark2pt = ROOT.TH1F("GenBquark2pt", ";b-quark 2 p_{T} [GeV]", 250, 0., 2500.)
            self.GenBquark2eta = ROOT.TH1F("GenBquark2eta", ";b-quark 2 #eta", 50, -5, 5.)
            
            setup.services["outputfile"].file.cd()
    
    def process(self, event):
        
        if not hasattr(event, "genParticles"):
            return True
        # Mediator
        event.genPhi = None
        event.genChi = []
        
        for g in event.genParticles:
            if g.pdgId() == 9100000 or g.pdgId() == 9900032 or g.pdgId() == 1023:
                event.genPhi = g
            if abs(g.pdgId()) == 9100022 or g.pdgId() == 9100012:
                chi.append(g)
        if event.genPhi:
            self.GenPhi1mass.Fill(event.genPhi.mass())
            self.GenPhi1pt.Fill(event.genPhi.pt())
            self.GenPhi1eta.Fill(event.genPhi.eta())
        if len(event.genChi) == 2:
            i1, i2 = [0, 1] if chi[0].pt() > chi[1].pt() else [1, 0]
            self.GenChi1mass.Fill(chi[i1].mass())
            self.GenChi1pt.Fill(chi[i1].pt())
            self.GenChi1eta.Fill(chi[i1].eta())
            self.GenChi2mass.Fill(chi[i1].mass())
            self.GenChi2pt.Fill(chi[i1].pt())
            self.GenChi2eta.Fill(chi[i1].eta())
            self.GenChi12dR.Fill(deltaR(chi[0].eta(), chi[0].phi(), chi[1].eta(), chi[1].phi()))
        # Z
        if hasattr(event, "genVBosons"):
            if len(event.genVBosons) > 0:
                self.GenZmass.Fill(event.genVBosons[0].mass())
                self.GenZpt.Fill(event.genVBosons[0].pt())
                self.GenZeta.Fill(event.genVBosons[0].eta())
        # Higgs
        if hasattr(event, "genHiggsBosons"):
            if len(event.genHiggsBosons) > 0:
                self.GenHmass.Fill(event.genHiggsBosons[0].mass())
                self.GenHpt.Fill(event.genHiggsBosons[0].pt())
                self.GenHeta.Fill(event.genHiggsBosons[0].eta())
        # Leptons from Z
        if hasattr(event, "genleps"):
            if len(event.genleps) >= 2:
                self.GenZdecay.Fill(abs(event.genleps[0].pdgId()))
                self.GenZdR.Fill(deltaR(event.genleps[0].eta(), event.genleps[0].phi(), event.genleps[1].eta(), event.genleps[1].phi()))
                i1, i2 = [0, 1] if event.genleps[0].pt() > event.genleps[1].pt() else [1, 0]
                self.GenLepton1pt.Fill(event.genleps[i1].pt())
                self.GenLepton1eta.Fill(event.genleps[i1].eta())
                self.GenLepton2pt.Fill(event.genleps[i2].pt())
                self.GenLepton2eta.Fill(event.genleps[i2].eta())
        # b-quarks from Higgs
        if hasattr(event, "genbquarks"):
            if len(event.genbquarks) == 1:
                self.GenBquark1pt.Fill(event.genbquarks[0].pt())
                self.GenBquark1eta.Fill(event.genbquarks[0].eta())
            elif len(event.genbquarks) >= 2:
                self.GenHdecay.Fill(abs(event.genbquarks[0].pdgId()))
                self.GenHdR.Fill(deltaR(event.genbquarks[0].eta(), event.genbquarks[0].phi(), event.genbquarks[1].eta(), event.genbquarks[1].phi()))
                self.GenHdPhi.Fill(deltaPhi(event.genbquarks[0].phi(), event.genbquarks[1].phi()))
                i1, i2 = [0, 1] if event.genbquarks[0].pt() > event.genbquarks[1].pt() else [1, 0]
                self.GenBquark1pt.Fill(event.genbquarks[i1].pt())
                self.GenBquark1eta.Fill(event.genbquarks[i1].eta())
                self.GenBquark2pt.Fill(event.genbquarks[i2].pt())
                self.GenBquark2eta.Fill(event.genbquarks[i2].eta())
            
        return True
    
