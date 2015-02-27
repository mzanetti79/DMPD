#! /usr/bin/env python
import ROOT
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
from DMPD.Heppy.analyzers.monoXObjectsFormat import *
cfg.Analyzer.nosubdir=True

#collections = {
#      "selectedMuons"     : NTupleCollection("muons", muonType, 3, help="Muons after the preselection"),
#      "selectedElectrons" : NTupleCollection("electrons", electronType, 3, help="Electrons after the preselection"),
#      "selectedTaus"      : NTupleCollection("taus", tauType, 3, help="Taus after the preselection"),
#      "selectedPhotons"   : NTupleCollection("photons", photonType, 3, help="Photons after the preselection"),
#      "cleanJets"         : NTupleCollection("jets", jetType, 3, help="Jets after the preselection"),
#      }

##############################
### SIGNAL REGION TREE     ###
##############################

SignalRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='SignalRegionTreeProducer',
    treename='SR',
    verbose=False,
    vectorTree = True,
    globalObjects = {
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        },
    collections = {
      #"selectedMuons"     : NTupleCollection("muons", muonType, 3, help="Muons after the preselection"),
      #"selectedElectrons" : NTupleCollection("electrons", electronType, 3, help="Electrons after the preselection"),
      #"selectedTaus"      : NTupleCollection("taus", tauType, 3, help="Taus after the preselection"),
      #"selectedPhotons"   : NTupleCollection("photons", photonType, 3, help="Photons after the preselection"),
      "cleanJets"         : NTupleCollection("jets", jetType, 3, help="Jets after the preselection"),
      }
    )


##############################
### Z CONTROL REGION TREE  ###
##############################

ZControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='ZControlRegionTreeProducer',
    treename='ZCR',
    verbose=False,
    vectorTree = True,
    globalObjects = {
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        "fakeMEt" : NTupleObject("fakeMEt", fourVectorType, help="fake MET in Z -> mu mu event obtained removing the muons"),
        "Z" : NTupleObject("Z", fourVectorType, help="Z boson candidate"),
        },
    collections = {
      "selectedMuons"     : NTupleCollection("muons", muonType, 2, help="Muons after the preselection"),
      #"selectedElectrons" : NTupleCollection("electrons", electronType, 3, help="Electrons after the preselection"),
      #"selectedTaus"      : NTupleCollection("taus", tauType, 3, help="Taus after the preselection"),
      #"selectedPhotons"   : NTupleCollection("photons", photonType, 3, help="Photons after the preselection"),
      "cleanJets"         : NTupleCollection("jets", jetType, 3, help="Jets after the preselection"),
      }
    )
    

##############################
### W CONTROL REGION TREE  ###
##############################

WControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='WControlRegionTreeProducer',
    treename='WCR',
    verbose=False,
    vectorTree = True,
    globalObjects = {
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        "fakeMEt" : NTupleObject("fakeMEt", fourVectorType, help="fake MET in W -> mu nu event obtained removing the muon"),
        "W" : NTupleObject("W", fourVectorType, help="W boson candidate"),
        },
    collections = {
      "selectedMuons"     : NTupleCollection("muons", muonType, 1, help="Muons after the preselection"),
      #"selectedElectrons" : NTupleCollection("electrons", electronType, 3, help="Electrons after the preselection"),
      #"selectedTaus"      : NTupleCollection("taus", tauType, 3, help="Taus after the preselection"),
      #"selectedPhotons"   : NTupleCollection("photons", photonType, 3, help="Photons after the preselection"),
      "cleanJets"         : NTupleCollection("jets", jetType, 3, help="Jets after the preselection"),
      }
    )
    
##############################
### G CONTROL REGION TREE  ###
##############################

GammaControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='GammaControlRegionTreeProducer',
    treename='GCR',
    verbose=False,
    vectorTree = True,
    globalObjects = {
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        "fakeMEt" : NTupleObject("fakeMEt", fourVectorType, help="fake MET in gamma + jets event obtained removing the photon"),
        },
    collections = {
      #"selectedMuons"     : NTupleCollection("muons", muonType, 3, help="Muons after the preselection"),
      #"selectedElectrons" : NTupleCollection("electrons", electronType, 3, help="Electrons after the preselection"),
      #"selectedTaus"      : NTupleCollection("taus", tauType, 3, help="Taus after the preselection"),
      "selectedPhotons"   : NTupleCollection("photons", photonType, 1, help="Photons after the preselection"),
      "cleanJets"         : NTupleCollection("jets", jetType, 3, help="Jets after the preselection"),
      }
    )


##############################
### PILEUPANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
pilupeAnalyzer = PileUpAnalyzer.defaultConfig

##############################
### VERTEXANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
vertexAnalyzer = VertexAnalyzer.defaultConfig

##############################
### LEPTONANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.objects.LeptonAnalyzer import LeptonAnalyzer
leptonAnalyzer = cfg.Analyzer(

    class_object                = LeptonAnalyzer,

    ### Lepton - General
    ##############################
    doMuScleFitCorrections      = False, # "rereco"
    doRochesterCorrections      = False,
    doElectronScaleCorrections  = False, # "embedded" in 5.18 for regression
    doSegmentBasedMuonCleaning  = False,
    # minimum deltaR between a loose electron and a loose muon (on overlaps, discard the electron)
    min_dr_electron_muon        = 0.02,
    # do MC matching
    do_mc_match                 = True, # note: it will in any case try it only on MC, not on data

    ### Electron - General
    ##############################
    electrons                   = 'slimmedElectrons',
    rhoElectron                 = 'fixedGridRhoFastjetAll',
    ele_isoCorr                 = "rhoArea",
    el_effectiveAreas           = "Phys14_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1')
    ele_tightId                 = "Cuts_2012",

    ### Electron selection - First step
    inclusive_electron_id       = "",
    inclusive_electron_pt       = 5,
    inclusive_electron_eta      = 2.5,
    inclusive_electron_dxy      = 0.5,
    inclusive_electron_dz       = 1.0,
    inclusive_electron_lostHits = 1.0,

    ### Electron selection - Second step
    loose_electron_id           = "POG_Cuts_ID_CSA14_25ns_v1_Veto",
    loose_electron_pt           = 10,
    loose_electron_eta          = 2.4,
    loose_electron_dxy          = 0.05,
    loose_electron_dz           = 0.2,
    loose_electron_relIso       = 0.4,
    loose_electron_lostHits     = 1.0,

    ### Muon - General
    ##############################
    muons                       = 'slimmedMuons',
    rhoMuon                     = 'fixedGridRhoFastjetAll',
    mu_isoCorr                  = "rhoArea" ,
    mu_effectiveAreas           = "Phys14_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1')

    ### Muon selection - First step
    inclusive_muon_id           = "POG_ID_Loose",
    inclusive_muon_pt           = 3,
    inclusive_muon_eta          = 2.4,
    inclusive_muon_dxy          = 0.5,
    inclusive_muon_dz           = 1.0,

    ### Muon selection - Second step
    loose_muon_id               = "POG_ID_Loose",
    loose_muon_pt               = 10,
    loose_muon_eta              = 2.4,
    loose_muon_dxy              = 0.05,
    loose_muon_dz               = 0.2,
    loose_muon_relIso           = 0.4
    ### ====================== ###
    )

##############################
### JETANALYZER            ###
##############################
from PhysicsTools.Heppy.analyzers.objects.JetAnalyzer import JetAnalyzer
jetAnalyzer = cfg.Analyzer(

    class_object                = JetAnalyzer,

    ### Jet - General
    ##############################
    jetCol                      = 'slimmedJets',
    jetPt                       = 20.,
    jetEta                      = 4.7,
    jetEtaCentral               = 2.4,
    jetLepDR                    = 0.4,
    jetLepArbitration           = (lambda jet,lepton : jet), # you can decide which to keep in case of overlaps -> keeping the jet
    minLepPt                    = 10,
    relaxJetId                  = False,
    doPuId                      = False, # Not commissioned in 7.0.X
    doQG                        = False,
    recalibrateJets             = False,
    shiftJEC                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    smearJets                   = True,
    shiftJER                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    cleanJetsFromFirstPhoton    = False,
    cleanJetsFromTaus           = False,
    cleanJetsFromIsoTracks      = False,
    jecPath                     = ""
    ### ====================== ###
    )
    
