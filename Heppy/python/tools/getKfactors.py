#! /usr/bin/env python

import os, sys, getopt
import copy, math
from array import array
from ROOT import gROOT, gStyle, gRandom
from ROOT import TFile, TChain, TTree, TCut, TH1F, TH2F, THStack, TGraph, TGaxis
from ROOT import TStyle, TCanvas, TPad, TLegend, TLatex, TText
from DMPD.Heppy.tools.samples import *
from DMPD.Heppy.samples.Spring15.xSections import xsections
from utils import *

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
#gStyle.SetErrorX(1)
RATIO       = 4

#NTUPLEDIR   = "/lustre/cmsdata/DM/ntuples/Prod_v20/"
NTUPLEDIR   = "/homeui/pazzini/lustreSymbLink/CMSSW_7_4_14/src/DMPD/Heppy/test/Prod_v21_MCall/"


ROOTFILE = "./scalefactors_v2.root"


def getKfactors():
    inFile = TFile(ROOTFILE, "READ")
    znlo = inFile.Get("znlo012/znlo012_nominal")
    zlo = inFile.Get("zlo/zlo_nominal")
    wnlo = inFile.Get("wnlo012/wnlo012_nominal")
    wlo = inFile.Get("wlo/wlo_nominal")
    
    znlo.Scale(1./znlo.Integral())
    zlo.Scale(1./zlo.Integral())
    wnlo.Scale(1./wnlo.Integral())
    wlo.Scale(1./wlo.Integral())
    
    zkf = znlo.Clone("Zkfactor")
    zkf.Divide(zlo)
    wkf = wnlo.Clone("Wkfactor")
    wkf.Divide(wlo)
    
    
    outFile = TFile("./Kfactors.root", "RECREATE")
    outFile.cd()
    zkf.Write()
    wkf.Write()
    outFile.Close()
    print "Histograms written to ./Kfactors.root file"
    
    

