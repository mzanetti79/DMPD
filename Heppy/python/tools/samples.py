from collections import OrderedDict

sample = {
    'Data' : {
        'order' : 0,
        #'files' : ['SingleMuon_Run2015B_PromptReco_v1'],
        'files' : ['SingleMuon_Run2015B_17Jul2015_v1'],
        'fillcolor' : 0,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linestyle' : 1,
        'label' : "Data",
        'weight': 1.,
    },
    'DYJetsToLL_amcatnlo' : {
        'order' : 1,
        'files' : ['DYJetsToLL_M50_amcatnloFXFX_pythia8_v3'],
        'fillcolor' : 418,
        'fillstyle' : 1001,
        'linecolor' : 418,
        'linestyle' : 1,
        'label' : "Z(ll) + jets",
        'weight': 1.,
    },
    'WJetsToLNu_amcatnlo' : {
        'order' : 2,
        'files' : ['WJetsToLNu_amcatnloFXFX_pythia8_v1'],
        'fillcolor' : 881,
        'fillstyle' : 1001,
        'linecolor' : 881,
        'linestyle' : 1,
        'label' : "W + jets",
        'weight': 1.,
    },
    'TTbar' : {
        'order' : 3,
        #'files' : ['TT_powheg_pythia8_v2'],
        'files' : ['TTJets_madgraphMLM_pythia8_v2'],
        'fillcolor' : 798,
        'fillstyle' : 1001,
        'linecolor' : 798,
        'linestyle' : 1,
        'label' : "t#bar{t}, single t",
        'weight': 1.,
    },
    'VV' : {
        'order' : 4,
        'files' : ['ZZ_pythia8_v3','WZ_pythia8_v1','WW_pythia8_v1'],
        'fillcolor' : 602,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linestyle' : 1,
        'label' : "VV",
        'weight': 1.,
    },
    # Signals 623 625 628 629 633 634 635 636
    'ZZhllbb_M600' : {
        'order' : 0,
        'files' : ['ZprimeToZhToZlephbb_narrow_M600_madgraph_v1'],
        'fillcolor' : 0,
        'fillstyle' : 1,
        'linecolor' : 623,
        'linestyle' : 1,
        'label' : "m_{Z'} = 1000 GeV",
        'weight': 1.,
    },
    # Dummy entry for background sum
    'BkgSum' : {
        'order' : 0,
        'files' : [],
        'fillcolor' : 1,
        'fillstyle' : 3003,
        'linecolor' : 1,
        'linestyle' : 1,
        'label' : "MC Stat",
        'weight': 1.,
    },
}

