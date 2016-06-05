import random
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet
from PhysicsTools.HeppyCore.utils.deltar import * 
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.Heppy.physicsutils.JetReCalibrator import JetReCalibrator
import PhysicsTools.HeppyCore.framework.config as cfg

import operator 
import itertools
import copy
import ROOT
import math
import os

from copy import deepcopy



class RecoilAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(RecoilAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def beginLoop(self, setup):
        super(RecoilAnalyzer,self).beginLoop(setup)
        ### RECOIL CORRECTIONS SETUP ###
        ROOT.gROOT.ProcessLine(self.cfg_ana.processLine)
        self.Recoil = ROOT.RecoilCorrector(self.cfg_ana.ref_recoilMC_file)
        self.Recoil.addDataFile(self.cfg_ana.ref_recoilData_file)
        self.Recoil.addMCFile(self.cfg_ana.ref_recoilMC_file)
    
    
    def process(self, event):

        ''' RECOIL '''
        
        # add corrected MET in all regions
        event.cormet = copy.deepcopy(event.met)
        
        ### fill default values
        cmetpt           = ROOT.Double(event.met.pt())
        cmetphi          = ROOT.Double(event.met.phi())
        cmetptScaleUp    = ROOT.Double(event.met.pt())
        cmetphiScaleUp   = ROOT.Double(event.met.phi())
        cmetptScaleDown  = ROOT.Double(event.met.pt())
        cmetphiScaleDown = ROOT.Double(event.met.phi())
        cmetptResUp      = ROOT.Double(event.met.pt())
        cmetphiResUp     = ROOT.Double(event.met.phi())
        cmetptResDown    = ROOT.Double(event.met.pt())
        cmetphiResDown   = ROOT.Double(event.met.phi())
        
        applyrecoil    = True # safety (maybe useless now)
        
        nJets = len(event.cleanJets)
        
        # configure input parameters (GENMET / RECO_V_PT / RECOIL) only for Z->ll, Z->vv, and W->lv
        if self.cfg_comp.isMC and hasattr(event, "genV"):
            genmetpt  = ROOT.Double(event.genV.pt())
            genmetphi = ROOT.Double(event.genV.phi())
            leppt     = ROOT.Double(0.)
            lepphi    = ROOT.Double(0.)
            Upar      = ROOT.Double(0.)
            Uper      = ROOT.Double(0.)
            if event.isZCR and hasattr(event, "theZ") and hasattr(event, "Upara") and hasattr(event, "Uperp"):
                leppt     = ROOT.Double(event.theZ.pt())
                lepphi    = ROOT.Double(event.theZ.phi())
                Upar      = ROOT.Double(event.Upara)
                Uper      = ROOT.Double(event.Uperp)
            elif event.isWCR and hasattr(event, "theW") and hasattr(event, "Upara") and hasattr(event, "Uperp"):
                leppt     = ROOT.Double(event.xcleanLeptons[0].pt())
                lepphi    = ROOT.Double(event.xcleanLeptons[0].phi())
                Upar      = ROOT.Double(event.Upara)
                Uper      = ROOT.Double(event.Uperp)
            elif event.isTCR:
                # in situ evaluation of pseudo-boson (mu^\pm + e^\mp)
                pseudoboson = ROOT.reco.Particle.LorentzVector(0, 0, 0, 0)
                for l in event.xcleanLeptons: pseudoboson += l.p4()
                recoilX = - event.met.px() - pseudoboson.px()
                recoilY = - event.met.py() - pseudoboson.py()
                pseudoUpara = (recoilX*pseudoboson.px() + recoilY*pseudoboson.py())/pseudoboson.pt()
                pseudoUperp = (recoilX*pseudoboson.py() - recoilY*pseudoboson.px())/pseudoboson.pt()    
                leppt     = ROOT.Double(pseudoboson.pt())
                lepphi    = ROOT.Double(pseudoboson.phi())
                Upar      = ROOT.Double(pseudoUpara)
                Uper      = ROOT.Double(pseudoUperp)
            elif event.genV.pt()>0.:
                recoilX = - event.met.px() - event.genV.px()
                recoilY = - event.met.py() - event.genV.py()
                event.Upara = (recoilX*event.genV.px() + recoilY*event.genV.py())/event.genV.pt()
                event.Uperp = (recoilX*event.genV.py() - recoilY*event.genV.px())/event.genV.pt()        
            else:
                applyrecoil = False
            
            if applyrecoil:
                ### do the MET recoil corrections in SR, ZCR and WCR, only for DYJets, ZJets and WJets samples
                self.Recoil.CorrectType2(cmetpt,          cmetphi,          genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 0, nJets)
                self.Recoil.CorrectType2(cmetptScaleUp,   cmetphiScaleUp,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 3, 0, nJets)
                self.Recoil.CorrectType2(cmetptScaleDown, cmetphiScaleDown, genmetpt,genmetphi,leppt,lepphi,Upar,Uper,-3, 0, nJets)
                self.Recoil.CorrectType2(cmetptResUp,     cmetphiResUp,     genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 3, nJets)
                self.Recoil.CorrectType2(cmetptResDown,   cmetphiResDown,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0,-3, nJets)
                #
                event.cormet.setP4(ROOT.reco.Particle.LorentzVector(cmetpt*math.cos(cmetphi), cmetpt*math.sin(cmetphi), 0, cmetpt))
            pass
            
        pass
        
        ### fill the scale/resolution variables
        event.cormet.ptScaleUp = cmetptScaleUp
        event.cormet.ptScaleDown = cmetptScaleDown
        event.cormet.ptResUp = cmetptResUp
        event.cormet.ptResDown = cmetptResDown
        
        return True


setattr(RecoilAnalyzer,"defaultConfig", cfg.Analyzer(
    class_object = RecoilAnalyzer,
    processLine = '.L %s/src/DMPD/Heppy/python/tools/RECOIL/RecoilCorrector.hh+' % os.environ['CMSSW_BASE'],
    ref_recoilMC_file = '%s/src/DMPD/Heppy/python/tools/RECOIL/recoilfit_gjetsMC_Zu1_pf_v5.root' % os.environ['CMSSW_BASE'],
    ref_recoilData_file = '%s/src/DMPD/Heppy/python/tools/RECOIL/recoilfit_gjetsData_Zu1_pf_v5.root' % os.environ['CMSSW_BASE'],
    )
)
