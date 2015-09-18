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
from faculty_hiring.parse.load import load_assistant_profs


NAME_FIELD = 0
GS_FIELD = 2
DBLP_FIELD = 3


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-o', '--output-file', help='Output file')
    args.add_argument('-i', '--faculty-file', help='Faculty profiles')
    args.add_argument('-b', '--by-hand-file', help='GS/DBLP profiles obtained by hand')
    args = args.parse_args()
    return args


def sanitize(input_string):
    """ Remove all unicode characters """
    filtered = filter(lambda x: x in string.printable, input_string)
    filtered = filtered.replace(',', ';')
    return filtered 


def link_by_hand_profiles(faculty, by_hand_file):
    f_max = len(faculty)
    f_current = 0
    linked = 0
    
    for line in open(by_hand_file):
        pieces = line.strip().split(',')
        name = pieces[NAME_FIELD]
        
        for f in xrange(f_current, f_max):
            f_name = faculty[f]['facultyName']
            san_f_name = sanitize(f_name)
            if name == f_name or name == san_f_name:
                if pieces[GS_FIELD]:
                    faculty[f]['gs'] = pieces[GS_FIELD]

                if pieces[DBLP_FIELD]:
                    author_tag = re.findall(r'(?<=pers/hd/./)[^,]+', pieces[DBLP_FIELD])[0]
                    faculty[f]['dblp'] = author_tag
                linked += 1
                f_current = f
                break

    print 'Linked %d by-hand profiles.' % linked


def add_links_to_file(faculty, faculty_file, output_file):
    gs_linked = 0
    dblp_linked = 0
    output = open(output_file, 'w')
    in_fp = open(faculty_file, 'rU')

    for f in faculty:
        if 'gs' not in f and 'dblp' not in f:
            continue  # ok to skip this person
        name = f['facultyName']
        
        line = in_fp.readline()
        while line:
            # look for the person with f's name and add the pub profiles
            if line.startswith('# facultyName'):
                found_name = line.split(':')[1].strip()
                if found_name == name:  # if the name you found matches the one you're looking for.. 
                    output.write(line)
                    if 'dblp' in f:
                        output.write('# dblp        : %s\n' % f['dblp'])
                        dblp_linked += 1
                    if 'gs' in f:
                        output.write('# gs          : %s\n' % f['gs'])
                        gs_linked += 1
                    break
                else:  # otherwise leave it alone
                    output.write(line)
            elif line.startswith('# gs') or line.startswith('# dblp'):
                pass  # don't duplicate these lines!
            else:  # not a name-line, leave it alone
                output.write(line)
            line = in_fp.readline()

    # Finish writing the last record(s)
    if line:  # Didn't reach the end yet, so grab the next line
        line = in_fp.readline()
        while line:
            output.write(line)
            line = in_fp.readline()
                
    output.close()


if __name__=="__main__":
    args = interface()
    
    faculty = load_assistant_profs(open(args.faculty_file, 'rU'))
    link_by_hand_profiles(faculty, args.by_hand_file)
    add_links_to_file(faculty, args.faculty_file, args.output_file)
    
    covered = 0
    both = 0
    for f in faculty:
        if 'gs' in f or 'dblp' in f:
            covered += 1
        #else:
        #    print f['facultyName']
        if 'gs' in f and 'dblp' in f:
            both += 1
    print '%d of %d have at least one of the two profiles.' % (covered, len(faculty))
    print '%d of %d have both profiles.' % (both, len(faculty))
            
    
