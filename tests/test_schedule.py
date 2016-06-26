#!/usr/bin/env python

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from tritonschedule.schedule import Schedule
from tritonschedule.schedule import ScheduleError

class ScheduleTest(unittest.TestCase):
    def setUp(self):
        self.schedule = Schedule();

    def testValidateTerm(self):
        self.assertTrue(Schedule.validateTerm("FA15"))
        self.assertTrue(Schedule.validateTerm("WI99"))
        self.assertTrue(Schedule.validateTerm("SP00"))
        self.assertTrue(Schedule.validateTerm("SU16"))
        self.assertTrue(Schedule.validateTerm("S115"))
        self.assertTrue(Schedule.validateTerm("S227"))
        self.assertTrue(Schedule.validateTerm("SA01"))
        
        self.assertFalse(Schedule.validateTerm(""))
        self.assertFalse(Schedule.validateTerm("FA"))
        self.assertFalse(Schedule.validateTerm("16"))
        self.assertFalse(Schedule.validateTerm("FA 16"))
        self.assertFalse(Schedule.validateTerm("FA1 6"))
        self.assertFalse(Schedule.validateTerm("FB00"))
        self.assertFalse(Schedule.validateTerm("XY16"))

    def testGetScheduleURL(self):
        self.schedule.courses = None
        self.schedule.term = None

        self.assertRaises(ScheduleError, self.schedule.getScheduleURL)

        self.schedule.courses = []
        self.assertRaises(ScheduleError, self.schedule.getScheduleURL)

        self.schedule.courses = None
        self.schedule.term = "FA16"
        self.assertRaises(ScheduleError, self.schedule.getScheduleURL)

        self.schedule.courses = ["CSE 30"]
        self.assertEqual(self.schedule.getScheduleURL(),
                         "https://act.ucsd.edu/scheduleOfClasses/scheduleOf" \
                         "ClassesFacultyResult.htm?tabNum=tabs-crs&selected" \
                         "Term=FA16&courses=CSE+30")

        self.schedule.courses.append("CSE 12")
        self.assertEqual(self.schedule.getScheduleURL(),
                         "https://act.ucsd.edu/scheduleOfClasses/scheduleOf" \
                         "ClassesFacultyResult.htm?tabNum=tabs-crs&selected" \
                         "Term=FA16&courses=CSE+30%0D%0ACSE+12")

    def testRetrieve(self):
        self.schedule.courses = None
        self.schedule.term = None
        self.assertRaises(ScheduleError, self.schedule.retrieve)

        self.schedule.courses = ["CSE 30"]
        self.assertRaises(ScheduleError, self.schedule.retrieve)

        self.schedule.term = "FA16"

        result = self.schedule.retrieve()

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result["CSE 30"]), 2)
        
        self.schedule.courses = ["CSE 12", "DOC 1", "CSE 15L"]

        result = self.schedule.retrieve()

        self.assertEqual(len(result), 3)
        self.assertEqual(len(result["CSE 12"]), 3)
        self.assertEqual(len(result["CSE 15L"]), 3)
        self.assertEqual(len(result["DOC 1"]), 3)

        self.assertEqual(len(result["CSE 12"][0]["DI"]), 1)
        self.assertEqual(len(result["CSE 12"][1]["DI"]), 1)

if __name__ == "__main__":
    unittest.main()
