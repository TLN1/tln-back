from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Application


@dataclass
class ResponseContent:
    pass


@dataclass
class TokenResponse(ResponseContent):
    token: str


@dataclass
class ApplicationIdResponse(ResponseContent):
    application_id: int


@dataclass
class ApplicationResponse(ResponseContent):
    application: Application


@dataclass
class CoreResponse:
    status: Status = Status.OK
    response_content: ResponseContent = ResponseContent()
