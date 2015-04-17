#! /usr/bin/env python
import ROOT
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
from DMPD.Heppy.analyzers.monoXObjectsFormat import *
cfg.Analyzer.nosubdir=True

##############################
### TRIGGERANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.core.TriggerBitAnalyzer import TriggerBitAnalyzer
triggerAnalyzer= cfg.Analyzer(
    verbose=False,
    class_object=TriggerBitAnalyzer,
    #grouping several paths into a single flag
    # v* can be used to ignore the version of a path
    triggerBits={
    'MET':['HLT_PFHT350_PFMET120_NoiseCleaned_v1','HLT_PFMET170_NoiseCleaned_v1','HLT_PFMET120_NoiseCleaned_BTagCSV07_v1'],
    'JET':['HLT_PFJet260_v1'],
    },
#   processName='HLT',
#   outprefix='HLT'
    #setting 'unrollbits' to true will not only store the OR for each set of trigger bits but also the individual bits
    #caveat: this does not unroll the version numbers
    unrollbits=True
    )

##############################
### PILEUPANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
pileupAnalyzer = PileUpAnalyzer.defaultConfig

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
    inclusive_electron_id       = "POG_Cuts_ID_CSA14_25ns_v1_Veto",
    inclusive_electron_pt       = 5,
    inclusive_electron_eta      = 2.5,
    inclusive_electron_dxy      = 0.5,
    inclusive_electron_dz       = 1.0,
    inclusive_electron_lostHits = 1.0,

    ### Electron selection - Second step
    loose_electron_id           = "POG_Cuts_ID_CSA14_25ns_v1_Veto",
    loose_electron_pt           = 10,
    loose_electron_eta          = 2.5,
    loose_electron_dxy          = 0.05,
    loose_electron_dz           = 0.2,
    loose_electron_lostHits     = 1.0,
    loose_electron_relIso       = 0.15,

    ### Muon - General
    ##############################
    muons                       = 'slimmedMuons',
    rhoMuon                     = 'fixedGridRhoFastjetAll',
    mu_isoCorr                  = "deltaBeta" ,
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
    loose_muon_relIso           = 0.2
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
    jetPt                       = 30.,
    jetEta                      = 4.7,
    jetEtaCentral               = 2.5,
    jetLepDR                    = 0.4,
    jetLepArbitration           = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps -> keeping the lepton
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

from PhysicsTools.Heppy.analyzers.objects.FatJetAnalyzer import FatJetAnalyzer
fatJetAnalyzer = cfg.Analyzer(

    class_object                = FatJetAnalyzer,

    ### Jet - General
    ##############################
    jetCol                      = 'slimmedJetsAK8',
    jetPt                       = 50.,
    jetEta                      = 4.7,
    jetEtaCentral               = 2.5,
    jetLepDR                    = 0.8,
    jetLepArbitration           = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps -> keeping the lepton
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
    ptMin                       = 15.,
    etaMax                      = 2.5,
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

### GLOBAL CUTS
met_pt_cut = 100. # met or fakemet
jet_met_deltaphi_cut = 0. # wrt met or fakemet

from DMPD.Heppy.analyzers.PreselectionAnalyzer import PreselectionAnalyzer
PreselectionAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = PreselectionAnalyzer,
    jet1_pt = 100.,
    jet1_eta = 2.5,
    jet1_tag = -1e99,
    jet1_chf_min = 0.2,
    jet1_nhf_max = 0.7,
    jet1_phf_max = 0.7,
    jet2_pt = 30.,
    jet2_eta = 2.5,
    jet2_tag = -1e99,
    deltaPhi12 = 2.5,
    fatjet_pt = 250.,
    jetveto_pt = 0.,
    jetveto_eta = 2.5,
    )

from DMPD.Heppy.analyzers.SRAnalyzer import SRAnalyzer
SRAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = SRAnalyzer,
    met_pt = met_pt_cut,
    deltaPhi1met = jet_met_deltaphi_cut,
    )

from DMPD.Heppy.analyzers.ZAnalyzer import ZAnalyzer
ZAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = ZAnalyzer,
    fakemet_pt = met_pt_cut,
    deltaPhi1met = jet_met_deltaphi_cut,

    mass_low = 50.,
    mass_high = 9e99,
    mu1_pt = 20.,
    mu1_id = "POG_ID_Tight",
    mu2_pt = 10.,
    mu2_id = "POG_ID_Loose",
    ele1_pt = 20.,
    ele1_id = "POG_Cuts_ID_CSA14_25ns_v1_Medium",
    ele2_pt = 10.,
    ele2_id = "POG_Cuts_ID_CSA14_25ns_v1_Medium",
    )

