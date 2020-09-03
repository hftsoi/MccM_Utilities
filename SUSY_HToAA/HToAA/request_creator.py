import os
import csv

pjoin = os.path.join

class RequestCreator():
    def __init__(self, template_dict, tag, mass_points, filter_effs, num_events, years=[2016, 2017, 2018]):
        # Set some member variables
        self.dataset_name_template = template_dict['Dataset name']
        self.fragment_template = template_dict['Fragment']
        self.gridpack_path_template = template_dict['Gridpack path']
        self.mass_points = mass_points
        self.filter_effs = filter_effs
        self.num_events = num_events
        self.years = years
        self.tag = tag
    
    def set_values_for_single_mp(self, mass_point):
        '''Set gridpack path, dataset name and fragment for a given mass point.'''
        self.gridpack_path = self.gridpack_path_template.format(__MASS__=mass_point)
        self.dataset_name = self.dataset_name_template.format(__MASS__=mass_point)
        self.fragment = self.fragment_template.format(__GRIDPACK__=self.gridpack_path)

    def return_dict(self):
        '''Set gridpack path, dataset name and fragment for all mass points and return them in a dictionary.'''
        request_info = {}
        for year in self.years:
            request_info[year] = {}
            for idx, mass_point in enumerate(self.mass_points):
                self.set_values_for_single_mp(mass_point)
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
        outdir = './output/csv'
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        # Get dictionary containing request information for all years/mass points
        request_dict = self.return_dict()

        # Save into separate CSV files for each year
        for year in self.years:
            csvfile = pjoin(outdir, '{}_{}_requests.csv'.format(self.tag, year))
            with open(csvfile, 'w+') as f:
                writer = csv.DictWriter(f)
                for mass_point in self.mass_points:
                    request_info = request_dict[year][mass_point]
                    writer.writerow(request_info)

        print('CSV file saved: {}'.format(csvfile))