fatJetAnalyzer = cfg.Analyzer(

    class_object                = JetAnalyzer,

    ### Jet - General
    ##############################
    jetCol                      = 'slimmedJetsAK8',
    jetPt                       = 50.,
    jetEta                      = 4.7,
    jetEtaCentral               = 2.4,
    jetLepDR                    = 0.4,
    jetLepArbitration           = (lambda jet,lepton : jet), # you can decide which to keep in case of overlaps -> keeping the jet
    minLepPt                    = 10,
    relaxJetId                  = False,
    doPuId                      = False, # Not commissioned in 7.0.X
    doQG                        = False,
    recalibrateJets             = False,
    shiftJEC                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    smearJets                   = True,
    shiftJER                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    cleanJetsFromFirstPhoton    = False,
    cleanJetsFromTaus           = False,
    cleanJetsFromIsoTracks      = False,
    jecPath                     = ""
    ### ====================== ###
    )

##############################
### TAUANALYZER            ###
##############################
from PhysicsTools.Heppy.analyzers.objects.TauAnalyzer import TauAnalyzer
tauAnalyzer = cfg.Analyzer(

    class_object                = TauAnalyzer,

    ### Tau - General
    ##############################
    ptMin                       = 20,
    etaMax                      = 9999,
    dxyMax                      = 1000.,
    dzMax                       = 0.2,
    vetoLeptons                 = True,
    leptonVetoDR                = 0.4,
    decayModeID                 = "decayModeFindingNewDMs", # ignored if not set or ""
    tauID                       = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    vetoLeptonsPOG              = False, # If True, the following two IDs are required
    tauAntiMuonID               = "againstMuonLoose3",
    tauAntiElectronID           = "againstElectronLooseMVA5",
    tauLooseID                  = "decayModeFinding",
    ### ====================== ###
    )

##############################
### PHOTONANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.objects.PhotonAnalyzer import PhotonAnalyzer
photonAnalyzer = cfg.Analyzer(

    class_object                = PhotonAnalyzer,

    ### Photon - General
    ##############################
    photons                     = 'slimmedPhotons',
    ptMin                       = 10,
    etaMax                      = 2.5,
    gammaID                     = "PhotonCutBasedIDLoose",
    do_mc_match                 = True,
    ### ====================== ###
    )

##############################
### METANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.objects.METAnalyzer import METAnalyzer
MEtAnalyzer = METAnalyzer.defaultConfig

##############################
### DM ANALYZERS           ###
##############################

from DMPD.Heppy.analyzers.PreselectionAnalyzer import PreselectionAnalyzer
PreselectionAnalyzer = cfg.Analyzer(
   verbose = False,
   class_object = PreselectionAnalyzer,
   jet_pt = 80.,
   met_pt = 80.,
   )

from DMPD.Heppy.analyzers.SRAnalyzer import SRAnalyzer
SRAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = SRAnalyzer,
    jet1_pt = 150.,
    jet1_eta = 2.0,
    jet1_tag = -99.,
    jet2_pt = 30.,
    jet2_eta = 2.5,
    jet2_tag = -99.,
    deltaPhi12 = 2.,
    jetveto_pt = 20.,
    jetveto_eta = 2.5,
    met_pt = 100.,
    )

from DMPD.Heppy.analyzers.ZAnalyzer import ZAnalyzer
ZAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = ZAnalyzer,
    mass_low = 61.,
    mass_high = 121.,
    mu1_pt = 0., # cut implemented in the Analyzer
    mu1_id = "POG_ID_Tight",
    jet_pt = 100.,
    met_pt = 100.,
    )

from DMPD.Heppy.analyzers.WAnalyzer import WAnalyzer
WAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = WAnalyzer,
    mt_low = 50.,
    mt_high = 100.,
    mu_pt = 20., 
    mu_id = "POG_ID_Tight",    
    jet_pt = 100.,
    met_pt = 100.,
    )

