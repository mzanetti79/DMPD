#! /usr/bin/env python

import os, multiprocessing, math
from array import array
from ROOT import TFile, TH1, TF1, TLorentzVector

from DMPD.Heppy.samples.Spring15.xSections import xsections, kfactors, xsectionsunc

#ROOT.gROOT.SetBatch(1)

#1.28/fb   Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt
#2.1/fb    Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt

ref_kf_file         = '%s/src/DMPD/Heppy/python/tools/Kfactors.root' % os.environ['CMSSW_BASE']
#ref_pu_file         = '%s/src/DMPD/Heppy/python/tools/PU/PU.root' % os.environ['CMSSW_BASE']
#ref_pu_file         = '%s/src/DMPD/Heppy/python/tools/PU/PU_1p3fb.root' % os.environ['CMSSW_BASE']
ref_pu_file         = '%s/src/DMPD/Heppy/python/tools/PU/PU_2p1fb.root' % os.environ['CMSSW_BASE']
ref_btag_file       = '%s/src/DMPD/Heppy/python/tools/BTAG/CSVv2.csv' % os.environ['CMSSW_BASE']
ref_csv_file        = '%s/src/DMPD/Heppy/python/tools/BTAG/BTagShapes.root' % os.environ['CMSSW_BASE']
ref_recoilMC_file   = '%s/src/DMPD/Heppy/python/tools/RECOIL/recoilfit_gjetsMC_Zu1_pf_v5.root' % os.environ['CMSSW_BASE']
ref_recoilData_file = '%s/src/DMPD/Heppy/python/tools/RECOIL/recoilfit_gjetsData_Zu1_pf_v5.root' % os.environ['CMSSW_BASE']
ref_muTrig_file     = '%s/src/DMPD/Heppy/python/tools/HLT/SingleMuonTrigger_Z_RunCD_Reco74X_Dec1.root' % os.environ['CMSSW_BASE']
ref_muId_file       = '%s/src/DMPD/Heppy/python/tools/SFMUON/MuonID_Z_RunCD_Reco74X_Dec1.root' % os.environ['CMSSW_BASE']
ref_muIso_file      = '%s/src/DMPD/Heppy/python/tools/SFMUON/MuonIso_Z_RunCD_Reco74X_Dec1.root' % os.environ['CMSSW_BASE']
ref_muHighpt_file   = '%s/src/DMPD/Heppy/python/tools/SFMUON/MuonHighPt_Z_RunCD_Reco74X_Dec17.root' % os.environ['CMSSW_BASE']
ref_ele_file        = '%s/src/DMPD/Heppy/python/tools/SFELE/scalefactors_ele.root' % os.environ['CMSSW_BASE']
ref_trig_file       = '%s/src/DMPD/Heppy/python/tools/HLT/TriggerEffSF.root' % os.environ['CMSSW_BASE']
ref_ewcorr_file     = '%s/src/DMPD/Heppy/python/tools/EW/scalefactors_v4.root' % os.environ['CMSSW_BASE']

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input', action='store', type='string', dest='origin', default='')
parser.add_option('-o', '--output', action='store', type='string', dest='target', default='')
parser.add_option('-j', '--json', action='store', type='string', dest='json', default='')
parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)

(options, args) = parser.parse_args()

origin      = options.origin
target      = options.target
json_path   = options.json
verboseon   = options.verbose

numberOfJets = {'ZCR' : 3, 'WCR' : 4, 'TCR' : 3, 'SR': 4}

import json

if len(json_path) <= 0 or not os.path.exists(json_path):
    print '  WARNING, no JSON file (-j option) has been specified'#. Press Enter to continue'
    #raw_input()
    isJson_file = False
else:
    with open(json_path) as json_file:    
        json_data = json.load(json_file)
    isJson_file = True

if not os.path.exists(origin):
    print 'Origin directory', origin, 'does not exist, aborting...'
    exit()
if not os.path.exists(target):
    print 'Target directory', target,'does not exist, aborting...'
    exit()

##############################

### Btagging setup ###

import ROOT
# from within CMSSW:
ROOT.gSystem.Load('libCondFormatsBTagObjects')
# OR using standalone code:
ROOT.gROOT.ProcessLine('.L %s/src/DMPD/Heppy/python/tools/BTAG/BTagCalibrationStandalone.cc+' % os.environ['CMSSW_BASE'])

fl = ['B', 'C', 'L']
wp = ['L', 'M', 'T']
workingpoint = [0., 0.605, 0.890, 0.980, 1.]
shape = {}

calib = ROOT.BTagCalibration('csvv2', ref_btag_file)
reader = {}
for i, w in enumerate(wp):
    reader[w] = {}
    reader[w][0] = ROOT.BTagCalibrationReader(calib, i, 'comb', 'central')
    reader[w][1] = ROOT.BTagCalibrationReader(calib, i, 'comb', 'up')
    reader[w][-1] = ROOT.BTagCalibrationReader(calib, i, 'comb', 'down')


shFile = TFile(ref_csv_file, 'READ')
shFile.cd()
if not shFile.IsZombie():
    for i, f in enumerate(fl):
        shape[f] = shFile.Get('j_bTagDiscr'+f)
else: print ' - BTagWeight Error: No Shape File'

for i, f in enumerate(fl):
    #shape[f].Smooth(100)
    #shape[f].Rebin(10)
    shape[f].Scale(1./shape[f].Integral())


def returnNewWorkingPoint(f, p, pt, eta, sigma):
    if f<0 or f>2: print ' - BTagWeight Error: unrecognized flavour', f
    if p<0 or p>4: print ' - BTagWeight Error: working point', p, 'not defined'
    if p==0 or p==4: return workingpoint[p]
    
    integral = shape[fl[f]].Integral(shape[fl[f]].FindBin(workingpoint[p]), shape[fl[f]].GetNbinsX()+1)
    
    sf = reader[wp[p-1]][sigma].eval(f, eta, pt)
    if sf <= 0: return workingpoint[p]
    integral /= sf
    
    n = shape[fl[f]].GetNbinsX()+1
    step = 100
    for i in list(reversed(range(0, n, step))):
        if shape[fl[f]].Integral(i-step + 1, n) >= integral:
            for j in list(reversed(range(0, i, step/10))):
                if shape[fl[f]].Integral(j-step/10 + 1, n) >= integral:
                    for k in list(reversed(range(0, j, step/100))):
                        if shape[fl[f]].Integral(k-step/100 + 1, n) >= integral:
                            return (k-1.)/(n-1.)

    return workingpoint[p]


def returnReshapedDiscr(f, discr, pt, eta, sigma=''):
    if discr<0.001: return discr
    if discr>1: return 1.
    if f<0 or f>2: return discr
    i0, i1 = 0, 4
    x0, x1 = 0., 1.
    
    for i in range(1, 5):
        if discr<=workingpoint[i]:
            x0 = workingpoint[i-1]
            x1 = workingpoint[i]
            i0 = i-1
            i1 = i
            break
    
    y0 = returnNewWorkingPoint(f, i0, pt, eta, sigma)
    y1 = returnNewWorkingPoint(f, i1, pt, eta, sigma)
    d = y0 + (discr-x0)*((y1-y0)/(x1-x0))
    if d < 0.: d = 0.
    if d > 1.: d = 1.
    return d

### RECOIL CORRECTIONS SETUP ###

ROOT.gROOT.ProcessLine('.L %s/src/DMPD/Heppy/python/tools/RECOIL/RecoilCorrector.hh+' % os.environ['CMSSW_BASE'])
Recoil = ROOT.RecoilCorrector(ref_recoilMC_file)
Recoil.addDataFile(ref_recoilData_file)
Recoil.addMCFile(ref_recoilMC_file)

### ELECTROWEAK CORRECTIONS SETUP ###

ewFile = TFile(ref_ewcorr_file, 'READ')
ewFile.cd()

if ewFile.IsZombie():
    print 'No EW corrections file found, aborting...'
    exit()
    
ewcorrFunc_z     = ewFile.Get("z_ewkcorr/z_ewkcorr_func")
ewcorrFunc_w     = ewFile.Get("w_ewkcorr/w_ewkcorr_func")


def isJSON(run, lumi):
    runstr = '%d' % run
    if not runstr in json_data:
        return False
    else:
        if any(l <= lumi <= u for [l, u] in json_data[runstr]):
            return True
    return False


