#/usr/bin/env python

QUERY_RESULT = '//tr[@class="sectxt" or @class="nonenrtxt"]|//h2|' \
               '//tr[.//td[@class="crsheader"]]'

REGEX_CODE = "\(([A-Z][A-Z][A-Z]*[A-Z]*)\s+\)"

INDEX_ID = 1
INDEX_TYPE = 2
INDEX_SECTION = 3
INDEX_DAYS = 4
INDEX_TIMES = 5
INDEX_BUILDING = 6
INDEX_ROOM = 7
INDEX_INSTR = 8

LEN_HEADER = 4
LEN_MEETING = 9

HEADER_NUM = 1

from lxml import html
from classtime import ClassTime

import re

class ParserError(Exception):
    pass

class Parser:
    def load(self, data):
        """
        Creates a tree from the HTML contents from the given HTML data for use
        in the parsing of the HTML data.

        :param self: the parser object
        :param schedule: the bytes of HTML data
        """
        tree = html.fromstring(data)
        self.elements = tree.xpath(QUERY_RESULT)

    def parse(self):
        """
        Takes the tree from loaded data, then finds the lectures, sections, and
        final times.

        :param self: the parser object
        :raises: ParserError
        :returns: the list of lectures and sections found
        """
        schedule = {}
        course = None
        courseInfo = None
        courseCode = ""
        courseNum = 0

        if not self.elements:
            raise ParserError("no data loaded for parsing")

        for element in self.elements:
            if element.tag == "h2":
                match = re.search(REGEX_CODE, element.text_content())

                # Change the current course if a header for it was encountered.
                if match:
                    courseCode = match.group(1)
            elif (element.tag == "tr" and len(element) == LEN_HEADER and
                  courseCode):
                if (course and course in schedule and courseInfo is not None and
                    len(courseInfo) > 0):
                    schedule[course].append(courseInfo)

                # Set the course number if it was found in the course header.
                course = (courseCode + " "
                          + element[HEADER_NUM].text_content().strip())

                if course not in schedule:
                    schedule[course] = []

                courseInfo = {}
            elif courseInfo is not None and len(element) == LEN_MEETING:
                # Get the parts of the meeting.
                sectionID = element[INDEX_ID].text_content().strip()
                meetingType = element[INDEX_TYPE].text_content().strip()
                section = element[INDEX_SECTION].text_content().strip()
                days = element[INDEX_DAYS].text_content().strip()
                times = element[INDEX_TIMES].text_content().strip()
                building = element[INDEX_BUILDING].text_content().strip()
                room = element[INDEX_ROOM].text_content().strip()
                instructor = element[INDEX_INSTR].text_content().strip()

                # If the meeting is a final, then add it to the course in its
                # own format instead of a list, since a list is not needed.
                if meetingType == "FI":
                    courseInfo["FI"] = {
                        "date": section,
                        "time": ClassTime.fromString(days + " " + times),
                        "building": building,
                        "room": room
                    }    

                    continue


                # Otherwise, add the meeting normally.
                meeting = {
                    "sectionID": sectionID,
                    "time": ClassTime.fromString(days + " " + times),
                    "building": building,
                    "room": room,
                    "instructor": instructor
                }

                if meetingType == "LE":
                    # If the meeting is a lecture, there is no need to make it a
                    # part of a list since there is only 1 lecture.
                    courseInfo["LE"] = meeting
                else:
                    # But other sections can have multiples, so a list is
                    # needed.
                    if meetingType not in courseInfo:
                        courseInfo[meetingType] = []

                    courseInfo[meetingType].append(meeting)

        # Add any leftover course.
        if courseInfo is not None and len(courseInfo) > 0:
            schedule[course].append(courseInfo)

        return schedule
