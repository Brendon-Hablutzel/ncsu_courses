from ncsu_courses.courses import _course_html_to_courses_soup, _parse_course_html_soup
from tests.util import assert_dicts_equals


def test_course_parsing(expected_f22_csc_course_html, expected_f22_csc_course_dicts):
    '''
    Tests course parsing functions against predefined html responses.
    '''
    courses_soup = _course_html_to_courses_soup(expected_f22_csc_course_html)
    parsed_courses = map(lambda course_soup: _parse_course_html_soup(
        "CSC - Computer Science", course_soup), courses_soup)
    parsed_courses_dicts = [course.to_dict() for course in parsed_courses]

    assert len(expected_f22_csc_course_dicts) == len(parsed_courses_dicts)

    for i in range(len(expected_f22_csc_course_dicts)):
        expected_course = expected_f22_csc_course_dicts[i]
        actual_course = parsed_courses_dicts[i]

        assert_dicts_equals(expected_course, actual_course)
