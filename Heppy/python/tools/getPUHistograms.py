#! /usr/bin/env python

import os
from array import array
from ROOT import gStyle, TFile, TH1F, TCanvas
gStyle.SetOptStat(0)

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-d", "--dataFile", action="store", type="string", default=False, dest="dataFileName")
parser.add_option("-m", "--mcFile", action="store", type="string", default=False, dest="mcFileName")
parser.add_option("-r", "--mcReweightedFile", action="store", type="string", default=False, dest="mcReweightedFileName")
parser.add_option("-p", "--plot", action="store_true", default=False, dest="doPlot")
parser.add_option("-s", "--save", action="store_true", default=True, dest="doSave")

(options, args) = parser.parse_args()

dataFileName = options.dataFileName
mcFileName = options.mcFileName
mcReweightedFileName = options.mcReweightedFileName
doPlot = options.doPlot
doSave = options.doSave

print "\n\n\n"
print dataFileName, mcFileName, mcReweightedFileName


dataFile = TFile(dataFileName, "READ")
dataTree = dataFile.Get("ZCR")
data = TH1F("data", "nPV distribution", 60, 0, 60)
data.Sumw2()
dataTree.Project("data", "nPV", "HLT_BIT_HLT_IsoMu27_v")
data.Scale(1./data.Integral())
data.SetMarkerSize(1.25)
data.SetMarkerStyle(20)

mcFile = TFile(mcFileName, "READ")
mcTree = mcFile.Get("ZCR")
mc = TH1F("mc", "nPV distribution", 60, 0, 60)
mc.Sumw2()
mcTree.Project("mc", "nPV", "abs(genWeight)/genWeight * HLT_BIT_HLT_IsoMu27_v")
mc.Scale(1./mc.Integral())
mc.SetLineWidth(2)

ratio = data.Clone("ratio")
ratio.Divide(mc)

if doSave:
    outFile = TFile("./PU.root", "RECREATE")
    outFile.cd()
    data.Write()
    mc.Write()
    ratio.Write()
    outFile.Close()
    print "Histograms written to ./PU.root file"

if doPlot:
    if mcReweightedFileName:
        rmcFile = TFile(mcReweightedFileName, "READ")
        rmcTree = rmcFile.Get("ZCR")
        rmc = TH1F("mc", "nPV distribution", 60, 0, 60)
        rmc.Sumw2()
        rmcTree.Project("rmc", "nPV", "pileupWeight*abs(genWeight)/genWeight")
    else:
        rmc = mc.Clone("rmc")
        rmc.Multiply(ratio)
    rmc.Scale(1./rmc.Integral())
    rmc.SetLineWidth(2)
    rmc.SetLineColor(2)

    c1 = TCanvas("c1", "PileUp reweighting", 800, 800)
    c1.cd()
    rmc.Draw("H")
    mc.Draw("SAME, H")
    data.Draw("SAME, PE")
    c1.Print("PU.pdf")
    c1.Print("PU.png")
