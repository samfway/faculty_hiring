#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Unit tests for faculty network loading. """

import faculty_hiring.parse.google_scholar as gs
from unittest import TestCase, main


class tests(TestCase):
    def setUp(self):
        self.test_file = './gs/test.html'

    def test_load(self):
        pubs, stats = gs.parse_gs_page(open(self.test_file).read())
        self.assertEqual(stats['citations'], 7780)
        self.assertEqual(stats['h-index'], 37)
        self.assertEqual(stats['i10-index'], 77)
        self.assertEqual(len(pubs), 100)
        self.assertEqual(pubs[0]['title'], 'Method and system for searching for information on a network in response to an image query sent by a user from a mobile communications device')
        self.assertEqual(pubs[0]['authors'], 'GD Ramkumar, R Manmatha, S Bhattacharyya, G Bhargava, MA Ruzon')
        self.assertEqual(pubs[0]['year'], 2015)
        

if __name__ == '__main__':
    main()
