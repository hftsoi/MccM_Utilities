import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *  

import math

baseSLHATable="""
BLOCK QNUMBERS 5000001 # singlino singlinobar
      1     0  # 3 times electric charge
      2     2  # number of spin states (2S+1)
      3     1  # colour rep (1: singlet, 3: triplet, 6: sextet, 8: octet)
      4     1  # Particle/Antiparticle distinction (0=own anti)
BLOCK QNUMBERS 5000002 # singlet singletbar
      1     0  # 3 times electric charge
      2     1  # number of spin states (2S+1)
      3     1  # colour rep (1: singlet, 3: triplet, 6: sextet, 8: octet)
      4     1  # Particle/Antiparticle distinction (0=own anti)
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     1.00000000E+05   # ~d_L
   2000001     1.00000000E+05   # ~d_R
   1000002     1.00000000E+05   # ~u_L
   2000002     1.00000000E+05   # ~u_R
   1000003     1.00000000E+05   # ~s_L
   2000003     1.00000000E+05   # ~s_R
   1000004     1.00000000E+05   # ~c_L
   2000004     1.00000000E+05   # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     1.00000000E+05   # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     1.00000000E+05   # ~g
   1000022     1.00000000E+05   # ~chi_10
   1000023     1.00000000E+05   # ~chi_20
   1000025     1.00000000E+05   # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     %MCHI%           # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+
   1000039     1.0  # m(Gravitino)
   5000001     100.0  # m(singlino)
   5000002     90.0   # m(singlet)

# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.00000000E+00   # sdown_L decays
DECAY   2000001     0.00000000E+00   # sdown_R decays
DECAY   1000002     0.00000000E+00   # sup_L decays
DECAY   2000002     0.00000000E+00   # sup_R decays
DECAY   1000003     0.00000000E+00   # sstrange_L decays
DECAY   2000003     0.00000000E+00   # sstrange_R decays
DECAY   1000004     0.00000000E+00   # scharm_L decays
DECAY   2000004     0.00000000E+00   # scharm_R decays
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   1000006     0.00000000E+00   # stop1 decays
DECAY   2000006     0.00000000E+00   # stop2 decays
DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00  # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     0.00000000E+00   # gluino decays
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     0.00000000E+00   # neutralino2 decays
DECAY   1000024     1.00000000E-01   # chargino1+ decays
    0.00000000E+00   3    1000022   12   -11
    1.00000000E+00   2    5000001   24
DECAY   5000001     1.00000000E-03   # singlino decays
     1.00000000E+00    2     5000002   1000039        # BR(singlino -> singlet gravitino)
DECAY   5000002     1.00000000E-03   # singlet decays
     1.00000000E+00    2     21   21  # BR(singlet -> g g)
DECAY   1000025     0.00000000E+00   # neutralino3 decays
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
DECAY   1000039     0.00000000E+00   # gravitino decay
"""

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)

model = "Stealth_TChiWWpm"
print "pp -> C1 C1, C1 -> W S~"
print "W -> any, S~ -> S + G~, S -> g g"
# weighted average of matching efficiencies for the full scan
# must equal the number entered in McM generator params
mcm_eff = 0.44

def matchParams(mass):
  if mass < 124: return 76,0.64
  elif mass < 151: return 76, 0.6
  elif mass < 176: return 76, 0.57
  elif mass < 226: return 76, 0.54
  elif mass < 326: return 76, 0.51
  elif mass < 451: return 76, 0.48
  elif mass < 651: return 76, 0.45 
  elif mass < 751: return 76, 0.436
  elif mass < 851: return 76, 0.433
  elif mass < 951: return 76, 0.424
  elif mass < 1051: return 76, 0.421
  elif mass < 1151: return 76, 0.415
  elif mass < 1251: return 76, 0.407
  elif mass < 1351: return 76, 0.400
  elif mass < 1451: return 76, 0.394
  elif mass < 1551: return 76, 0.389
  elif mass < 1651: return 76, 0.384
  elif mass < 1751: return 76, 0.381
  elif mass < 1851: return 76, 0.379
  else: return 76, 0.379

nev = 100 # no. of events in thousands
chi_MassList = [300,350,400,450,500,550,600,
                650,700,750,800,850,900,950,1000,1050,1100,1150,1200]

cols = []
for mx in chi_MassList:
  col = []
  col.append([mx])
  cols.append(col)

mpoints = []
for col in cols: mpoints.extend(col)

for point in mpoints:
    print(point[0], nev)
    mchi  = point[0]
    qcut, tru_eff = matchParams(mchi)
    wgt = nev*(mcm_eff/tru_eff)
    
    slhatable = baseSLHATable.replace('%MCHI%','%e' % mchi)

    basePythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock, 
        JetMatchingParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = %.0f' % qcut, #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            'Check:abortIfVeto = on',
        ), 
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings', 
                                    'JetMatchingParameters'
        )
    )

    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(wgt),
            GridpackPath =  cms.string('/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/sus_sms/SMS-C1C1_v2/SMS-C1C1_mC1-%i_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz' % mchi),
            ConfigDescription = cms.string('%s_%i' % (model, mchi)),
            SLHATableForPythia8 = cms.string('%s' % slhatable),
            PythiaParameters = basePythiaParameters,
        ),
    )
