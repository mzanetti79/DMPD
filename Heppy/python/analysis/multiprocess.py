#! /usr/bin/env python
import os, sys, time, multiprocessing
from ROOT import TFile, gROOT
gROOT.Macro('functions.C')

# the timeout
timeout = 20

## tell me what I need to plot
common_plots = ['nJets','jet1Pt']
to_be_processed = {
    'SR':['nJets','met','jet1Pt'],
    'ZCR':common_plots+['fakemet','Zmass'],
    #'WCR':common_plots,
    #'GCR':common_plots,
    }

## the configuration. First the common features
from setup import Configuration
cfg=Configuration()
cfg.parametersSet['lumi'] = '5000' # pb^-1

## the analyzer
from analyzer import Analyzer
def worker(cfg, label, result_queue):
    analyzer = Analyzer(cfg, label)
    analyzer.analyze()
    analyzer.format_histograms()
    result_queue.put([cfg.parametersSet['observable'],analyzer])

### launch the threads
processes = []
result_queue = multiprocessing.Queue()
## looping on the regions and the plots
for phasespace_region in to_be_processed:
    for plot in to_be_processed[phasespace_region]:
        cfg.parametersSet['region'] = phasespace_region
        cfg.parametersSet['observable'] = plot
        cfg.name=cfg.parametersSet['region']+'_'+cfg.parametersSet['observable']
        #label = str(hash(frozenset(cfg.parametersSet.items())))
        label = ''
        process = multiprocessing.Process(target = worker, args = [cfg, label, result_queue])
        process.start()
        processes.append(process)
for process in processes: process.join(timeout)

### retrieve the results
results = {}
while len(results) < len(processes):
    result = result_queue.get()
    print 'retriving results', result
    results[result[0]] = result[1]
    result[1].draw()

### save the results
    
### kill the processes    
for process in processes: process.terminate()