def processFile(dir_name, verbose=False):
    
    #print '##################################################'
    print dir_name#, ':'
    #print '##################################################'
    
    isMC = not '2015' in dir_name
    
    # Unweighted input
    ref_file_name = origin + '/' + dir_name + '/Loop/tree.root'
    if not os.path.exists(ref_file_name): 
        print '  WARNING: file', ref_file_name, 'does not exist, continuing'
        return True
    
    # Weighted output
    new_file_name = target + '/' + dir_name + '.root'
    if os.path.exists(new_file_name):
        print '  WARNING: weighted file exists, overwriting', new_file_name
        #return True
    
    new_file = TFile(new_file_name, 'RECREATE')
    new_file.cd()
    
    # Get event number
    ref_file = TFile(ref_file_name, 'READ')
    ref_hist = ref_file.Get('Counters/Counter')
    totalEntries = ref_hist.GetBinContent(0)
    if isMC: 
        weightXS = xsections[dir_name[:-3]]/totalEntries
        if dir_name[:-3] in kfactors: kfactorXS = kfactors[dir_name[:-3]]
        else: kfactorXS = 1.
    else: weightXS = kfactorXS = 1.
    
    
    # K factors
    kfFile = TFile(ref_kf_file, 'READ')
    zkf = kfFile.Get("Zkfactor")
    wkf = kfFile.Get("Wkfactor")
    if verbose: print 'Kfactors histogram entries: ', zkf.GetEntries(), wkf.GetEntries()
    
    # PU reweighting
    puFile = TFile(ref_pu_file, 'READ')
    puRatio = puFile.Get('ratio')
    puRatioUp = puFile.Get('ratioUp')
    puRatioDown = puFile.Get('ratioDown')
    if verbose: print 'PU histogram entries: ', puRatio.GetEntries()
    
    # Muon trigger SF
    #mutrigRunCFile = TFile(ref_muTrig_file, 'READ')
    #trigMuRunCSF = mutrigRunCFile.Get('MuTrig_SF')  
    
    #mutrigRunDv42File = TFile(ref_muTrig_file, 'READ')
    #trigMuRunDv42SF = mutrigRunDv42File.Get('MuTrig_SF')  
    
    #mutrigRunDv43File = TFile(ref_muTrig_file, 'READ')
    #trigMuRunDv43SF = mutrigRunDv43File.Get('MuTrig_SF')  

    # Muon trigger SF
    trigMuFile = TFile(ref_muTrig_file, 'READ')
    trigMuSF_C = trigMuFile.Get('runCreRECO_IsoMu20_OR_IsoTkMu20_PtEtaBins/pt_abseta_ratio')
    trigMuSF_C.Scale(18)
    trigMuSF_D1 = trigMuFile.Get('runD_IsoMu20_OR_IsoTkMu20_HLTv4p2_PtEtaBins/pt_abseta_ratio')
    trigMuSF_D1.Scale(594-18)
    trigMuSF_D2 = trigMuFile.Get('runD_IsoMu20_OR_IsoTkMu20_HLTv4p3_PtEtaBins/pt_abseta_ratio')
    trigMuSF_D2.Scale(2110-594-18)
    trigMuSF = trigMuSF_C.Clone("trigMuSF")
    trigMuSF.Add(trigMuSF_D1)
    trigMuSF.Add(trigMuSF_D2)
    trigMuSF.Scale(1./2110)
    trigMu45SF = trigMuFile.Get('runD_Mu45_eta2p1_PtEtaBins/pt_abseta_ratio')
    trigMu50SF = trigMuFile.Get('runD_Mu50_PtEtaBins/pt_abseta_ratio')
    
    # trigger SF
    trigFile = TFile(ref_trig_file, 'READ')
    #
    #trigMuSF = trigFile.Get('MuTrig_SF')
    #trigMuSFUp = trigFile.Get('MuTrig_SFUp')
    #trigMuSFDown = trigFile.Get('MuTrig_SFDown')
    #
    trigEleSF = trigFile.Get('EleTrig_SF')
    trigEleSFUp = trigFile.Get('EleTrig_SFUp')
    trigEleSFDown = trigFile.Get('EleTrig_SFDown')
    #
    trigMETSF = trigFile.Get('METTrig_SF')
    trigMETSFUp = trigFile.Get('METTrig_SFUp')
    trigMETSFDown = trigFile.Get('METTrig_SFDown')
    
    # Electron Id+Iso
    eleFile = TFile(ref_ele_file, 'READ')
    eleVeto = eleFile.Get('unfactorized_scalefactors_Veto_ele')
    eleTight = eleFile.Get('unfactorized_scalefactors_Tight_ele')
    
    # Muon Id
    muonIdFile = TFile(ref_muId_file, 'READ')
    muonIdLoose = muonIdFile.Get('NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio')
    muonIdTight = muonIdFile.Get('NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio')
    
    # Muon Iso
    muonIsoFile = TFile(ref_muIso_file, 'READ')
    muonIsoLoose = muonIsoFile.Get('NUM_LooseRelIso_DEN_LooseID_PAR_pt_spliteta_bin1/pt_abseta_ratio')
    muonIsoTight = muonIsoFile.Get('NUM_TightRelIso_DEN_TightID_PAR_pt_spliteta_bin1/pt_abseta_ratio')
    
    # Muon HighPt
    muonHighptFile = TFile(ref_muHighpt_file, 'READ')
    muonIdHighpt = muonHighptFile.Get('HighPtID_PtEtaBins_Pt53/pTtuneP_abseta_ratio')
    muonIsoHighpt = muonHighptFile.Get('tkRelIsoID_PtEtaBins_Pt53/pTtuneP_abseta_ratio')
    
    # Variables declaration
    eventWeight = array('f', [1.0])  # global event weight
    xsWeight = array('f', [1.0])  # weight due to the MC sample cross section
    sigxsWeight = array('f', [1.0])  # weight due to the MC sample cross section
    kfactorWeight = array('f', [1.0])  # weight due to the MC sample cross section
    kfactorWeightUp = array('f', [1.0])
    kfactorWeightDown = array('f', [1.0])
    pileupWeight = array('f', [1.0])  # weight from PU reweighting
    pileupWeightUp = array('f', [1.0])
    pileupWeightDown = array('f', [1.0])
    electroweakWeight = array('f', [1.0])  # weight from EW corrections
    triggerMuonWeight = array('f', [1.0]) # Weights for trigger
    triggerMuonWeightUp = array('f', [1.0])
    triggerMuonWeightDown = array('f', [1.0])
    triggerMuonIsoWeight = array('f', [1.0])
    triggerMuonIsoWeightUp = array('f', [1.0])
    triggerMuonIsoWeightDown = array('f', [1.0])
    triggerElectronWeight = array('f', [1.0])
    triggerElectronWeightUp = array('f', [1.0])
    triggerElectronWeightDown = array('f', [1.0])
    triggerElectronIsoWeight = array('f', [1.0])
    triggerElectronIsoWeightUp = array('f', [1.0])
    triggerElectronIsoWeightDown = array('f', [1.0])
    triggerMETWeight = array('f', [1.0])
    triggerMETWeightUp = array('f', [1.0])
    triggerMETWeightDown = array('f', [1.0])
    electronWeight = array('f', [1.0]) # Weights for leptons
    electronWeightUp = array('f', [1.0])
    electronWeightDown = array('f', [1.0])
    electronIsoWeight = array('f', [1.0])
    electronIsoWeightUp = array('f', [1.0])
    electronIsoWeightDown = array('f', [1.0])
    muonWeight = array('f', [1.0])
    muonWeightUp = array('f', [1.0])
    muonWeightDown = array('f', [1.0])
    muonIsoWeight = array('f', [1.0])
    muonIsoWeightUp = array('f', [1.0])
    muonIsoWeightDown = array('f', [1.0])
    btagWeight = array('f', [1.0])  # weight from btag SF
    btagWeightUp = array('f', [1.0])
    btagWeightDown = array('f', [1.0])
    nBtagJets = array('f', [1.0])
    nBtagSubJets = array('f', [1.0])
    # Lists of arrays do not work #@!
    CSV = {}
    CSVUp = {}
    CSVDown = {}
    for i in range(10):
        CSV[i] = array('f', [1.0])
        CSVUp[i] = array('f', [1.0])
        CSVDown[i] = array('f', [1.0])
    subjetCSV = {}
    subjetCSVUp = {}
    subjetCSVDown = {}
    for i in range(2):
        subjetCSV[i] = array('f', [1.0])
        subjetCSVUp[i] = array('f', [1.0])
        subjetCSVDown[i] = array('f', [1.0])
    # Recoil Variables
    cormet_pt         = array('f', [0.0])  
    cormet_phi        = array('f', [0.0])  
    cormet_ptScaleUp  = array('f', [0.0])  
    cormet_ptScaleDown= array('f', [0.0])
    cormet_ptResUp    = array('f', [0.0])
    cormet_ptResDown  = array('f', [0.0])
    fakecormet_pt         = array('f', [0.0])  
    fakecormet_phi        = array('f', [0.0])  
    fakecormet_ptScaleUp  = array('f', [0.0])  
    fakecormet_ptScaleDown= array('f', [0.0])
    fakecormet_ptResUp    = array('f', [0.0])
    fakecormet_ptResDown  = array('f', [0.0])

    # Looping over file content
    for key in ref_file.GetListOfKeys():
        obj = key.ReadObj()
          
        # Copy and rescale histograms
        if obj.IsA().InheritsFrom('TH1'):
            if verbose: print ' + TH1:', obj.GetName()
            new_file.cd()
            #if 'SR' in obj.GetName() or 'CR' in obj.GetName():
            #    obj.Add(ref_hist)
            if 'Counter' in obj.GetName():
                obj.Scale(weightXS)
            obj.SetBinContent(0, totalEntries)
            new_file.cd()
            obj.Write()
        
        # Copy trees
        elif obj.IsA().InheritsFrom('TTree'):
            nev = obj.GetEntriesFast()
            njets = numberOfJets[obj.GetName()] if obj.GetName() in numberOfJets else 0 #FIXME
            nbjets = 1 if hasattr(obj, 'bjet1_CSV') else 0
            new_file.cd()
            new_tree = obj.CloneTree(-1, 'fast')
            # New branches
            eventWeightBranch = new_tree.Branch('eventWeight', eventWeight, 'eventWeight/F')
            xsWeightBranch = new_tree.Branch('xsWeight', xsWeight, 'xsWeight/F')
            sigxsWeightBranch = new_tree.Branch('sigxsWeight', sigxsWeight, 'sigxsWeight/F')
            kfactorWeightBranch = new_tree.Branch('kfactorWeight', kfactorWeight, 'kfactorWeight/F')
            kfactorWeightUpBranch = new_tree.Branch('kfactorWeightUp', kfactorWeightUp, 'kfactorWeightUp/F')
            kfactorWeightDownBranch = new_tree.Branch('kfactorWeightDown', kfactorWeightDown, 'kfactorWeightDown/F')
            electroweakWeightBranch = new_tree.Branch('electroweakWeight', electroweakWeight, 'electroweakWeight/F')
            pileupWeightBranch = new_tree.Branch('pileupWeight', pileupWeight, 'pileupWeight/F')
            pileupWeightUpBranch = new_tree.Branch('pileupWeightUp', pileupWeightUp, 'pileupWeightUp/F')
            pileupWeightDownBranch = new_tree.Branch('pileupWeightDown', pileupWeightDown, 'pileupWeightDown/F')
            triggerMuonWeightBranch = new_tree.Branch('triggerMuonWeight', triggerMuonWeight, 'triggerMuonWeight/F')
            triggerMuonWeightUpBranch = new_tree.Branch('triggerMuonWeightUp', triggerMuonWeightUp, 'triggerMuonWeightUp/F')
            triggerMuonWeightDownBranch = new_tree.Branch('triggerMuonWeightDown', triggerMuonWeightDown, 'triggerMuonWeightDown/F')
            triggerMuonIsoWeightBranch = new_tree.Branch('triggerMuonIsoWeight', triggerMuonIsoWeight, 'triggerMuonIsoWeight/F')
            triggerMuonIsoWeightUpBranch = new_tree.Branch('triggerMuonIsoWeightUp', triggerMuonIsoWeightUp, 'triggerMuonIsoWeightUp/F')
            triggerMuonIsoWeightDownBranch = new_tree.Branch('triggerMuonIsoWeightDown', triggerMuonIsoWeightDown, 'triggerMuonIsoWeightDown/F')
            triggerElectronWeightBranch = new_tree.Branch('triggerElectronWeight', triggerElectronWeight, 'triggerElectronWeight/F')
            triggerElectronWeightUpBranch = new_tree.Branch('triggerElectronWeightUp', triggerElectronWeightUp, 'triggerElectronWeightUp/F')
            triggerElectronWeightDownBranch = new_tree.Branch('triggerElectronWeightDown', triggerElectronWeightDown, 'triggerElectronWeightDown/F')
            triggerElectronIsoWeightBranch = new_tree.Branch('triggerElectronIsoWeight', triggerElectronIsoWeight, 'triggerElectronIsoWeight/F')
            triggerElectronIsoWeightUpBranch = new_tree.Branch('triggerElectronIsoWeightUp', triggerElectronIsoWeightUp, 'triggerElectronIsoWeightUp/F')
            triggerElectronIsoWeightDownBranch = new_tree.Branch('triggerElectronIsoWeightDown', triggerElectronIsoWeightDown, 'triggerElectronIsoWeightDown/F')
            triggerMETWeightBranch = new_tree.Branch('triggerMETWeight', triggerMETWeight, 'triggerMETWeight/F')
            triggerMETWeightUpBranch = new_tree.Branch('triggerMETWeightUp', triggerMETWeightUp, 'triggerMETWeightUp/F')
            triggerMETWeightDownBranch = new_tree.Branch('triggerMETWeightDown', triggerMETWeightDown, 'triggerMETWeightDown/F')
            electronWeightBranch = new_tree.Branch('electronWeight', electronWeight, 'electronWeight/F')
            electronWeightUpBranch = new_tree.Branch('electronWeightUp', electronWeightUp, 'electronWeightUp/F')
            electronWeightDownBranch = new_tree.Branch('electronWeightDown', electronWeightDown, 'electronWeightDown/F')
            electronIsoWeightBranch = new_tree.Branch('electronIsoWeight', electronIsoWeight, 'electronIsoWeight/F')
            electronIsoWeightUpBranch = new_tree.Branch('electronIsoWeightUp', electronIsoWeightUp, 'electronIsoWeightUp/F')
            electronIsoWeightDownBranch = new_tree.Branch('electronIsoWeightDown', electronIsoWeightDown, 'electronIsoWeightDown/F')
            muonWeightBranch = new_tree.Branch('muonWeight', muonWeight, 'muonWeight/F')
            muonWeightUpBranch = new_tree.Branch('muonWeightUp', muonWeightUp, 'muonWeightUp/F')
            muonWeightDownBranch = new_tree.Branch('muonWeightDown', muonWeightDown, 'muonWeightDown/F')
            muonIsoWeightBranch = new_tree.Branch('muonIsoWeight', muonIsoWeight, 'muonIsoWeight/F')
            muonIsoWeightUpBranch = new_tree.Branch('muonIsoWeightUp', muonIsoWeightUp, 'muonIsoWeightUp/F')
            muonIsoWeightDownBranch = new_tree.Branch('muonIsoWeightDown', muonIsoWeightDown, 'muonIsoWeightDown/F')
            btagWeightBranch = new_tree.Branch('btagWeight', btagWeight, 'btagWeight/F')
            btagWeightUpBranch = new_tree.Branch('btagWeightUp', btagWeightUp, 'btagWeightUp/F')
            btagWeightDownBranch = new_tree.Branch('btagWeightDown', btagWeightDown, 'btagWeightDown/F')
            nBtagJetsBranch = new_tree.Branch('nBtagJets', nBtagJets, 'nBtagJets/F')
            CSVBranch = {}
            CSVUpBranch = {}
            CSVDownBranch = {}
            for i in range(njets+nbjets):
                CSVBranch[i] = new_tree.Branch('jet%d_CSVR' % (i+1), CSV[i], 'jet%d_CSVR/F' % (i+1)) if i < njets else new_tree.Branch('bjet1_CSVR', CSV[i], 'bjet1_CSVR/F')
                CSVUpBranch[i] = new_tree.Branch('jet%d_CSVRUp' % (i+1), CSVUp[i], 'jet%d_CSVRUp/F' % (i+1)) if i < njets else new_tree.Branch('bjet1_CSVRUp', CSVUp[i], 'bjet1_CSVRUp/F')
                CSVDownBranch[i] = new_tree.Branch('jet%d_CSVRDown' % (i+1), CSVDown[i], 'jet%d_CSVRDown/F' % (i+1)) if i < njets else new_tree.Branch('bjet1_CSVRDown', CSVDown[i], 'bjet1_CSVRDown/F')
            subjetCSVBranch = {}
            subjetCSVUpBranch = {}
            subjetCSVDownBranch = {}
            for i in range(2):
                subjetCSVBranch[i] = new_tree.Branch('fatjet1_CSVR%d' % (i+1), subjetCSV[i], 'fatjet1_CSVR%d/F' % (i+1))
                subjetCSVUpBranch[i] = new_tree.Branch('fatjet1_CSVR%dUp' % (i+1), subjetCSVUp[i], 'fatjet1_CSVR%dUp/F' % (i+1))
                subjetCSVDownBranch[i] = new_tree.Branch('fatjet1_CSVR%dDown' % (i+1), subjetCSVDown[i], 'fatjet1_CSVR%dDown/F' % (i+1))
            nBtagSubJetsBranch = new_tree.Branch('fatjet1_nBtag', nBtagSubJets, 'fatjet1_nBtag/F')
            cormet_ptBranch          = new_tree.Branch('cormet_pt',          cormet_pt,          'cormet_pt/F')
            cormet_phiBranch         = new_tree.Branch('cormet_phi',         cormet_phi,         'cormet_phi/F')
            cormet_ptScaleUpBranch   = new_tree.Branch('cormet_ptScaleUp',   cormet_ptScaleUp,   'cormet_ptScaleUp/F')
            cormet_ptScaleDownBranch = new_tree.Branch('cormet_ptScaleDown', cormet_ptScaleDown, 'cormet_ptScaleDown/F')
            cormet_ptResUpBranch     = new_tree.Branch('cormet_ptResUp',     cormet_ptResUp,     'cormet_ptResUp/F')
            cormet_ptResDownBranch   = new_tree.Branch('cormet_ptResDown',   cormet_ptResDown,   'cormet_ptResDown/F')
            fakecormet_ptBranch          = new_tree.Branch('fakecormet_pt',          fakecormet_pt,          'fakecormet_pt/F')
            fakecormet_phiBranch         = new_tree.Branch('fakecormet_phi',         fakecormet_phi,         'fakecormet_phi/F')
            fakecormet_ptScaleUpBranch   = new_tree.Branch('fakecormet_ptScaleUp',   fakecormet_ptScaleUp,   'fakecormet_ptScaleUp/F')
            fakecormet_ptScaleDownBranch = new_tree.Branch('fakecormet_ptScaleDown', fakecormet_ptScaleDown, 'fakecormet_ptScaleDown/F')
            fakecormet_ptResUpBranch     = new_tree.Branch('fakecormet_ptResUp',     fakecormet_ptResUp,     'fakecormet_ptResUp/F')
            fakecormet_ptResDownBranch   = new_tree.Branch('fakecormet_ptResDown',   fakecormet_ptResDown,   'fakecormet_ptResDown/F')

            # looping over events
            for event in range(0, obj.GetEntries()):
                if verbose and (event%10000==0 or event==nev-1): print ' = TTree:', obj.GetName(), 'events:', nev, '\t', int(100*float(event+1)/float(nev)), '%\r',
                #print '.',#*int(20*float(event)/float(nev)),#printProgressBar(event, nev)
                obj.GetEntry(event)
                
                # Initialize
                eventWeight[0] = xsWeight[0] = kfactorWeight[0] = kfactorWeightUp[0] = kfactorWeightDown[0] = pileupWeight[0] = pileupWeightUp[0] = pileupWeightDown[0] = btagWeight[0] = btagWeightUp[0] = btagWeightDown[0] = electroweakWeight[0] = sigxsWeight[0] = 1.
                triggerMuonWeight[0] = triggerMuonWeightUp[0] = triggerMuonWeightDown[0] = triggerMuonIsoWeight[0] = triggerMuonIsoWeightUp[0] = triggerMuonIsoWeightDown[0] = 1.
                triggerElectronWeight[0] = triggerElectronWeightUp[0] = triggerElectronWeightDown[0] = triggerElectronIsoWeight[0] = triggerElectronIsoWeightUp[0] = triggerElectronIsoWeightDown[0] = 1.
                triggerMETWeight[0] = triggerMETWeightUp[0] = triggerMETWeightDown[0] = 1.
                electronWeight[0] = electronWeightUp[0] = electronWeightDown[0] = electronIsoWeight[0] = electronIsoWeightUp[0] = electronIsoWeightDown[0] = 1.
                muonWeight[0] = muonWeightUp[0] = muonWeightDown[0] = muonIsoWeight[0] = muonIsoWeightUp[0] = muonIsoWeightDown[0] = 1.
                
                nBtagJets[0] = nBtagSubJets[0] = 0
                for i in range(njets+nbjets):
                    CSV[i][0] = CSVUp[i][0] = CSVDown[i][0] = getattr(obj, 'jet%d_CSV' % (i+1) if i<njets else "bjet1_CSV", -99)
                for i in range(2):
                    subjetCSV[i][0] = subjetCSVUp[i][0] = subjetCSVDown[i][0] = getattr(obj, 'fatjet1_CSV%d' % (i+1), -99)
                
                
                # Weights
                if isMC:
                    ''' XSECTION '''
                    xsWeight[0] = weightXS if obj.genWeight > 0. else -weightXS
                    
                    ''' SIGNAL XSECTION WEIGHT [ RELATIVE UNCERTAINTY -> delta(sigma)/sigma ]'''
                    sigxsWeight[0] = (1.+abs(xsectionsunc[dir_name[:-3]]/xsections[dir_name[:-3]])) if dir_name[:-3] in xsectionsunc else 1.
                    
                    ''' K-FACTOR '''
                    kfactorWeight[0] = kfactorXS
                    ''' OLD K-FACTOR 
                    kfBin = max(zkf.GetXaxis().GetXmin(), min(zkf.FindBin(obj.genVpt), zkf.GetXaxis().GetXmax()))
                    if 'WJets' in dir_name and 'madgraph' in dir_name:
                        kfactorWeight[0] = wkf.GetBinContent(kfBin)
                        kfactorWeightUp[0] = wkf.GetBinContent(kfBin) + wkf.GetBinError(kfBin)
                        kfactorWeightDown[0] = wkf.GetBinContent(kfBin) - wkf.GetBinError(kfBin)
                    elif ('ZJets' in dir_name or 'DYJets' in dir_name) and 'madgraph' in dir_name:
                        kfactorWeight[0] = zkf.GetBinContent(kfBin)
                        kfactorWeightUp[0] = zkf.GetBinContent(kfBin) + zkf.GetBinError(kfBin)
                        kfactorWeightDown[0] = zkf.GetBinContent(kfBin) - zkf.GetBinError(kfBin)
                    '''
                    
                    ''' PILEUP '''
                    puBin = min(puRatio.FindBin(obj.nPU), puRatio.GetNbinsX())
                    pileupWeight[0] = puRatio.GetBinContent(puBin)
                    pileupWeightUp[0] = puRatioUp.GetBinContent(puBin)
                    pileupWeightDown[0] = puRatioDown.GetBinContent(puBin)
                    
                    ''' ELECTROWEAK '''                    
                    if 'DYJets' in dir_name or 'ZJets' in dir_name:
                        electroweakWeight[0]    = ewcorrFunc_z.Eval(obj.genVpt)
                    elif 'WJets' in dir_name:
                        electroweakWeight[0]    = ewcorrFunc_w.Eval(obj.genVpt)
                    
                    ''' TRIGGER '''
                    ### SINGLE MUON
                    if (( 'ZCR' in obj.GetName() and obj.isZtoMM ) or ( 'WCR' in obj.GetName() and obj.isWtoMN ) or ( 'TCR' in obj.GetName() )) and ( obj.HLT_BIT_HLT_IsoMu20_v or obj.HLT_BIT_HLT_IsoTkMu20_v ):
                        hbin = trigMuSF.FindBin(min(max(obj.lepton1_pt, trigMuSF.GetXaxis().GetXmin()), trigMuSF.GetXaxis().GetXmax()-1.), min(abs(obj.lepton1_eta), trigMuSF.GetYaxis().GetXmax()-0.01))
                        triggerMuonIsoWeight[0]        = trigMuSF.GetBinContent( hbin )
                        triggerMuonIsoWeightUp[0]      = trigMuSF.GetBinContent( hbin ) + trigMuSF.GetBinError( hbin )
                        triggerMuonIsoWeightDown[0]    = trigMuSF.GetBinContent( hbin ) - trigMuSF.GetBinError( hbin )
                    if ( 'XZh' in obj.GetName() and obj.isZtoMM ) or ( 'WCR' in obj.GetName() and obj.isWtoMN ):
                        if obj.HLT_BIT_HLT_Mu45_eta2p1_v:
                            hbin = trigMu45SF.FindBin(min(max(obj.lepton1_pt, trigMu45SF.GetXaxis().GetXmin()), trigMu45SF.GetXaxis().GetXmax()-1.), min(abs(obj.lepton1_eta), trigMu45SF.GetYaxis().GetXmax()-0.01))
                            triggerMuonWeight[0]        = trigMu45SF.GetBinContent( hbin )
                            triggerMuonWeightUp[0]      = trigMu45SF.GetBinContent( hbin ) + trigMu45SF.GetBinError( hbin )
                            triggerMuonWeightDown[0]    = trigMu45SF.GetBinContent( hbin ) - trigMu45SF.GetBinError( hbin )
                        elif obj.HLT_BIT_HLT_Mu50_v:
                            hbin = trigMu50SF.FindBin(min(max(obj.lepton1_pt, trigMu50SF.GetXaxis().GetXmin()), trigMu50SF.GetXaxis().GetXmax()-1.), min(abs(obj.lepton1_eta), trigMu50SF.GetYaxis().GetXmax()-0.01))
                            triggerMuonWeight[0]        = trigMu50SF.GetBinContent( hbin )
                            triggerMuonWeightUp[0]      = trigMu50SF.GetBinContent( hbin ) + trigMu50SF.GetBinError( hbin )
                            triggerMuonWeightDown[0]    = trigMu50SF.GetBinContent( hbin ) - trigMu50SF.GetBinError( hbin )
                    
                    ### SINGLE ELECTRON
                    if (( 'ZCR' in obj.GetName() and obj.isZtoEE ) or ( 'WCR' in obj.GetName() and obj.isWtoEN )) and ( obj.HLT_BIT_HLT_Ele27_WPLoose_Gsf_v or obj.HLT_BIT_HLT_Ele27_WP85_Gsf_v ): # or ( 'TCR' in obj.GetName() )) # do not apply electron trigger for TCR
                        hbin = trigEleSF.FindBin(min(max(obj.lepton1_pt, trigEleSF.GetXaxis().GetXmin()), trigEleSF.GetXaxis().GetXmax()-1.), min(abs(obj.lepton1_eta), trigEleSF.GetYaxis().GetXmax()-0.01))
                        triggerElectronIsoWeight[0]        = trigEleSF.GetBinContent( hbin )
                        triggerElectronIsoWeightUp[0]      = trigEleSFUp.GetBinContent( hbin )
                        triggerElectronIsoWeightDown[0]    = trigEleSFDown.GetBinContent( hbin )
                    if (( 'XZh' in obj.GetName() and obj.isZtoEE ) or ( 'WCR' in obj.GetName() and obj.isWtoEN )) and ( obj.HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v or obj.HLT_BIT_HLT_Ele115_CaloIdVT_GsfTrkIdT_v ): # or ( 'TCR' in obj.GetName() )) # do not apply electron trigger for TCR
                        triggerElectronWeight[0]        = 1.002
                        triggerElectronWeightUp[0]      = 1.002 + 0.017
                        triggerElectronWeightDown[0]    = 1.002 - 0.017
                    
                    ### MET
                    if 'SR' in obj.GetName() and ( obj.HLT_BIT_HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v or obj.HLT_BIT_HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v or obj.HLT_BIT_HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v or obj.HLT_BIT_HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v or obj.HLT_BIT_HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v or obj.HLT_BIT_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v ):
                        hbin = trigMETSF.FindBin(min(obj.met_pt, trigMETSF.GetXaxis().GetXmax()-1.))
                        triggerMETWeight[0]        = trigMETSF.GetBinContent( hbin )
                        triggerMETWeightUp[0]      = trigMETSFUp.GetBinContent( hbin )
                        triggerMETWeightDown[0]    = trigMETSFDown.GetBinContent( hbin )
                    
                    ''' ELECTRON ID+ISO '''
                    if ( 'ZCR' in obj.GetName() and obj.isZtoEE ) or ( 'WCR' in obj.GetName() and obj.isWtoEN ):
                        hbin = eleTight.FindBin(min(abs(obj.lepton1_eta), eleTight.GetXaxis().GetXmax()-0.01), min(obj.lepton1_pt, eleTight.GetYaxis().GetXmax()-1.))
                        electronIsoWeight[0]     *= eleTight.GetBinContent( hbin )
                        electronIsoWeightUp[0]   *= eleTight.GetBinContent( hbin ) + eleTight.GetBinError( hbin )
                        electronIsoWeightDown[0] *= eleTight.GetBinContent( hbin ) - eleTight.GetBinError( hbin )
                        electronWeight[0]     *= eleTight.GetBinContent( hbin )
                        electronWeightUp[0]   *= eleTight.GetBinContent( hbin ) + eleTight.GetBinError( hbin )
                        electronWeightDown[0] *= eleTight.GetBinContent( hbin ) - eleTight.GetBinError( hbin )
                    if 'TCR' in obj.GetName():
                        hbin = eleTight.FindBin(min(abs(obj.lepton2_eta), eleTight.GetXaxis().GetXmax()-0.01), min(obj.lepton2_pt, eleTight.GetYaxis().GetXmax()-1.))
                        electronIsoWeight[0]     *= eleTight.GetBinContent( hbin )
                        electronIsoWeightUp[0]   *= eleTight.GetBinContent( hbin ) + eleTight.GetBinError( hbin )
                        electronIsoWeightDown[0] *= eleTight.GetBinContent( hbin ) - eleTight.GetBinError( hbin )
                    if ( 'ZCR' in obj.GetName() and obj.isZtoEE ):
                        hbin = eleVeto.FindBin(min(abs(obj.lepton2_eta), eleVeto.GetXaxis().GetXmax()-0.01), min(obj.lepton2_pt, eleVeto.GetYaxis().GetXmax()-1.))
                        electronIsoWeight[0]     *= eleVeto.GetBinContent( hbin )
                        electronIsoWeightUp[0]   *= eleVeto.GetBinContent( hbin ) + eleTight.GetBinError( hbin )
                        electronIsoWeightDown[0] *= eleVeto.GetBinContent( hbin ) - eleTight.GetBinError( hbin )
                    if ( 'XZh' in obj.GetName() and obj.isZtoEE ):
                        hbin = eleVeto.FindBin(min(abs(obj.lepton1_eta), eleVeto.GetXaxis().GetXmax()-0.01), min(obj.lepton1_pt, eleVeto.GetYaxis().GetXmax()-1.))
                        electronWeight[0]     *= eleVeto.GetBinContent( hbin )
                        electronWeightUp[0]   *= eleVeto.GetBinContent( hbin ) + eleVeto.GetBinError( hbin )
                        electronWeightDown[0] *= eleVeto.GetBinContent( hbin ) - eleVeto.GetBinError( hbin )
                        hbin = eleVeto.FindBin(min(abs(obj.lepton2_eta), eleVeto.GetXaxis().GetXmax()-0.01), min(obj.lepton2_pt, eleVeto.GetYaxis().GetXmax()-1.))
                        electronWeight[0]     *= eleVeto.GetBinContent( hbin )
                        electronWeightUp[0]   *= eleVeto.GetBinContent( hbin ) + eleVeto.GetBinError( hbin )
                        electronWeightDown[0] *= eleVeto.GetBinContent( hbin ) - eleVeto.GetBinError( hbin )
                    
                    ''' MUON ID/ISO '''
                    if ( 'ZCR' in obj.GetName() and obj.isZtoMM ) or ( 'WCR' in obj.GetName() and obj.isWtoMN ) or ( 'TCR' in obj.GetName() ) or ( 'XZh' in obj.GetName() and obj.isZtoMM ):
                        hbin = muonIdTight.FindBin(min(max(obj.lepton1_pt, muonIdTight.GetXaxis().GetXmin()), muonIdTight.GetXaxis().GetXmax()-1.), min(abs(obj.lepton1_eta), muonIdTight.GetYaxis().GetXmax()-0.01))
                        muonIsoWeight[0]     *= muonIdTight.GetBinContent( hbin )
                        muonIsoWeightUp[0]   *= muonIdTight.GetBinContent( hbin ) + muonIdTight.GetBinError( hbin )
                        muonIsoWeightDown[0] *= muonIdTight.GetBinContent( hbin ) - muonIdTight.GetBinError( hbin )
                        muonIsoWeight[0]     *= muonIsoTight.GetBinContent( hbin )
                        muonIsoWeightUp[0]   *= muonIsoTight.GetBinContent( hbin ) + muonIsoTight.GetBinError( hbin )
                        muonIsoWeightDown[0] *= muonIsoTight.GetBinContent( hbin ) - muonIsoTight.GetBinError( hbin )
                        hbin = muonIdHighpt.FindBin(min(max(obj.lepton1_pt, muonIdHighpt.GetXaxis().GetXmin()), muonIdHighpt.GetXaxis().GetXmax()-1.), min(abs(obj.lepton1_eta), muonIdHighpt.GetYaxis().GetXmax()-0.01))
                        if obj.lepton1_highptId:
                            muonWeight[0]     *= muonIdHighpt.GetBinContent( hbin )
                            muonWeightUp[0]   *= muonIdHighpt.GetBinContent( hbin ) + muonIdHighpt.GetBinError( hbin )
                            muonWeightDown[0] *= muonIdHighpt.GetBinContent( hbin ) - muonIdHighpt.GetBinError( hbin )
                        muonWeight[0]     *= muonIsoHighpt.GetBinContent( hbin )
                        muonWeightUp[0]   *= muonIsoHighpt.GetBinContent( hbin ) + muonIsoHighpt.GetBinError( hbin )
                        muonWeightDown[0] *= muonIsoHighpt.GetBinContent( hbin ) - muonIsoHighpt.GetBinError( hbin )
                    if ( 'ZCR' in obj.GetName() and obj.isZtoMM ) or ( 'XZh' in obj.GetName() and obj.isZtoMM ):
                        hbin = muonIdLoose.FindBin(min(max(obj.lepton2_pt, muonIdLoose.GetXaxis().GetXmin()), muonIdLoose.GetXaxis().GetXmax()-1.), min(abs(obj.lepton2_eta), muonIdLoose.GetYaxis().GetXmax()-0.01))
                        muonIsoWeight[0]     *= muonIdLoose.GetBinContent( hbin )
                        muonIsoWeightUp[0]   *= muonIdLoose.GetBinContent( hbin ) + muonIdLoose.GetBinError( hbin )
                        muonIsoWeightDown[0] *= muonIdLoose.GetBinContent( hbin ) - muonIdLoose.GetBinError( hbin )
                        muonIsoWeight[0]     *= muonIsoLoose.GetBinContent( hbin )
                        muonIsoWeightUp[0]   *= muonIsoLoose.GetBinContent( hbin ) + muonIsoLoose.GetBinError( hbin )
                        muonIsoWeightDown[0] *= muonIsoLoose.GetBinContent( hbin ) - muonIsoLoose.GetBinError( hbin )
                        hbin = muonIdHighpt.FindBin(min(max(obj.lepton2_pt, muonIdHighpt.GetXaxis().GetXmin()), muonIdHighpt.GetXaxis().GetXmax()-1.), min(abs(obj.lepton2_eta), muonIdHighpt.GetYaxis().GetXmax()-0.01))
                        if obj.lepton2_highptId and not obj.lepton1_highptId:
                            muonWeight[0]     *= muonIdHighpt.GetBinContent( hbin )
                            muonWeightUp[0]   *= muonIdHighpt.GetBinContent( hbin ) + muonIdHighpt.GetBinError( hbin )
                            muonWeightDown[0] *= muonIdHighpt.GetBinContent( hbin ) - muonIdHighpt.GetBinError( hbin )
                        muonWeight[0]     *= muonIsoHighpt.GetBinContent( hbin )
                        muonWeightUp[0]   *= muonIsoHighpt.GetBinContent( hbin ) + muonIsoHighpt.GetBinError( hbin )
                        muonWeightDown[0] *= muonIsoHighpt.GetBinContent( hbin ) - muonIsoHighpt.GetBinError( hbin )
                        if muonWeight[0]<0.1: print obj.lepton2_pt, obj.lepton2_eta
                    
                    ''' BTAGGING '''
                    # Reshaping
                    nbtagjets = 0
                    sf = [1]*3
                    sfUp = [1]*3
                    sfDown = [1]*3
                    for i in range(njets+nbjets):
                        pt = getattr(obj, 'jet%d_pt' % (i+1) if i<njets else 'bjet1_pt', -1)
                        eta = getattr(obj, 'jet%d_eta' % (i+1) if i<njets else 'bjet1_eta', -1)
                        flav = getattr(obj, 'jet%d_flavour' % (i+1) if i<njets else 'bjet1_flavour', -1)
                        csv = getattr(obj, 'jet%d_CSV' % (i+1) if i<njets else 'bjet1_CSV', -1)
                        pt = min(pt, 669)
                        if abs(flav) == 5: fl = 0
                        elif abs(flav) == 4: fl = 1
                        else: fl = 2
