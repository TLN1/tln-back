from dataclasses import dataclass

from app.core.constants import Status


@dataclass
class ResponseGeneric:
    status_code: int = Status.OK


@dataclass
class ResponseRegister(ResponseGeneric):
    pass
