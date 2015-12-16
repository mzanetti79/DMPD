#! /usr/bin/env python

import os, multiprocessing, math
from array import array
from ROOT import TFile, TH1, TF1, TLorentzVector

import optparse
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input', action='store', type='string', dest='origin', default='')
parser.add_option('-o', '--output', action='store', type='string', dest='target', default='')
parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)

(options, args) = parser.parse_args()

origin      = options.origin
target      = options.target
verboseon   = options.verbose

cut = {
    "SR"  : "eventWeight!=0 && met_pt>200",
    "WCR" : "eventWeight!=0 && kW_pt>200 && fatjet1_pt>200",
    "ZCR" : "eventWeight!=0 && Z_pt>200 && Z_mass>70 && Z_mass<110 && fatjet1_pt>200",
    "TCR" : "eventWeight!=0",
    "XZh" : "eventWeight!=0",
}


if not os.path.exists(origin):
    print 'Origin directory', origin, 'does not exist, aborting...'
    exit()
if not os.path.exists(target):
    print 'Target directory', target,'does not exist, aborting...'
    exit()

##############################

def processFile(dir_name, verbose=False):
    
    #print '##################################################'
    print dir_name#, ':'
    #print '##################################################'
    
    isMC = not '2015' in dir_name
    
    # Unweighted input
    ref_file_name = origin + '/' + dir_name
    if not os.path.exists(ref_file_name): 
        print '  WARNING: file', ref_file_name, 'does not exist, continuing'
        return True
    
    # Weighted output
    new_file_name = target + '/' + dir_name
    if os.path.exists(new_file_name):
        print '  WARNING: weighted file exists, overwriting', new_file_name
        #return True
    
    new_file = TFile(new_file_name, 'RECREATE')
    new_file.cd()
    
    # Open old file
    ref_file = TFile(ref_file_name, 'READ')
    
    # Variables declaration
    eventWeightLumi = array('f', [1.0])  # global event weight with lumi
    
    # Looping over file content
    for key in ref_file.GetListOfKeys():
        obj = key.ReadObj()
        if obj.IsA().InheritsFrom('TTree'):
            nev = obj.GetEntriesFast()
            new_file.cd()
            new_tree = obj.CopyTree(cut[obj.GetName()])
            # New branches
            eventWeightLumiBranch = new_tree.Branch('eventWeightLumi', eventWeightLumi, 'eventWeightLumi/F')

            # looping over events
            for event in range(0, obj.GetEntries()):
                if verbose and (event%10000==0 or event==nev-1): print ' = TTree:', obj.GetName(), 'events:', nev, '\t', int(100*float(event+1)/float(nev)), '%\r',
                #print '.',#*int(20*float(event)/float(nev)),#printProgressBar(event, nev)
                obj.GetEntry(event)
                
                # Initialize
                eventWeightLumi[0] = obj.eventWeight
                
                # Weights
                if isMC: eventWeightLumi[0] *= 2110
                
                # Fill the branches
                eventWeightLumiBranch.Fill()

            new_file.cd()
            new_tree.Write()
            if verbose: print ' '
        
    new_file.Close() 



jobs = []
for d in os.listdir(origin):
    
#    print d
    p = multiprocessing.Process(target=processFile, args=(d,verboseon,))
    jobs.append(p)
    p.start()
    #exit()
    
#print '\nDone.'

