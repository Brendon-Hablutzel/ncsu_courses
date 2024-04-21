import requests
from term import Term

SUBJECTS_URL = "https://webappprd.acs.ncsu.edu/php/coursecat/subjects.php"


def get_all_subjects(term: Term) -> list[str]:
    '''
    Gets all the subjects that courses may be listed under for the
    current term.
    '''

    payload = {
        "strm": term.get_term_number()
    }

    res = requests.post(SUBJECTS_URL, data=payload).json()

    subjects = res['subj_js']

    return subjects
