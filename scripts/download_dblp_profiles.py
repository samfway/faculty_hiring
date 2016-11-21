#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import os
import re
import time
import argparse
import urllib
import string
from bs4 import BeautifulSoup


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--profile-file', help='List of faculty profiles')
    args.add_argument('-s', '--start-after', help='What was the last successful record', default=None)
    args.add_argument('-o', '--output-dir', help='Output directory')
    args = args.parse_args()
    return args


def get_author_tag(dblp_url):
    return re.findall(r'(?<=pers/hd/./)[^,]+(?=,?)', dblp_url)[0]


def get_dblp_url(author_tag):
    first_letter = author_tag[0].lower()
    return 'http://dblp.uni-trier.de/pers/hd/%s/%s' % (first_letter, author_tag)


def download_dblp_page(dblp_url, output_prefix, page_number=0):
    author_tag = get_author_tag(dblp_url)
    filename = output_prefix + author_tag + '_file_%d.html' % (page_number)
    fname, response = urllib.urlretrieve(dblp_url, filename)
    return response, filename


if __name__=="__main__":
    args = interface()

    print 'USE download_all.py INSTEAD!'
    exit()
    
    output_prefix = os.path.join(args.output_dir, 'DBLP_')
    look_for = args.start_after  # Name to start after
    collect = look_for is None   # If name is None, start right away

    c = 0
    for line in open(args.profile_file, 'rU'):
        line = line.strip()
        if collect == False:
            if line.startswith(look_for):
                collect = True
            continue  # skip to next record

        pieces = line.split(',')
        if len(pieces) < 2:
            continue

        dblp_name = pieces[0]
        dblp_url = pieces[1].split(';')[0]
        download_dblp_page(dblp_url, output_prefix)
            
        print c, dblp_name

        time.sleep(2)
        c += 1
        
