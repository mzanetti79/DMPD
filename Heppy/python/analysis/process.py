#! /usr/bin/env python
import os, sys, time, multiprocessing

from ROOT import TFile, gROOT
gROOT.Macro('functions.C')

from setup import Configuration
cfg=Configuration()
from observables import Observable

cfg.parametersSet['region'] = 'SR'
cfg.parametersSet['observable'] = 'met'
cfg.parametersSet['lumi'] = '10000' # pb^-1
#cfg.parametersSet['observable'] = Observable(variable='ZpT',formula='z_pt',labelX='Z p_{T} [GeV]')
#cfg.parametersSet['selection'] = '{"leading jet":"jets_pt[0]>120"}'

label = str(hash(frozenset(cfg.parametersSet.items())))

from analyzer import Analyzer
analyzer = Analyzer(cfg, label)
analyzer.analyze()
analyzer.format_histograms()
analyzer.draw('pippo')

histograms = analyzer.formatted_histograms

# manage output
output_file = TFile('plots.root' if not cfg.parametersSet.has_key('output_name') else cfg.parametersSet['output_name'],
                    'recreate')
for h in histograms: histograms[h].Write()
output_file.Close()

output_file = TFile('logs/log.root', 'update')
output_file.mkdir(label)
output_file.cd(label)
for h in histograms: histograms[h].Write()
output_file.Close()

