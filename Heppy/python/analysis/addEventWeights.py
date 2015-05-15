#! /usr/bin/env python

import os
from array import array
from ROOT import TFile, TH1

from DMPD.Heppy.samples.Phys14.fileLists import samples

#prod_version = 'QWERTY'
prod_version = 'Prod_v03/'
heppy_output_dir = '/lustre/cmsdata/DM/ntuples/'+prod_version

if not os.path.exists(heppy_output_dir+'weighted'):
    print 'Output dir does not exist, creating it'
    os.makedirs(heppy_output_dir+'weighted')

for ref_file_name in samples.keys():
    print "##################################################"
    print "Processing:", ref_file_name.replace(heppy_output_dir, '')
    print "##################################################"

    # Unweighted input
    ref_file_name_with_path = heppy_output_dir+ref_file_name+'/tree.root'
    if not os.path.exists(ref_file_name_with_path): 
        print "WARNING:", ref_file_name_with_path, "does not exist, continuing"
        continue
    
    # Weighted output
    new_file_name_with_path = heppy_output_dir+"weighted/"+ref_file_name+".root"
    if os.path.exists(new_file_name_with_path):
        print "WARNING:", new_file_name_with_path, 'exists, continuing' 
        continue
    new_file = TFile(new_file_name_with_path, "RECREATE")
    new_file.cd()
    
    # Get event number
    ref_file = TFile(ref_file_name_with_path, "READ")
    ref_hist = ref_file.Get('Counter')
    totalEntries = ref_hist.GetBinContent(0)
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
            new_file.cd()
            obj.Write()
        # Copy trees
        elif obj.IsA().InheritsFrom("TTree"):
            print "  TTree:", obj.GetName()
            new_file.cd()
            new_tree = obj.CloneTree(-1, 'fast')
            weight = array('f',[1.0])  # weight
            weightBranch = new_tree.Branch('weight',weight,'weight/F') 
            # looping over events
            for event in range(0, obj.GetEntries()):
                if event%100000==0: print event 
                obj.GetEntry(event)
                weight[0] = weightXS
                weightBranch.Fill() # fill the branch
            new_file.cd()
            new_tree.Write()
        else:
            print "  Unknown object:", obj.GetName()
    new_file.Close() 

