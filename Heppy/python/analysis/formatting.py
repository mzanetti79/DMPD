#! /usr/bin/env python
from ROOT import RooDataSet, RooRealVar, RooArgSet, RooFit, RooAbsData

RooDataSet.setDefaultStorageType(RooAbsData.Tree)

def getRooDataSet(tree,variables,cfg):
    rooRealVars = {}
    for variable in variables:
        xLow = variable.bins[0] if not (variable.variable == 'met' and cfg.has_key('met_cut')) else cfg['met_cut']
        rooRealVars[variable] = RooRealVar(variable.variable,'',xLow,variable.bins[-1])
    weight = RooRealVar('weight','',1)
    argSet = RooArgSet(weight)
    for rooRealVar in rooRealVars: argSet.add(rooRealVars[rooRealVar])
    tree_name = tree.GetName()
    print tree_name
    rooDataSet = RooDataSet('roo'+tree_name,'',argSet,RooFit.WeightVar(weight)) 

    for i in range(tree.GetSelectedRows()):
        for j, rooRealVar in enumerate(variables): rooRealVars[rooRealVar].setVal(tree.GetVal(j)[i]) 
        if tree_name=='data': weight.setVal(1)
        else: 
            weightValue = tree.GetVal(len(variables))[i]*float(cfg['lumi']) # weight*lumi 
            weight.setVal(weightValue) 
        rooDataSet.add(argSet, weight.getVal()) 

    return rooDataSet
