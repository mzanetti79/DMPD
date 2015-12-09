#! /usr/bin/env python
import ROOT 
import os, copy
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
from DMPD.Heppy.analyzers.ObjectsFormat import *
cfg.Analyzer.nosubdir=True


##############################
### LHEANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer
lheAnalyzer= cfg.Analyzer(
    class_object=LHEAnalyzer,
    )

##############################
### GENANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer import GeneratorAnalyzer
generatorAnalyzer= cfg.Analyzer(
    verbose=False,
    class_object=GeneratorAnalyzer,
    stableBSMParticleIds = [ 1000022, 9100000, 9000001, 9000002, -9000002, 9100012, 9100022, -9100022, 9900032, 1023 ], # BSM particles that can appear with status <= 2 and should be kept
    # Particles of which we want to save the pre-FSR momentum (a la status 3).
    # Note that for quarks and gluons the post-FSR doesn't make sense,
    # so those should always be in the list
    savePreFSRParticleIds = [ 1,2,3,4,5, 11,12,13,14,15,16, 21 ],
    makeAllGenParticles = False, # Make also the list of all genParticles, for other analyzers to handle
    makeSplittedGenLists = False, # Make also the splitted lists
    allGenTaus = False,
    makeLHEweights = True,
    )

##############################
### PDFANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.gen.PDFWeightsAnalyzer import PDFWeightsAnalyzer
pdfAnalyzer= cfg.Analyzer(
    class_object=PDFWeightsAnalyzer,
    doPDFWeights = False,
    doPDFVars = False,
    PDFWeights = ["cteq6ll", "MSTW2008nlo68cl"],
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
        'SingleMu'       : ['HLT_IsoMu20_v*', 'HLT_IsoTkMu20_v*', 'HLT_IsoMu27_v*', 'HLT_Mu45_eta2p1_v*', 'HLT_Mu50_v*'],
        'DoubleMu'       : ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*','HLT_Mu30_TkMu11_v*'],
        'DoubleElectron' : ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*', 'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v*'],
        'MuonEG'         : ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*'],        
        'SingleElectron' : ['HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v*', 'HLT_Ele23_WPLoose_Gsf_v*', 'HLT_Ele23_WP85_Gsf_v*', 'HLT_Ele27_WP85_Gsf_v*', 'HLT_Ele27_WPLoose_Gsf_v*', 'HLT_Ele105_CaloIdVT_GsfTrkIdT_v*'],
        'SinglePhoton'   : ['HLT_Photon165_HE10', 'HLT_Photon175'],
        'MET'            : [
                            'HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v*',
                            'HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v*',
                            'HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v*',
                            'HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v*',
                            'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*',
                            'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*',
                            'HLT_PFMET120_JetIdCleaned_BTagCSV0p72_v*',
                            'HLT_PFMET120_NoiseCleaned_BTagCSV07_v*',
                            'HLT_PFHT350_PFMET100_JetIdCleaned_v*', 
                            'HLT_PFMET90_PFMHT90_IDTight_v*', 
                            'HLT_PFMET120_PFMHT120_IDTight_v*', 
                            'HLT_PFMET170_NoiseCleaned_v*', 
                            ],
        
        #'JET'            : ['HLT_PFJet260_v*'],
    },
#   processName='HLT',
#   outprefix='HLT'
    #setting 'unrollbits' to true will not only store the OR for each set of trigger bits but also the individual bits
    #caveat: this does not unroll the version numbers
    unrollbits=True
    )

