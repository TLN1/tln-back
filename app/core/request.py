from dataclasses import dataclass


@dataclass
class RegisterRequest:
    username: str
    password: str


@dataclass
class LoginRequest:
    username: str
    password: str
