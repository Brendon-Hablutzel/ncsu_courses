from ncsu_courses.term import Term, Session


def test_term_numbers():
    """
    Use the expected term values from the API and compare them to the computed values
    """
    expected_spring_2015 = 2151
    spring_2015 = Term(15, Session.Spring).get_term_number()
    assert expected_spring_2015 == spring_2015

    expected_summer1_2011 = 2116
    summer1_2011 = Term(11, Session.Summer1).get_term_number()
    assert expected_summer1_2011 == summer1_2011

    expected_summer2_2020 = 2207
    summer2_2020 = Term(20, Session.Summer2).get_term_number()
    assert expected_summer2_2020 == summer2_2020

    expected_fall_2023 = 2238
    fall_2023 = Term(23, Session.Fall).get_term_number()
    assert expected_fall_2023 == fall_2023
