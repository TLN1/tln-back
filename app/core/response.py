from dataclasses import dataclass

from app.core.constants import Status


@dataclass
class ResponseContent:
    pass


@dataclass
class RegisterResponse(ResponseContent):
    pass


@dataclass
class CoreResponse:
    message: str = ""
    status: Status = Status.OK
    response_content: ResponseContent = ResponseContent()
