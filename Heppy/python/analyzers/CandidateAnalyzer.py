from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT
import os, sys

class CandidateAnalyzer( Analyzer ):
    '''
    '''
    
    def beginLoop(self,setup):
        super(CandidateAnalyzer,self).beginLoop(setup)
        
    
    def createFakeMet(self, event, particles):
        # Copy regular met
        event.fakecormet = copy.deepcopy(event.cormet)
        px, py = event.cormet.px(), event.cormet.py()
        pxScaleUp, pyScaleUp = event.cormet.ptScaleUp*math.cos(event.cormet.phi()), event.cormet.ptScaleUp*math.sin(event.cormet.phi())
        pxScaleDown, pyScaleDown = event.cormet.ptScaleDown*math.cos(event.cormet.phi()), event.cormet.ptScaleDown*math.sin(event.cormet.phi())
        pxResUp, pyResUp = event.cormet.ptResUp*math.cos(event.cormet.phi()), event.cormet.ptResUp*math.sin(event.cormet.phi())
        pxResDown, pyResDown = event.cormet.ptResDown*math.cos(event.cormet.phi()), event.cormet.ptResDown*math.sin(event.cormet.phi())
        
        for p in particles:
            if not p:
                continue
            else:
                px += p.px()
                py += p.py()
                pxScaleUp += p.px()
                pyScaleUp += p.py()
                pxScaleDown += p.px()
                pyScaleDown += p.py()
                pxResUp += p.px()
                pyResUp += p.py()
                pxResDown += p.px()
                pyResDown += p.py()
                
        event.fakecormet.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px, py)))
        event.fakecormet.ptScaleUp = math.hypot(pxScaleUp, pyScaleUp)
        event.fakecormet.ptScaleDown = math.hypot(pxScaleDown, pyScaleDown)
        event.fakecormet.ptResUp = math.hypot(pxResUp, pyResUp)
        event.fakecormet.ptResDown = math.hypot(pxResDown, pyResDown)
        
        return True
    

    # X candidate
    # number of leptons:
    # 2 - dedicated analyzer
    # 1 - m from kinematic reconstruction, mT is transverse mass
    # 0 - m from collinear approximation, mT is transverse mass
    def createX(self, event, lepton=None):
        event.theX = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
        event.thekW = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
        #met = event.cormet if hasattr(event, "cormet") else event.met
        if len(event.xcleanJetsAK8) > 0:
            event.theX = event.xcleanJetsAK8[0].p4()
            # --- 1 lepton case: kinematic reconstruction of the neutrino pz
            if not lepton is None:
                # Step 1: solve 2nd degree equation
                pz = 0.
                a = 80.4**2 - lepton.mass()**2 + 2.*lepton.px()*event.met.px() + 2.*lepton.py()*event.met.py()
                A = 4*( lepton.energy()**2 - lepton.pz()**2 )
                B = -4*a*lepton.pz()
                C = 4*lepton.energy()**2 * (event.met.px()**2  + event.met.py()**2) - a**2
                D = B**2 - 4*A*C
                # If there are real solutions, use the one with lowest pz
                if D>=0:
                    s1 = (-B+math.sqrt(D))/(2*A)
                    s2 = (-B-math.sqrt(D))/(2*A)
                    pz = s1 if abs(s1) < abs(s2) else s2
                # Otherwise, use real part
                else:
                    pz = -B/(2*A)
                
                # Neutrino candidate
                event.neutrino = ROOT.reco.Particle.LorentzVector(event.met.px(), event.met.py(), pz, math.hypot(event.met.pt(), pz))
                
                # Kinematic W
                event.thekW = lepton.p4() + event.neutrino
                event.thekW.charge = lepton.charge()
                event.thekW.deltaR = deltaR(lepton.eta(), lepton.phi(), event.neutrino.eta(), event.neutrino.phi())
                event.thekW.deltaEta = abs(lepton.eta()-event.neutrino.eta())
                event.thekW.deltaPhi = abs(deltaPhi(lepton.phi(), event.neutrino.phi()))
                event.thekW.deltaPhi_met = abs(deltaPhi(event.thekW.phi(), event.met.phi()))
                event.thekW.mT = math.sqrt( 2.*lepton.et()*event.met.pt()*(1.-math.cos(deltaPhi(lepton.phi(), event.met.phi())) ) )
                
                event.theX += lepton.p4() + event.neutrino
                event.theX.charge = lepton.charge()
                event.theX.deltaR = deltaR(event.thekW.eta(), event.thekW.phi(), event.xcleanJetsAK8[0].eta(), event.xcleanJetsAK8[0].phi())
                event.theX.deltaEta = abs(event.thekW.eta()-event.xcleanJetsAK8[0].eta())
                event.theX.deltaPhi = abs(deltaPhi(event.thekW.phi(), event.xcleanJetsAK8[0].phi()))
                event.theX.deltaPhi_met = abs(deltaPhi(event.thekW.phi(), event.xcleanJetsAK8[0].phi()))
                event.theX.mT = (lepton.p4() + event.met.p4() + event.xcleanJetsAK8[0].p4()).Mt()
                
            # --- 0  lepton case: recoil mass formula
            else:
                cmet = event.cormet.p4()
                cmet.SetPz( -event.xcleanJetsAK8[0].pz() )
                event.theX += event.cormet.p4()
                event.theX.SetPz(0)
                B = -2.*event.xcleanJetsAK8[0].energy()
                C = event.xcleanJetsAK8[0].mass()**2 - 90.18**2
                D = B**2 - 4*1*C
                if D>0:
                    s1 = (-B+math.sqrt(D))/2.
                    s2 = (-B-math.sqrt(D))/2.
                    mX = s1 if abs(s1) > abs(s2) else s2
                else:
                    mX = -B/2.
                event.theX.SetE(math.sqrt(mX**2 + event.theX.Px()**2+event.theX.Py()**2+event.theX.Pz()**2))
                event.theX.charge = 0
                event.theX.deltaR = deltaR(event.cormet.eta(), event.cormet.phi(), event.xcleanJetsAK8[0].eta(), event.xcleanJetsAK8[0].phi())
                event.theX.deltaEta = abs(event.cormet.eta()-event.xcleanJetsAK8[0].eta())
                event.theX.deltaPhi = abs(deltaPhi(event.cormet.phi(), event.xcleanJetsAK8[0].phi()))
                event.theX.deltaPhi_met = abs(deltaPhi(event.xcleanJetsAK8[0].phi(), event.cormet.phi()))
                event.theX.mT = math.sqrt( 2.*event.xcleanJetsAK8[0].et()*event.cormet.pt()*(1.-math.cos(deltaPhi(event.xcleanJetsAK8[0].phi(), event.cormet.phi())) ) )
                event.theX.mTScaleUp = math.sqrt( 2.*event.xcleanJetsAK8[0].et()*event.cormet.ptScaleUp*(1.-math.cos(deltaPhi(event.xcleanJetsAK8[0].phi(), event.cormet.phi())) ) )
                event.theX.mTScaleDown = math.sqrt( 2.*event.xcleanJetsAK8[0].et()*event.cormet.ptScaleDown*(1.-math.cos(deltaPhi(event.xcleanJetsAK8[0].phi(), event.cormet.phi())) ) )
                event.theX.mTResUp = math.sqrt( 2.*event.xcleanJetsAK8[0].et()*event.cormet.ptResUp*(1.-math.cos(deltaPhi(event.xcleanJetsAK8[0].phi(), event.cormet.phi())) ) )
                event.theX.mTResDown = math.sqrt( 2.*event.xcleanJetsAK8[0].et()*event.cormet.ptResDown*(1.-math.cos(deltaPhi(event.xcleanJetsAK8[0].phi(), event.cormet.phi())) ) )
        return True
    
    
    def createT(self, event):
        # Top reconstruction with dR method
        event.T_mass = -1.
        
        # Promote the highest b-tagged jets as b
        xcleanJetsCSV = copy.deepcopy(event.xcleanBJetsNoAK8) +  copy.deepcopy(event.xcleanJetsAK8)
        xcleanJetsCSV.sort(key = lambda l : l.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags'), reverse = True)
        if not len(xcleanJetsCSV) >= 4:
            return True
        
        b1 = xcleanJetsCSV[0]
        xcleanJetsCSV.pop(0)
        b2 = xcleanJetsCSV[0]
        xcleanJetsCSV.pop(0)
        
        # Select the closest jets
        mindR = 99.
        l1, l2 = -1, -1
        for i in range(len(xcleanJetsCSV)):
            for j in range(1, len(xcleanJetsCSV)):
                if deltaR(xcleanJetsCSV[i].eta(), xcleanJetsCSV[i].phi(), xcleanJetsCSV[j].eta(), xcleanJetsCSV[j].phi()) < mindR:
                    Wmass = (xcleanJetsCSV[i].p4() + xcleanJetsCSV[j].p4()).mass()
                    if Wmass > 60 and Wmass < 100:
                        l1, l2 = i, j
                        mindR = deltaR(xcleanJetsCSV[i].eta(), xcleanJetsCSV[i].phi(), xcleanJetsCSV[j].eta(), xcleanJetsCSV[j].phi())
        
        if l1 < 0 or l2 < 0:
            return True
        
        W = xcleanJetsCSV[l1].p4() + xcleanJetsCSV[l2].p4()
        T = W + (b1 if deltaR(b1.eta(), b1.phi(), W.eta(), W.phi()) < deltaR(b2.eta(), b2.phi(), W.eta(), W.phi()) else b2).p4()
        event.T_mass = T.mass()
        
        return True
    
    
    
    
    
    
    def process(self, event):
        
        ### Two leptons
        if event.isZCR:
            if event.isZtoMM: self.createFakeMet(event, [event.selectedMuons[0], event.selectedMuons[1]])
            elif event.isZtoEE: self.createFakeMet(event, [event.selectedElectrons[0], event.selectedElectrons[1]])
        elif event.isTCR: self.createFakeMet(event, [event.selectedElectrons[0], event.selectedMuons[0]])
        elif event.isWCR:
            if event.isWtoMN: self.createFakeMet(event, [event.selectedMuons[0]])
            elif event.isWtoEN: self.createFakeMet(event, [event.selectedElectrons[0]])
        else: self.createFakeMet(event, [])
        
        if event.isZCR:
            pass
        elif event.isTCR:
            self.createT(event)
        elif event.isWCR:
            if event.isWtoMN: self.createX(event, event.selectedMuons[0])
            elif event.isWtoEN: self.createX(event, event.selectedElectrons[0])
            self.createT(event)
        else: self.createX(event)
        
        return True
    
