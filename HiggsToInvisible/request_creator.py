import os
import csv

pjoin = os.path.join

class RequestCreator:
    '''Class to create requests.'''
    def __init__(self, proc_tag, mass_points, 
        proc_card_link, dataset_name_template, gridpack_path_templates, 
        lhe_fragment_template, pythia_fragment_template, num_events_list, years,
        filter_eff=1.0, match_eff=1.0
        ):
        self.proc_tag = proc_tag
        self.mass_points = mass_points
        self.proc_card_link = proc_card_link
        self.dataset_name_template = dataset_name_template
        self.gridpack_path_templates = gridpack_path_templates
        self.lhe_fragment_template = lhe_fragment_template
        self.pythia_fragment_template = pythia_fragment_template
        self.num_events_list = num_events_list
        self.years = years
        # FIXME: Can genearlize for non-constant filter/match efficiency values
        self.filter_eff = filter_eff
        self.match_eff = match_eff

    def prepare_requests(self):
        '''Prepare the complete LHE+GEN production fragments for all requests and store them in a dictionary.'''
        # Loop over years and mass points, fill in the necessary parameters for each request and store them
        self.requests = {}
        for year in self.years:
            self.requests[year] = {}
            for idx, mass_point in enumerate(self.mass_points):
                print('MSG% Working on request: Mass={}, Year={}'.format(mass_point, year))
                # Fill in the LHE fragment first 
                dataset_name = self.dataset_name_template.format(__MASS__ = mass_point)
                # Get the gridpack path according to year (same for 2017/18, different only for 2016)
                if year == 2016:
                    gridpack_path_template = self.gridpack_path_templates['2016']
                elif year in [2017, 2018]:
                    gridpack_path_template = self.gridpack_path_templates['2017/2018']
                gridpack_path = gridpack_path_template.format(__MASS__ = mass_point)
                lhe_fragment = self.lhe_fragment_template.format(
                    __LINK__ = self.proc_card_link,
                    __GRIDPACK__ = gridpack_path
                )
                # Fill in the pythia fragment
                pythia_fragment = self.pythia_fragment_template.format(
                    __MASS__ = mass_point
                )

                complete_fragment_template = '''
                {__LHE_FRAGMENT__}
                
                {__PYTHIA_FRAGMENT__}
                
                {__SEQUENCE__}
                '''
                # Production sequence
                sequence = 'ProductionFilterSequence = cms.Sequence(generator)'

                # Prepare the full fragment
                complete_fragment = complete_fragment_template.format(
                    __LHE_FRAGMENT__    = lhe_fragment,
                    __PYTHIA_FRAGMENT__ = pythia_fragment, 
                    __SEQUENCE__        = sequence
                )

                # Store all the parameters for this request
                self.requests[year][mass_point] = {
                    'Dataset name'      : dataset_name,
                    'gridpack'          : gridpack_path,
                    'proc_card_link'    : self.proc_card_link,
                    'fragment'          : complete_fragment,
                    'Events'            : self.num_events_list[idx],
                    'generator'         : 'Powheg+Pythia8',
                    'Filter efficiency' : self.filter_eff,
                    'Match efficiency'  : self.match_eff,
                    'notes'             : dataset_name.split('_')
                }
    
    def write_to_csv(self):
        '''Having prepared the request information, write them to a CSV file.'''
        outdir = './csv/{}'.format(self.proc_tag)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        fieldnames = ['Dataset name', 'Events', 'Filter efficiency', 'Match efficiency','fragment', 'notes', 'generator']  

        for year in self.years:
            filename = '{}_{}_requests.csv'.format(self.proc_tag, year)
            filepath = pjoin(outdir, filename)
            print('MSG% Writing the request info to CSV file: {}'.format(filepath))
            with open(filepath, 'w+') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames,extrasaction='ignore')
                writer.writeheader()
                for mass_point in self.mass_points:
                    data = self.requests[year][mass_point]
                    writer.writerow(data)





