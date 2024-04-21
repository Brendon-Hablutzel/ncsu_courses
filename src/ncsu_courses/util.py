import requests
from ncsu_courses.term import Term

COURSES_URL = "https://webappprd.acs.ncsu.edu/php/coursecat/search.php"


def get_course_html(subject: str, term: Term) -> str:
    '''
    Returns the API's generated html containing all of the courses and sections
    for the given subject during the given term. Term number is generated using
    the get_term_number(year, session) function.
    '''
    payload = {
        "term": term.get_term_number(),
        "subject": subject,
        "course-inequality": "=",
        "course-number": "",
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
