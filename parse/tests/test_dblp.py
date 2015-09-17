#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Unit tests for faculty network loading. """

import faculty_hiring.parse.dblp as gs
from unittest import TestCase, main


class tests(TestCase):
    def setUp(self):
        self.test_file = './dblp/test.html'

    def test_load(self):
        pubs, stats = gs.parse_dblp_page(open(self.test_file).read())
        self.assertEqual(len(pubs), 31)
        self.assertEqual(pubs[0]['title'], 'Detecting Change Points in the Large-Scale Structure of Evolving Networks.')
        self.assertEqual(pubs[0]['pub_type'],'inproceedings')
        

if __name__ == '__main__':
    main()
