import os
import csv

pjoin = os.path.join

# ================================
# Script to add missing time/event and 
# size/event values for some requests on McM.
# ================================

# PrepIDs of the requests which are effected
prep_id_list = ['HIG-RunIIFall17wmLHEGS-05{}'.format(num) for num in range(673,717)]

time_event = 100
size_event = 1000

# Write into the output csv file
outdir = './csv/patches'
if not os.path.exists(outdir):
    os.makedirs(outdir)

outfile = pjoin(outdir, 'missing_timeevent_sizeevent_info.csv')
with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(['PrepID', 'Time per event (s)', 'Size per event (kB)'])
    for prep_id in prep_id_list:
        writer.writerow([prep_id, time_event, size_event])