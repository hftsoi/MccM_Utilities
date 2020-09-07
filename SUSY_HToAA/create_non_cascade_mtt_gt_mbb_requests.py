from lib.request_creator import RequestCreator

# Files containing fragment templates for each process type
fragment_files = {
    'WH/ZH'   : {
        2016: './fragments/2016/fragment_noncascade_mttgtmbb_wh_zh.py',
        2017: './fragments/fragment_noncascade_mttgtmbb_wh_zh.py',
        2018: './fragments/fragment_noncascade_mttgtmbb_wh_zh.py'
    },
    'ggH/VBF' : {
        2016: './fragments/2016/fragment_noncascade_mttgtmbb_ggh_qqh.py',
        2017: './fragments/fragment_noncascade_mttgtmbb_ggh_qqh.py',
        2018: './fragments/fragment_noncascade_mttgtmbb_ggh_qqh.py'
    }
}

def create_wh_zh_requests():
    '''Create CSV files containing configuration of the WH and ZH requests'''
    # Gridpack locations 
    # TODO: Put gridpack location here once they are on CVMFS
    gridpack_location_temps = {
        'WH': '',
        'ZH': ''
    }
    
    dataset_name_temps = {
        'WH' : 'SUSYWlepHA1A2_A1ToTauTau_A2ToBB_MA1-{__MASS1__}_MA2-{__MASS2__}_FilterTauTauReco_TuneCP5_13TeV_madgraph_pythia8',
        'ZH' : 'SUSYZlepHA1A2_A1ToTauTau_A2ToBB_MA1-{__MASS1__}_MA2-{__MASS2__}_FilterTauTauReco_TuneCP5_13TeV_madgraph_pythia8'
    }

    # List of several quantities
    mass_points = [
        (20,15),
        (30,15),
        (30,20),
        (40,20),
        (40,30),
        (50,30),
        (60,30),
        (50,40),
        (60,40),
        (70,40),
        (80,40),
        (60,50)
    ]
    years = [2016, 2017, 2018]
    filter_effs_dict = {
        'WH': [0.15]*12,
        'ZH': [0.15]*12
    }
    # Number of events before filter for each mass point (same for WH and ZH)
    num_events = [125000]*12

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
            dtype='Noncascade_mtt_larger_mbb'
        )
        
        r.dump_to_csv()

def create_vbf_ggh_requests():
    '''Create CSV files containing configuration of the VBF and ggH requests'''
    # Gridpack locations 
    # TODO: Put gridpack location here once they are on CVMFS
    gridpack_location_temps = {
        'VBF': '',
        'ggH': ''
    }
    
    dataset_name_temps = {
        'VBF' : 'SUSYVBFHToA1A2_A1ToTauTau_A2ToBB_MA1-{__MASS1__}_MA2-{__MASS2__}_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8',
        'ggH' : 'SUSYGluGluToHToA1A2_A1ToTauTau_A2ToBB_MA1-{__MASS1__}_MA2-{__MASS2__}_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8'
    }

    # List of several quantities
    mass_points = [
        (20,15),
        (30,15),
        (30,20),
        (40,20),
        (40,30),
        (50,30),
        (60,30),
        (50,40),
        (60,40),
        (70,40),
        (80,40),
        (60,50)
    ]
    years = [2016, 2017, 2018]
    filter_effs_dict = {
        'VBF': [0.02, 0.023, 0.02, 0.04, 0.02, 0.02, 0.01, 0.02, 0.023, 0.037, 0.02, 0.02, 0.02],
        'ggH': [0.03]*8 + [0.035]*5
    }
    # Number of events before filter for each mass point (same for WH and ZH)
    num_events = [125000]*13

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
            dtype='Noncascade_mtt_smaller_mbb'
        )
        
        r.dump_to_csv()

def main():
    create_wh_zh_requests()
    create_vbf_ggh_requests()

if __name__ == '__main__':
    main()
