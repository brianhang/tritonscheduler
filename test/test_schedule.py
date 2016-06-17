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
        self.assertTrue(self.schedule.validateTerm("FA15"))
        self.assertTrue(self.schedule.validateTerm("WI99"))
        self.assertTrue(self.schedule.validateTerm("SP00"))
        self.assertTrue(self.schedule.validateTerm("SU16"))
        self.assertTrue(self.schedule.validateTerm("S115"))
        self.assertTrue(self.schedule.validateTerm("S227"))
        self.assertTrue(self.schedule.validateTerm("SA01"))
        
        self.assertFalse(self.schedule.validateTerm(""))
        self.assertFalse(self.schedule.validateTerm("FA"))
        self.assertFalse(self.schedule.validateTerm("16"))
        self.assertFalse(self.schedule.validateTerm("FA 16"))
        self.assertFalse(self.schedule.validateTerm("FA1 6"))
        self.assertFalse(self.schedule.validateTerm("FB00"))
        self.assertFalse(self.schedule.validateTerm("XY16"))

    def testTerm(self):
        self.assertTrue(self.schedule.setTerm("FA15"))
        self.assertEqual(self.schedule.getTerm(), "FA15")

        self.assertFalse(self.schedule.setTerm("_"))

    def testCourse(self):
        self.assertEqual(len(self.schedule.getCourses()), 0)

        self.schedule.addCourse("CSE 11")
        self.assertEqual(len(self.schedule.getCourses()), 1)

if __name__ == "__main__":
    unittest.main()
