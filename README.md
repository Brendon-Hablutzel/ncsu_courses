# NCSU Courses

A Python library for getting data about NCSU's course offerings. Contains functionality for retrieving historical and current courses and their sections, including instructor, meeting information, seats, and more.

This library uses the same API that [this](https://webappprd.acs.ncsu.edu/php/coursecat/) website does.

## Courses

Use `ncsu_courses.courses.get_all_courses(subject, term)` to get all courses for a given subject during the given term. A course has data such as a curriculum and code, a description, title, etc.

## Sections

A section of a course is a specific instance of the course being offered during a certain term. A section contains information such as instructor, meeting days and times, meeting location, seats, etc.

## Subjects

Subjects represent broad areas of study. Each course's name begins with the letters of the subject that it belongs to (ex. CSC 111 is a Computer Science course because CSC represents the Computer Science subject). The `ncsu_courses.subjects.get_all_subjects(term)` function returns a list of all subjects that exist during the current term.

## Terms

A term is identified by a year and a session (Fall, Spring, Summer 1, or Summer 2). Use `ncsu_courses.term.Term` to represent a specific term. Terms are passed to the API as integers representing a combination of year and session, and the `Term` object handles this internally.