from ncsu_courses.term import Term, Session
from ncsu_courses._api import API
from bs4 import BeautifulSoup
import pytest


@pytest.mark.skip(reason="flaky test, relies on a network call")
def test_api_course_equals_expected(expected_f22_csc_course_html):
    '''
    Assert that the API's returned course HTML equals the expected
    course HTML.
    '''
    subject = "CSC - Computer Science"
    term = Term(22, Session.Fall)
    course_html = API.get_course_html(subject, term)

    course_soup = BeautifulSoup(course_html, 'html.parser')

    expected_course_soup = BeautifulSoup(
        expected_f22_csc_course_html, 'html.parser')

    # asserting equality is quicker between BeautifulSoup encoded objects than
    # the raw html strings
    assert expected_course_soup.encode_contents() == course_soup.encode_contents()


@pytest.mark.skip(reason="flaky test, relies on a network call")
def test_api_subjects_equals_expected(expected_f22_subjects):
    '''
    Assert that the API's returned array of subjects equals the expected
    array of subjects.
    '''
    term = Term(22, Session.Fall)
    f22_subjects = str(API.get_subjects_list(term))

    assert expected_f22_subjects == f22_subjects
