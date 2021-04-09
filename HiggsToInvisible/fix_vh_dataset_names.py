import csv
import os
import sys

pjoin = os.path.join

### For the existing VH requests on McM, fix the dataset names by adding the tune being used.

# PrepIDs for all requests
prep_ids = {
    'HWminusJ_2017':
        ['HIG-RunIIFall17wmLHEGS-05378', 'HIG-RunIIFall17wmLHEGS-05379', 'HIG-RunIIFall17wmLHEGS-05380', 'HIG-RunIIFall17wmLHEGS-05381',
         'HIG-RunIIFall17wmLHEGS-05382', 'HIG-RunIIFall17wmLHEGS-05383', 'HIG-RunIIFall17wmLHEGS-05384', 'HIG-RunIIFall17wmLHEGS-05385',
         'HIG-RunIIFall17wmLHEGS-05386'
        ],
    'HWplusJ_2017':
        ['HIG-RunIIFall17wmLHEGS-05387', 'HIG-RunIIFall17wmLHEGS-05388', 'HIG-RunIIFall17wmLHEGS-05389', 'HIG-RunIIFall17wmLHEGS-05390',
         'HIG-RunIIFall17wmLHEGS-05391', 'HIG-RunIIFall17wmLHEGS-05392', 'HIG-RunIIFall17wmLHEGS-05393', 'HIG-RunIIFall17wmLHEGS-05394',
         'HIG-RunIIFall17wmLHEGS-05395'
        ],
    'HZJ_2017':
        ['HIG-RunIIFall17wmLHEGS-05396', 'HIG-RunIIFall17wmLHEGS-05397', 'HIG-RunIIFall17wmLHEGS-05398', 'HIG-RunIIFall17wmLHEGS-05399',
         'HIG-RunIIFall17wmLHEGS-05400', 'HIG-RunIIFall17wmLHEGS-05401', 'HIG-RunIIFall17wmLHEGS-05402', 'HIG-RunIIFall17wmLHEGS-05403',
         'HIG-RunIIFall17wmLHEGS-05404'
        ],
    'ggHZ_2017':
        ['HIG-RunIIFall17wmLHEGS-05405', 'HIG-RunIIFall17wmLHEGS-05406', 'HIG-RunIIFall17wmLHEGS-05407', 'HIG-RunIIFall17wmLHEGS-05408',
         'HIG-RunIIFall17wmLHEGS-05409', 'HIG-RunIIFall17wmLHEGS-05410', 'HIG-RunIIFall17wmLHEGS-05411', 'HIG-RunIIFall17wmLHEGS-05412',
         'HIG-RunIIFall17wmLHEGS-05413'
        ],
    'HWminusJ_2018':
        ['HIG-RunIIFall18wmLHEGS-04444', 'HIG-RunIIFall18wmLHEGS-04445', 'HIG-RunIIFall18wmLHEGS-04446', 'HIG-RunIIFall18wmLHEGS-04447',
         'HIG-RunIIFall18wmLHEGS-04448', 'HIG-RunIIFall18wmLHEGS-04449', 'HIG-RunIIFall18wmLHEGS-04450', 'HIG-RunIIFall18wmLHEGS-04451',
         'HIG-RunIIFall18wmLHEGS-04452'
        ],
}

dataset_name_templates = {
    'HWminusJ' : 'WminusH_WToQQ_HToInvisible_M{__MASS__}_TuneCP5_13TeV_powheg_pythia8',
    'HWplusJ'  : 'WplusH_WToQQ_HToInvisible_M{__MASS__}_TuneCP5_13TeV_powheg_pythia8',
    'HZJ'      : 'ZH_ZToQQ_HToInvisible_M{__MASS__}_TuneCP5_13TeV_powheg_pythia8',
    'ggHZ'     : 'ggZH_ZToQQ_HToInvisible_M{__MASS__}_TuneCP5_13TeV_powheg_pythia8',
}

output_dirs = {
    'HWminusJ' : './csv/WminusH_HToInv/dataset_name_fix',
    'HWplusJ'  : './csv/WplusH_HToInv/dataset_name_fix',
    'HZJ'      : './csv/ZH_HToInv/dataset_name_fix',
    'ggHZ'     : './csv/ggZH_HToInv/dataset_name_fix',
}

# Read in the process+year from the command line
request_tag = sys.argv[1]
process, year = request_tag.split('_')

mass_points = [110,150,200,300,400,500,600,800,1000]

# Output CSV file with fixed dataset names
outdir = output_dirs[process]
if not os.path.exists(outdir):
    os.makedirs(outdir)

outfile = pjoin(outdir, 'fixed_dataset_names_{}.csv'.format(year))

dataset_name_template = dataset_name_templates[process]
prepid_list = prep_ids[request_tag]

with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    # Write header
    writer.writerow(['PrepID', 'Dataset name'])
    for idx, mass in enumerate(mass_points):
        dataset_name = dataset_name_template.format(__MASS__ = mass)
        prepid = prepid_list[idx]
        writer.writerow([prepid, dataset_name])
