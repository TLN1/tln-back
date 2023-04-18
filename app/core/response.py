from dataclasses import dataclass

from app.core.constants import Status


@dataclass
class ResponseContent:
    pass


@dataclass
class RegisterResponse(ResponseContent):
    token: str


@dataclass
class CoreResponse:
    message: str = ""
    status: Status = Status.OK
    response_content: ResponseContent = ResponseContent()
