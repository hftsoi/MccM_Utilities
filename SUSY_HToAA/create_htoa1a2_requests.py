from lib.request_creator import RequestCreator

# Files containing fragment templates for each process type
fragment_files = {
    'WH/ZH'   : {
        2016: './fragments/2016/fragment_cascade_wh_zh.py',
        2017: './fragments/fragment_cascade_wh_zh.py',
        2018: './fragments/fragment_cascade_wh_zh.py'
    },
    'ggH/VBF' : {
        2016: './fragments/2016/fragment_cascade_ggh_qqh.py',
        2017: './fragments/fragment_cascade_ggh_qqh.py',
        2018: './fragments/fragment_cascade_ggh_qqh.py'
    }
}

def create_wh_zh_requests():
    '''Create CSV files containing configuration of the WH and ZH requests'''
    # Gridpack locations 
    gridpack_location_temps = {
        'WH': {
            2016: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/Wh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/Wh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2017: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/Wh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/Wh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2018: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/Wh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/Wh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
            },
        'ZH': {
            2016: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/Zh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/Zh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2017: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/Zh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/Zh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2018: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/Zh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/Zh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
            }
    }
    
    # Careful about the mass 1/2 naming convention here!
    dataset_name_temps = {
        'WH': 'Cascade_WlepH125ToA1A2To3A1_A1ToBBorTauTau_MA2-{__MASS1__}_MA1-{__MASS2__}_Filter_TuneCP5_13TeV_madgraph_pythia8',
        'ZH': 'Cascade_ZlepH125ToA1A2To3A1_A1ToBBorTauTau_MA2-{__MASS1__}_MA1-{__MASS2__}_Filter_TuneCP5_13TeV_madgraph_pythia8'
    }

    # List of several quantities
    mass_points = [
        (40,15),
        (60,15),
        (80,15),
        (100,15),
        (40,20),
        (60,20),
        (80,20),
        (100,20),
        (60,30),
        (80,30)
    ]
    years = [2016, 2017, 2018]
    filter_effs_dict = {
        'WH': [0.015]*5 + [0.02]*5,
        'ZH': [0.02]*4 + [0.012] + [0.02]*5
    }
    # Number of events before filter for each mass point (same for WH and ZH)
    num_events = [200000]*10
    
    for proc in ['WH', 'ZH']:
        dataset_name_temp = dataset_name_temps[proc]
        gridpack_location_temp = gridpack_location_temps[proc]
        tag = proc.lower()
        filter_effs = filter_effs_dict[proc]

        template_dict = {
            'Dataset name': dataset_name_temp, 
            'Gridpack path': gridpack_location_temp
        }
        
        # Dump the request to csv files
        r = RequestCreator(
            template_dict=template_dict,
            fragment_files=fragment_files,
            mass_points=mass_points,
            filter_effs=filter_effs,
            num_events=num_events,
            years=years, tag=tag,
            dtype='HToA1A2_cascade'
        )
        
        r.dump_to_csv()

def create_vbf_ggh_requests():
    '''Create CSV files containing configuration of the VBF and ggH requests'''
    # Gridpack locations 
    gridpack_location_temps = {
        'VBF': {
            2016: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/vbfh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/vbfh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2017: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/vbfh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/vbfh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2018: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/vbfh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/vbfh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
        },
        'ggH': {
            2016: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/ggh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/ggh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2017: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/ggh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/ggh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2018: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/ggh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1/v1/ggh3_M125_Toh1h2_M{__MASS2__}_M{__MASS1__}_h2_Toh1h1_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
            }
    }
    
    # Careful about the mass 1/2 naming convention here!
    dataset_name_temps = {
        'VBF': 'Cascade_VBFH125ToA1A2To3A1_A1ToBBorTauTau_MA2-{__MASS1__}_MA1-{__MASS2__}_Filter_TuneCP5_13TeV_madgraph_pythia8',
        'ggH': 'Cascade_ggH125ToA1A2To3A1_A1ToBBorTauTau_MA2-{__MASS1__}_MA1-{__MASS2__}_Filter_TuneCP5_13TeV_madgraph_pythia8'
    }

    # List of several quantities
    mass_points = [
        (40,15),
        (60,15),
        (80,15),
        (100,15),
        (40,20),
        (60,20),
        (80,20),
        (100,20),
        (60,30),
        (80,30)
    ]
    years = [2016, 2017, 2018]
    filter_effs_dict = {
        'VBF' : [0.003, 0.002, 0.002, 0.003, 0.003, 0.004, 0.005, 0.004, 0.004, 0.003],
        'ggH' : [0.003, 0.002, 0.002, 0.003, 0.003, 0.004, 0.005, 0.004, 0.003, 0.002]
    }
    
    # Number of events before filter for each mass point (same for VBF and ggH)
    num_events = [200000]*10
    
    for proc in ['ggH', 'VBF']:
        dataset_name_temp = dataset_name_temps[proc]
        gridpack_location_temp = gridpack_location_temps[proc]
        tag = proc.lower()
        filter_effs = filter_effs_dict[proc]

        template_dict = {
            'Dataset name': dataset_name_temp, 
            'Gridpack path': gridpack_location_temp
        }
        
        # Dump the request to csv files
        r = RequestCreator(
            template_dict=template_dict,
            fragment_files=fragment_files,
            mass_points=mass_points,
            filter_effs=filter_effs,
            num_events=num_events,
            years=years, tag=tag,
            dtype='HToA1A2_cascade'
        )
        
        r.dump_to_csv()

def main():
    create_wh_zh_requests()
    create_vbf_ggh_requests()

if __name__ == '__main__':
    main()
