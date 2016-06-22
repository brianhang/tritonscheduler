#!/usr/bin/env python

class Schedule:
    courses = []
    term = "FA16"

    @staticmethod
    def validateTerm(self, newTerm):
        """
        Checks whether or not a given term code is in the format of a two letter
        valid season followed by a two digit year.

        :param self: the schedule object
        :param newTerm: the term code to check
        :returns: True if the given term is valid, False otherwise
        """
        return False

    def getScheduleURL(self):
        """
        Creates a URL that searches for the specified courses at the given term
        using the UCSD Schedule of Classes.

        :param self: the schedule object
        :returns: the URL as a string if successful, empty string otherwise
        """
        return ""

    def retrieve(self):
        """
        Finds all of the available, matching courses (with their corresponding
        lectures and sections) for the given term.

        :param self: the schedule object
        :returns: a dictionary with the course name as the key and list of
        course objects as the value
        """
        return []
