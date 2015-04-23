#! /usr/bin/env python
from setup import Setup
from datasets import processes
from selections import Selection
from plottingTools import *
from ROOT import THStack, TLegend, TCanvas

class Analyzer():
    def __init__(self, cfg, hash_label=''):
        self.cfg = cfg
        self.cfg.check_parametersSet()
        if hash_label: self.cfg.log_parametersSet(hash_label)
        self.setup = Setup(cfg.parametersSet)
        self.trees = self.setup.grow_trees()
        self.setup.create_observable()
        self.init_selection()

    def init_selection(self):
        selection = Selection(self.setup.configuration)
        selection.build_selection()
        self.selection = selection.selection
        if self.cfg.parametersSet['verbosity'] > 2:
            print ''
            print 'Applying the following selection:'
            print self.selection
            print ''

    def analyze(self):
        self.histograms = {}
        for process_name in self.trees:
            if self.cfg.parametersSet['verbosity'] > 2:
                print 'processing', process_name, self.trees[process_name].GetName()
            self.histograms[process_name] = self.setup.make_histogram(process_name+'_'+self.cfg.name)
            selection = self.selection
            if process_name.find('data')==-1: 
                weight = str(self.cfg.parametersSet['lumi'])+'*weight' 
                selection = '('+selection+')*'+weight 
            self.trees[process_name].Project(self.histograms[process_name].GetName(), 
                                             self.setup.observable.plot, 
                                             selection)


    def generate(self, variables, weight=':weight'):
        from formatting import getRooDataSet
        rooDataSets = {}
        for process_name in self.trees:
            self.trees[process_name].Project('h'+process_name,
                                             ':'.join([o.formula for o in variables])+weight,
                                             self.selection,
                                             'para goff')
            rooDataSets[process_name] = getRooDataSet(self.trees[process_name], variables, self.cfg.parametersSet)
        return rooDataSets
    
            
    def print_yields(self):
        print ''
        print 'Yields:'
        for process_name in self.histograms: 
            print process_name, int(self.histograms[process_name].Integral(0,-1))

    def rescale_bins(self,hist):
        for bin in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(bin,hist.GetBinContent(bin)/hist.GetBinWidth(bin))
            hist.SetBinError(bin,hist.GetBinError(bin)/hist.GetBinWidth(bin))

            
    def format_histograms(self):
        self.formatted_histograms = {}
        stack = THStack('stack'+self.cfg.name,'')
        self.legend = TLegend(0.65,0.6,0.88,0.88)
        self.legend.SetFillColor(0)
        self.legend.SetLineColor(0)
        self.legend.SetBorderSize(0)

        for process_name in self.setup.order_processes():
            try: self.histograms[process_name]
            except KeyError: continue
            hist = self.histograms[process_name]
            # --> events / GeV
            if self.setup.observable.scale_bin_content: self.rescale_bins(hist)
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

    
    def draw(self,name=''):
        if name=='': name=self.cfg.name
        self.make_canvas(name) 
        self.formatted_histograms['background'].Draw('fhist')
        self.formatted_histograms['background'].GetXaxis().SetTitle(self.setup.observable.labelX)
        self.formatted_histograms['background'].GetYaxis().SetTitle(self.setup.observable.labelY)
        self.formatted_histograms['background'].GetXaxis().SetNdivisions(505)
        self.formatted_histograms['background'].GetYaxis().SetNdivisions(505)
        try: 
            self.formatted_histograms['data'].Draw('ep,same') 
            self.draw_compare()
        except:
            if self.cfg.parametersSet['verbosity'] > 2: print 'data not plotted'
        try: self.formatted_histograms['signal'].Draw('hist,same') 
        except:
            if self.cfg.parametersSet['verbosity'] > 2: print 'signal not plotted'
        self.legend.Draw()
            

    def make_canvas(self,name):
        self.canvas = MultiCanvas(name) if self.formatted_histograms.has_key('data') else TCanvas(name,name,1000,800)
        self.canvas.SetLogy()
        SetOwnership(self.canvas,False)

