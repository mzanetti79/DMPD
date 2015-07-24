#! /usr/bin/env python
import ROOT
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
from DMPD.Heppy.analyzers.ObjectsFormat import *
cfg.Analyzer.nosubdir=True

##############################
### GENANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer import GeneratorAnalyzer
generatorAnalyzer= cfg.Analyzer(
    verbose=False,
    class_object=GeneratorAnalyzer,
    stableBSMParticleIds = [ 1000022, 9100000, 9100012, 9100022, -9100022, 9900032, 1023 ], # BSM particles that can appear with status <= 2 and should be kept
    # Particles of which we want to save the pre-FSR momentum (a la status 3).
    # Note that for quarks and gluons the post-FSR doesn't make sense,
    # so those should always be in the list
    savePreFSRParticleIds = [ 1,2,3,4,5, 11,12,13,14,15,16, 21 ],
    makeAllGenParticles = True, # Make also the list of all genParticles, for other analyzers to handle
    makeSplittedGenLists = True, # Make also the splitted lists
    allGenTaus = False,
    makeLHEweights = True,
    )

##############################
### TRIGGERANALYZER        ###
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
    # energy scale corrections and ghost muon suppression (off by default)
    doMuScleFitCorrections=False, # "rereco"
    doRochesterCorrections=False,
    doElectronScaleCorrections=False, # "embedded" in 5.18 for regression
    doSegmentBasedMuonCleaning=False,
    # minimum deltaR between a loose electron and a loose muon (on overlaps, discard the electron)
    min_dr_electron_muon        = 0.02,
    # do MC matching
    do_mc_match                 = True, # note: it will in any case try it only on MC, not on data
    match_inclusiveLeptons      = False, # match to all inclusive leptons

    ### Electron - General
    ##############################
    electrons                   = 'slimmedElectrons',
    rhoElectron                 = 'fixedGridRhoFastjetAll',
    #ele_isoCorr                 = 'deltaBeta',
    ele_isoCorr                 = 'rhoArea',
    el_effectiveAreas           = 'Phys14_25ns_v1', #(can be 'Data2012' or 'Phys14_25ns_v1')
    ele_tightId                 = 'POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Veto',

    ### Electron selection - First step
    inclusive_electron_id       = 'POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Veto',
    #inclusive_electron_id       = 'POG_Cuts_ID_PHYS14_25ns_v1_Veto',
    inclusive_electron_pt       = 10,
    inclusive_electron_eta      = 2.5,
    inclusive_electron_dxy      = 1.e99,
    inclusive_electron_dz       = 1.e99,
    inclusive_electron_lostHits = 9.0,
    inclusive_electron_isoCut   = lambda electron : ( ( electron.isEB() and electron.relIso03 < 0.158721 ) or  ( electron.isEE() and electron.relIso03 < 0.177032 ) ) ,
    inclusive_electron_relIso   = 1.e99,

    ### Electron selection - Second step
    loose_electron_id           = 'POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Veto',
    loose_electron_pt           = 10,
    loose_electron_eta          = 2.5,
    loose_electron_dxy          = 1.e99,
    loose_electron_dz           = 1.e99,
    loose_electron_lostHits     = 9.0,
    loose_electron_isoCut       = lambda electron : ( ( electron.isEB() and electron.relIso03 < 0.158721 ) or  ( electron.isEE() and electron.relIso03 < 0.177032 ) ) ,
    loose_electron_relIso       = 1.e99,

    ### Muon - General
    ##############################
    muons                       = 'slimmedMuons',
    rhoMuon                     = 'fixedGridRhoFastjetAll',
    mu_isoCorr                  = 'deltaBeta' ,
    mu_effectiveAreas           = 'Phys14_25ns_v1', #(can be 'Data2012' or 'Phys14_25ns_v1')
    muon_dxydz_track            = 'muonBestTrack',

    ### Muon selection - First step
    inclusive_muon_id           = 'POG_ID_Loose',
    inclusive_muon_pt           = 10,
    inclusive_muon_eta          = 2.4,
    inclusive_muon_dxy          = 1.e99,
    inclusive_muon_dz           = 1.e99,
    inclusive_muon_isoCut       = lambda muon : muon.relIso04 < 0.2,
    inclusive_muon_relIso       = 1.e99,

    ### Muon selection - Second step
    loose_muon_id               = 'POG_ID_Loose',
    loose_muon_pt               = 10,
    loose_muon_eta              = 2.4,
    loose_muon_dxy              = 1.e99,
    loose_muon_dz               = 1.e99,
    loose_muon_isoCut           = lambda muon : muon.relIso04 < 0.2,
    loose_muon_relIso           = 1.e99,

    # Mini-isolation, with pT dependent cone: will fill in the miniRelIso, miniRelIsoCharged, miniRelIsoNeutral variables of the leptons (see https://indico.cern.ch/event/368826/ )
    doMiniIsolation = True, # off by default since it requires access to all PFCandidates
    packedCandidates = 'packedPFCandidates',
    miniIsolationPUCorr = 'rhoArea', # Allowed options: 'rhoArea' (EAs for 03 cone scaled by R^2), 'deltaBeta', 'raw' (uncorrected), 'weights' (delta beta weights; not validated)
    miniIsolationVetoLeptons = None, # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
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
    jetLepArbitration           = (lambda jet,lepton : jet), # you can decide which to keep in case of overlaps -> keeping the jet -> resolving it later
    minLepPt                    = 10,
    relaxJetId                  = False,
    doPuId                      = True,
    doQG                        = False,
    recalibrateJets             = False,
    shiftJEC                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    smearJets                   = False,
    shiftJER                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    cleanJetsFromFirstPhoton    = False,
    cleanJetsFromTaus           = False,
    cleanJetsFromIsoTracks      = False,
    jecPath                     = '',

    genJetCol                   = 'slimmedGenJets',
    rho                         = ('fixedGridRhoFastjetAll','',''),
    copyJetsByValue             = False, #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    cleanSelectedLeptons        = False, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    lepSelCut                   = lambda lep : True,
    recalibrationType           = 'AK4PFchs',
    alwaysCleanPhotons          = False,
    cleanGenJetsFromPhoton      = False,
    collectionPostFix           = ''
    ### ====================== ###
    )

