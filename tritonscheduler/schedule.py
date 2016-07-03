#!/usr/bin/env python

from classparser import ClassParser

import re
import requests

# The URL for loading the normal Schedule of Classes.
BASE_URL = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesFaculty" \
           "Result.htm?tabNum=tabs-crs"

# The URL for the printable version of the Schedule of Classes.
BASE_URL_PRINT = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClasses" \
                  "FacultyResultPrint.htm?tabNum=tabs-crs"

# Patterns for identifying a course name.
REGEX_TERM = "([A-Z][0-9A-Z])(\d\d)"
REGEX_COURSE = "([A-Z][A-Z][A-Z]*[A-Z]*\s\w+)"

# The URL encoded new line.
NEW_LINE = "%0D%0A"

# Two letter term codes used by the Schedule of Classes.
VALID_TERMS = set(["FA", "WI", "SU", "SP", "SA", "S3", "S2", "S1"])

class ScheduleError(Exception):
    """
    A type of exception that is raised by the Schedule class.
    """
    pass

class Schedule(object):
    """
    The Schedule class is responsible for handling input for a schedule and
    loading the corresponding schedule data. It also delegates the parsing of
    schedule data to the ClassParser class.

    :ivar courses: a list of course codes for desired courses
    :ivar term: which term to search in (two uppercase letters and 2 digit year)
    """

    @staticmethod
    def validateTerm(newTerm):
        """
        Checks whether or not a given term code is in the format of a two letter
        valid season followed by a two digit year.

        :param newTerm: the term code to check
        :returns: True if the given term is valid, False otherwise
        """
        newTerm = newTerm.upper()
        match = re.match(REGEX_TERM, newTerm)

        if not match:
            return False

        return (match.group(1) in VALID_TERMS)

    @staticmethod
    def validateCourse(course):
        """
        Checks whether or not a given course code is in the valid format of the
        department followed by the course number.

        :param course: the course code to check
        :returns: True if the course code is valid, False otherwise
        """
        course = course.upper()
        match = re.match(REGEX_COURSE, course)

        return match is not None

    def getScheduleURL(self, forPrinting = False):
        """
        Creates a URL that searches for the specified courses at the given term
        using the UCSD Schedule of Classes. This will return an empty string if
        the list of desired courses is empty.

        :param self: the schedule object
        :param forPrinting: whether or not the print URL is needed
        :raises: ScheduleError
        :returns: the URL as a string if successful, empty string otherwise
        """
        if not self.courses:
            raise ScheduleError("no course list provided")

        if not self.term:
            raise ScheduleError("no term provided")

        return ((BASE_URL_PRINT if forPrinting else BASE_URL)
                + "&selectedTerm=" + self.term
                + "&courses=" + NEW_LINE.join(self.courses).replace(" ", "+"))

    def retrieve(self):
        """
        Finds all of the available, matching courses (with their corresponding
        lectures and sections) for the given term.

        :param self: the schedule object
        :raises: ScheduleError
        :returns: a dictionary with the course name as the key and list of
        course objects as the value
        """
        if not self.courses:
            raise ScheduleError("no course list provided")

        if len(self.courses) == 0:
            return []
        
        if not self.term or not Schedule.validateTerm(self.term):
            raise ScheduleError("invalid term provided")

        # Get the Schedule of Classes result.
        session = requests.Session()
        session.get(self.getScheduleURL(False))

        result = session.get(self.getScheduleURL(True))

        # Close the connection.
        session.close()

        # Raise an exception if the request failed.
        result.raise_for_status()

        parser = ClassParser()
        parser.load(result.content)

        return parser.parse()
