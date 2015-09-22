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
from faculty_hiring.scripts.download_dblp_profiles import download_dblp_page, get_dblp_url
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
    gs_prefix = os.path.join(args.gs_dir, 'GSP_')
    dblp_prefix = os.path.join(args.dblp_dir, 'DBLP_')

    for f in faculty:
        # Check for each profile, download if missing
        if 'gs' in f:
            gs_file = os.path.join(args.gs_dir, GS_FILE % f['gs'])
            if not os.path.isfile(gs_file):
                print 'GS -> ', f['facultyName']
                download_all_gs_pages(f['gs'], gs_prefix)
            
        if 'dblp' in f:
            dblp_file = os.path.join(args.dblp_dir, DBLP_FILE % f['dblp'])
            if not os.path.isfile(dblp_file):
                print 'DBLP -> ', f['facultyName']
                dblp_url = get_dblp_url(f['dblp'])
                download_dblp_page(dblp_url, dblp_prefix)
