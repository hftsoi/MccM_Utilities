import subprocess
import argparse
from glob import glob

# =================================
# Wrapper script to create request CSV files
# =================================

def create_csv():
    '''Call the relevant python scripts to create CSV files for given requests.'''
    # List of scripts to use for CSV file generation
    scripts = glob('create_h*.py') + glob('create_non_cascade*.py')

    for script in scripts:
        print('Calling script: {}'.format(script))
        cmd = ['python', script]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

def main():
    create_csv()


if __name__ == '__main__':
    main()

