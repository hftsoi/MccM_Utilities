# Script to create 2018 HToEMu requests, write items to CSV file

import csv
import os
from pprint import pprint

pjoin = os.path.join

pythia_fragment_temp = '''
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                                    comEnergy = cms.double(13000.0),
                                    filterEfficiency = cms.untracked.double(1),
                                    maxEventsToPrint = cms.untracked.int32(1),
                                    pythiaHepMCVerbosity = cms.untracked.bool(False),
                                    pythiaPylistVerbosity = cms.untracked.int32(1),
                                    PythiaParameters = cms.PSet(
                           pythia8CommonSettingsBlock,
                           pythia8CP5SettingsBlock,
                           pythia8PSweightsSettingsBlock,
                           pythia8PowhegEmissionVetoSettingsBlock,
                                         processParameters = cms.vstring('POWHEG:nFinal = {__NFINAL__}', 
                                                                         '25:m0 = {__MASS__}.0', 
                                                                         '25:addChannel 1 0.001 100 11 -13', 
                                                                         '25:addChannel 1 0.001 100 13 -11', 
                                                                         '25:onMode = off', 
                                                                         '25:onIfMatch 11 13'),
                                         
                          parameterSets = cms.vstring(
                                        'pythia8PowhegEmissionVetoSettings',
                                        'pythia8CommonSettings',
                                        'pythia8CP5Settings',
                                        'pythia8PSweightsSettings',
                                        'processParameters',
                                        )
                          )
            )

ProductionFilterSequence = cms.Sequence(generator)
'''

lhe_fragment_temp = '''
import FWCore.ParameterSet.Config as cms

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

# Complete fragment, LHE and GEN pt filters are used for ggH requests
complete_fragment_template = '''
{__LHE_FRAGMENT__}

{__PYTHIA_FRAGMENT__}
'''

# Links to proc cards for different production modes
proc_card_links = {
    'VBF' : 'https://github.com/cms-sw/genproductions/tree/22cdc0aba20c34087929cef168da715dad25581a/bin/Powheg/production/2017/13TeV/VBF_H_NNPDF31_13TeV',
    'ggH' : 'https://github.com/cms-sw/genproductions/tree/22cdc0aba20c34087929cef168da715dad25581a/bin/Powheg/production/2017/13TeV/gg_H_ZZ_quark-mass-effects_NNPDF31_13TeV'
}


# Dataset names for each production mode
dataset_name_templates = {
    'VBF' : 'VBF_LFV_HToEMu_M{__MASS__}_TuneCP5_PSweights_13TeV_powheg_pythia8',
    'ggH' : 'GluGlu_LFV_HToEMu_M{__MASS__}_TuneCP5_PSweights_13TeV_powheg_pythia8'
}

# Gridpacks for different production modes
gridpack_path_templates = {
    'ggH' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_NNPDF31_13TeV_M{__MASS__}/v1/gg_H_quark-mass-effects_NNPDF31_13TeV_M{__MASS__}_slc6_amd64_gcc630_CMSSW_9_3_0.tgz',
    'VBF' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/VBF_H_NNPDF31_13TeV_M{__MASS__}/v1/VBF_H_NNPDF31_13TeV_M{__MASS__}_slc6_amd64_gcc630_CMSSW_9_3_0.tgz'
}

num_final_particles = {'VBF' : 3, 'ggH' : 1}

# TODO: Double check the number of events 
numevents = 1000000 

# Fill in all the information about all production modes 
request_info = {}
prod_modes = ['ggH', 'VBF']

# Mass points for each production mode
mass_points = {
    'VBF' : [120],
    'ggH' : [120,130]
}


for prod_mode in prod_modes:
    for mass in mass_points[prod_mode]:
        proc_card_link = proc_card_links[prod_mode]
        gridpack_path = gridpack_path_templates[prod_mode].format(__MASS__ = mass)
        dataset_name = dataset_name_templates[prod_mode].format(__MASS__ = mass)
    
        lhe_fragment = lhe_fragment_temp.format(
            __LINK__ = proc_card_link,
            __GRIDPACK__ = gridpack_path
        )
        pythia_fragment = pythia_fragment_temp.format(
            __NFINAL__ = num_final_particles[prod_mode],
            __MASS__ = mass,
        )
    
        complete_fragment = complete_fragment_template.format(
            __LHE_FRAGMENT__    = lhe_fragment,
            __PYTHIA_FRAGMENT__ = pythia_fragment
        )
    
        request_info[prod_mode] = {
            'Dataset name'      : dataset_name,
            'gridpack'          : gridpack_path,
            'proc_card_link'    : proc_card_link,
            'fragment'          : complete_fragment,
            'Events'            : numevents,
            'generator'         : 'Powheg+Pythia8',
            'Filter efficiency' : 1.0, 
            'Match efficiency'  : 1.0, 
            'notes'             : dataset_name.split('_')
        }

# Write into CSV file
outdir = './csv'
if not os.path.exists(outdir):
    os.makedirs(outdir)

fieldnames = ['Dataset name', 'Events', 'Filter efficiency', 'Match efficiency','fragment', 'notes', 'generator']  

for prod_mode in prod_modes:
    out_csv_file_temp = pjoin(outdir, '{__PROD_MODE__}_HToEMu_requests.csv')

    filename = out_csv_file_temp.format(__PROD_MODE__ = prod_mode)
    with open(filename, 'w+') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,extrasaction='ignore')
        writer.writeheader()
        data = request_info[prod_mode]
        writer.writerow(data)

