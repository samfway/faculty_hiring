#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import time
import argparse
import urllib2
import string
from bs4 import BeautifulSoup


GS_URL = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=%s&hl=en&oi=ao'


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--name-file', help='List of faculty names')
    args.add_argument('-s', '--start-after', help='What was the last successful record', default=None)
    args.add_argument('-o', '--output-file', help='Output CSV file')
    args = args.parse_args()
    return args


def sanitize(input_string):
    """ Remove all unicode characters """
    filtered = filter(lambda x: x in string.printable, input_string)
    filtered = filtered.replace(',', ';')
    return filtered 


def parse_google_scholar_profile(div):
    """ Parse a google scholar profile 
        out of a BeautifulSoup'd gsc_1usr_text div
    """ 
    profile = {}

    # Get the person's name... 
    profile['name'] = div.find("h3", { "class": "gsc_1usr_name" }).text

    # ...their GS id...
    temp = div.find("h3", { "class": "gsc_1usr_name" }).find("a")['href'].replace('/citations?user=', '')
    temp = temp.split('&')[0]
    profile['id'] = temp

    # ...their affiliation string... 
    try:
        profile['aff'] = div.find("div", { "class": "gsc_1usr_aff" }).text
    except:
        profile['aff'] = ''
    
    # ...and any associated tags.
    tags = []
    try:
        for link in div.findAll("a", attrs={'class': 'gsc_co_int'}):
            tags.append(link.text)
        profile['tags'] = '; '.join(tags)
    except:
        profile['tags'] = ''

    return profile

def get_google_scholar_profiles(name):
    """ Plug the faculty name into Google scholar and 
        see if there are any (maybe several) user ids.
        Save them all to the output file. 
        
        You'll have to go through by hand (yuck) to 
        determine who the real ones are! 

        Returns a list of Google Scholar ids, which
        is empty if there are none! """
    formatted_name = '+'.join(name.split())
    query_url = GS_URL % formatted_name
    results_page = urllib2.urlopen(query_url).read()
    soup = BeautifulSoup(results_page, "html.parser")
    divs = soup.findAll("div", { "class": "gsc_1usr_text" })

    profiles = []
    for d in divs:
        profiles.append(parse_google_scholar_profile(d))

    return profiles 


if __name__=="__main__":
    args = interface()
    output = open(args.output_file, 'a') 
    look_for = args.start_after  # Name to start after
    collect = look_for is None   # If name is None, start right away

    c = 0
    for line in open(args.name_file, 'rU'):
        name = line.strip()
        if collect == False:
            if name.startswith(look_for):
                collect = True
            continue  # skip to next record

        time.sleep(2)
        profiles = get_google_scholar_profiles(name) 
        for p in profiles:
            to_write = [name]
            to_write.append(sanitize(p['name']))
            to_write.append(sanitize(p['id']))
            to_write.append(sanitize(p['aff']))
            to_write.append(sanitize(p['tags']))

            # Dump to file
            output.write(','.join(to_write) + '\n')

        print c, name, len(profiles)
        c += 1
        
    output.close()
