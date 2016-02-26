#!/bin/env python
from math import *
import ROOT
from PhysicsTools.Heppy.analyzers.core.autovars import *
from PhysicsTools.Heppy.analyzers.objects.autophobj  import *

lorentzVectorType = NTupleObjectType("lorentzVector", baseObjectTypes = [ fourVectorType ], variables = [])

particleType = NTupleObjectType("particle", baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("pdgId",   lambda x : x.pdgId(), int, help="particle Id"),
])

candidateType = NTupleObjectType("candidate", baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("tmass",   lambda x : getattr(x, "mT", -1.), float, help="transverse mass"),
    #NTupleVariable("charge",   lambda x : getattr(x, "charge", -9.), int, help="charge"),
    NTupleVariable("dR",   lambda x : getattr(x, "deltaR", -1.), float, help="delta R"),
    NTupleVariable("dEta",   lambda x : getattr(x, "deltaEta", -9.), float, help="delta Eta"),
    NTupleVariable("dPhi",   lambda x : getattr(x, "deltaPhi", -9.), float, help="delta Phi"),
    #NTupleVariable("dPhi_met",   lambda x : getattr(x, "deltaPhi_met", -9.), float, help="delta Phi with met"),
    #NTupleVariable("dPhi_jet1",   lambda x : getattr(x, "deltaPhi_jet1", -9.), float, help="delta Phi with leading jet"),
])


candidateMetType = NTupleObjectType("candidate", baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("tmass",   lambda x : getattr(x, "mT", -1.), float, help="transverse mass"),
    NTupleVariable('tmassScaleUp',      lambda x: getattr(x, "mTScaleUp", -1.), float, help='Transverse mass, met Scale Up'),
    NTupleVariable('tmassScaleDown',      lambda x: getattr(x, "mTScaleDown", -1.), float, help='Transverse mass, met Scale Down'),
    NTupleVariable('tmassResUp',      lambda x: getattr(x, "mTResUp", -1.), float, help='Transverse mass, met Resolution Up'),
    NTupleVariable('tmassResDown',      lambda x: getattr(x, "mTResDown", -1.), float, help='Transverse mass, met Resolution Down'),
    NTupleVariable("dR",   lambda x : getattr(x, "deltaR", -1.), float, help="delta R"),
    NTupleVariable("dEta",   lambda x : getattr(x, "deltaEta", -9.), float, help="delta Eta"),
    NTupleVariable("dPhi",   lambda x : getattr(x, "deltaPhi", -9.), float, help="delta Phi"),
])

candidateFullType = NTupleObjectType("candidate", baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("tmass",   lambda x : getattr(x, "mT", -1.), float, help="transverse mass"),
    NTupleVariable("cmass",   lambda x : getattr(x, "mC", -1.), float, help="collinear mass"),
    NTupleVariable("kmass",   lambda x : getattr(x, "mK", -1.), float, help="Mass with kinematic fit"),
    NTupleVariable("charge",   lambda x : getattr(x, "charge", -9.), int, help="charge"),
    NTupleVariable("dR",   lambda x : getattr(x, "deltaR", -1.), float, help="delta R"),
    NTupleVariable("dEta",   lambda x : getattr(x, "deltaEta", -9.), float, help="delta Eta"),
    NTupleVariable("dPhi",   lambda x : getattr(x, "deltaPhi", -9.), float, help="delta Phi"),
    #NTupleVariable("dPhi_met",   lambda x : getattr(x, "deltaPhi_met", -9.), float, help="delta Phi with met"),
    #NTupleVariable("dPhi_jet1",   lambda x : getattr(x, "deltaPhi_jet1", -9.), float, help="delta Phi with leading jet"),
])


