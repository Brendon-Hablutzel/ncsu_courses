from bs4 import BeautifulSoup
from dataclasses import dataclass
from ncsu_courses.util import get_course_html, course_html_to_courses_soup
from ncsu_courses.term import Term
from typing import Generator


@dataclass
class Course:
    '''
    Represents a parsed course.
    '''
    subject: str
    course_curriculum: str
    course_code: int
    title: str
    description: str
    num_sections: int
    units: int | tuple[int, int]


def parse_course_html_soup(subject: str, course_soup: BeautifulSoup) -> Course:
    '''
    Takes a BeautifulSoup representation of a course and parses it into
    a Course object.
    '''
    course_info = course_soup.get("id").split("-")
    curriculum = course_info[0]
    code = int(course_info[1])

    course_details = course_soup.find("h1")
    title = course_details.find("small").text
    units = course_details.find(class_="units").text.split("Units: ")[1]

    if ("-") in units:
        # units is a range
        units_range = units.split(" - ")
        units = (int(units_range[0]), int(units_range[1]))
    else:
        # units is a single digit
        units = int(units)

    description = course_soup.find("p").text

    sections = course_soup.find(
        class_="section-table").findChildren("tr", recursive=False)
    num_sections = len(sections)

    return Course(
        subject,
        curriculum,
        code,
        title,
        description,
        num_sections,
        units
    )


def get_courses(subject: str, term: Term, course_code: int | None = None) -> Generator[Course, None, None]:
    '''
    Returns a generator of parsed courses of the given subject during
    the given term.
    '''

    course_html = get_course_html(subject, term, course_code)

    courses_soup = course_html_to_courses_soup(course_html)

    for course in courses_soup:
        yield parse_course_html_soup(subject, course)
