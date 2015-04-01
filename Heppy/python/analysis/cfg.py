from setup import Configuration
cfg=Configuration()
from observables import Observable

cfg.parametersSet['region'] = 'SR'
cfg.parametersSet['observable'] = 'met'
#cfg.parametersSet['observable'] = Observable(variable='ZpT',formula='Z_pt',labelX='Z p_{T} [GeV]')
cfg.parametersSet['selection'] = 'baseline'
