from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass
class Account:
    id: int
    username: str
    password: str


@dataclass
class Requirement:
    pass


class JobLocation(Enum):
    ON_SITE = "on-site"
    REMOTE = "remote"


class JobType(Enum):
    PART_TIME = "part-time"
    FULL_TIME = "full-time"


class ExperienceLevel(Enum):
    INTERN = "intern"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"


@dataclass
class Benefit:
    pass


@dataclass
class Application:
    id: int
    location: JobLocation = JobLocation.ON_SITE
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.JUNIOR
    requirements: list[Requirement] = field(default_factory=list)
    benefits: list[Benefit] = field(default_factory=list)