from DMPD.Heppy.analyzers.WAnalyzer import WAnalyzer
WAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = WAnalyzer,
    fakemet_pt = met_pt_cut,
    deltaPhi1met = jet_met_deltaphi_cut,
    
    mt_low = 50.,
    mt_high = 9e99,
    mu_pt = 20., 
    mu_id = "POG_ID_Tight",    
    )

from DMPD.Heppy.analyzers.GammaAnalyzer import GammaAnalyzer
GammaAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = GammaAnalyzer,
    fakemet_pt = met_pt_cut,
    deltaPhi1met = jet_met_deltaphi_cut,
    photon_pt = 175.,
    photon_id = "PhotonCutBasedIDLoose",
#    photon_eta = 2.5,
#    photon_eta_remove_min = 1.442,
#    photon_eta_remove_max = 1.56,
    )

globalVariables = [
    NTupleVariable("isSR",  lambda x: x.isSR, int, help="Signal Region flag"),
    NTupleVariable("isZCR",  lambda x: x.isZCR, int, help="Z+jets Control Region flag"),
    NTupleVariable("isWCR",  lambda x: x.isWCR, int, help="W+jets Control Region flag"),
    NTupleVariable("isGCR",  lambda x: x.isGCR, int, help="Gamma+jets Control Region flag"),
    NTupleVariable("Cat",  lambda x: x.Category, int, help="Signal Region Category 1/2/3"),
    NTupleVariable("nMuons",  lambda x: len(x.selectedMuons), int, help="Number of selected muons"),
    NTupleVariable("nElectrons",  lambda x: len(x.selectedElectrons), int, help="Number of selected electrons"),
    NTupleVariable("nTaus",  lambda x: len(x.selectedTaus), int, help="Number of selected taus"),
    NTupleVariable("nPhotons",  lambda x: len(x.selectedPhotons), int, help="Number of selected photons"),
    NTupleVariable("nJets",  lambda x: len(x.cleanJets) if not x.Category==1 else len(x.cleanFatJets), int, help="Number of cleaned jets"),
    NTupleVariable("nBJets",  lambda x: len([jet for jet in x.cleanJets if abs(jet.partonFlavour()) == 5]), int, help="Number of cleaned jets"),
]


##############################
### SIGNAL REGION TREE     ###
##############################

SignalRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='SignalRegionTreeProducer',
    treename='SR',
    filter = lambda x: x.isSR,
    verbose=False,
    vectorTree = True,
    globalVariables = globalVariables,
    globalObjects = {
        #"jet1" : NTupleObject("jet1", jetType, help="leading jet"),
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        },
    collections = {
      #"selectedMuons"     : NTupleCollection("muon", muonType, 3, help="Muons after the preselection"),
      #"selectedElectrons" : NTupleCollection("electron", electronType, 3, help="Electrons after the preselection"),
      #"selectedTaus"      : NTupleCollection("tau", tauType, 3, help="Taus after the preselection"),
      #"selectedPhotons"   : NTupleCollection("photon", photonType, 3, help="Photons after the preselection"),
      "Jets"              : NTupleCollection("jet", jetType, 4, help="Jets after the preselection"),
      }
    )


##############################
### G CONTROL REGION TREE  ###
##############################

GammaControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='GammaControlRegionTreeProducer',
    treename='GCR',
    filter = lambda x: x.isGCR,
    verbose=False,
    vectorTree = True,
    globalVariables = globalVariables,
    globalObjects = {
        #"photon1" : NTupleObject("photon1", photonType, help="leading photon"),
        #"jet1" : NTupleObject("jet1", jetType, help="leading jet"),
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        "fakemet" : NTupleObject("fakemet", fourVectorType, help="fake MET in gamma + jets event obtained removing the photon"),
        },
    collections = {
      #"selectedMuons"     : NTupleCollection("muon", muonType, 3, help="Muons after the preselection"),
      #"selectedElectrons" : NTupleCollection("electron", electronType, 3, help="Electrons after the preselection"),
      #"selectedTaus"      : NTupleCollection("tau", tauType, 3, help="Taus after the preselection"),
      "selectedPhotons"   : NTupleCollection("photon", photonType, 1, help="Photons after the preselection"),
      "Jets"              : NTupleCollection("jet", jetType, 4, help="Jets after the preselection"),
      }
    )


