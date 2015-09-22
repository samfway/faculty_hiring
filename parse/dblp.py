#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import os
from bs4 import BeautifulSoup


DBLP_FILE = 'DBLP_%s_file_0.html'


"""
Parsing of DBLP profile pages
""" 
def parse_dblp_page(html_string):
    stats = {}
    publications = []

    soup = BeautifulSoup(html_string, "html.parser")
    uls = soup.findAll('ul', {'class':'publ-list'})

    for ul in uls:
        lis = ul.findAll('li')
        year = -1
        for li in lis:
            try:  # See if it's a year line
                year = int(li.text)
                continue
            except:
                pass
            if 'class' in li.attrs:
                if li.attrs['class'][0] == 'entry':
                    nav = li.findAll('nav', {'class':'publ'})[0]
                    head = nav.find('div', {'class':'head'})
                    link = head.find('a')
                    if link:
                        link = link['href']
                    else:
                        link = None

                    pub_type = li.attrs['class'][1]
                    authors = [a.text for a in li.findAll('span', {'itemprop':'author'})]
                    title = li.find('span', {'class':'title'}).text

                    pub = dict(zip(['title', 'authors', 'link', 'pub_type', 'year'], 
                                   [title, authors, link, pub_type, year]))
                    publications.append(pub)

    return publications, stats


def parse_dblp_publications(faculty, dblp_dir):
    """ Load all publications into the faculty record """ 
    for f in faculty:
        print f['facultyName']
        if 'dblp' in f:
            filename = os.path.join(dblp_dir, DBLP_FILE % f['dblp'])
            if os.path.isfile(filename):
                pubs, stats = parse_dblp_page(open(filename, 'rU').read())
                f['dblp_pubs'] = pubs
                f['dblp_stats'] = stats
            else:
                print 'DBLP file missing for "%s"!' % f['facultyName']
            
