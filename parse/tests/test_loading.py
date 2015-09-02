#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Unit tests for faculty network loading. """

from faculty_hiring.parse.faculty_parser import parse_faculty_records
from faculty_hiring.parse.load import load_hires_by_year
from StringIO import StringIO
from unittest import TestCase, main
import numpy as np


def get_test_records():
    return StringIO("""
>>> record 1
# facultyName : Joe Shmoe
# email       : js@asu.edu
# sex         : M
# department  : Information and Computer Science
# place       : Arizona State University
# current     : Associate Professor
# [Education]
# degree      : BS
# place       : Stanford University
# field       : Computer Science
# years       : ????-1994
# [Education]
# degree      : PhD
# place       : Stanford University
# field       : Information Technology
# years       : ????-2000
# [Faculty]
# rank        : PostDoc
# place       : Arizona State University
# years       : 2000-2000
# [Faculty]
# rank        : Assistant Professor
# place       : University of Arizona
# years       : 2000-2005
# recordDate  : 9/29/2011

>>> record 2
# facultyName : Bob Roberts
# email       : br@cse.tamu.edu
# sex         : M
# department  : Computer Science
# place       : Texas A&M
# current     : Emeritus
# [Education]
# degree      : PhD
# place       : University of New Mexico
# field       : Computer and Information Sciences
# years       : ????-1989
# [Faculty]
# rank        : Assistant Professor
# place       : MIT
# years       : 1990-1996
# [Faculty]
# rank        : Full Professor
# place       : Texas A&M
# years       : 1996-2008
# [Faculty]
# rank        : Emeritus
# place       : Texas A&M
# years       : 2008-2011
# recordDate  : 10/6/2011

>>> record 2
# facultyName : Bob McRoberts
# email       : br@cse.tamu.edu
# sex         : M
# department  : Computer Science
# place       : Texas A&M
# current     : Something
# [Education]
# degree      : PhD
# place       : University of New Mexico
# field       : Computer and Information Sciences
# years       : ????-1989
# [Faculty]
# rank        : Assistant Professor
# place       : University of Wisconsin
# years       : 1988-1996
# [Faculty]
# rank        : Full Professor
# place       : Texas A&M
# years       : 1996-2008
# [Faculty]
# rank        : Emeritus
# place       : Texas A&M
# years       : 2008-2011
# recordDate  : 10/6/2011


>>> record 3
# facultyName : NoStart Date
# email       : hnnnn@ng.com
# sex         : M
# department  : Computer Science
# place       : University of New Mexico
# current     : Emeritus
# [Education]
# degree      : PhD
# place       : University of New Mexico
# field       : Computer and Information Sciences
# years       : ????-????
# [Faculty]
# rank        : Assistant Professor
# place       : MIT
# years       : ????-1996
# [Faculty]
# rank        : Full Professor
# place       : Texas A&M
# years       : 1996-2008
# [Faculty]
# rank        : Emeritus
# place       : Texas A&M
# years       : 2008-2011
# recordDate  : 10/6/2011""")


class tests(TestCase):
    def setUp(self):
       pass 

    def test_load(self):
        fac_fp = get_test_records()
        candidates, jobs, years = load_hires_by_year(fac_fp)
        self.assertEqual(jobs[np.where(years == 1990)[0]][0], 'MIT')
        self.assertEqual(candidates[np.where(years == 2000)[0]][0]['facultyName'], 'Joe Shmoe')

    def test_load_steps(self):
        fac_fp = get_test_records()
        candidates, jobs, years = load_hires_by_year(fac_fp, year_step=10)
        self.assertEqual(jobs[np.where(years == 1980)[0]][0], 'University of Wisconsin')

if __name__ == '__main__':
    main()