def deriveKfactors(type="Lhe", bkg="WJetsToLNu"):
    boson = 'W' if bkg.startswith('W') else 'Z'

    nloFile = TFile(NTUPLEDIR + sample[bkg]['files'][0] + "/Loop/tree.root", "READ")
    nloHist = nloFile.Get(type+"/"+type+boson+"pt")
    nloHist.Rebin(10)
    nloHist.Scale(xsections[sample[bkg]['files'][0][:-3]] / nloFile.Get('Counters/Counter').GetBinContent(0))
    nloHist.GetXaxis().SetRangeUser(0., 1000)
    nloHist.SetLineWidth(2)
    nloHist.SetLineColor(1)
    
    loSamples = sample[bkg+'_HT']['files'] #['DYJetsToLL_M50_madgraphMLM_pythia8_v1'] + 
    ranges = [[100., 200.], [200., 400.], [400., 600.], [600., 1.e99]]
    n = len(loSamples)
    loFile = [None]*n
    loHist = [None]*n
    for i in range(n):
        loFile[i] = TFile(NTUPLEDIR + loSamples[i] + "/Loop/tree.root", "READ")
        loHist[i] = loFile[i].Get(type+"/"+type+boson+"pt")
        loHist[i].Rebin(10)
        loHist[i].Scale(xsections[loSamples[i][:-3]] / loFile[i].Get('Counters/Counter').GetBinContent(0))
        loHist[i].GetXaxis().SetRangeUser(0., 1000)
        loHist[i].SetLineWidth(2)
        loHist[i].SetLineColor(416+i)
    
    
    kfactors = [1, 1, 1, 1]
    
    for k in reversed(range(n)):
        lowbin, highbin = nloHist.FindBin(ranges[k][0]+1)+1, nloHist.GetNbinsX()+1
        nloInt = nloHist.Integral(lowbin, highbin)
        for i in list(reversed(range(k+1, n))): nloInt -= loHist[i].Integral(lowbin, highbin)
        kfactors[k] = nloInt/loHist[k].Integral(lowbin, highbin)
        print "k-factor", k, "in range", nloHist.GetXaxis().GetBinLowEdge(lowbin), "-", nloHist.GetXaxis().GetBinUpEdge(highbin), ": %.3f" % kfactors[k]
        loHist[k].Scale(kfactors[k])
    print "kfactors =", kfactors
    
    loSum = loHist[0].Clone("Sum")
    loSum.SetLineColor(2)
    for i in range(1, n): loSum.Add(loHist[i])
    
    ratio = nloHist.Clone("ratio")
    ratio.GetYaxis().SetTitle("NLO / LO")
    ratio.Divide(loSum)
    
    leg = TLegend(0.7, 0.65, 0.95, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.AddEntry(nloHist, "inclusive NLO", "pl")
    leg.AddEntry(loSum, "exclusive LO sum", "pl")
    
    
    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.Divide(1, 2)
    setTopPad(c1.GetPad(1), RATIO)
    setBotPad(c1.GetPad(2), RATIO)
    c1.cd(1)
    c1.GetPad(bool(RATIO)).SetTopMargin(0.06)
    c1.GetPad(bool(RATIO)).SetRightMargin(0.05)
    c1.GetPad(bool(RATIO)).SetTicks(1, 1)
    c1.GetPad(1).SetLogy()
    setHistStyle(nloHist)
    nloHist.Draw("HE")
    for i in range(n): loHist[i].Draw("SAME,HE")
    loSum.Draw("SAME,HE")
    leg.Draw()
    
    c1.cd(2)
    setBotStyle(ratio)
    ratio.GetYaxis().SetRangeUser(0.8, 1.2)
    ratio.Draw("HE")
    
    print "Ratio:", nloHist.Integral(nloHist.FindBin(100), nloHist.FindBin(1.e99))/loSum.Integral(nloHist.FindBin(100)+1, nloHist.FindBin(1.e99))
    
    print "Summary:"
    for i in range(n):
        print "    '"+loSamples[i][:-3]+"' : %.3f"',' % kfactors[i]
    
    c1.Print("plots/Hist/"+type+bkg+"Ratio.png")
    c1.Print("plots/Hist/"+type+bkg+"Ratio.pdf")
    if not gROOT.IsBatch(): raw_input("Press Enter to continue...")



def GenZpt():
    #kfactors = [1.5992641737053377, 1.388778036943685, 1.5360789955333298, 1.1347900247061118]
    bkg = "DYJetsToNuNu"
    
    nloFile = TFile(NTUPLEDIR + sample[bkg]['files'][0] + ".root", "READ")
    nloHist = nloFile.Get("Gen/GenZpt")
    nloHist.Rebin(10)
    nloHist.GetXaxis().SetRangeUser(0., 1000)
    nloHist.SetLineWidth(2)
    nloHist.SetLineColor(1)
    
    loSamples = sample['DYJetsToLL_HT']['files'] #['DYJetsToLL_M50_madgraphMLM_pythia8_v1'] + 
    ranges = [[100., 200.], [200., 400.], [400., 600.], [600., 1.e99]]
    n = len(loSamples)
    loFile = [None]*n
    loHist = [None]*n
    for i in range(n):
        loFile[i] = TFile(NTUPLEDIR + loSamples[i] + ".root", "READ")
        loHist[i] = loFile[i].Get("Gen/GenZpt")
        #loHist[i].Scale(kfactors[i])
        loHist[i].Rebin(10)
        loHist[i].GetXaxis().SetRangeUser(0., 1000)
        loHist[i].SetLineWidth(2)
        loHist[i].SetLineColor(416+i)
    
    loSum = loHist[0].Clone("Sum")
    loSum.SetLineColor(2)
    for i in range(1, n): loSum.Add(loHist[i])
    
    ratio = nloHist.Clone("ratio")
    ratio.GetYaxis().SetTitle("NLO / LO")
    ratio.Divide(loSum)
    
    leg = TLegend(0.7, 0.65, 0.95, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.AddEntry(nloHist, "inclusive NLO", "pl")
    leg.AddEntry(loSum, "exclusive LO sum", "pl")
    
    
    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.Divide(1, 2)
    setTopPad(c1.GetPad(1), RATIO)
    setBotPad(c1.GetPad(2), RATIO)
    c1.cd(1)
    c1.GetPad(bool(RATIO)).SetTopMargin(0.06)
    c1.GetPad(bool(RATIO)).SetRightMargin(0.05)
    c1.GetPad(bool(RATIO)).SetTicks(1, 1)
    c1.GetPad(1).SetLogy()
    setHistStyle(nloHist)
    nloHist.Draw("HE")
    for i in range(n): loHist[i].Draw("SAME,HE")
    loSum.Draw("SAME,HE")
    leg.Draw()
    
    c1.cd(2)
    setBotStyle(ratio)
    ratio.GetYaxis().SetRangeUser(0.8, 1.2)
    ratio.Draw("HE")
    
#    c1.Print("plots/Hist/GenZptRatio.png")
#    c1.Print("plots/Hist/GenZptRatio.pdf")
    if not gROOT.IsBatch(): raw_input("Press Enter to continue...")



def LheHT():
    kfactors = [1.398, 1.065, 0.887, 0.738]
    bins = array('d', [0., 100., 200., 400., 600., 1000.])
    
    nloFile = TFile(NTUPLEDIR + "/DYJetsToLL_M50_amcatnloFXFX_pythia8_v3.root", "READ")
    nloHist = nloFile.Get("Lhe/LheHT").Rebin(len(bins)-1, "NLO", bins)
    nloHist.SetLineWidth(2)
    nloHist.SetLineColor(1)
    
    #loSamples = ['DYJetsToLL_M50_madgraphMLM_pythia8_v1']
    loSamples = sample['DYJetsToLL_HT']['files']
    n = len(loSamples)
    loFile = [None]*n
    loHist = [None]*n
    for i in range(n):
        loFile[i] = TFile(NTUPLEDIR + loSamples[i] + ".root", "READ")
        loHist[i] = loFile[i].Get("Lhe/LheHT").Rebin(len(bins)-1, "NLO", bins)
        #loHist[i].Scale(kfactors[i])
        loHist[i].SetLineWidth(2)
        loHist[i].SetLineColor(416+i)
    
    loSum = loHist[0].Clone("Sum")
    loSum.SetLineColor(2)
    for i in range(1, n): loSum.Add(loHist[i])
    
    ratio = nloHist.Clone("ratio")
    ratio.Divide(loSum)
    ratio.GetYaxis().SetTitle("NLO / LO")
    
    leg = TLegend(0.7, 0.65, 0.95, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.AddEntry(nloHist, "inclusive NLO", "pl")
    leg.AddEntry(loHist[0], "exclusive LO", "pl")
    leg.AddEntry(loSum, "exclusive LO sum", "pl")
    
    
    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.Divide(1, 2)
    setTopPad(c1.GetPad(1), RATIO)
    setBotPad(c1.GetPad(2), RATIO)
    c1.cd(1)
    c1.GetPad(bool(RATIO)).SetTopMargin(0.06)
    c1.GetPad(bool(RATIO)).SetRightMargin(0.05)
    c1.GetPad(bool(RATIO)).SetTicks(1, 1)
    c1.GetPad(1).SetLogy()
    setHistStyle(nloHist)
    nloHist.Draw("HE")
    for i in range(n): loHist[i].Draw("SAME,HE")
    loSum.Draw("SAME,HE")
    leg.Draw()
    
    c1.cd(2)
    setBotStyle(ratio)
    ratio.GetYaxis().SetRangeUser(0., 2.)
    ratio.Draw("HE")
    
    for i in range(nloHist.GetNbinsX()): print "nlo/lo scale factor in range", nloHist.GetXaxis().GetBinLowEdge(i+1), "-", nloHist.GetXaxis().GetBinUpEdge(i+1), ": %.3f" % (nloHist.GetBinContent(i+1)//loSum.GetBinContent(i+2) if loSum.GetBinContent(i+2) > 0 else 0)
    
#    c1.Print("plots/Hist/LheHTRatio.png")
#    c1.Print("plots/Hist/LheHTRatio.pdf")
    if not gROOT.IsBatch(): raw_input("Press Enter to continue...")


#getKfactors()
deriveKfactors("Gen", "DYJetsToLL")
deriveKfactors("Gen", "DYJetsToNuNu")
deriveKfactors("Gen", "WJetsToLNu")
#GenZpt()
