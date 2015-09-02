#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import os

home_dir = os.getenv('HOME', None)
if home_dir == '/Users/sawa6416/':
    raise NotImplementedError('Set this up!')
else:
    INST_FILE = '/Users/samway/Documents/Work/ClausetLab/projects/faculty_hiring/data/inst_cs.txt'
    FAC_FILE = '/Users/samway/Documents/Work/ClausetLab/projects/faculty_hiring/data/faculty_cs.txt'

