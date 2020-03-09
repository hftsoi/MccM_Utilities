import os
from pprint import pprint

pjoin = os.path.join

## Fragment
fragment = '''import FWCore.ParameterSet.Config as cms
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

cctauFilter = cms.EDFilter("PythiaDauVFilter",
    ChargeConjugation = cms.untracked.bool(True),
    DaughterIDs = cms.untracked.vint32(11, 13),
    MaxEta = cms.untracked.vdouble(999.0, 999.0),
    MinEta = cms.untracked.vdouble(-999.0, -999.0),
    MinPt = cms.untracked.vdouble(0.0, 0.0),
    MotherID = cms.untracked.int32(24),
    NumberDaughters = cms.untracked.int32(0),
    ParticleID = cms.untracked.int32(15),
    verbose = cms.untracked.int32(0)
)



ProductionFilterSequence = cms.Sequence(generator+~cctauFilter)
'''

lhe_fragment = '''import FWCore.ParameterSet.Config as cms

# link to card:
# __LINK__

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('__GRIDPACK__'),
    nEvents = cms.untracked.uint32(10000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

__PYTHIA_FRAGMENT__
'''

# Links to proc cards on GitHub
proc_card_links = {
	'scalar' : {
		'INT' : 'https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/Htottbar_dilepton/heavyhiggs_13TeV_m400_INT_SCALAR_wnat/heavyhiggs_13TeV_m400_INT_SCALAR_wnat_proc_card.dat',
		'RES' : 'https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/Htottbar_dilepton/heavyhiggs_13TeV_m400_RES_SCALAR_wnat/heavyhiggs_13TeV_m400_RES_SCALAR_wnat_proc_card.dat'
	},
	
	'psuedo' : {
		'INT' : 'https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/Htottbar_dilepton/heavyhiggs_13TeV_m400_INT_PSEUDO_wnat/heavyhiggs_13TeV_m400_INT_PSEUDO_wnat_proc_card.dat',
		'RES' : 'https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/Htottbar_dilepton/heavyhiggs_13TeV_m400_RES_PSEUDO_wnat/heavyhiggs_13TeV_m400_RES_PSEUDO_wnat_proc_card.dat'
	}
}

# Gridpack locations in cvmfs
gridpack_dirs = {
	'scalar' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.0/heavyhiggs_13TeV_mX_INT_SCALAR_wnat/v1/',
	'psuedo' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.0/heavyhiggs_13TeV_mX_INT_PSEUDO_wnat/v1/'
}

gridpack_templates = {
	'scalar' : pjoin(gridpack_dirs['scalar'], 'heavyhiggs_13TeV_m{__MASS__}_{__TYPE__}_SCALAR_wnat_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz'),
	'psuedo' : pjoin(gridpack_dirs['psuedo'], 'heavyhiggs_13TeV_m{__MASS__}_{__TYPE__}_PSEUDO_wnat_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz')
}

mass_points = [365, 400, 600, 800, 1000]
types = ['INT', 'RES']

sample_type = {
	'INT' : 'interference',
	'RES' : 'resonance'
}

gridpack_dict = {}

for type_ in types:
	gridpack_dict[type_] = {}
	for mass_point in mass_points:
		gridpack_dict[type_][mass_point] = {
			'scalar' : gridpack_templates['scalar'].format(__MASS__=mass_point, __TYPE__=type_),
			'psuedo' : gridpack_templates['psuedo'].format(__MASS__=mass_point, __TYPE__=type_),
		} 

#pprint(gridpack_dict)	

dataset_name_template = 'H{__HIGGS_TYPE__}ToTTbar_M-{__MASS__}_TuneCP5_PSweights_{__SAMPLE_TYPE__}_13TeV-madgraph_pythia8'

# Main containers
def get_containers():
	container_17 = {'scalar' : {}, 'psuedo' : {}}
	for key in container_17.keys():
		for type_ in types:
			container_17[key][type_] = {}
			for mass_point in mass_points:
				gridpack_path = gridpack_templates[key].format(__MASS__=mass_point, __TYPE__=type_)
				proc_card_link = proc_card_links[key][type_]
				dataset_name = dataset_name_template.format(__MASS__=mass_point, __HIGGS_TYPE__=key, __SAMPLE_TYPE__=sample_type[type_])
				container_17[key][type_][mass_point] = {
					'gridpack' : gridpack_path, 
					'Events' : 500000,	
					'Filter efficiency' : 0.551, # Constant filter eff for each request
					'proc_card_link' : proc_card_link,
					'fragment' : lhe_fragment.replace('__LINK__', proc_card_link).replace('__GRIDPACK__',gridpack_path).replace('__PYTHIA_FRAGMENT__',fragment),
					'generator' : 'Madgraph+Pythia',
					'Dataset name' : dataset_name,
					'notes': dataset_name.split('_')
				}

	container_18 = {'scalar' : {}, 'psuedo' : {}}
	for key in container_18.keys():
		for type_ in types:
			container_18[key][type_] = {}
			for mass_point in mass_points:
				gridpack_path = gridpack_templates[key].format(__MASS__=mass_point, __TYPE__=type_)
				proc_card_link = proc_card_links[key][type_]
				dataset_name = dataset_name_template.format(__MASS__=mass_point, __HIGGS_TYPE__=key, __SAMPLE_TYPE__=sample_type[type_])
				container_18[key][type_][mass_point] = {
					'gridpack' : gridpack_path, 
					'Events' : 2000000,
					'Filter efficiency' : 0.551, # Constant filter eff for each request
					'proc_card_link' : proc_card_link,
					'fragment' : lhe_fragment.replace('__LINK__', proc_card_link).replace('__GRIDPACK__',gridpack_path).replace('__PYTHIA_FRAGMENT__',fragment),
					'generator' : 'Madgraph+Pythia',
					'Dataset name' : dataset_name,
					'notes': dataset_name.split('_')
				}

	container_dict = {'2017' : container_17, '2018' : container_18}

	return container_dict
	


