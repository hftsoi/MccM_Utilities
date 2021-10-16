### Get the request information and create csv files.
import csv
import argparse
from container_ggh_UL import request_information # Holds all information about the requests
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--years", choices=[2016,2017,2018], nargs='*', type=int,
                              required=True, help="MC year condition (2016-2017-2018)" )

args = parser.parse_args()
years = args.years

for year in years:
    requests = request_information[year]
    with open('GluGluHToAAToMuMuTauTau_{__YEAR__}.csv'.format(__YEAR__=year), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['Dataset name', 'Events', 'Filter efficiency', 'Match efficiency','fragment', 'notes', 'generator'], extrasaction='ignore')
        writer.writeheader()
        for mass_point in requests.keys():
            data = requests[mass_point]
            writer.writerow(data)
