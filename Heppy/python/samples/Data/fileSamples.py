import PhysicsTools.HeppyCore.framework.config as cfg
from DMPD.Heppy.samples.Data.fileLists import datasamples

sampleSingleMuon_Run2015B_17Jul2015_v1 = cfg.Component(
        files      = datasamples["SingleMuon_Run2015B_17Jul2015_v1"]["files"],
        name       = "SingleMuon_Run2015B_17Jul2015_v1",
        splitFactor= 20,
)


samplesSingleMuon_Run2015B_PromptReco_v1 = cfg.Component(
        files      = datasamples["SingleMuon_Run2015B_PromptReco_v1"]["files"],
        name       = "SingleMuon_Run2015B_PromptReco_v1",
        splitFactor= 20,
)
