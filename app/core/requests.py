from dataclasses import dataclass

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
