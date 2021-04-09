import csv
import os

pjoin = os.path.join

# Script to add PS weights to 2018 VH requests

outdir = './csv/WplusH_HToInv/fix_2017'
if not os.path.exists(outdir):
    os.makedirs(outdir)

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

pythia_fragment_template = '''
from Configuration.Generator.Pythia8CommonSettings_cfi import *
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
            '25:m0 = {__MASS__}.0',
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

# Production sequence
sequence = 'ProductionFilterSequence = cms.Sequence(generator)'

# Complete fragment, LHE and GEN pt filters are used for ggH requests
complete_fragment_template = '''
{__LHE_FRAGMENT__}

{__PYTHIA_FRAGMENT__}

{__SEQUENCE__}
'''

proc_card_link = 'https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/2017/13TeV/Higgs/WplusHJ_HanythingJ_NNPDF31_13TeV/HWplusJ_HanythingJ_NNPDF31_13TeV_Vhadronic_template.input'
gridpack_path_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/HWJ_slc6_amd64_gcc700_CMSSW_10_2_22_HWplusJ_M{__MASS__}/v1/HWJ_slc6_amd64_gcc700_CMSSW_10_2_22_HWplusJ_M{__MASS__}.tgz'
dataset_name_template = 'WplusH_WToQQ_HToInvisible_M{__MASS__}_TuneCP5_13TeV_powheg_pythia8'

mass_points = [110,150,200,300,400,500,600,800,1000]

prep_ids = [
    'HIG-RunIIFall17wmLHEGS-05387',
    'HIG-RunIIFall17wmLHEGS-05388',
    'HIG-RunIIFall17wmLHEGS-05389',
    'HIG-RunIIFall17wmLHEGS-05390',
    'HIG-RunIIFall17wmLHEGS-05391',
    'HIG-RunIIFall17wmLHEGS-05392',
    'HIG-RunIIFall17wmLHEGS-05393',
    'HIG-RunIIFall17wmLHEGS-05394',
    'HIG-RunIIFall17wmLHEGS-05395'
]

wminush_csv = pjoin(outdir, 'wplush_2017.csv')

with open(wminush_csv, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(['PrepID', 'Fragment'])
    for idx, mass_point in enumerate(mass_points):
        gridpack_path = gridpack_path_template.format(__MASS__ = mass_point)
        lhe_fragment = lhe_fragment_template.format(
            __LINK__ = proc_card_link,
            __GRIDPACK__ = gridpack_path
        )
        pythia_fragment = pythia_fragment_template.format(
            __MASS__ = mass_point
        )
        fragment = complete_fragment_template.format(
            __LHE_FRAGMENT__ = lhe_fragment,
            __PYTHIA_FRAGMENT__ = pythia_fragment,
            __SEQUENCE__ = sequence
        )
    
        # Write to CSV file
        prepid = prep_ids[idx]
        writer.writerow([prepid, fragment])
