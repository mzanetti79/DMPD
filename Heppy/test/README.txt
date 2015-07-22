(1) 
edit `PhysicsTools/Heppy/python/analyzers/gen/GeneratorAnalyzer.py`
adding the line:
`self.cfg_comp.isMC         = True`
right after 
`super(GeneratorAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)`
(within `    def __init__(self, cfg_ana, cfg_comp, looperName ):`)
 
