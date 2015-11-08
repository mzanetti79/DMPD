#! /usr/bin/env python

import os, multiprocessing
from array import array
from ROOT import TFile, TH1

#from DMPD.Heppy.samples.Phys14.fileLists import samples
#from DMPD.Heppy.samples.Spring15.fileLists import mcsamples
#from DMPD.Heppy.samples.Data.fileLists import datasamples
#samples = datasamples.copy()
#samples.update(mcsamples)
from DMPD.Heppy.samples.Spring15.xSections import xsections, kfactors

#ROOT.gROOT.SetBatch(1)

ref_kf_file = '%s/src/DMPD/Heppy/python/tools/Kfactors.root' % os.environ['CMSSW_BASE']
ref_pu_file = '%s/src/DMPD/Heppy/python/tools/PU/PU.root' % os.environ['CMSSW_BASE']
ref_btag_file = '%s/src/DMPD/Heppy/python/tools/BTAG/CSVv2.csv' % os.environ['CMSSW_BASE']
ref_csv_file = '%s/src/DMPD/Heppy/python/tools/BTAG/BTagShapes.root' % os.environ['CMSSW_BASE']
ref_recoilMC_file = '%s/src/DMPD/Heppy/python/tools/RECOIL/recoilfit_gjetsMC_Zu1_pf_v1.root' % os.environ['CMSSW_BASE']
ref_recoilData_file = '%s/src/DMPD/Heppy/python/tools/RECOIL/recoilfit_gjetsData_Zu1_pf_v1.root' % os.environ['CMSSW_BASE']

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input', action='store', type='string', dest='origin', default='')
parser.add_option('-o', '--output', action='store', type='string', dest='target', default='')
parser.add_option('-j', '--json', action='store', type='string', dest='json', default='')
parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)

(options, args) = parser.parse_args()

origin = options.origin
target = options.target
json_path = options.json
verboseon = options.verbose

numberOfJets = {'ZCR' : 3, 'WCR' : 4, 'TCR' : 3, 'SR': 3}

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
    if discr<0.001 or discr>1: return discr
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
    return y0 + (discr-x0)*((y1-y0)/(x1-x0))

##############################

### ADD RECOIL CORRECTIONS ###

ROOT.gROOT.ProcessLine('.L %s/src/DMPD/Heppy/python/tools/RECOIL/RecoilCorrector.hh+' % os.environ['CMSSW_BASE'])
Recoil = ROOT.RecoilCorrector(ref_recoilMC_file)
Recoil.addDataFile(ref_recoilData_file)
Recoil.addMCFile(ref_recoilMC_file)

