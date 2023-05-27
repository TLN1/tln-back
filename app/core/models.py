from dataclasses import dataclass

from pydantic import BaseModel, Field


class Industry(BaseModel):
    name: str
    description: str


class JobType(BaseModel):
    name: str
    description: str


class EmploymentType(BaseModel):
    name: str
    description: str


class ExperienceLevel(BaseModel):
    name: str
    description: str


class Preference(BaseModel):
    industry: list[Industry] = Field(default_factory=list)
    job_type: list[JobType] = Field(default_factory=list)
    employment_type: list[EmploymentType] = Field(default_factory=list)
    experience_level: list[ExperienceLevel] = Field(default_factory=list)


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


@dataclass
class Account:
    id: int
    username: str
    password: str
