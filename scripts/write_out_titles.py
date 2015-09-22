#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import re
import os
import argparse
from collections import Counter
from faculty_hiring.parse import faculty_parser, institution_parser
from faculty_hiring.parse import load
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-o', '--output-dir', help='Output directory')
    args.add_argument('-i', '--input-file', help='Input file')
    args.add_argument('-d', '--dblp-dir', help='DBLP directory')
    args.add_argument('-g', '--gs-dir', help='GS directory')
    args.add_argument('-s', '--custom_stops', help='Custom stop words')
    args = args.parse_args()
    return args


def sanitize(input_string):
    """ Remove all unicode characters """
    filtered = filter(lambda x: x in string.printable, input_string)
    filtered = filtered.replace(',', ';')
    return filtered 


def word_filter(word, stop_list, lemmer):
    if 'cid:' in word or word.startswith("\\x") or word.startswith("arx"):
        return None
    w = lemmer.lemmatize(re.sub(r'[^a-zA-Z]+', '', word).lower())
    if w in stop_list:
        return None
    if len(w) < 3:
        return None
    return w


def add_words_from_title(words, title, stop_words, lem):
    for word in title.split():
        w = word_filter(word, stop_words, lem)
        if w:
            words.append(w)


if __name__=="__main__":
    args = interface()
    
    faculty = load.load_assistant_profs(open(args.input_file))
    load.load_all_publications(faculty, args.dblp_dir, args.gs_dir)

    lem = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    if args.custom_stops:
        custom_words = [word_filter(w.strip(), [], lem) for w in open(args.custom_stops, 'rU')]
        stop_words += custom_words

    for f in faculty:
        tag = None
        words = []
    
        if 'dblp_pubs' in f:
            tag = f['dblp']
            for pub in f['dblp_pubs']:
                add_words_from_title(words, pub['title'], stop_words, lem)
            
        if 'gs_pubs' in f:
            tag = f['gs']
            if len(f['gs_pubs']) > 1500:
                print 'Skipping %s...' % f['facultyName']
                continue 
            for pub in f['gs_pubs']:
                add_words_from_title(words, pub['title'], stop_words, lem)
            
        output = open(os.path.join(args.output_dir, '%s.txt' % tag), 'w')
        output.write(' '.join(words))
        output.close()
        print f['facultyName']
    
