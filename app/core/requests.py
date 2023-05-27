from dataclasses import dataclass

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
class LogoutRequest:
    token: str


@dataclass
class CreateCompanyRequest:
    token: str
    name: str
    website: str
    industry: Industry
    organization_size: OrganizationSize
