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
            setup.services["outputfile"].file.mkdir("Sync")
            setup.services["outputfile"].file.cd("Sync")
            
            SRLabels = ["All events", "Jet pT > 110", "dPhi(j1,j2)<2.5", "MET > 200", "Jets < 3", "Lepton veto", "Tau veto", "Photon veto"]
            ZCRLabels = ["All events", "Jet pT > 110", "dPhi(j1,j2)<2.5", "Jets < 3", "Electron veto", "Tau veto", "Photon veto", "Muons = 2", "60 < M(Z) < 120", "fakeMet > 200"]
            WCRLabels = ["All events", "Muons = 1", "Jet pT > 110", "dPhi(j1,j2)<2.5", "Jets < 3", "Electron veto", "Tau veto", "Photon veto", "Mt(W) > 50", "fakeMet > 200"]
            
            self.SR = ROOT.TH1F("SR", "Signal Region", len(SRLabels), 0, len(SRLabels))
            self.ZCR = ROOT.TH1F("ZCR", "Z Control Region", len(ZCRLabels), 0, len(ZCRLabels))
            self.WCR = ROOT.TH1F("WCR", "W Control Region", len(WCRLabels), 0, len(WCRLabels))
            
            for i, l in enumerate(SRLabels): self.SRCounter.GetXaxis().SetBinLabel(i+1, l)
            for i, l in enumerate(ZCRLabels): self.ZCRCounter.GetXaxis().SetBinLabel(i+1, l)
            for i, l in enumerate(WCRLabels): self.WCRCounter.GetXaxis().SetBinLabel(i+1, l)
    
    
    
    def syncSR(self, event):
        self.Sync.Fill(0)
        if len(event.cleanJets) >= 1 and event.cleanJets[0].pt()>110. and event.cleanJets[0].chargedHadronEnergyFraction()>0.2 and event.cleanJets[0].neutralHadronEnergyFraction()<0.7 and event.cleanJets[0].neutralEmEnergyFraction()<0.7:
            self.Sync.Fill(1)                               
            if len(event.cleanJets) < 2 or ( abs(deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi())) < 2.5 and event.cleanJets[1].neutralHadronEnergyFraction()<0.7 and event.cleanJets[1].neutralEmEnergyFraction()<0.9 ):
                self.Sync.Fill(2)
                if event.met.pt()>200.:
                    self.Sync.Fill(3)
                    if len(event.cleanJets)<3:
                        self.Sync.Fill(4)
                        if len(event.inclusiveLeptons) == 0:
                            self.Sync.Fill(5)
                            if len(event.selectedTaus) == 0:
                                self.Sync.Fill(6)
                                if len(event.selectedPhotons) == 0:
                                    self.Sync.Fill(7)
                                    if self.cfg_ana.print: print "%d:%d:%d" % ( event.input.eventAuxiliary().id().run(), event.input.eventAuxiliary().id().luminosityBlock(), event.input.eventAuxiliary().id().event() )
    
    
    
    def syncZCR(self, event):
        self.Sync.Fill(0)
        if len(event.cleanJets) >= 1 and event.cleanJets[0].pt()>110. and event.cleanJets[0].chargedHadronEnergyFraction()>0.2 and event.cleanJets[0].neutralHadronEnergyFraction()<0.7 and event.cleanJets[0].neutralEmEnergyFraction()<0.7:
            self.Sync.Fill(1)                      
            if len(event.cleanJets) < 2 or ( abs(deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi())) < 2.5 and event.cleanJets[1].neutralHadronEnergyFraction()<0.7 and event.cleanJets[1].neutralEmEnergyFraction()<0.9 ):
                self.Sync.Fill(2)
                if len(event.cleanJets)<3:
                    self.Sync.Fill(3)
                    if len(event.selectedElectrons) == 0:
                        self.Sync.Fill(4)
                        if len(event.selectedTaus) == 0:
                            self.Sync.Fill(5)
                            if len(event.selectedPhotons) == 0:
                                self.Sync.Fill(6)                                
                                if event.selectedMuons[0].pt() > 20 and event.selectedMuons[0].muonID('POG_ID_Tight') and event.selectedMuons[0].relIso04 < 0.12 and \
                                   event.selectedMuons[1].pt() > 10 and event.selectedMuons[1].muonID('POG_ID_Loose') and event.selectedMuons[1].relIso04 < 0.20:
                                    self.Sync.Fill(7)
                                    if event.Z.mass() > 60 and event.Z.mass() < 120:
                                        self.Sync.Fill(8)
                                        if event.fakemet.pt() > 200:
                                            self.Sync.Fill(9)
                                            if self.cfg_ana.print: print "ZCR %d:%d:%d" % ( event.input.eventAuxiliary().id().run(), event.input.eventAuxiliary().id().luminosityBlock(), event.input.eventAuxiliary().id().event() )
    
    
    
    def syncWCR(self, event):
        self.Sync.Fill(0)
        if event.selectedMuons[0].pt() > 20 and event.selectedMuons[0].muonID('POG_ID_Tight') and event.selectedMuons[0].relIso04 < 0.12:
            self.Sync.Fill(1)
            if len(events.xcleanJets) > 0 and events.xcleanJets[0].pt()>110. and events.xcleanJets[0].chargedHadronEnergyFraction()>0.2 and events.xcleanJets[0].neutralHadronEnergyFraction()<0.7 and events.xcleanJets[0].neutralEmEnergyFraction()<0.7:
                self.Sync.Fill(2)
                if len(events.xcleanJets) == 1 or ( abs(deltaPhi(events.xcleanJets[0].phi(), events.xcleanJets[1].phi())) < 2.5 and events.xcleanJets[1].neutralHadronEnergyFraction()<0.7 and events.xcleanJets[1].neutralEmEnergyFraction()<0.9 ):
                    self.Sync.Fill(3)
                    if len(events.xcleanJets)<3:
                        self.Sync.Fill(4)
                        if len(event.selectedElectrons) == 0:
                            self.Sync.Fill(5)
                            if len(events.xcleanTaus) == 0:
                                self.Sync.Fill(6)
                                if len(events.selectedPhotons) == 0:
                                    self.Sync.Fill(7)
                                    if event.W.mT > 50:
                                        self.Sync.Fill(8)
                                        if event.fakemet.pt() > 200:
                                            self.Sync.Fill(9)
                                            if self.cfg_ana.print: print "WCR %d:%d:%d" % ( event.input.eventAuxiliary().id().run(), event.input.eventAuxiliary().id().luminosityBlock(), event.input.eventAuxiliary().id().event() )

    
    
    def process(self, event):
        if event.isSR:
            self.syncSR(event)
        elif event.isZCR:
            if len(event.selectedMuons) == 2:
                self.syncZCR(event)
        else event.isWCR:
            if len(event.selectedMuons) == 1:
                self.syncWCR(event)
        
        return True
    