fatJetAnalyzer = cfg.Analyzer(

    class_object                = JetAnalyzer,

    ### Jet - General
    ##############################
    jetCol                      = 'slimmedJetsAK8',
    jetPt                       = 50.,
    jetEta                      = 4.7,
    jetEtaCentral               = 2.5,
    jetLepDR                    = 0.8,
    jetLepArbitration           = (lambda jet,lepton : jet), # you can decide which to keep in case of overlaps -> keeping the jet -> resolving it later
    minLepPt                    = 10,
    relaxJetId                  = False,
    doPuId                      = True, # Not commissioned in 7.0.X
    doQG                        = False,
    recalibrateJets             = False,
    shiftJEC                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    smearJets                   = False,
    shiftJER                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    cleanJetsFromFirstPhoton    = False,
    cleanJetsFromTaus           = False,
    cleanJetsFromIsoTracks      = False,
    jecPath                     = '',

    genJetCol                   = 'slimmedGenJets',
    rho                         = ('fixedGridRhoFastjetAll','',''),
    copyJetsByValue             = False, #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    cleanSelectedLeptons        = False, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    lepSelCut                   = lambda lep : True,
    recalibrationType           = 'AK8PFchs',
    alwaysCleanPhotons          = False,
    cleanGenJetsFromPhoton      = False,
    collectionPostFix           = 'AK8'
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
    inclusive_ptMin = 18,
    inclusive_etaMax = 2.3,
    inclusive_dxyMax = 1000.,
    inclusive_dzMax = 1000, #0.4,
    inclusive_vetoLeptons = False,
    inclusive_leptonVetoDR = 0.4,
    #inclusive_decayModeID = "decayModeFindingNewDMs", # ignored if not set or ""
    #inclusive_tauID = "decayModeFindingNewDMs",
    inclusive_decayModeID = "decayModeFinding", # ignored if not set or ""
    inclusive_tauID = "byCombinedIsolationDeltaBetaCorrRaw3Hits",
    inclusive_tauIDnHits = 5,
    inclusive_vetoLeptonsPOG = False, # If True, the following two IDs are required
    inclusive_tauAntiMuonID = "",
    inclusive_tauAntiElectronID = "",
    # loose hadronic tau selection
    loose_ptMin = 18,
    loose_etaMax = 2.3,
    loose_dxyMax = 1000.,
    loose_dzMax = 1000, #0.2,
    loose_vetoLeptons = False,
    loose_leptonVetoDR = 0.4,
    #loose_decayModeID = "decayModeFinding", # ignored if not set or ""
    #loose_tauID = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    loose_decayModeID = "decayModeFinding", # ignored if not set or ""
    loose_tauID = "byCombinedIsolationDeltaBetaCorrRaw3Hits",
    loose_tauIDnHits = 5,
    loose_vetoLeptonsPOG = False, # If True, the following two IDs are required
    loose_tauAntiMuonID = "",
    loose_tauAntiElectronID = "",
    loose_tauLooseID = "decayModeFinding"
    ### ====================== ###
    )

    #if ( tau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits") >= 5 ) continue;

