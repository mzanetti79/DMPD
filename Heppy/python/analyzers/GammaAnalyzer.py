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
            GCRLabels = ["Trigger", "#Jets > 1", "Jet cuts", "Muon veto", "Photons #geq 1", "Photon cuts", "MEt cut"]
            self.GCRCounter = ROOT.TH1F("GCRCounter", "GCRCounter", 8, 0, 8)
            for i, l in enumerate(GCRLabels):
                self.GCRCounter.GetXaxis().SetBinLabel(i+1, l)
            
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
      return True

    def makeFakeMET(self,event):
        # Make ject in the event and adding photon px, py
        event.fakemet = copy.deepcopy(event.met)
        px, py = event.met.px()+event.selectedPhotons[0].px(), event.met.py()+event.selectedPhotons[0].py()
        event.fakemet.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        event.fakemetNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px()+event.selectedPhotons[0].px(), event.metNoPU.py()+event.selectedPhotons[0].py()
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
        
        # No Muons
        if not len(event.selectedMuons) == 0:
            return True
        self.GCRCounter.Fill(3)
        # At least one photon
        if not len(event.selectedPhotons) >= 1:
            return True
        self.GCRCounter.Fill(4)
        # Photon selection
        if not self.selectPhoton(event):
            return True
        self.GCRCounter.Fill(5)
        # Build and cut fake MET
        if not self.makeFakeMET(event) or not self.selectFakeMET(event):
            return True
        self.GCRCounter.Fill(6)
        # Vetoes
        #self.GCRCounter.Fill(7)
        
        event.isGCR = True
        return True

