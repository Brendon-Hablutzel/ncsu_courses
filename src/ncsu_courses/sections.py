from bs4 import BeautifulSoup
from dataclasses import dataclass
import datetime
from enum import Enum
from util import get_course_html
from term import Term
from typing import Generator


class MeetingDay(Enum):
    '''
    Represents a possible meeting day for a section.
    '''

    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

    def from_str(string):
        '''
        Takes a string meeting day and converts it to its enum variant.
        '''
        match string:
            case "Monday":
                return MeetingDay.Monday
            case "Tuesday":
                return MeetingDay.Tuesday
            case "Wednesday":
                return MeetingDay.Wednesday
            case "Thursday":
                return MeetingDay.Thursday
            case "Friday":
                return MeetingDay.Friday
            case "Saturday":
                return MeetingDay.Saturday
            case "Sunday":
                return MeetingDay.Sunday
            case other:
                raise AttributeError(
                    "could not find corresponding meeting day for:", other)


class Component(Enum):
    '''
    Represents a section component type, such as Lab or Lecture.
    '''
    Lecture = "Lec"
    Lab = "Lab"
    Research = "Res"
    Project = "Pro"
    Independent = "Ind"
    Thesis = "The"  # uncertain

    def from_str(string):
        '''
        Takes a string section component and returns its corresponding
        enum variant.
        '''
        match string:
            case "Lec":
                return Component.Lecture
            case "Lab":
                return Component.Lab
            case "Res":
                return Component.Research
            case "Pro":
                return Component.Project
            case "Ind":
                return Component.Independent
            case "The":
                return Component.Thesis
            case other:
                raise AttributeError(
                    "could not find corresponding course component for:", other)


class Availability(Enum):
    '''
    Represents the availability for a section, such as Open or Closed.
    '''
    Closed = "Closed"
    Waitlist = "Waitlist"
    Open = "Open"
    Reserved = "Reserved"

    def from_str(string):
        '''
        Takes a string availability status and returns its corresponding 
        enum variant.
        '''
        match string:
            case "Closed":
                return Availability.Closed
            case "Waitlist":
                return Availability.Waitlist
            case "Open":
                return Availability.Open
            case "Reserved":
                return Availability.Reserved
            case other:
                raise AttributeError(
                    "could not find corresponding availability for:", other)


@dataclass
class Section:
    '''
    Represents a parsed section of a course.
    '''
    course_curriculum: str
    course_code: int
    section: str
    component: Component
    instructor_name: str
    open_seats: int
    total_seats: int
    availability_status: Availability
    num_on_waitlist: int | None
    start_time: datetime.time | None
    end_time: datetime.time | None
    start_date: datetime.date
    end_date: datetime.date
    meeting_days: list[MeetingDay]
    location: str | None  # change this to an enum later?

    def to_json(self) -> dict:
        '''
        Returns the given section's JSON representation.
        '''
        return {
            "curriculum": self.course_curriculum,
            "code": self.course_code,
            "section": self.section,
            "component": self.component,
            "instructor_name": self.instructor_name,
            "open_seats": self.open_seats,
            "total_seats": self.total_seats,
            "availability_status": self.availability_status,
            "num_on_waitlist": self.num_on_waitlist,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "meeting_days": self.meeting_days,
            "location": self.location
        }


def parse_section_html_soup(
    course_curriculum: str,
    course_code: int,
    section_soup: BeautifulSoup
) -> Section:
    '''
    Takes a BeautifulSoup representation of a section and returns a
    Section object.
    '''
    data_columns = section_soup.find_all("td")

    section = data_columns[0].text

    component = Component.from_str(data_columns[1].text)

    availability_info = list(data_columns[3].strings)
    availability_status = Availability.from_str(availability_info[0])
    seats_info = availability_info[1]

    match availability_status:
        case Availability.Open | Availability.Closed | Availability.Reserved:
            seats_info = seats_info.split("/")
            open_seats = int(seats_info[0])
            total_seats = int(seats_info[1])
            num_on_waitlist = 0
        case Availability.Waitlist:
            seats_info = seats_info.split("/")
            open_seats = int(seats_info[0])
            seats_info = seats_info[1].split(" ")
            total_seats = int(seats_info[0])
            num_on_waitlist = int(
                seats_info[1].replace("(", "").replace(")", ""))
        case other:
            raise KeyError("invalid availability status:", other)

    meeting_info = data_columns[4]

    if meeting_info.find(class_="weekdisplay") is not None:
        meeting_day_strs = (day.get("title").split(" - ")[0]
                            for day in meeting_info.find_all("abbr") if "meet" in day.get("title"))
        meeting_days = list(map(MeetingDay.from_str, meeting_day_strs))

        meeting_time = list(meeting_info.strings)[-1].split("-")

        if meeting_time[0] == "TBD":
            start_time = None
            end_time = None
        else:
            start_time = meeting_time[0].strip()
            start_time = datetime.datetime.strptime(
                start_time, "%I:%M %p").time()

            end_time = meeting_time[1].strip()
            end_time = datetime.datetime.strptime(end_time, "%I:%M %p").time()

    else:
        meeting_days = []
        start_time = None
        end_time = None

    location = data_columns[5].text
    if location == "":
        location = None

    instructor_name = data_columns[6].text

    date_info = data_columns[7].text.split("-")
    start_date = date_info[0].strip()
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%y").date()

    # sometimes, a string with details is appended to the date range
    end_date = date_info[1].strip()[:8]
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%y").date()

    return Section(
        course_curriculum,
        course_code,
        section,
        component,
        instructor_name,
        open_seats,
        total_seats,
        availability_status,
        num_on_waitlist,
        start_time,
        end_time,
        start_date,
        end_date,
        meeting_days,
        location
    )


def get_all_sections(subject: str, term: Term) -> Generator[Section, None, None]:
    '''
    Returns a generator of parsed sections of all courses associated with 
    the given subject during the given term.
    '''

    course_html = get_course_html(subject, term)

    soup = BeautifulSoup(course_html, 'html.parser')

    courses = soup.find_all(class_="course")
    for course in courses:
        course_info = course.get("id").split("-")
        curriculum = course_info[0]
        code = int(course_info[1])

        sections = course.find(
            class_="section-table").findChildren("tr", recursive=False)

        for section in sections:
            yield parse_section_html_soup(curriculum, code, section)
