## Fragments and girdpacks' collection for H->aa->4gamma samples
import os

pjoin = os.path.join

### General fragments 
pythia_fragment_run2_CUEP8M1 = """import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
             __CHANNEL_DECAY_FRAGMENT__
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
        )
                         )


ProductionFilterSequence = cms.Sequence(generator)"""

pythia_fragment_run2_CP5 = """import FWCore.ParameterSet.Config as cms
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
        processParameters = cms.vstring(
            __CHANNEL_DECAY_FRAGMENT__
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)
"""

def fragmentsDictCreator (decay_fr):
    dict = { '2016': pythia_fragment_run2_CUEP8M1.replace('__CHANNEL_DECAY_FRAGMENT__',decay_fr),
             '2017': pythia_fragment_run2_CP5.replace('__CHANNEL_DECAY_FRAGMENT__',decay_fr),
             '2018': pythia_fragment_run2_CP5.replace('__CHANNEL_DECAY_FRAGMENT__',decay_fr)
                    }
    return dict

lhe_fragment = """import FWCore.ParameterSet.Config as cms

# link to card:
# __LINK__


externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    nEvents = cms.untracked.uint32(5000),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring('__GRIDPACK__')
)

__PYTHIA_FRAGMENT__
"""

# Process parameters
h_aa = '''
'JetMatching:setMad = off',
'JetMatching:scheme = 1',
'JetMatching:merge = on',
'JetMatching:jetAlgorithm = 2',
'JetMatching:etaJetMax = 5.',
'JetMatching:coneRadius = 1.',
'JetMatching:slowJetPower = 1',
'JetMatching:qCut = 30.', 
'JetMatching:nQmatch = 4', 
'JetMatching:nJetMax = 1', 
'JetMatching:doShowerKt = off', 
'''

# Mass points in GeV
mass_points = ['0p1', '0p2', '0p4', '0p6', '0p8', '1', '1p2', '1p6', '2', '2p4', '3', 
               '5', '10', '15', '20', '25', '30', '35', '40', '45', '50',
			   '55', '60']

# Paths to proc cards on Github
proc_card_path = 'https://github.com/mbandrews/genproductions/blob/13ccb9321b7320770f5b8e7c211c93a2ebbd3591/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/hToaaTo4gamma_ma_AMASS_GeV_MLM_4f_max1j/hToaaTo4gamma_ma_AMASS_GeV_MLM_4f_max1j_proc_card.dat'

# Add gridpack path once they are loaded on cvmfs

gridpack_dir = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/hToaaTo4gamma_MLM_4f/v1'
gridpack_file_template = 'hToaaTo4gamma_ma{}GeV_MLM_4f_max1j_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'

gridpack_path_template = pjoin(gridpack_dir, gridpack_file_template)

gp_haa_2016 = {} # gridpack path & proc_card_path for 2016
gp_haa_2017 = {} # gridpack path & proc_card_path for 2017
gp_haa_2018 = {} # gridpack path & proc_card_path for 2018

# Create dictionary mapping mass points to number of eventts
mass_points_nevents = {}

for mass_point in mass_points:
	mass_points_nevents[mass_point] = 500000
	path_tup = proc_card_path, gridpack_path_template.format(mass_point)
	gp_haa_2016[mass_point] = path_tup 
	gp_haa_2017[mass_point] = path_tup
	gp_haa_2018[mass_point] = path_tup

dataset_names = {'2016' : 'HAHMHToAA_AToGG_MA-{}GeV_TuneCUETP8M1_PSweights_13TeV-madgraph_pythia8',
                 '2017' : 'HAHMHToAA_AToGG_MA-{}GeV_TuneCP5_PSweights_13TeV-madgraph_pythia8',
                 '2018' : 'HAHMHToAA_AToGG_MA-{}GeV_TuneCP5_PSweights_13TeV-madgraph_pythia8'}


# Get the dictionary containing 2016, 2017 and 2018 fragments
pythia_fragment_dict = fragmentsDictCreator(h_aa)

gridpacks_dict = {'2016': gp_haa_2016, '2017': gp_haa_2017, '2018': gp_haa_2018}

