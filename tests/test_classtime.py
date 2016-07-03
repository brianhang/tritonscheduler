#!/usr/bin/env python

import unittest

from classtime import ClassTime

class ClassTimeTest(unittest.TestCase):
    def testFromString(self):
        time = ClassTime.fromString("MWF 9:00a-5:00p")

        self.assertTrue(type(time) is ClassTime)
        self.assertEqual(time.days, "MWF")
        self.assertEqual(time.start, "9:00a")
        self.assertEqual(time.finish, "5:00p")
        self.assertEqual(time.startTime, 540)
        self.assertEqual(time.finishTime, 1020)

        time = ClassTime.fromString("TuTh 12:00a-12:00p")
        
        self.assertTrue(type(time) is ClassTime)
        self.assertEqual(time.days, "TuTh")
        self.assertEqual(time.start, "12:00a")
        self.assertEqual(time.finish, "12:00p")
        self.assertEqual(time.startTime, 0)
        self.assertEqual(time.finishTime, 720)
        
        time = ClassTime.fromString("MWF 5:31a-12:00p")
        
        self.assertTrue(type(time) is ClassTime)
        self.assertEqual(time.days, "MWF")
        self.assertEqual(time.start, "5:31a")
        self.assertEqual(time.finish, "12:00p")
        self.assertEqual(time.startTime, 331)
        self.assertEqual(time.finishTime, 720)

        time = ClassTime.fromString("TuTh 12:00a-5:43p")
        
        self.assertTrue(type(time) is ClassTime)
        self.assertEqual(time.days, "TuTh")
        self.assertEqual(time.start, "12:00a")
        self.assertEqual(time.finish, "5:43p")
        self.assertEqual(time.startTime, 0)
        self.assertEqual(time.finishTime, 1063)

        time = ClassTime.fromString("M 12:00a-12:00a")

        self.assertTrue(type(time) is ClassTime)
        self.assertEqual(time.days, "M")
        self.assertEqual(time.start, "12:00a")
        self.assertEqual(time.start, time.finish)
        self.assertEqual(time.startTime, 0)
        self.assertEqual(time.startTime, time.finishTime)

    def testSetTimes(self):
        time = ClassTime()
        time.setTimes("12:00a", "12:00a")

        self.assertEqual(time.start, "12:00a")
        self.assertEqual(time.finish, "12:00a")
        self.assertEqual(time.startTime, 0)
        self.assertEqual(time.finishTime, 0)

        time.setTimes("12:00a", "12:00p")

        self.assertEqual(time.start, "12:00a")
        self.assertEqual(time.finish, "12:00p")
        self.assertEqual(time.startTime, 0)
        self.assertEqual(time.finishTime, 720)

        time.setTimes("11:59p", "12:00a")

        self.assertEqual(time.start, "11:59p")
        self.assertEqual(time.finish, "12:00a")
        self.assertEqual(time.startTime, 1439)
        self.assertEqual(time.finishTime, 0)

        time.setTimes("11:59p", "11:59p")

        self.assertEqual(time.start, "11:59p")
        self.assertEqual(time.finish, "11:59p")
        self.assertEqual(time.startTime, 1439)
        self.assertEqual(time.finishTime, 1439)

    def testIsOnDay(self):
        time = ClassTime.fromString("MWF 12:00a-12:00p")

        self.assertTrue(time.isOnDay("M"))
        self.assertTrue(time.isOnDay("W"))
        self.assertTrue(time.isOnDay("F"))
        self.assertFalse(time.isOnDay("Tu"))
        self.assertFalse(time.isOnDay("Th"))

        time = ClassTime.fromString("TuTh 12:00a-12:00p")

        self.assertFalse(time.isOnDay("M"))
        self.assertFalse(time.isOnDay("W"))
        self.assertFalse(time.isOnDay("F"))
        self.assertTrue(time.isOnDay("Tu"))
        self.assertTrue(time.isOnDay("Th"))

        time = ClassTime.fromString("M 12:00a-12:00p")

        self.assertTrue(time.isOnDay("M"))
        self.assertFalse(time.isOnDay("Tu"))
        self.assertFalse(time.isOnDay("W"))
        self.assertFalse(time.isOnDay("Th"))
        self.assertFalse(time.isOnDay("F"))

        time = ClassTime.fromString("Tu 12:00a-12:00p")

        self.assertFalse(time.isOnDay("M"))
        self.assertFalse(time.isOnDay("W"))
        self.assertFalse(time.isOnDay("Th"))
        self.assertFalse(time.isOnDay("F"))
        self.assertTrue(time.isOnDay("Tu"))

        time = ClassTime.fromString("MTuWThF 12:00a-12:00p")

        self.assertTrue(time.isOnDay("M"))
        self.assertTrue(time.isOnDay("W"))
        self.assertTrue(time.isOnDay("F"))
        self.assertTrue(time.isOnDay("Tu"))
        self.assertTrue(time.isOnDay("Th"))

    def testConflictsWith(self):
        time = ClassTime.fromString("MWF 3:00p-3:50p")
        time2 = ClassTime.fromString("MWF 3:00p-3:50p")

        self.assertTrue(time.conflictsWith(time2))
        
        time = ClassTime.fromString("TuTh 2:00p-3:20p")
        time2 = ClassTime.fromString("TuTh 2:00p-3:20p")

        self.assertTrue(time.conflictsWith(time2))

        time = ClassTime.fromString("MWF 5:00p-6:20p")
        time2 = ClassTime.fromString("TuTh 5:00p-6:20p")

        self.assertFalse(time.conflictsWith(time2))

        time = ClassTime.fromString("M 12:00a-11:59p")
        time2 = ClassTime.fromString("MWF 5:00p-5:50p")

        self.assertTrue(time.conflictsWith(time2))

        time = ClassTime.fromString("Tu 3:00p-3:01p")
        time2 = ClassTime.fromString("Tu 3:01p-3:02p")

        self.assertTrue(time.conflictsWith(time2))

        time = ClassTime.fromString("Tu 2:59p-3:00p")

        self.assertFalse(time.conflictsWith(time2))

    def testIsTimeBefore(self):
        time = ClassTime.fromString("M 12:00a-12:50a")
        time2 = ClassTime.fromString("W 12:00a-12:49a")

        self.assertFalse(time.isTimeBefore(time2))
        self.assertFalse(time2.isTimeBefore(time))

        time = ClassTime.fromString("M 12:50a-12:51a")
        time2 = ClassTime.fromString("W 12:00a-12:49a")

        self.assertFalse(time.isTimeBefore(time2))
        self.assertTrue(time2.isTimeBefore(time))

        time = ClassTime.fromString("M 12:00a-12:50a")
        time2 = ClassTime.fromString("W 12:50a-12:51a")

        self.assertFalse(time.isTimeBefore(time2))
        self.assertFalse(time2.isTimeBefore(time))

        time = ClassTime.fromString("M 12:00a-12:50a")
        time2 = ClassTime.fromString("W 12:00a-11:59p")

        self.assertFalse(time.isTimeBefore(time2))
        self.assertFalse(time2.isTimeBefore(time))

        time = ClassTime.fromString("M 12:00a-12:50a")
        time2 = ClassTime.fromString("W 11:00p-11:59p")

        self.assertTrue(time.isTimeBefore(time2))
        self.assertFalse(time2.isTimeBefore(time))

        time = ClassTime.fromString("M 12:00p-12:50p")
        time2 = ClassTime.fromString("W 12:00a-12:50a")

        self.assertFalse(time.isTimeBefore(time2))
        self.assertTrue(time2.isTimeBefore(time))

    def testIsTimeAfter(self):
        time = ClassTime.fromString("M 12:00a-12:50a")
        time2 = ClassTime.fromString("W 12:00a-12:49a")

        self.assertFalse(time.isTimeAfter(time2))
        self.assertFalse(time2.isTimeAfter(time))

        time = ClassTime.fromString("M 12:50a-12:51a")
        time2 = ClassTime.fromString("W 12:00a-12:49a")

        self.assertTrue(time.isTimeAfter(time2))
        self.assertFalse(time2.isTimeAfter(time))

        time = ClassTime.fromString("M 12:00a-12:50a")
        time2 = ClassTime.fromString("W 12:50a-12:51a")

        self.assertFalse(time.isTimeAfter(time2))
        self.assertFalse(time2.isTimeAfter(time))

        time = ClassTime.fromString("M 12:00a-12:50a")
        time2 = ClassTime.fromString("W 12:00a-11:59p")

        self.assertFalse(time.isTimeAfter(time2))
        self.assertFalse(time2.isTimeAfter(time))

        time = ClassTime.fromString("M 12:00a-12:50a")
        time2 = ClassTime.fromString("W 11:00p-11:59p")

        self.assertFalse(time.isTimeAfter(time2))
        self.assertTrue(time2.isTimeAfter(time))

        time = ClassTime.fromString("M 12:00p-12:50p")
        time2 = ClassTime.fromString("W 12:00a-12:50a")

        self.assertTrue(time.isTimeAfter(time2))
        self.assertFalse(time2.isTimeAfter(time))

    def testToString(self):
        time = ClassTime.fromString("MTuWThF 12:00a-11:59p")
        time2 = ClassTime.fromString(time.toString())

        self.assertEqual(time.days, time2.days)
        self.assertEqual(time.start, time2.start)
        self.assertEqual(time.finish, time2.finish)
        self.assertEqual(time.startTime, time2.startTime)
        self.assertEqual(time.finishTime, time2.finishTime)

        time = ClassTime.fromString("M 11:00p-11:59p")
        time2 = ClassTime.fromString(time.toString())

        self.assertEqual(time.days, time2.days)
        self.assertEqual(time.start, time2.start)
        self.assertEqual(time.finish, time2.finish)
        self.assertEqual(time.startTime, time2.startTime)
        self.assertEqual(time.finishTime, time2.finishTime)

        time = ClassTime.fromString("TuThF 12:00a-12:59a")
        time2 = ClassTime.fromString(time.toString())

        self.assertEqual(time.days, time2.days)
        self.assertEqual(time.start, time2.start)
        self.assertEqual(time.finish, time2.finish)
        self.assertEqual(time.startTime, time2.startTime)
        self.assertEqual(time.finishTime, time2.finishTime)

if __name__ == "__main__":
    unittest.main() 
