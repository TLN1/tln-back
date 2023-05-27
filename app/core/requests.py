from dataclasses import dataclass

from app.core.models import User

# TODO maybe implement builder pattern for building requests


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
class GetUserRequest:
    username: str


@dataclass
class SetupUserRequest:
    username: str
    user: User