leptonType = NTupleObjectType("lepton", baseObjectTypes = [ particleType ], variables = [
    # Is Muon/Electron
    NTupleVariable("isElectron",   lambda x : True if x.isElectron() else False, int, help="Electron flag" ),
    NTupleVariable("isMuon",   lambda x : True if x.isMuon() else False, int, help="Muon flag" ),
    # Charge
    NTupleVariable("charge",   lambda x : x.charge(), int, help="Lepton charge"),
    NTupleVariable("dPhi_met",   lambda x : getattr(x, "deltaPhi_met", -9.), float, help="dPhi between lepton and met"),
    # Impact parameters
    NTupleVariable("dxy", lambda x : getattr(x, "dxyPV", -99.), float, help="Lepton dxy w.r.t. PV"),
    NTupleVariable("dz",  lambda x : getattr(x, "dzPV", -99.), float, help="Lepton dz w.r.t. PV"),
    # Isolations with the two radia
    NTupleVariable("relIso03",  lambda x : x.relIso03, float, help="PF Rel Iso, R=0.3, pile-up corrected"),
    NTupleVariable("relIso04",  lambda x : x.relIso04, float, help="PF Rel Iso, R=0.4, pile-up corrected"),
    NTupleVariable("miniIso",   lambda x : getattr(x, "miniRelIso", -1.), float, help="Rel Mini-Iso, pile-up corrected"),
    NTupleVariable("trkIso",    lambda x : x.trkIso, float, help="Tracker-Iso, pile-up corrected (tracks from PV only)"),
    # Cut Based Identification
    NTupleVariable("vetoId",  lambda x : getattr(x, "isCustomTracker", 0) if x.isMuon() else ( x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto")    and ( ( x.isEB() and x.relIso03 < 0.1260 ) or  ( x.isEE() and x.relIso03 < 0.1440 ) ) ), int, help="Cut Based Veto id" ),
    NTupleVariable("looseId", lambda x : x.muonID("POG_ID_Loose")   if x.isMuon() else ( x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Loose")   and ( ( x.isEB() and x.relIso03 < 0.0893 ) or  ( x.isEE() and x.relIso03 < 0.1210 ) ) ), int, help="Cut Based Loose id" ),
    NTupleVariable("mediumId",lambda x : x.muonID("POG_ID_Medium")  if x.isMuon() else ( x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Medium")  and ( ( x.isEB() and x.relIso03 < 0.0766 ) or  ( x.isEE() and x.relIso03 < 0.0678 ) ) ), int, help="Cut Based Medium id"),
    NTupleVariable("tightId", lambda x : x.muonID("POG_ID_Tight")   if x.isMuon() else ( x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Tight")   and ( ( x.isEB() and x.relIso03 < 0.0354 ) or  ( x.isEE() and x.relIso03 < 0.0646 ) ) ), int, help="Cut Based Tight id"),
    NTupleVariable("highptId",lambda x : x.muonID("POG_ID_HighPt")  if x.isMuon() else getattr(x, "isHEEP", 0), int, help="Cut Based Tight id"),   

    NTupleVariable("trigMatch",    lambda x : x.trigMatch if hasattr(x,'trigMatch') else False, int, help="Is trigger matched" ),
    #NTupleVariable("trigMatchPt",  lambda x : x.trigMatchPt if hasattr(x,'trigMatchPt') else -999., float, help="Pt of trigger object" ),
    #NTupleVariable("trigMatchPhi", lambda x : x.trigMatchPhi if hasattr(x,'trigMatchPhi') else -999., float, help="Phi of trigger object" ),
    #NTupleVariable("trigMatchEta", lambda x : x.trigMatchEta if hasattr(x,'trigMatchEta') else -999., float, help="Eta of trigger object" ),
])

muonType = NTupleObjectType("muon", baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge", lambda x : x.charge(), int, help="Muon charge"),
    # Identification
    NTupleVariable("looseId",  lambda x : x.muonID("POG_ID_Loose") if x.isMuon() else -9, int, help="Muon POG Loose id" ),
    NTupleVariable("mediumId", lambda x : x.muonID("POG_ID_Medium") if x.isMuon() else -9, int, help="Muon POG Medium id"),
    NTupleVariable("tightId",  lambda x : x.muonID("POG_ID_Tight") if x.isMuon() else -9, int, help="Muon POG Tight id"),
    # Relative Isolations fixed ratia / variable ratio
    NTupleVariable("relIso03",   lambda x : x.relIso03, float, help="Muon PF Rel Iso, R=0.3, pile-up corrected"),
    NTupleVariable("relIso04",   lambda x : x.relIso04, float, help="Muon PF Rel Iso, R=0.4, pile-up corrected"),
    NTupleVariable("miniIso",    lambda x : x.miniRelIso, float, help="Muon Rel Mini-Iso, pile-up corrected"),
    # Impact parameters
    NTupleVariable("ip2d", lambda x : x.dB(1), float, help="Lepton 2D impact parameter"),
    NTupleVariable("ip3d", lambda x : x.dB(2), float, help="Lepton 3D impact parameter"),
    NTupleVariable("dz",  lambda x : x.dz(), float, help="Lepton dz"),

])

electronType = NTupleObjectType("electron", baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int, help="Electron charge"),
    # Identification
    NTupleVariable("vetoId",   lambda x : x.cutBasedId("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto") if abs(x.pdgId())==11 else -9, int, help="Electron POG Cut-based Veto id"),
    NTupleVariable("looseId",  lambda x : x.cutBasedId("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Loose") if abs(x.pdgId())==11 else -9, int, help="Electron POG Cut-based Loose id"),
    NTupleVariable("mediumId", lambda x : x.cutBasedId("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Medium") if abs(x.pdgId())==11 else -9, int, help="Electron POG Cut-based Medium id"),
    NTupleVariable("tightId",  lambda x : x.cutBasedId("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Tight") if abs(x.pdgId())==11 else -9, int, help="Electron POG Cut-based Tight id"),
    # Isolations with the two radia
    NTupleVariable("relIso03",  lambda x : x.relIso03, float, help="Electron PF Rel Iso, R=0.3, pile-up corrected"),
    NTupleVariable("relIso04",  lambda x : x.relIso04, float, help="Electron PF Rel Iso, R=0.4, pile-up corrected"),
    # Impact parameters
    NTupleVariable("ip2d", lambda x : x.dB(1), float, help="Lepton 2D impact parameter"),
    NTupleVariable("ip3d", lambda x : x.dB(2), float, help="Lepton 3D impact parameter"),
    NTupleVariable("dz",  lambda x : x.dz(), float, help="Lepton dz"),
])

jetSlimType = NTupleObjectType("jet",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("flavour", lambda x : x.hadronFlavour(), int,     mcOnly=False, help="flavour of the ghost hadron clustered inside the jet"),
    NTupleVariable("CSV",   lambda x : x.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags'), float, help="Jet CSV-IVF v2 discriminator"),
])

jetType = NTupleObjectType("jet",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("dPhi_met",   lambda x : getattr(x, "deltaPhi_met", -9.), float, help="dPhi between jet and met"),
    NTupleVariable("dPhi_jet1",   lambda x : getattr(x, "deltaPhi_jet1", -9.), float, help="dPhi between jet and leading jet"),
    #NTupleVariable("puId", lambda x : getattr(x, 'puJetIdPassed', -999.), int,     mcOnly=False, help="puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now)"),
    NTupleVariable("CSV",   lambda x : x.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags'), float, help="Jet CSV-IVF v2 discriminator"),
    NTupleVariable("flavour", lambda x : x.hadronFlavour(), int,     mcOnly=False, help="flavour of the ghost hadron clustered inside the jet"),
#    NTupleVariable("motherPdgId", lambda x : x.mother().pdgId() if x.mother() else 0, int,     mcOnly=False, help="parton flavour (physics definition, i.e. including b's from shower)"),
#    NTupleVariable("mcMatchPdgId",  lambda x : getattr(x, 'mcMatchId', -999.), int, mcOnly=False, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake"),
    #NTupleVariable("mcPt",   lambda x : x.mcJet.pt() if getattr(x,"mcJet",None) else 0., mcOnly=True, help="p_{T} of associated gen jet"),
    #NTupleVariable("rawPt",  lambda x : x.pt()*x.rawFactor(), help="p_{T} before JEC"),
    #NTupleVariable("ptUnc",  lambda x : x.pt()*x.jetEnergyCorrUncertainty(), help="JEC uncertainty"),
    #NTupleVariable("corr",  lambda x : x.pt()*x.rawFactor()*x.corr, help="JEC uncertainty"),
    NTupleVariable("ptJESUp",  lambda x : getattr(x, "ptJESUp", 0), float, help="JEC uncertainty Up"),
    NTupleVariable("ptJESDown",  lambda x : getattr(x, "ptJESDown", 0), float, help="JEC uncertainty Down"),
    NTupleVariable("chf",    lambda x : x.chargedHadronEnergyFraction() , float, mcOnly=False,help="Jet charged hadron energy fraction"),
    NTupleVariable("nhf",    lambda x : x.neutralHadronEnergyFraction() , float, mcOnly=False,help="Jet neutral hadron energy fraction"),
    NTupleVariable("phf",    lambda x : x.neutralEmEnergyFraction() , float, mcOnly=False,help="Jet neutral electromagnetic energy fraction"),
    NTupleVariable("elf",    lambda x : x.chargedEmEnergyFraction() , float, mcOnly=False,help="Jet charged electromagnetic energy fraction"),
    NTupleVariable("muf",    lambda x : x.muonEnergyFraction() , float, mcOnly=False,help="Jet muon energy fraction"),
    NTupleVariable("chm",    lambda x : x.chargedHadronMultiplicity() , int, mcOnly=False,help="Jet charged hadron multiplicity"),
    NTupleVariable("npr",    lambda x : x.chargedMultiplicity()+x.neutralMultiplicity() , int, mcOnly=False,help="Jet constituents multiplicity"),
    #NTupleVariable("looseId",    lambda x : x.jetID("POG_PFID_Loose") , int, mcOnly=False,help="Jet POG Loose id"),
    #NTupleVariable("mediumId",    lambda x : x.jetID("POG_PFID_Medium") , int, mcOnly=False,help="Jet POG Medium id"),
    #NTupleVariable("tightId",    lambda x : x.jetID("POG_PFID_Tight") , int, mcOnly=False,help="Jet POG Tight id"),
])

fatjetType = NTupleObjectType("jet",  baseObjectTypes = [ fourVectorType ], variables = [
    #NTupleVariable("trimmedMass",   lambda x : x.userFloat("ak8PFJetsCHSTrimmedMass") if x.hasUserFloat("ak8PFJetsCHSTrimmedMass") else -1., float, help="Jet trimmed mass"),
    #NTupleVariable("filteredMass",   lambda x : x.userFloat("ak8PFJetsCHSFilteredMass") if x.hasUserFloat("ak8PFJetsCHSFilteredMass") else -1., float, help="Jet filtered mass"),
    NTupleVariable("prunedMass",   lambda x : x.userFloat("ak8PFJetsCHSPrunedMass") if x.hasUserFloat("ak8PFJetsCHSPrunedMass") else -1., float, help="Jet pruned mass"),
    NTupleVariable("softdropMass",   lambda x : x.userFloat("ak8PFJetsCHSSoftDropMass") if x.hasUserFloat("ak8PFJetsCHSSoftDropMass") else -1., float, help="Jet SoftDrop mass"),
    NTupleVariable("prunedMassCorr",   lambda x : x.userFloat("ak8PFJetsCHSPrunedMassCorr") if x.hasUserFloat("ak8PFJetsCHSPrunedMassCorr") else -1., float, help="Jet pruned mass corrected"),
    NTupleVariable("softdropMassCorr",   lambda x : x.userFloat("ak8PFJetsCHSSoftDropMassCorr") if x.hasUserFloat("ak8PFJetsCHSSoftDropMassCorr") else -1., float, help="Jet SoftDrop mass corrected"),
    
    NTupleVariable("pt1",   lambda x : x.subjets('SoftDrop')[0].pt() if len(x.subjets('SoftDrop')) > 0 else -1., float, help="subJet 1 pt"),
    NTupleVariable("eta1",   lambda x : x.subjets('SoftDrop')[0].eta() if len(x.subjets('SoftDrop')) > 0 else -1., float, help="subJet 1 eta"),
    NTupleVariable("phi1",   lambda x : x.subjets('SoftDrop')[0].phi() if len(x.subjets('SoftDrop')) > 0 else -1., float, help="subJet 1 phi"),
    NTupleVariable("pt2",   lambda x : x.subjets('SoftDrop')[1].pt() if len(x.subjets('SoftDrop')) > 1 else -1., float, help="subJet 2 pt"),
    NTupleVariable("eta2",   lambda x : x.subjets('SoftDrop')[1].eta() if len(x.subjets('SoftDrop')) > 1 else -1., float, help="subJet 2 eta"),
    NTupleVariable("phi2",   lambda x : x.subjets('SoftDrop')[1].phi() if len(x.subjets('SoftDrop')) > 1 else -1., float, help="subJet 2 phi"),
    
    NTupleVariable("dR",   lambda x : getattr(x, "dR_subjets", -1.), float, help="dR between the two subjets"),
    NTupleVariable("dPhi_met",   lambda x : getattr(x, "deltaPhi_met", -9.), float, help="dPhi between jet and met"),
    #NTupleVariable("dPhi_jet1",   lambda x : getattr(x, "deltaPhi_jet1", -9.), float, help="dPhi between jet and leading jet"),
    #NTupleVariable("puId", lambda x : getattr(x, 'puJetIdPassed', -999.), int,     mcOnly=False, help="puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now)"),
    NTupleVariable("tau21",   lambda x : x.userFloat("NjettinessAK8:tau2")/x.userFloat("NjettinessAK8:tau1") if not x.userFloat("NjettinessAK8:tau1") == 0 else -1., float, help="n-subjettiness 2/1"),
    NTupleVariable("CSV",   lambda x : x.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags'), float, help="Jet CSV-IVF v2 discriminator"),
    NTupleVariable("CSV1",   lambda x : x.subjets('SoftDrop')[0].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') if len(x.subjets('SoftDrop')) > 0 else -1., float, help="subJet 1 CSV-IVF v2 discriminator"),
    NTupleVariable("CSV2",   lambda x : x.subjets('SoftDrop')[1].bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') if len(x.subjets('SoftDrop')) > 1 else -1., float, help="subJet 2 CSV-IVF v2 discriminator"),
    #NTupleVariable("nSubJetTags",   lambda x : getattr(x, "nSubJetTags", -999.), int, help="Number of b-tagged subjets"),
    NTupleVariable("flavour", lambda x : x.hadronFlavour(), int,     mcOnly=False, help="flavour of the ghost hadron clustered inside the jet"),
    NTupleVariable("flavour1", lambda x : x.subjets('SoftDrop')[0].hadronFlavour() if len(x.subjets('SoftDrop')) > 0 else -9, int,     mcOnly=False, help="flavour of the ghost hadron clustered inside the subjet 1"),
    NTupleVariable("flavour2", lambda x : x.subjets('SoftDrop')[1].hadronFlavour() if len(x.subjets('SoftDrop')) > 1 else -9, int,     mcOnly=False, help="flavour of the ghost hadron clustered inside the subjet 2"),
#    NTupleVariable("motherPdgId", lambda x : x.mother().pdgId() if x.mother() else 0, int,     mcOnly=False, help="parton flavour (physics definition, i.e. including b's from shower)"),
#    NTupleVariable("mcMatchPdgId",  lambda x : getattr(x, 'mcMatchId', -999.), int, mcOnly=False, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake"),
    #NTupleVariable("mcPt",   lambda x : x.mcJet.pt() if getattr(x,"mcJet",None) else 0., mcOnly=True, help="p_{T} of associated gen jet"),
    #NTupleVariable("rawPt",  lambda x : x.pt()*x.rawFactor(), help="p_{T} before JEC"),
    #NTupleVariable("ptUnc",  lambda x : x.pt()*x.jetEnergyCorrUncertainty(), help="JEC uncertainty"),
    NTupleVariable("ptJESUp",  lambda x : getattr(x, "ptJESUp", 0), float, help="JEC uncertainty Up"),
    NTupleVariable("ptJESDown",  lambda x : getattr(x, "ptJESDown", 0), float, help="JEC uncertainty Down"),
    NTupleVariable("prunedMassCorrJESUp",   lambda x : x.userFloat("ak8PFJetsCHSPrunedMassCorrJESUp") if x.hasUserFloat("ak8PFJetsCHSPrunedMassCorrJESUp") else -1., float, help="Jet pruned mass corrected JEC Up"),
    NTupleVariable("prunedMassCorrJESDown", lambda x : x.userFloat("ak8PFJetsCHSPrunedMassCorrJESDown") if x.hasUserFloat("ak8PFJetsCHSPrunedMassCorrJESDown") else -1., float, help="Jet pruned mass corrected JEC Down"),
    NTupleVariable("softDropMassCorrJESUp",   lambda x : x.userFloat("ak8PFJetsCHSSoftDropMassCorrJESUp") if x.hasUserFloat("ak8PFJetsCHSSoftDropMassCorrJESUp") else -1., float, help="Jet SoftDrop mass corrected JEC Up"),
    NTupleVariable("softDropMassCorrJESDown", lambda x : x.userFloat("ak8PFJetsCHSSoftDropMassCorrJESDown") if x.hasUserFloat("ak8PFJetsCHSSoftDropMassCorrJESDown") else -1., float, help="Jet SoftDrop mass corrected JEC Down"),

    NTupleVariable("chf",    lambda x : x.chargedHadronEnergyFraction() , float, mcOnly=False,help="Jet charged hadron energy fraction"),
    NTupleVariable("nhf",    lambda x : x.neutralHadronEnergyFraction() , float, mcOnly=False,help="Jet neutral hadron energy fraction"),
    NTupleVariable("phf",    lambda x : x.neutralEmEnergyFraction() , float, mcOnly=False,help="Jet neutral electromagnetic energy fraction"),
    NTupleVariable("elf",    lambda x : x.chargedEmEnergyFraction() , float, mcOnly=False,help="Jet charged electromagnetic energy fraction"),
    NTupleVariable("muf",    lambda x : x.muonEnergyFraction() , float, mcOnly=False,help="Jet muon energy fraction"),
    NTupleVariable("chm",    lambda x : x.chargedHadronMultiplicity() , int, mcOnly=False,help="Jet charged hadron multiplicity"),
    NTupleVariable("npr",    lambda x : x.chargedMultiplicity()+x.neutralMultiplicity() , int, mcOnly=False,help="Jet constituents multiplicity"),
    #NTupleVariable("looseId",    lambda x : x.jetID("POG_PFID_Loose") , int, mcOnly=False,help="Jet POG Loose id"),
    #NTupleVariable("mediumId",   lambda x : x.jetID("POG_PFID_Medium") , int, mcOnly=False,help="Jet POG Medium id"),
    NTupleVariable("tightId",    lambda x : x.jetID("POG_PFID_Tight") , int, mcOnly=False,help="Jet POG Tight id"),
])

#subjetType = NTupleObjectType("subjet",  baseObjectTypes = [ fourVectorType ], variables = [
#    NTupleVariable("CSV",   lambda x : x.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags'), float, help="Jet CSV-IVF v2 discriminator"),
#    NTupleVariable("flavour", lambda x : x.hadronFlavour(), int,     mcOnly=False, help="flavour of the ghost hadron clustered inside the jet"),
#])

tauType = NTupleObjectType("tau",  baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    #NTupleVariable("decayMode",   lambda x : x.decayMode(), int),
    #NTupleVariable("idDecayMode",   lambda x : x.idDecayMode, int),
    #NTupleVariable("idDecayModeNewDMs",   lambda x : x.idDecayModeNewDMs, int),
    #NTupleVariable("dxy",   lambda x : x.dxy(), help="d_{xy} of lead track with respect to PV, in cm (with sign)"),
    #NTupleVariable("dz",    lambda x : x.dz() , help="d_{z} of lead track with respect to PV, in cm (with sign)"),
    #NTupleVariable("idMVA", lambda x : x.idMVA, int, help="-99.,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the MVA3oldDMwLT discriminator"),
    #NTupleVariable("idMVANewDM", lambda x : x.idMVANewDM, int, help="-99.,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the MVA3newDMwLT discriminator"),
    #NTupleVariable("idCI3hit", lambda x : x.idCI3hit, int, help="-99.,2,3 if the tau passes the loose, medium, tight WP of the By<X>CombinedIsolationDBSumPtCorr3Hits discriminator"),
    #NTupleVariable("idAntiMu", lambda x : x.idAntiMu, int, help="-99.,2 if the tau passes the loose/tight WP of the againstMuon<X>3 discriminator"),
    #NTupleVariable("idAntiE", lambda x : x.idAntiE, int, help="-99.,2,3,4,5 if the tau passes the v loose, loose, medium, tight, v tight WP of the againstElectron<X>MVA5 discriminator"),
    #NTupleVariable("isoCI3hit",  lambda x : x.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits"), help="byCombinedIsolationDeltaBetaCorrRaw3Hits raw output discriminator"),
    # MC-match info
    #NTupleVariable("mcMatchId",  lambda x : x.mcMatchId, int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake"),
])

photonType = NTupleObjectType("photon", baseObjectTypes = [ particleType ], variables = [
    #NTupleVariable("idCutBased", lambda x : x.idCutBased, int, help="-99.,2,3 if the photon passes the loose, medium, tight WP of PhotonCutBasedID"),
    NTupleVariable("looseId",    lambda x : x.photonID("PhotonCutBasedIDLoose") , int, mcOnly=False,help="Photon POG Cut-based Loose id"),
#    NTupleVariable("mediumId",    lambda x : x.photonID("PhotonCutBasedIDMedium") , int, mcOnly=False,help="Photon POG Cut-based Medium id"),
    NTupleVariable("tightId",    lambda x : x.photonID("PhotonCutBasedIDTight") , int, mcOnly=False,help="Photon POG Cut-based Tight id"),
    #NTupleVariable("hOverE",  lambda x : x.hOVERe(), float, help="hoverE for photons"),
    #NTupleVariable("r9",  lambda x : x.full5x5_r9(), float, help="r9 for photons"),
    #NTupleVariable("sigmaIetaIeta",  lambda x : x.full5x5_sigmaIetaIeta(), float, help="sigmaIetaIeta for photons"),
    #NTupleVariable("chHadIso",  lambda x : x.chargedHadronIso(), float, help="chargedHadronIsolation for photons"),
    #NTupleVariable("neuHadIso",  lambda x : x.neutralHadronIso(), float, help="neutralHadronIsolation for photons"),
    #NTupleVariable("phIso",  lambda x : x.photonIso(), float, help="gammaIsolation for photons"),
    #NTupleVariable("chHadIso",  lambda x : x.recoChargedHadronIso(), float, help="chargedHadronIsolation for photons"),
    #NTupleVariable("neuHadIso",  lambda x : x.recoNeutralHadronIso(), float, help="neutralHadronIsolation for photons"),
    #NTupleVariable("phIso",  lambda x : x.recoPhotonIso(), float, help="gammaIsolation for photons"),
    #NTupleVariable("mcMatchId",  lambda x : x.mcMatchId, int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake"),
])

metType = NTupleObjectType("met",  baseObjectTypes = [ twoVectorType ], variables = [])

metCorType = NTupleObjectType("met",  baseObjectTypes = [ twoVectorType ], variables = [
    NTupleVariable("ptScaleUp",     lambda x : x.ptScaleUp, float, mcOnly=False, help="ptScaleUp"),
    NTupleVariable("ptScaleDown",     lambda x : x.ptScaleDown, float, mcOnly=False, help="ptScaleDown"),
    NTupleVariable("ptResUp",     lambda x : x.ptResUp, float, mcOnly=False, help="ptResUp"),
    NTupleVariable("ptResDown",     lambda x : x.ptResDown, float, mcOnly=False, help="ptResDown"),
])

metFullType = NTupleObjectType("met",  baseObjectTypes = [ twoVectorType ], variables = [
    NTupleVariable("ptRaw",     lambda x : x.uncorPt(), float, mcOnly=False, help="Raw MET pt"),
    NTupleVariable("phiRaw",    lambda x : x.uncorPhi(), float, mcOnly=False, help="Raw MET phi"),
    NTupleVariable("ptGen",     lambda x : x.genMET().pt() if x.genMET() else -1, float, mcOnly=False, help="Gen MET pt"),
    NTupleVariable("phiGen",    lambda x : x.genMET().phi() if x.genMET() else -1, float, mcOnly=False, help="Gen MET phi"),
    NTupleVariable("ptJERUp",   lambda x : x.shiftedPt(0), float, mcOnly=False, help="pt with JER Up (METUncertainty 0)"),
    NTupleVariable("ptJERDown", lambda x : x.shiftedPt(1), float, mcOnly=False, help="pt with JER Down (METUncertainty 1)"),
    NTupleVariable("ptJESUp",   lambda x : x.shiftedPt(2), float, mcOnly=False, help="pt with JES Up (METUncertainty 2)"),
    NTupleVariable("ptJESDown", lambda x : x.shiftedPt(3), float, mcOnly=False, help="pt with JES Down (METUncertainty 3)"),
    NTupleVariable("ptMUSUp",   lambda x : x.shiftedPt(4), float, mcOnly=False, help="pt with MUS Up (METUncertainty 4)"),
    NTupleVariable("ptMUSDown", lambda x : x.shiftedPt(5), float, mcOnly=False, help="pt with MUS Down (METUncertainty 5)"),
    NTupleVariable("ptELSUp",   lambda x : x.shiftedPt(6), float, mcOnly=False, help="pt with ELS Up (METUncertainty 6)"),
    NTupleVariable("ptELSDown", lambda x : x.shiftedPt(7), float, mcOnly=False, help="pt with ELS Down (METUncertainty 7)"),
    NTupleVariable("ptTAUUp",   lambda x : x.shiftedPt(8), float, mcOnly=False, help="pt with TAU Up (METUncertainty 8)"),
    NTupleVariable("ptTAUDown", lambda x : x.shiftedPt(9), float, mcOnly=False, help="pt with TAU Down (METUncertainty 9)"),
    NTupleVariable("ptUNCUp",   lambda x : x.shiftedPt(10), float, mcOnly=False, help="pt with UNC Up (METUncertainty 10)"),
    NTupleVariable("ptUNCDown", lambda x : x.shiftedPt(11), float, mcOnly=False, help="pt with UNC Down (METUncertainty 11)"),
    NTupleVariable("ptPHOUp",   lambda x : x.shiftedPt(12), float, mcOnly=False, help="pt with PHO Up (METUncertainty 12)"),
    NTupleVariable("ptPHODown", lambda x : x.shiftedPt(13), float, mcOnly=False, help="pt with PHO Down (METUncertainty 13)"),
#    NTupleVariable("calo_pt",    lambda x : x.caloMETPt(), float, mcOnly=False, help="CaloMET pt"), #does not work if not CaloMET
#    NTupleVariable("calo_phi",    lambda x : x.caloMETPhi(), float, mcOnly=False, help="CaloMET phi"), #does not work if not CaloMET
#    NTupleVariable("sign",    lambda x : x.metSignificance() if x.isCaloMET() else -1., float, mcOnly=False, help="missing energy significance"), #does not work if not CaloMET
#    NTupleVariable("uncorrected",    lambda x : x.uncorrectedPt(), float, mcOnly=False, help="missing energy significance"), #uncorrected met
#    NTupleVariable("phf",     lambda x : x.NeutralEMFraction(), float, mcOnly=False, help="neutral electromagnetic energy fraction"),
#    NTupleVariable("nhf",     lambda x : x.NeutralHadEtFraction(), float, mcOnly=False, help="neutral hadron energy fraction"),
#    NTupleVariable("elf",     lambda x : x.ChargedEMEtFraction(), float, mcOnly=False, help="charged electromagnetic energy fraction"),
#    NTupleVariable("chf",     lambda x : x.ChargedHadEtFraction(), float, mcOnly=False, help="charged hadron energy fraction"),
#    NTupleVariable("muf",     lambda x : x.MuonEtFraction(), float, mcOnly=False, help="muon energy fraction"),
])
