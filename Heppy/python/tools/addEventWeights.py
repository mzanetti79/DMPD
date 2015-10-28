#! /usr/bin/env python

import os, multiprocessing
from array import array
from ROOT import TFile, TH1

#from DMPD.Heppy.samples.Phys14.fileLists import samples
from DMPD.Heppy.samples.Spring15.fileLists import mcsamples
from DMPD.Heppy.samples.Data.fileLists import datasamples
samples = datasamples.copy()
samples.update(mcsamples)

#ROOT.gROOT.SetBatch(1)

ref_pu_file = "%s/src/DMPD/Heppy/python/tools/PU.root" % os.environ['CMSSW_BASE']
ref_btag_file = "%s/src/DMPD/Heppy/python/tools/BTAG/CSVv2.csv" % os.environ['CMSSW_BASE']
ref_csv_file = "%s/src/DMPD/Heppy/python/tools/BTAG/BTagShapes.root" % os.environ['CMSSW_BASE']
ref_recoilMC_file = "%s/src/DMPD/Heppy/python/tools/RECOIL/recoilfit_gjetsMC_Zu1_pf_v1.root" % os.environ['CMSSW_BASE']
ref_recoilData_file = "%s/src/DMPD/Heppy/python/tools/RECOIL/recoilfit_gjetsData_Zu1_pf_v1.root" % os.environ['CMSSW_BASE']

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-i", "--input", action="store", type="string", dest="origin", default="")
parser.add_option("-o", "--output", action="store", type="string", dest="target", default="")
parser.add_option("-j", "--json", action="store", type="string", dest="json", default="")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)

(options, args) = parser.parse_args()

origin = options.origin
target = options.target
json_path = options.json
verboseon = options.verbose

numberOfJets = {"ZCR" : 3, "WCR" : 4, "TCR" : 3, "SR": 3}

import json

if len(json_path) <= 0 or not os.path.exists(json_path):
    print "  WARNING, no JSON file (-j option) has been specified"#. Press Enter to continue"
    #raw_input()
    isJson_file = False
else:
    with open(json_path) as json_file:    
        json_data = json.load(json_file)
    isJson_file = True

if not os.path.exists(origin):
    print "Origin directory", origin, "does not exist, aborting..."
    exit()
if not os.path.exists(target):
    print "Target directory", target,"does not exist, aborting..."
    exit()

##############################

### Btagging setup ###

import ROOT
# from within CMSSW:
ROOT.gSystem.Load('libCondFormatsBTagObjects')
# OR using standalone code:
ROOT.gROOT.ProcessLine('.L %s/src/DMPD/Heppy/python/tools/BTAG/BTagCalibrationStandalone.cc+' % os.environ['CMSSW_BASE'])

fl = ["B", "C", "L"]
wp = ["L", "M", "T"]
workingpoint = [0., 0.605, 0.890, 0.980, 1.]
shape = {}

calib = ROOT.BTagCalibration("csvv2", ref_btag_file)
reader = {}
for i, w in enumerate(wp):
    reader[w] = {}
    reader[w][0] = ROOT.BTagCalibrationReader(calib, i, "comb", "central")
    reader[w][1] = ROOT.BTagCalibrationReader(calib, i, "comb", "up")
    reader[w][-1] = ROOT.BTagCalibrationReader(calib, i, "comb", "down")


shFile = TFile(ref_csv_file, "READ")
shFile.cd()
if not shFile.IsZombie():
    for i, f in enumerate(fl):
        shape[f] = shFile.Get("j_bTagDiscr"+f)
else: print " - BTagWeight Error: No Shape File"

for i, f in enumerate(fl):
    #shape[f].Smooth(100)
    shape[f].Rebin(10)
    shape[f].Scale(1./shape[f].Integral())


