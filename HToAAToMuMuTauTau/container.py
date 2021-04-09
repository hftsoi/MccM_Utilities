import os
from pprint import pprint

pjoin = os.path.join

# Fragments
pythia_fragment = ''' 
import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
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
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

__PYTHIA_FRAGMENT__
'''

# Link to proc card on GitHub
proc_card_link = 'https://github.com/cms-sw/genproductions/pull/2848, https://github.com/cms-sw/genproductions/blob/fb1ef8b3df0ab35b1cfcc7c992449538293b1ce6/bin/MadGraph5_aMCatNLO/cards/ggh01_Toa01a01_Tomumutautau/haa_h125_10_gp/ggh01_M125_Toa01a01_M10_Tomumutautau_proc_card.dat'

# Mass points
mass_points = [
    (125,3.6),
    (125,4),
    (125,5),
    (125,6),
    (125,7),
    (125,8),
    (125,9),
    (125,10),
    (125,11),
    (125,12),
    (125,13),
    (125,14),
    (125,15),
    (125,16),
    (125,17),
    (125,18),
    (125,19),
    (125,20),
    (125,21),
    (250,5),
    (250,10),
    (250,15),
    (250,20),
    (500,5),
    (500,10),
    (500,15),
    (500,20),
    (500,25),
    (750,10),
    (750,15),
    (750,20),
    (750,25),
    (750,30),
    (1000,10),
    (1000,20),
    (1000,30),
    (1000,40),
    (1000,50)
]

# Gridpack locations at cvmfs
gridpack_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/ggh01_M{__MASS1__}_Toa01a01_M{__MASS2__}_Tomumutautau/v1/ggh01_M{__MASS1__}_Toa01a01_M{__MASS2__}_Tomumutautau_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'
gridpack_locs = {}

for mass_point in mass_points:
    gridpack_locs[mass_point] = gridpack_template.format(__MASS1__ = mass_point[0], __MASS2__ = mass_point[1])

# Dataset names
datasetname_template = 'SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-{__MASS1__}_M-{__MASS2__}_13TeV_madgraph_pythia8'
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
            'Events' : 250000, # 10M events for each mass point
            'Filter efficiency' : 1.0, # random value for now, check later
            'Match efficiency' : 1.0, # random value for now, check later
            'proc_card_link' : proc_card_link,
            'fragment' : lhe_fragment.replace('__LINK__', proc_card_link).replace('__PYTHIA_FRAGMENT__', pythia_fragment).replace('__GRIDPACK__', gridpack_path),
            'generator' : 'Madgraph+Pythia8',
            'Dataset name' : dataset_name,
            'notes' : dataset_name.split('_')
        }

