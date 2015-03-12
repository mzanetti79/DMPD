#/bin/sh

dir=../../../PhysicsTools/Heppy/python/analyzers/objects
cp $dir/JetAnalyzer.py $dir/FatJetAnalyzer.py

sed -i.bak -e 's/JetAnalyzer/FatJetAnalyzer/g' -e 's/event.jets/event.fatJets/g' -e 's/event.cleanJets/event.cleanFatJets/g' -e 's/event.discardedJets/event.discardedFatJets/g' $dir/FatJetAnalyzer.py

