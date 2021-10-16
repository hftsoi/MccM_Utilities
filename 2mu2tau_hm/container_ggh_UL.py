import os
from pprint import pprint

pjoin = os.path.join

# Fragments
pythia_fragment = ''' 
import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

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
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    )
    )
)

ProductionFilterSequence = cms.Sequence(generator)
'''

lhe_fragment = '''import FWCore.ParameterSet.Config as cms

# link to cards:
# __LINK__

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('__GRIDPACK__'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True)
)

__PYTHIA_FRAGMENT__
'''

# Link to proc card on GitHub
proc_card_link = 'https://github.com/cms-sw/genproductions/pull/2973'

# Mass points
mass_points = [15,20,25,30,35,40,45,50,55,60]

# Gridpack locations at cvmfs
gridpack_template = '/cvmfs/'
gridpack_locs = {}

for mass_point in mass_points:
    gridpack_locs[mass_point] = gridpack_template.format(__MASS__ = mass_point)

# Dataset names
datasetname_template = 'GluGluToHToAA_AToMuMu_AToTauTau_M-{__MASS__}_TuneCP5_13TeV_madgraph_pythia8'
datasetnames = {}

for mass_point in mass_points:
    datasetnames[mass_point] = datasetname_template.format(__MASS__ = mass_point)

# Fill request information for 2017 and 2018
request_information = {}
for year in [2016,2017,2018]:
    request_information[year] = {}
    for mass_point in mass_points:
        gridpack_path = gridpack_locs[mass_point]
        dataset_name = datasetnames[mass_point]
        request_information[year][mass_point] = {
            'gridpack' : gridpack_path,
            'Events' : 125000, # 10M events for each mass point
            'Filter efficiency' : 1.0, # random value for now, check later
            'Match efficiency' : 1.0, # random value for now, check later
            'proc_card_link' : proc_card_link,
            'fragment' : lhe_fragment.replace('__LINK__', proc_card_link).replace('__PYTHIA_FRAGMENT__', pythia_fragment).replace('__GRIDPACK__', gridpack_path),
            'generator' : 'Madgraph+Pythia8',
            'Dataset name' : dataset_name,
            'notes' : dataset_name.split('_')
        }

