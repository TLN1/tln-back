from dataclasses import dataclass


@dataclass
class RequestRegister:
    username: str
    password: str
