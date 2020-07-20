from request_creator import RequestCreator

# Templates for LHE and Pythia fragments
lhe_fragment_template = '''import FWCore.ParameterSet.Config as cms

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

pythia_fragment_template = '''from Configuration.Generator.Pythia8CommonSettings_cfi import *
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
            '25:m0 = {__MASS__}',
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

### Request creator for WminusH requests
mass_points = [110,150,200,300,400,500,600,800,1000]
dataset_name_template = 'WminusH_WToQQ_HToInvisible_M{__MASS__}_13TeV_powheg_pythia8'
num_events_list = [1000000, 1000000, 500000, 250000, 100000, 100000, 100000, 100000, 100000]
years = [2017, 2018]
proc_card_link = 'https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/2017/13TeV/Higgs/WminusHJ_HanythingJ_NNPDF31_13TeV/HWminusJ_HanythingJ_NNPDF31_13TeV_Vhadronic_template.input'
# Gridpack path templates for 2016 and 2017/2018
gridpack_path_templates = {
    '2017/2018' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/HWJ_slc7_amd64_gcc700_CMSSW_10_2_22_HWminusJ_M{__MASS__}/v1/HWJ_slc7_amd64_gcc700_CMSSW_10_2_22_HWminusJ_M{__MASS__}.tgz'
}

rc = RequestCreator(
    proc_tag='WminusH_HToInv', mass_points=mass_points, dataset_name_template=dataset_name_template,
    lhe_fragment_template=lhe_fragment_template, pythia_fragment_template=pythia_fragment_template,
    num_events_list=num_events_list, years=years, proc_card_link=proc_card_link, gridpack_path_templates=gridpack_path_templates
    ) 

# Get the request information and store them into CSV files for each year
rc.prepare_requests()
rc.write_to_csv()

### Request creator for WplusH requests
mass_points = [110,150,200,300,400,500,600,800,1000]
dataset_name_template = 'WplusH_WToQQ_HToInvisible_M{__MASS__}_13TeV_powheg_pythia8'
num_events_list = [1000000, 1000000, 500000, 250000, 100000, 100000, 100000, 100000, 100000]
years = [2017, 2018]
proc_card_link = 'https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/2017/13TeV/Higgs/WplusHJ_HanythingJ_NNPDF31_13TeV/HWplusJ_HanythingJ_NNPDF31_13TeV_Vhadronic_template.input'
gridpack_path_templates = {
    '2017/2018' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/HWJ_slc7_amd64_gcc700_CMSSW_10_2_22_HWplusJ_M{__MASS__}/v1/HWJ_slc7_amd64_gcc700_CMSSW_10_2_22_HWplusJ_M{__MASS__}.tgz'
}

rc = RequestCreator(
    proc_tag='WplusH_HToInv', mass_points=mass_points, dataset_name_template=dataset_name_template,
    lhe_fragment_template=lhe_fragment_template, pythia_fragment_template=pythia_fragment_template,
    num_events_list=num_events_list, years=years, proc_card_link=proc_card_link, gridpack_path_templates=gridpack_path_templates
    ) 

# Get the request information and store them into CSV files for each year
rc.prepare_requests()
rc.write_to_csv()

### Request creator for ZH requests
mass_points = [110,150,200,300,400,500,600,800,1000]
dataset_name_template = 'ZH_ZToQQ_HToInvisible_M{__MASS__}_13TeV_powheg_pythia8'
num_events_list = [1000000, 1000000, 500000, 250000, 100000, 100000, 100000, 100000, 100000]
years = [2017, 2018]
proc_card_link = 'https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/2017/13TeV/Higgs/HZJ_HanythingJ_NNPDF31_13TeV/HZJ_HanythingJ_NNPDF31_13TeV_M125_Vhadronic.input'
gridpack_path_templates = {
    '2017/2018' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/HZJ_slc7_amd64_gcc700_CMSSW_10_2_22_HZJ_M{__MASS__}/v1/HZJ_slc7_amd64_gcc700_CMSSW_10_2_22_HZJ_M{__MASS__}.tgz'
}

rc = RequestCreator(
    proc_tag='ZH_HToInv', mass_points=mass_points, dataset_name_template=dataset_name_template,
    lhe_fragment_template=lhe_fragment_template, pythia_fragment_template=pythia_fragment_template,
    num_events_list=num_events_list, years=years, proc_card_link=proc_card_link, gridpack_path_templates=gridpack_path_templates
    ) 

# Get the request information and store them into CSV files for each year
rc.prepare_requests()
rc.write_to_csv()

### ggZH requests: Pythia fragment
pythia_fragment_template_ggZH = '''from Configuration.Generator.Pythia8CommonSettings_cfi import *
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
            '25:m0 = {__MASS__}',
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
### Request creator for ggZH requests
mass_points = [110,150,200,300,400,500,600,800,1000]
dataset_name_template = 'ggZH_ZToQQ_HToInvisible_M{__MASS__}_13TeV_powheg_pythia8'
num_events_list = [1000000, 1000000, 500000, 250000, 100000, 100000, 100000, 100000, 100000]
years = [2016, 2017, 2018]
proc_card_link = 'https://github.com/cms-sw/genproductions/tree/master/bin/Powheg/production/2017/13TeV/Higgs/ggHZ_HanythingJ_NNPDF31_13TeV'
gridpack_path_templates = {
    '2016'      : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/Powheg/V2/ggHZ_slc7_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}/v1/ggHZ_slc7_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}.tgz',
    '2017/2018' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/ggHZ_slc7_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}/v1/ggHZ_slc7_amd64_gcc700_CMSSW_10_2_22_ggHZ_M{__MASS__}.tgz'
}

rc = RequestCreator(
    proc_tag='ggZH_HToInv', mass_points=mass_points, dataset_name_template=dataset_name_template,
    lhe_fragment_template=lhe_fragment_template, pythia_fragment_template=pythia_fragment_template,
    num_events_list=num_events_list, years=years, proc_card_link=proc_card_link, gridpack_path_templates=gridpack_path_templates
    ) 

# Get the request information and store them into CSV files for each year
rc.prepare_requests()
rc.write_to_csv()
