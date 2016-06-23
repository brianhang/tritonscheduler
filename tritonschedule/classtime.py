#!/usr/bin/env python

import re

HOUR = 60

REGEX_CLASSTIME = "([a-zA-Z]+)[\s+](\d*\d:\d\d[ap])-(\d*\d:\d\d[ap])" 
REGEX_TIME = "(\d*\d):(\d\d)([ap])"
REGEX_DAY = "([A-Z][a-z]*)"

MAX_HOURS = 12
MAX_MINS = 60

INDEX_DAYS = 1
INDEX_START = 2
INDEX_FINISH = 3
INDEX_HOURS = 1
INDEX_MINS = 2
INDEX_PERIOD = 3

class ClassTime(object):
    days = "MTuWThF"
    start = "00:00a"
    finish = "11:59p"
    startTime = 0
    finishTime = (11 * HOUR) + 59

    @staticmethod
    def toMinutes(hour, minutes, period):
        """
        Converts hours and minutes into the number of minutes within the day. 

        :param hour: the hour number
        :param minutes: the minute number
        :returns: the number of minutes representing the hour:minutes time if
        successfully converted, -1 otherwise
        """
        period = period.lower()

        # Check that the period is valid.
        if period != "a" and period != "p":
            return -1

        # Return appropriate values for noon and midnight.
        if hour == MAX_HOURS:
            return HOUR * (MAX_HOURS if period == "p" else 0) + minutes

        # If PM, then add 12 hours to convert to a 24 hour time.
        if period == "p":
            hour += MAX_HOURS

        # Convert hours to minutes.
        hour *= HOUR

        return hour + minutes

    @classmethod
    def fromString(thisClass, date):
        """
        Creates a ClassTime object given a string that is in the format of
        weekday followed by a start time, a dash, and a finish time. Note that
        None will be returned if the given date string is not in a valid format.

        :param thisClass: the ClassTime class
        :param date: the string representation of the ClassTime
        :returns: a corresponding ClassTime object if valid, None otherwise
        """
        match = re.fullmatch(REGEX_CLASSTIME, date.strip())

        if not match:
            return None

        time = thisClass()
        time.days = match.group(INDEX_DAYS)
        time.setTimes(match.group(INDEX_START), match.group(INDEX_FINISH))

        return time

    def setTimes(self, newStart, newFinish):
        """
        Sets the time range for the class time. The times are formatted as
        hh:mma or hh:mmp where hours (hh) range from 00-12 and minutes (mm)
        range from 00-59.

        :param self: the ClassTime object
        :param newStart: the date/time string for when the class starts
        :param newFinish: the date/time string for when the class finishes
        """
        # Delegate the parsing and setting to setStart and setFinish.
        self.setStart(newStart)
        self.setFinish(newFinish)

    def setStart(self, newStart):
        """
        Sets the start time of the class.

        :param self: the ClassTime object
        :param newStart: the start time date/time string
        :returns: True if the start time was set, False otherwise
        """
        # Make sure the start time is valid.
        newStart = newStart.strip().lower()
        match = re.match(REGEX_TIME, newStart)

        if not match:
            return False

        # Get the hours and minutes as numbers.
        hours = int(match.group(INDEX_HOURS))
        minutes = int(match.group(INDEX_MINS)) % MAX_MINS
        period = match.group(INDEX_PERIOD)

        # Set the numeric start time.
        self.startTime = ClassTime.toMinutes(hours, minutes, period)
        self.start = newStart

        return (self.startTime > -1)

    def setFinish(self, newFinish):
        """
        Sets the finish time of the class.

        :param self: the ClassTime object
        :param newStart: the finish time date/time string
        """
        # Make sure the finish time is valid.
        newFinish = newFinish.strip().lower()
        match = re.match(REGEX_TIME, newFinish)

        if not match:
            return False

        # Get the hours and minutes as numbers.
        hours = int(match.group(INDEX_HOURS))
        minutes = int(match.group(INDEX_MINS))
        period = match.group(INDEX_PERIOD).lower()

        # Set the numeric start time.
        self.finishTime = ClassTime.toMinutes(hours, minutes, period)
        self.finish = newFinish

        return (self.finishTime > -1)

    def isTimeBefore(self, other):
        """
        Returns whether or not the time for this ClassTime is before the time of
        the given ClassTime object. This returns False if the other object is
        not a ClassTime object.

        :param self: the ClassTime object
        :param other: the other ClassTime object to compare with
        :returns: whether or not this ClassTime occurs before
        """
        if type(other) is ClassTime:
            return (self.startTime < other.startTime and
                    self.finishTime < other.startTime and
                    self.startTime < other.finishTime and
                    self.finishTime < other.finishTime)

        return False

    def isTimeAfter(self, other):
        """
        Returns whether or not the time for this ClassTime is after the time of
        the given ClassTime object. This returns False if the other object is
        not a ClassTime object.

        :param self: the ClassTime object
        :param other: the other ClassTime object to compare with
        :returns: whether or not this ClassTime occurs after
        """
        if type(other) is ClassTime:
            return (self.startTime > other.finishTime and
                    self.finishTime > other.finishTime and
                    self.startTime > other.startTime and
                    self.finishTime > other.startTime)

        return False

    def conflictsWith(self, other):
        """
        Returns whether or not the day or time for this ClassTime overlaps with
        a given ClassTime object.

        :param self: the ClassTime object
        :param other: the other ClassTime object to compare with
        :returns: whether or not there is any time overlap (if any days match)
        """
        # Check day conflicts before time conflicts.
        if not self.isOnDay(other.days):
            return False

        return (self.startTime <= other.finishTime and
                other.startTime <= self.finishTime)

    def isOnDay(self, day):
        """
        Returns whether or not the days of the ClassTime object contains the
        day.

        :param self: the ClassTime object
        :param day: a day of the week
        :returns: whether or not the ClassTime occurs on the given day
        """
        for day in re.findall(REGEX_DAY, day):
            if self.days.find(day) > -1:
                return True

        return False

    def toString(self):
        """
        Returns the string representation of the ClassTime object by combining
        the days and the dash separated start and finish times. This
        representation is the same as the input for the ClassTime.fromString
        function.

        :param self: the ClassTime object
        :returns: the string representation
        """
        return self.days + " " + self.start + "-" + self.finish

    def __str__(self):
        return self.toString()