##############################
### PHOTONANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.objects.PhotonAnalyzer import PhotonAnalyzer
photonAnalyzer = cfg.Analyzer(

    class_object                = PhotonAnalyzer,

    ### Photon - General
    ##############################
    photons                     = 'slimmedPhotons',
    ptMin                       = 15,
    etaMax                      = 2.5,
    gammaID                     = 'POG_PHYS14_25ns_Loose_hardcoded',
    do_mc_match                 = True,
    do_randomCone               = False,
    rhoPhoton                   = 'fixedGridRhoFastjetAll',
    ### ====================== ###
    )

##############################
### METANALYZER            ###
##############################
from PhysicsTools.Heppy.analyzers.objects.METAnalyzer import METAnalyzer
MEtAnalyzer = METAnalyzer.defaultConfig

##############################
### DM ANALYZERS           ###
##############################

### GLOBAL CUTS
met_pt_cut = 100. # met or fakemet
jet_met_deltaphi_cut = 0. # wrt met or fakemet

from DMPD.Heppy.analyzers.GenAnalyzer import GenAnalyzer
GenAnalyzer = cfg.Analyzer(
    class_object = GenAnalyzer,
    mediator = [9100000, 9900032, 1023],
    darkmatter = [9100022, -9100022, 9100012],
    )

from DMPD.Heppy.analyzers.PreselectionAnalyzer import PreselectionAnalyzer
PreselectionAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = PreselectionAnalyzer,
    )

from DMPD.Heppy.analyzers.XCleaningAnalyzer import XCleaningAnalyzer
XCleaningAnalyzer = cfg.Analyzer(
    verbose=False,
    class_object = XCleaningAnalyzer,
    mu_clean_pt  = 20.,
    mu_clean_id  = 'POG_ID_Tight',
    mu_clean_iso = lambda x : x.relIso04 < 0.2,
    mu_tau_dr    = 0.4,
    mu_jet_dr    = 0.4,
    mu_fatjet_dr = 0.4,
    ele_clean_pt = 20.,
    ele_clean_id = 'POG_Cuts_ID_PHYS14_25ns_v1_ConvVetoDxyDz_Veto',
    ele_clean_iso= lambda x : ( ( x.isEB() and x.relIso03 <  0.069537 ) or  ( x.isEE() and x.relIso03 < 0.078265 ) ),
    ele_tau_dr   = 0.4,
    ele_jet_dr   = 0.4,
    ele_fatjet_dr= 0.4,
    )

from DMPD.Heppy.analyzers.SyncAnalyzer import SyncAnalyzer
PreselectionAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = SyncAnalyzer,
    verbose = False,
    )

