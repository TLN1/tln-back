from dataclasses import dataclass


@dataclass
class Account:
    username: str
    password: str
    token: str
    token_is_valid: bool
