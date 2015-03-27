from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import copy
import math
import ROOT

class GammaAnalyzer( Analyzer ):
    '''Analyze and select gamma+jets events'''
    
    def beginLoop(self,setup):
        super(GammaAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            self.inputCounter = ROOT.TH1F("GCounter", "GCounter", 10, 0, 10)
            self.inputCounter.GetXaxis().SetBinLabel(1, "All events")
            self.inputCounter.GetXaxis().SetBinLabel(2, "Trigger")
            self.inputCounter.GetXaxis().SetBinLabel(3, "#Jets > 1")
            self.inputCounter.GetXaxis().SetBinLabel(4, "Jet cuts")
            self.inputCounter.GetXaxis().SetBinLabel(5, "Muon veto")
            self.inputCounter.GetXaxis().SetBinLabel(6, "Photons #geq 1")
            self.inputCounter.GetXaxis().SetBinLabel(7, "Photon cuts")
            self.inputCounter.GetXaxis().SetBinLabel(8, "MEt cut")
            
    #def selectGamma(self, event):
      ## Select at least one photon
      #if len(event.selectedPhotons) < 1: return False
      #if event.selectedPhotons[0] < self.cfg_ana.photon_pt:
        #return False
      #event.Gamma = event.selectedPhotons[0]
      #return True

#    def vetoMuon(self, event):
#        # VETO MUONS - selectedMuons must pass the 'veto' SelectionCuts
#        if len(event.selectedMuons) != 0:
#            return False
#        return True

#    def selectPhoton(self, event):
#      # At least one photon
#      if len(event.selectedPhotons) < 1: 
#          return False
#      # List all the photons passing the cuts
##      GammaPostCuts = [x for x in event.selectedPhotons if x.photonID(self.cfg_ana.photon_id) and x.pt() > self.cfg_ana.photon_pt and abs(x.eta()) < self.cfg_ana.photon_eta and ( abs(x.eta()) < self.cfg_ana.photon_eta_remove_min or abs(x.eta()) > self.cfg_ana.photon_eta_remove_max ) ]
##      if len(GammaPostCuts) != 1: 
##          return False

    def selectPhoton(self, event):
      # At least one photon
      if len(event.selectedPhotons) < 1: 
          return False
      if not event.selectedPhotons[0].pt() > self.cfg_ana.photon_pt:
          return False
      if not event.selectedPhotons[0].photonID(self.cfg_ana.photon_id):
            return False
      event.Photon = event.selectedPhotons[0]
      return True

    def makeFakeMET(self,event):
        if not event.Photon:
            return False
        # Make ject in the event and adding photon px, py
        event.fakemet = copy.deepcopy(event.met)
        px, py = event.met.px()+event.Photon.px(), event.met.py()+event.Photon.py()
        event.fakemet.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        event.fakemetNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px()+event.Photon.px(), event.metNoPU.py()+event.Photon.py()
        event.fakemetNoPU.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        return True

    def selectFakeMET(self, event):
        if event.fakemet.pt() < self.cfg_ana.fakemet_pt:
            return False
#        if event.Category == 1 and deltaPhi(event.fatJets[0].phi(), event.fakemet.phi()) > self.cfg_ana.deltaPhi1met:
#            return True
#        if (event.Category == 2 or event.Category == 3) and deltaPhi(event.JetPostCuts[0].phi(), event.fakemet.phi()) > self.cfg_ana.deltaPhi1met:
#            return True
        return True
        
    def process(self, event):
        # Select exactly 1 photon
        event.isGCR = False
        event.Photon = None
        
        # No Muons
        if not len(event.selectedMuons) == 0:
            return True
        self.inputCounter.Fill(4)
        # At least one photon
        if not len(event.selectedPhotons) >= 1:
            return True
        self.inputCounter.Fill(5)
        # Photon selection
        if not self.selectPhoton(event):
            return True
        self.inputCounter.Fill(6)
        # Build and cut fake MET
        if not self.makeFakeMET(event) or not self.selectFakeMET(event):
            return True
        self.inputCounter.Fill(7)
        # Vetoes
        #self.inputCounter.Fill(8)
        
        event.isGCR = True
        return True

