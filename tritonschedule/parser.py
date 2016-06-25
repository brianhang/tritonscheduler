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
from schedule import Schedule

import re
import requests

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, schedule):
        self.schedule = schedule

    def load(self):
        """
        Creates a tree from the HTML contents from the given URL.

        :param self: the parser object
        :param schedule: the schedule to get the schedule URL from
        :raises: ParserError
        """
        if type(self.schedule) is not Schedule:
            raise ParserError("invalid type for schedule")

        session = requests.Session()
        session.get(self.schedule.getScheduleURL(False))

        result = session.get(self.schedule.getScheduleURL(True))

        # Raise an exception if the request failed.
        result.raise_for_status()

        tree = html.fromstring(result.content)
        self.elements = tree.xpath(QUERY_RESULT)

    def parse(self):
        """
        Takes the tree from the given URL and finds the lectures, sections, and
        final times.

        :param self: the parser object
        :raises: ParserError
        :returns: the list of lectures and sections found
        """
        schedule = {}
        course = None
        courseCode = ""
        courseNum = 0

        if type(self.schedule) is not Schedule:
            raise ParserError("invalid type for schedule")

        for element in self.elements:
            if element.tag == "h2":
                match = re.search(REGEX_CODE, element.text_content())

                # Change the current course if a header for it was encountered.
                if match:
                    courseCode = match.group(1)
            elif (element.tag == "tr" and len(element) == LEN_HEADER and
                  courseCode):
                # Set the course number if it was found in the course header.
                course = (courseCode + " "
                          + element[HEADER_NUM].text_content().strip())
            elif course is not None and len(element) == LEN_MEETING:
                # Add a meeting if one was found and a course has been set.
                if course not in schedule:
                    schedule[course] = {}

                # Get the parts of the meeting.
                sectionID = element[INDEX_ID].text_content().strip()
                meetingType = element[INDEX_TYPE].text_content().strip()
                section = element[INDEX_SECTION].text_content().strip()
                days = element[INDEX_DAYS].text_content().strip()
                times = element[INDEX_TIMES].text_content().strip()
                building = element[INDEX_BUILDING].text_content().strip()
                room = element[INDEX_BUILDING].text_content().strip()
                instructor = element[INDEX_INSTR].text_content().strip()

                # If the meeting is a final, add it in a special format.
                if meetingType == "FI":
                    schedule[course]["FI"] = {
                        "date": section,
                        "day": days,
                        "times": times,
                        "building": building,
                        "room": room
                    }    

                    continue

                # Otherwise, add the meeting normally.
                if meetingType not in schedule[course]:
                    schedule[course][meetingType] = []

                schedule[course][meetingType].append({
                    "sectionID": sectionID,
                    "days": days,
                    "times": times,
                    "building": building,
                    "room": room,
                    "instructor": instructor
                })

        return schedule
