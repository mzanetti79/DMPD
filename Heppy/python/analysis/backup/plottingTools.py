import math
from array import array
from ROOT import TStyle, TCanvas, TPad, TH1D, TLine, SetOwnership, TGraphErrors, TGraph, TMultiGraph

def plotMC(mc, signal, name, legend, *text):
    canvas = TCanvas(name,name)
    SetOwnership(canvas,False)
    mc.Draw('fhist')
    if signal: signal.Draw('hist,same')
    if legend: legend.Draw()
    for t in range(len(text)): text[t].Draw()
    raw_input('plot MC for '+name) # why the hack this is needed?!?
    canvas.Modified()
    canvas.Update()
    return canvas

class MultiCanvas:
    def __init__(self, name='', yMargin = 0.2 ):
        self.name = name
        self.frame = TCanvas(name,name) # in case set the width above
        SetOwnership(self.frame,False)
        self.mainPad = TPad(name+'mainPad', '' ,0.01,yMargin,0.99,0.99)
        self.mainPad.SetBottomMargin(0)
        self.comparisonPad = TPad(name+'comparisonPad', '' ,0.01,0.01,0.99,yMargin)
        self.comparisonPad.SetTopMargin(0)
        self.comparisonPad.SetBottomMargin(0.33);
        self.comparisonPad.SetGridy()
        self.draw()
    def draw(self):
        self.mainPad.Draw()
        self.comparisonPad.Draw()
        self.frame.Modified()
        self.frame.Update()


def compareHistograms(reference,model,name):
    """
    reference can only be a TH1*, whereas model can either
    be a TH1* or a THStack 
    """
#    comparison = TH1D('comparison'+name,'', reference.GetNbinsX(),
#                      reference.GetBinLowEdge(1),reference.GetBinLowEdge(reference.GetNbinsX())+reference.GetBinWidth(1))
    comparison = reference.Clone('comparison'+name)

    maxY,minY=2,0
    #maxY,minY=5,-5
    content, uncertainty = {}, {} 
    for bin in range(1,reference.GetNbinsX()+1):
        reference_content= reference.GetBinContent(bin)
        reference_error = reference.GetBinError(bin)**2 # squared
        model_content = 0.0
        model_error = 0.0
        if model.Class_Name()=='THStack':
            for h in model.GetHists():
                model_content+=h.GetBinContent(bin)
                model_error+=h.GetBinError(bin)**2 # squared
        else:
            model_content= model.GetBinContent(bin)
            model_error = model.GetBinError(bin)**2 # squared

        #### Data/MC ###
        if True:
            try:    
                comparison.SetBinContent(bin,min(max(reference_content/model_content, minY),maxY))
                comparison.SetBinError(bin,(reference_content/model_content)*math.sqrt(float(reference_error)/(reference_content**2) + float(model_error)/(model_content**2)))
            except: 
                comparison.SetBinContent(bin,1)
                comparison.SetBinError(bin,0)

        #### Chi ###
        if False:
            try:    
                error = math.sqrt(model_error+reference_error)
                comparison.SetBinContent(bin,min(max((reference_content - model_content)/error, minY),maxY))
                comparison.SetBinError(bin, 1 )
            except: 
                comparison.SetBinContent(bin,0)
                comparison.SetBinError(bin,1)

    #comparison.SetAxisRange(minY,maxY,'Y')
    comparison.SetAxisRange(0.5,1.5,'Y')
    return comparison



