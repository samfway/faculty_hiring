#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Unit tests for faculty network parsing. """

from faculty_hiring.parse.faculty_parser import parse_faculty_records
from faculty_hiring.parse.institution_parser import parse_institution_records
from faculty_hiring.parse.pub_parser import parse_pub_records
from StringIO import StringIO
from unittest import TestCase, main

def get_test_records():
    return StringIO(
"""
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
# place       : MIT
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
# years       : ????-????
# [Faculty]
# rank        : Full Professor
# place       : Texas A&M
# years       : 1996-2008
# [Faculty]
# rank        : Emeritus
# place       : Texas A&M
# years       : 2008-2011
# recordDate  : 10/6/2011""")


def get_test_universities():
    return StringIO(
"""
# u\tpi\tUSN2010\tNRC95\tRegion\tinstitution
1\t2.23\t1\t1\tWest\tStanford University
2\t2.31\t1\t3\tWest\tUC Berkeley
3\t3.52\t1\t2\tNortheast\tMIT
4\t5.24\t11\t12\tWest\tCalifornia Institute of Technology
5\t6.12\t17\t11\tNortheast\tHarvard University
6\t8.29\t5\t5\tNortheast\tCornell University
7\t9.28\t1\t4\tNortheast\tCarnegie Mellon University
8\t9.32\t8\t6\tNortheast\tPrinceton University
9\t9.98\t20\t14\tNortheast\tYale University""")


class parsing_tests(TestCase):
    """ Test parsing of faculty networks. """
    def setUp(self):
       pass 

    def test_parse(self):
        X = get_test_records()
        records = parse_faculty_records(X)

        first_record = records.next()
        self.assertEqual(first_record.facultyName, 'Joe Shmoe')
        self.assertEqual(first_record.email, 'js@asu.edu')
        self.assertEqual(first_record.sex, 'M')
        self.assertEqual(first_record.department, 'Information and Computer Science')
        self.assertEqual(first_record.place, 'Arizona State University')
        self.assertEqual(first_record.current, 'Associate Professor')
        self.assertEqual(first_record.education[0]['degree'], 'BS')
        self.assertEqual(first_record.education[0]['place'], 'Stanford University')
        self.assertEqual(first_record.education[0]['field'], 'Computer Science')
        self.assertEqual(first_record.education[0]['years'], '????-1994')
        self.assertEqual(first_record.education[0]['start_year'], None)
        self.assertEqual(first_record.education[0]['end_year'], 1994)
        self.assertEqual(len(first_record.education), 2)
        self.assertEqual(len(first_record.faculty), 2)
        self.assertEqual(first_record.faculty[1]['rank'], 'Assistant Professor')
        self.assertEqual(first_record.faculty[1]['place'], 'MIT')
        self.assertEqual(first_record.faculty[1]['years'], '2000-2005')
        self.assertEqual(first_record.faculty[1]['start_year'], 2000) 
        self.assertEqual(first_record.faculty[1]['end_year'], 2005) 
        self.assertEqual(first_record['recordDate'], '9/29/2011')

        second_record = records.next()
        self.assertEqual(len(second_record.education), 1) 
        self.assertEqual(len(second_record.faculty), 2) 
        self.assertEqual(second_record.education[0]['place'], 'University of New Mexico') 
        self.assertEqual(second_record.faculty[1]['rank'], 'Emeritus') 

    def test_uni_parse(self):
        X = get_test_universities()
        institutions = parse_institution_records(X)
        self.assertEqual(institutions['Yale University']['Region'], 'Northeast')
        self.assertEqual(institutions['Princeton University']['NRC95'], 6)
        self.assertEqual(institutions['Carnegie Mellon University']['USN2010'], 1)
        self.assertEqual(institutions['Harvard University']['pi'], 6.12)
        self.assertEqual(institutions['Harvard University']['pi_inv'], 1./6.12)
        self.assertEqual(institutions['Stanford University']['pi_rescaled'], 1.)
        self.assertEqual(institutions['MIT']['u'], 3)

    def test_pub_parse(self):
        records = parse_pub_records('./pub_test/faclist.txt', './pub_test/')
        self.assertEqual(records['Per Son'][0]['Title'], 'TESTING_TITLE0')
        self.assertEqual(records['Per Son'][1]['Title'], 'TESTING_TITLE1')
        self.assertEqual(records['Per Son'][1]['Citations'], 321)
        self.assertEqual(len(records['A.A. Ron']), 0)
    

if __name__ == '__main__':
    main()
