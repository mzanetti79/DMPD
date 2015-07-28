#! /usr/bin/env python
import ROOT
import copy
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
    inclusive_electron_id       = '',
    #inclusive_electron_id       = 'POG_Cuts_ID_PHYS14_25ns_v1_Veto',
    inclusive_electron_pt       = 10,
    inclusive_electron_eta      = 2.5,
    inclusive_electron_dxy      = 1.e99,
    inclusive_electron_dz       = 1.e99,
    inclusive_electron_lostHits = 99.,
    #inclusive_electron_isoCut   = lambda electron : ( ( electron.isEB() and electron.relIso03 < 0.158721 ) or  ( electron.isEE() and electron.relIso03 < 0.177032 ) ) ,
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
    inclusive_muon_id           = '',
    inclusive_muon_pt           = 10,
    inclusive_muon_eta          = 2.4,
    inclusive_muon_dxy          = 1.e99,
    inclusive_muon_dz           = 1.e99,
    #inclusive_muon_isoCut       = lambda muon : muon.relIso04 < 0.2,
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

jetAnalyzerJERUp = copy.deepcopy(jetAnalyzer)
jetAnalyzerJERUp.shiftJER = +1
jetAnalyzerJERDown = copy.deepcopy(jetAnalyzer)
jetAnalyzerJERDown.shiftJER = -1

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

fatJetAnalyzerJERUp = copy.deepcopy(fatJetAnalyzer)
fatJetAnalyzerJERUp.shiftJER = +1
fatJetAnalyzerJERDown = copy.deepcopy(fatJetAnalyzer)
fatJetAnalyzerJERDown.shiftJER = -1

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
    mu_clean_iso = lambda x : x.relIso04 < 0.12,
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
SyncAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = SyncAnalyzer,
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


from DMPD.Heppy.analyzers.SyncAnalyzerSR import SyncAnalyzerSR
SyncAnalyzerSR = cfg.Analyzer(
    verbose = False,
    class_object = SyncAnalyzerSR,
    )

from DMPD.Heppy.analyzers.SyncAnalyzerGCR import SyncAnalyzerGCR
SyncAnalyzerGCR = cfg.Analyzer(
    verbose = False,
    class_object = SyncAnalyzerGCR,
    )

from DMPD.Heppy.analyzers.SyncAnalyzerZCR import SyncAnalyzerZCR
SyncAnalyzerZCR = cfg.Analyzer(
    verbose = False,
    class_object = SyncAnalyzerZCR,
    )

from DMPD.Heppy.analyzers.SyncAnalyzerWCR import SyncAnalyzerWCR
SyncAnalyzerWCR = cfg.Analyzer(
    verbose = False,
    class_object = SyncAnalyzerWCR,
    )


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
    filter = lambda x: x.isSR and x.met.pt()>100,
    verbose=False,
    vectorTree = False,
    globalVariables = globalVariables + [
        NTupleVariable('met_pt',    lambda x: x.met.pt(), float, help='Missing energy'),
        NTupleVariable('met_phi',   lambda x: x.met.phi(), float, help='Missing energy azimuthal coordinate'),
    ],
    globalObjects = {
        #'met'       : NTupleObject('met',  metType, help='PF E_{T}^{miss}, after default type 1 corrections'),
        #'V'         : NTupleObject('V', candidateType, help='Boson candidate'),
        'A'         : NTupleObject('A', candidateFullType, help='Resonance candidate'),
    },
    collections = {
        #'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        #'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
#        'xcleanJetsJERUp'     : NTupleCollection('jetJERUp', lorentzVectorType, 3, help='cleaned Jet collection with JER +1 sigma'),
#        'xcleanJetsJERDown'   : NTupleCollection('jetJERDown', lorentzVectorType, 3, help='cleaned Jet collection with JER -1 sigma'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 1, help='cleaned fatJet collection'),
#        'xcleanJetsAK8JERUp'  : NTupleCollection('fatjetJERUp', lorentzVectorType, 1, help='cleaned fatJet collection with JER +1 sigma'),
#        'xcleanJetsAK8JERDown': NTupleCollection('fatjetJERDown', lorentzVectorType, 1, help='cleaned fatJet collection with JER -1 sigma'),
    }
)


