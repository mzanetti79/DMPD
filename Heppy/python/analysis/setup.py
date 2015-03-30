import os, pickle
from datasets import processes
from observables import observables
from ROOT import TChain, TH1D

class Configuration():
    def __init__(self):
        self.parametersSet = {}

    def check_parametersSet(self):
        parametersSet_is_good = True
        # list of mandatory parameters
        for p in ['region',  'observable', 'lumi']:
            if not self.parametersSet.has_key(p): 
                print 'ERROR:', p, 'not found in the configuration' 
                parametersSet_is_good = False
        # region must match tree names inside the root file    
        valid_regions = ['SR','ZCR','WCR','GCR']
        if not self.parametersSet['region'] in valid_regions: 
            print 'ERROR: not a valid phase space region '
            print 'valid phase space regions are', valid_regions
            parametersSet_is_good = False
        
        return parametersSet_is_good

    def log_parametersSet(self,label):
        log_file='logs/log.pkl'
        try: 
            with open(log_file,'rb'): log_data = pickle.load(open(log_file,'rb'))
        except IOError: log_data = {label:{}}
        log_data[label]=self.parametersSet
        pickle.dump(log_data,open(log_file,'wb'))


class Setup():

    def __init__(self, configuration):
        self.configuration = configuration
        self.setup_processes()

    def setup_processes(self):
        '''
        Remove processes which do not have a corresponding ntuple (e.g. data at the moment)
        '''
        self.processes = {}
        for p in processes:
            sample_to_be_added = True
            for f in processes[p]['files']:
                if not os.path.exists(f): 
                    sample_to_be_added = False
                    print 'WARNING:', p, 'is not there'
                if self.configuration['region']!='GJets' and p=='GJets': sample_to_be_added = False
            if sample_to_be_added: self.processes[p] = processes[p]


    def order_processes(self):
        '''
        order the list of processes
        '''
        tmp = {}
        for p in self.processes: 
            if self.processes[p]['ordering']>-1: tmp[p] = self.processes[p]['ordering']
        ordered_processes = []
        for key, value in sorted(tmp.iteritems(), key=lambda (k,v): (v,k)):
            ordered_processes.append(key)
        return ordered_processes

    def grow_trees(self):
        '''
        build the TChains.
        '''
        trees = {}
        for process in self.processes:
            trees[process] = TChain()
            for f in self.processes[process]['files']: 
                trees[process].Add(f+'/'+self.configuration['region'])
        return trees

    def create_observable(self):
        if type(self.configuration['observable'])==str:
            if observables.has_key(self.configuration['observable']):
                self.observable = observables[self.configuration['observable']]
        else: self.observable = self.configuration['observable']
        if not self.observable:
            print 'WARNING: not a recognizable observable:', self.configuration['observable']
            self.observable = observables['default']

    def make_histogram(self,process_name):
        histogram = TH1D(self.observable.variable+process_name,'',self.observable.nBinsX, self.observable.bins)
        histogram.Sumw2()
        return histogram
