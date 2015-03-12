from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
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

    def beginLoop(self,setup):
        super(ZAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            self.inputCounter = ROOT.TH1F("ZCounter", "ZCounter", 10, 0, 10)
    
#    def vetoGamma(self, event):
#        # VETO PHOTONS - selectedPhotons must pass the 'veto' SelectionCuts
#        if len(event.selectedPhotons) != 0:
#            return False
#        return True

#    def selectExclusiveZtoMM(self, event):
#        # Select exactly two muon
#        if not len(event.selectedMuons) >= 2: 
#            return False
#        if not event.selectedMuons[0].charge() != event.selectedMuons[1].charge(): 
#            return False
#        if event.selectedMuons[0].pt() < self.cfg_ana.mu1_pt: 
#            return False
#        if not event.selectedMuons[0].muonID(self.cfg_ana.mu1_id): 
#            return False
#        theZ =  event.selectedMuons[0].p4() + event.selectedMuons[1].p4()
#        if theZ.mass() < self.cfg_ana.mass_low or theZ.mass() > self.cfg_ana.mass_high: 
#            return False
#        event.Z = theZ
#        return True

#    def selectZtoLL(self, event):
#        # Select best Z candidate
#        if len(event.selectedLeptons) < 2:
#          return False
#        event.lep1 = event.selectedLeptons[0]
#        event.lep2 = None
#        for l in event.selectedLeptons:
#          if l.pdgId() == event.lep1.pdgId() and l.charge() != event.lep1.charge():
#            event.lep2 = l
#        if event.lep2 == None:
#          return False
#        theZ = event.lep1.p4() + event.lep2.p4()
#        if theZ.mass() < self.cfg_ana.mass_low or theZ.mass() > self.cfg_ana.mass_high:
#          return False
#        event.Z = theZ
#        return True

#    def selectZtoEE(self, event):
#        # Select best Z candidate
#        if len(event.selectedElectrons) < 2:
#          return False
#        event.elec1 = event.selectedElectrons[0]
#        event.elec2 = None
#        for l in event.selectedElectrons:
#          if l.charge() != event.elec1.charge():
#            event.elec2 = l
#        if event.elec2 == None:
#          return False
#        theZ = event.elec1.p4() + event.elec2.p4()
#        if theZ.mass() < self.cfg_ana.mass_low or theZ.mass() > self.cfg_ana.mass_high:
#          return False
#        event.Z = theZ
#        return True
    
    def selectMuon1(self, event):
        # The leading muons has to satisfy the following conditions
        if not len(event.selectedMuons) >= 1:
            return False
        if not event.selectedMuons[0].pt() > self.cfg_ana.mu1_pt: 
            return False
        if not event.selectedMuons[0].muonID(self.cfg_ana.mu1_id):
            return False
        event.Muon1 = event.selectedMuons[0]
        return True
        
    def selectMuon2(self, event):
        # Select the second muon, as the first one after the leading with opposite sign satisfying the following conditions
        if not len(event.selectedMuons) >= 2:
            return False
        for m in event.selectedMuons:
            if m.charge() == event.Muon1.charge():
                continue
            if not m.pt() > self.cfg_ana.mu2_pt: 
                return False
            if not m.muonID(self.cfg_ana.mu2_id):
                return False
            event.Muon2 = m
        return True
        
    def selectZtoMM(self, event):
        if not event.Muon1 or not event.Muon2:
            return False
        theZ = event.Muon1.p4() + event.Muon2.p4()
        if theZ.mass() < self.cfg_ana.mass_low or theZ.mass() > self.cfg_ana.mass_high:
            return False
        theZ.charge = event.Muon1.charge() + event.Muon2.charge()
        theZ.deltaEta = abs(event.Muon1.eta() - event.Muon2.eta())
        theZ.deltaPhi = deltaPhi(event.Muon1.phi(), event.Muon2.phi())
        theZ.deltaR = deltaR(event.Muon1.eta(), event.Muon1.phi(), event.Muon2.eta(), event.Muon2.phi())
        event.Z = theZ
        return True

    def makeFakeMET(self,event):
        if not event.Z:
            return False
        # Make ject in the event and adding Z px, py
        event.fakeMEt = copy.deepcopy(event.met)
        px, py = event.met.px()+event.Z.px(), event.met.py()+event.Z.py()
        event.fakeMEt.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        event.fakeMEtNoPU = copy.deepcopy(event.metNoPU)
        px, py = event.metNoPU.px()+event.Z.px(), event.metNoPU.py()+event.Z.py()
        event.fakeMEtNoPU.setP4(ROOT.reco.Particle.LorentzVector(px,py, 0, math.hypot(px,py)))
        
        return True

    def selectFakeMet(self, event):
        if event.fakeMEt.pt() < self.cfg_ana.fakemet_pt:
            return False
#        if event.Category == 1 and deltaPhi(event.fatJets[0].phi(), event.fakeMEt.phi()) > self.cfg_ana.deltaPhi1met:
#            return True
#        if (event.Category == 2 or event.Category == 3) and deltaPhi(event.JetPostCuts[0].phi(), event.fakeMEt.phi()) > self.cfg_ana.deltaPhi1met:
#            return True
        return True
         
    def process(self, event):
        event.isZCR = False
        event.Muon1 = None
        event.Muon2 = None
        event.Z = None
        
        # Muons >= 2
        if not len(event.selectedMuons) >= 2:
            return True
        self.inputCounter.Fill(3)
        # Select first muon
        if not self.selectMuon1(event):
            return True
        self.inputCounter.Fill(4)
        # Select second muon
        if not self.selectMuon2(event):
            return True
        self.inputCounter.Fill(5)
        # Build Z candidate
        if not self.selectZtoMM(event):
            return True
        self.inputCounter.Fill(6)
        # Build and cut fake MET
        if not self.makeFakeMET(event) or not self.selectFakeMet(event):
            return True
        self.inputCounter.Fill(7)
        # Vetoes
        #if not self.vetoGamma(event):
        #    return True
        #self.inputCounter.Fill(8)
        
        event.candidate = event.Z
        event.isZCR = True
        return True

