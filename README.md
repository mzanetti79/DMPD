# DMPD
DM analysis framework of the CMS PD group

## Manual changes to Heppy
###TauAnalyzer.py
replace tau.tauID(self.cfg_ana.loose_tauID) with tau.tauID(self.cfg_ana.loose_tauID) < self.cfg_ana.loose_tauIDnHits (L89, 108)
add loose_tauIDnHits = 0, argument (L166)

###PhotonAnalyzer.py
set EffectiveArea03[2] to 0.078, 0.0629, 0.0264, 0.0462, 0.0740, 0.0924, 0.1484
###Photon.py
set "conversionVeto": [False,False]
