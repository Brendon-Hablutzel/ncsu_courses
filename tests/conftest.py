import pytest
import os
import json


@pytest.fixture
def test_resources_dir(request):
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "resources")


@pytest.fixture
def expected_f22_csc_course_html(test_resources_dir):
    data_filepath = os.path.join(test_resources_dir, "f22_csc_courses.html")
    with open(data_filepath, "r") as f:
        return f.read()


@pytest.fixture
def expected_f22_csc_course_dicts(test_resources_dir):
    data_filepath = os.path.join(test_resources_dir, "f22_csc_courses.json")
    with open(data_filepath, "r") as f:
        obj = json.load(f)
    return obj['courses']


@pytest.fixture
def expected_f22_subjects(test_resources_dir):
    data_filepath = os.path.join(test_resources_dir, "f22_subjects.txt")
    with open(data_filepath, "r") as f:
        return f.read()
