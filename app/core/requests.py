from dataclasses import dataclass, field

from app.core.models import Benefit, ExperienceLevel, JobLocation, JobType, Requirement

# TODO maybe implement builder pattern for building requests
from app.core.models import Industry, OrganizationSize


@dataclass
class RegisterRequest:
    username: str
    password: str


@dataclass
class LoginRequest:
    username: str
    password: str


@dataclass
class TokenRequest:
    token: str


@dataclass
class LogoutRequest(TokenRequest):
    pass


@dataclass
class CreateApplicationRequest(TokenRequest):
    location: JobLocation = JobLocation.ON_SITE
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.JUNIOR
    requirements: list[Requirement] = field(default_factory=list)
    benefits: list[Benefit] = field(default_factory=list)


@dataclass
class UpdateApplicationRequest(TokenRequest):
    id: int
    location: JobLocation = JobLocation.ON_SITE
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.JUNIOR
    requirements: list[Requirement] = field(default_factory=list)
    benefits: list[Benefit] = field(default_factory=list)


@dataclass
class GetApplicationRequest(TokenRequest):
    id: int


@dataclass
class ApplicationInteractionRequest(TokenRequest):
    id: int


@dataclass
class DeleteApplicationRequest(TokenRequest):
    id: int


@dataclass
class CreateCompanyRequest:
    token: str
    name: str
    website: str
    industry: Industry
    organization_size: OrganizationSize
