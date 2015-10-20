#! /usr/bin/env python

import os
from array import array
from ROOT import gStyle, TFile, TH1F, TCanvas, TLegend
gStyle.SetOptStat(0)

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-n", "--nloFile", action="store", type="string", default=False, dest="nloFileName")
parser.add_option("-l", "--loFile", action="store", type="string", default=False, dest="loFileName")
parser.add_option("-p", "--plot", action="store_true", default=False, dest="doPlot")
parser.add_option("-s", "--save", action="store_true", default=False, dest="doSave")

(options, args) = parser.parse_args()

nloFileName = options.nloFileName
loFileName = options.loFileName
doPlot = options.doPlot
doSave = options.doSave


bins = array('d', [0]+[x for x in range(1, 20, 1)]+[x for x in range(20, 50, 5)]+[x for x in range(50, 100, 10)]+[x for x in range(100, 200, 20)]+[x for x in range(200, 500, 100)]+[x for x in range(500, 1000, 250)]+[2500]) #[x for x in range(1000, 2500, 500)]

nloFile = TFile(nloFileName, "READ")
nloHist = nloFile.Get("Gen/GenZpt")
if doSave: nlo = nloHist.Rebin(len(bins)-1, "nlo", bins)
else: nlo = nloHist.Rebin(25, "nlo")
nlo.Scale(1./nloHist.Integral())

loFile = TFile(loFileName, "READ")
loHist = loFile.Get("Gen/GenZpt")
if doSave: lo = loHist.Rebin(len(bins)-1, "lo", bins)
else: lo = loHist.Rebin(25, "lo")
lo.Scale(1./loHist.Integral())

lo.SetLineWidth(2)
nlo.SetLineWidth(2)
lo.SetLineColor(602)
nlo.SetLineColor(634)

ratio = nlo.Clone("ratio")
ratio.Divide(lo)
ratio.GetYaxis().SetTitle("NLO / LO")
ratio.SetLineColor(1)

if doSave:
    outFile = TFile("./Vpt.root", "RECREATE")
    outFile.cd()
    nlo.Write()
    lo.Write()
    ratio.Write()
    outFile.Close()
    print "Histograms written to ./Vpt.root file"

if doPlot:
    def setHistStyle(hist, r=1.1):
        hist.GetXaxis().SetTitleSize(hist.GetXaxis().GetTitleSize()*r)
        hist.GetYaxis().SetTitleSize(hist.GetYaxis().GetTitleSize()*r)
        hist.GetXaxis().SetLabelOffset(hist.GetXaxis().GetLabelOffset()*r*r*r*r*2)
        hist.GetXaxis().SetTitleOffset(hist.GetXaxis().GetTitleOffset()*r*r)
        hist.GetYaxis().SetTitleOffset(hist.GetYaxis().GetTitleOffset()*r)
        if hist.GetXaxis().GetTitle().find("GeV") != -1: # and not hist.GetXaxis().IsVariableBinSize()
            div = (hist.GetXaxis().GetXmax() - hist.GetXaxis().GetXmin()) / hist.GetXaxis().GetNbins()
            hist.GetYaxis().SetTitle("Events / %.1f GeV" % div)

    def setTopPad(TopPad, r=4):
        TopPad.SetPad("TopPad", "", 0., 1./r, 1.0, 1.0, 0, -1, 0)
        TopPad.SetTopMargin(0.24/r)
        TopPad.SetBottomMargin(0.)
        TopPad.SetRightMargin(0.05)
        TopPad.SetTicks(1, 1)

    def setBotPad(BotPad, r=4):
        BotPad.SetPad("BotPad", "", 0., 0., 1.0, 1./r, 0, -1, 0)
        BotPad.SetTopMargin(0.)
        BotPad.SetBottomMargin(r/10.)
        BotPad.SetRightMargin(0.05)
        BotPad.SetTicks(1, 1)

    def setBotStyle(h, r=4):
        h.GetXaxis().SetLabelSize(h.GetXaxis().GetLabelSize()*(r-1));
        h.GetXaxis().SetLabelOffset(h.GetXaxis().GetLabelOffset()*(r-1));
        h.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize()*(r-1));
        h.GetYaxis().SetLabelSize(h.GetYaxis().GetLabelSize()*(r-1));
        h.GetYaxis().SetNdivisions(505);
        h.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize()*(r-1));
        h.GetYaxis().SetTitleOffset(h.GetYaxis().GetTitleOffset()/(r-1));
        h.GetYaxis().SetRangeUser(0., 2.)
    
    c1 = TCanvas("c1", "Signals", 800, 600)
    c1.Divide(1, 2)
    setTopPad(c1.GetPad(1), 4)
    setBotPad(c1.GetPad(2), 4)
    c1.cd(1)
    c1.GetPad(1).SetTopMargin(0.06)
    c1.GetPad(1).SetRightMargin(0.05)
    c1.GetPad(1).SetTicks(1, 1)
    if doSave: c1.GetPad(1).SetLogx()
    c1.GetPad(1).SetLogy()
    setHistStyle(loHist)
    loHist.GetXaxis().SetLabelOffset(0.01)
    
    lo.Draw("HIST")
    nlo.Draw("SAME,HIST")
    
    leg = TLegend(0.6, 0.75, 0.95, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.AddEntry(nlo, "NLO", "pfl")
    leg.AddEntry(lo, "LO", "pfl")
    leg.Draw()
    
    c1.cd(2)
    setBotStyle(ratio)
    if doSave: c1.GetPad(2).SetLogx()
    ratio.GetXaxis().SetMoreLogLabels()
    ratio.GetXaxis().SetNoExponent()
    ratio.GetYaxis().SetRangeUser(0.5, 1.5)
    ratio.Draw("HE")
    
    c1.Print("Vpt.png")
    c1.Print("Vpt.pdf")
    raw_input()



















