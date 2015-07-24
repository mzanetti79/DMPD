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
            ZCRLabels = ["Trigger", "#Jets > 1", "Jet cuts", "Lep #geq 2", "Lep1 cuts", "Lep2 cuts", "Z cand", "MEt cut"]
            WCRLabels = ["Trigger", "#Jets > 1", "Jet cuts", "Lep #geq 2", "Lep1 cuts", "Lep2 cuts", "Z cand", "MEt cut"]
            
            self.SR = ROOT.TH1F("SR", "Signal Region", 8, 0, 8)
            self.ZCR = ROOT.TH1F("ZCR", "Z Control Region", 8, 0, 8)
            self.WCR = ROOT.TH1F("WCR", "W Control Region", 8, 0, 8)
            
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
                                    
                                    #print "%d:%d:%d" % ( event.input.eventAuxiliary().id().run(), event.input.eventAuxiliary().id().luminosityBlock(), event.input.eventAuxiliary().id().event() )
    
    
    def syncZCR(self, event):
        self.Sync.GetXaxis().SetBinLabel(1, "All events")
            self.Sync.Fill(0)
            if len(event.cleanJets) >= 1 and event.cleanJets[0].pt()>110. and event.cleanJets[0].chargedHadronEnergyFraction()>0.2 and event.cleanJets[0].neutralHadronEnergyFraction()<0.7 and event.cleanJets[0].neutralEmEnergyFraction()<0.7:
                self.Sync.GetXaxis().SetBinLabel(2, "Jet pT > 110")
                self.Sync.Fill(1)                      
                if len(event.cleanJets) < 2 or ( abs(deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi())) < 2.5 and event.cleanJets[1].neutralHadronEnergyFraction()<0.7 and event.cleanJets[1].neutralEmEnergyFraction()<0.9 ):
                    self.Sync.GetXaxis().SetBinLabel(3, "dPhi(j1,j2)<2.5")
                    self.Sync.Fill(2)
                    if len(event.cleanJets)<3:
                        self.Sync.GetXaxis().SetBinLabel(4, "Jets < 3")
                        self.Sync.Fill(3)
                        if len(event.selectedElectrons) == 0:
                            self.Sync.GetXaxis().SetBinLabel(5, "Electron veto")
                            self.Sync.Fill(4)
                            if len(event.selectedTaus) == 0:
                                self.Sync.GetXaxis().SetBinLabel(6, "Tau veto")
                                self.Sync.Fill(5)
                                if len(event.selectedPhotons) == 0:
                                    self.Sync.GetXaxis().SetBinLabel(7, "Photon veto")
                                    self.Sync.Fill(6)                                
                                    if len(event.selectedMuons) == 2 and \
                                        event.selectedMuons[0].pt() > 20 and event.selectedMuons[0].muonID('POG_ID_Tight') and event.selectedMuons[0].relIso04 < 0.12 and \
                                        event.selectedMuons[1].pt() > 10 and event.selectedMuons[1].muonID('POG_ID_Loose') and event.selectedMuons[1].relIso04 < 0.20 and \
                                        event.selectedMuons[0].charge() != event.selectedMuons[1].charge():
                                        theMu0 = event.selectedMuons[0]
                                        theMu1 = event.selectedMuons[1]
                                        self.Sync.GetXaxis().SetBinLabel(8, "Muons = 2")
                                        self.Sync.Fill(7)
                                        theZ = theMu0.p4() + theMu1.p4()
                                        if theZ.mass() > 60 and theZ.mass() < 120:
                                            self.Sync.GetXaxis().SetBinLabel(9, "60 < M(Z) < 120")
                                            self.Sync.Fill(8)
                                            fakemet = copy.deepcopy(event.met)
                                            px, py = event.met.px() + theZ.px(), event.met.py() + theZ.py()
                                            fakemet.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px,py)))
                                            if fakemet.pt() > 200:
                                                self.Sync.GetXaxis().SetBinLabel(10, "fakeMet > 200")
                                                self.Sync.Fill(9)
                                                print "ZCR %d:%d:%d" % ( event.input.eventAuxiliary().id().run(), event.input.eventAuxiliary().id().luminosityBlock(), event.input.eventAuxiliary().id().event() )
            
    
    
    def process(self, event):
        if event.isSR:
            self.syncSR(event)
        elif event.isZCR:
            self.syncZCR(event)
        else event.isWCR:
            self.syncWCR(event)
        
        
        
        
        
        
                                
        
        return True
    
