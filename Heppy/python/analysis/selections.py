
class Selection:
    def __init__(self, cfg):
        self.cfg = cfg
        met_cut = 200
        if self.cfg.has_key('met_cut'): met_cut = self.cfg['met_cut']
        self.cuts = {
            'common': {
                'leading jet':'jet1_pt>15&&abs(jet1_eta)<2.5',
                'trailing jet':'(jet2_pt <30||deltaPhi(jet1_phi,jet2_phi)<2)',
                'jet multiplicity':'nJets<3',
                'veto':'nElectrons==0&&nTaus==0',
                #'trigger':'',
                #'cleaning':'',
                },
            'SR': {
                'met':'met_pt>'+str(met_cut),
                'dPhi(Jet1,Met)':'deltaPhi(jet1_phi, met_phi)>2.0',
                'muon veto': 'nMuons==0',
                'photon veto': 'nPhotons==0',
                #'b-tag':'jet1_CSV>0.423',
                },
            'GCR': {
                'fakemet':'fakemet_pt>'+str(met_cut),
                'dPhi(Jet1,Met)':'deltaPhi(jet1_phi, fakemet_phi)>1.8',
                'photon pt': 'photon1_pt>160',
                'muon veto': 'nMuons==0',
                },
            'ZCR': {
                'met':'fakemet_pt>'+str(met_cut),
                'dPhi(Jet1,Met)':'deltaPhi(jet1_phi, fakemet_phi)>1.8',
                'Z': 'Z_mass>60&&Z_mass<120',
                'photon veto': 'nPhotons==0',
                },
            'WCR': {
                'met':'fakemet_pt>'+str(met_cut),
                'dPhi(Jet1,Met)':'deltaPhi(jet1_phi, fakemet_phi)>1.8',
                'W': 'abs(transverseMass(muon1_pt,muon1_phi,met_pt,met_phi)-75)<25',
                'photon veto': 'nPhotons==0',
                },
            }

    def build_selection(self):
        self.interpret_cfg()
        self.selection = ''
        for i in self.cuts:
            if not self.selection: self.selection='&&'.join(self.cuts[i].values())
            else: self.selection+='&&'+'&&'.join(self.cuts[i].values())

    def interpret_cfg(self):
        if self.cfg.has_key('selection'):
            for cut in self.cfg['selection']: # needs to be a dictionary
                for i in self.cuts: self.cuts[i][cut] = self.cfg['selection'][cut] 
        self.cuts = {i:self.cuts[i] for i in self.cuts if i in ['common', self.cfg['region']]}

        

