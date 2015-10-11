#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import numpy as np


def parse_phds_awarded(table_file):
    """ Returns graduation year, number of females, number total at doctoral level """
    PHD_WOMEN_INDEX = 11
    PHD_TOTAL_INDEX = 9
    YEAR_INDEX = 0

    years = []
    women = []
    total = []

    for line in open(table_file, 'rU'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        pieces = line.split('\t')
        if len(pieces) != 12:
            print line
            print pieces
            raise ValueError('Something went wrong!')
        
        year = int(pieces[YEAR_INDEX].split('-')[0])+1
        num_w = int(pieces[PHD_WOMEN_INDEX].replace(',', ''))
        num_t = int(pieces[PHD_TOTAL_INDEX].replace(',', ''))

        years.append(year)
        women.append(num_w)
        total.append(num_t)
    
    return np.array(years), np.array(women), np.array(total)
        
    
