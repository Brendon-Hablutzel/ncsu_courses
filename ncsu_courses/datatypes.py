from dataclasses import dataclass
from enum import Enum
import datetime


@dataclass
class Course:
    """
    Represents a parsed course.
    """

    subject: str
    course_curriculum: str
    course_code: int
    title: str
    description: str
    num_sections: int
    units: int | tuple[int, int]

    def to_dict(self) -> dict:
        """
        Returns the given course's dictionary representation.
        """
        return {
            "subject": self.subject,
            "course_curriculum": self.course_curriculum,
            "course_code": self.course_code,
            "title": self.title,
            "description": self.description,
            "num_sections": self.num_sections,
            "units": self.units
            if type(self.units) is int
            else [self.units[0], self.units[1]],
        }


class MeetingDay(Enum):
    """
    Represents a possible meeting day for a section.
    """

    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

    def from_str(string):
        """
        Takes a string meeting day and converts it to its enum variant.
        """
        match string:
            case "Monday":
                return MeetingDay.Monday
            case "Tuesday":
                return MeetingDay.Tuesday
            case "Wednesday":
                return MeetingDay.Wednesday
            case "Thursday":
                return MeetingDay.Thursday
            case "Friday":
                return MeetingDay.Friday
            case "Saturday":
                return MeetingDay.Saturday
            case "Sunday":
                return MeetingDay.Sunday
            case other:
                raise AttributeError(
                    "could not find corresponding meeting day for:", other
                )


class Component(Enum):
    """
    Represents a section component type, such as Lab or Lecture.
    """

    Lecture = "Lec"
    Lab = "Lab"
    Research = "Res"
    Project = "Pro"
    Independent = "Ind"
    Thesis = "The"  # uncertain

    def from_str(string):
        """
        Takes a string section component and returns its corresponding
        enum variant.
        """
        match string:
            case "Lec":
                return Component.Lecture
            case "Lab":
                return Component.Lab
            case "Res":
                return Component.Research
            case "Pro":
                return Component.Project
            case "Ind":
                return Component.Independent
            case "The":
                return Component.Thesis
            case other:
                raise AttributeError(
                    "could not find corresponding course component for:", other
                )


class Availability(Enum):
    """
    Represents the availability for a section, such as Open or Closed.
    """

    Closed = "Closed"
    Waitlist = "Waitlist"
    Open = "Open"
    Reserved = "Reserved"

    def from_str(string):
        """
        Takes a string availability status and returns its corresponding
        enum variant.
        """
        match string:
            case "Closed":
                return Availability.Closed
            case "Waitlist":
                return Availability.Waitlist
            case "Open":
                return Availability.Open
            case "Reserved":
                return Availability.Reserved
            case other:
                raise AttributeError(
                    "could not find corresponding availability for:", other
                )


@dataclass
class Section:
    """
    Represents a parsed section of a course.
    """

    course_curriculum: str
    course_code: int
    section: str
    component: Component
    instructor_name: str
    open_seats: int
    total_seats: int
    availability_status: Availability
    num_on_waitlist: int | None
    start_time: datetime.time | None
    end_time: datetime.time | None
    start_date: datetime.date
    end_date: datetime.date
    meeting_days: list[MeetingDay]
    location: str | None  # change this to an enum later?

    def to_dict(self) -> dict:
        """
        Returns the given section's dictionary representation.
        """
        return {
            "curriculum": self.course_curriculum,
            "code": self.course_code,
            "section": self.section,
            "component": self.component,
            "instructor_name": self.instructor_name,
            "open_seats": self.open_seats,
            "total_seats": self.total_seats,
            "availability_status": self.availability_status,
            "num_on_waitlist": self.num_on_waitlist,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "meeting_days": self.meeting_days,
            "location": self.location,
        }
