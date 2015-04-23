#! /usr/bin/env python
import os, sys, time, multiprocessing
from ROOT import TFile, gROOT, RooDataSet, RooAbsData
gROOT.Macro('functions.C')
RooDataSet.setDefaultStorageType(RooAbsData.Tree)

from analyzer import Analyzer
from observables import observables
from setup import Configuration

# the configuration
cfg=Configuration()
cfg.parametersSet['observable'] = 'met'
cfg.parametersSet['met_cut'] = 120
cfg.parametersSet['lumi'] = '20000' # pb^-1
cfg.parametersSet['verbosity'] = 3

# which variable to store where
variables = {'SR':['met'],
             'ZCR':['fakemet'],
             'WCR':['fakemet'],
             'GCR':['fakemet']}


# loop over the analysis regions
for region in variables:
    print region
    cfg.parametersSet['region'] = region
    analyzer = Analyzer(cfg)
    rooDataSets = analyzer.generate([observables[o] for o in observables if o in variables[region]])
    output_file = TFile('datasets_'+region+'.root','recreate')
    for d in rooDataSets: rooDataSets[d].Write()


