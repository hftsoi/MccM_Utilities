import csv
import os
from pprint import pprint

pjoin = os.path.join

fragment_temp = '''
import FWCore.ParameterSet.Config as cms

# link to card:
# https://github.com/cms-sw/genproductions/tree/705976d5de7ee8230d5a1a0b1d62890860b93103/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/ChargedHiggs_TB/ChargedHiggs_TB_NLO/ChargedHiggs_TB_NLO_proc_card.dat

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('{__GRIDPACK__}'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8PSweightsSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8aMCatNLOSettingsBlock,
        processParameters = cms.vstring(
            'TimeShower:nPartonsInBorn = 2', #number of coloured particles (before resonance decays) in born matrix element
            'Higgs:useBSM = on', ## enable handling of bsm particles
            'SLHA:keepSM = on', # read properties from lhe
            'SLHA:minMassSM = 100.', # as above
            '37:mayDecay = on', ## decay of the ch higgs
            '37:onMode = off',
            '37:onIfAny = 6',
            '37:doForceWidth = on' ## make it with a width
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8PSweightsSettings',
                                    'pythia8CP5Settings',
                                    'pythia8aMCatNLOSettings',
                                    'processParameters',
                                    )
    )
)

ProductionFilterSequence = cms.Sequence(generator)
'''

mass_points = [200,220,250,300,350,400,500,600,700,800,1000,1250,1500,1750,2000,2500,3000]

gridpack_path_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/ChargedHiggs_TB_NLO_M{__MASS__}/v1/ChargedHiggs_TB_NLO_M{__MASS__}_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
dataset_name_template = 'ChargedHiggs_HplusTB_HplusToTB_M-{__MASS__}_TuneCP5_13TeV_amcatnlo_pythia8'
# 10M events per mass point
num_events = 10000000

request_info = {}

for mass in mass_points:
    dataset_name = dataset_name_template.format(__MASS__ = mass)
    gridpack_path = gridpack_path_template.format(__MASS__ = mass)
    fragment = fragment_temp.format(__GRIDPACK__ = gridpack_path)

    request_info[mass] = {
        'Dataset name'       : dataset_name,
        'gridpack'           : gridpack_path,
        'fragment'           : fragment,
        'Events'             : num_events,
        'generator'          : 'Madgraph+Pythia8',
        'Filter efficiency'  : 1.0,
        'Match efficiency'   : 1.0,
        'notes'              : dataset_name.split('_')
    }

outdir = './csv'
if not os.path.exists(outdir):
    os.makedirs(outdir)

outpath = pjoin(outdir, 'charged_higgs_2016_requests.csv')

fieldnames = ['Dataset name', 'Events', 'Filter efficiency', 'Match efficiency','fragment', 'notes', 'generator']  

with open(outpath, 'w+') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames,extrasaction='ignore')
    writer.writeheader()
    for mass in mass_points: 
        data = request_info[mass]
        writer.writerow(data)
