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
                            processParameters = cms.vstring(
                                    '15:onMode = on', #Turn on all decays of Tau
                                    ),
                            parameterSets = cms.vstring(
                                    'processParameters',
                                    'pythia8CommonSettings',
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
    generateConcurrently = cms.untracked.bool(False),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

__PYTHIA_FRAGMENT__
'''

# Link to proc card on GitHub
proc_card_link = 'genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/13TeV/VLferm_EWcouplings_4321'


# Gridpack locations at cvmfs
gridpacks = [
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m500GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m550GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m600GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m650GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m700GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m750GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m800GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m850GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m900GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m950GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m1000GeV_EE_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m500GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m550GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m600GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m650GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m700GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m750GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m800GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m850GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m900GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m950GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m1000GeV_EN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m500GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m550GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m600GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m650GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m700GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m750GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m800GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m850GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m900GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m950GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
    '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/slc7_amd64_gcc10/MadGraph5_aMCatNLO/SUS_VLferm/VLferm_EWcouplings_4321_m1000GeV_NN_to_4b_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz',
]

nEvents = [
    120000
]

# Dataset names
datasetnames = [
    'VLferm_m500GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m550GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m600GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m650GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m700GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m750GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m800GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m850GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m900GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m950GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m1000GeV_EE_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m500GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m550GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m600GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m650GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m700GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m750GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m800GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m850GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m900GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m950GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m1000GeV_EN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m500GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m550GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m600GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m650GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m700GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m750GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m800GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m850GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m900GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m950GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
    'VLferm_m1000GeV_NN_to_4b_TuneCP5_13TeV-madgraph-pythia8',
]

# Fill request information for 2017 and 2018
request_information = {}
for year in ['2016','2016apv','2017','2018']:
    request_information[year] = {}
    for i in range(len(datasetnames)):
        gridpack_path = gridpacks[i]
        dataset_name = datasetnames[i]
        
        if year == '2016':
            nevts = int(nEvents[0]*0.46)
        elif year == '2016apv':
            nevts = int(nEvents[0]*0.54)
        elif year == '2017' or year == '2018':
            nevts = nEvents[0]
            
        request_information[year][i] = {
            'gridpack' : gridpack_path,
            'Events' : nevts,
            'Filter efficiency' : 1.0,
            'Match efficiency' : 1.0,
            'proc_card_link' : proc_card_link,
            'fragment' : lhe_fragment.replace('__LINK__', proc_card_link).replace('__PYTHIA_FRAGMENT__', pythia_fragment).replace('__GRIDPACK__', gridpack_path),
            'generator' : 'Madgraph+Pythia8',
            'Dataset name' : dataset_name,
            'notes' : dataset_name.split('_')
        }
