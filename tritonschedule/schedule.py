#!/usr/bin/env python

from .parser import Parser

import re
import requests

BASE_URL = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesFaculty" \
           "Result.htm?tabNum=tabs-crs"
BASE_URL_PRINT = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClasses" \
                  "FacultyResultPrint.htm?tabNum=tabs-crs"

REGEX_TERM = "([A-Z][0-9A-Z])(\d\d)"

NEW_LINE = "%0D%0A"
VALID_TERMS = set(["FA", "WI", "SU", "SP", "SA", "S3", "S2", "S1"])

class ScheduleError(Exception):
    pass

class Schedule(object):
    @staticmethod
    def validateTerm(newTerm):
        """
        Checks whether or not a given term code is in the format of a two letter
        valid season followed by a two digit year.

        :param self: the schedule object
        :param newTerm: the term code to check
        :returns: True if the given term is valid, False otherwise
        """
        newTerm = newTerm.upper()
        match = re.match(REGEX_TERM, newTerm)

        if not match:
            return False

        return (match.group(1) in VALID_TERMS)

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

        parser = Parser()
        parser.load(result.content)

        return parser.parse()
