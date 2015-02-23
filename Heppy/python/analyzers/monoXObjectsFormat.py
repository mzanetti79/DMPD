#!/bin/env python
from math import *
import ROOT
from PhysicsTools.Heppy.analyzers.core.autovars import *
from PhysicsTools.Heppy.analyzers.objects.autophobj  import *

muonType = NTupleObjectType("muon", baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int, help="Muon charge"),
    # Identification
    NTupleVariable("looseId",   lambda x : x.looseId() if abs(x.pdgId())==13 else 1, int, help="Muon POG Loose id" ),
    NTupleVariable("mediumId",   lambda x : x.muonID("POG_ID_Medium") if abs(x.pdgId())==13 else 1, int, help="Muon POG Medium id"),
    NTupleVariable("tightId",   lambda x : x.tightId() if abs(x.pdgId())==13 else 1, int, help="Muon POG Tight id"),
    # Isolations with the two radia
    NTupleVariable("relIso03",  lambda x : x.relIso03, help="Muon PF Rel Iso, R=0.3, pile-up corrected"),
    NTupleVariable("relIso04",  lambda x : x.relIso04, help="Muon PF Rel Iso, R=0.4, pile-up corrected"),
])

    #def branch_(self, selfmap, varName, type, len, postfix="", storageType="default", title=None):

electronType = NTupleObjectType("electron", baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int, help="Electron charge"),
    # Identification
    NTupleVariable("vetoId",   lambda x : x.cutBasedId("POG_CSA14_25ns_v1_Veto") if abs(x.pdgId())==11 else 1, int, help="Electron POG Cut-based Veto id"),
    NTupleVariable("looseId",  lambda x : x.cutBasedId("POG_CSA14_25ns_v1_Loose") if abs(x.pdgId())==11 else 1, int, help="Electron POG Cut-based Loose id"),
    NTupleVariable("mediumId", lambda x : x.cutBasedId("POG_CSA14_25ns_v1_Medium") if abs(x.pdgId())==11 else 1, int, help="Electron POG Cut-based Medium id"),
    NTupleVariable("tightId",  lambda x : x.cutBasedId("POG_CSA14_25ns_v1_Tight") if abs(x.pdgId())==11 else 1, int, help="Electron POG Cut-based Tight id"),
    # Isolations with the two radia
    NTupleVariable("relIso03",  lambda x : x.relIso03, help="Electron PF Rel Iso, R=0.3, pile-up corrected"),
    NTupleVariable("relIso04",  lambda x : x.relIso04, help="Electron PF Rel Iso, R=0.4, pile-up corrected"),
])

jetType = NTupleObjectType("jet",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("looseId",    lambda x : x.jetID("POG_PFID_Loose") , int, mcOnly=False,help="Jet POG Loose id"),
    NTupleVariable("mediumId",    lambda x : x.jetID("POG_PFID_Medium") , int, mcOnly=False,help="Jet POG Medium id"),
    NTupleVariable("tightId",    lambda x : x.jetID("POG_PFID_Tight") , int, mcOnly=False,help="Jet POG Tight id"),
    NTupleVariable("btagCSV",   lambda x : x.btag('combinedInclusiveSecondaryVertexV2BJetTags'), help="Jet CSV-IVF v2 discriminator"),
    NTupleVariable("puId", lambda x : getattr(x, 'puJetIdPassed', -99), int,     mcOnly=False, help="puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now)"),

    NTupleVariable("mcFlavour", lambda x : x.partonFlavour(), int,     mcOnly=True, help="parton flavour (physics definition, i.e. including b's from shower)"),
    #NTupleVariable("mcMatchId",  lambda x : getattr(x, 'mcMatchId', -99), int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake"),
    #NTupleVariable("mcPt",   lambda x : x.mcJet.pt() if getattr(x,"mcJet",None) else 0., mcOnly=True, help="p_{T} of associated gen jet"),
    NTupleVariable("rawPt",  lambda x : x.pt() * x.rawFactor(), help="p_{T} before JEC"),

    NTupleVariable("chf",    lambda x : x.chargedHadronEnergyFraction() , float, mcOnly=False,help="Jet charged hadron energy fraction"),
    NTupleVariable("nhf",    lambda x : x.neutralHadronEnergyFraction() , float, mcOnly=False,help="Jet neutral hadron energy fraction"),
    NTupleVariable("phf",    lambda x : x.neutralEmEnergyFraction() , float, mcOnly=False,help="Jet neutral electromagnetic energy fraction"),
    NTupleVariable("elf",    lambda x : x.chargedEmEnergyFraction() , float, mcOnly=False,help="Jet charged electromagnetic energy fraction"),
    NTupleVariable("muf",    lambda x : x.muonEnergyFraction() , float, mcOnly=False,help="Jet muon energy fraction"),
    NTupleVariable("chm",    lambda x : x.chargedHadronMultiplicity() , int, mcOnly=False,help="Jet charged hadron multiplicity"),
    NTupleVariable("npr",    lambda x : x.chargedMultiplicity()+x.neutralMultiplicity() , int, mcOnly=False,help="Jet constituents multiplicity"),
])

