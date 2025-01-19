from typing import Generator
from ncsu_courses._api import API
from ncsu_courses.datatypes import CatalogCourse


def get_catalog_courses(
    subject: str, career: str | None = None
) -> Generator[CatalogCourse, None, None]:
    """
    Returns a generator of parsed catalog courses of the given subject
    """

    catalog_courses = API.get_catalog_courses_by_subject(subject, career)

    for course_code, course in catalog_courses.items():
        parsed_course = CatalogCourse(
            course_code,
            course["course_id"],
            course["course_title"],
            int(course["units_min"]),
            int(course["units_max"]),
            int(course["offer_number"]),
            course["acad_org"],
            course["subject"],
            int(course["catalog_number"]),
            course["descr_formal"],
            course["dept_link"],
            course["reqs"],
            course["course_name"],
            course["descr"],
            course["attrs"],
            course["semesters"],
            course["cross_crse"],
        )

        yield parsed_course
