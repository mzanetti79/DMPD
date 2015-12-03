#! /usr/bin/env python

selection = {
    # triggers
    "triggerMET" : "( HLT_BIT_HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v || HLT_BIT_HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v || HLT_BIT_HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v || HLT_BIT_HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v || HLT_BIT_HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v || HLT_BIT_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v )",
    "triggerEle" : "( HLT_BIT_HLT_Ele27_WPLoose_Gsf_v || HLT_BIT_HLT_Ele27_WP85_Gsf_v )",
    "triggerMuo" : "( HLT_BIT_HLT_IsoMu20_v )",
    # Cat
    "cat1" : "( jet1_pt>50 && jet1_chf>0.1 && jet1_nhf<0.8 && ( ( nJets==1 && jet1_CSVR>0.890 ) || ( nJets==2 && ( ( jet1_CSVR>0.890 ) + ( jet2_CSVR>0.890 ) )==1 ) ) ) && nTaus==0 && nPhotons==0",
    "cat2" : "( jet1_pt>50 && jet1_chf>0.1 && jet1_nhf<0.8 && jet2_pt>50 && ( ( nJets==2 && ( ( jet1_CSVR>0.890 ) + ( jet2_CSVR>0.890 ) )==2 ) || ( nJets==3 && ( ( jet1_CSVR>0.890 ) + ( jet2_CSVR>0.890 ) + ( jet3_CSVR>0.890 ) )==2  ) ) ) && nTaus==0 && nPhotons==0",
    # SR
    "SR1" : "triggerMET && nElectrons==0 && nMuons==0 && cormet_pt>200 && minDeltaPhi>0.5 && cat1",
    "SR2" : "triggerMET && nElectrons==0 && nMuons==0 && cormet_pt>200 && minDeltaPhi>0.5 && cat2",
    "SR"  : "triggerMET && nElectrons==0 && nMuons==0 && cormet_pt>200 && minDeltaPhi>0.5 && (cat1 || cat2)",
    # W
    "WeInc" : "triggerEle && nElectrons==1 && lepton1_isElectron && lepton1_tightId && lepton1_pt>30 && W_tmass>50",
    "WmInc" : "triggerMuo && nMuons==1 && lepton1_isMuon && lepton1_tightId && lepton1_pt>30 && lepton1_relIso04<0.15 && W_tmass>50",
    "WeCR" : "WeInc && W_tmass<160 && fakecormet_pt>200 && (cat1 || cat2)",
    "WmCR" : "WmInc && W_tmass<160 && fakecormet_pt>200 && (cat1 || cat2)",
    "WebCR" : "WeInc && W_tmass<160 && fakecormet_pt>200 && cat1",
    "WmbCR" : "WmInc && W_tmass<160 && fakecormet_pt>200 && cat1",
    "WebbCR" : "WeInc && W_tmass<160 && fakecormet_pt>200 && cat2",
    "WmbbCR" : "WmInc && W_tmass<160 && fakecormet_pt>200 && cat2",
    # Z
    "ZeeInc" : "triggerEle && isZtoEE && lepton1_tightId && lepton1_pt>30 && lepton2_looseId && lepton2_pt>10 && Z_mass>70 && Z_mass<110",
    "ZmmInc" : "triggerMuo && isZtoMM && lepton1_tightId && lepton1_pt>30 && lepton1_relIso04<0.15 && lepton2_looseId && lepton2_pt>10 && lepton2_relIso04<0.25 && Z_mass>70 && Z_mass<110",
    "ZeeCR" : "ZeeInc && fakecormet_pt>200 && (cat1 || cat2) && lepton2_pt>30",
    "ZmmCR" : "ZmmInc && fakecormet_pt>200 && (cat1 || cat2)",
    "ZeebCR" : "ZeeInc && fakecormet_pt>200 && cat1 && lepton2_pt>30",
    "ZmmbCR" : "ZmmInc && fakecormet_pt>200 && cat1",
    "ZeebbCR" : "ZeeInc && fakecormet_pt>200 && cat2 && lepton2_pt>30",
    "ZmmbbCR" : "ZmmInc && fakecormet_pt>200 && cat2",
    # T
    "TInc" : "triggerMuo && lepton1_isMuon!=lepton2_isMuon && lepton1_pt>30 && lepton2_pt>30 && lepton1_tightId && lepton2_tightId && (lepton1_isMuon ? lepton1_relIso04<0.15 : lepton2_relIso04<0.15)",
    "TCR" : "TInc && fakecormet_pt>200 && (cat1 || cat2)",
    "TbCR" : "TInc && fakecormet_pt>200 && cat1",
    "TbbCR" : "TInc && fakecormet_pt>200 && cat2",
    # Other
    "QCDCR" : "triggerMET && nElectrons==0 && nMuons==0 && cormet_pt>200 && minDeltaPhi<0.5 && (cat1 || cat2)",
    "monoX" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && jet1_pt>110 && abs(jet1_dPhi_met)>2 && jet1_chf > 0.2 && jet1_nhf < 0.7 && jet1_phf < 0.7 && (nJets==1 || (nJets==2 && jet2_nhf < 0.7 && jet2_phf < 0.9 && abs(jet2_dPhi_jet1) < 2.5)) && nElectrons==0 && nTaus==0 && nPhotons==0",
    "monoB" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && jet1_pt>50 && jet1_chf>0.1 && jet1_nhf<0.8 && jet1_CSVR>0.890 && ((nJets==1 && abs(jet1_dPhi_met)>2) || (nJets==2 && jet2_nhf<0.7 && jet2_phf<0.9 && abs(jet2_dPhi_jet1)<2.5 && jet2_CSVR>0.890)) && nElectrons==0 && nMuons==0 && nTaus==0", # && abs(H_dPhi_met)>2
    
    # XZh preselections
    "preEle" : "HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && isZtoEE && lepton1_pt>115 && lepton2_pt>35 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1",
    "preMuo" : "HLT_BIT_HLT_Mu45_eta2p1_v && isZtoMM && (lepton1_highptId || lepton2_highptId) && lepton1_pt>50 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1",
    "preLep" : "(HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && isZtoEE && lepton1_pt>115 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1) || (HLT_BIT_HLT_Mu45_eta2p1_v && isZtoMM && (lepton1_highptId || lepton2_highptId) && lepton1_pt>50 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1)",
    "preNeu" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && fatjet1_pt>200 && fatjet1_chf>0.1 && fatjet1_nhf<0.8",
    # XZh
    "Zcut" : "Z_pt>200 && Z_mass>70 && Z_mass<110",
    "Hcut" : "fatjet1_pt>200 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145)",
    "Hanticut" : "fatjet1_pt>200 && fatjet1_prunedMassCorr>30 && (fatjet1_prunedMassCorr<65 || fatjet1_prunedMassCorr>145)",
    "Bcut" : "(fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
    "XZheebb" : "preEle && Zcut && Hcut && Bcut",
    "XZhmmbb" : "preMuo && Zcut && Hcut && Bcut",
    "XZhnnbb" : "preNeu && Hcut && Bcut && fatjet1_dPhi_met>2 && nFatJets==1 && nMuons==0 && nElectrons==0",
    "XZheebbNoHm" : "preEle && Zcut && fatjet1_pt>200 && Bcut",
    "XZhmmbbNoHm" : "preMuo && Zcut && fatjet1_pt>200 && Bcut",
}