tauType = NTupleObjectType("tau",  baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    #NTupleVariable("decayMode",   lambda x : x.decayMode(), int),
    #NTupleVariable("idDecayMode",   lambda x : x.idDecayMode, int),
    #NTupleVariable("idDecayModeNewDMs",   lambda x : x.idDecayModeNewDMs, int),
    #NTupleVariable("dxy",   lambda x : x.dxy(), help="d_{xy} of lead track with respect to PV, in cm (with sign)"),
    #NTupleVariable("dz",    lambda x : x.dz() , help="d_{z} of lead track with respect to PV, in cm (with sign)"),
    #NTupleVariable("idMVA", lambda x : x.idMVA, int, help="1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the MVA3oldDMwLT discriminator"),
    #NTupleVariable("idMVANewDM", lambda x : x.idMVANewDM, int, help="1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the MVA3newDMwLT discriminator"),
    #NTupleVariable("idCI3hit", lambda x : x.idCI3hit, int, help="1,2,3 if the tau passes the loose, medium, tight WP of the By<X>CombinedIsolationDBSumPtCorr3Hits discriminator"),
    #NTupleVariable("idAntiMu", lambda x : x.idAntiMu, int, help="1,2 if the tau passes the loose/tight WP of the againstMuon<X>3 discriminator"),
    #NTupleVariable("idAntiE", lambda x : x.idAntiE, int, help="1,2,3,4,5 if the tau passes the v loose, loose, medium, tight, v tight WP of the againstElectron<X>MVA5 discriminator"),
    #NTupleVariable("isoCI3hit",  lambda x : x.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits"), help="byCombinedIsolationDeltaBetaCorrRaw3Hits raw output discriminator"),
    # MC-match info
    #NTupleVariable("mcMatchId",  lambda x : x.mcMatchId, int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake"),
])

photonType = NTupleObjectType("photon", baseObjectTypes = [ particleType ], variables = [
    #NTupleVariable("idCutBased", lambda x : x.idCutBased, int, help="1,2,3 if the photon passes the loose, medium, tight WP of PhotonCutBasedID"),
    NTupleVariable("looseId",    lambda x : x.photonID("PhotonCutBasedIDLoose") , int, mcOnly=False,help="Photon POG Cut-based Loose id"),
    #NTupleVariable("mediumId",    lambda x : x.photonID("PhotonCutBasedIDMedium") , int, mcOnly=False,help="Photon POG Cut-based Medium id"),
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

metType = NTupleObjectType("met",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("sign",    lambda x : x.metSignificance() if x.isCaloMET() else -1, float, mcOnly=False, help="missing energy significance"), #does not work if not CaloMET
    NTupleVariable("phf",     lambda x : x.NeutralEMFraction(), float, mcOnly=False, help="neutral electromagnetic energy fraction"),
    NTupleVariable("nhf",     lambda x : x.NeutralHadEtFraction(), float, mcOnly=False, help="neutral hadron energy fraction"),
    NTupleVariable("elf",     lambda x : x.ChargedEMEtFraction(), float, mcOnly=False, help="charged electromagnetic energy fraction"),
    NTupleVariable("chf",     lambda x : x.ChargedHadEtFraction(), float, mcOnly=False, help="charged hadron energy fraction"),
    NTupleVariable("muf",     lambda x : x.MuonEtFraction(), float, mcOnly=False, help="muon energy fraction"),
])
