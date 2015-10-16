#! /usr/bin/env python

import os, multiprocessing
from array import array
from ROOT import TFile, TH1

#from DMPD.Heppy.samples.Phys14.fileLists import samples
from DMPD.Heppy.samples.Spring15.fileLists import mcsamples
from DMPD.Heppy.samples.Data.fileLists import datasamples
samples = datasamples.copy()
samples.update(mcsamples)

ref_pu_file = "%s/src/DMPD/Heppy/python/tools/PU.root" % os.environ['CMSSW_BASE']
ref_v_file = "%s/src/DMPD/Heppy/python/tools/Vpt.root" % os.environ['CMSSW_BASE']

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-i", "--input", action="store", type="string", dest="origin", default="")
parser.add_option("-o", "--output", action="store", type="string", dest="target", default="")
parser.add_option("-j", "--json", action="store", type="string", dest="json", default="")

(options, args) = parser.parse_args()

origin = options.origin
target = options.target
json_path = options.json

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



def isJSON(run, lumi):
    runstr = "%d" % run
    if not runstr in json_data:
        return False
    else:
        if any(l <= lumi <= u for [l, u] in json_data[runstr]):
            return True
    return False


def applyKfactor(name):
    if 'DYJets' in name or 'ZJets' in name:
        if 'HT100to200' in name: return 1.5992641737053377
        elif 'HT200to400' in name: return 1.388778036943685
        elif 'HT400to600' in name: return 1.5360789955333298
        elif 'HT600toInf' in name: return 1.1347900247061118
        else: return 1.
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
    
    # V reweighting
    vFile = TFile(ref_v_file, "READ")
    vRatio = vFile.Get("ratio")
    if verbose: print "V histogram entries: ", vRatio.GetEntries()
    
    enableVreweighting = False #('ZJetsToNuNu' in dir_name or 'DYJetsToLL' in dir_name) and 'madgraph' in dir_name
    
    # Variables declaration
    eventWeight = array('f', [1.0])  # global event weight
    xsWeight  = array('f', [1.0])  # weight due to the MC sample cross section
    pileupWeight = array('f', [1.0])  # weight from PU reweighting
    pileupWeightUp = array('f', [1.0])
    pileupWeightDown = array('f', [1.0])
    ptWeight = array('f', [1.0])  # weight from V pt reweighting
    ptWeightUp = array('f', [1.0])
    ptWeightDown = array('f', [1.0])
    
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
            new_file.cd()
            new_tree = obj.CloneTree(-1, 'fast')
            # New branches
            eventWeightBranch = new_tree.Branch('eventWeight', eventWeight, 'eventWeight/F')
            xsWeightBranch = new_tree.Branch('xsWeight', xsWeight, 'xsWeight/F')
            pileupWeightBranch = new_tree.Branch('pileupWeight', pileupWeight, 'pileupWeight/F')
            pileupWeightUpBranch = new_tree.Branch('pileupWeightUp', pileupWeightUp, 'pileupWeightUp/F')
            pileupWeightDownBranch = new_tree.Branch('pileupWeightDown', pileupWeightDown, 'pileupWeightDown/F')
            ptWeightBranch = new_tree.Branch('ptWeight', ptWeight, 'ptWeight/F')
            ptWeightUpBranch = new_tree.Branch('ptWeightUp', ptWeightUp, 'ptWeightUp/F')
            ptWeightDownBranch = new_tree.Branch('ptWeightDown', ptWeightDown, 'ptWeightDown/F')
            
            # looping over events
            for event in range(0, obj.GetEntries()):
                if verbose and (event%10000==0 or event==nev-1): print " = TTree:", obj.GetName(), "events:", nev, "\t", int(100*float(event+1)/float(nev)), "%\r",
                #print ".",#*int(20*float(event)/float(nev)),#printProgressBar(event, nev)
                obj.GetEntry(event)
                
                # Initialize
                eventWeight[0] = xsWeight[0] = pileupWeight[0] = pileupWeightUp[0] = pileupWeightDown[0] = ptWeight[0] = ptWeightUp[0] = ptWeightDown[0] = 1.
                
                # Weights
                if isMC:
                    # Cross section
                    xsWeight[0] = weightXS if obj.genWeight > 0. else -weightXS
                    # PU reweighting
                    #nbin = puData.FindBin(obj.nPV)
                    #pileupWeight[0] = puData.GetBinContent(nbin) / puMC.GetBinContent(nbin) if puMC.GetBinContent(nbin) > 0. else 0.
                    pileupWeight[0] = puRatio.GetBinContent(puRatio.FindBin(obj.nPV) )#if obj.nPV < puRatio.GetXaxis().GetMax() else puRatio.GetNbinsX())
                    pileupWeightUp[0] = pileupWeightDown[0] = pileupWeight[0]
                    # V boson pT reweight
                    if enableVreweighting:
                        vbin = vRatio.FindBin(obj.genVpt) #if obj.genVpt < vRatio.GetXaxis().GetMax() else vRatio.GetNbinsX()
                        ptWeight[0] = vRatio.GetBinContent(vbin)
                        ptWeightUp[0] = vRatio.GetBinContent(vbin)+vRatio.GetBinError(vbin)
                        ptWeightDown[0] = vRatio.GetBinContent(vbin)-vRatio.GetBinError(vbin)
                        
                # Data
                else:
                    # Check JSON
                    if isJson_file and not isJSON(obj.run, obj.lumi): xsWeight[0] = 0.
                    # Filters
                    #elif not (obj.Flag_BIT_Flag_CSCTightHaloFilter and obj.Flag_BIT_Flag_goodVertices and obj.Flag_BIT_Flag_eeBadScFilter): xsWeight[0] = 0. #obj.Flag_BIT_Flag_HBHENoiseFilter and 
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
                ptWeightBranch.Fill()
                ptWeightUpBranch.Fill()
                ptWeightDownBranch.Fill()
                
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
    p = multiprocessing.Process(target=processFile, args=(d,False,))
    jobs.append(p)
    p.start()
#    processFile(d, True)
    
#print "\nDone."