selection_tau = {
    # triggers
    "triggerMET" : "( HLT_BIT_HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v || HLT_BIT_HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v || HLT_BIT_HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v || HLT_BIT_HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v || HLT_BIT_HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v || HLT_BIT_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v )",
    "triggerEle" : "( HLT_BIT_HLT_Ele27_WPLoose_Gsf_v || HLT_BIT_HLT_Ele27_WP85_Gsf_v )",
    "triggerMuo" : "( HLT_BIT_HLT_IsoMu20_v )",
    # Cat
    "cat1" : "( jet1_pt>50 && jet1_chf>0.1 && jet1_nhf<0.8 && ( ( nJets==1 && jet1_CSV>0.890 ) || ( nJets==2 && ( ( jet1_CSV>0.890 ) + ( jet2_CSV>0.890 ) )==1 ) ) ) && nTaus==0 && nPhotons==0",
    "cat2" : "( jet1_pt>50 && jet1_chf>0.1 && jet1_nhf<0.8 && jet2_pt>50 && ( ( nJets==2 && ( ( jet1_CSV>0.890 ) + ( jet2_CSV>0.890 ) )==2 ) || ( nJets==3 && ( ( jet1_CSV>0.890 ) + ( jet2_CSV>0.890 ) + ( jet3_CSV>0.890 ) )==2  ) ) ) && nTaus==0 && nPhotons==0",
    # SR
    "SR1" : "triggerMET && nElectrons==0 && nMuons==0 && cormet_pt>200 && minDeltaPhi>0.5 && cat1",
    "SR2" : "triggerMET && nElectrons==0 && nMuons==0 && cormet_pt>200 && minDeltaPhi>0.5 && cat2",
    "SR"  : "triggerMET && nElectrons==0 && nMuons==0 && cormet_pt>200 && minDeltaPhi>0.5 && (cat1 || cat2)",
    # W
    "WeInc" : "triggerEle && nElectrons==1 && lepton1_isElectron && lepton1_tightId && lepton1_pt>30 && W_tmass>50",
    "WmInc" : "triggerMuo && nMuons==1 && lepton1_isMuon && lepton1_tightId && lepton1_pt>30 && lepton1_relIso04<0.15 && W_tmass>50",
    "WeCR" : "WeInc && W_tmass<160 && fakecormet_pt>200 && (cat1 || cat2)",
    "WmCR" : "WmInc && W_tmass<160 && fakecormet_pt>200 && (cat1 || cat2)",
    "WebCR" : "WeInc && W_tmass<160 && fakecormet_pt>200 && cat1",
    "WmbCR" : "WmInc && W_tmass<160 && fakecormet_pt>200 && cat1",
    "WebbCR" : "WeInc && W_tmass<160 && fakecormet_pt>200 && cat2",
    "WmbbCR" : "WmInc && W_tmass<160 && fakecormet_pt>200 && cat2",
    # Z
    "ZeeInc" : "triggerEle && isZtoEE && lepton1_tightId && lepton1_pt>30 && lepton2_looseId && lepton2_pt>10 && Z_mass>70 && Z_mass<110",
    "ZmmInc" : "triggerMuo && isZtoMM && lepton1_tightId && lepton1_pt>30 && lepton1_relIso04<0.15 && lepton2_looseId && lepton2_pt>10 && lepton2_relIso04<0.25 && Z_mass>70 && Z_mass<110",
    "ZeeCR" : "ZeeInc && fakecormet_pt>200 && (cat1 || cat2) && lepton2_pt>30",
    "ZmmCR" : "ZmmInc && fakecormet_pt>200 && (cat1 || cat2)",
    "ZeebCR" : "ZeeInc && fakecormet_pt>200 && cat1 && lepton2_pt>30",
    "ZmmbCR" : "ZmmInc && fakecormet_pt>200 && cat1",
    "ZeebbCR" : "ZeeInc && fakecormet_pt>200 && cat2 && lepton2_pt>30",
    "ZmmbbCR" : "ZmmInc && fakecormet_pt>200 && cat2",
    # T
    "TInc" : "triggerMuo && lepton1_isMuon!=lepton2_isMuon && lepton1_pt>30 && lepton2_pt>30 && lepton1_tightId && lepton2_tightId && (lepton1_isMuon ? lepton1_relIso04<0.15 : lepton2_relIso04<0.15)",
    "TCR" : "TInc && fakecormet_pt>200 && (cat1 || cat2)",
    "TbCR" : "TInc && fakecormet_pt>200 && cat1",
    "TbbCR" : "TInc && fakecormet_pt>200 && cat2",
    # Other
    "QCDCR" : "triggerMET && nElectrons==0 && nMuons==0 && cormet_pt>200 && minDeltaPhi<0.5 && (cat1 || cat2)",
    "monoX" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && jet1_pt>110 && abs(jet1_dPhi_met)>2 && jet1_chf > 0.2 && jet1_nhf < 0.7 && jet1_phf < 0.7 && (nJets==1 || (nJets==2 && jet2_nhf < 0.7 && jet2_phf < 0.9 && abs(jet2_dPhi_jet1) < 2.5)) && nElectrons==0 && nTaus==0 && nPhotons==0",
    "monoB" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && jet1_pt>50 && jet1_chf>0.1 && jet1_nhf<0.8 && jet1_CSV>0.890 && ((nJets==1 && abs(jet1_dPhi_met)>2) || (nJets==2 && jet2_nhf<0.7 && jet2_phf<0.9 && abs(jet2_dPhi_jet1)<2.5 && jet2_CSV>0.890)) && nElectrons==0 && nMuons==0 && nTaus==0", # && abs(H_dPhi_met)>2
    
    # XZh preselections
    "preEle" : "HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && isZtoEE && lepton1_pt>115 && lepton2_pt>35 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1",
    "preMuo" : "HLT_BIT_HLT_Mu45_eta2p1_v && isZtoMM && (lepton1_highptId || lepton2_highptId) && lepton1_pt>50 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1",
    "preLep" : "(HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && isZtoEE && lepton1_pt>115 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1) || (HLT_BIT_HLT_Mu45_eta2p1_v && isZtoMM && (lepton1_highptId || lepton2_highptId) && lepton1_pt>50 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1)",
    "preNeu" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && fatjet1_pt>200 && fatjet1_chf>0.1 && fatjet1_nhf<0.8 && fatjet1_dPhi_met>2 && nFatJets==1 && nMuons==0 && nElectrons==0 && jet2_dPhi_jet1<0.8 && nJets<=2",
    # XZh
    "Zcut" : "Z_pt>200 && Z_mass>70 && Z_mass<110",
    "Hcut" : "fatjet1_pt>200 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145)",
    "antiHcut" : "fatjet1_pt>200 && fatjet1_prunedMassCorr>30 && (fatjet1_prunedMassCorr<65 || fatjet1_prunedMassCorr>145)",
    "Bcut" : "(fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
    "XZheebb" : "HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v && isZtoEE && lepton1_pt>115 && lepton2_pt>35 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1 && Z_pt>200 && Z_mass>70 && Z_mass<110 && fatjet1_pt>200 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145) && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
    "XZhmmbb" : "HLT_BIT_HLT_Mu45_eta2p1_v && isZtoMM && (lepton1_highptId || lepton2_highptId) && lepton1_pt>50 && lepton2_pt>20 && lepton1_miniIso<0.1 && lepton2_miniIso<0.1 && Z_pt>200 && Z_mass>70 && Z_mass<110 && fatjet1_pt>200 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145) && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
    "XZhnnbb" : "HLT_BIT_HLT_PFMET170_NoiseCleaned_v && met_pt>200 && fatjet1_pt>200 && fatjet1_chf>0.1 && fatjet1_nhf<0.8 && fatjet1_dPhi_met>2 && nFatJets==1 && nMuons==0 && nElectrons==0 && jet2_dPhi_jet1<2 && nJets<=2 && (fatjet1_prunedMassCorr>105 && fatjet1_prunedMassCorr<145) && (fatjet1_dR>0.3 ? fatjet1_CSV1>0.605 && fatjet1_CSV2>0.605 : fatjet1_CSV1>0.605 || fatjet1_CSV2>0.605)",
}
