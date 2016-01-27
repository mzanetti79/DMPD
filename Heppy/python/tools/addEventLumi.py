#! /usr/bin/env python

import os, multiprocessing, math
from array import array
from ROOT import TFile, TH1, TF1, TLorentzVector

from DMPD.Heppy.tools.selections import *

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

#LUMI        = 2110

cut = {
    "SR"  : "eventWeight!=0 && (" + selection['XZhnnPre'] + ")",
    "WCR" : "eventWeight!=0 && ((" + selection['XWhenPre'] + ") || (" + selection['XWhmnPre'] + "))",
    "ZCR" : "0!=0",
    "TCR" : "0!=0",
    "XZh" : "eventWeight!=0 && ((" + selection['XZheePre'] + ") || (" + selection['XZhmmPre'] + "))",
}
for r, sel in cut.iteritems():
    for n, c in selection.iteritems():
        if n in sel: cut[r] = cut[r].replace(n, c)

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
        # Histograms
        if obj.IsA().InheritsFrom('TH1'):
            if verbose: print ' + TH1:', obj.GetName()
            new_file.cd()
            obj.Write()
        # Tree
        elif obj.IsA().InheritsFrom('TTree'):
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
                eventWeightLumi[0] = 1.
                
                # Weights
                if isMC:
                    eventWeightLumi[0] = obj.eventWeight #* (obj.triggerElectronWeight*obj.triggerMuonWeight*obj.electronWeight*obj.muonWeight)/(obj.triggerElectronIsoWeight*obj.triggerMuonIsoWeight*obj.electronIsoWeight*obj.muonIsoWeight)
                    eventWeightLumi[0] *= obj.triggerElectronWeight if obj.triggerElectronWeight>0 else 1.
                    eventWeightLumi[0] *= obj.triggerMuonWeight if obj.triggerMuonWeight>0 else 1.
                    eventWeightLumi[0] *= obj.electronWeight if obj.electronWeight>0 else 1.
                    eventWeightLumi[0] *= obj.muonWeight if obj.muonWeight>0 else 1.
                    eventWeightLumi[0] /= obj.triggerElectronIsoWeight if obj.triggerElectronIsoWeight>0 else 1.
                    eventWeightLumi[0] /= obj.triggerMuonIsoWeight if obj.triggerMuonIsoWeight>0 else 1.
                    eventWeightLumi[0] /= obj.electronIsoWeight if obj.electronIsoWeight>0 else 1.
                    eventWeightLumi[0] /= obj.muonIsoWeight if obj.muonIsoWeight>0 else 1.
                    eventWeightLumi[0] *= 2460 if 'XZh' in obj.GetName() else 2110
                
                # Fill the branches
                eventWeightLumiBranch.Fill()

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
                    new_file.cd(subdir)
                    subobj.Write()
            new_file.cd('..')
        
    new_file.Close() 



jobs = []
for d in os.listdir(origin):
    if 'BBbarDM' in d or 'TTbarDM' in d: continue
    #if not 'ZprimeToZhToZinvhbb_narrow_M-800_13TeV-madgraph-v1' in d: continue
#    print d
    p = multiprocessing.Process(target=processFile, args=(d,verboseon,))
    jobs.append(p)
    p.start()
    #exit()
    
#print '\nDone.'