##############################
### Z CONTROL REGION TREE  ###
##############################
ZControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='ZControlRegionTreeProducer',
    treename='ZCR',
    filter = lambda x: x.isZCR and x.fakemet.pt()>100,
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
        'Z'         : NTupleObject('Z', candidateType, help='Z boson candidate'),
        #'V'         : NTupleObject('V', candidateType, help='Higgs boson candidate'),
        'A'         : NTupleObject('A', candidateFullType, help='Resonance candidate'),
    },
    collections = {
        'xcleanLeptons'       : NTupleCollection('lepton', leptonType, 2, help='Muon or Electron collection'),
        #'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        #'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
#        'xcleanJetsJERUp'     : NTupleCollection('jetJERUp', lorentzVectorType, 3, help='cleaned Jet collection with JER +1 sigma'),
#        'xcleanJetsJERDown'   : NTupleCollection('jetJERDown', lorentzVectorType, 3, help='cleaned Jet collection with JER -1 sigma'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 1, help='cleaned fatJet collection'),
#        'xcleanJetsAK8JERUp'  : NTupleCollection('fatjetJERUp', lorentzVectorType, 1, help='cleaned fatJet collection with JER +1 sigma'),
#        'xcleanJetsAK8JERDown': NTupleCollection('fatjetJERDown', lorentzVectorType, 1, help='cleaned fatJet collection with JER -1 sigma'),
    }
)


##############################
### W CONTROL REGION TREE  ###
##############################
WControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='WControlRegionTreeProducer',
    treename='WCR',
    filter = lambda x: x.isWCR and x.fakemet.pt()>100,
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
        'W'         : NTupleObject('W', candidateType, help='W boson candidate'),
        #'V'         : NTupleObject('V', candidateType, help='Higgs boson candidate'),
        'A'         : NTupleObject('A', candidateFullType, help='Resonance candidate'),
    },
    collections = {
        'xcleanLeptons'       : NTupleCollection('lepton', leptonType, 2, help='Muon or Electron collection'),
        'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
#        'xcleanJetsJERUp'     : NTupleCollection('jetJERUp', lorentzVectorType, 3, help='cleaned Jet collection with JER +1 sigma'),
#        'xcleanJetsJERDown'   : NTupleCollection('jetJERDown', lorentzVectorType, 3, help='cleaned Jet collection with JER -1 sigma'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 1, help='cleaned fatJet collection'),
#        'xcleanJetsAK8JERUp'  : NTupleCollection('fatjetJERUp', lorentzVectorType, 1, help='cleaned fatJet collection with JER +1 sigma'),
#        'xcleanJetsAK8JERDown': NTupleCollection('fatjetJERDown', lorentzVectorType, 1, help='cleaned fatJet collection with JER -1 sigma'),
    }
)


##################################
### TTbar CONTROL REGION TREE  ###
##################################
TTbarControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='TTbarControlRegionTreeProducer',
    treename='TCR',
    filter = lambda x: x.isTCR and x.fakemet.pt()>100,
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
        #'V'         : NTupleObject('V', candidateType, help='Higgs boson candidate'),
    },
    collections = {
        'xcleanLeptons'       : NTupleCollection('lepton', leptonType, 2, help='Muon and Electron collection'),
        #'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        #'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
#        'xcleanJetsJERUp'     : NTupleCollection('jetJERUp', lorentzVectorType, 3, help='cleaned Jet collection with JER +1 sigma'),
#        'xcleanJetsJERDown'   : NTupleCollection('jetJERDown', lorentzVectorType, 3, help='cleaned Jet collection with JER -1 sigma'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 1, help='cleaned fatJet collection'),
#        'xcleanJetsAK8JERUp'  : NTupleCollection('fatjetJERUp', lorentzVectorType, 1, help='cleaned fatJet collection with JER +1 sigma'),
#        'xcleanJetsAK8JERDown': NTupleCollection('fatjetJERDown', lorentzVectorType, 1, help='cleaned fatJet collection with JER -1 sigma'),
    }
)