#samplegroups = {

    ##'QCD' : {
        ##'order' : 1,
        ##'files' : ['QCD_HT100To250','QCD_HT250To500','QCD_HT500To1000','QCD_HT1000ToInf'],
        ###'files' : ['QCD_HT500To1000','QCD_HT1000ToInf'],
        ##'color' : 920,#9909,
        ##'lcolor': 921,#9909,
        ##'label' : 'QCD',
        ##'weight': 1.,
        ##},

    #'singleT' : {
        #'order' : 2,
        #'files' : ['TToLeptons_schannel','TbarToLeptons_schannel','TToLeptons_tchannel','TbarToLeptons_tchannel','T_tWchannel','Tbar_tWchannel'],
        #'color' : 9908,
        #'lcolor': 9918,
        #'label' : 'single t',
        #'weight': 1.,
        #},

    #'TT' : {
        #'order' : 3,
        #'files' : ['TTJets'],
        #'color' : 9903,
        #'lcolor': 9913,
        #'label' : 't#bar{t}',
        #'weight': 1.,
        #},

    #'Gamma' : {
        #'order' : 4,
        #'files' : ['GJets_HT100to200','GJets_HT200to400','GJets_HT400to600','GJets_HT600toInf'],
        #'color' : 9904,
        #'lcolor': 9914,
        #'label' : '#gamma + jets',
        #'weight': 1.,
        #},

    #'Zmumu' : {
        #'order' : 5,
        #'files' : ['DYJetsToLL_M50_HT100to200','DYJetsToLL_M50_HT200to400','DYJetsToLL_M50_HT400to600','DYJetsToLL_M50_HT600toInf'],
        #'color' : 9905,
        #'lcolor': 9915,
        #'label' : 'Z#rightarrow#mu#mu + jets',
        #'weight': 1.,
        #},

    #'Wmunu' : {
        #'order' : 6,
        #'files' : ['WJetsToLNu_HT100to200','WJetsToLNu_HT200to400','WJetsToLNu_HT400to600','WJetsToLNu_HT600toInf'],
        #'color' : 9901,
        #'lcolor': 9911,
        #'label' : 'W#rightarrow#mu#nu + jets',
        #'weight': 1.,
        #},

    #'Znunu' : {
        #'order' : 7,
        #'files' : ['ZJetsToNuNu_HT100to200','ZJetsToNuNu_HT200to400','ZJetsToNuNu_HT400to600','ZJetsToNuNu_HT600toInf'],
        #'color' : 9906,
        #'lcolor': 9916,
        #'label' : 'Z#rightarrow#nu#nu + jets',
        #'weight': 1.,
        #},

    #'signal_DMM1AV' : {
        #'order' : 9,
        #'files' : ['DM_Monojet_M1_AV'],
        #'color' : 0,
        #'lcolor': 9957,
        #'label' : 'DM M1 AV [#sigma=1pb]',
        #'weight': 1.,
        #},

    #'signal_DMM10AV' : {
        #'order' : 10,
        #'files' : ['DM_Monojet_M10_AV'],
        #'color' : 0,
        #'lcolor': 9956,
        #'label' : 'DM M10 AV [#sigma=1pb]',
        #'weight': 1.,
        #},
    
    #'signal_DMM10V' : {
        #'order' : 11,
        #'files' : ['DM_Monojet_M10_V'],
        #'color' : 0,
        #'lcolor': 9955,
        #'label' : 'DM M10 V [#sigma=1pb]',
        #'weight': 1.,
        #},
    
    #'signal_DMM100AV' : {
        #'order' : 12,
        #'files' : ['DM_Monojet_M100_AV'],
        #'color' : 0,
        #'lcolor': 9954,
        #'label' : 'DM M100 AV [#sigma=1pb]',
        #'weight': 1.,
        #},
        
    #'signal_DMM100V' : {
        #'order' : 13,
        #'files' : ['DM_Monojet_M100_V'],
        #'color' : 0,
        #'lcolor': 9953,
        #'label' : 'DM M100 V [#sigma=1pb]',
        #'weight': 1.,
        #},
    
    #'signal_DMM1000AV' : {
        #'order' : 14,
        #'files' : ['DM_Monojet_M1000_AV'],
        #'color' : 0,
        #'lcolor': 9952,
        #'label' : 'DM M1000 AV [#sigma=1pb]',
        #'weight': 1.,
        #},
    
    #'signal_DMM1000V' : {
        #'order' : 15,
        #'files' : ['DM_Monojet_M1000_V'],
        #'color' : 0,
        #'lcolor': 9951,
        #'label' : 'DM M1000 V [#sigma=1pb]',
        #'weight': 1.,
        #},

    #'signal_ZnunuHbb' : {
        #'order' : 16,
        #'files' : ['ZH_HToBB_ZToNuNu'],
        #'color' : 60,
        #'lcolor': 60,
        #'label' : 'Z#rightarrow#nu#nu + H#rightarrowbb [#sigma=1pb]',
        #'weight': 1.,
        #},

    #'signal_DMMonoB' : {
        #'order' : 17,
        #'files' : ['DM_MonoB'],
        #'color' : 70,
        #'lcolor': 70,
        #'label' : 'DM-b/bb [#sigma=1pb]',
        #'weight': 1.,
        #},

    #'signal_DMMonoVbb' : {
        #'order' : 18,
        #'files' : ['DM_MonoVbb'],
        #'color' : 80,
        #'lcolor': 80,
        #'label' : 'DM-Z(bb) [#sigma=1pb]',
        #'weight': 1.,
        #},

    #'signal_DMMonoH' : {
        #'order' : 19,
        #'files' : ['DM_MonoH'],
        #'color' : 90,
        #'lcolor': 90,
        #'label' : 'DM-H(bb) [#sigma=1pb]',
        #'weight': 1.,
        #},

#}

