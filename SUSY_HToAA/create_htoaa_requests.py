import os
from lib.request_creator import RequestCreator

pjoin = os.path.join

# =======================================================================
# Dump the WH and ZH requests configuration into csv files for all three years. 
# =======================================================================

# Files containing fragment templates for each process type
fragment_files = {
    'WH/ZH'   : './fragments/fragment_symmetric_wh_zh.py',
    'ggH/VBF' : './fragments/fragment_symmetric_ggh_qqh.py'
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
    dataset_name_temps = {
        'WH': 'SUSYWlepHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauReco_TuneCP5_13TeV_madgraph_pythia8',
        'ZH': 'SUSYZlepHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauReco_TuneCP5_13TeV_madgraph_pythia8'
    }

    # Get fragment template
    fragment_temp = get_fragment_temp('WH/ZH')

    # List of several quantities (common between WH and ZH)
    mass_points = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    years = [2016, 2017, 2018]
    filter_effs = [0.2]*5 + [0.25]*6
    # Number of events before filter for each mass point
    num_events = [150000]*11

    # Create CSV files for WH and ZH
    for proc in ['WH', 'ZH']:
        dataset_name_temp = dataset_name_temps[proc]
        gridpack_location_temp = gridpack_location_temps[proc]
        tag = proc.lower()

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
            years=years, tag=tag
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
        'VBF': 'SUSYVBFHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8',
        'ggH': 'SUSYGluGluToHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauTrigger_TuneCP5_13TeV_madgraph_pythia8'
    }

    # Get fragment template
    fragment_temp = get_fragment_temp('ggH/VBF')

    # List of several quantities (common between WH and ZH)
    mass_points = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    years = [2016, 2017, 2018]
    filter_effs_dict = {
        'ggH' : [0.03]*2 + [0.04]*9,
        'VBF' : [0.05]*11 
    }

    # Number of events after the filter is applied    
    num_events_dict = {
        'ggH' : [200000, 200000, 1000000, 200000, 200000, 200000, 1000000, 200000, 200000, 200000, 1000000],
        'VBF' : [200000]*11
    }

    # Create CSV files for WH and ZH
    for proc in ['ggH', 'VBF']:
        dataset_name_temp = dataset_name_temps[proc]
        gridpack_location_temp = gridpack_location_temps[proc]
        tag = proc.lower()

        filter_effs = filter_effs_dict[proc]
        num_events = num_events_dict[proc]

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
            years=years, tag=tag
        )
        
        r.dump_to_csv()

def main():
    create_wh_zh_requests()
    create_vbf_ggh_requests()

if __name__ == '__main__':
    main()