import os
from pprint import pprint

pjoin = os.path.join

# Fragments
pythia_fragment = ''' 
import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        pythia8aMCatNLOSettingsBlock,
        processParameters = cms.vstring(
            'Higgs:useBSM = on',
            '25:onMode = off',
            '25:onIfMatch = 15 -15',
            '35:onMode = off',
            '35:onIfMatch = 15 -15',
            '36:onMode = off',
            '36:onIfMatch = 15 -15'
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    'pythia8aMCatNLOSettings',
                                    'pythia8PSweightsSettings'
        )
    )
)

'''

lhe_fragment = '''import FWCore.ParameterSet.Config as cms

# link to cards:
# __LINK__

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('__GRIDPACK__'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    generateConcurrently = cms.untracked.bool(False),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

__PYTHIA_FRAGMENT__
'''

# Link to proc card on GitHub
proc_card_link = 'https://github.com/cms-sw/genproductions/pull/3379'

# Mass points
mass_points = [
    (100,400),
    (100,40),
    (100,50),
    (110,200),
    (110,250),
    (110,300),
    (110,400),
    (110,40),
    (110,50),
    (125,400),
    (125,40),
    (125,50),
    (140,400),
    (140,40),
    (140,50),
    (160,400),
    (160,40),
    (160,50),
    (180,200),
    (180,250),
    (180,300),
    (180,400),
    (180,40),
    (180,50),
    (200,200),
    (200,250),
    (200,300),
    (200,400),
    (200,40),
    (200,50),
    (250,250),
    (250,300),
    (250,400),
    (250,40),
    (250,50),
    (300,300),
    (300,400),
    (300,40),
    (300,50),
    (300,600),
    (400,400),
    (400,600),
    (600,600),
    (60,40),
    (60,50),
    (60,60),
    (60,70),
    (60,80),
    (60,90),
    (70,40),
    (70,50),
    (70,70),
    (70,80),
    (70,90),
    (800,600),
    (80,40),
    (80,50),
    (80,80),
    (80,90),
    (90,40),
    (90,50),
    (90,90)
]

# Gridpack locations at cvmfs
gridpack_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc700/MadGraph5_aMCatNLO/ZstarTophi{__MASS1__}A{__MASS2__}To4Tau_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'
gridpack_locs = {}

for mass_point in mass_points:
    gridpack_locs[mass_point] = gridpack_template.format(__MASS1__ = mass_point[0], __MASS2__ = mass_point[1])

# Dataset names
datasetname_template = 'ZstarToPhiATo4Tau_Mphi{__MASS1__}_MA{__MASS2__}_TuneCP5_13TeV-amcatnlo-pythia8'
datasetnames = {}

for mass_point in mass_points:
    datasetnames[mass_point] = datasetname_template.format(__MASS1__ = mass_point[0], __MASS2__ = mass_point[1])

# Fill request information for 2017 and 2018
request_information = {}
for year in [2016,2017,2018]:
    request_information[year] = {}
    for mass_point in mass_points:
        gridpack_path = gridpack_locs[mass_point]
        dataset_name = datasetnames[mass_point]
        request_information[year][mass_point] = {
            'gridpack' : gridpack_path,
            'Events' : 200000, # 10M events for each mass point
            'Filter efficiency' : 1.0, # random value for now, check later
            'Match efficiency' : 1.0, # random value for now, check later
            'proc_card_link' : proc_card_link,
            'fragment' : lhe_fragment.replace('__LINK__', proc_card_link).replace('__PYTHIA_FRAGMENT__', pythia_fragment).replace('__GRIDPACK__', gridpack_path),
            'generator' : 'Madgraph+Pythia8',
            'Dataset name' : dataset_name,
            'notes' : dataset_name.split('_')
        }

