import os
import csv

pjoin = os.path.join

# ================================
# Script to add missing MCDB ID
# for some requests on McM.
# ================================

# PrepIDs of the requests which are effected
prep_id_list = ['HIG-RunIIFall17wmLHEGS-05{}'.format(num) for num in range(673,717)]

mcdb_id = 0

# Write into the output csv file
outdir = './csv/patches'
if not os.path.exists(outdir):
    os.makedirs(outdir)

outfile = pjoin(outdir, 'missing_mcdb_id_info.csv')
with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(['PrepID', 'MCDBID'])
    for prep_id in prep_id_list:
        writer.writerow([prep_id, mcdb_id])