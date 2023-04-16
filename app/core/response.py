from dataclasses import dataclass, field

from app.core.constants import Status


@dataclass
class ResponseGeneric:
    status_code: int = field(default=Status.STATUS_CODE_DEFAULT)


@dataclass
class ResponseRegister(ResponseGeneric):
    pass
