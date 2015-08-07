#! /usr/bin/env python

import os
from array import array
from ROOT import TFile, TH1

#from DMPD.Heppy.samples.Phys14.fileLists import samples
from DMPD.Heppy.samples.Spring15.fileLists import mcsamples
from DMPD.Heppy.samples.Data.fileLists import datasamples
samples = datasamples.copy()
samples.update(mcsamples)

#heppy_output_dir = '/lustre/cmsdata/DM/ntuples/Prod_v03/'
heppy_output_dir = '/lustre/cmswork/zucchett/CMSSW_7_4_7/src/DMPD/Heppy/test/Batch/'


if not os.path.exists(heppy_output_dir+'weighted'):
    print 'Output dir does not exist, creating it'
    os.makedirs(heppy_output_dir+'weighted')

for ref_file_name in samples.keys():
    #print "##################################################"
    print "\n", ref_file_name.replace(heppy_output_dir, ''), ":"
    #print "##################################################"
    
    isMC = not '2015' in ref_file_name
    
    # Unweighted input
    ref_file_name_with_path = heppy_output_dir+ref_file_name+'/Loop/tree.root'
    if not os.path.exists(ref_file_name_with_path): 
        print "  WARNING: file", ref_file_name_with_path, "does not exist, continuing"
        continue
    
    # Weighted output
    new_file_name_with_path = heppy_output_dir+"weighted/"+ref_file_name+".root"
    if os.path.exists(new_file_name_with_path):
        print "  WARNING: weighted file exists, continuing"
        continue
    
    new_file = TFile(new_file_name_with_path, "RECREATE")
    new_file.cd()
    
    # Get event number
    ref_file = TFile(ref_file_name_with_path, "READ")
    ref_hist = ref_file.Get('Counter')
    totalEntries = ref_hist.GetBinContent(0)
    if isMC:
        weightXS = samples[ref_file_name]['xsec']/totalEntries
    else:
        weightXS = 1.
    
    # PU reweighting
    puFile = TFile("./PU.root", "READ")
    puData = puFile.Get("data")
    puMC = puFile.Get("mc")
    print "PU histogram entries: data", puData.GetEntries(), "MC", puMC.GetEntries()
    
    # Variables declaration
    eventWeight = array('f',[1.0])  # global event weight
    xsWeight  = array('f',[1.0])  # weight due to the MC sample cross section
    pileupWeight = array('f',[1.0])  # weight from PU reweighting
    
    
    # Looping over file content
    for key in ref_file.GetListOfKeys():
        obj = key.ReadObj()
        # Copy and rescale histograms
        if obj.IsA().InheritsFrom("TH1"):
            print "  TH1:", obj.GetName()
            new_file.cd()
            if "SR" in obj.GetName() or "CR" in obj.GetName():
                obj.Add(ref_hist)
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
            
            # looping over events
            for event in range(0, obj.GetEntries()):
                if event%1000==0 or event==nev-1: print "  TTree:", obj.GetName(), "events:", nev, "\t", int(100*float(event+1)/float(nev)), "%\r",
                #print ".",#*int(20*float(event)/float(nev)),#printProgressBar(event, nev)
                obj.GetEntry(event)
                
                if isMC:
                    # Cross section
                    xsWeight[0] = weightXS if obj.genWeight > 0. else -weightXS
                    # PU reweighting
                    nbin = puData.FindBin(obj.nPV)
                    if puMC.GetBinContent(nbin) > 0.:
                        pileupWeight[0] = puData.GetBinContent(nbin) / puMC.GetBinContent(nbin)
                    else:
                        pileupWeight[0] = 0.
                    # Total
                    eventWeight[0] = xsWeight[0] * pileupWeight[0]
                else:
                    eventWeight[0] = pileupWeight[0] = xsWeight[0] = 1.
                # Fill the branches
                eventWeightBranch.Fill()
                xsWeightBranch.Fill()
                pileupWeightBranch.Fill()
                
            new_file.cd()
            new_tree.Write()
            print " "
        else:
            print "- Unknown object or Directory:", obj.GetName()
    new_file.Close() 

