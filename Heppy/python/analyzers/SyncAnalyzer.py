from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT
import sys

class SyncAnalyzer( Analyzer ):
    '''Sync plot'''
    
    def beginLoop(self,setup):
        super(SyncAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            self.Sync = ROOT.TH1F("Sync", "Sync", 7, -0.5, 6.5)
    
    def process(self, event):
        self.Sync.GetXaxis().SetBinLabel(1, "All events")
        self.Sync.Fill(0)
        if len(event.cleanJets) >= 1 and event.cleanJets[0].pt()>110. and event.cleanJets[0].chargedHadronEnergyFraction()>0.2 and event.cleanJets[0].neutralHadronEnergyFraction()<0.7 and event.cleanJets[0].neutralEmEnergyFraction()<0.7:
            self.Sync.GetXaxis().SetBinLabel(2, "Jet pT > 110")
            self.Sync.Fill(1)
            if event.met.pt()>200.:
                self.Sync.GetXaxis().SetBinLabel(3, "MET > 200")
                self.Sync.Fill(2)
                if len(event.cleanJets)<3:
                    self.Sync.GetXaxis().SetBinLabel(4, "Jets < 3")
                    self.Sync.Fill(3)
                    if len(event.inclusiveLeptons) == 0:
                        self.Sync.GetXaxis().SetBinLabel(5, "Lepton veto")
                        self.Sync.Fill(4)
                        if len(event.selectedTaus) == 0:
                            self.Sync.GetXaxis().SetBinLabel(6, "Tau veto")
                            self.Sync.Fill(5)
                            if len(event.selectedPhotons) == 0:
                                self.Sync.GetXaxis().SetBinLabel(7, "Photon veto")
                                self.Sync.Fill(6)
        
        return True
    