#from DMPD.Heppy.analyzers.ZZhAnalyzer import ZZhAnalyzer
#ZZhAnalyzer = cfg.Analyzer(
#    verbose = False,
#    class_object = ZZhAnalyzer,
#    fatjet_pt = 250.,
#    Z_pt = 100.,
#    Zmass_low = 75.,
#    Zmass_high = 105.,
#    fatjet_mass_algo = 'ak8PFJetsCHSSoftDropMass',
#    fatjet_mass_low = 100.,
#    fatjet_mass_high = 150.,
#    fatjet_btag_1 = 0.423,
#    fatjet_btag_2 = 0.423,
#    met_pt = 200.,
#    )


#from DMPD.Heppy.analyzers.CategorizationAnalyzer import CategorizationAnalyzer
#CategorizationAnalyzer = cfg.Analyzer(
#    verbose = False,
#    class_object = CategorizationAnalyzer,
#    jet1_pt = 30.,
#    jet1_eta = 2.5,
#    jet1_tag = -1e99,
#    jet1_chf_min = 0.2,
#    jet1_nhf_max = 0.7,
#    jet1_phf_max = 0.7,
#    jet2_pt = 30.,
#    jet2_eta = 2.5,
#    jet2_tag = -1e99,
#    deltaPhi12 = 2.5,
#    enableFatJets = True,
#    fatjet_pt = 250.,
#    fatjet_tag1 = 0.423,
#    fatjet_tag2 = 0.423,
#    fatjet_mass = 50.,
#    fatjet_mass_algo = 'ak8PFJetsCHSSoftDropMass',
#    fatjet_tau21 = -1.,
#    jetveto_pt = 0.,
#    jetveto_eta = 2.5,
#    )

