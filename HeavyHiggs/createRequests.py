from container import get_containers
from pprint import pprint
import csv
import argparse

container_dict = get_containers()

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--years", type=str, choices=['2017','2018'], nargs='*',
                              required=True, help="MC year condition (2017-2018)" )

args = parser.parse_args()
years = args.years

for year in years:
	container = container_dict[year]
	with open('HtoTTbar_{__YEAR__}.csv'.format(__YEAR__=year), 'w') as f:
		writer = csv.DictWriter(f, fieldnames=['Dataset name', 'Events', 'Filter efficiency', 'fragment', 'notes', 'generator'], extrasaction='ignore')
		writer.writeheader()
		for higgstype in container.keys(): # Scalar or psuedo
			for sampletype in container[higgstype].keys(): # Interference or resonance sample
				for masspoint in container[higgstype][sampletype].keys():
					data = container[higgstype][sampletype][masspoint]
					writer.writerow(data)



