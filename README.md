# DMPD
DM analysis framework of the CMS PD group

## Manual changes to Heppy for Syncronization
###TauAnalyzer.py
replace tau.tauID(self.cfg_ana.loose_tauID) with tau.tauID(self.cfg_ana.loose_tauID) < self.cfg_ana.loose_tauIDnHits (L89, 108)
add loose_tauIDnHits = 0, argument (L166)

###PhotonAnalyzer.py
set EffectiveArea03[2] to 0.0896, 0.0762, 0.0383, 0.0534, 0.0846, 0.1032, 0.1598
###Photon.py
set "conversionVeto": [False,False]
