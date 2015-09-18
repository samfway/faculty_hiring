#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import os
import time
import argparse
import urllib
import string
from bs4 import BeautifulSoup


GS_URL = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=%s&hl=en&oi=ao'
GS_PROFILE_URL = 'https://scholar.google.com/citations?hl=en&user=%s&view_op=list_works&sortby=pubdate&cstart=%d&pagesize=%d'
GS_PAGE_SIZE = 100
GS_NAME_FIELD = 0
GS_ID_FIELD = 2


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--profile-file', help='List of faculty profiles')
    args.add_argument('-s', '--start-after', help='What was the last successful record', default=None)
    args.add_argument('-o', '--output-dir', help='Output directory')
    args.add_argument('-e', '--error-file', help='Profiles needing inspection')
    args.add_argument('-p', '--page-number', help='Page number', type=int, default=0)
    args.add_argument('-a', '--grab-all', help='Grab all pubs', action="store_true")
    args = args.parse_args()
    return args


def download_gs_page(gs_id, output_prefix, page_number):
    filename = output_prefix + gs_id + '_file_%d.html' % (page_number)
    cstart = page_number * GS_PAGE_SIZE
    url = GS_PROFILE_URL % (gs_id, cstart, GS_PAGE_SIZE)
    fname, response = urllib.urlretrieve(url, filename)
    return response, filename


def download_all_gs_pages(gs_id, output_prefix, start_at=0):
    not_done = True
    grab = start_at

    while not_done:
        resp, filename = download_gs_page(gs_id, output_prefix, grab)
        not_done = has_more_pubs(filename)  # Check if there are more pubs
        grab += 1
        time.sleep(2)


def has_more_pubs(filename, page_size=100):
    """ Check the Google scholar results page. Determine if there are
        additional pages of publications.

        For now, this is done by looking for the range of publications,
        which indicates that there are additional pages.
    """ 
    has_more = False
    html = open(filename, 'rU').read()
    soup = BeautifulSoup(html, "html.parser") 
    sep = u'\u2013'

    try:
        spans = soup.findAll('span', {'id': 'gsc_a_nn'})
        for span in spans:
            if sep in span.text:
                start, stop = [int(x) for x in span.text.split(sep)]
                if start - 1 + page_size == stop:  # 1-100, 101-200, etc.
                    has_more = True
    except:
        pass
        
    return has_more
        

if __name__=="__main__":
    args = interface()
    
    output_prefix = os.path.join(args.output_dir, 'GSP_')
    look_for = args.start_after  # Name to start after
    collect = look_for is None   # If name is None, start right away
    error_out = open(args.error_file, 'w')
    grab_all = args.grab_all

    c = 0
    for line in open(args.profile_file, 'rU'):
        line = line.strip()
        if collect == False:
            if line.startswith(look_for):
                collect = True
            continue  # skip to next record

        pieces = line.split(',')
        if len(pieces) != 6:
            error_out.write('%s\n' % line) 
            continue

        gs_name = pieces[GS_NAME_FIELD]
        gs_id = pieces[GS_ID_FIELD]
        if not grab_all:
            # Just grab the one file
            resp, filename = download_gs_page(gs_id, output_prefix, args.page_number)
            time.sleep(2)
        else:
            download_all_gs_pages(gs_id, output_prefix, args.page_number)
        print c, gs_name, gs_id
        c += 1
        
    error_out.close()
