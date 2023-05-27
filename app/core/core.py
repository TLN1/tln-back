from dataclasses import dataclass

from pydantic import BaseModel

from app.core.constants import Status
from app.core.models import ApplicationId, Token
from app.core.requests import (
    ApplicationInteractionRequest,
    CreateApplicationRequest,
    DeleteApplicationRequest,
    GetApplicationRequest,
    LoginRequest,
    LogoutRequest,
    RegisterRequest,
    UpdateApplicationRequest,
)
from app.core.responses import CoreResponse
from app.core.services.account_service import AccountService
from app.core.services.application_service import ApplicationService


# TODO remove authorization from service classes
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

        token_response = BaseModel() if token is None else Token(token=token)
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
            BaseModel()
            if application_id is None
            else ApplicationId(application_id=application_id)
        )
        return CoreResponse(status=status, response_content=application_id_response)

    def get_application(self, request: GetApplicationRequest) -> CoreResponse:
        status, application = self.application_service.get_application(
            token=request.token, id=request.id
        )

        application_response = BaseModel() if application is None else application
        return CoreResponse(status=status, response_content=application_response)

    def update_application(self, request: UpdateApplicationRequest) -> CoreResponse:
        status = self.application_service.update_application(
            token=request.token,
            id=request.id,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            requirements=request.requirements,
            benefits=request.benefits,
        )
        return CoreResponse(status=status)

    def application_interaction(
        self, request: ApplicationInteractionRequest
    ) -> CoreResponse:
        status = self.application_service.application_interaction(
            token=request.token, id=request.id
        )
        return CoreResponse(status=status)

    def delete_application(self, request: DeleteApplicationRequest) -> CoreResponse:
        status = self.application_service.delete_application(
            token=request.token, id=request.id
        )
        return CoreResponse(status=status)
