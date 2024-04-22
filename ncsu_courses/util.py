import requests
from ncsu_courses.term import Term
from bs4 import BeautifulSoup
from typing import Iterable

COURSES_URL = "https://webappprd.acs.ncsu.edu/php/coursecat/search.php"


def _get_course_html(subject: str, term: Term, course_code: int | None = None) -> str:
    '''
    Returns the API's generated html containing all of the courses and sections
    for the given subject during the given term. Term number is generated using
    the get_term_number(year, session) function. If filtering for a specific course,
    use course_code, otherwise, leave it as None.
    '''

    if course_code == None:
        course_code = ""
    else:
        course_code = str(course_code)

    payload = {
        "term": term.get_term_number(),
        "subject": subject,
        "course-inequality": "=",
        "course-number": course_code,
        "session": "",
        "start-time-inequality": "<=",
        "start-time": "",
        "end-time-inequality": "<=",
        "end-time": "",
        "instructor-name": ""
        # below is a argument passed with requests made from the frontend,
        # but the API seems to work without it
        # "current_strm": 2248
    }

    res = requests.post(COURSES_URL, data=payload).json()
    html = res['html']
    return html


def _course_html_to_courses_soup(html: str) -> Iterable[BeautifulSoup]:
    soup = BeautifulSoup(html, 'html.parser')

    return soup.find_all(class_="course")


def _course_soup_to_sections_soup(course_soup: BeautifulSoup) -> Iterable[BeautifulSoup]:
    sections = course_soup.find(
        class_="section-table").findChildren("tr", recursive=False)
    return sections
