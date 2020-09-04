import os
from lib.request_creator import RequestCreator

pjoin = os.path.join

# =======================================================================
# Dump the VBF and ggH requests configuration into csv files for all three years. 
# =======================================================================

# Fragment template (both for VBF and ggH)
fragment_temp = '''import FWCore.ParameterSet.Config as cms

# link to cards:
# https://github.com/cms-sw/genproductions/pull/2670, https://github.com/cms-sw/genproductions/pull/2705
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

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         HepMCFilter = cms.PSet(
                             filterName = cms.string('EmbeddingHepMCFilter'),
                             filterParameters = cms.PSet(
                                 ElElCut = cms.string('El1.Pt > 22 && El2.Pt > 10 && El1.Eta < 2.6 && El2.Eta < 2.6'),
                                 ElHadCut = cms.string('El.Pt > 22 && Had.Pt > 16 && El.Eta < 2.6 && Had.Eta < 2.7'),
                                 ElMuCut = cms.string('Mu.Pt > 7 && El.Pt > 11 && El.Eta < 2.6 && Mu.Eta < 2.5'),
                                 HadHadCut = cms.string('Had1.Pt > 28 && Had2.Pt > 28 && Had1.Eta < 2.5 && Had2.Eta < 2.5'),
                                 MuHadCut = cms.string('Mu.Pt > 19 && Had.Pt > 16 && Mu.Eta < 2.5 && Had.Eta < 2.7'),
                                 MuMuCut = cms.string('Mu1.Pt > 17 && Mu2.Pt > 8 && Mu1.Eta < 2.5 && Mu2.Eta < 2.5'),
                                 Final_States = cms.vstring(
                                     'ElHad',
                                     'ElMu',
                                     'HadHad',
                                     'MuHad'
                                 ),
                                 BosonPDGID = cms.int32(36)
                             )
                         ),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock, 
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)
'''

def create_ggh_requests():
    '''Create CSV files containing configuration of the ggH requests'''
    # Gridpack locations 
    # TODO: Put gridpack location here once they are on CVMFS
    gridpack_location_temp = ''
    
    dataset_name_temp = 'SUSYGluGluToHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8'
    
    # List of several quantities
    mass_points = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    years = [2016, 2017, 2018]
    filter_effs = [0.03]*2 + [0.04]*9
    # Number of events before filter for each mass point
    num_events = [200000, 200000, 1000000, 200000, 200000, 200000, 1000000, 200000, 200000, 200000, 1000000]
    
    template_dict = {
        'Dataset name': dataset_name_temp, 
        'Gridpack path': gridpack_location_temp, 
        'Fragment': fragment_temp 
    }
    
    # Dump the request to csv files
    r = RequestCreator(
        template_dict=template_dict, 
        mass_points=mass_points,
        filter_effs=filter_effs,
        num_events=num_events,
        years=years, tag='ggh'
    )
    
    r.dump_to_csv()

def create_vbf_requests():
    '''Create CSV files containing configuration of the VBF requests'''
    # Gridpack locations 
    # TODO: Put gridpack location here once they are on CVMFS
    gridpack_location_temp = ''
    
    dataset_name_temp = 'SUSYVBFHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8'
    
    # List of several quantities
    mass_points = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    years = [2016, 2017, 2018]
    filter_effs = [0.05]*11 
    # Number of events before filter for each mass point
    num_events = [200000]*11
    
    template_dict = {
        'Dataset name': dataset_name_temp, 
        'Gridpack path': gridpack_location_temp, 
        'Fragment': fragment_temp 
    }
    
    # Dump the request to csv files
    r = RequestCreator(
        template_dict=template_dict, 
        mass_points=mass_points,
        filter_effs=filter_effs,
        num_events=num_events,
        years=years, tag='vbf'
    )
    
    r.dump_to_csv()

def main():
    create_ggh_requests()
    create_vbf_requests()

if __name__ == '__main__':
    main()