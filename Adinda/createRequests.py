import csv
from fragments import *

import argparse
parser = argparse.ArgumentParser(prog="createRequests")
parser.add_argument("--years", type=str, choices=['2016','2017','2018'], nargs='*',
                              required=True, help="MC year condition (2016-2017-2018)" )
args = parser.parse_args()


years = args.years

for year in years:
    with open('Zphi_rho_Powheg_'+year+'.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Dataset name','Events', 'fragment','notes','Generator'])

        for mode, nevents in production_modes_events.items():
            gridpacks = gridpacks_dict[mode]
            for res in resonances:
                #for ds_name in dataset_names.item():
                ds_name = dataset_names[year].format(mode, res)
                runcard_link = gridpacks[year][1]
                gridpack_path = gridpacks[year][0]
                pythia_fragment = pythia_fragmets_dict[mode+'_'+res][year]
                fragment = lhe_fragmet.replace('__LINK__',runcard_link).replace('__GRIDPACK__',gridpack_path).replace('__PYTHIA_FRAGMENT__',pythia_fragment)
                csvwriter.writerow([ds_name,nevents,fragment,ds_name.split('_'),'Powheg+Pythia'])
                    #print(year, ds_name.format(mode,res))
                    #print(lhe_fragmet.replace('__LINK__',runcard_link).replace('__GRIDPACK__',gridpack_path).replace('__PYTHIA_FRAGMENT__',fragment))
                    #print(pythia_fragmets_dict[mode][year])
