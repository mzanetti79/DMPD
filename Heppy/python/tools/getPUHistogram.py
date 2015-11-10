#! /usr/bin/env python

import os
from array import array
from ROOT import gStyle, TFile, TH1F, TCanvas, TLegend
gStyle.SetOptStat(0)

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-d", "--dataFile", action="store", type="string", default=False, dest="dataFileName")
parser.add_option("-m", "--mcFile", action="store", type="string", default=False, dest="mcFileName")
parser.add_option("-r", "--mcReweightedFile", action="store", type="string", default=False, dest="mcReweightedFileName")
parser.add_option("-p", "--plot", action="store_true", default=False, dest="doPlot")
parser.add_option("-s", "--save", action="store_true", default=False, dest="doSave")

(options, args) = parser.parse_args()

dataFileName = options.dataFileName
mcFileName = options.mcFileName
mcReweightedFileName = options.mcReweightedFileName
doPlot = options.doPlot
doSave = options.doSave


#python getPUHistogram.py -p -s -m ../../test/Batch/DYJetsToLL_M50_amcatnloFXFX_pythia8_v3/Loop/tree.root -d /lustre/cmswork/zucchett/CMSSW_7_4_12_patch4/src/DMPD/Heppy/test/Batch/SingleMuon_Run2015D_PromptReco_v3/Loop/tree.root

#print "\n\n\n"
#print dataFileName, mcFileName, mcReweightedFileName


#dataFile = TFile(dataFileName, "READ")
#dataTree = dataFile.Get("ZCR")
#data = TH1F("data", "nPV distribution", 60, 0, 60)
#data.Sumw2()
#dataTree.Project("data", "nPV", "(HLT_BIT_HLT_IsoMu27_v && lepton1_isMuon && lepton1_tightId && lepton1_pt>20 && lepton1_relIso04<0.12 && lepton2_isMuon && lepton2_pt>15 && Z_mass>70 && Z_mass<110)")
#data.Scale(1./data.Integral())
#data.SetMarkerSize(1.25)
#data.SetMarkerStyle(20)

#mcFile = TFile(mcFileName, "READ")
#mcTree = mcFile.Get("ZCR")
#mc = TH1F("mc", "nPV distribution", 60, 0, 60)
#mc.Sumw2()
#mcTree.Project("mc", "nPV", "abs(genWeight)/genWeight * (HLT_BIT_HLT_IsoMu27_v && lepton1_isMuon && lepton1_tightId && lepton1_pt>20 && lepton1_relIso04<0.12 && lepton2_isMuon && lepton2_pt>15 && Z_mass>70 && Z_mass<110)")
#mc.Scale(1./mc.Integral())
#mc.SetLineWidth(2)

#ratio = data.Clone("ratio")
#ratio.Divide(mc)

#if doSave:
#    outFile = TFile("./PU.root", "RECREATE")
#    outFile.cd()
#    data.Write()
#    mc.Write()
#    ratio.Write()
#    outFile.Close()
#    print "Histograms written to ./PU.root file"

#if doPlot:
#    if mcReweightedFileName:
#        rmcFile = TFile(mcReweightedFileName, "READ")
#        rmcTree = rmcFile.Get("ZCR")
#        rmc = TH1F("mc", "nPV distribution", 60, 0, 60)
#        rmc.Sumw2()
#        rmcTree.Project("rmc", "nPV", "pileupWeight*abs(genWeight)/genWeight * (HLT_BIT_HLT_IsoMu27_v && lepton1_isMuon && lepton1_tightId && lepton1_pt>20 && lepton1_relIso04<0.12 && lepton2_isMuon && lepton2_pt>15 && Z_mass>70 && Z_mass<110)")
#    else:
#        rmc = mc.Clone("rmc")
#        rmc.Multiply(ratio)
#    rmc.Scale(1./rmc.Integral())
#    rmc.SetLineWidth(2)
#    rmc.SetLineColor(2)

#    c1 = TCanvas("c1", "PileUp reweighting", 800, 800)
#    c1.cd()
#    rmc.Draw("H")
#    mc.Draw("SAME, H")
#    data.Draw("SAME, PE")
#    c1.Print("PU.pdf")
#    c1.Print("PU.png")



