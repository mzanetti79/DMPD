#! /usr/bin/env python
from observables import observables
from ROOT import TH1D, THStack, TLegend, TCanvas

class Looper():
    def __init__(self, variables, name):
        self.observables, self.histograms = {}, {}
        self.create_observables(variables, name)
        
    def create_observables(self, variables, name):
        for variable in variables:
            try: self.observables[variable] = observables[variable]
            except:
                print 'WARNING: '+variable+', not defined as observable, used default instead'
                self.observables[variable] = observables['default']
            self.make_histogram(variable, name)
            
    def make_histogram(self, variable, name):
        self.histograms[variable] = TH1D('h'+variable+name,'',
                                         self.observables[variable].nBinsX,
                                         self.observables[variable].bins)
        self.histograms[variable].Sumw2()

    def loop(self, tree):
        for event in range(0, tree.GetEntries()):
            if event%1000000==0: print event 
            tree.GetEntry(event)

            # 
            if not tree.HLT_BIT_HLT_IsoMu24_eta2p1_v: continue
            if not (tree.lepton1_isMuon and tree.lepton1_tightId and tree.lepton1_pt>20 and tree.lepton1_relIso04<0.12 and tree.lepton2_isMuon and tree.lepton2_pt>15): continue
            if not (tree.Z_mass>70 and tree.Z_mass<110): continue

            weight = 1 if (tree.isData and tree.eventWeight>0.001) else tree.eventWeight
            self.histograms['jet1Pt'].Fill(tree.jet1_pt, weight)
            self.histograms['Zmass'].Fill(tree.Z_mass, weight)
