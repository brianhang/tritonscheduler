#!/usr/bin/env python

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from tritonschedule.schedule import Schedule

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

    def testTerm(self):
        self.assertTrue(self.schedule.setTerm("FA15"))
        self.assertEqual(self.schedule.term, "FA15")

        self.assertFalse(self.schedule.setTerm("_"))

    def testGetScheduleURL(self):
        self.schedule.courses = []
        self.schedule.term = "FA16"

        self.assertEqual(self.schedule.getScheduleURL(), "")

        self.schedule.courses = ["CSE 30"]
        self.assertEqual(self.schedule.getScheduleURL(),
                         "https://act.ucsd.edu/scheduleOfClasses/scheduleOf" \
                         "ClassesFacultyResult.htm?selectedTerm=FA16&courses=" \
                         "CSE+30")

        self.schedule.courses.append("CSE 12")
        self.assertEqual(self.schedule.getScheduleURL(),
                         "https://act.ucsd.edu/scheduleOfClasses/scheduleOf" \
                         "ClassesFacultyResult.htm?selectedTerm=FA16&courses=" \
                         "CSE+30%0D%0ACSE+12")

if __name__ == "__main__":
    unittest.main()
