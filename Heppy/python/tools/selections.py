#! /usr/bin/env python

selection = {
    "monoX" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && jet1_pt>110 && abs(jet1_dPhi_met)>2 && jet1_chf > 0.2 && jet1_nhf < 0.7 && jet1_phf < 0.7 && (nJets==1 || (nJets==2 && jet2_nhf < 0.7 && jet2_phf < 0.9 && abs(jet2_dPhi_jet1) < 2.5)) && nElectrons==0 && nTaus==0 && nPhotons==0",
    "monoB" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && jet1_pt>50 && jet1_chf>0.2 && jet1_nhf<0.7 && jet1_phf<0.7 && jet1_CSV>0.890 && ((nJets==1 && abs(jet1_dPhi_met)>2) || (nJets==2 && jet2_nhf<0.7 && jet2_phf<0.9 && abs(jet2_dPhi_jet1)<2.5 && jet2_CSV>0.890)) && nElectrons==0 && nTaus==0", # && abs(H_dPhi_met)>2
    "hfDM1" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && jet1_pt>50 && jet1_chf>0.2 && jet1_nhf<0.7 && jet1_phf<0.7 && jet1_dPhi_met>2 && ((nJets==1 && jet1_CSV>0.890) || (nJets==2 && jet2_dPhi_met>2 && ((jet1_CSV>0.890)+(jet2_CSV>0.890) == 1))) && nElectrons==0",
    "hfDM2" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && jet1_pt>50 && jet1_chf>0.2 && jet1_nhf<0.7 && jet1_phf<0.7 && jet1_dPhi_met>2 && jet2_pt>50 && jet2_dPhi_met>2 && ( (nJets==2 && ((jet1_CSV>0.890)+(jet2_CSV>0.890) == 2)) || (nJets==3 && jet3_dPhi_met>2 && ((jet1_CSV>0.890)+(jet2_CSV>0.890)+(jet3_CSV>0.890) == 2)) ) && nElectrons==0",
    #"Wmbb" : "HLT_BIT_HLT_IsoMu27_v && nMuons==1 && lepton1_isMuon && lepton1_tightId && lepton1_pt>30 && abs(lepton1_eta)<2.1 && lepton1_relIso04<0.12 && jet1_flavour<4",
    # Muon Control Regions
    "Wmnu" : "HLT_BIT_HLT_IsoMu27_v && nMuons==1 && lepton1_isMuon && lepton1_tightId && lepton1_pt>30 && abs(lepton1_eta)<2.1 && lepton1_relIso04<0.12 && W_tmass>50 && W_tmass<100",
    "WmCR" : "HLT_BIT_HLT_IsoMu27_v && nMuons==1 && lepton1_isMuon && lepton1_tightId && lepton1_pt>30 && abs(lepton1_eta)<2.1 && lepton1_relIso04<0.12 && W_tmass>50 && W_tmass<100 && fakemet_pt>200 && jet1_pt>50 && jet1_chf>0.2 && jet1_nhf<0.7 && jet1_phf<0.7 && jet1_dPhi_met>2 && ((nJets==1) || (nJets==2 && jet2_dPhi_met>2)) && nElectrons==0",
    "Zmumu" : "HLT_BIT_HLT_IsoMu27_v && lepton1_isMuon && lepton1_tightId && lepton1_pt>20 && lepton1_relIso04<0.12 && lepton2_isMuon && lepton2_pt>15 && Z_mass>70 && Z_mass<110",
    "ZmmCR" : "HLT_BIT_HLT_IsoMu27_v && lepton1_isMuon && lepton1_tightId && lepton1_pt>20 && lepton1_relIso04<0.12 && lepton2_isMuon && lepton2_pt>15 && Z_mass>70 && Z_mass<110 && fakemet_pt>200 && jet1_pt>50 && jet1_chf>0.2 && jet1_nhf<0.7 && jet1_phf<0.7 && jet1_dPhi_met>2 && ((nJets==1) || (nJets==2 && jet2_dPhi_met>2)) && nElectrons==0",
    "Temu" : "HLT_BIT_HLT_IsoMu27_v && lepton1_isMuon!=lepton2_isMuon && lepton1_pt>30 && lepton2_pt>30 && lepton1_tightId && (lepton1_isElectron || lepton1_relIso04<0.12)",
    "TemCR" : "HLT_BIT_HLT_IsoMu27_v && lepton1_isMuon!=lepton2_isMuon && lepton1_pt>30 && lepton2_pt>30 && lepton1_tightId && (lepton1_isElectron || lepton1_relIso04<0.12) && jet1_pt>50 && jet1_chf>0.2 && jet1_nhf<0.7 && jet1_phf<0.7 && jet1_dPhi_met>2 && ((nJets==1) || (nJets==2 && jet2_dPhi_met>2))",
    # Electron Control Regions
    "Wenu" : "HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && nElectrons==1 && lepton1_isElectron && lepton1_tightId && lepton1_pt>110 && abs(lepton1_eta)<2.1 && W_tmass>50 && W_tmass<100",
    "Zee" : "HLT_BIT_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v && lepton1_isElectron && lepton1_tightId && lepton1_pt>30 && abs(lepton1_eta)<2.1 && lepton2_pt>20 && Z_mass>70 && Z_mass<110",
    "Zll" : "(HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v || HLT_BIT_HLT_IsoMu27_v) && lepton1_tightId && (lepton1_isElectron || lepton1_relIso04<0.12) && lepton1_pt>25 && lepton2_pt>20 && Z_mass>70 && Z_mass<110",
    # XZh preselections
    "preEle" : "HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && isZtoEE && lepton1_pt>115 && lepton2_pt>35 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1",
    "preMuo" : "HLT_BIT_HLT_Mu45_eta2p1_v && isZtoMM && (lepton1_highptId || lepton2_highptId) && lepton1_pt>50 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1",
    "preLep" : "(HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && isZtoEE && lepton1_pt>115 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1) || (HLT_BIT_HLT_Mu45_eta2p1_v && isZtoMM && (lepton1_highptId || lepton2_highptId) && lepton1_pt>50 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1)",
    "preNeu" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && fatjet1_pt>200 && fatjet1_chf>0.2 && fatjet1_nhf<0.7 && fatjet1_phf<0.7 && fatjet1_dPhi_met>2 && nFatJets==1 && nMuons==0 && nElectrons==0 && jet2_dPhi_jet1<0.8 && nJets<=2",
    # XZh
    "Zcut" : "Z_pt>200 && Z_mass>70 && Z_mass<110",
    "Hcut" : "fatjet1_pt>200 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145)",
    "antiHcut" : "fatjet1_pt>200 && fatjet1_prunedMassCorr>30 && (fatjet1_prunedMassCorr<65 || fatjet1_prunedMassCorr>145)",
    "Bcut" : "(fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
    "XZheebb" : "HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && isZtoEE && lepton1_pt>115 && lepton2_pt>35 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1 && Z_pt>200 && Z_mass>70 && Z_mass<110 && fatjet1_pt>200 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145) && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
    "XZhmmbb" : "HLT_BIT_HLT_Mu45_eta2p1_v && isZtoMM && (lepton1_highptId || lepton2_highptId) && lepton1_pt>50 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1 && Z_pt>200 && Z_mass>70 && Z_mass<110 && fatjet1_pt>200 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145) && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
    "XZhnnbb" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && fatjet1_pt>200 && fatjet1_chf>0.2 && fatjet1_nhf<0.7 && fatjet1_phf<0.7 && fatjet1_dPhi_met>2 && nFatJets==1 && nMuons==0 && nElectrons==0 && jet2_dPhi_jet1<2 && nJets<=2 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145) && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
}