##############################
### G CONTROL REGION TREE  ###
##############################
GammaControlRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='GammaControlRegionTreeProducer',
    treename='GCR',
    filter = lambda x: x.isGCR and x.fakemet.pt()>100,
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
        #'V' : NTupleObject('V', candidateType, help='Higgs boson candidate'),
    },
    collections = {
        #'selectedMuons'       : NTupleCollection('muon', muonType, 4, help='Muons after the preselection'),
        #'selectedElectrons'   : NTupleCollection('electron', electronType, 4, help='Electrons after the preselection'),
        #'xcleanTaus'          : NTupleCollection('tau', tauType, 1, help='cleaned Tau collection'),
        'xcleanPhotons'       : NTupleCollection('photon', photonType, 1, help='cleaned Photon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 3, help='cleaned Jet collection'),
#        'xcleanJetsJERUp'     : NTupleCollection('jetJERUp', lorentzVectorType, 3, help='cleaned Jet collection with JER +1 sigma'),
#        'xcleanJetsJERDown'   : NTupleCollection('jetJERDown', lorentzVectorType, 3, help='cleaned Jet collection with JER -1 sigma'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 1, help='cleaned fatJet collection'),
#        'xcleanJetsAK8JERUp'  : NTupleCollection('fatjetJERUp', lorentzVectorType, 1, help='cleaned fatJet collection with JER +1 sigma'),
#        'xcleanJetsAK8JERDown': NTupleCollection('fatjetJERDown', lorentzVectorType, 1, help='cleaned fatJet collection with JER -1 sigma'),
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
        'A' : NTupleObject('A', candidateType, help='A boson candidate'),
        'Z' : NTupleObject('Z', candidateType, help='Z boson candidate'),
        'H' : NTupleObject('h', candidateType, help='Higgs boson candidate'),
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
    #jetAnalyzerJERUp,
    #jetAnalyzerJERDown,
    fatJetAnalyzer,
    #fatJetAnalyzerJERUp,
    #fatJetAnalyzerJERDown,
    GenAnalyzer,
    #### Preselection Analyzers
#    SyncAnalyzerSR,
#    SyncAnalyzerGCR,
#    SyncAnalyzerZCR,
#    SyncAnalyzerWCR,
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
    SyncAnalyzer,
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
from DMPD.Heppy.samples.Spring15.fileSamples import *

sampleSYNCH_ADDMonojet = cfg.Component(
    files = ['file:/lustre/cmsdata/DM/DMS13TeVSynch/80CF5456-B9EC-E411-93DA-002618FDA248.root'],
    name='ADDMonojet',
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleSYNCH_TTBar = cfg.Component(
    files = ['file:/lustre/cmsdata/DM/DMS13TeVSynch/0A9E2CED-C9EC-E411-A8E4-003048FFCBA8.root'],
    name='TTBar',
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleSYNCH_DYJetsToLL = cfg.Component(
    files = ['file:/lustre/cmsdata/DM/DMS13TeVSynch/04963444-D107-E511-B245-02163E00F339.root'],
    name='DYJetsToLL',
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleSYNCH_WJetsToLNu = cfg.Component(
    files = ['file:/lustre/cmsdata/DM/DMS13TeVSynch/6408230F-9F08-E511-A1A6-D4AE526A023A.root'],
    name='WJetsToLNu',
    isMC=True,
    isEmbed=False,
    splitFactor=1
    )

sampleSYNCH_RSGravitonToGaGa = cfg.Component(
    files = ['file:/lustre/cmsdata/DM/DMS13TeVSynch/189277BA-DCEC-E411-B3B8-0025905B859E.root'],
    name='RSGravitonToGaGa',
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

#selectedComponents = [sampleSYNCH_ADDMonojet]
#selectedComponents = [sampleSYNCH_TTBar]
#selectedComponents = [sampleSYNCH_DYJetsToLL]
#selectedComponents = [sampleSYNCH_WJetsToLNu]
#selectedComponents = [sampleSYNCH_RSGravitonToGaGa]
#selectedComponents = [sampleSYNCH_ADDMonojet,sampleSYNCH_TTBar,sampleSYNCH_DYJetsToLL,sampleSYNCH_WJetsToLNu,sampleSYNCH_RSGravitonToGaGa]

selectedComponents = [
    sampleDYJetsToLL_M50_HT100to200_madgraphMLM_pythia8_v1,
    sampleDYJetsToLL_M50_HT100to200_madgraphMLM_pythia8_v2,
    sampleDYJetsToLL_M50_HT200to400_madgraphMLM_pythia8_v1,
    sampleDYJetsToLL_M50_HT200to400_madgraphMLM_pythia8_v2,
    sampleDYJetsToLL_M50_HT400to600_madgraphMLM_pythia8_v1,
    sampleDYJetsToLL_M50_HT400to600_madgraphMLM_pythia8_v2,
    sampleDYJetsToLL_M50_HT600toInf_madgraphMLM_pythia8_v1,
    sampleDYJetsToLL_M50_HT600toInf_madgraphMLM_pythia8_v2,
    sampleGJets_HT_100To200_madgraphMLM_pythia8_v1,
    sampleGJets_HT_100To200_madgraphMLM_pythia8_v2,
    sampleGJets_HT_200To400_madgraphMLM_pythia8_v1,
    sampleGJets_HT_200To400_madgraphMLM_pythia8_v2,
    sampleGJets_HT_400To600_madgraphMLM_pythia8_v1,
    sampleGJets_HT_600ToInf_madgraphMLM_pythia8_v1,
    sampleQCD_HT_1000to1500_madgraphMLM_pythia8_v2,
    sampleQCD_HT_100to200_madgraphMLM_pythia8_v2,
    sampleQCD_HT_1500to2000_madgraphMLM_pythia8_v1,
    sampleQCD_HT_2000toInf_madgraphMLM_pythia8_v1,
    sampleQCD_HT_200to300_madgraphMLM_pythia8_v2,
    sampleQCD_HT_300to500_madgraphMLM_pythia8_v2,
    sampleQCD_HT_500to700_madgraphMLM_pythia8_v1,
    sampleQCD_HT_700to1000_madgraphMLM_pythia8_v1,
#    sampleQCD_Pt_1000to1400_pythia8_v1,
#    sampleQCD_Pt_10to15_pythia8_v2,
#    sampleQCD_Pt_120to170_pythia8_v1,
#    sampleQCD_Pt_1400to1800_pythia8_v1,
#    sampleQCD_Pt_15to30_pythia8_v2,
#    sampleQCD_Pt_170to300_pythia8_v2,
#    sampleQCD_Pt_1800to2400_pythia8_v1,
#    sampleQCD_Pt_2400to3200_pythia8_v1,
#    sampleQCD_Pt_300to470_pythia8_v1,
#    sampleQCD_Pt_30to50_pythia8_v2,
#    sampleQCD_Pt_3200toInf_pythia8_v1,
#    sampleQCD_Pt_470to600_pythia8_v2,
#    sampleQCD_Pt_50to80_pythia8_v2,
#    sampleQCD_Pt_5to10_pythia8_v2,
#    sampleQCD_Pt_600to800_pythia8_v3,
#    sampleQCD_Pt_800to1000_pythia8_v2,
#    sampleQCD_Pt_80to120_pythia8_v1,
    sampleST_s_channel_4f_leptonDecays_amcatnlo_pythia8_v1,
    sampleST_t_channel_antitop_4f_leptonDecays_amcatnlo_pythia8_v1,
    sampleST_t_channel_top_4f_leptonDecays_amcatnlo_pythia8_v1,
    sampleST_tW_antitop_5f_inclusiveDecays_powheg_pythia8_v1,
    sampleST_tW_top_5f_inclusiveDecays_powheg_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_10_Mphi_100_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_10_Mphi_50_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_150_Mphi_200_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_1_Mphi_100_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_1_Mphi_10_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_1_Mphi_300_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_500_Mphi_500_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_50_Mphi_300_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_pseudoscalar_Mchi_50_Mphi_50_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_scalar_Mchi_10_Mphi_100_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_scalar_Mchi_10_Mphi_10_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_scalar_Mchi_150_Mphi_500_madgraphMLM_pythia8_v3,
#    sampleTTbarDMJets_scalar_Mchi_1_Mphi_100_madgraphMLM_pythia8_v1,
#    sampleTTbarDMJets_scalar_Mchi_1_Mphi_50_madgraphMLM_pythia8_v1,
    sampleTTJets_madgraphMLM_pythia8_v2,
    sampleTT_powheg_pythia8_v2,
    sampleWJetsToLNu_HT_100To200_madgraphMLM_pythia8_v1,
    sampleWJetsToLNu_HT_200To400_madgraphMLM_pythia8_v1,
    sampleWJetsToLNu_HT_400To600_madgraphMLM_pythia8_v3,
    sampleWJetsToLNu_HT_600ToInf_madgraphMLM_pythia8_v1,
    sampleWW_pythia8_v1,
    sampleWZ_pythia8_v1,
    sampleZH_HToBB_ZToLL_M120_amcatnloFXFX_madspin_pythia8_v1,
    sampleZH_HToBB_ZToNuNu_M120_amcatnloFXFX_madspin_pythia8_v1,
    sampleZH_HToBB_ZToNuNu_M120_amcatnloFXFX_madspin_pythia8_v2,
#    sampleZJetsToNuNu_HT_400To600_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M1000_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M1200_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M1400_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M1600_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M1800_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M2000_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M2500_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M3000_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M3500_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M4000_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M4500_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M600_madgraph_v1,
#    sampleZprimeToZhToZlephbb_narrow_M800_madgraph_v1,
    sampleZZ_pythia8_v3,
]


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
