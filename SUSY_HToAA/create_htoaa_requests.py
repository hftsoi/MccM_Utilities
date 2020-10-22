import os
from lib.request_creator import RequestCreator

pjoin = os.path.join

# =======================================================================
# Dump the WH and ZH requests configuration into csv files for all three years. 
# =======================================================================

# Files containing fragment templates for each process type
fragment_files = {
    'WH/ZH'   : {
        2016: './fragments/2016/fragment_symmetric_wh_zh.py',
        2017: './fragments/fragment_symmetric_wh_zh.py',
        2018: './fragments/fragment_symmetric_wh_zh.py',
    },
    'ggH/VBF' : {
        2016: './fragments/2016/fragment_symmetric_ggh_qqh.py',
        2017: './fragments/fragment_symmetric_ggh_qqh.py',
        2018: './fragments/fragment_symmetric_ggh_qqh.py'
    }
}

def create_wh_zh_requests():
    '''Create CSV files containing configuration of the WH and ZH requests'''
    # Gridpack locations 
    gridpack_location_temps = {
        'WH': {
            2016: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/Wh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/Wh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2017: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/Wh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/Wh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2018: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/Wh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/Wh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
        },
        'ZH': {
            2016: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/Zh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/Zh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2017: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/Zh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/Zh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2018: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/Zh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/Zh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
        }
    }
    dataset_name_temps = {
        'WH': 'SUSYWlepHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauReco_Tune{__TUNE__}_13TeV_madgraph_pythia8',
        'ZH': 'SUSYZlepHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauReco_Tune{__TUNE__}_13TeV_madgraph_pythia8'
    }

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
            'Gridpack path': gridpack_location_temp
        }
    
        # Dump the request to csv files
        r = RequestCreator(
            template_dict=template_dict,
            fragment_files=fragment_files,
            mass_points=mass_points,
            filter_effs=filter_effs,
            num_events=num_events,
            years=years, tag=tag
        )
        
        r.dump_to_csv()

def create_vbf_ggh_requests():
    '''Create CSV files containing configuration of the VBF and ggH requests'''
    # Gridpack locations 
    gridpack_location_temps = {
        'VBF': {
            2016: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/vbfh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/vbfh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2017: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/vbfh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/vbfh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2018: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/vbfh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/vbfh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
        },
        'ggH': {
            2016: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/madgraph/V5_2.6.5/ggh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/ggh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2017: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/ggh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/ggh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz',
            2018: '/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.5/ggh01_M125_Toa01a01_M{__MASS__}_Tobbtautau/v1/ggh01_M125_Toa01a01_M{__MASS__}_Tobbtautau_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
        }
    }
    dataset_name_temps = {
        'VBF': 'SUSYVBFHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauTrigger_Tune{__TUNE__}_13TeV_madgraph_pythia8',
        'ggH': 'SUSYGluGluToHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauTrigger_Tune{__TUNE__}_13TeV_madgraph_pythia8'
    }

    # List of several quantities (common between WH and ZH)
    mass_points = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    years = [2016, 2017, 2018]
    filter_effs_dict = {
        'ggH' : [0.03]*2 + [0.03215]*9,
        'VBF' : [0.065]*3 + [0.06816]*8 
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
            'Gridpack path': gridpack_location_temp
        }
    
        # Dump the request to csv files
        r = RequestCreator(
            template_dict=template_dict,
            fragment_files=fragment_files,
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