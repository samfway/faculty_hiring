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


DBLP_URL = 'http://dblp.uni-trier.de/search?q=%s'


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


def get_dblp_profiles(name):
    """ Plug the faculty name into DBLP and 
        see if there are any (maybe several) user ids.
        Save them all to the output file. 
        
        You'll have to go through by hand (yuck) to 
        determine who the real ones are! 

        Returns a list of Google Scholar ids, which
        is empty if there are none! """
    formatted_name = '+'.join(name.split())
    query_url = DBLP_URL % formatted_name
    results_page = urllib2.urlopen(query_url).read()
    soup = BeautifulSoup(results_page, "html.parser")
    person_items = soup.findAll("li", { "itemtype": "http://schema.org/Person" })

    profiles = []
    for p in person_items:
        link = p.find('a')['href']
        person_notes = p.find('small')
        if person_notes:
            line = ','.join([link, sanitize(person_notes.text)])
        else:
            line = link + ','
        profiles.append(line)

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
        profiles = get_dblp_profiles(name) 
        for p in profiles:
            to_write = [sanitize(name)]
            to_write.append(p)

            # Dump to file
            output.write(','.join(to_write) + '\n')

        print c, name, len(profiles)
        c += 1
        
    output.close()
