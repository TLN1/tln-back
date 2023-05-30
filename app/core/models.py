from enum import Enum

from pydantic import BaseModel, Field


class Industry(BaseModel):
    name: str
    description: str


class JobType2(BaseModel):
    name: str
    description: str


class EmploymentType2(BaseModel):
    name: str
    description: str


class ExperienceLevel2(BaseModel):
    name: str
    description: str


class Preference(BaseModel):
    industry: list[Industry] = Field(default_factory=list)
    job_type: list[JobType2] = Field(default_factory=list)
    employment_type: list[EmploymentType2] = Field(default_factory=list)
    experience_level: list[ExperienceLevel2] = Field(default_factory=list)


class Experience(BaseModel):
    name: str
    description: str


class Education(BaseModel):
    name: str
    description: str


class Skill(BaseModel):
    name: str
    description: str


class User(BaseModel):
    username: str
    education: list[Education] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    preference: Preference = Preference()

    def update(self,
               education: list[Education],
               skills: list[Skill],
               experience: list[Experience],
               preference: Preference
    ):
        self.education = education
        self.skills = skills
        self.experience = experience
        self.preference = preference


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
    views: int = 0

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