#pileupCalc.py -i ../JSON/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt --inputLumiJSON ../JSON/pileup_latest.txt --calcMode true --minBiasXsec 69000 --maxPileupBin 50 --numPileupBins 50 PU_69000.root
#pileupCalc.py -i ../JSON/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt --inputLumiJSON ../JSON/pileup_latest.txt --calcMode true --minBiasXsec 72450 --maxPileupBin 50 --numPileupBins 50 PU_72450.root
#pileupCalc.py -i ../JSON/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt --inputLumiJSON ../JSON/pileup_latest.txt --calcMode true --minBiasXsec 65550 --maxPileupBin 50 --numPileupBins 50 PU_65550.root


def setPUHistogram():
    # https://raw.githubusercontent.com/cms-sw/cmssw/CMSSW_7_4_X/SimGeneral/MixingModule/python/mix_2015_25ns_Startup_PoissonOOTPU_cfi.py
    probValue = [4.8551E-07, 1.74806E-06, 3.30868E-06, 1.62972E-05, 4.95667E-05, 0.000606966, 0.003307249, 0.010340741, 0.022852296, 0.041948781, 0.058609363, 0.067475755, 0.072817826, 0.075931405, 0.076782504, 0.076202319, 0.074502547, 0.072355135, 0.069642102, 0.064920999, 0.05725576, 0.047289348, 0.036528446, 0.026376131, 0.017806872, 0.011249422, 0.006643385, 0.003662904, 0.001899681, 0.00095614, 0.00050028, 0.000297353, 0.000208717, 0.000165856, 0.000139974, 0.000120481, 0.000103826, 8.88868E-05, 7.53323E-05, 6.30863E-05, 5.21356E-05, 4.24754E-05, 3.40876E-05, 2.69282E-05, 2.09267E-05, 1.5989E-05, 4.8551E-06, 2.42755E-06, 4.8551E-07, 2.42755E-07, 1.21378E-07, 4.8551E-08]
    mc = TH1F("mc", "nPV distribution", 50, 0, 50)
    mc.Sumw2()
    for i in range(50): mc.SetBinContent(i+1, probValue[i])
    mc.SetLineWidth(3)
    mc.SetLineColor(1)
    mc.SetLineStyle(2)
    mc.Scale(1./mc.Integral())
    
    puFile = TFile("./PU/PU_80000.root", "READ")
    data = puFile.Get("pileup")
    data.SetLineWidth(3)
    data.SetLineColor(1)
    data.Scale(1./data.Integral())
    
    puUpFile = TFile("./PU/PU_84000.root", "READ")
    dataUp = puUpFile.Get("pileup")
    dataUp.SetLineWidth(3)
    dataUp.SetLineColor(634)
    dataUp.Scale(1./dataUp.Integral())
    
    puDownFile = TFile("./PU/PU_76000.root", "READ")
    dataDown = puDownFile.Get("pileup")
    dataDown.SetLineWidth(3)
    dataDown.SetLineColor(598)
    dataDown.Scale(1./dataDown.Integral())
    
    ratio = data.Clone("ratio")
    ratioUp = dataUp.Clone("ratioUp")
    ratioDown = dataDown.Clone("ratioDown")
    
    ratio.Divide(mc)
    ratioUp.Divide(mc)
    ratioDown.Divide(mc)
    
    outFile = TFile("./PU/PU.root", "RECREATE")
    outFile.cd()
    mc.Write()
    data.Write()
    dataUp.Write()
    dataDown.Write()
    ratio.Write()
    ratioUp.Write()
    ratioDown.Write()
    outFile.Close()
    print "Histograms written to ./PU/PU.root file"
    
    leg = TLegend(0.65, 0.7, 0.98, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.SetHeader("pile-up reweighting")
    leg.AddEntry(dataUp, "Up", "pl")
    leg.AddEntry(data, "Central", "pl")
    leg.AddEntry(dataDown, "Down", "pl")
    leg.AddEntry(mc, "MC 25ns", "pl")
    
    c1 = TCanvas("c1", "PileUp reweighting", 800, 800)
    c1.cd()
    c1.GetPad(0).SetTopMargin(0.06)
    c1.GetPad(0).SetRightMargin(0.05)
    c1.GetPad(0).SetTicks(1, 1)
    dataDown.SetTitle(";number of true interactions")
    dataDown.GetXaxis().SetRangeUser(0., 30)
    dataDown.Draw("HIST")
    dataUp.Draw("SAME, HIST")
    data.Draw("SAME, HIST")
    mc.Draw("SAME, L")
    leg.Draw()
    c1.Print("PU/PU.pdf")
    c1.Print("PU/PU.png")
    
setPUHistogram()