#                        CSV[i][0] = reader['M'][0].eval(fl, eta, pt)
#                        CSVUp[i][0] = reader['M'][1].eval(fl, eta, pt)
#                        CSVDown[i][0] = reader['M'][-1].eval(fl, eta, pt)
                        CSV[i][0] = returnReshapedDiscr(fl, csv, pt, eta, 0)
                        CSVUp[i][0] = returnReshapedDiscr(fl, csv, pt, eta, +1)
                        CSVDown[i][0] = returnReshapedDiscr(fl, csv, pt, eta, -1)
                        if CSV[i][0] > workingpoint[2] and i<njets: nBtagJets[0] += 1
                        if i<3:
                            sf[i] = reader['M'][0].eval(fl, eta, pt)
                            sfUp[i] = reader['M'][1].eval(fl, eta, pt)
                            sfDown[i] = reader['M'][-1].eval(fl, eta, pt)
                            if csv>=workingpoint[2]: nbtagjets += 1
                    
                    # Subjet reshaping
                    for i in range(2):
                        pt = getattr(obj, 'fatjet1_pt%d' % (i+1), -1)
                        eta = getattr(obj, 'fatjet1_eta%d' % (i+1), -1)
                        flav = getattr(obj, 'fatjet1_flavour%d' % (i+1), -1)
                        csv = getattr(obj, 'fatjet1_CSV%d' % (i+1), -1)
                        pt = min(pt, 669)
                        if abs(flav) == 5: fl = 0
                        elif abs(flav) == 4: fl = 1
                        else: fl = 2
                        subjetCSV[i][0] = returnReshapedDiscr(fl, csv, pt, eta, 0)
                        subjetCSVUp[i][0] = returnReshapedDiscr(fl, csv, pt, eta, +1)
                        subjetCSVDown[i][0] = returnReshapedDiscr(fl, csv, pt, eta, -1)
                        if subjetCSV[i][0] > workingpoint[1]: nBtagSubJets[0] += 1
                    
                    
                    # Calculate weight
                    if njets <= 0:
                        btagWeight[0] = btagWeightUp[0] = btagWeightDown[0] = 1
                    elif njets == 1:
                        if nbtagjets == 0:
                            btagWeight[0] *= (1.-sf[0])
                            btagWeightUp[0] *= (1.-sfUp[0])
                            btagWeightDown[0] *= (1.-sfDown[0])
                        else:
                            btagWeight[0] *= sf[0]
                            btagWeightUp[0] *= sfUp[0]
                            btagWeightDown[0] *= sfDown[0]
                    elif njets == 2:
                        if nbtagjets == 0:
                            btagWeight[0] *= (1.-sf[0])*(1.-sf[1])
                            btagWeightUp[0] *= (1.-sfUp[0])*(1.-sfUp[1])
                            btagWeightDown[0] *= (1.-sfDown[0])*(1.-sfDown[1])
                        elif nbtagjets == 1:
                            btagWeight[0] *= (1.-sf[0])*sf[1] + sf[0]*(1.-sf[1])
                            btagWeightUp[0] *= (1.-sfUp[0])*sfUp[1] + sfUp[0]*(1.-sfUp[1])
                            btagWeightDown[0] *= (1.-sfDown[0])*sfDown[1] + sfDown[0]*(1.-sfDown[1])
                        else:
                            btagWeight[0] *= sf[0]*sf[1]
                            btagWeightUp[0] *= sfUp[0]*sfUp[1]
                            btagWeightDown[0] *= sfDown[0]*sfDown[1]
                    else:
                        if nbtagjets == 0:
                            btagWeight[0] *= (1.-sf[0])*(1.-sf[1])*(1.-sf[2])
                            btagWeightUp[0] *= (1.-sfUp[0])*(1.-sfUp[1])*(1.-sfUp[2])
                            btagWeightDown[0] *= (1.-sfDown[0])*(1.-sfDown[1])*(1.-sfDown[2])
                        elif nbtagjets == 1:
                            btagWeight[0] *= sf[0]*(1.-sf[1])*(1.-sf[2]) + sf[1]*(1.-sf[0])*(1.-sf[2]) + sf[2]*(1.-sf[0])*(1.-sf[1])
                            btagWeightUp[0] *= sfUp[0]*(1.-sfUp[1])*(1.-sfUp[2]) + sfUp[1]*(1.-sfUp[0])*(1.-sfUp[2]) + sfUp[2]*(1.-sfUp[0])*(1.-sfUp[1])
                            btagWeightDown[0] *= sfDown[0]*(1.-sfDown[1])*(1.-sfDown[2]) + sfDown[1]*(1.-sfDown[0])*(1.-sfDown[2]) + sfDown[2]*(1.-sfDown[0])*(1.-sfDown[1])
                        elif nbtagjets == 2:
                            btagWeight[0] *= sf[0]*sf[1]*(1.-sf[2]) + sf[0]*sf[2]*(1.-sf[1]) + sf[1]*sf[2]*(1.-sf[0])
                            btagWeightUp[0] *= sfUp[0]*sfUp[1]*(1.-sfUp[2]) + sfUp[0]*sfUp[2]*(1.-sfUp[1]) + sfUp[1]*sfUp[2]*(1.-sfUp[0])
                            btagWeightDown[0] *= sfDown[0]*sfDown[1]*(1.-sfDown[2]) + sfDown[0]*sfDown[2]*(1.-sfDown[1]) + sfDown[1]*sfDown[2]*(1.-sfDown[0])
                        else:
                            btagWeight[0] *= sf[0]*sf[1]*sf[2]
                            btagWeightUp[0] *= sfUp[0]*sfUp[1]*sfUp[2]
                            btagWeightDown[0] *= sfDown[0]*sfDown[1]*sfDown[2]
                    
                    
                    ''' RECOIL '''
                    ### fill default values
                    # in every region
                    cmetpt           = ROOT.Double(obj.met_pt)
                    cmetphi          = ROOT.Double(obj.met_phi)
                    cmetptScaleUp    = ROOT.Double(obj.met_pt)
                    cmetphiScaleUp   = ROOT.Double(obj.met_phi)
                    cmetptScaleDown  = ROOT.Double(obj.met_pt)
                    cmetphiScaleDown = ROOT.Double(obj.met_phi)
                    cmetptResUp      = ROOT.Double(obj.met_pt)
                    cmetphiResUp     = ROOT.Double(obj.met_phi)
                    cmetptResDown    = ROOT.Double(obj.met_pt)
                    cmetphiResDown   = ROOT.Double(obj.met_phi)
                    cfmetpt           = ROOT.Double(0.)
                    cfmetphi          = ROOT.Double(0.)
                    cfmetptScaleUp    = ROOT.Double(0.)
                    cfmetphiScaleUp   = ROOT.Double(0.)
                    cfmetptScaleDown  = ROOT.Double(0.)
                    cfmetphiScaleDown = ROOT.Double(0.)
                    cfmetptResUp      = ROOT.Double(0.)
                    cfmetphiResUp     = ROOT.Double(0.)
                    cfmetptResDown    = ROOT.Double(0.)
                    cfmetphiResDown   = ROOT.Double(0.)
                    # with valid fakemet in CRs
                    if (obj.GetName()=='ZCR' or obj.GetName()=='WCR' or obj.GetName()=='TCR'):
                        cfmetpt           = ROOT.Double(obj.fakemet_pt)
                        cfmetphi          = ROOT.Double(obj.fakemet_phi)
                        cfmetptScaleUp    = ROOT.Double(obj.fakemet_pt)
                        cfmetphiScaleUp   = ROOT.Double(obj.fakemet_phi)
                        cfmetptScaleDown  = ROOT.Double(obj.fakemet_pt)
                        cfmetphiScaleDown = ROOT.Double(obj.fakemet_phi)
                        cfmetptResUp      = ROOT.Double(obj.fakemet_pt)
                        cfmetphiResUp     = ROOT.Double(obj.fakemet_phi)
                        cfmetptResDown    = ROOT.Double(obj.fakemet_pt)
                        cfmetphiResDown   = ROOT.Double(obj.fakemet_phi)

                    applyrecoil    = True # safety (maybe useless now)
                    
                    # configure input parameters (GENMET / RECO_V_PT / RECOIL) only for Z->ll, Z->vv, and W->lv
                    if 'DYJets' in dir_name or 'ZJets' in dir_name or 'WJets' in dir_name:
                        if obj.GetName()=='ZCR' or obj.GetName()=='WCR'or obj.GetName()=='SR' or obj.GetName()=='TCR' :
                            genmetpt  = ROOT.Double(obj.genV_pt)
                            genmetphi = ROOT.Double(obj.genV_phi)
                            leppt     = ROOT.Double(0.)
                            lepphi    = ROOT.Double(0.)
                            Upar      = ROOT.Double(0.)
                            Uper      = ROOT.Double(0.)
                            if obj.GetName()=='SR':
                                leppt     = ROOT.Double(0.)
                                lepphi    = ROOT.Double(0.)
                                Upar      = ROOT.Double(0.)
                                Uper      = ROOT.Double(0.)
                            elif obj.GetName()=='ZCR':
                                leppt     = ROOT.Double(obj.Z_pt)
                                lepphi    = ROOT.Double(obj.Z_phi)
                                Upar      = ROOT.Double(obj.Upara)
                                Uper      = ROOT.Double(obj.Uperp)
                            elif obj.GetName()=='WCR':
                                leppt     = ROOT.Double(obj.lepton1_pt)
                                lepphi    = ROOT.Double(obj.lepton1_phi)
                                Upar      = ROOT.Double(obj.Upara)
                                Uper      = ROOT.Double(obj.Uperp)
                            elif obj.GetName()=='TCR':
                                # in situ evaluation of pseudo-boson (mu^\pm + e^\mp)
                                l1 = l2 = TLorentzVector(0,0,0,0) 
                                l1.SetPtEtaPhiM(obj.lepton1_pt,obj.lepton1_eta,obj.lepton1_phi,obj.lepton1_mass)
                                l2.SetPtEtaPhiM(obj.lepton2_pt,obj.lepton2_eta,obj.lepton2_phi,obj.lepton2_mass)
                                pseudoboson = l1+l2
                                recoilX = - obj.met_pt*math.cos(obj.met_phi) - pseudoboson.Px()
                                recoilY = - obj.met_pt*math.cos(obj.met_phi) - pseudoboson.Py()
                                pseudoUpara = (recoilX*pseudoboson.Px() + recoilY*pseudoboson.Py())/pseudoboson.Pt()
                                pseudoUperp = (recoilX*pseudoboson.Py() - recoilY*pseudoboson.Px())/pseudoboson.Pt()    
                                
                                leppt     = ROOT.Double(pseudoboson.Pt())
                                lepphi    = ROOT.Double(pseudoboson.Phi())
                                Upar      = ROOT.Double(pseudoUpara)
                                Uper      = ROOT.Double(pseudoUperp)
                            else:
                                applyrecoil = False
                            
                            if applyrecoil:
                                ### do the MET recoil corrections in SR, ZCR and WCR, only for DYJets, ZJets and WJets samples
                                Recoil.CorrectType2(cmetpt,          cmetphi,          genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 0,obj.nJets)        
                                Recoil.CorrectType2(cmetptScaleUp,   cmetphiScaleUp,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 3, 0,obj.nJets)        
                                Recoil.CorrectType2(cmetptScaleDown, cmetphiScaleDown, genmetpt,genmetphi,leppt,lepphi,Upar,Uper,-3, 0,obj.nJets)        
                                Recoil.CorrectType2(cmetptResUp,     cmetphiResUp,     genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 3,obj.nJets)        
                                Recoil.CorrectType2(cmetptResDown,   cmetphiResDown,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0,-3,obj.nJets)   
                                if obj.GetName()=='ZCR' or obj.GetName()=='WCR' or obj.GetName()=='TCR':
                                    ### correct fakeMET only in ZCR and WCR (and TCR)
                                    ### set reconstructed leptons and recoil to zero (as if in SR with fake-met)
                                    genmetpt  = ROOT.Double(obj.genV_pt)
                                    genmetphi = ROOT.Double(obj.genV_phi)
                                    leppt     = ROOT.Double(0.)
                                    lepphi    = ROOT.Double(0.)
                                    Upar      = ROOT.Double(0.)
                                    Uper      = ROOT.Double(0.)
                                    Recoil.CorrectType2(cfmetpt,          cfmetphi,          genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 0,obj.nJets)        
                                    Recoil.CorrectType2(cfmetptScaleUp,   cfmetphiScaleUp,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 3, 0,obj.nJets)        
                                    Recoil.CorrectType2(cfmetptScaleDown, cfmetphiScaleDown, genmetpt,genmetphi,leppt,lepphi,Upar,Uper,-3, 0,obj.nJets)        
                                    Recoil.CorrectType2(cfmetptResUp,     cfmetphiResUp,     genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 3,obj.nJets)        
                                    Recoil.CorrectType2(cfmetptResDown,   cfmetphiResDown,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0,-3,obj.nJets)   
                                pass
                            pass
                        pass
                    pass
                    
                    ### fill the variables
                    # add corrected MET in all regions
                    cormet_pt[0]         = cmetpt
                    cormet_phi[0]        = cmetphi
                    cormet_ptScaleUp[0]  = cmetptScaleUp
                    cormet_ptScaleDown[0]= cmetptScaleDown
                    cormet_ptResUp[0]    = cmetptResUp
                    cormet_ptResDown[0]  = cmetptResDown
                    # add corrected fake-MET in control regions only
                    if obj.GetName()=='ZCR' or obj.GetName()=='WCR' or obj.GetName()=='TCR':
                        fakecormet_pt[0]         = cfmetpt
                        fakecormet_phi[0]        = cfmetphi
                        fakecormet_ptScaleUp[0]  = cfmetptScaleUp
                        fakecormet_ptScaleDown[0]= cfmetptScaleDown
                        fakecormet_ptResUp[0]    = cfmetptResUp
                        fakecormet_ptResDown[0]  = cfmetptResDown               
                #### Data
                ### fill the recoil corrected variables for consistency (with uncorrected values)
                else:
                    cormet_pt[0]         = obj.met_pt
                    cormet_phi[0]        = obj.met_phi
                    cormet_ptScaleUp[0]  = obj.met_pt
                    cormet_ptScaleDown[0]= obj.met_pt
                    cormet_ptResUp[0]    = obj.met_pt
                    cormet_ptResDown[0]  = obj.met_pt
                    if obj.GetName()=='ZCR' or obj.GetName()=='WCR' or obj.GetName()=='TCR':
                        fakecormet_pt[0]         = obj.fakemet_pt
                        fakecormet_phi[0]        = obj.fakemet_phi
                        fakecormet_ptScaleUp[0]  = obj.fakemet_pt
                        fakecormet_ptScaleDown[0]= obj.fakemet_pt
                        fakecormet_ptResUp[0]    = obj.fakemet_pt
                        fakecormet_ptResDown[0]  = obj.fakemet_pt               
                    
                    # b-tagging multiplicity
                    for i in range(njets):
                        if getattr(obj, 'jet%d_CSV' % (i+1), -1) > workingpoint[2]: nBtagJets[0] += 1
                    for i in range(2):
                        if getattr(obj, 'fatjet1_CSV%d' % (i+1), -1) > workingpoint[1]: nBtagSubJets[0] += 1
                    
                    # Check JSON
                    if isJson_file and not isJSON(obj.run, obj.lumi):
                        if not 'XZh' in obj.GetName(): xsWeight[0] = 0.
                    # Filters
                    elif not (obj.Flag_BIT_Flag_HBHENoiseFilter and obj.Flag_BIT_Flag_HBHENoiseIsoFilter and obj.Flag_BIT_Flag_CSCTightHaloFilter and obj.Flag_BIT_Flag_goodVertices and obj.Flag_BIT_Flag_eeBadScFilter): xsWeight[0] = 0.
                    # Filter by PD
                    else:
                        xsWeight[0] = 1.
                        #den = 0
                        #if 'SingleMuon' in dir_name and obj.HLT_SingleMu: den +=1
                        #if 'SingleElectron' in dir_name and obj.HLT_SingleElectron: den +=1
                        #if 'MET' in dir_name and obj.HLT_MET: den +=1
                        #xsWeight[0] = 1./max(den, 1.)
                        #xsWeight[0] = 1./max(obj.HLT_SingleMu + obj.HLT_SingleElectron + obj.HLT_DoubleMu + obj.HLT_DoubleElectron + obj.HLT_MET, 1.)
                
                # Total
                eventWeight[0] = xsWeight[0] * kfactorWeight[0] * pileupWeight[0] * triggerMuonIsoWeight[0] * triggerElectronIsoWeight[0] * triggerMETWeight[0] * muonIsoWeight[0] * electronIsoWeight[0] * electroweakWeight[0]
                
                # Fill the branches
                eventWeightBranch.Fill()
                xsWeightBranch.Fill()
                sigxsWeightBranch.Fill()
                kfactorWeightBranch.Fill()
                kfactorWeightUpBranch.Fill()
                kfactorWeightDownBranch.Fill()
                electroweakWeightBranch.Fill()
                pileupWeightBranch.Fill()
                pileupWeightUpBranch.Fill()
                pileupWeightDownBranch.Fill()
                triggerMuonWeightBranch.Fill()
                triggerMuonWeightUpBranch.Fill()
                triggerMuonWeightDownBranch.Fill()
                triggerMuonIsoWeightBranch.Fill()
                triggerMuonIsoWeightUpBranch.Fill()
                triggerMuonIsoWeightDownBranch.Fill()
                triggerElectronWeightBranch.Fill()
                triggerElectronWeightUpBranch.Fill()
                triggerElectronWeightDownBranch.Fill()
                triggerElectronIsoWeightBranch.Fill()
                triggerElectronIsoWeightUpBranch.Fill()
                triggerElectronIsoWeightDownBranch.Fill()
                triggerMETWeightBranch.Fill()
                triggerMETWeightUpBranch.Fill()
                triggerMETWeightDownBranch.Fill()
                electronWeightBranch.Fill()
                electronWeightUpBranch.Fill()
                electronWeightDownBranch.Fill()
                electronIsoWeightBranch.Fill()
                electronIsoWeightUpBranch.Fill()
                electronIsoWeightDownBranch.Fill()
                muonWeightBranch.Fill()
                muonWeightUpBranch.Fill()
                muonWeightDownBranch.Fill()
                muonIsoWeightBranch.Fill()
                muonIsoWeightUpBranch.Fill()
                muonIsoWeightDownBranch.Fill()
                btagWeightBranch.Fill()
                btagWeightUpBranch.Fill()
                btagWeightDownBranch.Fill()
                nBtagJetsBranch.Fill()
                for i in range(njets+nbjets):
                    CSVBranch[i].Fill()
                    CSVUpBranch[i].Fill()
                    CSVDownBranch[i].Fill()
                for i in range(2):
                    subjetCSVBranch[i].Fill()
                    subjetCSVUpBranch[i].Fill()
                    subjetCSVDownBranch[i].Fill()
                nBtagSubJetsBranch.Fill()
                cormet_ptBranch.Fill()
                cormet_phiBranch.Fill()
                cormet_ptScaleUpBranch.Fill()
                cormet_ptScaleDownBranch.Fill()
                cormet_ptResUpBranch.Fill()
                cormet_ptResDownBranch.Fill()
                if obj.GetName()=='ZCR' or obj.GetName()=='WCR' or obj.GetName()=='TCR':
                    fakecormet_ptBranch.Fill()
                    fakecormet_phiBranch.Fill()
                    fakecormet_ptScaleUpBranch.Fill()
                    fakecormet_ptScaleDownBranch.Fill()
                    fakecormet_ptResUpBranch.Fill()
                    fakecormet_ptResDownBranch.Fill()

            new_file.cd()
            new_tree.Write()
            if verbose: print ' '
        
        # Directories
        elif obj.IsFolder():
            subdir = obj.GetName()
            if verbose: print ' \ Directory', subdir, ':'
            new_file.mkdir(subdir)
            new_file.cd(subdir)
            for subkey in ref_file.GetDirectory(subdir).GetListOfKeys():
                subobj = subkey.ReadObj()
                if subobj.IsA().InheritsFrom('TH1'):
                    if verbose: print '   + TH1:', subobj.GetName()
                    if not 'Eff' in subdir:
                        subobj.Scale(weightXS)
                        subobj.SetBinContent(0, totalEntries)
                    new_file.cd(subdir)
                    subobj.Write()
            new_file.cd('..')
        
        else:
            if verbose: print '- Unknown object:', obj.GetName()
    new_file.Close() 



jobs = []
for d in os.listdir(origin):
    if d.startswith('.') or 'Chunk' in d:
        continue
    if not d[:-3] in xsections.keys():
        continue
    #if not ('DYJetsToNuNu_TuneCUETP8M1_13TeV-amcatnloFXFX' in d or '_HT-' in d): continue
    #if not ('_HT-' in d): continue
    #if not 'SingleMuon_Run2015C-05Oct2015' in d: continue
    #if not 'TTbarDM' in d and not 'BBbarDM' in d: continue
    if not 'ZprimeToZhToZlephbb_narrow_M-1000' in d: continue
    p = multiprocessing.Process(target=processFile, args=(d,verboseon,))
    jobs.append(p)
    p.start()
#    processFile(d, True)
    
#print '\nDone.'