filterAnalyzer= cfg.Analyzer(
    verbose=False,
    class_object=TriggerBitAnalyzer,
    triggerBits = {
        'FILTERS' : [ 
                     "Flag_HBHENoiseFilter", 
                     "Flag_HBHENoiseIsoFilter",
                     "Flag_CSCTightHaloFilter", 
                     #"Flag_hcalLaserEventFilter", 
                     #"Flag_EcalDeadCellTriggerPrimitiveFilter", 
                     "Flag_goodVertices", 
                     #"Flag_trackingFailureFilter", 
                     "Flag_eeBadScFilter", 
                     #"Flag_ecalLaserCorrFilter", 
                     #"Flag_trkPOGFilters", 
                     #"Flag_trkPOG_manystripclus53X", 
                     #"Flag_trkPOG_toomanystripclus53X", 
                     #"Flag_trkPOG_logErrorTooManyClusters", 
                     #"Flag_METFilters" 
                     ],
    },
    processName = 'PAT',
    outprefix = 'Flag',
    #setting 'unrollbits' to true will not only store the OR for each set of trigger bits but also the individual bits
    #caveat: this does not unroll the version numbers
    unrollbits=True
    )


##############################
### JSONANALYZER         ###
##############################
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
jsonAnalyzer = cfg.Analyzer(
    verbose=False,
    class_object=JSONAnalyzer,
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
vertexAnalyzer = cfg.Analyzer(
    verbose=False,
    class_object=VertexAnalyzer,
    vertexWeight = None,
    fixedWeight = 1,
    doHists = False,
    keepFailingEvents = True,
    )

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
    do_mc_match                 = False, # note: it will in any case try it only on MC, not on data
    match_inclusiveLeptons      = False, # match to all inclusive leptons

    ### Electron - General
    ##############################
    electrons                   = 'slimmedElectrons',
    rhoElectron                 = 'fixedGridRhoFastjetAll',
    #ele_isoCorr                 = 'deltaBeta',
    ele_isoCorr                 = 'rhoArea',
    # NOTE -> SPRING15 25ns        
    el_effectiveAreas           = 'Spring15_25ns_v1',
    ele_tightId                 = 'POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto',

    ### Electron selection - First step
    inclusive_electron_id       = '',
    inclusive_electron_pt       = 0.,
    inclusive_electron_eta      = 99.,
    inclusive_electron_dxy      = 1.e99,
    inclusive_electron_dz       = 1.e99,
    inclusive_electron_lostHits = 99.,
    inclusive_electron_relIso   = 1.e99,

    ### Electron selection - Second step
    loose_electron_pt           = 10,
    loose_electron_eta          = 2.5,
    loose_electron_dxy          = 1.e99,
    loose_electron_dz           = 1.e99,
    loose_electron_lostHits     = 9.0,
    loose_electron_relIso       = 1.e99,
    # NOTE -> SPRING15 25ns        
    loose_electron_id           = 'POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto',
    loose_electron_isoCut       = lambda electron : ( ( electron.isEB() and electron.relIso03 < 0.126 ) or  ( electron.isEE() and electron.relIso03 < 0.144 ) ) ,

    ### Muon - General
    ##############################
    muons                       = 'slimmedMuons',
    rhoMuon                     = 'fixedGridRhoFastjetAll',
    mu_isoCorr                  = 'deltaBeta' ,
    mu_effectiveAreas           = 'Phys14_25ns_v1', #(can be 'Data2012' or 'Phys14_25ns_v1') ### NOTE -> not used
    muon_dxydz_track            = 'muonBestTrack',

    ### Muon selection - First step
    inclusive_muon_id           = '',
    inclusive_muon_pt           = 0,
    inclusive_muon_eta          = 99,
    inclusive_muon_dxy          = 1.e99,
    inclusive_muon_dz           = 1.e99,
    inclusive_muon_relIso       = 1.e99,

    ### Muon selection - Second step
    loose_muon_id               = 'POG_ID_Loose',
    loose_muon_pt               = 10,
    loose_muon_eta              = 2.4,
    loose_muon_dxy              = 1.e99,
    loose_muon_dz               = 1.e99,
    loose_muon_relIso           = 1.e99,
    # NOTE -> SPRING15 25ns        
    loose_muon_isoCut           = lambda muon : muon.relIso04 < 0.25,

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
    do_mc_match                 = False,
    recalibrateJets             = False,
    shiftJEC                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    addJECShifts                = False,
    smearJets                   = False,
    shiftJER                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    cleanJetsFromFirstPhoton    = False,
    cleanJetsFromTaus           = False,
    cleanJetsFromIsoTracks      = False,
    recalibrationType           = 'AK4PFchs',
    jecPath                     = '%s/src/DMPD/Heppy/python/tools/JEC/' % os.environ['CMSSW_BASE'], 
    mcGT                        = 'Summer15_25nsV6_MC',
    dataGT                      = 'Summer15_25nsV6_DATA',
    genJetCol                   = 'slimmedGenJets',
    rho                         = ('fixedGridRhoFastjetAll','',''),
    copyJetsByValue             = False, #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    cleanSelectedLeptons        = False, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    lepSelCut                   = lambda lep : True,
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
    jetPt                       = 200.,
    jetEta                      = 4.7,
    jetEtaCentral               = 2.5,
    jetLepDR                    = 1.0,
    jetLepArbitration           = (lambda jet,lepton : jet), # you can decide which to keep in case of overlaps -> keeping the jet -> resolving it later
    minLepPt                    = 20,
    relaxJetId                  = False,
    doPuId                      = False, # Not commissioned in 7.0.X
    doQG                        = False,
    do_mc_match                 = False,
    recalibrateJets             = True,
    shiftJEC                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    addJECShifts                = False,
    smearJets                   = False,
    shiftJER                    = 0, # set to +1 or -1 to get +/-1 sigma shifts
    cleanJetsFromFirstPhoton    = False,
    cleanJetsFromTaus           = False,
    cleanJetsFromIsoTracks      = False,
    recalibrationType           = 'AK8PFchs',
    jecPath                     = '%s/src/DMPD/Heppy/python/tools/JEC/' % os.environ['CMSSW_BASE'], 
    mcGT                        = 'Summer15_25nsV6_MC',
    dataGT                      = 'Summer15_25nsV6_DATA',
    genJetCol                   = 'slimmedGenJets',
    rho                         = ('fixedGridRhoFastjetAll','',''),
    copyJetsByValue             = False, #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    cleanSelectedLeptons        = False, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    lepSelCut                   = lambda lep : True,
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
    #inclusive_tauID = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    inclusive_decayModeID = "decayModeFinding", # ignored if not set or ""
    inclusive_tauID = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    inclusive_tauIDcut = 1e99, #NOTE -> inclusive_tauID < inclusive_tauIDcut
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
    loose_tauID = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    loose_tauIDcut = 1e99, #NOTE -> loose_tauID < loose_tauIDcut
    loose_vetoLeptonsPOG = False, # If True, the following two IDs are required
    loose_tauAntiMuonID = "",
    loose_tauAntiElectronID = "",
    loose_tauLooseID = "decayModeFinding"
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
    ptMin                       = 15,
    etaMax                      = 2.5,
    gammaID                     = 'POG_SPRING15_25ns_Loose',#'POG_PHYS14_25ns_Loose_hardcoded',
    gamma_isoCorr               = 'rhoArea',
    do_mc_match                 = False,
    do_randomCone               = False,
    rhoPhoton                   = 'fixedGridRhoFastjetAll',
    ### ====================== ###
    )