globalVariables = [
    NTupleVariable('isSR',      lambda x: x.isSR, int, help='Signal Region flag'),
    NTupleVariable('isZCR',     lambda x: x.isZCR, int, help='Z+jets Control Region flag'),
    NTupleVariable('isWCR',     lambda x: x.isWCR, int, help='W+jets Control Region flag'),
    NTupleVariable('isTCR',     lambda x: x.isTCR, int, help='ttbar Control Region flag'),
    NTupleVariable('isGCR',     lambda x: x.isGCR, int, help='Gamma+jets Control Region flag'),
    #NTupleVariable('Cat',       lambda x: x.Category, int, help='Category 1/2/3'),
    NTupleVariable('nMuons',    lambda x: len(x.selectedMuons), int, help='Number of selected muons'),
    NTupleVariable('nElectrons',lambda x: len(x.selectedElectrons), int, help='Number of selected electrons'),
    NTupleVariable('nTaus',     lambda x: len(x.xcleanTaus), int, help='Number of xcleaned taus'),
    NTupleVariable('nPhotons',  lambda x: len(x.xcleanPhotons), int, help='Number of selected photons'),
    NTupleVariable('nJets',     lambda x: len(x.xcleanJets), int, help='Number of xcleaned jets'),
    NTupleVariable('nFatJets',  lambda x: len(x.xcleanJetsAK8), int, help='Number of xcleaned fat jets'),
    NTupleVariable('nBJets',    lambda x: len([jet for jet in x.xcleanJets if abs(jet.hadronFlavour()) == 5]), int, help='Number of xcleaned b-jets'),
#    NTupleVariable('nBFatJets', lambda x: len([jet for jet in x.xcleanJetsAK8 if abs(jet.hadronFlavour()) == 5]), int, help='Number of xcleaned b- fat jets'),
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
    vectorTree = False,
    globalVariables = globalVariables + [
        NTupleVariable('met_pt',    lambda x: x.met.pt(), float, help='Missing energy'),
        NTupleVariable('met_phi',   lambda x: x.met.phi(), float, help='Missing energy azimuthal coordinate'),
    ],
    globalObjects = {
        #'met'       : NTupleObject('met',  metType, help='PF E_{T}^{miss}, after default type 1 corrections'),
        #'V'         : NTupleObject('V', compositeType, help='Boson candidate'),
    },
    collections = {
        'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 2, help='cleaned fatJets collection'),
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
    vectorTree = False,
    globalVariables = globalVariables + [
        NTupleVariable('isZtoEE',  lambda x: x.isZtoEE, int, help='Z -> mu mu flag'),
        NTupleVariable('isZtoMM',  lambda x: x.isZtoMM, int, help='Z -> e e flag'),
        NTupleVariable('met_pt',    lambda x: x.met.pt(), float, help='Missing energy'),
        NTupleVariable('met_phi',   lambda x: x.met.phi(), float, help='Missing energy azimuthal coordinate'),
        NTupleVariable('fakemet_pt',    lambda x: x.fakemet.pt(), float, help='fake Missing energy'),
        NTupleVariable('fakemet_phi',   lambda x: x.fakemet.phi(), float, help='fake Missing energy azimuthal coordinate'),
    ],
    globalObjects = {
        #'met'       : NTupleObject('met',  metType, help='PF E_{T}^{miss}, after default type 1 corrections'),
        #'fakemet'   : NTupleObject('fakemet', fourVectorType, help='fake MET in Z events obtained removing the leptons'),
        'Z'         : NTupleObject('Z', compositeType, help='Z boson candidate'),
        #'V'         : NTupleObject('V', compositeType, help='Higgs boson candidate'),
    },
    collections = {
        'xcleanLeptons'       : NTupleCollection('lepton', leptonType, 2, help='Muon or Electron collection'),
        'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 2, help='cleaned fatJets collection'),
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
    vectorTree = False,
    globalVariables = globalVariables + [
        NTupleVariable('isWtoEN',  lambda x: x.isWtoEN, int, help='W -> mu nu flag'),
        NTupleVariable('isWtoMN',  lambda x: x.isWtoMN, int, help='W -> e nu flag'),
        NTupleVariable('met_pt',    lambda x: x.met.pt(), float, help='Missing energy'),
        NTupleVariable('met_phi',   lambda x: x.met.phi(), float, help='Missing energy azimuthal coordinate'),
        NTupleVariable('fakemet_pt',    lambda x: x.fakemet.pt(), float, help='fake Missing energy'),
        NTupleVariable('fakemet_phi',   lambda x: x.fakemet.phi(), float, help='fake Missing energy azimuthal coordinate'),
    ],
    globalObjects = {
        #'met'       : NTupleObject('met',  metType, help='PF E_{T}^{miss}, after default type 1 corrections'),
        #'fakemet'   : NTupleObject('fakemet', fourVectorType, help='fake MET in W -> mu nu event obtained removing the lepton'),
        'W'         : NTupleObject('W', compositeType, help='W boson candidate'),
        #'V'         : NTupleObject('V', compositeType, help='Higgs boson candidate'),
    },
    collections = {
        'xcleanLeptons'       : NTupleCollection('lepton', leptonType, 2, help='Muon or Electron collection'),
        'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 2, help='cleaned fatJets collection'),
    }
)


##################################
### TTbar CONTROL REGION TREE  ###
##################################
TTbarControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='TTbarControlRegionTreeProducer',
    treename='TCR',
    filter = lambda x: x.isTCR,
    verbose=False,
    vectorTree = False,
    globalVariables = globalVariables + [
        NTupleVariable('met_pt',    lambda x: x.met.pt(), float, help='Missing energy'),
        NTupleVariable('met_phi',   lambda x: x.met.phi(), float, help='Missing energy azimuthal coordinate'),
        NTupleVariable('fakemet_pt',    lambda x: x.fakemet.pt(), float, help='fake Missing energy'),
        NTupleVariable('fakemet_phi',   lambda x: x.fakemet.phi(), float, help='fake Missing energy azimuthal coordinate'),
    ],
    globalObjects = {
        #'met'       : NTupleObject('met',  metType, help='PF E_{T}^{miss}, after default type 1 corrections'),
        #'fakemet'   : NTupleObject('fakemet', fourVectorType, help='fake MET in ttbar events obtained removing the leptons'),
        #'V'         : NTupleObject('V', compositeType, help='Higgs boson candidate'),
    },
    collections = {
        'xcleanLeptons'       : NTupleCollection('lepton', leptonType, 2, help='Muon and Electron collection'),
        'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 2, help='cleaned fatJets collection'),
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
    vectorTree = False,
    globalVariables = globalVariables + [
        NTupleVariable('met_pt',    lambda x: x.met.pt(), float, help='Missing energy'),
        NTupleVariable('met_phi',   lambda x: x.met.phi(), float, help='Missing energy azimuthal coordinate'),
        NTupleVariable('fakemet_pt',    lambda x: x.fakemet.pt(), float, help='fake Missing energy'),
        NTupleVariable('fakemet_phi',   lambda x: x.fakemet.phi(), float, help='fake Missing energy azimuthal coordinate'),
    ],
    globalObjects = {
        #'met'       : NTupleObject('met',  metType, help='PF E_{T}^{miss}, after default type 1 corrections'),
        #'fakemet'   : NTupleObject('fakemet', fourVectorType, help='fake MET in gamma + jets event obtained removing the photon'),
        #'V' : NTupleObject('V', compositeType, help='Higgs boson candidate'),
    },
    collections = {
        #'selectedMuons'       : NTupleCollection('muon', muonType, 4, help='Muons after the preselection'),
        #'selectedElectrons'   : NTupleCollection('electron', electronType, 4, help='Electrons after the preselection'),
        'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 2, help='cleaned fatJets collection'),
        #'SubJets'             : NTupleCollection('jet', subjetType, 2, help='subJets of the leading fatJet'),
    }
)


##############################
###  Zprime -> Zh -> llbb  ###
##############################

ZZhTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='ZZhTreeProducer',
    treename='ZZh',
    filter = lambda x: x.isZZh,
    verbose=False,
    vectorTree = False,
    globalVariables = globalVariables + [
        NTupleVariable('isZtoMM',  lambda x: x.isZtoMM, int, help='Z -> mu mu flag')
    ],
    globalObjects = {
        'A' : NTupleObject('A', compositeType, help='A boson candidate'),
        'Z' : NTupleObject('Z', compositeType, help='Z boson candidate'),
        'H' : NTupleObject('h', compositeType, help='Higgs boson candidate'),
        'met' : NTupleObject('met',  metType, help='PF E_{T}^{miss}, after default type 1 corrections'),
        },
    collections = {
        'Leptons'           : NTupleCollection('lepton', leptonType, 2, help='Muons and Electrons after the preselection'),
        'xcleanJets'        : NTupleCollection('jet', jetType, 3, help='Jets after the preselection'),
        'xcleanJetsAK8'     : NTupleCollection('fatjet', fatjetType, 2, help='fatJets after the preselection'),
        #'SubJets'           : NTupleCollection('jet', subjetType, 2, help='subJets of the leading fatJet'),
        }
    )

##############################
### SEQUENCE               ###
##############################

sequence = [
    generatorAnalyzer,
    triggerAnalyzer,
    pileupAnalyzer,
    vertexAnalyzer,
    MEtAnalyzer,
    photonAnalyzer,
    leptonAnalyzer,
    tauAnalyzer,
    jetAnalyzer,
    fatJetAnalyzer,
    GenAnalyzer,
    #### Preselection Analyzers
    #SyncAnalyzerSR,
    #SyncAnalyzerGCR,
    #SyncAnalyzerZCR,
    #SyncAnalyzerWCR,
    PreselectionAnalyzer,
    ##### Analysis Analyzers
#    ZeroLeptonAnalyzer,
#    ZeroLeptonGammaAnalyzer,
#    OneLeptonAnalyzer,
#    TwoLeptonOSSFAnalyzer,
#    TwoLeptonOSDFAnalyzer,
#    ZZhAnalyzer,
    ##### Categorization Analyzers
    XCleaningAnalyzer,
#    CategorizationAnalyzer,
    ##### Tree producers
    SignalRegionTreeProducer,
    ZControlRegionTreeProducer,
    WControlRegionTreeProducer,
    TTbarControlRegionTreeProducer,
    GammaControlRegionTreeProducer,
#    ZZhTreeProducer,
    ]

##############################
### TFILESERVICE           ###
##############################
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name='outputfile',
    fname='tree.root',
    option='recreate'
    )

