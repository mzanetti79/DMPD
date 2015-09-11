#! /usr/bin/env python
import os, sys, time, multiprocessing
from ROOT import TFile, gROOT
gROOT.Macro('functions.C')

### the timeout (needed for some to be understood reasons..)
timeout = 10

### tell me what I need to plot
common_plots = [] #['nJets','jet1Pt']
to_be_processed = {
    #'SR':common_plots+['met', 'dPhiJet1Jet2', 'jet2Phi'],
    'ZCR':common_plots+['jet1Pt', 'Zmass'],
    #'WCR':common_plots,
    #'GCR':common_plots,
    }

### the configuration. First the common features
from setup import Configuration
cfg=Configuration()
cfg.parametersSet['lumi'] = '41.9' # pb^-1
cfg.parametersSet['samples_set'].append('data_singlemu') ### FIXME

### the analyzer
from analyzer import Analyzer
def worker(cfg, label, result_queue):
    analyzer = Analyzer(cfg, label)
    analyzer.analyze()
    result_queue.put([cfg.name,analyzer])

### launch the processes
processes = []
result_queue = multiprocessing.Queue()
## looping on the regions and the plots
for phasespace_region in to_be_processed:
    for plot in to_be_processed[phasespace_region]:
        print 'Launching analysis for region', phasespace_region, 'and plotting', plot
        cfg.parametersSet['region'] = phasespace_region
        cfg.parametersSet['observable'] = plot
        cfg.name=cfg.parametersSet['region']+'_'+cfg.parametersSet['observable']
        process = multiprocessing.Process(target = worker, args = [cfg, '', result_queue])
        process.start()
        processes.append(process)

### close the processes
for process in processes: process.join(timeout)

### retrieve the results
results = {}
while len(results) < len(processes):
    result = result_queue.get()
    results[result[0]] = result[1]

### plot and save the results
output = TFile(cfg.parametersSet['output_name'],'recreate')
from plotter import Plotter
plotters = {}
for plot in results:
    plotters[plot] = Plotter(results[plot])
    plotters[plot].plot()
    plotters[plot].multi_canvas.canvas.SaveAs('/Users/mzanetti/Sites/cms/DMPD/'+plotters[plot].multi_canvas.canvas.GetName()+'.png')
    plotters[plot].multi_canvas.canvas.Write()
    #results[plot].draw()
    #results[plot].canvas.SaveAs('plots/'+results[plot].canvas.GetName()+'.png')
    #results[plot].canvas.Write()
    

