from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import ROOT

class ZmmAnalyzer( Analyzer ):
    '''Analyze and select Z->mm events
    '''
    def declareHandles(self):
        super(ZmmAnalyzer, self).declareHandles()

    def beginLoop(self,setup):
        super(ZmmAnalyzer,self).beginLoop(setup)
        self.handles['met'] = AutoHandle( 'slimmedMETs', 'std::vector<pat::MET>' ) #tmp
        if "outputfile" in setup.services :
            setup.services["outputfile"].file.cd()
            self.inputCounter = ROOT.TH1F("hCounts","hCounts",1,0,2)

    def selectZ(self,event):
        if not len(event.selectedMuons) == 2: return False
        if not event.selectedMuons[0].charge() != event.selectedMuons[1].charge(): return False
	#event.Z = ROOT.reco.Particle.LorentzVector(0.,0.,0.,0.)        
        event.Z = event.selectedMuons[0].p4() + event.selectedMuons[1].p4() 
        return True

    def makeMET(self,event):
        event.met = self.handles['met'].product()[0] # tmp
	event.fakeMET = ROOT.reco.Particle.LorentzVector(0.,0.,0.,0.)
        event.fakeMET = event.met.p4() + event.Z

    def process(self, event):
        self.readCollections( event.input )
        self.inputCounter.Fill(1)
        if not self.selectZ(event): return False
	self.makeMET(event)
        return True


        return True