##############################
### W CONTROL REGION TREE  ###
##############################

WControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='WControlRegionTreeProducer',
    treename='WCR',
    filter = lambda x: x.isWCR,
    verbose=False,
    vectorTree = True,
    globalVariables = globalVariables,
    globalObjects = {
#        "muon1" : NTupleObject("muon1", leptonType, help="leading muon"),
#        "jet1" : NTupleObject("jet1", jetType, help="leading jet"),
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        "fakemet" : NTupleObject("fakemet", fourVectorType, help="fake MET in W -> mu nu event obtained removing the muon"),
        "W" : NTupleObject("W", compositeType, help="W boson candidate"),
        },
    collections = {
      "selectedMuons"     : NTupleCollection("muon", muonType, 1, help="Muons after the preselection"),
      #"selectedElectrons" : NTupleCollection("electron", electronType, 3, help="Electrons after the preselection"),
      #"selectedTaus"      : NTupleCollection("tau", tauType, 3, help="Taus after the preselection"),
      #"selectedPhotons"   : NTupleCollection("photon", photonType, 3, help="Photons after the preselection"),
      "Jets"              : NTupleCollection("jet", jetType, 4, help="Jets after the preselection"),
      }
    )
    
    
##############################
### Z CONTROL REGION TREE  ###
##############################

ZControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='ZControlRegionTreeProducer',
    treename='ZCR',
    filter = lambda x: x.isZCR,
    verbose=False,
    vectorTree = True,
    globalVariables = globalVariables + [
        NTupleVariable("isZtoMM",  lambda x: x.isZtoMM, int, help="Z -> mu mu flag")
    ],
    globalObjects = {
#        "lepton1" : NTupleObject("lepton1", leptonType, help="leading lepton"),
#        "lepton2" : NTupleObject("lepton2", leptonType, help="subleading lepton"),
#        "jet1" : NTupleObject("jet1", jetType, help="leading jet"),
        "met" : NTupleObject("met",  metType, help="PF E_{T}^{miss}, after default type 1 corrections"),
        "fakemet" : NTupleObject("fakemet", fourVectorType, help="fake MET in Z events obtained removing the muons"),
        "Z" : NTupleObject("Z", compositeType, help="Z boson candidate"),
        "A" : NTupleObject("A", compositeType, help="A boson candidate"),
        },
    collections = {
      "Leptons"           : NTupleCollection("lepton", muonType, 2, help="Muons and Electrons after the preselection"),
      #"selectedMuons"     : NTupleCollection("muon", muonType, 4, help="Muons after the preselection"),
      #"selectedElectrons" : NTupleCollection("electron", electronType, 4, help="Electrons after the preselection"),
      #"selectedTaus"      : NTupleCollection("tau", tauType, 3, help="Taus after the preselection"),
      #"selectedPhotons"   : NTupleCollection("photon", photonType, 3, help="Photons after the preselection"),
      "Jets"              : NTupleCollection("jet", jetType, 4, help="Jets after the preselection"),
      }
    )    


##############################
### SEQUENCE               ###
##############################

