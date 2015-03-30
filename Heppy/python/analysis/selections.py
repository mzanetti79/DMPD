
class Selection:
    def __init__(self):
        self.cuts = {
            'common': {
                'leading jet':'jets_pt[0]>150&&abs(jets_eta[0])<2.4',
                'trailing jet':'(jets_pt[1] <30||deltaPhi(jets_phi[0],jets_phi[1])<2)',
                'jet multiplicity':'nJets<3',
                'veto':'nElectrons==0&&nTaus==0',
                #'trigger':'',
                #'cleaning':'',
                },
            'SR': {
                'met':'met_pt>200',
                'dPhi(Jet1,Met)':'deltaPhi(jets_phi[0], met_phi)>1.8',
                'muon veto': 'nMuons==0',
                'photon veto': 'nPhoton==0',
                },
            'ZCR': {
                'met':'fakeMEt_pt>200',
                'dPhi(Jet1,Met)':'deltaPhi(jets_phi[0], fakeMEt_phi)>1.8',
                'Z': 'z_mass>60&&z_mass<120',
                'photon veto': 'nphotons==0',
                },
            }

    def build_selection(self, cfg):
        self.interpret_cfg(cfg)
        self.selection = ''
        for i in self.cuts:
            if not self.selection: self.selection='&&'.join(self.cuts[i].values())
            else: self.selection+='&&'+'&&'.join(self.cuts[i].values())

    def interpret_cfg(self,cfg):
        if cfg.has_key('selection'):
            for cut in cfg['selection']: # needs to be a dictionary
                for i in self.cuts: self.cuts[i][cut] = cfg['selection'][cut] 
        self.cuts = {i:self.cuts[i] for i in self.cuts if i in ['common',cfg['region']]}

        

