from lib.request_creator import RequestCreator

# Files containing fragment templates for each process type
fragment_files = {
    'WH/ZH'   : './fragments/fragment_cascade_wh_zh.py',
    'ggH/VBF' : './fragments/fragment_cascade_ggh_qqh.py'
}

def get_fragment_temp(proc):
    '''Read and return the fragment template for the relevant process type.'''
    fragment_temp_file = fragment_files[proc]
    with open(fragment_temp_file, 'r') as f:
        fragment_temp = f.read().replace('mygridpack.tgz', '{__GRIDPACK__}') 

    return fragment_temp

def create_wh_zh_requests():
    '''Create CSV files containing configuration of the WH and ZH requests'''
    # Gridpack locations 
    # TODO: Put gridpack location here once they are on CVMFS
    gridpack_location_temps = {
        'WH': '',
        'ZH': ''
    }
    
    # Careful about the mass 1/2 naming convention here!
    dataset_name_temps = {
        'WH': 'SUSYWlepHA1A2_A2ToA1A1_A1ToBBorTauTau_MA2-{__MASS1__}_MA1-{__MASS2__}_FilterTauTauReco_TuneCP5_13TeV_madgraph_pythia8',
        'ZH': 'SUSYZlepHA1A2_A2ToA1A1_A1ToBBorTauTau_MA2-{__MASS1__}_MA1-{__MASS2__}_FilterTauTauReco_TuneCP5_13TeV_madgraph_pythia8'
    }
    
    # Get fragment template
    fragment_temp = get_fragment_temp('WH/ZH')

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
            'Gridpack path': gridpack_location_temp, 
            'Fragment': fragment_temp 
        }
        
        # Dump the request to csv files
        r = RequestCreator(
            template_dict=template_dict, 
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
    # TODO: Put gridpack location here once they are on CVMFS
    gridpack_location_temps = {
        'VBF': '',
        'ggH': ''
    }
    
    # Careful about the mass 1/2 naming convention here!
    dataset_name_temps = {
        'VBF': 'SUSYVBFHToA1A2_A2ToA1A1_A1ToBBorTauTau_MA2-{__MASS1__}_MA1-{__MASS2__}_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8',
        'ggH': 'SUSYGluGluToHToA1A2_A2ToA1A1_A1ToBBorTauTau_MA2-{__MASS1__}_MA1-{__MASS2__}_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8'
    }
    # Get fragment template
    fragment_temp = get_fragment_temp('ggH/VBF')

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
    # TODO: Confirm filter efficiencies with the analysis team!
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
            'Gridpack path': gridpack_location_temp, 
            'Fragment': fragment_temp 
        }
        
        # Dump the request to csv files
        r = RequestCreator(
            template_dict=template_dict, 
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
