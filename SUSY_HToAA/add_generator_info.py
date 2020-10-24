import os
import csv

pjoin = os.path.join

# ================================
# Script to add missing generator information
# for some requests on McM.
# ================================

# PrepIDs of the requests which are effected
prep_id_list = ['HIG-RunIIFall17wmLHEGS-05{}'.format(num) for num in range(673,717)]

generator_info = 'Madgraph+Pythia'

# Write into the output csv file
outdir = './csv/patches'
if not os.path.exists(outdir):
    os.makedirs(outdir)

outfile = pjoin(outdir, 'missing_gen_info.csv')
with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(['PrepID', 'Generator'])
    for prep_id in prep_id_list:
        writer.writerow([prep_id, generator_info])