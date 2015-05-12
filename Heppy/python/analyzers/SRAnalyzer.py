from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import math
import ROOT

class SRAnalyzer( Analyzer ):
    '''Select Signal Region'''
    
    def beginLoop(self,setup):
        super(SRAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            SRLabels = ["Trigger", "#Jets > 1", "Jet cuts", "MEt cut", "Muon veto", "Electron veto", "Tau veto", "Photon veto"]
            self.SRCounter = ROOT.TH1F("SRCounter", "SRCounter", 8, 0, 8)
            for i, l in enumerate(SRLabels):
                self.SRCounter.GetXaxis().SetBinLabel(i+1, l)
            
    
    def vetoMuon(self, event):
        if len(event.selectedMuons) != 0:
            return False
        return True
    def vetoElectron(self, event):
        if len(event.selectedElectrons) != 0:
            return False
        return True
    def vetoTau(self, event):
        if len(event.selectedTaus) != 0:
            return False
        return True
    def vetoGamma(self, event):
        if len(event.selectedPhotons) != 0:
            return False
        return True

    def selectMET(self, event):
        if event.met.pt() < self.cfg_ana.met_pt:
            return False
        return True
        
    def process(self, event):
        event.isSR = False

        if not self.selectMET(event):
            return True
        self.SRCounter.Fill(3)
        
        # other cuts NOT in Ntuple
        # Muon veto
        if self.vetoMuon(event):
            self.SRCounter.Fill(4)
            # Electron veto
            if self.vetoElectron(event):
                self.SRCounter.Fill(5)
                # Tau veto
                if self.vetoTau(event):
                    self.SRCounter.Fill(6)
                    # Photon veto
                    if self.vetoGamma(event):
                        self.SRCounter.Fill(7)
        
        event.isSR = True
        return True
