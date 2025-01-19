from bs4 import BeautifulSoup
from ncsu_courses.datatypes import Course
from ncsu_courses.datatypes import Section, Component, MeetingDay, Availability
from typing import Generator, Iterable
import datetime


class HTMLParser:
    def __init__(self, html_str: str, subject: str):
        self.soup = BeautifulSoup(html_str, "html.parser")
        self.subject = subject

    def get_courses_soup(self) -> Iterable[BeautifulSoup]:
        return self.soup.find_all(class_="course")


class CourseParser:
    def __init__(self, course_soup: BeautifulSoup, subject: str):
        self.course_soup = course_soup
        self.subject = subject
        (self.course_curriculum, self.course_code) = self._get_course_name()

    def _get_course_name(self) -> tuple[str, int]:
        course_name = self.course_soup.get("id").split("-")
        curriculum = course_name[0]
        code = int(course_name[1])
        return (curriculum, code)

    def get_parsed_course(self) -> Course:
        """
        Takes a BeautifulSoup representation of a course and parses it into
        a Course object.
        """
        course_details = self.course_soup.find("h1")
        title = course_details.find("small").text
        units = course_details.find(class_="units").text.split("Units: ")[1]

        if ("-") in units:
            # units is a range
            units_range = units.split(" - ")
            units = (int(units_range[0]), int(units_range[1]))
        else:
            # units is a single digit
            units = int(units)

        description = self.course_soup.find("p").text

        sections = self.course_soup.find(class_="section-table").findChildren(
            "tr", recursive=False
        )
        num_sections = len(sections)

        return Course(
            self.subject,
            self.course_curriculum,
            self.course_code,
            title,
            description,
            num_sections,
            units,
        )

    def get_sections_soup(self, course_soup: BeautifulSoup) -> list[BeautifulSoup]:
        return course_soup.find(class_="section-table").findChildren(
            "tr", recursive=False
        )


class SectionParser:
    def __init__(
        self, section_soup: BeautifulSoup, course_curriculum: str, course_code: int
    ):
        self.section_soup = section_soup
        self.course_curriculum = course_curriculum
        self.course_code = course_code

    def get_parsed_section(self) -> Section:
        """
        Takes a BeautifulSoup representation of a section and returns a
        Section object.
        """
        data_columns = self.section_soup.find_all("td")

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
                num_on_waitlist = int(seats_info[1].replace("(", "").replace(")", ""))
            case other:
                raise KeyError("invalid availability status:", other)

        meeting_info = data_columns[4]

        if meeting_info.find(class_="weekdisplay") is not None:
            meeting_day_strs = (
                day.get("title").split(" - ")[0]
                for day in meeting_info.find_all("abbr")
                if "meet" in day.get("title")
            )
            meeting_days = list(map(MeetingDay.from_str, meeting_day_strs))

            meeting_time = list(meeting_info.strings)[-1].split("-")

            if meeting_time[0] == "TBD":
                start_time = None
                end_time = None
            else:
                start_time = meeting_time[0].strip()
                start_time = datetime.datetime.strptime(start_time, "%I:%M %p").time()

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
            self.course_curriculum,
            self.course_code,
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
            location,
        )


class Parser:
    def __init__(self, html_str: str, subject: str):
        self.html_parser = HTMLParser(html_str, subject)
        self.subject = subject

    def _get_course_parsers(self) -> Generator[CourseParser, None, None]:
        courses_soup = self.html_parser.get_courses_soup()
        for course in courses_soup:
            yield CourseParser(course, self.subject)

    def get_courses(self) -> Generator[Course, None, None]:
        course_parsers = self._get_course_parsers()
        for parser in course_parsers:
            yield parser.get_parsed_course()

    def _get_section_parsers(self) -> Generator[SectionParser, None, None]:
        course_parsers = self._get_course_parsers()
        for course_parser in course_parsers:
            sections = course_parser.get_sections_soup()
            for section in sections:
                yield SectionParser(
                    section, course_parser.course_curriculum, course_parser.course_code
                )

    def get_sections(self):
        section_parsers = self._get_section_parsers()
        for parser in section_parsers:
            yield parser.get_parsed_section()