def plotDataMC(data, mc, signal, name, legend, *text):
    canvas = MultiCanvas(name)

    canvas.mainPad.cd()
    maxY = data.GetMaximum() if data.GetMaximum()> mc.GetMaximum() else mc.GetMaximum()
    data.SetAxisRange(0.05,maxY*1.5,'Y')
    data.GetYaxis().SetTitleOffset(1.5)
    data.Draw('ep')
    mc.Draw('fhist,same')
    if signal: signal.Draw('hist,same')
    data.Draw('ep,same')
    if legend: legend.Draw()
    for t in range(len(text)): text[t].Draw()
    canvas.mainPad.SetLogy()
    canvas.mainPad.Update()

    canvas.comparisonPad.cd()
    comparison = compareHistograms(data,mc,name)
    comparison.GetYaxis().SetTitle('data/MC')
    #comparison.GetYaxis().SetTitle('#chi')
    comparison.GetXaxis().SetLabelSize(0.15);
    comparison.GetXaxis().SetTitleSize(0.15);
    comparison.GetXaxis().SetTickLength(0.13);
    comparison.GetYaxis().SetNdivisions(505);
    comparison.GetYaxis().SetLabelFont(42);
    comparison.GetYaxis().SetLabelSize(0.12);
    comparison.GetYaxis().SetTitleSize(0.13);
    comparison.GetYaxis().SetTitleOffset(0.27);

    comparison.Draw()
    line = TLine(data.GetBinLowEdge(1),1,data.GetBinLowEdge(data.GetNbinsX())+data.GetBinWidth(data.GetNbinsX()),1)
    #line = TLine(data.GetBinLowEdge(1),0,data.GetBinLowEdge(data.GetNbinsX())+data.GetBinWidth(data.GetNbinsX()),0)
    line.SetLineColor(2)
    line.Draw('same')
    canvas.comparisonPad.Update()

    canvas.frame.SaveAs('plots/'+name+'.png')
    raw_input('plot data-MC for '+name) # why the hack this is needed?!?
    return canvas.frame


def plotComparison(reference, model, name, legend=None, *text):
    canvas = MultiCanvas(name)

    canvas.mainPad.cd()
    ### FIXME!! WATCH OUT!!
    #reference.Scale(1./reference.Integral(0,-1))
    #model.Scale(1./model.Integral(0,-1))
    reference.SetLineWidth(3)
    reference.SetLineColor(1)
    reference.Draw('l')
    #reference.SetMarkerStyle(20)
    #reference.Draw('p')

    model.SetLineWidth(3)
    model.SetLineColor(1)
    model.SetLineStyle(7)
    #model.Draw('l,same')
    #model.Draw('same')
    model.Draw('h,same')
    if legend: legend.Draw()
    for t in range(len(text)): text[t].Draw()
    canvas.mainPad.Update()

    canvas.comparisonPad.cd()
    comparison = compareHistograms(reference,model,name)
    comparison.GetXaxis().SetLabelSize(0.15);
    comparison.GetXaxis().SetTitleSize(0.15);
    comparison.GetXaxis().SetTickLength(0.13);
    comparison.GetYaxis().SetTitle('#chi')
    comparison.GetYaxis().SetNdivisions(505);
    comparison.GetYaxis().SetLabelFont(42);
    comparison.GetYaxis().SetLabelSize(0.12);
    comparison.GetYaxis().SetTitleSize(0.13);
    comparison.GetYaxis().SetTitleOffset(0.27);
    comparison.Draw('p')
    line = TLine(reference.GetBinLowEdge(1),0,reference.GetBinLowEdge(reference.GetNbinsX())+reference.GetBinWidth(reference.GetNbinsX()),0)
    line.SetLineColor(2)
    line.Draw('same')
    canvas.comparisonPad.Update()

    raw_input('compare reference-model for '+name) # why the hack this is needed?!?
    return canvas.frame


def computeROC(signal,bkgd):
    """
    compute ROC 
    """
    roc = {'signal':[signal,{'efficiency':[],'efficiencyError':[]}],
           'bkgd':[bkgd,{'efficiency':[],'efficiencyError':[]}]}

    for process in roc:
        for cut in range ( 1, roc[process][0].GetNbinsX(), 1 ):
            num   = roc[process][0].Integral(0, cut)
            denum = roc[process][0].Integral(0, -1)
            eff=1 
            effErr=0 
            if denum>0: 
                eff = num/denum
                effErr = math.sqrt(eff*(1-eff)/denum)
            roc[process][1]['efficiency'].append(eff)
            roc[process][1]['efficiencyError'].append(effErr)

    return TGraphErrors(len(roc[process][1]['efficiency']),
                        array('f',roc['bkgd'][1]['efficiency']),array('f',roc['signal'][1]['efficiency']),
                        array('f',roc['bkgd'][1]['efficiencyError']),array('f',roc['signal'][1]['efficiencyError']))


