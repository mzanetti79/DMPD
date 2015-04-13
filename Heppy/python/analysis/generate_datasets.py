#! /usr/bin/env python
import os, sys, time, multiprocessing

from ROOT import TFile, gROOT, RooDataSet, RooAbsData
gROOT.Macro('functions.C')
RooDataSet.setDefaultStorageType(RooAbsData.Tree)

from analyzer import Analyzer
from observables import observables
from setup import Configuration

cfg=Configuration()
cfg.parametersSet['observable'] = 'met'
cfg.parametersSet['met_cut'] = 120
cfg.parametersSet['lumi'] = '20000' # pb^-1

variables = {'SR':['met'],
             'ZCR':['fakemet'],
             'WCR':['fakemet'],
             'GCR':['fakemet']}


for region in variables:
    print region
    cfg.parametersSet['region'] = region
    analyzer = Analyzer(cfg)
    rooDataSets = analyzer.generate([observables[o] for o in observables if o in variables[region]])
    output_file = TFile('datasets_'+region+'.root','recreate')
    for d in rooDataSets: rooDataSets[d].Write()


