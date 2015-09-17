# DMPD
DM analysis framework of the CMS PD group
 
## Manual changes to Heppy for Syncronization

### TauAnalyzer.py
[PhysicsTools/Heppy/python/analyzers/objects/TauAnalyzer.py]

L89 REPLACE 
```python
tau.tauID(self.cfg_ana.inclusive_tauID)
```
WITH 
```python
tau.tauID(self.cfg_ana.inclusive_tauID) < self.cfg_ana.inclusive_tauIDnHits
```

L108 REPLACE 
```python
tau.tauID(self.cfg_ana.loose_tauID)
```
WITH 
```python
tau.tauID(self.cfg_ana.loose_tauID) < self.cfg_ana.loose_tauIDnHits
```

L145-170 ADD
```python
inclusive_tauIDnHits = 0,
loose_tauIDnHits = 0,
```
### PhotonAnalyzer.py
[PhysicsTools/Heppy/python/analyzers/objects/PhotonAnalyzer.py]

L76-82 SOBSTITUTE WITH
```python
if   abs(gamma.eta()) < 1.0:   gamma.EffectiveArea03 = [ 0.0234, 0.0053, 0.0896 ]
elif abs(gamma.eta()) < 1.479: gamma.EffectiveArea03 = [ 0.0189, 0.0103, 0.0762 ]
elif abs(gamma.eta()) < 2.0:   gamma.EffectiveArea03 = [ 0.0171, 0.0057, 0.0383 ]
elif abs(gamma.eta()) < 2.2:   gamma.EffectiveArea03 = [ 0.0129, 0.0070, 0.0534 ]
elif abs(gamma.eta()) < 2.3:   gamma.EffectiveArea03 = [ 0.0110, 0.0152, 0.0846 ]
elif abs(gamma.eta()) < 2.4:   gamma.EffectiveArea03 = [ 0.0074, 0.0232, 0.1032 ]
else:                          gamma.EffectiveArea03 = [ 0.0035, 0.1709, 0.1598 ]
```

### JetAnalyzer.py
[PhysicsTools/Heppy/python/analyzers/objects/JetAnalyzer.py]

L123-124 MODIFY
```python
if self.cfg_ana.do_mc_match:
  self.matchJets(event, allJets)
```
WITH
```python
self.matchJets(event, allJets)
```
L236-237 MODIFY
```python
if self.cfg_ana.do_mc_match:
  self.jetFlavour(event)
```
WITH
```python
self.jetFlavour(event)
```

L260-264 MODIFY
```if self.cfg_ana.do_mc_match:
  setattr(event,"bqObjects"              +self.cfg_ana.collectionPostFix, self.bqObjects              )
  setattr(event,"cqObjects"              +self.cfg_ana.collectionPostFix, self.cqObjects              )
  setattr(event,"partons"                +self.cfg_ana.collectionPostFix, self.partons                )
  setattr(event,"heaviestQCDFlavour"     +self.cfg_ana.collectionPostFix, self.heaviestQCDFlavour     )
```
WITH
```setattr(event,"bqObjects"              +self.cfg_ana.collectionPostFix, self.bqObjects              )
setattr(event,"cqObjects"              +self.cfg_ana.collectionPostFix, self.cqObjects              )
setattr(event,"partons"                +self.cfg_ana.collectionPostFix, self.partons                )
setattr(event,"heaviestQCDFlavour"     +self.cfg_ana.collectionPostFix, self.heaviestQCDFlavour     )
```

### Photon.py
[PhysicsTools/Heppy/python/physicsobjects/Photon.py]

FIND AND REPLACE
```conversionVeto": [True,True]
```
WITH
```conversionVeto": [False,False]
```