##############################
### METANALYZER            ###
##############################
from PhysicsTools.Heppy.analyzers.objects.METAnalyzer import METAnalyzer
MEtAnalyzer = cfg.Analyzer(

    class_object = METAnalyzer,
    
    ### MET - General
    ##############################
    metCollection     = "slimmedMETs",
    noPUMetCollection = "slimmedMETs",
    copyMETsByValue = False,
    recalibrate = True,
    jetAnalyzerCalibrationPostFix = "",
    doTkMet = False,
    includeTkMetCHS = False,
    includeTkMetPVLoose = False,
    includeTkMetPVTight = False,
    doMetNoPU = False,  
    doMetNoMu = False,  
    doMetNoEle = False,  
    doMetNoPhoton = False,  
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "",
    ### ====================== ###
    )


MEtNoHFAnalyzer = copy.deepcopy(MEtAnalyzer)
MEtNoHFAnalyzer.metCollection = "slimmedMETsNoHF"
MEtNoHFAnalyzer.noPUMetCollection = "slimmedMETsNoHF"
MEtNoHFAnalyzer.collectionPostFix = "NoHF"

######################################
### TRIGGER MATCHING ANALYZERS     ###
######################################
from PhysicsTools.Heppy.analyzers.core.TriggerMatchAnalyzer import TriggerMatchAnalyzer
TriggerMatchAnalyzer = cfg.Analyzer(
   
   class_object = TriggerMatchAnalyzer,
   
   processName = 'RECO',
   label = '',
   unpackPathNames = True,
   trgObjSelectors = [lambda ob: ob.pt()>10, lambda ob: abs(ob.eta())<2.5],
   collToMatch = "selectedLeptons",
   collMatchSelectors = [lambda lep,ob: abs(lep.pt()/ob.pt()-1)<0.5],
   collMatchDRCut = 0.3,
   univoqueMatching = True,
   verbose = False
)