def returnNewWorkingPoint(f, p, pt, eta, sigma):
    if f<0 or f>2: print " - BTagWeight Error: unrecognized flavour", f
    if p<0 or p>4: print " - BTagWeight Error: working point", p, "not defined"
    if p==0 or p==4: return workingpoint[p]
    
    integral = shape[fl[f]].Integral(shape[fl[f]].FindBin(workingpoint[p]), shape[fl[f]].GetNbinsX()+1)
    
    sf = reader[wp[p-1]][sigma].eval(f, eta, pt)
    if sf == 0: return workingpoint[p]
    integral /= sf
    
    n = shape[fl[f]].GetNbinsX()+1
    step = 10
    for i in list(reversed(range(0, n, step))):
        if shape[fl[f]].Integral(i-step, n) >= integral:
            for j in list(reversed(range(0, i, step/10))):
                if shape[fl[f]].Integral(j-step/10, n) >= integral:
                    return (j-0.5*step/10)/(n-1)

    return workingpoint[p]


def returnReshapedDiscr(f, discr, pt, eta, sigma=""):
    if discr<0.01 or discr>0.99: return discr
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
    runstr = "%d" % run
    if not runstr in json_data:
        return False
    else:
        if any(l <= lumi <= u for [l, u] in json_data[runstr]):
            return True
    return False


def applyKfactor(name):
    if 'madgraph' in name and ('DYJets' in name or 'ZJets' in name):
        if 'HT100to200' in name: return 1.5992641737053377
        elif 'HT200to400' in name: return 1.388778036943685
        elif 'HT400to600' in name: return 1.5360789955333298
        elif 'HT600toInf' in name: return 1.1347900247061118
        else: return 1.
    elif 'madgraph' in name and 'WJets' in name:
        return 1.21
    else:
        return 1.

