#! /usr/bin/env python

import os
from array import array
from ROOT import TFile, TH1

#from DMPD.Heppy.samples.Phys14.fileLists import samples
from DMPD.Heppy.samples.Spring15.fileLists import samples
#from DMPD.Heppy.samples.Data.fileLists import samples

#heppy_output_dir = '/lustre/cmsdata/DM/ntuples/Prod_v03/'
heppy_output_dir = '/lustre/cmswork/zucchett/CMSSW_7_4_7/src/DMPD/Heppy/test/Test/'


if not os.path.exists(heppy_output_dir+'weighted'):
    print 'Output dir does not exist, creating it'
    os.makedirs(heppy_output_dir+'weighted')

for ref_file_name in samples.keys():
    #print "##################################################"
    print "\n", ref_file_name.replace(heppy_output_dir, ''), ":"
    #print "##################################################"

    # Unweighted input
    ref_file_name_with_path = heppy_output_dir+ref_file_name+'/Loop/tree.root'
    if not os.path.exists(ref_file_name_with_path): 
        print "  WARNING: file does not exist, continuing"
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
    if '2015' in ref_file_name:
        weightXS = 1.
    else:
        weightXS = samples[ref_file_name]['xsec']/totalEntries 

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
            weight = array('f',[1.0])  # weight
            weightBranch = new_tree.Branch('weight',weight,'weight/F') 
            # looping over events
            for event in range(0, obj.GetEntries()):
                if event%1000==0 or event-1==nev: print "  TTree:", obj.GetName(), "events:", nev, "\t", int(100*float(event)/float(nev)), "%\r",
                #print ".",#*int(20*float(event)/float(nev)),#printProgressBar(event, nev)
                obj.GetEntry(event)
                weight[0] = weightXS
                weightBranch.Fill() # fill the branch
            new_file.cd()
            new_tree.Write()
            print " "
        else:
            print "- Unknown object or Directory:", obj.GetName()
    new_file.Close() 

