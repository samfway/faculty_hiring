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
import numpy as np

NEW_RECORD_SYMBOL = ">>>"
INDIVIDUAL_FIELDS = ['facultyName', 'email', 'sex', 'department', 
                     'place', 'current', 'recordDate', 'gs', 'dblp', 'topic_dist', 'dblp_z']
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

    def __contains__(self, key):
        return key in self.__dict__

    def __init__(self, lines, school_info=None, ranking='pi_rescaled'):
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
                    key, value = [p.strip() for p in line.split(':',1)]
                    if key in INDIVIDUAL_FIELDS:
                        setattr(self, key, value)
                    if key == 'topic_dist':
                        topic_dist = np.array([float(x) for x in value.split(',')])
                        setattr(self, key, topic_dist)
                    if key == 'dblp_z':
                        setattr(self, key, float(value))

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

        # Set PhD info
        self.phd_location = None
        self.phd_year = None
        for record in self.education:
            if record['degree'] == 'PhD':
                self.phd_location = record['place']
                self.phd_year = record['end_year']

        # Set first job info - ASSUMES ORDERED RECORDS
        self.first_job_location = None
        self.first_job_year = None
        for record in self.faculty:
            if record['rank'] != 'PostDoc':
                self.first_job_location = record['place']
                self.first_job_year = record['end_year']
                break 

        # Set Assistant Professor info
        self.first_asst_job_location = None
        self.first_asst_job_year = None
        year = np.inf
        self.num_asst_jobs = 0     # Number of assistant jobs
        self.num_asst_jobs_kd = 0  # With a known date
        for record in self.faculty:
            if record['rank'] == 'Assistant Professor':
                self.num_asst_jobs += 1
                if record['start_year']:
                    self.num_asst_jobs_kd += 1
                    if record['start_year'] < year:
                        self.first_asst_job_location = record['place']
                        self.first_asst_job_year = record['start_year']

        # Do they have a post-doc? 
        self.has_postdoc = False
        for record in self.faculty:
            if record['rank'] == 'PostDoc':
                self.has_postdoc = True

        # Are they female? 
        self.is_female = self['sex'] == 'F'

        # Set ranking/geography info, if supplied
        if school_info is not None:
            if self.phd_location in school_info:
                self.phd_rank = school_info[self.phd_location][ranking]
                self.phd_region = school_info[self.phd_location]['Region']
            else:
                self.phd_rank = school_info['UNKNOWN'][ranking]
                self.phd_region = school_info['UNKNOWN']['Region']

            if self.first_asst_job_location in school_info:
                self.first_asst_job_rank = school_info[self.first_asst_job_location][ranking]
                self.first_asst_job_region = school_info[self.first_asst_job_location]['Region']
            else:
                self.first_asst_job_rank = school_info['UNKNOWN'][ranking]
                self.first_asst_job_region = school_info['UNKNOWN']['Region']
        

    def phd(self):
        """ Return location + year of PhD """
        return self.phd_location, self.phd_year


    def first_job(self):
        """ Return location + year of first non-postdoc job """
        return self.first_job_location, self.first_job_year

    
    def first_asst_prof(self):
        """ Return location + year of earliest assistant professorship """ 
        return self.first_asst_job_location, self.first_asst_job_year 
                    

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


def parse_faculty_records(fp, school_info=None, ranking='pi_rescaled'):
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
                yield faculty_record(temp_buffer, school_info, ranking)
            temp_buffer = []
            partial_record = True  # new individual
        else:
            temp_buffer.append(line)

    if partial_record:
        yield faculty_record(temp_buffer, school_info, ranking)

