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
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         HepMCFilter = cms.PSet(
                             filterName = cms.string('EmbeddingHepMCFilter'),
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
        pythia8CUEP8M1SettingsBlock,
        pythia8PSweightsSettingsBlock, 
        processParameters = cms.vstring(
            '25:onMode = off',
            '25:onIfMatch = 15 -15',
            '35:onMode = off',
            '35:onIfMatch = 5 -5',
            'SLHA:minMassSM = 10.',
            'ResonanceDecayFilter:filter = on',
            'ResonanceDecayFilter:exclusive = on', #off: require at least the specified number of daughters, on: require exactly the specified number of daughters
            'ResonanceDecayFilter:eMuAsEquivalent    = off', #on: treat electrons and muons as equivalent
            'ResonanceDecayFilter:eMuTauAsEquivalent = off',  #on: treat electrons, muons , and taus as equivalent
            'ResonanceDecayFilter:allNuAsEquivalent  = on',  #on: treat all three neutrino flavours as equivalent
            'ResonanceDecayFilter:udscAsEquivalent   = off', #on: treat u,d,s,c quarks as equivalent
            'ResonanceDecayFilter:udscbAsEquivalent  = off', #on: treat u,d,s,c,b quarks as equivalent
            #'ResonanceDecayFilter:mothers =', #list of mothers not specified -> count all particles in hard process+resonance decays (better to avoid specifying mothers when including leptons from the lhe in counting, since intermediate resonances are not gauranteed to appear in general
            #'ResonanceDecayFilter:daughters = 5,5,15,15'
            #'ResonanceDecayFilter:mothers = 25,35',
            #'ResonanceDecayFilter:daughters = 15,15,5,5'
            'ResonanceDecayFilter:mothers = 25',
            'ResonanceDecayFilter:daughters = 15,15'
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)

