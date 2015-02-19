#!/bin/env python
from math import *
import ROOT
from PhysicsTools.Heppy.analyzers.core.autovars import *
from PhysicsTools.Heppy.analyzers.objects.autophobj  import *

muonType = NTupleObjectType("muon", baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    # Identification
    NTupleVariable("softMuonId", lambda x : x.muonID("POG_ID_Soft") if abs(x.pdgId())==13 else 1, int, help="Muon POG Soft id"),
    NTupleVariable("pfMuonId",   lambda x : x.muonID("POG_ID_Loose") if abs(x.pdgId())==13 else 1, int, help="Muon POG Loose id"),
    NTupleVariable("mediumMuonId",   lambda x : x.muonID("POG_ID_Medium") if abs(x.pdgId())==13 else 1, int, help="Muon POG Medium id"),
    # Isolations with the two radia
    NTupleVariable("relIso03",  lambda x : x.relIso03, help="PF Rel Iso, R=0.3, pile-up corrected"),
    NTupleVariable("relIso04",  lambda x : x.relIso04, help="PF Rel Iso, R=0.4, pile-up corrected"),
])