##############################
### ANALYSIS ANALYZERS     ###
##############################

fake_met_cut = 0

from DMPD.Heppy.analyzers.GenAnalyzer import GenAnalyzer
GenAnalyzer = cfg.Analyzer(
    class_object = GenAnalyzer,
    phi = [9100000, 9900032, 9000001, 9000002, -9000002, 1023],
    chi = [9100022, -9100022, 9100012],
    )

from DMPD.Heppy.analyzers.PreselectionAnalyzer import PreselectionAnalyzer
PreselectionAnalyzer = cfg.Analyzer(
    verbose = False,
    class_object = PreselectionAnalyzer,
    addJECUncertainties         = False,
    recalibrateMass             = False,
    recalibrationType           = 'AK8PFchs',
    jecPath                     = '%s/src/DMPD/Heppy/python/tools/JEC/' % os.environ['CMSSW_BASE'], 
    #jecPath                     = 'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms/store/user/zucchett/JEC/', 
    mcGT                        = 'Summer15_25nsV6_MC',
    dataGT                      = 'Summer15_25nsV6_DATA',
    )

from DMPD.Heppy.analyzers.XCleaningAnalyzer import XCleaningAnalyzer
XCleaningAnalyzer = cfg.Analyzer(
    verbose=False,
    class_object = XCleaningAnalyzer,
    cleanTaus = False,
    cleanJets = False,
    cleanJetsAK8 = False,
    cleanFromMuons = False,
    cleanFromElectrons = False,
    mu_clean_pt  = 20.,
    mu_clean_id  = 'POG_ID_Tight',
    mu_clean_iso = lambda x : x.relIso04 < 0.15,
    mu_tau_dr    = 0.4,
    mu_jet_dr    = 0.4,
    mu_fatjet_dr = 0.4,
    ele_clean_pt = 20.,
    ele_clean_id = 'POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Tight',
    ele_clean_iso= lambda electron : ( ( electron.isEB() and electron.relIso03 < 0.0354 ) or  ( electron.isEE() and electron.relIso03 < 0.0646 ) ) ,
    #ele_clean_id = 'POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto',
    #ele_clean_iso= lambda electron : ( ( electron.isEB() and electron.relIso03 < 0.1260 ) or  ( electron.isEE() and electron.relIso03 < 0.1440 ) )
    ele_tau_dr   = 0.4,
    ele_jet_dr   = 0.4,
    ele_fatjet_dr= 0.4,
    )



