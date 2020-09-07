import os
import csv

pjoin = os.path.join

class RequestCreator():
    '''Class to create request configurations and save them into output CSV files.'''
    def __init__(self, template_dict, fragment_files, tag, mass_points, 
                filter_effs, num_events, dtype='HToAA', years=[2016, 2017, 2018]):
        self.dtype = dtype
        # Set some member variables
        self.dataset_name_template = template_dict['Dataset name']
        self.fragment_files = fragment_files
        self.gridpack_path_template = template_dict['Gridpack path']
        # If dtype is not 'HToAA', mass_points should be a list of tuples, for the a1, a2 masses
        self.mass_points = mass_points
        self.filter_effs = filter_effs
        self.num_events = num_events
        self.years = years
        self.tag = tag
        self.dtype = dtype

        # Do some internal checks before moving on
        self._internal_checks()

    def _internal_checks(self):
        if self.dtype not in ['HToAA', 'HToA1A2_cascade', 'Noncascade_mtt_larger_mbb', 'Noncascade_mtt_smaller_mbb']:
            raise ValueError('Type is not acceptable, please check: {}'.format(self.dtype))

        if self.dtype != 'HToAA':
            if not isinstance(self.mass_points[0], tuple):
                raise ValueError('For this decay mode, each mass point should be a tuple containing A1 and A2 masses.')
        else:
            if not (isinstance(self.mass_points[0], float) or isinstance(self.mass_points[0], int)):
                raise ValueError('For this decay mode, each mass point should be an integer or float.')

    def _get_fragment_temp(self, proc, year):
        '''Read and return the fragment template for the relevant process type.'''
        fragment_temp_file = self.fragment_files[proc][year]
        with open(fragment_temp_file, 'r') as f:
            fragment_temp = f.read().replace('mygridpack.tgz', '{__GRIDPACK__}') 
    
        return fragment_temp


    def set_values_for_single_mp(self, mass_point, year):
        '''Set gridpack path, dataset name and fragment for a given mass point.'''
        tunes = {
            2016: 'CUETP8M1', 
            2017: 'CP5', 
            2018: 'CP5'
        }
        pythia_tune = tunes[year]

        if self.dtype == 'HToAA':
            self.gridpack_path = self.gridpack_path_template.format(__MASS__=mass_point)
            self.dataset_name = self.dataset_name_template.format(__MASS__=mass_point, __TUNE__=pythia_tune)
        else:
            self.gridpack_path = self.gridpack_path_template.format(__MASS1__=mass_point[0], __MASS2__=mass_point[1])
            self.dataset_name = self.dataset_name_template.format(__MASS1__=mass_point[0], 
                                            __MASS2__=mass_point[1], 
                                            __TUNE__=pythia_tune)
        
        # Get fragment template
        if self.tag in ['ggh', 'vbf']:
            proc = 'ggH/VBF'
        elif self.tag in ['wh', 'zh']:
            proc = 'WH/ZH'
        self.fragment_template = self._get_fragment_temp(proc=proc, year=year)
        self.fragment = self.fragment_template.format(__GRIDPACK__=self.gridpack_path)

    def return_dict(self):
        '''Set gridpack path, dataset name and fragment for all mass points and return them in a dictionary.'''
        request_info = {}
        for year in self.years:
            request_info[year] = {}
            for idx, mass_point in enumerate(self.mass_points):
                self.set_values_for_single_mp(mass_point, year)
                request_info[year][mass_point] = {
                    'Fragment' : self.fragment,
                    'Gridpack' : self.gridpack_path,
                    'Dataset name' : self.dataset_name,
                    'Filter efficiency' : self.filter_effs[idx],
                    'Number of Events'  : self.num_events[idx],
                    'Notes' : self.dataset_name.split('_') 
                }

        return request_info

    def dump_to_csv(self):
        '''Dump the request information in dictionary to an output CSV file.'''
        # Create the output CSV file
        outdir = './{}/csv'.format(self.dtype)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        # Get dictionary containing request information for all years/mass points
        request_dict = self.return_dict()

        # Save into separate CSV files for each year
        for year in self.years:
            csvfile = pjoin(outdir, '{}_{}_requests.csv'.format(self.tag, year))
            with open(csvfile, 'w+') as f:
                fieldnames = ['Dataset name', 'Gridpack', 'Number of Events', 'Filter efficiency', 'Fragment', 'Notes']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                for mass_point in self.mass_points:
                    request_info = request_dict[year][mass_point]
                    writer.writerow(request_info)

        print('CSV file saved: {}'.format(csvfile))
