#! /usr/bin/env python

import os
from array import array
from ROOT import TFile, TH1F, TCanvas

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-d", "--dataFile", action="store", type="string", default=False, dest="dataFileName")
parser.add_option("-m", "--mcFile", action="store", type="string", default=False, dest="mcFileName")
parser.add_option("-p", "--plot", action="store", default=False, dest="doPlot")
parser.add_option("-s", "--save", action="store", default=True, dest="doSave")

(options, args) = parser.parse_args()

dataFileName = options.dataFile
mcFileName = options.dataFile
doPlot = options.doPlot
doSave = options.doSave



dataFile = TFile(dataFileName, "READ")
dataTree = dataFile.Get("ZCR")
data = TH1F("data", "nPV distribution", 60, 0, 60)
data.Sumw2()
dataTree.Project("data", "nPV", "")
data.Scale(1./data.Integral())
data.SetMarkerSize(1.)
data.SetMarkerStyle(20)

mcFile = TFile(mcFileName, "READ")
mcTree = mcFile.Get("ZCR")
mc = TH1F("mc", "nPV distribution", 60, 0, 60)
mc.Sumw2()
mcTree.Project("mc", "nPV", "abs(genWeight)/genWeight")
mc.Scale(1./mc.Integral())
mc.SetLineWidth(2)

if doSave:
    outFile = TFile("./PU.root", "RECREATE")
    outFile.cd()
    data.Write()
    mc.Write()
    outFile.Close()
    print "Histograms written to ./PU.root file"

if doPlot:
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
