from tests.util import assert_dicts_equals
from ncsu_courses._parsers import Parser


def test_course_parsing(expected_f22_csc_course_html, expected_f22_csc_course_dicts):
    """
    Tests course parsing functions against predefined html responses.
    """
    subject = "CSC - Computer Science"
    parser = Parser(expected_f22_csc_course_html, subject)

    parsed_courses_dicts = [course.to_dict() for course in parser.get_courses()]

    assert len(expected_f22_csc_course_dicts) == len(parsed_courses_dicts)

    for i in range(len(expected_f22_csc_course_dicts)):
        expected_course = expected_f22_csc_course_dicts[i]
        actual_course = parsed_courses_dicts[i]

        assert_dicts_equals(expected_course, actual_course)
