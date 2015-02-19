#! /usr/bin/env python
import ROOT
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 
from DMPD.Heppy.analyzers.monoXObjectsFormat import *
cfg.Analyzer.nosubdir=True
zjetsTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer, 
    name='zjetsTreeProducer',
    treename='treeZjets',
    verbose=False, 
    vectorTree = True,
    globalObjects = {
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        "fakeMET" : NTupleObject("fakeMET", fourVectorType, help="fake MET in Zmumu event obtained removing the muons"),
        "Z" : NTupleObject("Z", fourVectorType, help="Z boson"),
        },
    collections = {
        "selectedMuons" : NTupleCollection("muons", muonType, 3, help="Muons after the preselection"),
        }
    )

from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
pilupeAnalyzer = PileUpAnalyzer.defaultConfig
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
vertexAnalyzer = VertexAnalyzer.defaultConfig
from DMPD.Heppy.selectors.MuonAnalyzer import MuonAnalyzer
muonAnalyzer = MuonAnalyzer.defaultConfig
from DMPD.Heppy.analyzers.ZmmAnalyzer import ZmmAnalyzer
zmmAnalyzer = cfg.Analyzer(verbose=False, class_object=ZmmAnalyzer)

sequence = [pilupeAnalyzer, vertexAnalyzer, muonAnalyzer, zmmAnalyzer, zjetsTreeProducer]

from PhysicsTools.HeppyCore.framework.services.tfile import TFileService 
output_service = cfg.Service(
      TFileService,
      'outputfile',
      name="outputfile",
      fname='tree.root',
      option='recreate'
    )

from PhysicsTools.Heppy.utils.miniAodFiles import miniAodFiles
sample = cfg.Component(
    files = miniAodFiles(),
    name="SingleSample", isMC=False,isEmbed=False
    )

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
selectedComponents = [sample]
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [output_service],  
                     events_class = Events)

# and the following runs the process directly if running as with python filename.py  
if __name__ == '__main__':
    from PhysicsTools.HeppyCore.framework.looper import Looper 
    looper = Looper( 'MonoX', config, nPrint = 5,nEvents=300) 
    looper.loop()
    looper.write()
