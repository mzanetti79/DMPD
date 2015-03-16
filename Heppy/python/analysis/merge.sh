#/bin/bash

filedir=/lustre/cmsdata/DM/ntuples/Prod_v01/weighted

for s in DYJetsToLL GJets QCD WJetsToLNu ZJetsToNuNu
do
  echo Merging $s...
  hadd -f $s.root $filedir/$s\_*.root
  #rm $sample_*.root
done
echo Done.

