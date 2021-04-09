import os
import csv
from pprint import pprint

# PrepIDS of the requests affected by the issue
prep_ids = [
    'HIG-RunIIFall17wmLHEGS-056{}'.format(num) for num in range(73,84)
]

# Read the correct fragments and filter efficiencies from the relevant csv file
infile = './csv/HToAA/ggh_2017_requests.csv'

with open(infile, 'r') as f:
    correct_fragments = []
    correct_filter_effs = []
    reader = csv.DictReader(f)
    for row in reader:
        correct_fragments.append(row['Fragment'])
        correct_filter_effs.append(row['Filter efficiency'])

# Write the corrected fragments and filter effs to an output file
outfile = './csv/patches/corrected_ggh_2017.csv'
with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(['PrepID', 'Fragment', 'Filter efficiency'])
    for idx in range(len(prep_ids)):
        writer.writerow([prep_ids[idx], correct_fragments[idx], correct_filter_effs[idx] ])





