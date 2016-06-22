#!/usr/bin/env python

SECONDS_MIN = 60
SECONDS_HOUR = SECONDS_MIN * 60

class ClassTime:
    days = "MTuWThF"
    start = "00:00a"
    finish = "11:59p"
    startTime = 0
    finishTime = (11 * SECONDS_HOUR) + (59 * SECONDS_MIN)

    @classmethod
    def fromString(myClass, date):
        """
        Creates a ClassTime object given a string that is in the format of
        weekday followed by a start time, a dash, and a finish time.

        :param myClass: the ClassTime class
        :param date: the string representation of the ClassTime
        :returns: a corresponding ClassTime object
        """
        pass

    def setTimes(self, newStart, newFinish):
        """
        Sets the time range for the class time. The times are formatted as
        hh:mma or hh:mmp where hours (hh) range from 00-12 and minutes (mm)
        range from 00-59.

        :param self: the ClassTime object
        :param newStart: the date/time string for when the class starts
        :param newFinish: the date/time string for when the class finishes
        """
        self.setStart(newStart)
        self.setFinish(newFinish)

    def setStart(self, newStart):
        """
        Sets the start time of the class.

        :param self: the ClassTime object
        :param newStart: the start time date/time string
        """
        pass

    def setFinish(self, newFinish):
        """
        Sets the finish time of the class.

        :param self: the ClassTime object
        :param newStart: the finish time date/time string
        """
        pass

    def conflictsWith(self, other):
        """
        Returns whether or not the day or time for this ClassTime overlaps with
        a given ClassTime object.

        :param self: the ClassTime object
        :param other: the other ClassTime object to compare with
        :returns: whether or not there is any time overlap (if any days match)
        """
        return False

    def isOnDay(self, day):
        """
        Returns whether or not the days of the ClassTime object contains the
        day.

        :param self: the ClassTime object
        :param day: a day of the week
        :returns: whether or not the ClassTime occurs on the given day
        """
        return False

    def isTimeBefore(self, other):
        """
        Returns whether or not the time for this ClassTime is before the time of
        the given ClassTime object.

        :param self: the ClassTime object
        :param other: the other ClassTime object to compare with
        :returns: whether or not this ClassTime occurs before
        """
        return False

    def isTimeAfter(self, other):
        """
        Returns whether or not the time for this ClassTime is after the time of
        the given ClassTime object.

        :param self: the ClassTime object
        :param other: the other ClassTime object to compare with
        :returns: whether or not this ClassTime occurs after
        """
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
        return ""

    def __str__(self):
        return self.toString()
