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
from faculty_hiring.parse.google_scholar import parse_gs_page
from faculty_hiring.parse.dblp import parse_dblp_page
try:
   import cPickle as pickle
except:
   import pickle


GS_FILE = 'GSP_%s_file_%d.html'
GS_PKL = 'GSP_%s.pkl'
DBLP_FILE = 'DBLP_%s_file_%d.html'
DBLP_PKL = 'DBLP_%s.pkl'


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
    num_processed = 0

    for f in faculty:
        if f['facultyName'] != 'Aravind Srinivasan':
            continue 

        # Check for each profile, download if missing
        if 'gs' in f:
            num_loaded = 0
            gs_file = os.path.join(args.gs_dir, GS_FILE % (f['gs'], num_loaded))
            all_pubs = []
            stats = None

            while os.path.isfile(gs_file):
                pubs, stats = parse_gs_page(open(gs_file).read())
                all_pubs += pubs
                num_loaded += 1
                gs_file = os.path.join(args.gs_dir, GS_FILE % (f['gs'], num_loaded))

            output_file = os.path.join(args.gs_dir, GS_PKL % f['gs']) 
            with open(output_file,'wb') as fp:
                pickle.dump(all_pubs, fp)
                pickle.dump(stats, fp)
            
        if 'dblp' in f:
            dblp_file = os.path.join(args.dblp_dir, DBLP_FILE % (f['dblp'], 0))
            all_pubs, stats = parse_dblp_page(open(dblp_file).read())
            
            output_file = os.path.join(args.dblp_dir, DBLP_PKL % f['dblp']) 
            with open(output_file,'wb') as fp:
                pickle.dump(all_pubs, fp)
                pickle.dump(stats, fp)
            
        print num_processed, f['facultyName']
        num_processed += 1
