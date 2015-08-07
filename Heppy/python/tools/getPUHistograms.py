#! /usr/bin/env python

import os
from array import array
from ROOT import TFile, TH1F, TCanvas




dataFile = TFile("/lustre/cmswork/zucchett/CMSSW_7_4_7/src/DMPD/Heppy/test/Batch/SingleMuon_Run2015B_PromptReco_v1/Loop/tree.root", "READ")
dataTree = dataFile.Get("ZCR")
data = TH1F("data", "nPV distribution", 60, 0, 60)
data.Sumw2()
dataTree.Project("data", "nPV", "")
data.Scale(1./data.Integral())
data.SetMarkerSize(1.)
data.SetMarkerStyle(20)

mcFile = TFile("/lustre/cmswork/zucchett/CMSSW_7_4_7/src/DMPD/Heppy/test/Batch/DYJetsToLL_M50_amcatnloFXFX_pythia8_v3/Loop/tree.root", "READ")
mcTree = mcFile.Get("ZCR")
mc = TH1F("mc", "nPV distribution", 60, 0, 60)
mc.Sumw2()
mcTree.Project("mc", "nPV", "abs(genWeight)/genWeight")
mc.Scale(1./mc.Integral())
mc.SetLineWidth(2)

outFile = TFile("./PU.root", "RECREATE")
outFile.cd()
data.Write()
mc.Write()
outFile.Close()
print "Histograms written to PU.root file"

mc2File = TFile("/lustre/cmsdata/DM/ntuples/Prod_v08/weighted/DYJetsToLL_M50_amcatnloFXFX_pythia8_v3.root", "READ")
mc2Tree = mc2File.Get("ZCR")
mc2 = TH1F("mc", "nPV distribution", 60, 0, 60)
mc2.Sumw2()
mc2Tree.Project("mc", "nPV", "pileupWeight*abs(genWeight)/genWeight")
mc2.Scale(1./mc2.Integral())
mc2.SetLineWidth(2)
mc2.SetLineColor(2)

c1 = TCanvas("c1", "PileUp reweighting", 800, 800)
c1.cd()
data.Draw("PE")
mc.Draw("SAME, H")
mc2.Draw("SAME, H")
c1.Print("PU.pdf")
c1.Print("PU.png")
