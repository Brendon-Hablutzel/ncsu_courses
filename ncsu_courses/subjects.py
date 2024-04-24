import requests
from ncsu_courses.term import Term
from ncsu_courses._api import API

SUBJECTS_URL = "https://webappprd.acs.ncsu.edu/php/coursecat/subjects.php"


def get_all_subjects(term: Term) -> list[str]:
    '''
    Gets all the subjects that courses may be listed under for the
    current term.
    '''

    return API.get_subjects_list(term)
