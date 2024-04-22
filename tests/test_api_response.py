from bs4 import BeautifulSoup
from ncsu_courses.util import get_course_html
from ncsu_courses.term import Term, Session
from ncsu_courses.subjects import get_all_subjects


def test_api_course_equals_expected(expected_f22_csc_course_html):
    '''
    Assert that the API's returned course HTML equals the expected
    course HTML.
    '''
    expected_course_soup = BeautifulSoup(
        expected_f22_csc_course_html, 'html.parser')

    subject = "CSC - Computer Science"
    term = Term(22, Session.Fall)
    course_html = get_course_html(subject, term)
    course_soup = BeautifulSoup(course_html, 'html.parser')

    assert expected_course_soup.encode_contents() == course_soup.encode_contents()


def test_api_subjects_equals_expected(expected_f22_subjects):
    '''
    Assert that the API's returned array of subjects equals the expected
    array of subjects.
    '''
    term = Term(22, Session.Fall)
    f22_subjects = str(get_all_subjects(term))

    assert expected_f22_subjects == f22_subjects
