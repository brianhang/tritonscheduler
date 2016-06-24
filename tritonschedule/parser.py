#/usr/bin/env python

QUERY_RESULT = "//tr[@class=\"sectxt\" or @class=\"nonenrtxt\"]|//h2"

REGEX_CODE = "(\([A-Z][A-Z][A-Z]*[A-Z]*\)[\s+])"

INDEX_ID = 1
INDEX_TYPE = 2
INDEX_SECTION = 3
INDEX_DAYS = 4
INDEX_TIMES = 5
INDEX_BUILDING = 6
INDEX_ROOM = 7
INDEX_INSTR = 8

from lxml import html
import requests

class Parser:
    def load(self, url):
        """
        Creates a tree from the HTML contents from the given URL.

        :param self: the parser object
        :param url: where the HTML content is located
        """
        result = requests.get(url)

        # Raise an exception if the request failed.
        result.raise_for_status()

        tree = html.fromstring(result.content)
        self.elements = tree.xpath(RESULT_QUERY)

    def parse():
        """
        Takes the tree from the given URL and finds the lectures, sections, and
        final times.

        :param self: the parser object
        :returns: the list of lectures and sections found
        """
        schedule = {}
        course = None

        for element in self.elements:
            if element.tag == "h2":
                match = re.match(REGEX_CODE, element.text_content())

                # Change the current course if a header for it was encountered.
                if match:
                    course = match.group(1)
            else if course is not None:
                # Otherwise, add a meeting to the last course.
                if not schedule[course]:
                    schedule[course] = {}

                # Get the parts of the meeting.
                sectionID = element[INDEX_ID].text_content().trim()
                meetingType = element[INDEX_TYPE].text_content().trim()
                section = element[INDEX_SECTION].text_content().trim()
                days = element[INDEX_DAYS].text_content().trim()
                times = element[INDEX_TIMES].text_content().trim()
                building = element[INDEX_BUILDING].text_content().trim()
                room = element[INDEX_BUILDING].text_content().trim()
                instructor = element[INDEX_INSTR].text_content().trim()

                # If the meeting is a final, add it in a special format.
                if meetingType == "FI":
                    schedule[course].FI = {
                        date = section,
                        day = days,
                        times = times,
                        building = building,
                        room = room
                    }    

                    continue

                # Otherwise, add the meeting normally.
                if not schedule[course][meetingType]:
                    schedule[course][meetingType] = []

                schedule[course][meetingType].append({
                    sectionID = sectionID,
                    days = days,
                    times = times,
                    building = building,
                    room = room,
                    instructor = instructor
                })

        return schedule