sequence = [
    triggerAnalyzer,
    pileupAnalyzer,
    vertexAnalyzer,
    leptonAnalyzer,
    jetAnalyzer,
    fatJetAnalyzer,
    tauAnalyzer,
    photonAnalyzer,
    MEtAnalyzer,
    ### Preselection Analyzers
    PreselectionAnalyzer,
    ### Analysis Analyzers
    SRAnalyzer,
    GammaAnalyzer,
    WAnalyzer,
    ZAnalyzer,
    ### Tree producers
    SignalRegionTreeProducer,
    GammaControlRegionTreeProducer,
    WControlRegionTreeProducer, 
    ZControlRegionTreeProducer,
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
from DMPD.Heppy.samples.Phys14.fileLists import samples

sampleTest = cfg.Component(
    files = ["file:/lustre/cmswork/zucchett/CMSSW_7_2_0_patch1/src/Buggy/M2000/MINIAODSIM.root"],
    #files = ["dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/Phys14DR/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/021C8316-1E71-E411-8CBD-0025901D484C.root"],
    name="Test",
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleQCD_HT100To250 = cfg.Component(
    ### QCD
    files = samples['QCD_HT100To250']['files'],
    name="QCD_HT100To250",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleQCD_HT250To500 = cfg.Component(
    ### QCD
    files = samples['QCD_HT250To500']['files'],
    name="QCD_HT250To500",
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleQCD_HT500To1000 = cfg.Component(
    ### QCD
    files = samples['QCD_HT500To1000']['files'],
    name="QCD_HT500To1000",
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleQCD_HT1000ToInf = cfg.Component(
    ### QCD
    files = samples['QCD_HT1000ToInf']['files'],
    name="QCD_HT1000ToInf",
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleDYJetsToLL_M50_HT100to200 = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT100to200']['files'],
    name="DYJetsToLL_M50_HT100to200",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleDYJetsToLL_M50_HT200to400 = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT200to400']['files'],
    name="DYJetsToLL_M50_HT200to400",
    isMC=True,
    isEmbed=False,
    splitFactor=8
    )

sampleDYJetsToLL_M50_HT400to600 = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT400to600']['files'],
    name="DYJetsToLL_M50_HT400to600",
    isMC=True,
    isEmbed=False,
    splitFactor=8
    )

sampleDYJetsToLL_M50_HT600toInf = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT600toInf']['files'],
    name="DYJetsToLL_M50_HT600toInf",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleGJets_HT100to200 = cfg.Component(
    ### GJets
    files = samples['GJets_HT100to200']['files'],
    name="GJets_HT100to200",
    isMC=True,
    isEmbed=False,
    splitFactor=8
    )

sampleGJets_HT200to400 = cfg.Component(
    ### GJets
    files = samples['GJets_HT200to400']['files'],
    name="GJets_HT200to400",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleGJets_HT400to600 = cfg.Component(
    ### GJets
    files = samples['GJets_HT400to600']['files'],
    name="GJets_HT400to600",
    isMC=True,
    isEmbed=False,
    splitFactor=8
    )

sampleGJets_HT600toInf = cfg.Component(
    ### GJets
    files = samples['GJets_HT600toInf']['files'],
    name="GJets_HT600toInf",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleTT = cfg.Component(
    ### TT
    files = samples['TT']['files'],
    name="TT",
    isMC=True,
    isEmbed=False,
    splitFactor=5
    )

sampleTToLeptons_schannel = cfg.Component(
    ### TToLeptons_schannel
    files = samples['TToLeptons_schannel']['files'],
    name="TToLeptons_schannel",
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleTToLeptons_tchannel = cfg.Component(
    ### TToLeptons_tchannel
    files = samples['TToLeptons_tchannel']['files'],
    name="TToLeptons_tchannel",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleT_tWchannel = cfg.Component(
    ### SingleT
    files = samples['T_tWchannel']['files'],
    name="T_tWchannel",
    isMC=True,
    isEmbed=False,
    splitFactor=2
    )

sampleTbar_tWchannel = cfg.Component(
    ### SingleT
    files = samples['Tbar_tWchannel']['files'],
    name="Tbar_tWchannel",
    isMC=True,
    isEmbed=False,
    splitFactor=2
    )

sampleWJetsToLNu_HT100to200 = cfg.Component(
    ### WJetsToLNu
    files = samples['WJetsToLNu_HT100to200']['files'],
    name="WJetsToLNu_HT100to200",
    isMC=True,
    isEmbed=False,
    splitFactor=8
    )

sampleWJetsToLNu_HT200to400 = cfg.Component(
    ### WJetsToLNu
    files = samples['WJetsToLNu_HT200to400']['files'],
    name="WJetsToLNu_HT200to400",
    isMC=True,
    isEmbed=False,
    splitFactor=8
    )

sampleWJetsToLNu_HT400to600 = cfg.Component(
    ### WJetsToLNu
    files = samples['WJetsToLNu_HT400to600']['files'],
    name="WJetsToLNu_HT400to600",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleWJetsToLNu_HT600toInf = cfg.Component(
    ### WJetsToLNu
    files = samples['WJetsToLNu_HT600toInf']['files'],
    name="WJetsToLNu_HT600toInf",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleZJetsToNuNu_HT100to200 = cfg.Component(
    ### ZJetsToNuNu
    files = samples['ZJetsToNuNu_HT100to200']['files'],
    name="ZJetsToNuNu_HT100to200",
    isMC=True,
    isEmbed=False,
    splitFactor=8
    )

sampleZJetsToNuNu_HT200to400 = cfg.Component(
    ### ZJetsToNuNu
    files = samples['ZJetsToNuNu_HT200to400']['files'],
    name="ZJetsToNuNu_HT200to400",
    isMC=True,
    isEmbed=False,
    splitFactor=8
    )

sampleZJetsToNuNu_HT400to600 = cfg.Component(
    ### ZJetsToNuNu
    files = samples['ZJetsToNuNu_HT400to600']['files'],
    name="ZJetsToNuNu_HT400to600",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

sampleZJetsToNuNu_HT600toInf = cfg.Component(
    ### ZJetsToNuNu
    files = samples['ZJetsToNuNu_HT600toInf']['files'],
    name="ZJetsToNuNu_HT600toInf",
    isMC=True,
    isEmbed=False,
    splitFactor=7
    )

##############################
### FWLITE                 ###
##############################
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
preprocessor = CmsswPreprocessor("tagFatJets.py")

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

#### TEST (LOCAL)
selectedComponents = [sampleTest]

#### FULL QCD
#selectedComponents = [sampleQCD_HT100To250,sampleQCD_HT250To500,sampleQCD_HT500To1000,sampleQCD_HT_1000ToInf] 

#### FULL DYJetsToLL
#selectedComponents = [sampleDYJetsToLL_M50_HT100to200,sampleDYJetsToLL_M50_HT200to400,sampleDYJetsToLL_M50_HT400to600,sampleDYJetsToLL_M50_HT600toInf] 

#### FULL GJets
#selectedComponents = [sampleGJets_HT100to200,sampleGJets_HT200to400,sampleGJets_HT400to600,sampleGJets_HT600toInf] 

#### FULL TT
#selectedComponents = [sampleTT] 

#### FULL T
#selectedComponents = [sampleT_tWchannel,sampleTbar_tWchannel,sampleTToLeptons_schannel,sampleTToLeptons_tchannel] 

#### FULL WJetsToLNu
#selectedComponents = [sampleWJetsToLNu_HT100to200,sampleWJetsToLNu_HT200to400,sampleWJetsToLNu_HT400to600,sampleWJetsToLNu_HT600toInf] 

#### FULL ZJetsToNuNu
#selectedComponents = [sampleZJetsToNuNu_HT100to200,sampleZJetsToNuNu_HT200to400,sampleZJetsToNuNu_HT400to600,sampleZJetsToNuNu_HT600toInf] 


#### SINGLE COMPONENTS
#selectedComponents = [sampleQCD_HT100To250]
#selectedComponents = [sampleQCD_HT250To500]
#selectedComponents = [sampleQCD_HT500To1000]
#selectedComponents = [sampleQCD_HT_1000ToInf]
#selectedComponents = [sampleTT]
#selectedComponents = [sampleT_tWchannel]
#selectedComponents = [sampleTbar_tWchannel]
#selectedComponents = [sampleTToLeptons_schannel]
#selectedComponents = [sampleTToLeptons_tchannel] 

#selectedComponents = [sampleDYJetsToLL_M50_HT100to200]
#selectedComponents = [sampleDYJetsToLL_M50_HT200to400]
#selectedComponents = [sampleDYJetsToLL_M50_HT400to600]
#selectedComponents = [sampleDYJetsToLL_M50_HT600toInf] 

#selectedComponents = [sampleGJets_HT100to200]
#selectedComponents = [sampleGJets_HT200to400]
#selectedComponents = [sampleGJets_HT400to600]
#selectedComponents = [sampleGJets_HT600toInf]

#selectedComponents = [sampleWJetsToLNu_HT100to200]
#selectedComponents = [sampleWJetsToLNu_HT200to400]
#selectedComponents = [sampleWJetsToLNu_HT400to600]
#selectedComponents = [sampleWJetsToLNu_HT600toInf]

#selectedComponents = [sampleZJetsToNuNu_HT100to200]
#selectedComponents = [sampleZJetsToNuNu_HT200to400]
#selectedComponents = [sampleZJetsToNuNu_HT400to600]
#selectedComponents = [sampleZJetsToNuNu_HT600toInf] 

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [output_service],
    #preprocessor = preprocessor,
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
