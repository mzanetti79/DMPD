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
            self.Sync = ROOT.TH1F("Sync", "Sync", 8, 0, 8)
    
    def process(self, event):
        self.Sync.GetXaxis().SetBinLabel(1, "All events")
        self.Sync.Fill(0)
        if len(event.cleanJets) >= 1 and event.cleanJets[0].pt()>110. and event.cleanJets[0].chargedHadronEnergyFraction()>0.2 and event.cleanJets[0].neutralHadronEnergyFraction()<0.7 and event.cleanJets[0].neutralEmEnergyFraction()<0.7:
            self.Sync.GetXaxis().SetBinLabel(2, "Jet pT > 110")
            self.Sync.Fill(1)
            # print
            print "* %5d * %5d * %5d * %10.3f * %10.3f * %10.3f * %10.3f * %10.3f * %10.3f * %10.3f * %5d * %5d * %5d * %5d *" % ( event.input.eventAuxiliary().id().run(), event.input.eventAuxiliary().id().luminosityBlock(), event.input.eventAuxiliary().id().event(),  event.cleanJets[0].pt(), event.cleanJets[0].eta(), event.cleanJets[0].phi(), event.cleanJets[1].pt() if len(event.cleanJets)>1 else 0., event.cleanJets[1].eta() if len(event.cleanJets)>1 else 0., event.cleanJets[1].phi() if len(event.cleanJets)>1 else 0., event.met.pt(), len(event.cleanJets), len(event.inclusiveLeptons), len(event.selectedTaus), len(event.selectedPhotons))
            
            if event.input.eventAuxiliary().id().event()==458: print "@@@@@@@@@@@@@@@@@@", abs(deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi())), event.cleanJets[1].neutralHadronEnergyFraction(), event.cleanJets[1].neutralEmEnergyFraction()
            
            
            if len(event.cleanJets) < 2 or ( abs(deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi())) < 2.5 and event.cleanJets[1].neutralHadronEnergyFraction()<0.7 and event.cleanJets[1].neutralEmEnergyFraction()<0.9 ):
                self.Sync.GetXaxis().SetBinLabel(3, "dPhi(j1,j2)<2.5")
                self.Sync.Fill(2)
                if event.met.pt()>200.:
                    self.Sync.GetXaxis().SetBinLabel(4, "MET > 200")
                    self.Sync.Fill(3)
                    if len(event.cleanJets)<3:
                        self.Sync.GetXaxis().SetBinLabel(5, "Jets < 3")
                        self.Sync.Fill(4)
                        if len(event.inclusiveLeptons) == 0:
                            self.Sync.GetXaxis().SetBinLabel(6, "Lepton veto")
                            self.Sync.Fill(5)
                            if len(event.selectedTaus) == 0:
                                self.Sync.GetXaxis().SetBinLabel(7, "Tau veto")
                                self.Sync.Fill(6)
                                if len(event.selectedPhotons) == 0:
                                    self.Sync.GetXaxis().SetBinLabel(8, "Photon veto")
                                    self.Sync.Fill(7)
                                
        
        return True
    
