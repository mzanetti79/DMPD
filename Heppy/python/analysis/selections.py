
class Selection:
    def __init__(self, cfg):
        self.cfg = cfg
        self.cuts_values = {'met':'-1', #200
                            'dPhiJetMet': '-1', #'2.0',
                            'dPhiJet1Jet2': '5', #'2.5',
                            'jet1_CSV':'-1e3', #'0.814',
                            'jet2_CSV':'-1e3', #'0.814',
                            }
        if self.cfg.has_key('met_cut'): self.cuts_values['met'] = self.cfg['met_cut']
        self.cuts = {
            'common': {
                #'leading jet':'jet1_pt>50&&abs(jet1_eta)<2.5 && jet1_chf>0.2 && jet1_nhf<0.7 && jet1_phf<0.7',
                #'trailing jet':'(nJets==1 || (nJets==2 && jet2_nhf<0.7 && jet2_phf<0.9 && deltaPhi(jet1_phi,jet2_phi)<'+self.cuts_values['dPhiJet1Jet2']+' && jet2_CSV>='+self.cuts_values['jet2_CSV']+'))',
                #'jet multiplicity':'nJets<3',
                'veto':'nTaus==0',
                #'b-tag':'jet1_CSV>='+self.cuts_values['jet1_CSV'],
                },
            'SR': {
                #'trigger':'',
                'met':'met_pt>'+self.cuts_values['met'],
                'topology':'deltaPhi(jet1_phi, met_phi)>'+self.cuts_values['dPhiJetMet'],
                'objects veto': 'nMuons==0&&nElectrons==0&&nPhotons==0',
                },
            'GCR': {
                #'trigger':'',
                'met':'fakemet_pt>'+self.cuts_values['met'],
                'topology':'deltaPhi(jet1_phi, fakemet_phi)>'+self.cuts_values['dPhiJetMet'],
                'photon pt': 'photon1_pt>160',
                'objects veto': 'nMuons==0&&nElectrons==0',
                },
            'ZCR': {
                'trigger':'HLT_BIT_HLT_IsoMu24_eta2p1_v',
                'met':'fakemet_pt>'+self.cuts_values['met'],
                #'dPhi(Jet1,Met)':'deltaPhi(jet1_phi, fakemet_phi)>'+self.cuts_values['dPhiJetMet'],
                'muon1Id': 'lepton1_isMuon && lepton1_tightId && lepton1_pt>20 && lepton1_relIso04<0.12',
                'muon2Id':'lepton2_isMuon && lepton2_pt>15',
                'Z':'Z_mass>70 && Z_mass<110',
                'object veto': 'nPhotons==0&&nElectrons==0',
                },
            'WCR': {
                'trigger':'HLT_BIT_HLT_IsoMu24_eta2p1_v',
                'met':'fakemet_pt>'+self.cuts_values['met'],
                #'dPhi(Jet1,Met)':'deltaPhi(jet1_phi, fakemet_phi)>1.8'+self.cuts_values['dPhiJetMet'],
                'muonId':'lepton1_isMuon && lepton1_tightId && lepton1_pt>30 && abs(lepton1_eta)<2.1 && lepton1_relIso04<0.12',
                #'W': 'abs(transverseMass(lepton1_pt,lepton1_phi,met_pt,met_phi)-75)<25',
                #'W': 'abs(W_mass-75)<25',
                'photon veto': 'nPhotons==0&&nElectrons==0',                
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

        