##############################
### INPUT                  ###
##############################
from PhysicsTools.Heppy.utils.miniAodFiles import miniAodFiles
#from DMPD.Heppy.samples.Phys14.fileLists import samples
from DMPD.Heppy.samples.Spring15.fileLists import samples

sampleDYJetsToLL_M50_HT100to200_v1 = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT100to200_v1']['files'],
    name='DYJetsToLL_M50_HT100to200_v1',
    isMC=True,
    isEmbed=False,
    splitFactor=50
    )

sampleDYJetsToLL_M50_HT100to200_v2 = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT100to200_v2']['files'],
    name='DYJetsToLL_M50_HT100to200_v2',
    isMC=True,
    isEmbed=False,
    splitFactor=50
    )

sampleDYJetsToLL_M50_HT400to600_v1 = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT400to600_v1']['files'],
    name='DYJetsToLL_M50_HT400to600_v1',
    isMC=True,
    isEmbed=False,
    splitFactor=50
    )

sampleDYJetsToLL_M50_HT600toInf_v1 = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT600toInf_v1']['files'],
    name='DYJetsToLL_M50_HT600toInf_v1',
    isMC=True,
    isEmbed=False,
    splitFactor=50
    )

sampleDYJetsToLL_M50_HT600toInf_v2 = cfg.Component(
    ### DYJetsToLL
    files = samples['DYJetsToLL_M50_HT600toInf_v2']['files'],
    name='DYJetsToLL_M50_HT600toInf_v2',
    isMC=True,
    isEmbed=False,
    splitFactor=50
    )

