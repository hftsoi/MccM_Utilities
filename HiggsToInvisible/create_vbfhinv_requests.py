# Script to create VBF H(inv) requests, write items to CSV file

import csv
import os
from pprint import pprint

pjoin = os.path.join

pythia_fragment_temp_CP5 = '''from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,
        processParameters = cms.vstring(
            'POWHEG:nFinal = 3',   ## Number of final state particles
                                   ## (BEFORE THE DECAYS) in the LHE
                                   ## other than emitted extra parton
            '25:m0 = {__MASS__}.0',
            '25:onMode = off',
            '25:onIfMatch = 23 23', ## H -> ZZ
            '23:onMode = off',      # turn OFF all Z decays
            '23:onIfAny = 12 14 16',# turn ON Z->vv
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'processParameters'
                                    )
        )
                         )
'''

lhe_fragment_temp = '''import FWCore.ParameterSet.Config as cms

# link to card:
# {__LINK__}

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('{__GRIDPACK__}'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
    )
'''

# Production sequence
sequence = 'ProductionFilterSequence = cms.Sequence(generator)'

# Complete fragment, LHE and GEN pt filters are used for ggH requests
complete_fragment_template = '''
{__LHE_FRAGMENT__}

{__PYTHIA_FRAGMENT__}

{__SEQUENCE__}
'''

# Link to proc card for this request (DOUBLE CHECK!)
proc_card_link = 'https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/2017/13TeV/Higgs/gg_H_quark-mass-effects_NNPDF31_13TeV/gg_H_quark-mass-effects_NNPDF31_13TeV_template.input'

# Mass points
mass_points = [110,150,200,300,400,500,600,800,1000]

# Dataset names and gridpacks for each mass point
dataset_name_template = 'VBF_HToInvisible_M{__MASS__}_TuneCP5_13TeV_powheg_pythia8'
gridpack_path_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/VBF_H_NNPDF31_13TeV_M{__MASS__}/v1/VBF_H_NNPDF31_13TeV_M{__MASS__}_slc6_amd64_gcc630_CMSSW_9_3_0.tgz'

# Number of events for each mass point
numevents = [1000000, 1000000, 500000, 250000, 100000, 100000, 100000, 100000, 100000]

# Years
years = [2016, 2017, 2018]

# Fill in all the information about all ggH requests
request_info = {}
for year in years:
    pythia_fragment_temp = pythia_fragment_temp_CP5
    request_info[year] = {}
    for idx, mass_point in enumerate(mass_points):
        dataset_name = dataset_name_template.format(__MASS__ = mass_point)
        gridpack_path = gridpack_path_template.format(__MASS__ = mass_point)
        lhe_fragment = lhe_fragment_temp.format(
            __LINK__ = proc_card_link,
            __GRIDPACK__ = gridpack_path
        )
        pythia_fragment = pythia_fragment_temp.format(
            __MASS__ = mass_point
        )
    
        complete_fragment = complete_fragment_template.format(
            __LHE_FRAGMENT__    = lhe_fragment,
            __PYTHIA_FRAGMENT__ = pythia_fragment, 
            __SEQUENCE__        = sequence
        )
    
        request_info[year][mass_point] = {
            'Dataset name'      : dataset_name,
            'gridpack'          : gridpack_path,
            'proc_card_link'    : proc_card_link,
            'fragment'          : complete_fragment,
            'Events'            : numevents[idx],
            'generator'         : 'Powheg+Pythia8',
            'Filter efficiency' : 1.0, 
            'Match efficiency'  : 1.0, 
            'notes'             : dataset_name.split('_')
        }

# Write into CSV file
outdir = './csv/VBF_Hinv'
if not os.path.exists(outdir):
    os.makedirs(outdir)

out_csv_file_temp = pjoin(outdir, 'VBF_Hinv_{__YEAR__}_requests.csv')
fieldnames = ['Dataset name', 'Events', 'Filter efficiency', 'Match efficiency','fragment', 'notes', 'generator']  

for year in years:
    filename = out_csv_file_temp.format(__YEAR__ = year)
    with open(filename, 'w+') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,extrasaction='ignore')
        writer.writeheader()
        for mass_point in mass_points:
            data = request_info[year][mass_point]
            writer.writerow(data)
