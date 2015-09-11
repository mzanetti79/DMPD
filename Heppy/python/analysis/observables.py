from array import array

momentum_bins=range(0,150,10)+range(150,326,25)+[350, 380, 430, 500, 1000]

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
                        formula='jet1_pt',
                        labelX='leading jet p_{T} [GeV]',
                        ),
    'fatjetPt':Observable(variable='fatjetPt',
                        formula='fatjet1_pt',
                        labelX='fat jet p_{T} [GeV]',
                        ),
    'fatjetMass':Observable(variable='fatjetMass',
                        formula='fatjet1_mass',
                        labelX='fat jet mass [GeV]',
                        ),
    'jet2Phi':Observable(variable='jet2Phi',
                        formula='jet2_phi',
                        labelX='leading jet #phi',
                        scale_bin_content=False,
                        bins = array('d',[v/10. for v in range(-33,33)])
                        ),
    'lep1Pt':Observable(variable='lep1Pt',
                        formula='lepton1_pt',
                        labelX='leading lepton p_{T} [GeV]',
                        ),
    'lep2Pt':Observable(variable='lep2Pt',
                        formula='lepton2_pt',
                        labelX='trailing lepton p_{T} [GeV]',
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
                        bins = array('d',range(0,10))
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
                               formula='deltaPhi(jet1_phi,jet2_phi)',
                               labelX='#Delta#phi(jet_{1},jet_{2})',
                               scale_bin_content=False,
                               bins = array('d',[v/10. for v in range(-33,33)])
                               ),  
    'bDisc': Observable(variable='bDisc',
                        formula='jet1_CSV',
                        labelX='leading jet CSV',
                        scale_bin_content=False,
                        bins = array('d',[v/25. for v in range(0,26)]),  
                        ),
    'Zmass': Observable(variable='Zmass',
                        formula='Z_mass',
                        labelX='mass [GeV]',
                        bins = array('d',[60,70,80,85]+range(86,95)+[95,100,110,120]),  
                        ),
    'Wmass': Observable(variable='Wmass',
                        #formula='W_mass',
                        formula='transverseMass(lepton1_pt,lepton1_phi,met_pt,met_phi)',
                        labelX='mass [GeV]',
                        bins = array('d',range(0,201,5)),  
                        ),
                

    }



