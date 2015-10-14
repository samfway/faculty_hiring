#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"


import argparse
import string
import re
import os
import numpy as np
from faculty_hiring.parse.load import load_assistant_profs
from faculty_hiring.parse import institution_parser


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-o', '--output-file', help='Output faculty file')
    args.add_argument('-f', '--faculty-file', help='Faculty profiles')
    args.add_argument('-i', '--inst-file', help='Institution profiles')
    args.add_argument('-d', '--doc-topics-file', help='Doc-topics from MALLET')
    args = args.parse_args()
    return args


def parse_doc_topics_file(doc_topics_file):
    """ Parse doc-topics file from MALLET.
        Returns a dictionary, indexed by the author publication key (GS/DBLP).
            Dictionary values are numpy arrays denoting topic distributions.
    """
    doc_topics_dict = {}
    num_topics = 0
    
    for line in open(doc_topics_file, 'rU'):
        if line.startswith('#'):
            continue  # Skip comments
        
        pieces = line.strip().split()
        # index, filename, then key-value pairs. Just want num keys
        num_keys = (len(pieces)-2)/2
        num_pieces = len(pieces)
        if not num_topics:
            num_topics = num_keys
        elif num_topics != num_keys:
            raise ValueError('Inconsistent number of key-value pairs!')

        filename = pieces[1]
        author_tag = os.path.basename(filename).replace('.txt', '')
        topic_dist = np.zeros(num_topics)
        
        for i in xrange(2, num_pieces, 2):
            topic_dist[int(pieces[i])] = float(pieces[i+1])

        doc_topics_dict[author_tag] = topic_dist
            
    return doc_topics_dict


def link_doc_topics(faculty, doc_topics_dict, just_dblp=True):
    for f in faculty:
        pub_tag = None
        
        if 'dblp' in f:
            pub_tag = f['dblp']

        if not just_dblp and 'gs' in f:
            pub_tag = f['gs']

        if pub_tag in doc_topics_dict:
            f['topic_dist'] = doc_topics_dict[pub_tag]


def add_doc_topics_to_file(doc_topics_dict, input_file, output_file):
    output = open(output_file, 'w')
    for line in open(input_file, 'rU'):
        written = False
        if line.startswith('# dblp ') or line.startswith('# gs '):
            tag = line.split(':', 1)[1].strip()
            if tag in doc_topics_dict:
                output.write(line)
                output.write('# topic_dist  : %s\n' % ','.join([str(x) for x in doc_topics_dict[tag]]))
                written = True
        if not written:
            output.write(line)
    output.close()


if __name__=="__main__":
    args = interface()
    
    inst = institution_parser.parse_institution_records(open(args.inst_file))
    faculty = load_assistant_profs(open(args.faculty_file, 'rU'), inst)

    doc_topics_dict = parse_doc_topics_file(args.doc_topics_file)
    link_doc_topics(faculty, doc_topics_dict)
    add_doc_topics_to_file(doc_topics_dict, args.faculty_file, args.output_file)

