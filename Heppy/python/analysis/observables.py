from array import array

momentum_bins=range(200,331,10)+[350, 380, 430, 500, 1000]

class Observable():
    def __init__(self,**k):
        # defaults
        self.variable='met' 
        self.formula=self.variable 
        self.bins = array('d',sorted(momentum_bins)) 
        self.labelX = self.variable
        self.labelY = 'events / GeV'
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
    'metPhi':Observable(variable='metPhi',
                        formula='met_phi',
                        labelX='E_{T}^{miss} #phi',
                        ),
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
               }



