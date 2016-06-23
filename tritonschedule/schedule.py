#!/usr/bin/env python

import re

BASE_URL = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesFaculty" \
           "Result.htm"
TERM_REGEX = "([A-Z][0-9A-Z])(\d\d)"
NEW_LINE = "%0D%0A"
VALID_TERMS = set(["FA", "WI", "SU", "SP", "SA", "S3", "S2", "S1"])

class Schedule(object):
    courses = []
    term = "FA00"

    def setTerm(self, newTerm):
        """
        Validates the given term to ensure it is in the proper format for the
        Schedule of Classes and sets the schedule's term to it if it is valid.

        :param self: the schedule object
        :param newTerm: the desired term for the schedule
        :returns: True if the term is valid, False otherwise
        """
        if not self.validateTerm(newTerm):
            return False

        self.term = newTerm

        return True

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
        match = re.match(TERM_REGEX, newTerm)

        if not match:
            return False

        return (match.group(1) in VALID_TERMS)

    def getScheduleURL(self):
        """
        Creates a URL that searches for the specified courses at the given term
        using the UCSD Schedule of Classes. This will return an empty string if
        the list of desired courses is empty.

        :param self: the schedule object
        :returns: the URL as a string if successful, empty string otherwise
        """
        if len(self.courses) == 0:
            return ""

        return (BASE_URL + "?selectedTerm=" + self.term + "&courses=" +
                NEW_LINE.join(self.courses).replace(" ", "+"))

    def retrieve(self):
        """
        Finds all of the available, matching courses (with their corresponding
        lectures and sections) for the given term.

        :param self: the schedule object
        :returns: a dictionary with the course name as the key and list of
        course objects as the value
        """
        return []
