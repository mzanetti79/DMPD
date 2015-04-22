from array import array

#momentum_bins=range(200,331,10)+[350, 380, 430, 500, 1000]
momentum_bins=range(100,331,25)+[350, 380, 430, 500, 1000]

class Observable():
    def __init__(self,**k):
        # defaults
        self.variable='met' 
        self.formula=self.variable 
        self.bins = array('d',sorted(momentum_bins)) 
        self.labelX = self.variable
        self.labelY = 'events / GeV'
        self.scale_bin_content = True
        # from constructor
        self.__dict__.update(k)
        self.nBinsX = len(self.bins)-1
        self.plot = 'min(max('+self.formula+','+str(self.bins[0])+'),'+str(self.bins[-1])+')' 


observables = {
    'default':Observable(variable='met',
                         formula='met_pt',
                         labelX='E_{T}^{miss} [GeV]',
                         ),
    'met':Observable(variable='met',
                     formula='met_pt',
                     labelX='E_{T}^{miss} [GeV]',
                     ),
    'fakemet':Observable(variable='met',
                        formula='fakemet_pt',
                        labelX='E_{T}^{miss} [GeV]',
                     ),
    'jet1Pt':Observable(variable='jet1Pt',
                        formula='jet_pt[0]',
                        labelX='leading jet p_{T} [GeV]',
                        ),
    'metPhi':Observable(variable='metPhi',
                        formula='fakemet_phi',
                        labelX='E_{T}^{miss} #phi',
                        scale_bin_content=False,
                        ),
    'fakemetPhi':Observable(variable='metPhi',
                        formula='met_phi',
                        labelX='E_{T}^{miss} #phi',
                        scale_bin_content=False,
                        ),
    'nJets':Observable(variable='nJets',
                        formula='nJets',
                        labelX='muon multiplicity',
                        scale_bin_content=False,
                        bins = array('d',range(0,5))
                        ),
    'nMuons':Observable(variable='nMuons',
                        formula='nMuons',
                        labelX='muon multiplicity',
                        scale_bin_content=False,
                        bins = array('d',range(0,5))
                        ),
    'nElectrons':Observable(variable='nElectrons',
                            formula='nElectrons',
                            labelX='muon multiplicity',
                            scale_bin_content=False,
                            bins = array('d',range(0,5))
                            ),
    'dPhiJet1Jet2': Observable(variable='dPhiJet1Jet2',
                               formula='deltaPhi(jet_phi[0],jet_phi[1])',
                               labelX='#Delta#phi(jet_{1},jet_{2})',
                               scale_bin_content=False,
                               bins = array('d',[v/10. for v in range(0,33)])
                               ),  
    'bDisc': Observable(variable='bDisc',
                        formula='jet_CSV[0]',
                        labelX='leading jet CSV',
                        scale_bin_content=False,
                        bins = array('d',[v/25. for v in range(0,26)]),  
                        ),
    'Zmass': Observable(variable='Zmass',
                        formula='Z_mass',
                        labelX='mass [GeV]',
                        bins = array('d',[60,70,80,85]+range(86,95)+[95,100,110,120]),  
                        ),
                

    }

#               'dPhiMetJet1':'deltaPhi(jet1.Phi(), metPhi)',
#               'dPhiMetJet2':'deltaPhi(jet2.Phi(), metPhi)',
#               'njets':'njets',
#               'nphotons':'nphotons',
#               'jet1Pt':'jet1_pt()',
#               'jet2Pt':'jet2_pt()',
#               'jet1Eta':'jet1_eta()',
#               'jet2Eta':'jet2_eta()',
#               'lep1Pt':'lep1.pt()',
#               'lep2Pt':'lep2.pt()',
#               'lep1Eta':'lep1.eta()',
#               'lep2Eta':'lep2.eta()',
#               'mll':'vectorSumMass(lep1.px(),lep1.py(),lep1.pz(),lep2.px(),lep2.py(),lep2.pz())',                        
#               'mT':'transverseMass(lep1.Pt(),lep1.Phi(),met,metPhi)',                        