##############################


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
    
    # Variables declaration
    eventWeight = array('f', [1.0])  # global event weight
    xsWeight = array('f', [1.0])  # weight due to the MC sample cross section
    kfactorWeight = array('f', [1.0])  # weight due to the MC sample cross section
    kfactorWeightUp = array('f', [1.0])
    kfactorWeightDown = array('f', [1.0])
    pileupWeight = array('f', [1.0])  # weight from PU reweighting
    pileupWeightUp = array('f', [1.0])
    pileupWeightDown = array('f', [1.0])
    # Lists of arrays do not work #@!
    CSV = {}
    CSVUp = {}
    CSVDown = {}
    for i in range(10):
        CSV[i] = array('f', [1.0])
        CSVUp[i] = array('f', [1.0])
        CSVDown[i] = array('f', [1.0])
    # Recoil Variables
    cormet_pt         = array('f', [0.0])  
    cormet_phi        = array('f', [0.0])  
    cormet_ptScaleUp  = array('f', [0.0])  
    cormet_ptScaleDown= array('f', [0.0])
    cormet_ptResUp    = array('f', [0.0])
    cormet_ptResDown  = array('f', [0.0])
    corfakemet_pt         = array('f', [0.0])  
    corfakemet_phi        = array('f', [0.0])  
    corfakemet_ptScaleUp  = array('f', [0.0])  
    corfakemet_ptScaleDown= array('f', [0.0])
    corfakemet_ptResUp    = array('f', [0.0])
    corfakemet_ptResDown  = array('f', [0.0])

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
            new_file.cd()
            new_tree = obj.CloneTree(-1, 'fast')
            # New branches
            eventWeightBranch = new_tree.Branch('eventWeight', eventWeight, 'eventWeight/F')
            xsWeightBranch = new_tree.Branch('xsWeight', xsWeight, 'xsWeight/F')
            kfactorWeightBranch = new_tree.Branch('kfactorWeight', kfactorWeight, 'kfactorWeight/F')
            kfactorWeightUpBranch = new_tree.Branch('kfactorWeightUp', kfactorWeightUp, 'kfactorWeightUp/F')
            kfactorWeightDownBranch = new_tree.Branch('kfactorWeightDown', kfactorWeightDown, 'kfactorWeightDown/F')
            pileupWeightBranch = new_tree.Branch('pileupWeight', pileupWeight, 'pileupWeight/F')
            pileupWeightUpBranch = new_tree.Branch('pileupWeightUp', pileupWeightUp, 'pileupWeightUp/F')
            pileupWeightDownBranch = new_tree.Branch('pileupWeightDown', pileupWeightDown, 'pileupWeightDown/F')
            CSVBranch = {}
            CSVUpBranch = {}
            CSVDownBranch = {}
            for i in range(njets):
                CSVBranch[i] = new_tree.Branch('jet%d_CSVR' % (i+1), CSV[i], 'jet%d_CSVR/F' % (i+1))
                CSVUpBranch[i] = new_tree.Branch('jet%d_CSVRUp' % (i+1), CSVUp[i], 'jet%d_CSVRUp/F' % (i+1))
                CSVDownBranch[i] = new_tree.Branch('jet%d_CSVRDown' % (i+1), CSVDown[i], 'jet%d_CSVRDown/F' % (i+1))
            
            cormet_ptBranch          = new_tree.Branch('cormet_pt',          cormet_pt,          'cormet_pt/F')
            cormet_phiBranch         = new_tree.Branch('cormet_phi',         cormet_phi,         'cormet_phi/F')
            cormet_ptScaleUpBranch   = new_tree.Branch('cormet_ptScaleUp',   cormet_ptScaleUp,   'cormet_ptScaleUp/F')
            cormet_ptScaleDownBranch = new_tree.Branch('cormet_ptScaleDown', cormet_ptScaleDown, 'cormet_ptScaleDown/F')
            cormet_ptResUpBranch     = new_tree.Branch('cormet_ptResUp',     cormet_ptResUp,     'cormet_ptResUp/F')
            cormet_ptResDownBranch   = new_tree.Branch('cormet_ptResDown',   cormet_ptResDown,   'cormet_ptResDown/F')
            corfakemet_ptBranch          = new_tree.Branch('corfakemet_pt',          corfakemet_pt,          'corfakemet_pt/F')
            corfakemet_phiBranch         = new_tree.Branch('corfakemet_phi',         corfakemet_phi,         'corfakemet_phi/F')
            corfakemet_ptScaleUpBranch   = new_tree.Branch('corfakemet_ptScaleUp',   corfakemet_ptScaleUp,   'corfakemet_ptScaleUp/F')
            corfakemet_ptScaleDownBranch = new_tree.Branch('corfakemet_ptScaleDown', corfakemet_ptScaleDown, 'corfakemet_ptScaleDown/F')
            corfakemet_ptResUpBranch     = new_tree.Branch('corfakemet_ptResUp',     corfakemet_ptResUp,     'corfakemet_ptResUp/F')
            corfakemet_ptResDownBranch   = new_tree.Branch('corfakemet_ptResDown',   corfakemet_ptResDown,   'corfakemet_ptResDown/F')

            # looping over events
            for event in range(0, obj.GetEntries()):
                if verbose and (event%10000==0 or event==nev-1): print ' = TTree:', obj.GetName(), 'events:', nev, '\t', int(100*float(event+1)/float(nev)), '%\r',
                #print '.',#*int(20*float(event)/float(nev)),#printProgressBar(event, nev)
                obj.GetEntry(event)
                
                # Initialize
                eventWeight[0] = xsWeight[0] = kfactorWeight[0] = kfactorWeightUp[0] = kfactorWeightDown[0] = pileupWeight[0] = pileupWeightUp[0] = pileupWeightDown[0] = 1.
                for i in range(njets):
                    csv = getattr(obj, 'jet%d_CSV' % (i+1), -999)
                    CSV[i][0] = CSVUp[i][0] = CSVDown[i][0] = csv
                
                # Weights
                if isMC:
                    # Cross section
                    xsWeight[0] = weightXS if obj.genWeight > 0. else -weightXS
                    
                    # K factors
                    #kfactorWeight[0] = kfactorXS
                    kfBin = max(zkf.GetXaxis().GetXmin(), min(zkf.FindBin(obj.genVpt), zkf.GetXaxis().GetXmax()))
                    if 'WJets' in dir_name and 'madgraph' in dir_name:
                        kfactorWeight[0] = wkf.GetBinContent(kfBin)
                        kfactorWeightUp[0] = wkf.GetBinContent(kfBin) + wkf.GetBinError(kfBin)
                        kfactorWeightDown[0] = wkf.GetBinContent(kfBin) - wkf.GetBinError(kfBin)
                    elif ('ZJets' in dir_name or 'DYJets' in dir_name) and 'madgraph' in dir_name:
                        kfactorWeight[0] = zkf.GetBinContent(kfBin)
                        kfactorWeightUp[0] = zkf.GetBinContent(kfBin) + zkf.GetBinError(kfBin)
                        kfactorWeightDown[0] = zkf.GetBinContent(kfBin) - zkf.GetBinError(kfBin)
                    
                    # PU reweighting
                    puBin = min(puRatio.FindBin(obj.nPU), puRatio.GetXaxis().GetXmax())
                    pileupWeight[0] = puRatio.GetBinContent(puBin)
                    pileupWeightUp[0] = puRatioUp.GetBinContent(puBin)
                    pileupWeightDown[0] = puRatioDown.GetBinContent(puBin)
                    
                    for i in range(njets):
                        pt = getattr(obj, 'jet%d_pt' % (i+1), -1)
                        eta = getattr(obj, 'jet%d_eta' % (i+1), -1)
                        flav = getattr(obj, 'jet%d_flavour' % (i+1), -1)
                        csv = getattr(obj, 'jet%d_CSV' % (i+1), -1)
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

                    applyrecoil    = True
                    nJets          = int(obj.nJets)
                    
                    # apply recoil corrections only for Z->ll, Z->vv, and W->lv
                    if 'DYJets' in dir_name or 'ZJets' in dir_name or 'WJets' in dir_name:
                        if obj.GetName()=='ZCR' or obj.GetName()=='WCR'or obj.GetName()=='SR':
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
                            else:
                                applyrecoil = False
                            
                            if applyrecoil:
                                ### do the MET recoil corrections in SR, ZCR and WCR, only for DYJets, ZJets and WJets samples
                                Recoil.CorrectType2(cmetpt,          cmetphi,          genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 0,nJets)        
                                Recoil.CorrectType2(cmetptScaleUp,   cmetphiScaleUp,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 1, 0,nJets)        
                                Recoil.CorrectType2(cmetptScaleDown, cmetphiScaleDown, genmetpt,genmetphi,leppt,lepphi,Upar,Uper,-1, 0,nJets)        
                                Recoil.CorrectType2(cmetptResUp,     cmetphiResUp,     genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 1,nJets)        
                                Recoil.CorrectType2(cmetptResDown,   cmetphiResDown,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0,-1,nJets)   
                                if obj.GetName()=='ZCR' or obj.GetName()=='WCR':
                                    ### correct fakeMET only in ZCR and WCR
                                    ### set reconstructed leptons and recoil to zero
                                    ### leave genmet set as standard. it is correct as it is always the genV pt
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
                                    genmetpt  = ROOT.Double(obj.genV_pt)
                                    genmetphi = ROOT.Double(obj.genV_phi)
                                    leppt     = ROOT.Double(0.)
                                    lepphi    = ROOT.Double(0.)
                                    Upar      = ROOT.Double(0.)
                                    Uper      = ROOT.Double(0.)
                                    Recoil.CorrectType2(cfmetpt,          cfmetphi,          genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 0,nJets)        
                                    Recoil.CorrectType2(cfmetptScaleUp,   cfmetphiScaleUp,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 1, 0,nJets)        
                                    Recoil.CorrectType2(cfmetptScaleDown, cfmetphiScaleDown, genmetpt,genmetphi,leppt,lepphi,Upar,Uper,-1, 0,nJets)        
                                    Recoil.CorrectType2(cfmetptResUp,     cfmetphiResUp,     genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 1,nJets)        
                                    Recoil.CorrectType2(cfmetptResDown,   cfmetphiResDown,   genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0,-1,nJets)   
                                pass
                            pass
                        pass
                    pass
                    
                    # fill the variables 
                    cormet_pt[0]         = cmetpt
                    cormet_phi[0]        = cmetphi
                    cormet_ptScaleUp[0]  = cmetptScaleUp
                    cormet_ptScaleDown[0]= cmetptScaleDown
                    cormet_ptResUp[0]    = cmetptResUp
                    cormet_ptResDown[0]  = cmetptResDown
                    if obj.GetName()=='ZCR' or obj.GetName()=='WCR':
                        corfakemet_pt[0]         = cfmetpt
                        corfakemet_phi[0]        = cfmetphi
                        corfakemet_ptScaleUp[0]  = cfmetptScaleUp
                        corfakemet_ptScaleDown[0]= cfmetptScaleDown
                        corfakemet_ptResUp[0]    = cfmetptResUp
                        corfakemet_ptResDown[0]  = cfmetptResDown               
                # Data
                else:
                    cormet_pt[0]         = obj.met_pt
                    cormet_phi[0]        = obj.met_phi
                    cormet_ptScaleUp[0]  = obj.met_pt
                    cormet_ptScaleDown[0]= obj.met_pt
                    cormet_ptResUp[0]    = obj.met_pt
                    cormet_ptResDown[0]  = obj.met_pt
                    if obj.GetName()=='ZCR' or obj.GetName()=='WCR':
                        corfakemet_pt[0]         = obj.met_pt
                        corfakemet_phi[0]        = obj.met_phi
                        corfakemet_ptScaleUp[0]  = obj.met_pt
                        corfakemet_ptScaleDown[0]= obj.met_pt
                        corfakemet_ptResUp[0]    = obj.met_pt
                        corfakemet_ptResDown[0]  = obj.met_pt               

                    # Check JSON
                    if isJson_file and not isJSON(obj.run, obj.lumi): xsWeight[0] = 0.
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
                eventWeight[0] = xsWeight[0] * pileupWeight[0]
                
                # Fill the branches
                eventWeightBranch.Fill()
                xsWeightBranch.Fill()
                kfactorWeightBranch.Fill()
                kfactorWeightUpBranch.Fill()
                kfactorWeightDownBranch.Fill()
                pileupWeightBranch.Fill()
                pileupWeightUpBranch.Fill()
                pileupWeightDownBranch.Fill()
                for i in range(njets):
                    CSVBranch[i].Fill()
                    CSVUpBranch[i].Fill()
                    CSVDownBranch[i].Fill()
                cormet_ptBranch.Fill()
                cormet_phiBranch.Fill()
                cormet_ptScaleUpBranch.Fill()
                cormet_ptScaleDownBranch.Fill()
                cormet_ptResUpBranch.Fill()
                cormet_ptResDownBranch.Fill()
                if obj.GetName()=='ZCR' or obj.GetName()=='WCR':
                    corfakemet_ptBranch.Fill()
                    corfakemet_phiBranch.Fill()
                    corfakemet_ptScaleUpBranch.Fill()
                    corfakemet_ptScaleDownBranch.Fill()
                    corfakemet_ptResUpBranch.Fill()
                    corfakemet_ptResDownBranch.Fill()

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
    p = multiprocessing.Process(target=processFile, args=(d,verboseon,))
    jobs.append(p)
    p.start()
#    processFile(d, True)
    
#print '\nDone.'

