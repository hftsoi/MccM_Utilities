# Link to cards:
# {__LINK__}

import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('{__GRIDPACK__}'),
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
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
                                    '24:onMode = off', 
                                    '24:onIfAny = 1 2 3 4 5 11 13 15',
                                    'ResonanceDecayFilter:filter = on',
                                    'ResonanceDecayFilter:exclusive = off', #off: require at least the specified number of daughters, on: require exactly the specified number of daughters
                                    'ResonanceDecayFilter:eMuTauAsEquivalent = on',  #on: treat electrons, muons , and taus as equivalent
                                    'ResonanceDecayFilter:allNuAsEquivalent  = on',  #on: treat all three neutrino flavours as equivalent
                                    'ResonanceDecayFilter:udscbAsEquivalent  = on', #on: treat u,d,s,c,b quarks as equivalent
                                    'ResonanceDecayFilter:mothers = 24',
                                    'ResonanceDecayFilter:daughters = 11,1', #Require one quark decay and one leptonic decay
                                    ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters'
                                    )
    )
)