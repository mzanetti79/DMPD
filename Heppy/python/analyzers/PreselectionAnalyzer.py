from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2, deltaPhi
import copy
import math
import ROOT
import sys

class PreselectionAnalyzer( Analyzer ):
    '''
    '''
    
    def beginLoop(self,setup):
        super(PreselectionAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            Labels = ["Trigger"]
            self.Counter = ROOT.TH1F("Counter", "Counter", 8, 0, 8)
            for i, l in enumerate(Labels):
                self.Counter.GetXaxis().SetBinLabel(i+1, l)
    
    
#    def fillJetVariables(self, event):
#        for j in event.Jets + event.cleanJets + event.cleanJetsAK8:
#            j.deltaPhi_met = deltaPhi(j.phi(), event.met.phi())
#            j.deltaPhi_jet1 = deltaPhi(j.phi(), event.Jets[0].phi())
#    
#    def fillFatJetVariables(self, event):
#        # Add n-subjettiness
#        for i, j in enumerate(event.cleanJetsAK8):
#            j.tau21 = j.userFloat("NjettinessAK8:tau2")/j.userFloat("NjettinessAK8:tau1") if not j.userFloat("NjettinessAK8:tau1") == 0 else -1.
#        
#        # Count b-tagged subjets
#        for i, j in enumerate(event.cleanJetsAK8):
#            nSubJetTags = 0
#            subJets = j.subjets('SoftDrop')
#            for iw, wsub in enumerate(subJets):
#                if iw == 0:
#                    j.flavour1 = wsub.hadronFlavour()
#                    j.CSV1 = wsub.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')
#                    if j.CSV1 > self.cfg_ana.fatjet_tag1:
#                        nSubJetTags += 1
#                elif iw == 1:
#                    j.flavour2 = wsub.hadronFlavour()
#                    j.CSV2 = wsub.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')
#                    if j.CSV2 > self.cfg_ana.fatjet_tag2:
#                        nSubJetTags += 1
#            j.nSubJetTags = nSubJetTags
#            
#    def selectFatJet(self, event):
#        if not len(event.cleanJetsAK8) >= 1:
#            return False
#        if not event.cleanJetsAK8[0].pt() > self.cfg_ana.fatjet_pt: 
#            return False
#        
#        # FatJet selections
#        if not event.cleanJetsAK8[0].nSubJetTags >= 2:
#            return False
#        if not event.cleanJetsAK8[0].userFloat(self.cfg_ana.fatjet_mass_algo) > self.cfg_ana.fatjet_mass:
#            return False
#        if not hasattr(event.cleanJetsAK8[0], "tau21") or not event.cleanJetsAK8[0].tau21 > self.cfg_ana.fatjet_tau21:
#            return False
#        
#        # Add subjets to the event
#        event.SubJets = event.cleanJetsAK8[0].subjets('SoftDrop')
#        
#        # Higgs candidate
#        theV = event.cleanJetsAK8[0].p4()
#        theV.charge = event.cleanJetsAK8[0].charge()
#        theV.deltaR = deltaR(event.SubJets[0].eta(), event.SubJets[0].phi(), event.SubJets[1].eta(), event.SubJets[1].phi())
#        theV.deltaEta = abs(event.SubJets[0].eta() - event.SubJets[1].eta())
#        theV.deltaPhi = deltaPhi(event.SubJets[0].phi(), event.SubJets[1].phi())
#        theV.deltaPhi_met = deltaPhi(theV.phi(), event.met.phi())
#        theV.deltaPhi_jet1 = deltaPhi(theV.phi(), event.cleanJetsAK8[0].phi())
#        event.V = theV
#        
#        return True


#    def selectResolvedJet(self, event):
#        if not len(event.cleanJets) >= 2:
#            return False
#        if not event.cleanJets[0].pt() > self.cfg_ana.jet1_pt: 
#            return False
##        if not event.cleanJets[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.jet1_tag: 
##            return False
#        if not event.cleanJets[1].pt() > self.cfg_ana.jet2_pt: 
#            return False
##        if not event.cleanJets[1].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.jet2_tag: 
##            return False
#        
#        # Higgs candidate
#        theV = event.cleanJets[0].p4() + event.cleanJets[1].p4()
#        theV.charge = event.cleanJets[0].charge() + event.cleanJets[1].charge()
#        theV.deltaR = deltaR(event.cleanJets[0].eta(), event.cleanJets[0].phi(), event.cleanJets[1].eta(), event.cleanJets[1].phi())
#        theV.deltaEta = abs(event.cleanJets[0].eta() - event.cleanJets[1].eta())
#        theV.deltaPhi = deltaPhi(event.cleanJets[0].phi(), event.cleanJets[1].phi())
#        theV.deltaPhi_met = deltaPhi(theV.phi(), event.met.phi())
#        theV.deltaPhi_jet1 = deltaPhi(theV.phi(), event.cleanJets[0].phi())
#        event.V = theV
#        
#        return True
#    
#    
#    def selectMonoJet(self, event):
#        if not len(event.cleanJets) >= 1:
#            return False
#        if not event.cleanJets[0].pt() > self.cfg_ana.jet1_pt:
#            return False
#        #if not event.cleanJets[0].btag('combinedInclusiveSecondaryVertexV2BJetTags') > self.cfg_ana.jet1_tag:
#        #    return False
#        
#        # Higgs candidate
#        theV = event.cleanJets[0].p4()
#        theV.charge = event.cleanJets[0].charge()
#        theV.deltaR = -1.
#        theV.deltaEta = -9.
#        theV.deltaPhi = -9.
#        theV.deltaPhi_met = -9.
#        theV.deltaPhi_jet1 = -9.
#        event.V = theV
#        
#        return True
#    
    
    def addFakeMet(self, event, particles):
        # Copy regular met
        event.fakemet = copy.deepcopy(event.met)
        px, py = event.met.px(), event.met.py()
        for i, p in enumerate(particles):
            if not p:
                continue
            else:
                px += p.px()
                py += p.py()
        
        event.fakemet.setP4(ROOT.reco.Particle.LorentzVector(px, py, 0, math.hypot(px, py)))
        return True
    
    def createZ(self, event, leptons):
        theZ = leptons[0].p4() + leptons[1].p4()
        theZ.charge = leptons[0].charge() + leptons[1].charge()
        theZ.deltaR = deltaR(leptons[0].eta(), leptons[0].phi(), leptons[1].eta(), leptons[1].phi())
        theZ.deltaEta = abs(leptons[0].eta() - leptons[1].eta())
        theZ.deltaPhi = deltaPhi(leptons[0].phi(), leptons[1].phi())
        #theZ.deltaPhi_met = deltaPhi(theZ.phi(), event.met.phi())
        event.Z = theZ
        return True
    
    def createW(self, event, lepton):
        theW = lepton.p4() + event.met.p4()
        theW.charge = lepton.charge()
        theW.deltaR = deltaR(lepton.eta(), lepton.phi(), 0, event.met.phi())
        theW.deltaEta = abs(lepton.eta())
        theW.deltaPhi = deltaPhi(lepton.phi(), event.met.phi())
        theW.deltaPhi_met = deltaPhi(lepton.phi(), event.met.phi())
        theW.mT = math.sqrt( 2.*lepton.et()*event.met.pt()*(1.-math.cos(theW.deltaPhi_met)) )
        event.W = theW
        return True
    
    def createA(self, event):
        if not len(event.cleanJetsAK8) > 0:
            event.A = event.met.p4()
            event.A.SetE(0)
            event.A.SetPx(0)
            event.A.SetPy(0)
            event.A.SetPz(0)
            return True
        # Pseudo-kin fit
        kH = event.cleanJetsAK8[0].p4()
        k = 125.0/event.cleanJetsAK8[0].mass()#.userFloat("ak8PFJetsCHSSoftDropMass")
        kH.SetE( event.cleanJetsAK8[0].energy()*k )
        kH.SetPx( event.cleanJetsAK8[0].px()*k )
        kH.SetPy( event.cleanJetsAK8[0].py()*k )
        kH.SetPz( event.cleanJetsAK8[0].pz()*k )
        
        if event.isZCR:
            theA = event.Z + event.cleanJetsAK8[0].p4()
            theA.mT = theA.mass()
            theA.mC = theA.mass()
            theA.mK = (event.Z + kH).mass()
        elif event.isWCR:
            theA = event.xcleanLeptons[0].p4() + event.met.p4() + event.cleanJetsAK8[0].p4()
#            pz = 0.
#            a = 80.4**2 - event.xcleanLeptons[0].mass()**2 + 2.*event.xcleanLeptons[0].px()*event.met.px() + 2.*event.xcleanLeptons[0].py()*event.met.py()
#            A = 4*( event.xcleanLeptons[0].energy()**2 - event.xcleanLeptons[0].pz()**2 )
#            B = -4*a*event.xcleanLeptons[0].pz()
#            C = 4*event.xcleanLeptons[0].energy()**2 * (event.met.px()**2  + event.met.py()**2) - a**2
#            D = B**2 - 4*A*C
#            if D>0:
#                pz = min((-B+math.sqrt(D))/(2*A), (-B-math.sqrt(D))/(2*A))
#            else:
#                pz = -B/(2*A)
#            kmet = event.met.p4()
#            kmet.SetPz(pz)
#            theA.mT = (event.xcleanLeptons[0].p4() + kmet + event.cleanJetsAK8[0].p4()).mass()
#            cmet = event.met.p4()
#            cmet.SetPz(event.xcleanLeptons[0].pz())
#            theA.mC = (event.xcleanLeptons[0].p4() + cmet + event.cleanJetsAK8[0].p4()).mass()
#            theA.mK = (event.xcleanLeptons[0].p4() + kmet + kH).mass()
        else:
            theA = event.met.p4() + event.cleanJetsAK8[0].p4()
#            theA.mT = math.sqrt( 2.*event.cleanJetsAK8[0].energy()*event.met.pt()*(1.-math.cos( deltaPhi(event.cleanJetsAK8[0].phi(), event.met.phi()) )) )
#            cmet = event.met.p4()
#            cmet.SetPz( -event.cleanJetsAK8[0].pz() )
#            theA.mC = (cmet + event.cleanJetsAK8[0].p4()).mass()
#            theA.mK = math.sqrt( 2.*kH.energy()*event.met.pt()*(1.-math.cos( deltaPhi(kH.phi(), event.met.phi()) )) )
        event.A = theA
        return True
    
    def process(self, event):
        event.isSR = False
        event.isZCR = False
        event.isWCR = False
        event.isTCR = False
        event.isGCR = False
        event.isZtoEE = False
        event.isZtoMM = False
        event.isWtoEN = False
        event.isWtoMN = False
        
        # Build clean collections
        event.xcleanLeptons = event.selectedMuons + event.selectedElectrons
        event.xcleanTaus    = event.selectedTaus
        event.xcleanPhotons = event.selectedPhotons
        event.xcleanJets    = event.cleanJets
        event.xcleanJetsAK8 = event.cleanJetsAK8
#        event.xcleanJetsJERUp      = event.cleanJetsJERUp
#        event.xcleanJetsAK8JERUp   = event.cleanJetsAK8JERUp
#        event.xcleanJetsJERDown    = event.cleanJetsJERDown
#        event.xcleanJetsAK8JERDown = event.cleanJetsAK8JERDown
        
        for i, j in enumerate(event.xcleanJets+event.xcleanJetsAK8):#+event.xcleanJetsJERUp+event.xcleanJetsJERDown:
            j.deltaPhi_met = abs(deltaPhi(j.phi(), event.met.phi()))
            j.deltaPhi_jet1 = abs(deltaPhi(j.phi(), event.xcleanJets[0].phi()))
        for i, j in enumerate(event.xcleanJetsAK8):#+event.xcleanJetsAK8JERUp+event.xcleanJetsAK8JERDown):
            j.deltaPhi_met = abs(deltaPhi(j.phi(), event.met.phi()))
            j.deltaPhi_jet1 = abs(deltaPhi(j.phi(), event.xcleanJetsAK8[0].phi()))
            
        
        self.Counter.Fill(-1)
        # Trigger
        self.Counter.Fill(0)
        
        # Check if there is at least one jet
        #if len(event.cleanJets) < 1:# and len(event.cleanJetsAK8) < 1:
        #    return False
        #self.Counter.Fill(1)
        
        # Count Leptons and select Regions
        
        ### Two leptons
        if len(event.selectedLeptons) >= 2:
            ###   TTbar Control Region   ###
            if len(event.selectedElectrons) == 1 and len(event.selectedMuons) == 1 and event.selectedElectrons[0].charge() != event.selectedMuons[0].charge():
                self.addFakeMet(event, [event.selectedElectrons[0], event.selectedMuons[0]])
                event.xcleanLeptons.sort(key = lambda l : l.pt(), reverse = True)
                event.isTCR = True
            
            ###   Z(ee) Control Region   ###
            elif len(event.selectedElectrons) >= 2 and event.selectedElectrons[0].charge() != event.selectedElectrons[1].charge():
                self.addFakeMet(event, [event.selectedElectrons[0], event.selectedElectrons[1]])
                self.createZ(event, [event.selectedElectrons[0], event.selectedElectrons[1]])
                event.xcleanLeptons = event.selectedElectrons
                event.isZtoEE = True
                event.isZCR = True
            
            ###   Z(mm) Control Region   ###
            elif len(event.selectedMuons) >= 2 and event.selectedMuons[0].charge() != event.selectedMuons[1].charge():
                self.addFakeMet(event, [event.selectedMuons[0], event.selectedMuons[1]])
                self.createZ(event, [event.selectedMuons[0], event.selectedMuons[1]])
                event.xcleanLeptons = event.selectedMuons
                event.isZtoMM = True
                event.isZCR = True
        
        ### One lepton
        elif len(event.selectedLeptons) == 1:
            ###   W(enu) Control Region   ###
            if len(event.selectedElectrons) == 1:
                self.addFakeMet(event, [event.selectedElectrons[0]])
                self.createW(event, event.selectedElectrons[0])
                event.xcleanLeptons = event.selectedElectrons
                event.isWtoEN = True
                event.isWCR = True
            
            ###   W(mnu) Control Region   ###
            elif len(event.selectedMuons) == 1:
                self.addFakeMet(event, [event.selectedMuons[0]])
                self.createW(event, event.selectedMuons[0])
                event.xcleanLeptons = event.selectedMuons
                event.isWtoMN = True
                event.isWCR = True
        
        ### One photon
        elif len(event.selectedPhotons) >= 1:
            self.addFakeMet(event, [event.selectedPhotons[0]])
            event.isGCR = True
        
        ### No leptons nor photons
        else:
            self.addFakeMet(event, [])
            event.isSR = True
        
        # AZh
        self.createA(event)
        
        return True
    
