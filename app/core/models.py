from dataclasses import dataclass


@dataclass
class Account:
    id: int
    username: str
    password: str
