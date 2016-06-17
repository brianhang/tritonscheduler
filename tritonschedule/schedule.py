#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Schedule:
    courses = []
    term = "FA16"

    def setTerm(self, newTerm):
        """
        Sets which term will be used to find the desired courses.

        :param self: the schedule object
        :param newTerm: the term that will be used
        :returns: True if the term was valid, False otherwise.
        """
        self.term = newTerm;

    def getTerm(self):
        """
        Returns the last set term. By default this is FA16."

        :param self: the schedule object
        :returns: the last set term
        """
        return self.term

    def addCourse(self, code):
        """
        Adds a course code that will be searched for within the schedule of
        classes.

        :param self: the schedule object
        :param code: the course's code (CSE 30, MATH 20C, etc...)
        """
        self.courses.append(code)

    def getCourses(self):
        """
        Returns a list of all the added course codes.

        :param self: the schedule object
        :returns: a list with all the added course codes
        """
        return self.courses

    def validateTerm(self, newTerm):
        """
        Checks whether or not a given term code is in the format of a two letter
        valid season followed by a two digit year.

        :param self: the schedule object
        :param newTerm: the term code to check
        :returns: True if the given term is valid, False otherwise
        """
        pass

    def retrieve(self):
        """
        Finds all of the available, matching courses (with their corresponding
        lectures and sections) for the given term.

        :param self: the schedule object
        :returns: a dictionary with the course name as the key and list of
        course objects as the value
        """
        pass
