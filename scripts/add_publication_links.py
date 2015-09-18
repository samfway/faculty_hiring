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


GS_FIELD_NAME = 0
GS_FIELD_ID = 2
DBLP_FIELD_NAME = 0
DBLP_FIELD_ID = 1


def interface():
    args = argparse.ArgumentParser()
    args.add_argument('-o', '--output-file', help='Output file')
    args.add_argument('-i', '--faculty-file', help='Faculty profiles')
    args.add_argument('-g', '--gs-file', help='(cleaned) Google scholar profile list')
    args.add_argument('-d', '--dblp-file', help='(cleaned) DBLP profile list')
    args = args.parse_args()
    return args


def sanitize(input_string):
    """ Remove all unicode characters """
    filtered = filter(lambda x: x in string.printable, input_string)
    filtered = filtered.replace(',', ';')
    return filtered 


def link_gs_profiles(faculty, gs_file):
    f_max = len(faculty)
    f_current = 0
    linked = 0

    for line in open(gs_file):
        pieces = line.strip().split(',')
        name = pieces[GS_FIELD_NAME]
        gsid = pieces[GS_FIELD_ID]
        
        # Look for a reasonable amount of time then give up
        for f in xrange(f_current, min(f_current+50, f_max)):
            f_name = faculty[f]['facultyName']
            san_f_name = sanitize(f_name)
            if name == f_name or name == san_f_name:
                if 'gs' in faculty[f]:
                    raise ValueError('Something went wrong...')
                faculty[f]['gs'] = gsid
                linked += 1
                f_current = f
                break

    print 'Linked %d Google Scholar profiles.' % linked


def link_dblp_profiles(faculty, dblp_file):
    f_max = len(faculty)
    f_current = 0
    linked = 0
    
    for line in open(dblp_file):
        pieces = line.strip().split(',')
        name = pieces[DBLP_FIELD_NAME]
        
        for f in xrange(f_current, f_max):
            f_name = faculty[f]['facultyName']
            san_f_name = sanitize(f_name)
            if name == f_name or name == san_f_name:
                dblp_url = pieces[DBLP_FIELD_ID]
                author_tag = re.findall(r'(?<=pers/hd/./)[^,]+', dblp_url)[0]
                if 'dblp' in faculty[f]:
                    print name
                faculty[f]['dblp'] = author_tag
                linked += 1
                f_current = f
                break

    print 'Linked %d DBLP profiles.' % linked


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
            else:  # not a name-line, leave it alone
                output.write(line)
            line = in_fp.readline()

    # Finish writing the last record(s)
    if line:  # Didn't reach the end yet, so grab the next line
        line = in_fp.readline()
        while line:
            output.write(line)
            line = in_fp.readline()
                
    print 'Linked %d DBLP profiles and %d GS profiles in new output file' % (dblp_linked, gs_linked)
    output.close()


if __name__=="__main__":
    args = interface()
    
    faculty = load_assistant_profs(open(args.faculty_file, 'rU'))
    link_gs_profiles(faculty, args.gs_file)
    link_dblp_profiles(faculty, args.dblp_file)
    add_links_to_file(faculty, args.faculty_file, args.output_file)
    
    covered = 0
    both = 0
    for f in faculty:
        if 'gs' in f or 'dblp' in f:
            covered += 1
        else:
            print f['facultyName']
        if 'gs' in f and 'dblp' in f:
            both += 1
    print '%d of %d have at least one of the two profiles.' % (covered, len(faculty))
    print '%d of %d have both profiles.' % (both, len(faculty))
            
    
