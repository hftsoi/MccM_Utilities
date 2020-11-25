import os
import csv

pjoin = os.path.join

# TODO: Adjust width for Higgs depending on mass!
fragment_template = '''
import FWCore.ParameterSet.Config as cms

# link to card:
# {__PROC_CARD__}

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
                                     args = cms.vstring('{__GRIDPACK__}'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

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
                                                                         'TauDecays:mode = 2', 
                                                                         'TauDecays:tauPolarization = 0', 
                                                                         'TauDecays:tauMother = 25', 
                                                                         '25:m0 = {__MASS__}.0', 
                                                                         '25:addChannel 1 0.001 100 13 -15', 
                                                                         '25:addChannel 1 0.001 100 15 -13', 
                                                                         '25:onMode = off', 
                                                                         '25:onIfMatch 13 15'),
                                         
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

proc_card_links = {
    'ggH' : 'https://github.com/cms-sw/genproductions/tree/22cdc0aba20c34087929cef168da715dad25581a/bin/Powheg/production/2017/13TeV/gg_H_ZZ_quark-mass-effects_NNPDF31_13TeV',
    'VBF' : 'https://github.com/cms-sw/genproductions/tree/22cdc0aba20c34087929cef168da715dad25581a/bin/Powheg/production/2017/13TeV/VBF_H_NNPDF31_13TeV',
}

dataset_name_templates = {
    'ggH' : 'GluGlu_LFV_HToMuTau_M{__MASS__}_13TeV_PSweights_powheg_pythia8',
    'VBF' : 'VBF_LFV_HToMuTau_M{__MASS__}_13TeV_PSweights_powheg_pythia8',
}

gridpack_path_templates = {
    'ggH' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_NNPDF31_13TeV_M{__MASS__}/v1/gg_H_quark-mass-effects_NNPDF31_13TeV_M{__MASS__}_slc6_amd64_gcc630_CMSSW_9_3_0.tgz',
    'VBF' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/VBF_H_NNPDF31_13TeV_M{__MASS__}/v1/VBF_H_NNPDF31_13TeV_M{__MASS__}_slc6_amd64_gcc630_CMSSW_9_3_0.tgz',
}

numevents = 100000
mass_points = [120,130,150,200]

processes = ['ggH', 'VBF']

num_final_particles = {
    'ggH' : 1,
    'VBF' : 3,
}

request_info = {}
for proc in processes:
    num_fp = num_final_particles[proc]
    proc_card_link = proc_card_links[proc]
    request_info[proc] = {}
    for mass in mass_points:
        dataset_name = dataset_name_templates[proc].format(__MASS__=mass)
        gridpack_path = gridpack_path_templates[proc].format(__MASS__=mass)
        fragment = fragment_template.format(
            __MASS__ = mass,
            __GRIDPACK__ = gridpack_path,
            __PROC_CARD__ = proc_card_link
        )

        request_info[proc][mass] = {
            'Dataset name'        : dataset_name,
            'gridpack'            : gridpack_path,
            'fragment'            : fragment,
            'Events'              : numevents,
            'generator'           : 'Powheg+Pythia8',
            'Filter efficiency'   : 1.0,
            'Match efficiency'    : 1.0,
            'notes'               : dataset_name.split('_')
        }

# Write into CSV file
outdir = './csv'
if not os.path.exists(outdir):
    os.makedirs(outdir)

fieldnames = ['Dataset name', 'Events', 'Filter efficiency', 'Match efficiency','fragment', 'notes', 'generator']  

for prod_mode in prod_modes:
    out_csv_file_temp = pjoin(outdir, '{__PROD_MODE__}_HToMuTau_requests.csv')

    filename = out_csv_file_temp.format(__PROD_MODE__ = prod_mode)
    with open(filename, 'w+') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,extrasaction='ignore')
        writer.writeheader()
        data = request_info[prod_mode]
        writer.writerow(data)

