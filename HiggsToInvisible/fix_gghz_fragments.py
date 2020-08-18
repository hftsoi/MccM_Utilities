import csv
import os

pjoin = os.path.join

csv_dir = './csv/ggZH_HToInv/fragment_fix'

if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

# Templates for LHE and Pythia fragments
lhe_fragment_template = '''
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

pythia_fragment_template_2017 = '''
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'POWHEG:nFinal = 2',   ## Number of final state particles
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
                                    'processParameters'
                                    )
        )
                         )
'''

pythia_fragment_template_2018 = '''
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
            'POWHEG:nFinal = 2',   ## Number of final state particles
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
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
        )
                         )
'''
# 2018 fragment has the PS weights added in
pythia_fragment_templates = {
    2016 : pythia_fragment_template_2017,
    2017 : pythia_fragment_template_2017,
    2018 : pythia_fragment_template_2018
}

# Production sequence
sequence = 'ProductionFilterSequence = cms.Sequence(generator)'

# Complete fragment
complete_fragment_template = '''
{__LHE_FRAGMENT__}

{__PYTHIA_FRAGMENT__}

{__SEQUENCE__}
'''

# List of prepIDs for each year
prep_ids = {
    2016: [
        'HIG-RunIISummer15wmLHEGS-04550',
        'HIG-RunIISummer15wmLHEGS-04551',
        'HIG-RunIISummer15wmLHEGS-04552',
        'HIG-RunIISummer15wmLHEGS-04553',
        'HIG-RunIISummer15wmLHEGS-04554',
        'HIG-RunIISummer15wmLHEGS-04555',
        'HIG-RunIISummer15wmLHEGS-04556',
        'HIG-RunIISummer15wmLHEGS-04557',
        'HIG-RunIISummer15wmLHEGS-04558'
    ],
    2017: [
        'HIG-RunIIFall17wmLHEGS-05405',
        'HIG-RunIIFall17wmLHEGS-05406',
        'HIG-RunIIFall17wmLHEGS-05407',
        'HIG-RunIIFall17wmLHEGS-05408',
        'HIG-RunIIFall17wmLHEGS-05409',
        'HIG-RunIIFall17wmLHEGS-05410',
        'HIG-RunIIFall17wmLHEGS-05411',
        'HIG-RunIIFall17wmLHEGS-05412',
        'HIG-RunIIFall17wmLHEGS-05413'
    ],
    2018: [
        'HIG-RunIIFall18wmLHEGS-04483',
        'HIG-RunIIFall18wmLHEGS-04484',
        'HIG-RunIIFall18wmLHEGS-04485',
        'HIG-RunIIFall18wmLHEGS-04486',
        'HIG-RunIIFall18wmLHEGS-04487',
        'HIG-RunIIFall18wmLHEGS-04488',
        'HIG-RunIIFall18wmLHEGS-04489',
        'HIG-RUNIIFALL18WMLHEGS-04490',
        'HIG-RunIIFall18wmLHEGS-04491'
    ]
}

mass_points = [110,150,200,300,400,500,600,800,1000]
dataset_name_templates = {
    2016 : 'ggZH_ZToQQ_HToInvisible_M{__MASS__}_TuneCP5_13TeV_powheg_pythia8',
    2017 : 'ggZH_ZToQQ_HToInvisible_M{__MASS__}_TuneCP5_13TeV_powheg_pythia8',
    2018 : 'ggZH_ZToQQ_HToInvisible_M{__MASS__}_TuneCP5_PSweights_13TeV_powheg_pythia8'
}

proc_card_link = 'https://github.com/cms-sw/genproductions/tree/master/bin/Powheg/production/2017/13TeV/Higgs/ggHZ_HanythingJ_NNPDF31_13TeV'
gridpack_path_templates = {
    2016      : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/Powheg/V2/ggHZ_slc6_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}/v1/ggHZ_slc6_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}.tgz',
    2017      : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/ggHZ_slc6_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}/v1/ggHZ_slc6_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}.tgz',

    2018      : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/ggHZ_slc6_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}/v1/ggHZ_slc6_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}.tgz'
}

years = [2016, 2017, 2018]

# Write updated fragments to CSV file
for year in years:
    csv_file = pjoin(csv_dir, 'gghz_fragments_{}.csv'.format(year))
    with open(csv_file, 'w+') as f: 
        writer = csv.writer(f)
        writer.writerow(['PrepID', 'Fragment'])
        dataset_name_template = dataset_name_templates[year]
        gridpack_path_template = gridpack_path_templates[year]
        pythia_fragment_template = pythia_fragment_templates[year]

        prep_id_list = prep_ids[year]

        for idx, mass_point in enumerate(mass_points):
            dataset_name = dataset_name_template.format(__MASS__ = mass_point)
            gridpack_path = gridpack_path_template.format(__MASS__ = mass_point)                

            lhe_fragment = lhe_fragment_template.format(__GRIDPACK__ = gridpack_path, __LINK__ = proc_card_link)
            pythia_fragment = pythia_fragment_template.format(__MASS__ = mass_point)
        
            fragment = complete_fragment_template.format(__LHE_FRAGMENT__ = lhe_fragment, __PYTHIA_FRAGMENT__ = pythia_fragment, __SEQUENCE__ = sequence)    
        
            prepid = prep_id_list[idx]

            writer.writerow([prepid, fragment])



