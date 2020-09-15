import os
import csv

pjoin = os.path.join

# Get the fragment template (same for 2017 and 2018)
fragment_temp_file = './fragments/semi_leptonic_fragment.py'
with open(fragment_temp_file, 'r') as f:
    fragment_temp = f.read()