globalEventVariables = [
    NTupleVariable('lheNb',            lambda x: getattr(x, "lheNb", -1.), int, help='Number of b-quarks at LHE level'),
    NTupleVariable('lheHT',            lambda x: getattr(x, "lheHT", -1.), float, help='HT at LHE level'),
    NTupleVariable('lheVpt',           lambda x: getattr(x, "lheV_pt", -1.), float, help='Vector boson pt at LHE level'),
    #NTupleVariable('genVpt',           lambda x: x.genV.pt() if hasattr(x, "genV") else -1., float, help='Vector boson pt at Gen level'),
    #NTupleVariable('genVphi',          lambda x: x.genV.phi() if hasattr(x, "genV") else -1., float, help='Vector boson phi at Gen level'),
    #NTupleVariable('genNb',            lambda x: len(x.genbquarks) if hasattr(x, "genbquarks") else -1, int, help='Number of b-quarks at generator level'),
    #NTupleVariable('genNl',            lambda x: ( len(x.genleps)+len(x.gentaus) ) if ( hasattr(x, "genleps") and hasattr(x, "genleps") ) else -1, int, help='Number of leptons at generator level'),
    #NTupleVariable('genWtauHad',       lambda x: x.genWtauHad, int, help='Generated tau from W is hadronic'), 
    #NTupleVariable('genWtauLep',       lambda x: x.genWtauLep, int, help='Generated tau from W is leptonic'), 
    #NTupleVariable('facWeightUp',       lambda x: getattr(x, "FacScaleUp", 1.), float, help='Factorization Weight Up'),
    #NTupleVariable('facWeightDown',     lambda x: getattr(x, "FacScaleDown", 1.), float, help='Factorization Weight Down'),
    #NTupleVariable('renWeightUp',       lambda x: getattr(x, "RenScaleUp", 1.), float, help='Renormalization Weight Up'),
    #NTupleVariable('renWeightDown',     lambda x: getattr(x, "RenScaleDown", 1.), float, help='Renormalization Weight Down'),
    NTupleVariable('LHEweight',        lambda x: abs(getattr(x, "LHE_originalWeight", 1.))/getattr(x, "LHE_originalWeight", 1.), float, help='LHE weight'),
    #NTupleVariable('pdfWeight',        lambda x: getattr(x, "PDFweight", 1.), float, help='PDF weight'),
    NTupleVariable('nPU',              lambda x: getattr(x, "nPU", -1.) if hasattr(x, "nPU") and x.nPU is not None else -1, int, help='Number of true interactions'),
    NTupleVariable('nPV',              lambda x: len(x.vertices), int, help='Number of reconstructed primary vertices'),
    NTupleVariable('rho',              lambda x: getattr(x, "rho", -1.), int, help='Energy density in the event'),
    NTupleVariable('HT',               lambda x: sum([x.pt() for x in x.xcleanJets]), float, help='HT from AK4 jets with pt>30 GeV'),
]
globalDMVariables = globalEventVariables + [
    NTupleVariable('nMuons',           lambda x: len(x.selectedMuons), int, help='Number of selected muons'),
    NTupleVariable('nElectrons',       lambda x: len(x.selectedElectrons), int, help='Number of selected electrons'),
    NTupleVariable('nTaus',            lambda x: len(x.xcleanTaus), int, help='Number of xcleaned taus'),
    NTupleVariable('nPhotons',         lambda x: len(x.xcleanPhotons), int, help='Number of selected photons'),
    NTupleVariable('nJets',            lambda x: len(x.xcleanJets), int, help='Number of xcleaned jets'),
    NTupleVariable('nFatJets',         lambda x: len(x.xcleanJetsAK8), int, help='Number of xcleaned fat jets'),
    NTupleVariable('nBJets',           lambda x: len([jet for jet in x.xcleanJets if abs(jet.hadronFlavour()) == 5]), int, help='Number of xcleaned b-jets'),
    #NTupleVariable('minDeltaPhi',      lambda x: getattr(x, "minDeltaPhi", -1.), float, help='Number of xcleaned b-jets'),
]


