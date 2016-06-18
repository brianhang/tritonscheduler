#!/usr/bin/env python

SECONDS_MIN = 60
SECONDS_HOUR = SECONDS_MIN * 60

class ClassTime:
    days = "MTuWThF"
    start = "00:00a"
    finish = "11:59p"
    startTime = 0
    finishTime = (11 * SECONDS_HOUR) + (59 * SECONDS_MIN)

    def setDays(self, newDays):
        """
        Sets which days this time occurs on. The days available are (M)onday,
        (Tu)esday, (W)ednesday, (Th)ursday, and (F)riday.

        :param self: the ClassTime object
        :param newDays: which days this class occurs on
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
        self.setStart(newStart, newFinish)

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
        """
        pass

    def isOnDay(self, day):
        """
        Returns whether or not the days of the ClassTime object contains the
        day.

        :param self: the ClassTime object
        :param day: a day of the week
        """
        pass

    def isTimeBefore(self, other):
        """
        Returns whether or not the time for this ClassTime is before the time of
        the given ClassTime object.

        :param self: the ClassTime object
        :param other: the other ClassTime object to compare with
        """
        pass

    def isTimeAfter(self, other):
        """
        Returns whether or not the time for this ClassTime is after the time of
        the given ClassTime object.

        :param self: the ClassTime object
        :param other: the other ClassTime object to compare with
        """
        pass
