import requests
from ncsu_courses.term import Term

COURSES_URL = "https://webappprd.acs.ncsu.edu/php/coursecat/search.php"
SUBJECTS_URL = "https://webappprd.acs.ncsu.edu/php/coursecat/subjects.php"
CATALOG_URL = "https://webappprd.acs.ncsu.edu/php/coursecat/directory_search.php"


class API:
    @staticmethod
    def get_course_html(
        subject: str, term: Term, course_code: int | None = None
    ) -> str:
        """
        Returns the API's generated html containing all of the courses and sections
        for the given subject during the given term. Term number is generated using
        the get_term_number(year, session) function. If filtering for a specific course,
        use course_code, otherwise, leave it as None.
        """

        if course_code is None:
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
            "instructor-name": "",
            # below is a argument passed with requests made from the frontend,
            # but the API seems to work without it
            # "current_strm": 2248
        }

        res = requests.post(COURSES_URL, data=payload).json()
        html = res["html"]
        return html

    @staticmethod
    def get_subjects_list(term: Term) -> list[str]:
        """
        Gets all the subjects that courses may be listed under for the
        current term.
        """

        payload = {"strm": term.get_term_number()}

        res = requests.post(SUBJECTS_URL, data=payload).json()

        subjects = res["subj_js"]

        return subjects

    @staticmethod
    def get_catalog_courses_by_subject(
        subject: str, career: str | None = None
    ) -> list[dict]:
        """
        Returns a list of objects representing all of the courses in the catalog
        for the given subject. Career may be specified (UGRD = undergraduate)
        """

        payload = {"search_val": subject, "type": "subject", "career": career}

        res = requests.post(CATALOG_URL, data=payload).json()

        courses = res["courses"]
        return courses
