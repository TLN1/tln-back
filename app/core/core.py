from dataclasses import dataclass

from pydantic import BaseModel

from app.core.constants import Status
from app.core.models import ApplicationId, Industry, OrganizationSize, InMemoryToken
from app.core.requests import (
    ApplicationInteractionRequest,
    CreateApplicationRequest,
    DeleteApplicationRequest,
    GetApplicationRequest,
    GetUserRequest,
    LoginRequest,
    LogoutRequest,
    RegisterRequest,
    SetupUserRequest,
    UpdateApplicationRequest,
)
from app.core.responses import CoreResponse, UserResponse
from app.core.services.account_service import AccountService
from app.core.services.application_service import ApplicationService
from app.core.services.company_service import CompanyService
from app.core.services.user_service import UserService


# TODO remove authorization from service classes
@dataclass
class Core:
    account_service: AccountService
    company_service: CompanyService
    application_service: ApplicationService
    user_service: UserService

    def register(self, request: RegisterRequest) -> CoreResponse:
        status, account = self.account_service.register(
            username=request.username, password=request.password
        )

        if status != Status.OK or account is None:
            return CoreResponse(status=status)

        login_response = self.login(
            request=LoginRequest(username=account.username, password=account.password)
        )

        if login_response.status != Status.OK:
            return CoreResponse(status=status)

        status, _ = self.user_service.create_user(username=request.username)

        if status != Status.OK:
            return CoreResponse(status=status)

        return CoreResponse(
            status=status, response_content=login_response.response_content
        )

    def login(self, request: LoginRequest) -> CoreResponse:
        status, token = self.account_service.login(
            username=request.username, password=request.password
        )

        token_response = BaseModel() if token is None else InMemoryToken(token=token)
        return CoreResponse(status=status, response_content=token_response)

    def logout(self, request: LogoutRequest) -> CoreResponse:
        status = self.account_service.logout(token=request.token)
        return CoreResponse(status=status)

    def get_user(self, request: GetUserRequest) -> CoreResponse:
        status, user = self.user_service.get_user(username=request.username)
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=UserResponse(user=user))

    def update_user(self, request: SetupUserRequest) -> CoreResponse:
        status, user = self.user_service.update_user(
            username=request.username, user=request.user
        )
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=UserResponse(user=user))

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

    def create_company(
        self,
        token: str,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> CoreResponse:
        status, company = self.company_service.create_company(
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
        )

        if company is None:
            return CoreResponse(status=status)

        status = self.account_service.link_company(token=token, company=company)
        # TODO: what if error occurred during linking company with account

        return CoreResponse(status=status, response_content=company)

    def get_company(self, company_id: int) -> CoreResponse:
        company = self.company_service.get_company(company_id=company_id)
        if company is None:
            return CoreResponse(status=Status.COMPANY_DOES_NOT_EXIST)

        return CoreResponse(status=Status.OK, response_content=company)

    def update_company(
        self,
        token: str,
        company_id: int,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> CoreResponse:
        status, account = self.account_service.get_account(token=token)
        if account is None:
            return CoreResponse(status=status)
        if company_id not in account.companies:
            return CoreResponse(status=Status.COMPANY_DOES_NOT_EXIST)

        status, company = self.company_service.update_company(
            token=token,
            company_id=company_id,
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
        )
        if company is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=company)

    def delete_company(self, token: str, company_id: int) -> CoreResponse:
        status, account = self.account_service.get_account(token=token)
        if account is None:
            return CoreResponse(status=status)

        if company_id not in account.companies:
            return CoreResponse(status=Status.COMPANY_DOES_NOT_EXIST)

        status = self.company_service.delete_company(company_id=company_id)
        return CoreResponse(status=status)
