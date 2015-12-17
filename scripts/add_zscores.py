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
from faculty_hiring.parse import faculty_parser, institution_parser
from faculty_hiring.parse import load


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--inst-file', help='Institution profiles')
    args.add_argument('-f', '--faculty-file', help='Faculty profiles')
    args.add_argument('-o', '--output-file', help='Output faculty profiles')
    args.add_argument('-d', '--dblp-dir', help='DBLP dir')
    args = args.parse_args()
    return args


def get_paper_counts_by_topic(faculty, max_papers=200):
    """ Get weighted distributions for paper counts""" 
    # How many topics are there?
    for f in faculty:
        if 'dblp_pubs' in f:
            num_topics = len(f['topic_dist'])
            break 

    dists = np.zeros((num_topics, max_papers), dtype=float)
    tots = np.zeros(num_topics, dtype=float)

    for f in faculty:
        if 'dblp_pubs' in f:
            paper_count = 0
            paper_count_2011 = 0
            for paper in f['dblp_pubs']:
                if 'year' in paper and paper['year'] <= f.first_asst_job_year + 1:
                    paper_count += 1
                elif 'year' in paper and paper['year'] == 2011:
                    paper_count_2011 += 1

            f.first_asst_job_papers = paper_count
            f.papers_in_2011 = paper_count_2011
            dists[:,paper_count] += f['topic_dist']
            tots += f['topic_dist']
        else:
            f.papers_in_2011 = 0
            f.first_asst_job_papers = 0

    return dists, tots


def get_topic_means_stds(dists, tots):
    """ Get weighted means and standard deviations 
        for computing z-scores """ 
    num_topics = len(tots)
    means = np.zeros(num_topics, dtype=float)
    stds = np.zeros(num_topics, dtype=float)
    vals = np.arange(dists.shape[1])
    
    for i in xrange(num_topics):
        p = dists[i,:] / tots[i]
        means[i] = np.average(vals, weights=p)
        stds[i] = np.sqrt(np.average((vals-means[i])**2, weights=p))

    return means, stds


def set_zscores(faculty, means, stds):
    # Get the number of topics
    for f in faculty:
        if 'topic_dist' in f:
            num_topics = len(f['topic_dist'])
            default_topic_dist = np.zeros(num_topics, dtype=float)
            break

    # Get the average topic vector
    for f in faculty:
        if 'topic_dist' in f:
            default_topic_dist += f['topic_dist']
    default_topic_dist /= default_topic_dist.sum()

    for f in faculty:
        if 'dblp_pubs' in f:
            z = (f.first_asst_job_papers - means) / stds
            f.dblp_z = np.dot(z, f['topic_dist'])
        else:
            z = (0. - means) / stds
            f.dblp_z = np.dot(z, default_topic_dist)
        '''
        if f.facultyName == 'Aaron Clauset':
            print f.first_asst_job_papers - means
            #print means
            print stds
            #print f.dblp_z
            print z
            exit()
        ''' 


def add_zscores_to_file(faculty, in_file, out_file):
    """ Add scores to faculty file """ 
    names = []
    zscores = []
    for f in faculty:
        if 'dblp_z' in f:
            names.append(f.facultyName)
            num_papers.append(f.first_asst_job_papers)
            zscores.append(f.dblp_z)
    
    next_ind = 0
    next_name = names[next_ind]
    max_ind = len(names)
    done = False

    output = open(out_file, 'w')
    for line in open(in_file, 'rU'):
        output.write(line)  # Copy all lines
        if not done and line.startswith('# facultyName '): 
            name = line.split(':', 1)[-1].strip()
            if name == next_name:
                output.write('# dblp_n      : %d\n' % num_papers[next_ind])
                #output.write('# dblp_z      : %f\n' % zscores[next_ind])
                next_ind += 1
                if next_ind < max_ind:
                    next_name = names[next_ind]
                else:
                    done = True

    if not done:
        print 'WARNING: failed to link all z-scores!'

    output.close()
        

def add_counts_to_file(faculty, in_file, out_file):
    """ Add scores to faculty file """ 
    names = []
    zscores = []
    num_papers = []
    num_papers_2011 = []

    for f in faculty:
        if 'dblp_z' in f:
            names.append(f.facultyName)
            num_papers.append(f.first_asst_job_papers)
            num_papers_2011.append(f.papers_in_2011)
            zscores.append(f.dblp_z)
    print np.mean(num_papers)
    
    next_ind = 0
    next_name = names[next_ind]
    max_ind = len(names)
    done = False

    output = open(out_file, 'w')
    for line in open(in_file, 'rU'):
        output.write(line)  # Copy all lines
        if not done and line.startswith('# facultyName '): 
            name = line.split(':', 1)[-1].strip()
            if name == next_name:
                output.write('# dblp_n      : %d\n' % num_papers[next_ind])
                output.write('# dblp_n_2011 : %d\n' % num_papers_2011[next_ind])
                next_ind += 1
                if next_ind < max_ind:
                    next_name = names[next_ind]
                else:
                    done = True

    if not done:
        print 'WARNING: failed to link all z-scores!'

    output.close()
        

if __name__=="__main__":
    args = interface()
    
    inst = institution_parser.parse_institution_records(open(args.inst_file))
    faculty = load_assistant_profs(open(args.faculty_file, 'rU'), inst)
    load.load_all_publications(faculty, args.dblp_dir, gs_dir=None)
    dists, tots = get_paper_counts_by_topic(faculty)
    means, stds = get_topic_means_stds(dists, tots)
    print means
    print stds
    set_zscores(faculty, means, stds)
    #add_zscores_to_file(faculty, args.faculty_file, args.output_file)
    add_counts_to_file(faculty, args.faculty_file, args.output_file)