sampleSYNCH_TTBar = cfg.Component(
   files = ['file:/lustre/cmsdata/DM/DMS13TeVSynch/0A9E2CED-C9EC-E411-A8E4-003048FFCBA8.root'],
   name='TTBar',
   isMC=True,
   isEmbed=False,
   splitFactor=1
   )

##############################
### FWLITE                 ###
##############################
#from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
#preprocessor = CmsswPreprocessor('tagFatJets.py')
#preprocessor = CmsswPreprocessor('test.py')

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

### TEST (LOCAL)
#selectedComponents = [sampleTest]

#### FULL QCD
#selectedComponents = [sampleQCD_HT100To250,sampleQCD_HT250To500,sampleQCD_HT500To1000,sampleQCD_HT1000ToInf]

#### FULL DYJetsToLL
#selectedComponents = [sampleDYJetsToLL_M50_HT100to200_v1,sampleDYJetsToLL_M50_HT100to200_v2,sampleDYJetsToLL_M50_HT400to600_v1,sampleDYJetsToLL_M50_HT600toInf_v1,sampleDYJetsToLL_M50_HT600toInf_v2]

#### FULL GJets
#selectedComponents = [sampleGJets_HT100to200,sampleGJets_HT200to400,sampleGJets_HT400to600,sampleGJets_HT600toInf]

#### FULL TT
#selectedComponents = [sampleTT,sampleTTJets]

#### FULL T
#selectedComponents = [sampleT_tWchannel,sampleTbar_tWchannel,sampleTToLeptons_schannel,sampleTbarToLeptons_schannel,sampleTToLeptons_tchannel,sampleTbarToLeptons_tchannel]

#### FULL WJetsToLNu
#selectedComponents = [sampleWJetsToLNu_HT100to200,sampleWJetsToLNu_HT200to400,sampleWJetsToLNu_HT400to600,sampleWJetsToLNu_HT600toInf]

#### FULL ZJetsToNuNu
#selectedComponents = [sampleZJetsToNuNu_HT100to200,sampleZJetsToNuNu_HT200to400,sampleZJetsToNuNu_HT400to600,sampleZJetsToNuNu_HT600toInf]

#### FULL ZH_HToBB_ZToNuNu
#selectedComponents = [sampleZH_HToBB_ZToNuNu]

#### FULL DM-MonoJet
#selectedComponents = [sampleDM_Monojet_M10_V,sampleDM_Monojet_M100_V,sampleDM_Monojet_M1000_V,sampleDM_Monojet_M1_AV,sampleDM_Monojet_M10_AV,sampleDM_Monojet_M100_AV,sampleDM_Monojet_M1000_AV]

