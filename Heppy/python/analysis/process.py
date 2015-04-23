#! /usr/bin/env python
import os, sys, time, multiprocessing
from ROOT import TFile, gROOT
gROOT.Macro('functions.C')

### The Configuration
from setup import Configuration
cfg=Configuration()

## mandatory configurations parameters
cfg.parametersSet['region'] = 'SR'
cfg.parametersSet['observable'] = 'met'
cfg.name=cfg.parametersSet['region']+'_'+cfg.parametersSet['observable']
cfg.parametersSet['lumi'] = '5000' # pb^-1

### you can build observables and selections on the fly
#from observables import Observable
#cfg.parametersSet['observable'] = Observable(variable='ZpT',formula='z_pt',labelX='Z p_{T} [GeV]')
#cfg.parametersSet['selection'] = '{"leading jet":"jets_pt[0]>120"}'

### The Analysis
from analyzer import Analyzer
label = str(hash(frozenset(cfg.parametersSet.items()))) if False else '' # log or not
analyzer = Analyzer(cfg, label)
analyzer.analyze()
analyzer.print_yields()
analyzer.format_histograms()
analyzer.draw()

    


