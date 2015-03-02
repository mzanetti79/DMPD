from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import copy
import math
import ROOT

class ZAnalyzer( Analyzer ):
    '''Analyze and select Z->ll events
    selectExclusiveZtoMM: selects exactly two muons
    selectZtoLL: selects best lepton combination to build the Z, does not veto other leptons
    selectZtoLL: selects best electron combination to build the Z, does not veto other electrons
    selectZtoLL: selects best muon combination to build the Z, does not veto other muons
    '''

    #def selectExclusiveZtoMM(self, event):
        ## Select exactly two muon
        #if not len(event.selectedMuons) == 2: return False
        #if not event.selectedMuons[0].charge() != event.selectedMuons[1].charge(): return False
        #theZ =  event.selectedMuons[0].p4() + event.selectedMuons[1].p4()
        #if theZ.mass() < self.cfg_ana.mass: return False
        #event.Z = theZ
        #return True

    def selectExclusiveZtoMM(self, event):
        # Select exactly two muon
        if not len(event.selectedMuons) == 2: 
            return False
        if not event.selectedMuons[0].charge() != event.selectedMuons[1].charge(): 
            return False
        if event.selectedMuons[0].pt() < self.cfg_ana.mu1_pt: 
            return False
        if not event.selectedMuons[0].muonID(self.cfg_ana.mu1_id): 
            return False
        theZ =  event.selectedMuons[0].p4() + event.selectedMuons[1].p4()
        if theZ.mass() < self.cfg_ana.mass_low or theZ.mass() > self.cfg_ana.mass_high: 
            return False
        event.Z = theZ
        return True

    def selectZtoLL(self, event):
        # Select best Z candidate
        if len(event.selectedLeptons) < 2:
          return False
        event.lep1 = event.selectedLeptons[0]
        event.lep2 = None
        for l in event.selectedLeptons:
          if l.pdgId() == event.lep1.pdgId() and l.charge() != event.lep1.charge():
            event.lep2 = l
        if event.lep2 == None:
          return False
        theZ = event.lep1.p4() + event.lep2.p4()
        if theZ.mass() < self.cfg_ana.mass:
          return False
        event.Z = theZ

    def selectZtoEE(self, event):
        # Select best Z candidate
        if len(event.selectedElectrons) < 2:
          return False
        event.elec1 = event.selectedElectrons[0]
        event.elec2 = None
        for l in event.selectedElectrons:
          if l.charge() != event.elec1.charge():
            event.elec2 = l
        if event.elec2 == None:
          return False
        theZ = event.elec1.p4() + event.elec2.p4()
        if theZ.mass() < self.cfg_ana.mass:
          return False
        event.Z = theZ
     
    def selectZtoMM(self, event):
        # Select best Z candidate
        if len(event.selectedMuons) < 2:
          return False
        event.muon1 = event.selectedMuons[0]
        event.muon2 = None
        for m in event.selectedMuons:
          if m.charge() != event.muon1.charge():
            event.muon2 = m
        if event.muon2 == None:
          return False
        theZ = event.muon1.p4() + event.muon2.p4()
        if theZ.mass() < self.cfg_ana.mass:
          return False
        event.Z = theZ

    def makeFakeMET(self,event):
        # Make ject in the event and adding Z px, py
        event.fakeMEt = copy.deepcopy(event.met)
        px, py = event.met.px()+event.Z.px(), event.met.py()+event.Z.py()
        event.fakeMEt.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        event.fakeMEtNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px()+event.Z.px(), event.metNoPU.py()+event.Z.py()
        event.fakeMEtNoPU.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        if event.fakeMEt.pt() < self.cfg_ana.met_pt:
          return False
        return True
         
         
    def process(self, event):
        #self.inputCounter.Fill(1)
        if not self.selectExclusiveZtoMM(event):
          return False
        if not self.makeFakeMET(event):
          return False
        return True