def plotROC(signal, bkgd, name, *text):
    canvas = MultiCanvas(name,0.5)

    canvas.mainPad.cd()
    roc = computeROC(signal,bkgd)
    roc.SetMarkerStyle(20)
    roc.SetTitle('')
    roc.Draw('apL')
    for t in range(len(text)): text[t].Draw()

    canvas.comparisonPad.cd()
    signal.Scale(1./signal.Integral(0,-1))
    bkgd.Scale(1./bkgd.Integral(0,-1))
    signal.SetLineColor(1)
    signal.SetMarkerStyle(20)
    signal.Draw('p')
    bkgd.SetLineColor(1)
    bkgd.Draw('h,same')

    canvas.frame.cd()
    canvas.frame.Modified()
    canvas.frame.cd()
    canvas.frame.SetSelected(canvas.frame)
    raw_input('ROC for '+name) # why the hack this is needed?!?
    return canvas.frame



def setStyle():
    print "setting TDR style"

    tdrStyle = TStyle("tdrStyle","Style for P-TDR")

    kWhite = 0

    tdrStyle.SetPalette(1)

    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasColor(kWhite)
    tdrStyle.SetCanvasDefH(800) 
    tdrStyle.SetCanvasDefW(1000) 
    tdrStyle.SetCanvasDefX(0)   
    tdrStyle.SetCanvasDefY(0)

    tdrStyle.SetPadBorderMode(0)
    tdrStyle.SetPadColor(kWhite)
    tdrStyle.SetPadGridX(False)
    tdrStyle.SetPadGridY(False)
    tdrStyle.SetGridColor(0)
    tdrStyle.SetGridStyle(3)
    tdrStyle.SetGridWidth(1)

    tdrStyle.SetFrameBorderMode(0)
    tdrStyle.SetFrameBorderSize(1)
    tdrStyle.SetFrameFillColor(0)
    tdrStyle.SetFrameFillStyle(0)
    tdrStyle.SetFrameLineColor(1)
    tdrStyle.SetFrameLineStyle(1)
    tdrStyle.SetFrameLineWidth(1)

    tdrStyle.SetHistFillColor(0)
    tdrStyle.SetHistLineColor(1)
    tdrStyle.SetHistLineStyle(0)
    tdrStyle.SetHistLineWidth(1)

    tdrStyle.SetErrorX(0.)

    tdrStyle.SetMarkerStyle(20)

    tdrStyle.SetOptFit(1)
    tdrStyle.SetFitFormat("5.4g")
    tdrStyle.SetFuncColor(2)
    tdrStyle.SetFuncStyle(1)
    tdrStyle.SetFuncWidth(1)

    tdrStyle.SetOptDate(0)

    tdrStyle.SetOptFile(0)
    #tdrStyle.SetOptStat(0111) 
    tdrStyle.SetOptStat(0) 
    tdrStyle.SetStatColor(kWhite)
    tdrStyle.SetStatFont(42)
    tdrStyle.SetStatFontSize(0.025)
    tdrStyle.SetStatTextColor(1)
    tdrStyle.SetStatFormat("6.4g")
    tdrStyle.SetStatBorderSize(0)
    tdrStyle.SetStatH(0.1)
    tdrStyle.SetStatW(0.15)

    tdrStyle.SetPadTopMargin(0.05)
    tdrStyle.SetPadBottomMargin(0.1)
    tdrStyle.SetPadLeftMargin(0.1)
    tdrStyle.SetPadRightMargin(0.05)


    tdrStyle.SetTitleFont(42)
    tdrStyle.SetTitleColor(1)
    tdrStyle.SetTitleTextColor(1)
    tdrStyle.SetTitleFillColor(10)
    tdrStyle.SetTitleFontSize(0.05)

    tdrStyle.SetTitleColor(1, "XYZ")
    tdrStyle.SetTitleFont(42, "XYZ")
    tdrStyle.SetTitleSize(0.06, "XYZ")
    tdrStyle.SetTitleXOffset(0.9)
    tdrStyle.SetTitleYOffset(1.05)

    tdrStyle.SetLabelColor(1, "XYZ")
    tdrStyle.SetLabelFont(42, "XYZ")
    tdrStyle.SetLabelOffset(0.007, "XYZ")
    tdrStyle.SetLabelSize(0.05, "XYZ")

    tdrStyle.SetAxisColor(1, "XYZ")
    tdrStyle.SetStripDecimals(1)
    tdrStyle.SetTickLength(0.03, "XYZ")
    tdrStyle.SetNdivisions(505, "XYZ")
    tdrStyle.SetPadTickX(1)
    tdrStyle.SetPadTickY(1)

    tdrStyle.SetOptLogx(0)
    tdrStyle.SetOptLogy(0)
    tdrStyle.SetOptLogz(0)
    tdrStyle.cd()

