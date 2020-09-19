import os
import csv

pjoin = os.path.join

# Get the fragment template (same for 2017 and 2018)
fragment_temp_file = './fragments/fully_leptonic_fragment.py'
with open(fragment_temp_file, 'r') as f:
    fragment_temp = f.read()

# TODO: Once the gridpacks are loaded to cvmfs, add the paths for each mass point here
gridpack_path_temp = ''

# TODO: Check the dataset name with authors!
dataset_name_temp = 'ChargedHiggsToWToLNu_M{__MASS__}_TuneCP5_13TeV-madgraph-pythia8' 
# Link to proc cards PR
proc_card_link = 'https://github.com/cms-sw/genproductions/pull/2717'

mass_points = list(range(200,1100,100)) + [1500,2000]
# Same number of events for each mass point
num_events = int(1.5e5)
filter_eff = 1.0
match_eff = 1.0

# Accumulate the information about each request and write all into a CSV file
for year in [2017, 2018]:
    csv_dir = './csv'
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    csv_file = pjoin(csv_dir, 'fully_leptonic_{}.csv'.format(year))
    with open(csv_file, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['Dataset name', 'Events', 'Gridpack', 'Filter efficiency', 'Match efficiency', 'Fragment', 'Notes'])
        for mass_point in mass_points:
            dataset_name = dataset_name_temp.format(__MASS__ = mass_point)
            gridpack_path = gridpack_path_temp.format(__MASS__ = mass_point)
            fragment = fragment_temp.format(
                __LINK__ = proc_card_link,
                __GRIDPACK__ = gridpack_path
            )
            notes = dataset_name.split('_')
            info = [dataset_name, num_events, gridpack_path, filter_eff, match_eff, fragment, notes]
            writer.writerow(info)