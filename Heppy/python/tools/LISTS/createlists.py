#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable=C0301,C0103,R0914,R0903

# system modules
import os
import re
import time
import json
import urllib
import urllib2
import httplib
import cookielib
from   optparse import OptionParser
from   math import log
from   types import GeneratorType

import optparse
usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-i", "--input", action="store", type="string", dest="SAMPLEFILE", default="samplefile.txt")
parser.add_option("-f", "--folder", action="store", type="string", dest="FOLDER", default="fileLists/")
parser.add_option("-l", "--legnaro", action="store_true", default=False, dest="LEGNARO")
parser.add_option("-d", "--dataonly", action="store_true", default=False, dest="DATAONLY")
parser.add_option("-n", "--nodasquery", action="store_true", default=False, dest="NODASQUERY")
parser.add_option("-v", "--valid", action="store_true", default=False, dest="VALID")

(options, args) = parser.parse_args()

SAMPLEFILE = options.SAMPLEFILE
FOLDER     = options.FOLDER+'/'
LEGNARO    = options.LEGNARO
DATAONLY   = options.DATAONLY
NODASQUERY = options.NODASQUERY
VALID      = options.VALID

if not os.path.exists(FOLDER): os.makedirs(FOLDER)

local = ' site=T2_IT_Legnaro' if LEGNARO else ''

valid = ' status=VALID' if VALID else ''

if not NODASQUERY:
    os.system('voms-proxy-init --voms cms')

    SAMPLES = [ i for i in open(SAMPLEFILE,'r').read().splitlines()]

    for s in SAMPLES:
        os.system('python das_client.py --query=\"dataset dataset='+s+local+valid+'\" --limit=0 --format=plain > '+'tmplist.tmp')
        subSAMPLES = [ j for j in open('tmplist.tmp','r').read().splitlines()]
        for ss in subSAMPLES:  
            if DATAONLY and 'Run2015' not in ss: continue
            filename = ss.split('/')[1]+'_'+ss.split('/')[2] if 'Run2015' in ss else ss.split('/')[1]+ss.split('/')[2][-3:]
            print filename
            os.system('python das_client.py --query=\"file dataset='+ss+local+'\" --limit=0 --format=plain > '+ FOLDER + filename)
            os.system('python das_client.py --query=\"dataset dataset='+ss+' | grep dataset.nevents\" --limit=0 >> '+ FOLDER + filename)
            #os.system('python das_client.py --query=\"dataset='+ss+local+'\" | grep dataset.nevents')            
        os.system('rm tmplist.tmp')
    pass 
pass

if not os.path.exists(FOLDER+'/DATA/'): os.makedirs(FOLDER+'/DATA/')
fdata = open(FOLDER+"DATA/fileLists.py",'w')        
fdata.write('datasamples   = {\n')

if not os.path.exists(FOLDER+'/MC/'): os.makedirs(FOLDER+'/MC/')
fmc = open(FOLDER+"MC/fileLists.py",'w')        
fmc.write('mcsamples   = {\n')

for dirname, dirnames, filenames in os.walk(FOLDER):
    for filename in filenames:
        files   = [f for f in open(os.path.join(dirname, filename),'r').read().splitlines()]
        nevents = files[-1]
        if 'Run2015' in filename:
            fdata.write('  \''+filename+'\' : {\n')
            fdata.write('    \'files\'   : [\n')
            for f in files[:-1]:    
                fdata.write('      \'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms/'+f+'\',\n')
            fdata.write('    ],\n')
            fdata.write('    \'xsec\'    : 0.0,\n')
            fdata.write('    \'nevents\' : '+str(nevents)+'.,\n')   
            fdata.write('  },\n\n')
        else:
            fmc.write('  \''+filename+'\' : {\n')
            fmc.write('    \'files\'   : [\n')
            for f in files[:-1]:    
                fmc.write('      \'dcap://t2-srm-02.lnl.infn.it/pnfs/lnl.infn.it/data/cms/'+f+'\',\n')
            fmc.write('    ],\n')
            fmc.write('    \'xsec\'    : 0.0,\n')
            fmc.write('    \'nevents\' : '+str(nevents)+'.,\n')   
            fmc.write('  },\n\n')            

fdata.write('\n}\n')
fmc.write('\n}\n')
