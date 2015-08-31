#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

"""
Parsing of faculty record files.  
The two main pieces in this module are the `parse_faculty_records()` function
and the `faculty_record` class in which entries are returned.  

Example for a plain-text file containing the entry below.

    >>> from university_network.parse.faculty_parser import parse_faculty_records
    >>> records = parse_faculty_records(open('EXAMPLE.TXT', 'rU'))
    >>> first_record = records.next()  # Note: generator function.
    >>> print first_record.facultyName
        Aaron Clauset
    >>> print first_record.education[0].place
        Haverford College
    >>> print first_record.phd()
        ('University of New Mexico', 2006)

Where "EXAMPLE.TXT" contains:
>>> record 1
# facultyName : Aaron Clauset
# email       : aaron.clauset@colorado.edu
# sex         : M
# department  : Computer Science
# place       : University of Colorado, Boulder
# current     : Assistant Professor
# [Education]
# degree      : BS
# place       : Haverford College
# field       : Physics
# years       : 1997-2001
# [Education]
# degree      : PhD
# place       : University of New Mexico
# field       : Computer Science
# years       : 2002-2006
# [Faculty]
# rank        : PostDoc
# place       : Santa Fe Institute
# years       : 2006-2010
# [Faculty]
# rank        : Assistant Professor
# place       : University of Colorado, Boulder
# years       : 2010-2011
# recordDate  : 7/4/2011
"""

from faculty_hiring.misc.util import Struct

NEW_RECORD_SYMBOL = ">>>"
INDIVIDUAL_FIELDS = ['facultyName', 'email', 'sex', 'department', 
                     'place', 'current', 'recordDate']
EDUCATION_FIELDS = ['degree', 'place', 'field', 'years']
FACULTY_FIELDS = ['rank', 'place', 'years']
EDUCATION_FLAG = '[Education]'
FACULTY_FLAG = '[Faculty]'


def finalize_exp_entry(entry):
    if 'years' in entry:
        start, end = entry['years'].split('-')
        try:
            start_year = int(start)
            entry['start_year'] = start_year
        except:
            entry['start_year'] = None
        try:
            end_year = int(end)
            entry['end_year'] = end_year
        except:
            entry['end_year'] = None

    for key in entry:
        if entry[key] == '.':
            entry[key] = None

    return entry


class faculty_record:
    def __setitem__(self, key, value):
        self.__dict__[key]= value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __init__(self, lines):
        self.education = []
        self.faculty = []

        status = 'ready'
        for line in lines:
            if not line.startswith('# '):
                raise ValueError('File does not appear to be a '
                                 'valid faculty record file!')
            line = line[2:]  # remove the leading pound+space

            if status == 'ready':
                if line == EDUCATION_FLAG:
                    status = 'education'
                    values = [None]*len(EDUCATION_FIELDS)

                elif line == FACULTY_FLAG:
                    status = 'faculty'
                    values = [None]*len(FACULTY_FIELDS)

                else:
                    pieces = line.split(':')
                    key = pieces[0].strip()
                    value = ''.join(pieces[1:]).strip()
                    if key in INDIVIDUAL_FIELDS:
                        setattr(self, key, value)

            elif status == 'education':
                pieces = line.split(':')
                key = pieces[0].strip()
                value = ''.join(pieces[1:]).strip()
                if key not in EDUCATION_FIELDS:
                    raise ValueError('Unexpected education field!')

                i = EDUCATION_FIELDS.index(key)
                values[i] = value 

                if None not in values:
                    entry = dict(zip(EDUCATION_FIELDS, values))
                    entry = finalize_exp_entry(entry)
                    self.education.append(entry)
                    status = 'ready'

            elif status == 'faculty':
                pieces = line.split(':')
                key = pieces[0].strip()
                value = ''.join(pieces[1:]).strip()
                if key not in FACULTY_FIELDS:
                    raise ValueError('Unexpected faculty field!')

                i = FACULTY_FIELDS.index(key)
                values[i] = value 

                if None not in values:
                    entry = dict(zip(FACULTY_FIELDS, values))
                    entry = finalize_exp_entry(entry)
                    self.faculty.append(entry)
                    status = 'ready'


    def phd(self):
        """ Return location + year of PhD """
        for record in self.education:
            if record['degree'] == 'PhD':
                return record['place'], record['end_year']
        return None, None


    def first_job(self):
        """ Return location + year of first non-postdoc job """
        for record in self.faculty:
            if record['rank'] != 'PostDoc':
                return record['place'], record['start_year']
        return None, None

    
    def first_asst_prof(self):
        place, year = None, 3000
        ambig = False

        for record in self.faculty:
            if record['rank'] == 'Assistant Professor':
                if record['start_year'] and record['start_year'] < year:
                    place = record['place']
                    year = record['start_year']
                elif not record['start_year']:
                    ambig = True
    
        if place is not None:
            return place, year
        else:
            #if ambig:
            #    print 'Missing start year!', self['facultyName'], '(%s)' % self['sex']
            return None, None
                    

    def current_job(self, ignore=['PostDoc', 'Emeritus']):
        """ Return location + year of current (non-postdoc) job """
        place = self['place']
        current = self['current']

        if ignore is None:
            ignore = []

        if current in ignore:
            return None, None

        for record in self.faculty:
            if record['place'] == place and record['rank'] == current:
                return record['place'], record['start_year']
        return None, None


    def full_professor(self, titles=['Associate Professor', 'Full Professor']):
        """ Return when & where person got tenure.
            ASSUMES that faculty positions are listed in order, which
            may not be the case for some records """ 
        for record in self.faculty:
            if record['rank'] in titles:
                return record['place'], record['start_year']
        return None, None


    def alma_mater(self):
        """ Return location + year of first degree """
        if self.education:
            return self.education[0]['place'], self.education[0]['end_year']
        return None, None


def parse_faculty_records(fp):
    """ Parse a faculty record file.
        This is a generator function which yields
        one record at a time, as they appear in the 
        file being parsed.

        Inputs:
          + fp - an *open* file pointer containing 
                 faculty records.  
        
        Yields:
          + faculty profile object
    """
    partial_record = False

    for line in fp:
        line = line.strip()
        if not line:  continue  # skip empty lines

        if line.startswith(NEW_RECORD_SYMBOL):
            if partial_record:
                yield faculty_record(temp_buffer)
            temp_buffer = []
            partial_record = True  # new individual
        else:
            temp_buffer.append(line)

    if partial_record:
        yield faculty_record(temp_buffer)


if __name__=="__main__":
    fp = open('/Users/samway/Documents/Work/ClausetLab/faculty_network/data/allFaculty_BS_CS_HS-shortform_txt/allFaculty_CS_n5762_19-Apr-2012-shortform.txt', 'ru')
    for x in parse_faculty_records(fp):
        phd_loc, phd_year = x.phd()
        job_loc, job_year = x.first_job()
        
        if phd_loc is not None and phd_loc != '.' \
           and job_loc is not None and job_loc != '.':
            print '%s -> %s' % (phd_loc, job_loc)
        print x.phd()