from DMPD.Heppy.analyzers.GammaAnalyzer import GammaAnalyzer
GammaAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = GammaAnalyzer,
    photon_pt = 160.,
    photon_id = "PhotonCutBasedIDLoose",
    photon_eta = 2.5,
    photon_eta_remove_min = 1.442,
    photon_eta_remove_max = 1.56,
    jet_pt = 100.,
    met_pt = 100.,
    )

##############################
### SEQUENCE               ###
##############################
sequence = [
    pilupeAnalyzer, 
    vertexAnalyzer, 
    leptonAnalyzer, 
    jetAnalyzer, 
    #fatJetAnalyzer,
    tauAnalyzer, 
    photonAnalyzer, 
    MEtAnalyzer, 
    #### Preselection (Jet+Met)
    #PreselectionAnalyzer, 
    #### Gamma
    #GammaAnalyzer,
    #GammaControlRegionTreeProducer,
    #### Zmm
    #ZAnalyzer,
    #ZControlRegionTreeProducer,
    #### Wmn
    #WAnalyzer, 
    #WControlRegionTreeProducer,
    #### SignalRegion
    SRAnalyzer, 
    SignalRegionTreeProducer,
    ]

##############################
### TFILESERVICE           ###
##############################
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='tree.root',
    option='recreate'
    )

##############################
### INPUT                  ###
##############################
from PhysicsTools.Heppy.utils.miniAodFiles import miniAodFiles
#from DMPD.Heppy.samples.Phys14 import fileLists

sample = cfg.Component(
    files = ["file:/lustre/cmswork/zucchett/CMSSW_7_2_0_patch1/src/MINIAODSIM.root"],
    #files = ["dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/Phys14DR/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/021C8316-1E71-E411-8CBD-0025901D484C.root"],
    ### QCD
    #files = fileLists.QCD_HT100To250+
             #fileLists.QCD_HT250To500+
             #fileLists.QCD_HT500To1000+
             #fileLists.QCD_HT_1000ToInf,
    ### DYJetsToLL
    #files = fileLists.DYJetsToLL_M50_HT100to200+
            #fileLists.DYJetsToLL_M50_HT200to400+
            #fileLists.DYJetsToLL_M50_HT400to600+
            #fileLists.DYJetsToLL_M50_HT600toInf,
    ### GJets
    #files = fileLists.GJets_HT100to200+
    #        fileLists.GJets_HT200to400+
    #        fileLists.GJets_HT400to600+
    #        fileLists.GJets_HT600toInf,
    ### TTbar
    #files = fileLists.TT+
            #fileLists.TToLeptons_schannel+
            #fileLists.TToLeptons_tchannel,
    ### SingleT
    #files = fileLists.T_tWchannel+
            #fileLists.Tbar_tWchannel,
    ### WJetsToLNu
    #files = fileLists.WJetsToLNu_HT100to200+
            #fileLists.WJetsToLNu_HT200to400+
            #fileLists.WJetsToLNu_HT400to600+
            #fileLists.WJetsToLNu_HT600toInf,
    ### ZJetsToNuNu
    #files = fileLists.ZJetsToNuNu_HT100to200+
            #fileLists.ZJetsToNuNu_HT200to400+
            #fileLists.ZJetsToNuNu_HT400to600+
            #fileLists.ZJetsToNuNu_HT600toInf,
    name="GJets",
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

##############################
### FWLITE                 ###
##############################
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
preprocessor = CmsswPreprocessor("tagFatJets.py")

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
selectedComponents = [sample]
config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [output_service],
    #preprocessor=preprocessor,
    events_class = Events
    )

##############################
### LOOPER                 ###
##############################
# and the following runs the process directly if running as with python filename.py
if __name__ == '__main__':
    from PhysicsTools.HeppyCore.framework.looper import Looper
    looper = Looper(
        'MonoX',
        config,
        nPrint = 0,
        nEvents=1000,
        )
    looper.loop()
    looper.write()