##############################
### SAME-SIGN REGION TREE  ###
##############################
SSRegionTreeProducer= cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    name='SSRegionTreeProducer',
    treename='SSR',
    filter = lambda x: (len(x.inclusiveMuons)>=1 and x.inclusiveMuons[0].pt()>40) or (len(x.selectedMuons)>=1 and x.selectedMuons[0].pt()>20) or (len(x.selectedElectrons)>=1 and x.selectedElectrons[0].pt()>25.),
    verbose=False,
    vectorTree = False,
    globalVariables = globalDMVariables + [],
    globalObjects = {
        'met'       : NTupleObject('met',      metType, help='PF MET after default type 1 corrections'),
        'metNoHF'   : NTupleObject('metNoHF',  metType, help='PF MET after default type 1 corrections without HF'),
    },
    collections = {
        #'xcleanLeptons'       : NTupleCollection('lepton', leptonType, 1, help='Muon or Electron collection'),
        'inclusiveElectrons'   : NTupleCollection('electron', leptonType, 5, help='inclusive Electron collection'),
        'inclusiveMuons'       : NTupleCollection('muon', leptonType, 5, help='inclusive Muon collection'),
        'xcleanJets'          : NTupleCollection('jet', jetType, 8, help='cleaned Jet collection'),
        'xcleanJetsAK8'       : NTupleCollection('fatjet', fatjetType, 2, help='cleaned fatJet collection'),
    }
)



##############################
### SEQUENCE               ###
##############################