samplegroups = {

    'QCD' : {
        'order' : 1,
        #'files' : ['QCD_HT100To250','QCD_HT250To500','QCD_HT500To1000','QCD_HT1000ToInf'],
        #'files' : ['QCD_HT500To1000','QCD_HT1000ToInf'],
        'files' : ['QCD_HT1000ToInf'],
        'color' : 920,#9909,
        'lcolor': 921,#9909,
        'label' : 'QCD',
        'weight': 1.,
        'region': ['SR','ZCR','WCR','GCR'],
        },

    'Top' : {
        'order' : 2,
        'files' : ['Top'],
        'color' : 9903,
        'lcolor': 9913,
        'label' : 't',
        'weight': 1.,
        'region': ['SR','ZCR','WCR','GCR'],
        },

    'Gamma' : {
        'order' : 4,
        'files' : ['GJets'],
        'color' : 9904,
        'lcolor': 9914,
        'label' : '#gamma + jets',
        'weight': 1.,
        'region': ['SR','ZCR','WCR','GCR'],
        },

    'Zmumu' : {
        'order' : 5,
        'files' : ['DYJetsToLL'],
        'color' : 9905,
        'lcolor': 9915,
        'label' : 'Z#rightarrow#mu#mu + jets',
        'weight': 1.,
        'region': ['SR','ZCR','WCR','GCR'],        
        },

    'Wmunu' : {
        'order' : 6,
        'files' : ['WJetsToLNu'],
        'color' : 9901,
        'lcolor': 9911,
        'label' : 'W#rightarrow#mu#nu + jets',
        'weight': 1.,
        'region': ['SR','ZCR','WCR','GCR'],        
        },

    'Znunu' : {
        'order' : 7,
        'files' : ['ZJetsToNuNu'],
        'color' : 9906,
        'lcolor': 9916,
        'label' : 'Z#rightarrow#nu#nu + jets',
        'weight': 1.,
        'region': ['SR','ZCR','WCR','GCR'],        
        },

    #'signal_DMM1AV' : {
        #'order' : 9,
        #'files' : ['DM_Monojet_M1_AV'],
        #'color' : 0,
        #'lcolor': 9957,
        #'label' : 'DM M1 AV [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},

    #'signal_DMM10AV' : {
        #'order' : 10,
        #'files' : ['DM_Monojet_M10_AV'],
        #'color' : 0,
        #'lcolor': 9956,
        #'label' : 'DM M10 AV [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},
    
    #'signal_DMM10V' : {
        #'order' : 11,
        #'files' : ['DM_Monojet_M10_V'],
        #'color' : 0,
        #'lcolor': 9955,
        #'label' : 'DM M10 V [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},
    
    'signal_DMM100AV' : {
        'order' : 12,
        'files' : ['DM_Monojet_M100_AV'],
        'color' : 0,
        'lcolor': 9954,
        'label' : 'DM M100 AV [#sigma=1pb]',
        'weight': 1.,
        'region': ['SR'],        
        },
        
    #'signal_DMM100V' : {
        #'order' : 13,
        #'files' : ['DM_Monojet_M100_V'],
        #'color' : 0,
        #'lcolor': 9953,
        #'label' : 'DM M100 V [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},
    
    #'signal_DMM1000AV' : {
        #'order' : 14,
        #'files' : ['DM_Monojet_M1000_AV'],
        #'color' : 0,
        #'lcolor': 9952,
        #'label' : 'DM M1000 AV [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},
    
    #'signal_DMM1000V' : {
        #'order' : 15,
        #'files' : ['DM_Monojet_M1000_V'],
        #'color' : 0,
        #'lcolor': 9951,
        #'label' : 'DM M1000 V [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},

    #'signal_ZnunuHbb' : {
        #'order' : 16,
        #'files' : ['ZH_HToBB_ZToNuNu'],
        #'color' : 60,
        #'lcolor': 60,
        #'label' : 'Z#rightarrow#nu#nu + H#rightarrowbb [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},

    #'signal_DMMonoB' : {
    #    'order' : 17,
    #    'files' : ['DM_MonoB'],
    #    'color' : 0,
    #    'lcolor': 9950,
    #    'label' : 'DM+bb [#sigma=1pb]',
    #    'weight': 1.,
    #    'region': ['SR'],        
    #    },

    #'signal_DMMonoVbb' : {
        #'order' : 18,
        #'files' : ['DM_MonoVbb'],
        #'color' : 80,
        #'lcolor': 80,
        #'label' : 'DM-Z(bb) [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},

    #'signal_DMMonoH' : {
        #'order' : 19,
        #'files' : ['DM_MonoH'],
        #'color' : 90,
        #'lcolor': 90,
        #'label' : 'DM-H(bb) [#sigma=1pb]',
        #'weight': 1.,
        #'region': ['SR'],        
        #},

}
    
samplegroups = OrderedDict(sorted(samplegroups.iteritems(), key=lambda x: x[1]['order']))
