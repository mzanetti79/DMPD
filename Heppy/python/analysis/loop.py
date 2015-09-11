#! /usr/bin/env python
import multiprocessing
from ROOT import TFile, gROOT

### the timeout (needed for some to be understood reasons..)
timeout = 20

### what to plot
variables = ['jet1Pt','Zmass']

### The Configuration
from setup import Configuration, Setup
cfg=Configuration()

## mandatory configurations parameters
cfg.parametersSet['region'] = 'ZCR'
cfg.parametersSet['samples_set'].append('data_singlemu')
cfg.parametersSet['verbosity'] = 3
cfg.name=cfg.parametersSet['region']+'_pippo' # FIXME
cfg.parametersSet['lumi'] = '41.9' # pb^-1

### creating the setup
setup = Setup(cfg.parametersSet)
trees = setup.grow_trees()

### the looper
from looper import Looper
def worker(tree, variables, process_name, result_queue):
    looper = Looper(variables,process_name)
    looper.loop(tree)
    result_queue.put([process_name,looper])

### launch the processes
processes = []
result_queue = multiprocessing.Queue()
for process_name in trees:
    print 'Launching analysis for', process_name
    process = multiprocessing.Process(target = worker,
                                      args = [trees[process_name], variables, process_name, result_queue])
    process.start()
    processes.append(process)
    
### close the processes
for process in processes: process.join(timeout)

### retrieve the results
results = {}
while len(results) < len(processes):
    result = result_queue.get()
    results[result[0]] = result[1]

### post process the results
## rearrange
histograms, formatted_histograms, legends, plotters = {}, {}, {}, {}
from post_processing import *
for plot in variables:
    histograms[plot] = {}
    for result in results: histograms[plot][result] = results[result].histograms[plot]
    formatted_histograms[plot], legends[plot] = format_histograms(result, histograms[plot], setup, True)
    plotters[plot] = Plotter(plot, formatted_histograms[plot], legends[plot])
    plotters[plot].plot()
    plotters[plot].multi_canvas.canvas.SaveAs('/Users/mzanetti/Sites/cms/DMPD/looper_'+plotters[plot].multi_canvas.canvas.GetName()+'.png')
    #plotters[plot].multi_canvas.canvas.Write()
    

        
