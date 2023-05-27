from enum import Enum

from pydantic import BaseModel


class Account(BaseModel):
    id: int
    username: str
    password: str


class Requirement(BaseModel):
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


class Benefit(BaseModel):
    pass


class Application(BaseModel):
    id: int
    location: JobLocation
    job_type: JobType
    experience_level: ExperienceLevel
    requirements: list[Requirement]
    benefits: list[Benefit]
    views: int

    def update(
        self,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> None:
        self.location = location
        self.job_type = job_type
        self.experience_level = experience_level
        self.requirements = requirements
        self.benefits = benefits


class ApplicationId(BaseModel):
    application_id: int


class Token(BaseModel):
    token: str
