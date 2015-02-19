from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
import PhysicsTools.HeppyCore.framework.config as cfg
from ROOT import heppy

class MuonAnalyzer( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(MuonAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.effectiveArea  = getattr(cfg_ana, 'effectiveArea',  "Phys14_25ns_v1")

    def declareHandles(self):
        super(MuonAnalyzer, self).declareHandles()
        self.handles['muons'] = AutoHandle(self.cfg_ana.muons,"std::vector<pat::Muon>")            
        self.handles['rho'] = AutoHandle( self.cfg_ana.rho, 'double')

    def beginLoop(self, setup):
        super(MuonAnalyzer,self).beginLoop(setup)

    def makeAllMuons(self, event):
        allmuons = map( Muon, self.handles['muons'].product() )
        for mu in allmuons:
            mu.rho = float(self.handles['rho'].product()[0])
            # Attach EAs for isolation:
            if self.effectiveArea == "Data2012":
                if   aeta < 1.0  : mu.EffectiveArea03 = 0.382;
                elif aeta < 1.47 : mu.EffectiveArea03 = 0.317;
                elif aeta < 2.0  : mu.EffectiveArea03 = 0.242;
                elif aeta < 2.2  : mu.EffectiveArea03 = 0.326;
                elif aeta < 2.3  : mu.EffectiveArea03 = 0.462;
                else             : mu.EffectiveArea03 = 0.372;
                if   aeta < 1.0  : mu.EffectiveArea04 = 0.674;
                elif aeta < 1.47 : mu.EffectiveArea04 = 0.565;
                elif aeta < 2.0  : mu.EffectiveArea04 = 0.442;
                elif aeta < 2.2  : mu.EffectiveArea04 = 0.515;
                elif aeta < 2.3  : mu.EffectiveArea04 = 0.821;
                else             : mu.EffectiveArea04 = 0.660;
            elif self.effectiveArea == "Phys14_25ns_v1":
                aeta = abs(mu.eta())
                if   aeta < 0.800: mu.EffectiveArea03 = 0.0913
                elif aeta < 1.300: mu.EffectiveArea03 = 0.0765
                elif aeta < 2.000: mu.EffectiveArea03 = 0.0546
                elif aeta < 2.200: mu.EffectiveArea03 = 0.0728
                else:              mu.EffectiveArea03 = 0.1177
                if   aeta < 0.800: mu.EffectiveArea04 = 0.1564
                elif aeta < 1.300: mu.EffectiveArea04 = 0.1325
                elif aeta < 2.000: mu.EffectiveArea04 = 0.0913
                elif aeta < 2.200: mu.EffectiveArea04 = 0.1212
                else:              mu.EffectiveArea04 = 0.2085
            else: raise RuntimeError,  "Unsupported value for mu_effectiveAreas: can only use Data2012 (rho: ?) and Phys14_v1 (rho: fixedGridRhoFastjetAll)"
            # Attach the vertex to them, for dxy/dz calculation
            mu.associatedVertex = event.goodVertices[0]
            # Attach the isolation
            if self.cfg_ana.isoCorr=="rhoArea" :
                mu.absIso03 = (mu.pfIsolationR03().sumChargedHadronPt + max( mu.pfIsolationR03().sumNeutralHadronEt +  mu.pfIsolationR03().sumPhotonEt - mu.rho * mu.EffectiveArea03,0.0))
                mu.absIso04 = (mu.pfIsolationR04().sumChargedHadronPt + max( mu.pfIsolationR04().sumNeutralHadronEt +  mu.pfIsolationR04().sumPhotonEt - mu.rho * mu.EffectiveArea04,0.0))
            elif self.cfg_ana.isoCorr=="deltaBeta" :
                mu.absIso03 = (mu.pfIsolationR03().sumChargedHadronPt + max( mu.pfIsolationR03().sumNeutralHadronEt +  mu.pfIsolationR03().sumPhotonEt -  mu.pfIsolationR03().sumPUPt/2,0.0))
                mu.absIso04 = (mu.pfIsolationR04().sumChargedHadronPt + max( mu.pfIsolationR04().sumNeutralHadronEt +  mu.pfIsolationR04().sumPhotonEt -  mu.pfIsolationR04().sumPUPt/2,0.0))
            else :
                raise RuntimeError, "Unsupported isoCorr name '" + str(self.cfg_ana.isoCorr) +  "'! For now only 'rhoArea' and 'deltaBeta' are supported."
            mu.relIso03 = mu.absIso03/mu.pt()
            mu.relIso04 = mu.absIso04/mu.pt()
        return allmuons


    def selectMuons(self, event):
        """
        select the good muons
        """
        event.selectedMuons = []
        allmuons = self.makeAllMuons(event)
        for mu in allmuons:
            if (mu.track().isNonnull() and 
                mu.pt()>self.cfg_ana.muon_pt and
                abs(mu.dxy())<self.cfg_ana.muon_dxy and abs(mu.dz())<self.cfg_ana.muon_dz):
                event.selectedMuons.append(mu)
        event.selectedMuons.sort(key = lambda l : l.pt(), reverse = True)

    def process(self, event):
        self.readCollections( event.input )
        self.selectMuons(event)
        return True

#A default config
setattr(MuonAnalyzer,"defaultConfig",cfg.Analyzer(
    verbose=False,
    class_object=MuonAnalyzer,
    muons='slimmedMuons',
    rho= 'fixedGridRhoFastjetAll',
    muon_id  = "POG_ID_Loose",
    muon_pt  = 5,
    muon_dxy = 0.5,
    muon_dz  = 1.0,
    muon_relIso = 0.4,
    isoCorr = "rhoArea" ,
    effectiveAreas = "Phys14_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1')
    )
)
