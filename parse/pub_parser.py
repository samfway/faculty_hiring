#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

"""
         Title Role-based authorization constraints specification
           URL http://dl.acm.org/citation.cfm?id=382913
          Year 2000
     Citations 510
      Versions 13
    Cluster ID 1613924578938524769
Citations list http://scholar.google.com/scholar?cites=1613924578938524769&as_sdt=2005&sciodt=1,5&hl=en
 Versions list http://scholar.google.com/scholar?cluster=1613924578938524769&hl=en&as_sdt=1,5&as_yhi=2001&as_vis=1
   Author line GJ Ahn,R Sandhu- ACM Transactions on Information and System  &hellip;, 2000 - dl.acm.org

         Title Role-based access control on the web
           URL http://dl.acm.org/citation.cfm?id=383777
          Year 2001
     Citations 321
      Versions 13
    Cluster ID 16259048495598541056
Citations list http://scholar.google.com/scholar?cites=16259048495598541056&as_sdt=2005&sciodt=1,5&hl=en
 Versions list http://scholar.google.com/scholar?cluster=16259048495598541056&hl=en&as_sdt=1,5&as_yhi=2001&as_vis=1
   Author line JS Park,R Sandhu,GJ Ahn- ACM Transactions on Information and  &hellip;, 2001 - dl.acm.org
"""

from faculty_hiring.misc.util import Struct
from os.path import join as path_join

FIELDS = ['Title', 'URL', 'Year', 'Citations', 'Versions', 'Cluster ID', 'Citations list', 'Versions list', 'Author line']
F_TYPE = [str,     str,   int,     int,         int,        int,          str,             str,              str]
FIRST_FIELD = 0  # Which field appears first?
START = FIELDS[FIRST_FIELD]
START_TYPE = F_TYPE[FIRST_FIELD]

def parse_pub_file(pub_file):
    """ Extract Google scholar records from a plaintext file.
        Expected format for publication data is shown in parse_pub_records documentation. 
    """
    current_record = None
    records = []

    for line in open(pub_file, 'rU'):
        line = line.strip()
        if not line: continue 

        if line.startswith(START):
            if current_record:
                records.append(current_record)
            current_record = dict.fromkeys(FIELDS)
            current_record[START] = START_TYPE(line[len(START):].strip())
            next_f = 1
        elif current_record:
            f = FIELDS[next_f]
            f_type = F_TYPE[next_f]

            if line.startswith(f):
                current_record[f] = f_type(line[len(f):].strip())
                next_f = (next_f + 1) % len(FIELDS)

    if current_record:
        records.append(current_record)

    return records


def parse_pub_records(fac_list_file, pub_dir):
    """ Parse all publication results.
        
        Input files
          - fac_list_fp: file of faculty names used to create directory 
                         of publication files. Expected format is 
                         <name>|<university>|<year_hired>

          - pub_dir: directory containing all publication data from Google Scholar.
                     Expected format is:
                                     Title Role-based access control on the web
                                       URL http://dl.acm.org/citation.cfm?id=383777
                                      Year 2001
                                 Citations 321
                                  Versions 13
                                Cluster ID 16259048495598541056
                            Citations list http://scholar.google.com/scholar?c...
                             Versions list http://scholar.google.com/scholar?c...
                               Author line JS Park,R Sandhu,GJ Ahn- ACM Transa...
    """
    faculty_number = 0
    faculty_publications = {}

    for line in open(fac_list_file, 'rU'):
        line = line.strip()
        if not line: continue 

        name = line.split('|')[0]
        pub_file = path_join(pub_dir, '%d.txt' % faculty_number)
        faculty_number += 1
        faculty_publications[name] = parse_pub_file(pub_file)
    
    return faculty_publications
        