def processFile(dir_name, verbose=False):
    
    #print "##################################################"
    print dir_name#, ":"
    #print "##################################################"
    
    isMC = not '2015' in dir_name
    
    # Unweighted input
    ref_file_name = origin + "/" + dir_name + "/Loop/tree.root"
    if not os.path.exists(ref_file_name): 
        print "  WARNING: file", ref_file_name, "does not exist, continuing"
        return True
    
    # Weighted output
    new_file_name = target + "/" + dir_name + ".root"
    if os.path.exists(new_file_name):
        print "  WARNING: weighted file exists, overwriting", new_file_name
        #return True
    
    new_file = TFile(new_file_name, "RECREATE")
    new_file.cd()
    
    # Get event number
    ref_file = TFile(ref_file_name, "READ")
    ref_hist = ref_file.Get('Counters/Counter')
    totalEntries = ref_hist.GetBinContent(0)
    if isMC:
        weightXS = samples[dir_name]['xsec']/totalEntries
        weightXS *= applyKfactor(dir_name)
    else:
        weightXS = 1.
    
    # PU reweighting
    puFile = TFile(ref_pu_file, "READ")
    puData = puFile.Get("data")
    puMC = puFile.Get("mc")
    puRatio = puFile.Get("ratio")
    if verbose: print "PU histogram entries: ", puRatio.GetEntries()
    
    # Variables declaration
    eventWeight = array('f', [1.0])  # global event weight
    xsWeight  = array('f', [1.0])  # weight due to the MC sample cross section
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
    corrmet_pt         = array('f', [0.0])  
    corrmet_phi        = array('f', [0.0])  
    corrmet_pt_scaleH  = array('f', [0.0])  
    corrmet_phi_scaleH = array('f', [0.0])
    corrmet_pt_scaleL  = array('f', [0.0])
    corrmet_phi_scaleL = array('f', [0.0])  
    corrmet_pt_resH    = array('f', [0.0])
    corrmet_phi_resH   = array('f', [0.0])
    corrmet_pt_resL    = array('f', [0.0])
    corrmet_phi_resL   = array('f', [0.0])   
    
    # Looping over file content
    for key in ref_file.GetListOfKeys():
        obj = key.ReadObj()
          
        # Copy and rescale histograms
        if obj.IsA().InheritsFrom("TH1"):
            if verbose: print " + TH1:", obj.GetName()
            new_file.cd()
            #if "SR" in obj.GetName() or "CR" in obj.GetName():
            #    obj.Add(ref_hist)
            if "Counter" in obj.GetName():
                obj.Scale(weightXS)
            obj.SetBinContent(0, totalEntries)
            new_file.cd()
            obj.Write()
        
        # Copy trees
        elif obj.IsA().InheritsFrom("TTree"):
            nev = obj.GetEntriesFast()
            njets = numberOfJets[obj.GetName()] if obj.GetName() in numberOfJets else 0 #FIXME
            new_file.cd()
            new_tree = obj.CloneTree(-1, 'fast')
            # New branches
            eventWeightBranch = new_tree.Branch('eventWeight', eventWeight, 'eventWeight/F')
            xsWeightBranch = new_tree.Branch('xsWeight', xsWeight, 'xsWeight/F')
            pileupWeightBranch = new_tree.Branch('pileupWeight', pileupWeight, 'pileupWeight/F')
            pileupWeightUpBranch = new_tree.Branch('pileupWeightUp', pileupWeightUp, 'pileupWeightUp/F')
            pileupWeightDownBranch = new_tree.Branch('pileupWeightDown', pileupWeightDown, 'pileupWeightDown/F')
            CSVBranch = {}
            CSVUpBranch = {}
            CSVDownBranch = {}
            for i in range(njets):
                CSVBranch[i] = new_tree.Branch('jet%d_CSVWeight' % (i+1), CSV[i], 'jet%d_rCSV/F' % (i+1))
                CSVUpBranch[i] = new_tree.Branch('jet%d_CSVWeightUp' % (i+1), CSVUp[i], 'jet%d_rCSVUp/F' % (i+1))
                CSVDownBranch[i] = new_tree.Branch('jet%d_CSVWeightDown' % (i+1), CSVDown[i], 'jet%d_rCSVDown/F' % (i+1))
            
            corrmet_ptBranch        = new_tree.Branch('corrmet_pt',        corrmet_pt,        'corrmet_pt/F')
            corrmet_phiBranch       = new_tree.Branch('corrmet_phi',       corrmet_phi,       'corrmet_phi/F')
            corrmet_pt_scaleHBranch = new_tree.Branch('corrmet_pt_scaleH', corrmet_pt_scaleH, 'corrmet_pt_scaleH/F')
            corrmet_phi_scaleHBranch= new_tree.Branch('corrmet_phi_scaleH',corrmet_phi_scaleH,'corrmet_phi_scaleH/F')
            corrmet_pt_scaleLBranch = new_tree.Branch('corrmet_pt_scaleL', corrmet_pt_scaleL, 'corrmet_pt_scaleL/F')
            corrmet_pt_resHBranch   = new_tree.Branch('corrmet_pt_resH',   corrmet_pt_resH,   'corrmet_pt_resH/F')
            corrmet_phi_resHBranch  = new_tree.Branch('corrmet_phi_resH',  corrmet_phi_resH,  'corrmet_phi_resH/F')
            corrmet_pt_resLBranch   = new_tree.Branch('corrmet_pt_resL',   corrmet_pt_resL,   'corrmet_pt_resL/F')
            corrmet_phi_resLBranch  = new_tree.Branch('corrmet_phi_resL',  corrmet_phi_resL,  'corrmet_pt_resL/F')
            
            # looping over events
            for event in range(0, obj.GetEntries()):
                if verbose and (event%10000==0 or event==nev-1): print " = TTree:", obj.GetName(), "events:", nev, "\t", int(100*float(event+1)/float(nev)), "%\r",
                #print ".",#*int(20*float(event)/float(nev)),#printProgressBar(event, nev)
                obj.GetEntry(event)
                
                # Initialize
                eventWeight[0] = xsWeight[0] = pileupWeight[0] = pileupWeightUp[0] = pileupWeightDown[0] = 1.
                for i in range(njets):
                    csv = getattr(obj, "jet%d_CSV" % (i+1), -999)
                    CSV[i][0] = CSVUp[i][0] = CSVDown[i][0] = csv
                
                # Weights
                if isMC:
                    # Cross section
                    xsWeight[0] = weightXS if obj.genWeight > 0. else -weightXS
                    # PU reweighting
                    #nbin = puData.FindBin(obj.nPV)
                    #pileupWeight[0] = puData.GetBinContent(nbin) / puMC.GetBinContent(nbin) if puMC.GetBinContent(nbin) > 0. else 0.
                    pileupWeight[0] = puRatio.GetBinContent(puRatio.FindBin(obj.nPV) )#if obj.nPV < puRatio.GetXaxis().GetMax() else puRatio.GetNbinsX())
                    pileupWeightUp[0] = pileupWeightDown[0] = pileupWeight[0]
                    
                    for i in range(njets):
                        pt = getattr(obj, "jet%d_pt" % (i+1), -1)
                        eta = getattr(obj, "jet%d_eta" % (i+1), -1)
                        flav = getattr(obj, "jet%d_flavour" % (i+1), -1)
                        csv = getattr(obj, "jet%d_CSV" % (i+1), -1)
                        pt = min(pt, 669)
                        if abs(flav) == 5: fl = 0
                        elif abs(flav) == 4: fl = 1
                        else: fl = 2
                        CSV[i][0] = reader["M"][0].eval(fl, eta, pt)
                        CSVUp[i][0] = reader["M"][1].eval(fl, eta, pt)
                        CSVDown[i][0] = reader["M"][-1].eval(fl, eta, pt)
                        CSV[i][0] = returnReshapedDiscr(fl, csv, pt, eta, 0)
                        CSVUp[i][0] = returnReshapedDiscr(fl, csv, pt, eta, +1)
                        CSVDown[i][0] = returnReshapedDiscr(fl, csv, pt, eta, -1)
                    
                    cmetpt         = ROOT.Double(obj.met_pt)
                    cmetphi        = ROOT.Double(obj.met_phi)
                    cmetpt_scaleH  = ROOT.Double(obj.met_pt)
                    cmetphi_scaleH = ROOT.Double(obj.met_phi)
                    cmetpt_scaleL  = ROOT.Double(obj.met_pt)
                    cmetphi_scaleL = ROOT.Double(obj.met_phi)
                    cmetpt_resH    = ROOT.Double(obj.met_pt)
                    cmetphi_resH   = ROOT.Double(obj.met_phi)
                    cmetpt_resL    = ROOT.Double(obj.met_pt)
                    cmetphi_resL   = ROOT.Double(obj.met_phi)
                    applyrecoil    = True
                    nJets          = int(obj.nJets)
                    # apply recoil corrections only for Z->ll, Z->vv, and W->lv
                    if 'DYJets' in dir_name or 'ZJets' in dir_name or 'WJets' in dir_name:
                        if 'SR' in obj.GetName():
                            genmetpt  = ROOT.Double(obj.genV_pt)
                            genmetphi = ROOT.Double(obj.genV_phi)
                            leppt     = ROOT.Double(0)
                            lepphi    = ROOT.Double(0)
                            Upar      = ROOT.Double(0)
                            Uper      = ROOT.Double(0)
                        elif 'ZCR' in obj.GetName():
                            genmetpt  = ROOT.Double(obj.genV_pt)
                            genmetphi = ROOT.Double(obj.genV_phi)
                            leppt     = ROOT.Double(obj.Z_pt)
                            lepphi    = ROOT.Double(obj.Z_phi)
                            Upar      = ROOT.Double(obj.Upara)
                            Uper      = ROOT.Double(obj.Uperp)
                        elif 'WCR' in obj.GetName():
                            genmetpt  = ROOT.Double(obj.genV_pt)
                            genmetphi = ROOT.Double(obj.genV_phi)
                            leppt     = ROOT.Double(obj.lepton1_pt)
                            lepphi    = ROOT.Double(obj.lepton1_phi)
                            Upar      = ROOT.Double(obj.Upara)
                            Uper      = ROOT.Double(obj.Uperp)
                    # otherwise only copy the met in all the corrmet_ variables
                    else:
                        applyrecoil = False
                        
                    if applyrecoil:
                        Recoil.CorrectType2(cmetpt       ,cmetphi       ,genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 0,nJets)        
                        Recoil.CorrectType2(cmetpt_scaleH,cmetphi_scaleH,genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 1, 0,nJets)        
                        Recoil.CorrectType2(cmetpt_scaleL,cmetphi_scaleL,genmetpt,genmetphi,leppt,lepphi,Upar,Uper,-1, 0,nJets)        
                        Recoil.CorrectType2(cmetpt_resH  ,cmetphi_resH  ,genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0, 1,nJets)        
                        Recoil.CorrectType2(cmetpt_resL  ,cmetphi_resL  ,genmetpt,genmetphi,leppt,lepphi,Upar,Uper, 0,-1,nJets)        
                    corrmet_pt[0]         = cmetpt
                    corrmet_phi[0]        = cmetphi
                    corrmet_pt_scaleH[0]  = cmetpt_scaleH
                    corrmet_phi_scaleH[0] = cmetphi_scaleH
                    corrmet_pt_scaleL[0]  = cmetpt_scaleL
                    corrmet_phi_scaleL[0] = cmetphi_scaleL
                    corrmet_pt_resH[0]    = cmetpt_resH
                    corrmet_phi_resH[0]   = cmetphi_resH
                    corrmet_pt_resL[0]    = cmetpt_resL
                    corrmet_phi_resL[0]   = cmetphi_resL
                
                # Data
                else:
                    # Check JSON
                    if isJson_file and not isJSON(obj.run, obj.lumi): xsWeight[0] = 0.
                    # Filters
                    elif not (obj.Flag_BIT_Flag_HBHENoiseFilter and obj.Flag_BIT_Flag_CSCTightHaloFilter and obj.Flag_BIT_Flag_goodVertices and obj.Flag_BIT_Flag_eeBadScFilter): xsWeight[0] = 0.
                    # Filter by PD
                    else: xsWeight[0] = 1.
                        #xsWeight[0] = 1./max(obj.HLT_SingleMu + obj.HLT_SingleElectron + obj.HLT_DoubleMu + obj.HLT_DoubleElectron + obj.HLT_MET, 1.)
                
                # Total
                eventWeight[0] = xsWeight[0] * pileupWeight[0]
                
                # Fill the branches
                eventWeightBranch.Fill()
                xsWeightBranch.Fill()
                pileupWeightBranch.Fill()
                pileupWeightUpBranch.Fill()
                pileupWeightDownBranch.Fill()
                for i in range(njets):
                    CSVBranch[i].Fill()
                    CSVUpBranch[i].Fill()
                    CSVDownBranch[i].Fill()
                corrmet_ptBranch.Fill()
                corrmet_phiBranch.Fill()
                corrmet_pt_scaleHBranch.Fill()
                corrmet_phi_scaleHBranch.Fill()
                corrmet_pt_scaleLBranch.Fill()
                corrmet_pt_resHBranch.Fill()
                corrmet_phi_resHBranch.Fill()
                corrmet_pt_resLBranch.Fill()

            new_file.cd()
            new_tree.Write()
            if verbose: print " "
        
        # Directories
        elif obj.IsFolder():
            subdir = obj.GetName()
            if verbose: print " \ Directory", subdir, ":"
            new_file.mkdir(subdir)
            new_file.cd(subdir)
            for subkey in ref_file.GetDirectory(subdir).GetListOfKeys():
                subobj = subkey.ReadObj()
                if subobj.IsA().InheritsFrom("TH1"):
                    if verbose: print "   + TH1:", subobj.GetName()
                    if not 'Eff' in subdir:
                        subobj.Scale(weightXS)
                        subobj.SetBinContent(0, totalEntries)
                    new_file.cd(subdir)
                    subobj.Write()
            new_file.cd("..")
        
        else:
            if verbose: print "- Unknown object:", obj.GetName()
    new_file.Close() 



jobs = []
for d in os.listdir(origin):
    if d.startswith('.') or 'Chunk' in d:
        continue
    if not d in samples:
        continue
    p = multiprocessing.Process(target=processFile, args=(d,verboseon,))
    jobs.append(p)
    p.start()
#    processFile(d, True)
    
#print "\nDone."

