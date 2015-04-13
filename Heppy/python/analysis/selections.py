
class Selection:
    def __init__(self, cfg):
        self.cfg = cfg
        met_cut = 120
        if self.cfg.has_key('met_cut'): met_cut = self.cfg['met_cut']
        self.cuts = {
            'common': {
                'leading jet':'jet_pt[0]>100&&abs(jet_eta[0])<2.4',
                'trailing jet':'(jet_pt[1] <30||deltaPhi(jet_phi[0],jet_phi[1])<2)',
                #'trailing jet':'(jet_pt[1] <30||deltaPhi(jet_phi[0],jet_phi[1])<4)',
                'jet multiplicity':'nJets<3',
                'veto':'nElectrons==0&&nTaus==0',
                #'trigger':'',
                #'cleaning':'',
                },
            'SR': {
                'met':'met_pt>'+str(met_cut),
                'dPhi(Jet1,Met)':'deltaPhi(jet_phi[0], met_phi)>1.8',
                'muon veto': 'nMuons==0',
                'photon veto': 'nPhotons==0',
                #'b-tag':'jet_CSV[0]>0.423',
                },
            'GCR': {
                'fakemet':'fakemet_pt>'+str(met_cut),
                'dPhi(Jet1,Met)':'deltaPhi(jet_phi[0], fakemet_phi)>1.8',
                'photon pt': 'photon_pt[0]>160',
                'muon veto': 'nMuons==0',
                },
            'ZCR': {
                'met':'fakemet_pt>'+str(met_cut),
                'dPhi(Jet1,Met)':'deltaPhi(jet_phi[0], fakemet_phi)>1.8',
                'Z': 'Z_mass>60&&Z_mass<120',
                'photon veto': 'nPhotons==0',
                },
            'WCR': {
                'met':'fakemet_pt>'+str(met_cut),
                'dPhi(Jet1,Met)':'deltaPhi(jet_phi[0], fakemet_phi)>1.8',
                'W': 'abs(transverseMass(muon_pt[0],muon_phi[0],met_pt,met_phi)-75)<25',
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

        

