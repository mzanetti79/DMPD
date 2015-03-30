#! /usr/bin/env python
from setup import Setup
from datasets import processes
from selections import Selection
from plottingTools import *
from ROOT import THStack, TLegend, TCanvas

class Analyzer():
    def __init__(self, cfg, label):
        self.cfg = cfg
        self.cfg.check_parametersSet()
        self.cfg.log_parametersSet(label)
        self.setup = Setup(cfg.parametersSet)
        self.trees = self.setup.grow_trees()
        self.setup.create_observable()
        self.init_selection()

    def init_selection(self):
        selection = Selection()
        selection.build_selection(self.setup.configuration)
        self.selection = selection.selection
        print ''
        print 'Applying the following selection:'
        print self.selection
        print ''

    def analyze(self):
        self.histograms = {}
        for process_name in self.trees:
            self.histograms[process_name] = self.setup.make_histogram(process_name)
            selection = self.selection
            if process_name.find('data')==-1: 
                weight = str(self.cfg.parametersSet['lumi'])+'*weight' 
                selection = '('+selection+')*'+weight 
            self.trees[process_name].Project(self.histograms[process_name].GetName(), 
                                             self.setup.observable.plot, 
                                             selection)


    def format_histograms(self):
        self.formatted_histograms = {}
        stack = THStack('stack','')
        self.legend = TLegend(0.16,0.67,0.4,0.92)
        self.legend.SetFillColor(0)
        self.legend.SetLineColor(0)
        self.legend.SetBorderSize(0)

        for process_name in self.setup.order_processes():
            try: self.histograms[process_name]
            except KeyError: continue
            hist = self.histograms[process_name]
            # --> events / GeV
            for bin in range(1,hist.GetNbinsX()+1):
                hist.SetBinContent(bin,hist.GetBinContent(bin)/hist.GetBinWidth(bin))
                hist.SetBinError(bin,hist.GetBinError(bin)/hist.GetBinWidth(bin))
            # data
            if process_name.find('data')>-1:
                legendMarker = 'p'
                hist.SetMarkerStyle(20)
                hist.SetMarkerSize(1.3)
                self.formatted_histograms['data'] = hist
            # signal
            elif process_name.find('signal')>-1: 
                legendMarker = 'l'
                hist.SetLineWidth(2)            
                hist.SetFillColor(0)
                hist.SetLineColor(2)
                self.formatted_histograms['signal'] = hist
            # MC
            else:  
                legendMarker = 'f'
                hist.SetLineColor(processes[process_name]['color'])
                hist.SetFillColor(processes[process_name]['color'])
                stack.Add(hist)
                self.formatted_histograms['background'] = stack
            # adding to the legend
            self.legend.AddEntry(hist,processes[process_name]['label'],legendMarker)

    
    def draw(self,name):
        self.make_canvas(name) 
        self.formatted_histograms['background'].Draw('fhist')
        self.formatted_histograms['background'].GetXaxis().SetTitle(self.setup.observable.labelX)
        self.formatted_histograms['background'].GetYaxis().SetTitle(self.setup.observable.labelY)
        self.formatted_histograms['background'].GetXaxis().SetNdivisions(505)
        self.formatted_histograms['background'].GetYaxis().SetNdivisions(505)
        try: 
            self.formatted_histograms['data'].Draw('ep,same') 
            self.draw_compare()
        except: print 'data not plotted'
        try: self.formatted_histograms['signal'].Draw('hist,same') 
        except: print 'signal not plotted'
        self.legend.Draw()
            

    def make_canvas(self,name):
        self.canvas = MultiCanvas(name) if self.formatted_histograms.has_key('data') else TCanvas(name,name)
        SetOwnership(self.canvas,False)

