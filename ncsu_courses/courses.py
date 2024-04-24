from ncsu_courses.datatypes import Section
from ncsu_courses.term import Term
from typing import Generator
from ncsu_courses._api import API
from ncsu_courses._parsers import Parser
from ncsu_courses.datatypes import Course


def get_courses(subject: str, term: Term, course_code: int | None = None) -> Generator[Course, None, None]:
    '''
    Returns a generator of parsed courses of the given subject during
    the given term.
    '''

    course_html = API.get_course_html(subject, term, course_code)

    parser = Parser(course_html, subject)

    courses = parser.get_courses()
    for course in courses:
        yield course


def get_sections(subject: str, term: Term, course_code: int | None = None) -> Generator[Section, None, None]:
    '''
    Returns a generator of parsed sections of all courses associated with 
    the given subject during the given term.
    '''

    course_html = API.get_course_html(subject, term, course_code)

    parser = Parser(course_html, subject)
    sections = parser.get_sections()
    for section in sections:
        yield section
