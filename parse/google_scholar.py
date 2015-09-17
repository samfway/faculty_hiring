#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


from bs4 import BeautifulSoup


"""
Parsing of Google scholar pages
""" 
def parse_gs_page(html_string):
    stats = {}
    publications = []

    soup = BeautifulSoup(html_string, "html.parser")
    pub_listings = soup.findAll('tr', {'class':'gsc_a_tr'})
    
    for pub in pub_listings:
        temp = {}
        temp['title'] = pub.find('a', {'class':'gsc_a_at'}).text
        divs = pub.findAll('div', {'class':'gs_gray'})
        temp['authors'] = divs[0].text
        temp['notes'] = divs[1].text
        temp['year'] = int(pub.find('td', {'class':'gsc_a_y'}).text)
        temp['cited'] = pub.find('a', {'class':'gsc_a_ac'}).text
        publications.append(temp)
    
    stats_table = soup.find('table', {'id':'gsc_rsb_st'})
    stats_trs = stats_table.findAll('tr')
    if len(stats_trs) == 4:
        stats['citations'] = int(stats_trs[1].find('td', {'class':'gsc_rsb_std'}).text)
        stats['h-index'] = int(stats_trs[2].find('td', {'class':'gsc_rsb_std'}).text)
        stats['i10-index'] = int(stats_trs[3].find('td', {'class':'gsc_rsb_std'}).text)

    return publications, stats  

