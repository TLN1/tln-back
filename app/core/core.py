from dataclasses import dataclass

from app.core.constants import Status
from app.core.requests import (
    CreateApplicationRequest,
    GetApplicationRequest,
    LoginRequest,
    LogoutRequest,
    RegisterRequest,
)
from app.core.responses import (
    ApplicationIdResponse,
    ApplicationResponse,
    CoreResponse,
    ResponseContent,
    TokenResponse,
)
from app.core.services.account_service import AccountService
from app.core.services.application_service import ApplicationService


@dataclass
class Core:
    account_service: AccountService
    application_service: ApplicationService

    def register(self, request: RegisterRequest) -> CoreResponse:
        status, account = self.account_service.register(
            username=request.username, password=request.password
        )

        if status != Status.OK or account is None:
            return CoreResponse(status=status)

        return self.login(
            request=LoginRequest(username=account.username, password=account.password)
        )

    def login(self, request: LoginRequest) -> CoreResponse:
        status, token = self.account_service.login(
            username=request.username, password=request.password
        )

        token_response = (
            ResponseContent() if token is None else TokenResponse(token=token)
        )
        return CoreResponse(status=status, response_content=token_response)

    def logout(self, request: LogoutRequest) -> CoreResponse:
        status = self.account_service.logout(token=request.token)
        return CoreResponse(status=status)

    def create_application(self, request: CreateApplicationRequest) -> CoreResponse:
        status, application_id = self.application_service.create_application(
            token=request.token,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            requirements=request.requirements,
            benefits=request.benefits,
        )

        application_id_response = (
            ResponseContent()
            if application_id is None
            else ApplicationIdResponse(application_id=application_id)
        )
        return CoreResponse(status=status, response_content=application_id_response)

    def get_application(self, request: GetApplicationRequest) -> CoreResponse:
        status, application = self.application_service.get_application(
            token=request.token, id=request.id
        )

        application_response = (
            ResponseContent()
            if application is None
            else ApplicationResponse(application=application)
        )

        return CoreResponse(status=status, response_content=application_response)
