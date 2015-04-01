#/bin/bash

filedir=/lustre/cmsdata/DM/ntuples/Prod_v02/weighted

for s in DYJetsToLL GJets QCD WJetsToLNu ZJetsToNuNu 
do
  echo Merging $s...
  hadd -f $s.root $filedir/$s\_*.root
  #rm $sample_*.root
done
hadd -f ST.root $filedir/T\_*.root $filedir/Tbar\_*.root
cp $filedir/TT.root .
echo Done.

