#! /usr/bin/env python
import math
from ROOT import TStyle, TCanvas, TPad, TH1D, TLine, SetOwnership, TGraphErrors, TGraph, TMultiGraph

class MultiCanvas:
    def __init__(self, name='', border_y = 0.2, margin=0.01):
        self.name = name
        self.canvas = TCanvas(name,name) 
        SetOwnership(self.canvas,False)
        self.mainPad = TPad(name+'mainPad', '' ,0+margin,border_y,1-margin,1-margin)
        self.mainPad.SetBottomMargin(0.0) ##?
        self.comparisonPad = TPad(name+'comparisonPad', '' ,0+margin,0+margin,1-margin,border_y)
        self.comparisonPad.SetTopMargin(0)
        self.comparisonPad.SetBottomMargin(0.33);
        self.comparisonPad.SetGridy()
        self.draw()
    def draw(self):
        self.mainPad.Draw()
        self.comparisonPad.Draw()
        self.canvas.Modified()
        self.canvas.Update()



class Plotter():
    def __init__(self, analyzer,method='data/MC'):
        self.analyzer = analyzer
        self.name = analyzer.cfg.name
        self.histos = analyzer.formatted_histograms
        self.method=method
        self.parameters = [0.5,1.5,1] if self.method=='data/MC' else [-0.5,0.5,0]
        self.setStyle()
        self.multi_canvas = MultiCanvas(self.name)
    

    def plot(self):
        if self.histos.has_key('data'): self.plotDataMC()
        else: self.plotMC()

    def plotMC(self):
        self.histos['background'].Draw('fhist')
        self.histos['background'].GetXaxis().SetTitle(self.analyzer.setup.observable.labelX)
        self.histos['background'].GetYaxis().SetTitle(self.analyzer.setup.observable.labelY)
        self.histos['background'].GetXaxis().SetNdivisions(505)
        self.histos['background'].GetYaxis().SetNdivisions(505)
        try: self.histos['signal'].Draw('hist,same') 
        except:
            if self.analyzer.cfg.parametersSet['verbosity'] > 2: print 'signal not plotted'
        self.legend.Draw()

    def plotDataMC(self):
        # main canvas
        self.multi_canvas.mainPad.cd()
        self.histos['data'].Draw('ep')
        ## setup
        self.histos['data'].GetXaxis().SetLabelSize(0) ##?
        self.histos['data'].GetXaxis().SetTitle(self.analyzer.setup.observable.labelX)
        self.histos['data'].GetYaxis().SetTitle(self.analyzer.setup.observable.labelY)
        self.histos['data'].GetXaxis().SetNdivisions(505)
        self.histos['data'].GetYaxis().SetNdivisions(505)
        maxY = self.histos['data'].GetMaximum() if self.histos['data'].GetMaximum()> self.histos['background'].GetMaximum() else self.histos['background'].GetMaximum()
        self.histos['data'].SetAxisRange(0.05,maxY*1.3,'Y')
        self.histos['data'].GetYaxis().SetTitleOffset(1.5)
        ## background MC
        self.histos['background'].Draw('fhist,same')
        ## signal MC
        try: self.histos['signal'].Draw('hist,same') 
        except:
            if self.analyzer.cfg.parametersSet['verbosity'] > 2: print 'signal not plotted'
        self.histos['data'].Draw('ep,same')
        ## legend
        self.analyzer.legend.Draw()
        ## canvas
        self.multi_canvas.mainPad.SetLogy()
        self.multi_canvas.mainPad.Update()

        # comparison canvas
        self.multi_canvas.comparisonPad.cd()
        self.comparison = self.compareHistograms(self.histos['data'],self.histos['background'])
        self.comparison.GetYaxis().SetTitle(self.method)
        self.comparison.GetYaxis().CenterTitle()
        self.comparison.GetXaxis().SetLabelSize(0.15);
        self.comparison.GetXaxis().SetTitleSize(0.15);
        self.comparison.GetXaxis().SetTickLength(0.13);
        self.comparison.GetYaxis().SetNdivisions(505);
        self.comparison.GetYaxis().SetLabelFont(42);
        self.comparison.GetYaxis().SetLabelSize(0.12);
        self.comparison.GetYaxis().SetTitleSize(0.15);
        self.comparison.GetYaxis().SetTitleOffset(0.35);

        self.comparison.Draw('ep')
        line = TLine(self.histos['data'].GetBinLowEdge(1),self.parameters[2],
                     self.histos['data'].GetBinLowEdge(self.histos['data'].GetNbinsX())+self.histos['data'].GetBinWidth(self.histos['data'].GetNbinsX()),self.parameters[2])
        line.SetLineColor(2)
        line.Draw('same')
        self.multi_canvas.comparisonPad.Update()


        
    def compareHistograms(self, reference, model):
        """
        reference can only be a TH1*, whereas model can either be a TH1* or a THStack 
        """
        comparison = reference.Clone('comparison'+self.name)
        content, uncertainty = {}, {} 
        for bin in range(1,reference.GetNbinsX()+1):
            reference_content= reference.GetBinContent(bin)
            reference_error = reference.GetBinError(bin)**2 # squared
            model_content, model_error = 0.0, 0.0
            if model.Class_Name()=='THStack':
                for h in model.GetHists():
                    model_content+=h.GetBinContent(bin)
                    model_error+=h.GetBinError(bin)**2 # squared
            else:
                model_content= model.GetBinContent(bin)
                model_error = model.GetBinError(bin)**2 # squared

            #### Data/MC ###
            if self.method=='data/MC':
                try:    
                    comparison.SetBinContent(bin,min(max(reference_content/model_content, self.parameters[0]),self.parameters[1]))
                    comparison.SetBinError(bin,(reference_content/model_content)*math.sqrt(float(reference_error)/(reference_content**2) + float(model_error)/(model_content**2)))
                except: 
                    comparison.SetBinContent(bin,1)
                    comparison.SetBinError(bin,0)

            #### Chi ###
            if self.method=='Chi':
                try:    
                    error = math.sqrt(model_error+reference_error)
                    comparison.SetBinContent(bin,min(max((reference_content - model_content)/error, minY),maxY))
                    comparison.SetBinError(bin, 1 )
                except: 
                    comparison.SetBinContent(bin,0)
                    comparison.SetBinError(bin,1)

        comparison.SetAxisRange(self.parameters[0],self.parameters[1],'Y')
        return comparison



    def setStyle(self):
        self.style = TStyle('mz style','style for mz plots')
        self.style.SetPalette(1)
        self.style.SetOptStat(0)

        self.style.SetCanvasBorderMode(0)
        self.style.SetCanvasColor(0)
        self.style.SetCanvasDefH(800) 
        self.style.SetCanvasDefW(1000) 
        self.style.SetCanvasDefX(0)   
        self.style.SetCanvasDefY(0)
        self.style.SetPadBorderMode(0)
        self.style.SetPadColor(0)
        self.style.SetPadGridX(False)
        self.style.SetPadGridY(False)
        self.style.SetGridColor(0)
        self.style.SetGridStyle(3)
        self.style.SetGridWidth(1)
        self.style.SetFrameBorderMode(0)
        self.style.SetFrameBorderSize(1)
        self.style.SetFrameFillColor(0)
        self.style.SetFrameFillStyle(0)
        self.style.SetFrameLineColor(1)
        self.style.SetFrameLineStyle(1)
        self.style.SetFrameLineWidth(1)
        self.style.SetHistFillColor(0)
        self.style.SetHistLineColor(1)
        self.style.SetHistLineStyle(0)
        self.style.SetHistLineWidth(1)
        self.style.SetMarkerStyle(20)
        self.style.SetOptFit(1)
        self.style.SetFitFormat("5.4g")
        self.style.SetFuncColor(2)
        self.style.SetFuncStyle(1)
        self.style.SetFuncWidth(1)
        self.style.SetOptDate(0)
        self.style.SetOptFile(0)
        self.style.SetTitleFont(42)
        self.style.SetStripDecimals(1)
        self.style.SetTickLength(0.03, "XYZ")
        self.style.SetNdivisions(505, "XYZ")
        self.style.SetPadTickX(1)
        self.style.SetPadTickY(1)
        self.style.SetOptLogx(0)
        self.style.SetOptLogy(0)
        self.style.SetOptLogz(0)
        self.style.cd()
