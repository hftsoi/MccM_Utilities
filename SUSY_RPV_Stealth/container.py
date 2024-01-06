import os
from pprint import pprint

pjoin = os.path.join

# Fragments
pythia_fragment = ''' 
__fragment__
'''

# Link to proc card on GitHub
proc_card_link = 'https://github.com/cms-sw/genproductions/'

# Mass points
fragment_files = [
    'SMS-RChiWZ_LSPtoudb-mNLSP150To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'SMS-RChiWH_LSPtoudb-mNLSP200To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'SMS-RChiWZ_LSPtouds-mNLSP150To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'SMS-RChiWH_LSPtouds-mNLSP200To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'SMS-RChiWWpm_LSPtoudb-mNLSP150To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'SMS-RChiWWpm_LSPtouds-mNLSP150To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'Stealth_TChiWZ_Sget90Tobb_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'Stealth_TChiWZ_Sget90ToGluGlu_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'Stealth_TChiWH_Sget90Tobb_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'Stealth_TChiWH_Sget90ToGluGlu_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'Stealth_TChiWWpm_Sget90Tobb_TuneCP5_13TeV-madgraphMLM-pythia8.py',
    'Stealth_TChiWWpm_Sget90ToGluGlu_TuneCP5_13TeV-madgraphMLM-pythia8.py'
]

# Gridpack locations at cvmfs
gridpacks = [
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1C1_v2/SMS-C1C1_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1C1_v2/SMS-C1C1_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1N2_v2/SMS-C1N2_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1C1_v2/SMS-C1C1_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1C1_v2/SMS-C1C1_mC1-*_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'
]

nEvents = [
    28000000,
    26400000,
    28000000,
    26400000,
    28000000,
    28000000,
    1800000,
    1800000,
    1800000,
    1800000,
    1800000,
    1800000
]

# Dataset names
datasetnames = [
    'SMS-RChiWZ_LSPtoudb-mNLSP150To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8',
    'SMS-RChiWH_LSPtoudb-mNLSP200To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8',
    'SMS-RChiWZ_LSPtouds-mNLSP150To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8',
    'SMS-RChiWH_LSPtouds-mNLSP200To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8',
    'SMS-RChiWWpm_LSPtoudb-mNLSP150To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8',
    'SMS-RChiWWpm_LSPtouds-mNLSP150To1200_mLSP25To600_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Stealth_TChiWZ_Sget90Tobb_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Stealth_TChiWZ_Sget90ToGluGlu_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Stealth_TChiWH_Sget90Tobb_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Stealth_TChiWH_Sget90ToGluGlu_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Stealth_TChiWWpm_Sget90Tobb_TuneCP5_13TeV-madgraphMLM-pythia8',
    'Stealth_TChiWWpm_Sget90ToGluGlu_TuneCP5_13TeV-madgraphMLM-pythia8'
]

# Fill request information for 2017 and 2018
request_information = {}
for year in ['2016','2016apv','2017','2018']:
    request_information[year] = {}
    for i in range(len(datasetnames)):
        gridpack_path = gridpacks[i]
        dataset_name = datasetnames[i]
        
        with open(fragment_files[i], 'r') as file:
            frag = file.read()
            
        if year == '2016':
            nevts = int(nEvents[i]*0.46)
        elif year == '2016apv':
            nevts = int(nEvents[i]*0.54)
        elif year == '2017' or year == '2018':
            nevts = nEvents[i]
            
        request_information[year][i] = {
            'gridpack' : gridpack_path,
            'Events' : nevts,
            'Filter efficiency' : 1.0,
            'Match efficiency' : 1.0,
            'proc_card_link' : proc_card_link,
            'fragment' : pythia_fragment.replace('__fragment__', frag),
            'generator' : 'Madgraph+Pythia8',
            'Dataset name' : dataset_name,
            'notes' : dataset_name.split('_')
        }