#### FULL List
#selectedComponents = [sampleQCD_HT100To250,sampleQCD_HT250To500,sampleQCD_HT500To1000,sampleQCD_HT1000ToInf,
                      #sampleDYJetsToLL_M50_HT100to200,sampleDYJetsToLL_M50_HT200to400,sampleDYJetsToLL_M50_HT400to600,sampleDYJetsToLL_M50_HT600toInf,
                      #sampleGJets_HT100to200,sampleGJets_HT200to400,sampleGJets_HT400to600,sampleGJets_HT600toInf,
                      #sampleTT,sampleTTJets,
                      #sampleT_tWchannel,sampleTbar_tWchannel,sampleTToLeptons_schannel,sampleTbarToLeptons_schannel,sampleTToLeptons_tchannel,sampleTbarToLeptons_tchannel,
                      #sampleWJetsToLNu_HT100to200,sampleWJetsToLNu_HT200to400,sampleWJetsToLNu_HT400to600,sampleWJetsToLNu_HT600toInf,
                      #sampleZJetsToNuNu_HT100to200,sampleZJetsToNuNu_HT200to400,sampleZJetsToNuNu_HT400to600,sampleZJetsToNuNu_HT600toInf,
                      #sampleZH_HToBB_ZToNuNu,
                      #sampleDM_Monojet_M10_V,sampleDM_Monojet_M100_V,sampleDM_Monojet_M1000_V,sampleDM_Monojet_M1_AV,sampleDM_Monojet_M10_AV,sampleDM_Monojet_M100_AV,sampleDM_Monojet_M1000_AV]


#### SINGLE COMPONENTS
#selectedComponents = [sampleQCD_HT100To250]
#selectedComponents = [sampleQCD_HT250To500]
#selectedComponents = [sampleQCD_HT500To1000]
#selectedComponents = [sampleQCD_HT1000ToInf]

#selectedComponents = [sampleTT]
#selectedComponents = [sampleTTJets]
#selectedComponents = [sampleT_tWchannel]
#selectedComponents = [sampleTbar_tWchannel]
#selectedComponents = [sampleTToLeptons_schannel]
#selectedComponents = [sampleTbarToLeptons_schannel]
#selectedComponents = [sampleTToLeptons_tchannel]
#selectedComponents = [sampleTbarToLeptons_tchannel]

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

#selectedComponents = [sampleDM_Monojet_M10_V]
#selectedComponents = [sampleDM_Monojet_M100_V]
#selectedComponents = [sampleDM_Monojet_M1000_V]
#selectedComponents = [sampleDM_Monojet_M1_AV]
#selectedComponents = [sampleDM_Monojet_M10_AV]
#selectedComponents = [sampleDM_Monojet_M100_AV]
#selectedComponents = [sampleDM_Monojet_M1000_AV]

#selectedComponents = [sampleDM_MonoB]
#selectedComponents = [sampleDM_MonoVbb]
#selectedComponents = [sampleDM_MonoH]

#### FULL ZZhToLL
#selectedComponents = [sampleZZhToLLM1000]
#selectedComponents = [sampleZZhToLLM2000]
#selectedComponents = [sampleZZhToLLM3000]
#selectedComponents = [sampleZZhToLLM4000]

###LOCAL COMPONENTS
#selectedComponents = [sampleDM_MonoB,sampleDM_MonoVbb,sampleDM_MonoH]

#selectedComponents = [sampleADDMonojet]
#selectedComponents = [sampleTTBar]
#selectedComponents = [sampleADDMonojet,sampleTTBar]

#selectedComponents = [sampleSYNCH_ADDMonojet]
selectedComponents = [sampleSYNCH_TTBar]
#selectedComponents = [sampleSYNCH_DYJetsToLL]
#selectedComponents = [sampleSYNCH_WJetsToLNu]
#selectedComponents = [sampleSYNCH_RSGravitonToGaGa]

#selectedComponents = [sampleSYNCH_ADDMonojet,sampleSYNCH_TTBar,sampleSYNCH_DYJetsToLL,sampleSYNCH_WJetsToLNu,sampleSYNCH_RSGravitonToGaGa]

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
        'DM',
        config,
        nPrint = 0,
        nEvents=10000,
        )
    looper.loop()
    looper.write()
