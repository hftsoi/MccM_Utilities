import FWCore.ParameterSet.Config as cms

# link to cards:
# https://github.com/cms-sw/genproductions/pull/2670, https://github.com/cms-sw/genproductions/pull/2705
externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('mygridpack.tgz'),
	nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

import FWCore.ParameterSet.Config as cms
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
                                 ElHadCut = cms.string('El.Pt > 6 && Had.Pt > 16 && El.Eta < 2.6 && Had.Eta < 2.7'),
                                 ElMuCut = cms.string('Mu.Pt > 4 && El.Pt > 6 && El.Eta < 2.6 && Mu.Eta < 2.5'),
                                 HadHadCut = cms.string('Had1.Pt > 16 && Had2.Pt > 16 && Had1.Eta < 2.5 && Had2.Eta < 2.5'),
                                 MuHadCut = cms.string('Mu.Pt > 4 && Had.Pt > 16 && Mu.Eta < 2.5 && Had.Eta < 2.7'),
                                 MuMuCut = cms.string('Mu1.Pt > 17 && Mu2.Pt > 8 && Mu1.Eta < 2.5 && Mu2.Eta < 2.5'),
                                 Final_States = cms.vstring(
                                     'ElHad',
                                     'ElMu',
                                     'HadHad',
                                     'MuHad'
                                 ),
                                 BosonPDGID = cms.int32(25)
                             )
                         ),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock, 
        processParameters = cms.vstring(
         '25:onMode = off',
         '25:onIfMatch = 5 -5',
         '25:onIfMatch = 15 -15',
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)

