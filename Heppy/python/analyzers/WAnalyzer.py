from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import copy
import math
import ROOT

class WAnalyzer( Analyzer ):
    '''Analyze and select W->mu nu events
    '''
    
    #def selectW(self, event):
        ## Select exactly one muon
        #if len(event.selectedMuons) == 0:
          #return False
        #theW = event.selectedMuons[0].p4() + event.met.p4()
        #if theW.mt() < self.cfg_ana.mt_low or theW.mt() > self.cfg_ana.mt_high:
          #return False
        #event.W = theW
        #return True
    
    def vetoGamma(self, event):
        # VETO PHOTONS - selectedPhotons must pass the 'veto' SelectionCuts
        if len(event.selectedPhotons) != 0:
            return False
        return True
    
    def selectW(self, event):
        # Select exactly one muon
        if len(event.selectedMuons) < 1:
            return False
        MuonPostCuts = [x for x in event.selectedMuons if x.muonID(self.cfg_ana.mu_id) and x.pt() > self.cfg_ana.mu_pt]
        if len(MuonPostCuts) != 1:
            return False
        theW = MuonPostCuts[0].p4() + event.met.p4()
        if theW.mt() < self.cfg_ana.mt_low or theW.mt() > self.cfg_ana.mt_high:
            return False
        event.W = theW
        event.Muon = MuonPostCuts[0]
        return True
    
    def makeFakeMET(self,event):
        # Make ject in the event and adding muon px, py
        event.fakeMEt = copy.deepcopy(event.met)
        px, py = event.met.px()+event.Muon.px(), event.met.py()+event.Muon.py()
        event.fakeMEt.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        event.fakeMEtNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px()+event.Muon.px(), event.metNoPU.py()+event.Muon.py()
        event.fakeMEtNoPU.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        return True
                
    def selectFakeMet(self, event):
        if event.fakeMEt.pt() < self.cfg_ana.met_pt:
            return False
        if event.Category == 1 and deltaPhi(event.fatJets[0].phi(), event.fakeMEt.phi()) > self.cfg_ana.deltaPhi1met:
            return True
        if (event.Category == 2 or event.Category == 3) and deltaPhi(event.JetPostCuts[0].phi(), event.fakeMEt.phi()) > self.cfg_ana.deltaPhi1met:
            return True
        return False
    
    def process(self, event):
        # Select exactly one muon
        #self.inputCounter.Fill(1)
        event.isWCR = False
        if self.vetoGamma(event) and self.selectW(event) and self.makeFakeMET(event) and self.selectFakeMet(event):
            event.isWCR = True
            return True

