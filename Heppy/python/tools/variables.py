
variable = {}

var_template = {
    # Event
    "rho": {
      "title" : "rho",
      "nbins" : 50,
      "min" : 0,
      "max" : 50,
      "log" : False,
    },
    "nPV": {
      "title" : "number of reconstructed Primary Vertices",
      "nbins" : 40,
      "min" : -0.5,
      "max" : 39.5,
      "log" : False,
    },
    "nMuons": {
      "title" : "number of muons",
      "nbins" : 5,
      "min" : -0.5,
      "max" : 4.5,
      "log" : True,
    },
    "nElectrons": {
      "title" : "number of electrons",
      "nbins" : 5,
      "min" : -0.5,
      "max" : 4.5,
      "log" : True,
    },
    "nTaus": {
      "title" : "number of taus",
      "nbins" : 5,
      "min" : -0.5,
      "max" : 4.5,
      "log" : True,
    },
    "nPhotons": {
      "title" : "number of photons",
      "nbins" : 5,
      "min" : -0.5,
      "max" : 4.5,
      "log" : True,
    },
    "nJets": {
      "title" : "number of jets",
      "nbins" : 10,
      "min" : -0.5,
      "max" : 9.5,
      "log" : True,
    },
    "nFatJets": {
      "title" : "number of AK8 jets",
      "nbins" : 5,
      "min" : 0.5,
      "max" : 5.5,
      "log" : True,
    },
    "nBJets": {
      "title" : "number of b-jets",
      "nbins" : 5,
      "min" : -0.5,
      "max" : 4.5,
      "log" : True,
    },
    "nBtagJets": {
      "title" : "number of b-jets",
      "nbins" : 5,
      "min" : -0.5,
      "max" : 4.5,
      "log" : True,
    },
    "eventWeight": {
      "title" : "event weight",
      "nbins" : 100,
      "min" : -1,
      "max" : 1,
      "log" : False,
    },
    "genNl": {
      "title" : "number of leptons at generation level",
      "nbins" : 4,
      "min" : -0.5,
      "max" : 3.5,
      "log" : True,
    },
    
    
    # MET
    "met_pt": {
      "title" : "#slash{E}_{T} (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 0,
      "max" : 0,
      "log" : True,
    },
    "met_pt": {
      "title" : "#slash{E}_{T} (GeV)",
      "nbins" : 10,
      "min" : 200,
      "max" : 1200,
      "log" : True,
    },
#    "met_pt": {
#      "title" : "#slash{E}_{T} (GeV)",
#      "nbins" : 100,
#      "min" : 0,
#      "max" : 400,
#      "log" : True,
#    },
    "met_phi": {
      "title" : "#slash{E}_{T} #varphi",
      "nbins" : 50,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "met_ptRaw": {
      "title" : "raw #slash{E}_{T} (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 200,
      "max" : 1000,
      "log" : True,
    },
    "cormet_pt": {
      "title" : "#slash{E}_{T} (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 200,
      "max" : 1000,
      "log" : True,
    },
    "cormet_ptScaleUp": {
      "title" : "#slash{E}_{T} (scale up) (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 200,
      "max" : 1000,
      "log" : True,
    },
    "cormet_ptScaleDown": {
      "title" : "#slash{E}_{T} (scale down) (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 200,
      "max" : 1000,
      "log" : True,
    },
    "cormet_ptResUp": {
      "title" : "#slash{E}_{T} (resolution up) (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 200,
      "max" : 1000,
      "log" : True,
    },
    "cormet_ptResDown": {
      "title" : "#slash{E}_{T} (resolution Down) (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 200,
      "max" : 1000,
      "log" : True,
    },
    "fakemet_pt": {
      "title" : "hadronic recoil (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 200,
      "max" : 1000,
      "log" : True,
    },
    "fakemet_phi": {
      "title" : "hadronic recoil #varphi",
      "nbins" : 50,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "fakecormet_pt": {
      "title" : "hadronic recoil (GeV)",
      "nbins" : -1,
      "bins" : [200, 300, 400, 500, 700, 1000],
      "min" : 200,
      "max" : 1000,
      "log" : True,
    },
    "fakecormet_phi": {
      "title" : "hadronic recoil #varphi",
      "nbins" : 50,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "HT": {
      "title" : "HT (GeV)",
      "nbins" : 100,
      "min" : 0,
      "max" : 1000,
      "log" : True,
    },
    "nJetsNoFatJet150": {
      "title" : "number of jets with p_{T}>150 GeV",
      "nbins" : 10,
      "min" : 0,
      "max" : 10,
      "log" : True,
    },
    "nJetsNoFatJet100": {
      "title" : "number of jets with p_{T}>100 GeV",
      "nbins" : 10,
      "min" : 0,
      "max" : 10,
      "log" : True,
    },
    "nJetsNoFatJet50": {
      "title" : "number of jets with p_{T}>50 GeV",
      "nbins" : 10,
      "min" : 0,
      "max" : 10,
      "log" : True,
    },
    "nJetsNoFatJet30": {
      "title" : "number of jets with p_{T}>30 GeV",
      "nbins" : 10,
      "min" : 0,
      "max" : 10,
      "log" : True,
    },
    "maxCSVNoFatJet": {
      "title" : "max CSV, fat jet excluded",
      "nbins" : 25,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "minDeltaPhi": {
      "title" : "min #Delta #varphi (jet-#slash{E}_{T})",
      "nbins" : 28,
      "min" : 0,
      "max" : 3.15,
      "log" : True,
    },
    "minDeltaPhiNoFatJet": {
      "title" : "min #Delta #varphi (jet-#slash{E}_{T})",
      "nbins" : 28,
      "min" : 0,
      "max" : 3.15,
      "log" : True,
    },
    
    # Jets
    "jet[N]_pt": {
      "title" : "jet [N] p_{T} (GeV)",
      "nbins" : 40,
      "min" : 0,
      "max" : 800,
      "log" : True,
    },
    "jet[N]_eta": {
      "title" : "jet [N] #eta",
      "nbins" : 30,
      "min" : -3,
      "max" : 3,
      "log" : False,
    },
    "jet[N]_phi": {
      "title" : "jet [N] #varphi",
      "nbins" : 60,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "jet[N]_mass": {
      "title" : "jet [N] mass (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 150,
      "log" : False,
    },
    "jet[N]_dPhi_met": {
      "title" : "#Delta #varphi  jet[N]-#slash{E}_{T}",
      "nbins" : 14,
      "min" : 0,
      "max" : 3.15,
      "log" : False,
    },
    "jet[N]_dPhi_jet1": {
      "title" : "#Delta #varphi  jet[N]-jet1",
      "nbins" : 14,
      "min" : 0,
      "max" : 3.15,
      "log" : False,
    },
    "jet[N]_CSV": {
      "title" : "jet [N] CSV",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_CSVR": {
      "title" : "jet [N] CSV",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_CSVRUp": {
      "title" : "jet [N] CSV (+1 #sigma)",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_CSVRDown": {
      "title" : "jet [N] CSV (-1 #sigma)",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_flavour": {
      "title" : "jet [N] flavour",
      "nbins" : 25,
      "min" : -0.5,
      "max" : 24.5,
      "log" : False,
    },
    "jet[N]_chf": {
      "title" : "jet [N] charged hadron fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_nhf": {
      "title" : "jet [N] neutral hadron fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_phf": {
      "title" : "jet [N] photon fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_elf": {
      "title" : "jet [N] electron fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_muf": {
      "title" : "jet [N] muon fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "jet[N]_chm": {
      "title" : "jet [N] charged multiplicity",
      "nbins" : 20,
      "min" : 0,
      "max" : 50,
      "log" : False,
    },
    "jet[N]_npr": {
      "title" : "jet [N] constituents multiplicity",
      "nbins" : 50,
      "min" : 0,
      "max" : 50,
      "log" : False,
    },
    
    # bjet
    "bjet1_pt": {
      "title" : "highest CSV jet p_{T} (GeV)",
      "nbins" : 40,
      "min" : 0,
      "max" : 800,
      "log" : True,
    },
    "bjet1_eta": {
      "title" : "highest CSV jet #eta",
      "nbins" : 30,
      "min" : -3,
      "max" : 3,
      "log" : False,
    },
    "bjet1_phi": {
      "title" : "highest CSV jet #varphi",
      "nbins" : 60,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "bjet1_mass": {
      "title" : "highest CSV jet mass (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 150,
      "log" : False,
    },
    "bjet1_CSV": {
      "title" : "highest CSV in the event, AK8 jet excluded",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "bjet1_CSVR": {
      "title" : "highest CSV in the event, AK8 jet excluded",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "bjet1_CSVRUp": {
      "title" : "highest CSV in the event, AK8 jet excluded (+1 #sigma)",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "bjet1_CSVRDown": {
      "title" : "highest CSV in the event, AK8 jet excluded (-1 #sigma)",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "bjet1_flavour": {
      "title" : "jet flavour of the highest CSV in the event, AK8 jet excluded",
      "nbins" : 25,
      "min" : -0.5,
      "max" : 24.5,
      "log" : False,
    },
    
    # Fatjets
    "fatjet[N]_pt": {
      "title" : "jet [N] p_{T} (GeV)",
      "nbins" : 18,
      "min" : 200,
      "max" : 2000,
      "log" : True,
    },
    "fatjet[N]_eta": {
      "title" : "jet [N] #eta",
      "nbins" : 30,
      "min" : -3,
      "max" : 3,
      "log" : False,
    },
    "fatjet[N]_phi": {
      "title" : "jet [N] #varphi",
      "nbins" : 60,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "fatjet[N]_mass": {
      "title" : "jet [N] mass (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 150,
      "log" : False,
    },
    "fatjet[N]_prunedMass": {
      "title" : "pruned mass (GeV)",
      "nbins" : 60,
      "min" : 0,
      "max" : 300,
      "log" : False,
    },
    "fatjet[N]_prunedMassCorr": {
      "title" : "corrected pruned mass (GeV)",
      "nbins" : 60,
      "min" : 0,
      "max" : 300,
      "log" : True,
    },
    "fatjet[N]_softdropMass": {
      "title" : "soft drop mass (GeV)",
      "nbins" : 20,
      "min" : 0.,
      "max" : 200.,
      "log" : False,
    },
    "fatjet[N]_softdropMassCorr": {
      "title" : "corrected soft drop mass (GeV)",
      "nbins" : 20,
      "min" : 0.,
      "max" : 200.,
      "log" : False,
    },
    "fatjet[N]_trimmedMass": {
      "title" : "trimmed mass (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 200,
      "log" : False,
    },
    "fatjet[N]_filteredMass": {
      "title" : "filtered mass (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 200,
      "log" : False,
    },
    "fatjet[N]_dR": {
      "title" : "subjets #Delta R",
      "nbins" : 20,
      "min" : 0,
      "max" : 1.,
      "log" : False,
    },
    "fatjet[N]_dPhi_met": {
      "title" : "#Delta #varphi (jet-#slash{E}_{T})",
      "nbins" : 50,
      "min" : 0,
      "max" : 3.15,
      "log" : False,
    },
    "fatjet[N]_tau21": {
      "title" : "#tau_{2} / #tau_{1}",
      "nbins" : 25,
      "min" : 0,
      "max" : 1.,
      "log" : False,
    },
    "fatjet[N]_CSV": {
      "title" : "fatjet CSV",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_CSV1": {
      "title" : "subjet 1 CSV",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_CSV2": {
      "title" : "subjet 2 CSV",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_CSVR1": {
      "title" : "subjet 1 CSV",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_CSVR2": {
      "title" : "subjet 2 CSV",
      "nbins" : 50,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_nBtag": {
      "title" : "number of b-tagged subjets",
      "nbins" : 3,
      "min" : -0.5,
      "max" : 2.5,
      "log" : False,
    },
    "fatjet[N]_flavour": {
      "title" : "fatjet flavour",
      "nbins" : 25,
      "min" : -0.5,
      "max" : 24.5,
      "log" : False,
    },
    "fatjet[N]_flavour1": {
      "title" : "subjet 1 flavour",
      "nbins" : 25,
      "min" : -0.5,
      "max" : 24.5,
      "log" : False,
    },
    "fatjet[N]_flavour2": {
      "title" : "subjet 2 flavour",
      "nbins" : 25,
      "min" : -0.5,
      "max" : 24.5,
      "log" : False,
    },
    "fatjet[N]_chf": {
      "title" : "jet [N] charged hadron fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_nhf": {
      "title" : "jet [N] neutral hadron fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_phf": {
      "title" : "jet [N] photon fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_elf": {
      "title" : "jet [N] electron fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_muf": {
      "title" : "jet [N] muon fraction",
      "nbins" : 20,
      "min" : 0,
      "max" : 1,
      "log" : False,
    },
    "fatjet[N]_chm": {
      "title" : "jet [N] charged multiplicity",
      "nbins" : 50,
      "min" : 0,
      "max" : 50,
      "log" : False,
    },
    "fatjet[N]_npr": {
      "title" : "jet [N] constituents multiplicity",
      "nbins" : 50,
      "min" : 0,
      "max" : 100,
      "log" : False,
    },
    
    
    # Leptons
    "lepton[N]_pt": {
      "title" : "lepton [N] p_{T} (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 500,
      "log" : True,
    },
    "lepton[N]_eta": {
      "title" : "lepton [N] #eta",
      "nbins" : 30,
      "min" : -3.,
      "max" : 3.,
      "log" : False,
    },
    "lepton[N]_phi": {
      "title" : "lepton [N] #varphi",
      "nbins" : 30,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "lepton[N]_mass": {
      "title" : "lepton [N] mass (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 150,
      "log" : False,
    },
    "lepton[N]_dPhi_met": {
      "title" : "lepton [N] #varphi (l-#slash{E}_{T})",
      "nbins" : 30,
      "min" : 0,
      "max" : 3.15,
      "log" : False,
    },
    "lepton[N]_isElectron": {
      "title" : "isElectron",
      "nbins" : 2,
      "min" : -0.5,
      "max" : 1.5,
      "log" : False,
    },
    "lepton[N]_isMuon": {
      "title" : "isMuon",
      "nbins" : 2,
      "min" : -0.5,
      "max" : 1.5,
      "log" : False,
    },
    "lepton[N]_charge": {
      "title" : "lepton [N] charge",
      "nbins" : 3,
      "min" : -1.5,
      "max" : 1.5,
      "log" : False,
    },
    "lepton[N]_ip2d": {
      "title" : "lepton [N] IP_{2D}",
      "nbins" : 50,
      "min" : -0.02,
      "max" : 0.02,
      "log" : True,
    },
    "lepton[N]_ip3d": {
      "title" : "lepton [N] IP_{3D}",
      "nbins" : 50,
      "min" : -0.05,
      "max" : 0.05,
      "log" : True,
    },
    "lepton[N]_relIso03": {
      "title" : "lepton [N] PFIso_{03}",
      "nbins" : 50,
      "min" : 0,
      "max" : 0.25,
      "log" : True,
    },
    "lepton[N]_relIso04": {
      "title" : "lepton [N] PFIso_{04}",
      "nbins" : 50,
      "min" : 0,
      "max" : 0.25,
      "log" : True,
    },
    "lepton[N]_miniIso": {
      "title" : "lepton [N] miniIso",
      "nbins" : 50,
      "min" : 0,
      "max" : 0.1,
      "log" : True,
    },
    "lepton[N]_looseId": {
      "title" : "loose Id",
      "nbins" : 2,
      "min" : -0.5,
      "max" : 1.5,
      "log" : False,
    },
    "lepton[N]_mediumId": {
      "title" : "medium Id",
      "nbins" : 2,
      "min" : -0.5,
      "max" : 1.5,
      "log" : False,
    },
    "lepton[N]_tightId": {
      "title" : "tight Id",
      "nbins" : 2,
      "min" : -0.5,
      "max" : 1.5,
      "log" : False,
    },
    "lepton[N]_highptId": {
      "title" : "high pT Id",
      "nbins" : 2,
      "min" : -0.5,
      "max" : 1.5,
      "log" : False,
    },
    
    # Candidates
    "Z_pt": {
      "title" : "Z candidate p_{T} (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 1000,
      "log" : True,
    },
    "Z_eta": {
      "title" : "Z candidate #eta",
      "nbins" : 30,
      "min" : -3.,
      "max" : 3.,
      "log" : False,
    },
    "Z_phi": {
      "title" : "Z candidate #varphi",
      "nbins" : 60,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "Z_mass": {
      "title" : "m_{Z} (GeV)",
      "nbins" : 60,
      "min" : 70,
      "max" : 110,
      "log" : False,
    },
    "Z_charge": {
      "title" : "Z candidate charge",
      "nbins" : 3,
      "min" : -1.5,
      "max" : 1.5,
      "log" : False,
    },
    "Z_dR": {
      "title" : "#Delta R_{ll}",
      "nbins" : 40,
      "min" : 0,
      "max" : 2,
      "log" : False,
    },
    "Z_dEta": {
      "title" : "#Delta #eta_{ll}",
      "nbins" : 50,
      "min" : 0,
      "max" : 5,
      "log" : False,
    },
    "Z_dPhi": {
      "title" : "#Delta #varphi_{ll}",
      "nbins" : 50,
      "min" : 0,
      "max" : 3.14,
      "log" : False,
    },
    
    
    # W
    "W_pt": {
      "title" : "W candidate p_{T} (GeV)",
      "nbins" : 25,
      "min" : 0,
      "max" : 500,
      "log" : True,
    },
    "W_eta": {
      "title" : "W candidate #eta",
      "nbins" : 30,
      "min" : -3.,
      "max" : 3.,
      "log" : False,
    },
    "W_phi": {
      "title" : "W candidate #varphi",
      "nbins" : 60,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "W_tmass": {
      "title" : "W candidate m_{T} (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 200,
      "log" : False,
    },
    "W_charge": {
      "title" : "W candidate charge",
      "nbins" : 3,
      "min" : -1.5,
      "max" : 1.5,
      "log" : False,
    },
    "W_dR": {
      "title" : "#Delta R_{l-#slash{E}_{T}}",
      "nbins" : 50,
      "min" : 0,
      "max" : 5,
      "log" : False,
    },
    "W_dEta": {
      "title" : "#Delta #eta_{l-#slash{E}_{T}}",
      "nbins" : 50,
      "min" : 0,
      "max" : 5,
      "log" : False,
    },
    "W_dPhi": {
      "title" : "#Delta #varphi_{l-#slash{E}_{T}}",
      "nbins" : 30,
      "min" : 0,
      "max" : 3.14,
      "log" : False,
    },
    "kW_pt": {
      "title" : "W candidate p_{T} (GeV)",
      "nbins" : 25,
      "min" : 200,
      "max" : 1200,
      "log" : True,
    },
    "kW_eta": {
      "title" : "W candidate #eta",
      "nbins" : 30,
      "min" : -3.,
      "max" : 3.,
      "log" : False,
    },
    "kW_phi": {
      "title" : "W candidate #varphi",
      "nbins" : 30,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "kW_dPhi": {
      "title" : "#Delta #varphi (l-#slash{E}_{T})",
      "nbins" : 30,
      "min" : 0,
      "max" : 3.14,
      "log" : False,
    },
    "kW_mass": {
      "title" : "W candidate mass (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 200,
      "log" : False,
    },
    "T_mass": {
      "title" : "Top candidate mass (GeV)",
      "nbins" : 80,
      "min" : 0,
      "max" : 800,
      "log" : False,
    },
    
    # X
    "X_pt": {
      "title" : "X candidate p_{T} (GeV)",
      "nbins" : 50,
      "min" : 0,
      "max" : 1000,
      "log" : True,
    },
    "X_eta": {
      "title" : "X candidate #eta",
      "nbins" : 30,
      "min" : -3.,
      "max" : 3.,
      "log" : False,
    },
    "X_phi": {
      "title" : "X candidate #varphi",
      "nbins" : 60,
      "min" : -3.15,
      "max" : 3.15,
      "log" : False,
    },
    "X_mass": {
      "title" : "m_{X} (GeV)",
      "nbins" : 17*10,
      #"bins" : [500, 540, 583, 629, 678, 730, 785, 843, 904, 968, 1035, 1105, 1178, 1254, 1333, 1415, 1500, 1588, 1679, 1773, 1870, 1970, 2073, 2179, 2288, 2400, 2515, 2633, 2754, 2878, 3005, 3135, 3268, 3404, 3543, 3685, 3830, 3978, 4129, 4283, 4440, 4600],
      #"bins" : [500, 583, 678, 785, 904, 1035, 1178, 1333, 1500, 1679, 1870, 2073, 2288, 2515, 2754, 3005, 3268, 3543, 3830, 4129, 4600],
      "bins" : [x*(1+0.1*x)*40+800 for x in range(28)],#[x*(1+0.1*x)*20+500 for x in range(40)], #[x*(1+0.16*x)*50+500 for x in range(20)],
      "min" : 750.,
      "max" : 5000.,
      "log" : True,
    },
    "X_tmass": {
      "title" : "m_{T}^{X} (GeV)",
      "nbins" : 17,
      #"bins" : [500, 540, 583, 629, 678, 730, 785, 843, 904, 968, 1035, 1105, 1178, 1254, 1333, 1415, 1500, 1588, 1679, 1773, 1870, 1970, 2073, 2179, 2288, 2400, 2515, 2633, 2754, 2878, 3005, 3135, 3268, 3404, 3543, 3685, 3830, 3978, 4129, 4283, 4440, 4600],
      #"bins" : [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4500],
      "bins" : [x*(1+0.30*x)*50+800 for x in range(16)],
      "min" : 750.,
      "max" : 5000.,
      "log" : True,
    },
    "X_cmass": {
      "title" : "collinear m_{X} (GeV)",
      "nbins" : 90,
      "min" : 500.,
      "max" : 5000.,
      "log" : True,
    },
    "X_kmass": {
      "title" : "m_{X} with kinematic fit (GeV)",
      "nbins" : 90,
      "min" : 500.,
      "max" : 5000.,
      "log" : True,
    },
    "X_charge": {
      "title" : "X candidate charge",
      "nbins" : 20,
      "min" : -10,
      "max" : 10,
      "log" : False,
    },
    "X_dR": {
      "title" : "#Delta R (V-jet)",
      "nbins" : 50,
      "min" : 0,
      "max" : 5,
      "log" : False,
    },
    "X_dEta": {
      "title" : "#Delta #eta (V-jet)",
      "nbins" : 50,
      "min" : 0,
      "max" : 5,
      "log" : False,
    },
    "X_dPhi": {
      "title" : "#Delta #varphi (V-jet)",
      "nbins" : 50,
      "min" : 0,
      "max" : 3.14,
      "log" : False,
    },
    
    "transverseMass(fatjet1_pt,fatjet1_phi,met_pt,met_phi)": {
      "title" : "m_{T}^{X} (GeV)",
      "nbins" : -1,
      #"bins" : [500, 540, 583, 629, 678, 730, 785, 843, 904, 968, 1035, 1105, 1178, 1254, 1333, 1415, 1500, 1588, 1679, 1773, 1870, 1970, 2073, 2179, 2288, 2400, 2515, 2633, 2754, 2878, 3005, 3135, 3268, 3404, 3543, 3685, 3830, 3978, 4129, 4283, 4440, 4600],
      #"bins" : [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4500],
      "bins" : [x*(1+0.5*x)*50+500 for x in range(13)],#[x*(1+0.30*x)*50+500 for x in range(15)],
      "min" : 500.,
      "max" : 4500.,
      "log" : True,
    },
    "invariantMass(jet1_pt,jet1_eta,jet1_phi,jet1_mass,jet2_pt,jet2_eta,jet2_phi,jet2_mass)": {
      "title" : "m_{X} (GeV)",
      "nbins" : 100,
      "min" : 0.,
      "max" : 250.,
      "log" : True,
    },
    "invariantDoubleMass(Z_pt,Z_eta,Z_phi,jet1_pt,jet1_eta,jet1_phi,jet2_pt,jet2_eta,jet2_phi)": {
      "title" : "m_{X} (GeV)",
      "nbins" : 45,
      "min" : 200.,
      "max" : 2000.,
      "log" : True,
    },
    "W(lepton1_pt,lepton1_eta,lepton1_phi,lepton1_mass,met_pt,met_phi)": {
      "title" : "m_{X} (GeV)",
      "nbins" : 500,
      "min" : 0.,
      "max" : 500.,
      "log" : True,
    },
    "XWh(lepton1_pt,lepton1_eta,lepton1_phi,met_pt,met_phi,fatjet1_pt,fatjet1_eta,fatjet1_phi,fatjet1_mass)": {
      "title" : "m_{X} (GeV)",
      "nbins" : 21,
      #"bins" : [500, 540, 583, 629, 678, 730, 785, 843, 904, 968, 1035, 1105, 1178, 1254, 1333, 1415, 1500, 1588, 1679, 1773, 1870, 1970, 2073, 2179, 2288, 2400, 2515, 2633, 2754, 2878, 3005, 3135, 3268, 3404, 3543, 3685, 3830, 3978, 4129, 4283, 4440, 4600],
      #"bins" : [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4500],
      "bins" : [x*(1+0.5*x)*50+700 for x in range(13)],#[x*(1+0.30*x)*50+500 for x in range(15)],
      "min" : 800.,
      "max" : 5000.,
      "log" : True,
    },
    "deltaPhi(lepton1_phi,met_phi)": {
      "title" : "#Delta #varphi (l-#slash{E}_{T})",
      "nbins" : 50,
      "min" : -3.14,
      "max" : 3.14,
      "log" : False,
    },
    
    # Dummy
    "0*run": {
      "title" : "",
      "nbins" : 1,
      "bins" : [],
      "min" : -0.5,
      "max" : 0.5,
      "log" : False,
    },
    "0*run+0": {
      "title" : "",
      "nbins" : 4,
      "bins" : [],
      "min" : -0.5,
      "max" : 3.5,
      "log" : False,
    },
    "0*run+1": {
      "title" : "",
      "nbins" : 4,
      "bins" : [],
      "min" : -0.5,
      "max" : 3.5,
      "log" : False,
    },
    "0*run+2": {
      "title" : "",
      "nbins" : 4,
      "bins" : [],
      "min" : -0.5,
      "max" : 3.5,
      "log" : False,
    },
    "0*run+3": {
      "title" : "",
      "nbins" : 4,
      "bins" : [],
      "min" : -0.5,
      "max" : 3.5,
      "log" : False,
    },
    "0==0": {
      "title" : "",
      "nbins" : 5,
      "min" : 0,
      "max" : 5,
      "log" : True,
    },
}


for n, v in var_template.iteritems():
    if '[N]' in n:
        for i in range(1, 5):
            ni = n.replace('[N]', "%d" % i)
            variable[ni] = v.copy()
            variable[ni]['title'] = variable[ni]['title'].replace('[N]', "%d" % i)
    else:
        variable[n] = v

# Custom settings
variable['jet2_pt']['max'] = 400
variable['jet3_pt']['max'] = 200
variable['jet4_pt']['max'] = 200
variable['lepton2_pt']['max'] = 250
