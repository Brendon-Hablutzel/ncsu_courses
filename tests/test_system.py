from ncsu_courses.courses import get_courses
from ncsu_courses.term import Term, Session
from tests.util import assert_dicts_equals


def test_get_courses(expected_f22_csc_course_dicts):
    subject = "CSC - Computer Science"
    term = Term(22, Session.Fall)
    courses = [course.to_dict() for course in get_courses(subject, term)]

    assert len(expected_f22_csc_course_dicts) == len(courses)

    for i in range(len(expected_f22_csc_course_dicts)):
        expected_dict = expected_f22_csc_course_dicts[i]
        actual_dict = courses[i]

        assert_dicts_equals(expected_dict, actual_dict)
