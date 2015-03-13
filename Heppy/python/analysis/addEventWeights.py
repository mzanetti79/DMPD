#! /usr/bin/env python


import os
from array import array
from ROOT import TFile, TH1D

from DMPD.Heppy.samples.Phys14.fileLists import samples

prod_version = 'Prod_v00/'
heppy_output_dir = '/lustre/cmsdata/DM/ntuples/'+prod_version

if not os.path.exists(heppy_output_dir+'weighted'):
    print 'output dir does not exist, creating it'
    os.makedirs(heppy_output_dir+'weighted')

for ref_file_name in samples.keys: 

    # Unweighted input
    ref_file_name_with_path = heppy_output_dir+ref_file_name+'/tree.root'
    if not os.path.exists(ref_file_name_with_path): 
        print 'WARNING:', ref_file_name_with_path, 'does not exist, continuing' 
        continue
    ref_file = TFile(ref_file_name_with_path)
    Counter = ref_file.Get('Counter') 
    totalEntries = hCounters.GetBinContent(1)
    
    # Weighted output
    new_file_name_with_path = heppy_output_dir+'weighted/'+ref_file_name+'.root'
    if os.path.exists(new_file_name_with_path):
        print new_file_name_with_path, 'exists, continuing' 
        continue
    new_file = TFile(new_file_name_with_path,'recreate')

    # looping over trees
    for tree_name in ['SR','ZCR','WCR','GCR']: 
        print tree_name
        tree = ref_file.Get(tree_name)
        newTree = tree.CloneTree(-1,'fast')

        # weight
        weight = array('f',[1.0]) 
        weightBranch = newTree.Branch('weight',weight,'weight/F') 

        # looping over events
        for event in range(0, tree.GetEntries()):
            if event%100000==0: print event 
            tree.GetEntry(event)
            # set the weight somehow
            #weight[0] = tree.xsec*tree.puWeight*muWeight[0]
            weight[0] = samples[ref_file_name]['xsec']/totalEntries 
            # fill the branch
            weightBranch.Fill()

        new_file.cd()
        newTree.Write()

    new_file.Close()