sequence = [
    jsonAnalyzer, 
    lheAnalyzer,
    generatorAnalyzer,
    #pdfAnalyzer,
    triggerAnalyzer,
    filterAnalyzer,
    pileupAnalyzer,
    vertexAnalyzer,
    MEtAnalyzer,
    MEtNoHFAnalyzer,
    photonAnalyzer,
    leptonAnalyzer,
    tauAnalyzer,
    jetAnalyzer,
    fatJetAnalyzer,
    TriggerMatchAnalyzer,
    PreselectionAnalyzer,
    XCleaningAnalyzer,
    SSRegionTreeProducer,
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
from DMPD.Heppy.samples.Spring15.fileLists import mcsamples
from DMPD.Heppy.samples.Data.fileLists import datasamples

maxlsftime   = 5  # in hours
eventspersec = 5 # in ev/s

sample = {}
for i in datasamples:
    if int(datasamples[i]['nevents']) < 1: continue
    sample[i] = cfg.Component(
        files   = datasamples[i]['files'],
        name    = i,
        json    = '%s/src/DMPD/Heppy/python/tools/JSON/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt' % os.environ['CMSSW_BASE'],
        splitFactor = int(datasamples[i]['nevents']/(maxlsftime*3600*eventspersec)),
    )

for i in mcsamples:
    if int(mcsamples[i]['nevents']) < 1: continue
    #print i, " - ", int(mcsamples[i]['nevents']/(maxlsftime*3600*eventspersec))
    sample[i] = cfg.MCComponent(
        files   = mcsamples[i]['files'],
        name    = i,
        isMC    = True,
        isEmbed = False,
        splitFactor = int(mcsamples[i]['nevents']/(maxlsftime*3600*eventspersec)),
    )

testDataCompontent = cfg.Component(
        files   = ['dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring15MiniAODv2/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/548FB0B9-D072-E511-84CA-0025908653C4.root',],
        name    = "test",
        json    = '%s/src/DMPD/Heppy/python/tools/JSON/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt' % os.environ['CMSSW_BASE'],
        splitFactor = 1,
    )

testMCCompontent = cfg.MCComponent(
        files   = ['dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms//store/mc/RunIISpring15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/00759690-D16E-E511-B29E-00261894382D.root',],
        isMC    = True,
        name    = "test",
        splitFactor = 1,
    )

##############################
### FWLITE                 ###
##############################

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

## MC ###
selectedComponents = [

 #sample['DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v2'],
 #sample['DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1'],
 ##sample['DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],

 #sample['DYJetsToNuNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1'],
 #sample['ZJetsToNuNu_HT-100To200_13TeV-madgraph-v1'],
 #sample['ZJetsToNuNu_HT-200To400_13TeV-madgraph-v1'],
 #sample['ZJetsToNuNu_HT-400To600_13TeV-madgraph-v1'],
 #sample['ZJetsToNuNu_HT-600ToInf_13TeV-madgraph-v2'],

 ####sample['GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 ###sample['GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 ###sample['GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 ###sample['GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 ###sample['GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],

 #sample['QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],

 #sample['ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1-v1'],
 #sample['ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1-v1'],
 #sample['ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1-v1'],
 #sample['ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1-v1'],
 #sample['ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1-v2'],

 sample['TT_TuneCUETP8M1_13TeV-powheg-pythia8-v1'],
 ##sample['TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],

 #sample['WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
# sample['WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
# sample['WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
# sample['WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
# sample['WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],
 #sample['WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1'],
#  sample['WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'],


 #sample['WW_TuneCUETP8M1_13TeV-pythia8-v1'],
 #sample['WZ_TuneCUETP8M1_13TeV-pythia8-v1'],
 #sample['ZZ_TuneCUETP8M1_13TeV-pythia8-v1'],

 #sample['ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8-v1'],
 ##sample['ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8-v1'],
 #sample['ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8-v1'],
]
TriggerMatchAnalyzer.processName = 'PAT'


#### DATA ###
#selectedComponents = [
 ####Run2015D PromptReco
 #sample['DoubleEG_Run2015D-PromptReco-v4'],
 #sample['DoubleMuon_Run2015D-PromptReco-v4'],
 #sample['MET_Run2015D-PromptReco-v4'],
 #sample['SingleElectron_Run2015D-PromptReco-v4'],
 #sample['SingleMuon_Run2015D-PromptReco-v4'],
##  sample['SinglePhoton_Run2015D-PromptReco-v4'],

 ####Run2015C O5Oct2015
 #sample['DoubleEG_Run2015C-05Oct2015-v1'],
 #sample['DoubleMuon_Run2015C-05Oct2015-v1'],
 #sample['MET_Run2015C-05Oct2015-v1'],
 #sample['SingleElectron_Run2015C-05Oct2015-v1'],
 #sample['SingleMuon_Run2015C-05Oct2015-v1'],
##  sample['SinglePhoton_Run2015C-05Oct2015-v1'],
#]
#filterAnalyzer.processName = 'RECO'
#TriggerMatchAnalyzer.processName = 'RECO'

#### DATA ###
#selectedComponents = [
 ### Run2015D
 #sample['DoubleEG_Run2015D-05Oct2015-v1'],
 #sample['DoubleMuon_Run2015D-05Oct2015-v1'],
 #sample['MET_Run2015D-05Oct2015-v1'],
 #sample['SingleElectron_Run2015D-05Oct2015-v1'],
 #sample['SingleMuon_Run2015D-05Oct2015-v1'],
##  sample['SinglePhoton_Run2015D-05Oct2015-v1'],
#]
#filterAnalyzer.processName = 'RECO'
#TriggerMatchAnalyzer.processName = 'PAT'

#selectedComponents = [sample['SYNCH_ADDMonojet'],]
#selectedComponents = [sample['SYNCH_TTBar'],]
#selectedComponents = [sample['SYNCH_DYJetsToLL'],]
#selectedComponents = [sample['SYNCH_WJetsToLNu'],]
#selectedComponents = [sample['SYNCH_RSGravitonToGaGa'],]
#selectedComponents = [sample['SYNCH_ADDMonojet'],sample['SYNCH_TTBar'],sample['SYNCH_DYJetsToLL'],sample['SYNCH_WJetsToLNu'],sample['SYNCH_RSGravitonToGaGa'],]

#selectedComponents = [testDataCompontent,]
#filterAnalyzer.processName = 'RECO'
#TriggerMatchAnalyzer.processName = 'PAT'

#selectedComponents = [testMCCompontent,]
#TriggerMatchAnalyzer.processName = 'PAT'

from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
preprocessor = CmsswPreprocessor("preprocessor.py")

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
        nEvents=100000,
        )
    looper.loop()
    looper.write()
