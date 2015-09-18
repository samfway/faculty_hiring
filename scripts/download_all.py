#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import os
import argparse
from faculty_hiring.parse.load import load_assistant_profs
from faculty_hiring.scripts.download_dblp_profiles import download_dblp_page
from faculty_hiring.scripts.download_google_scholar_profiles import download_all_gs_pages


GS_FILE = 'GSP_%s_file_0.html'
DBLP_FILE = 'DBLP_%s_file_0.html'


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--faculty-file', help='Faculty profiles')
    args.add_argument('-g', '--gs-dir', help='Directory of GS profiles')
    args.add_argument('-d', '--dblp-dir', help='Directory of DBLP profiles')
    args = args.parse_args()
    return args


if __name__=="__main__":
    args = interface()
    faculty = load_assistant_profs(open(args.faculty_file, 'rU')) 
    for f in faculty:
        if 'gs' in f:  # If they have a GS profile
            os.path.isfile(fname) 
            
