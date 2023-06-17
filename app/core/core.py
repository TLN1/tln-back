from dataclasses import dataclass

from pydantic import BaseModel

from app.core.constants import Status
from app.core.models import Account, ApplicationId, Industry, OrganizationSize
from app.core.requests import (
    ApplicationInteractionRequest,
    CreateApplicationRequest,
    DeleteApplicationRequest,
    GetApplicationRequest,
    RegisterRequest,
    SetupUserRequest,
    UpdateApplicationRequest,
)
from app.core.responses import CoreResponse
from app.core.services.account import AccountService
from app.core.services.application import ApplicationService
from app.core.services.company import CompanyService
from app.core.services.user import UserService


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

        status, user = self.user_service.create_user(account)

        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(
            status=status, response_content=account  # login_response.response_content
        )

    def get_user(self, username: str) -> CoreResponse:
        status, user = self.user_service.get_user(username=username)
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=user)

    def update_user(self, request: SetupUserRequest) -> CoreResponse:
        status, user = self.user_service.update_user(
            account=request.account, user=request.user
        )
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=user)

    def create_application(self, request: CreateApplicationRequest) -> CoreResponse:
        get_company_response = self.get_company(request.company_id)
        if get_company_response.status != Status.OK:
            return get_company_response

        status, application = self.application_service.create_application(
            account=request.account,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            requirements=request.requirements,
            benefits=request.benefits,
        )

        if status != Status.OK or application is None:
            return CoreResponse(status)

        self.account_service.link_application(
            account=request.account, application=application
        )
        self.company_service.link_application(
            company_id=request.company_id, application=application
        )

        return CoreResponse(
            status=status, response_content=ApplicationId(application_id=application.id)
        )

    def get_application(self, request: GetApplicationRequest) -> CoreResponse:
        status, application = self.application_service.get_application(id=request.id)

        application_response = BaseModel() if application is None else application
        return CoreResponse(status=status, response_content=application_response)

    def update_application(self, request: UpdateApplicationRequest) -> CoreResponse:
        status, application = self.application_service.update_application(
            account=request.account,
            id=request.id,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            requirements=request.requirements,
            benefits=request.benefits,
        )

        if status != Status.OK or application is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=application)

    def application_interaction(
        self, request: ApplicationInteractionRequest
    ) -> CoreResponse:
        status = self.application_service.application_interaction(
            account=request.account, id=request.id
        )
        return CoreResponse(status=status)

    def delete_application(self, request: DeleteApplicationRequest) -> CoreResponse:
        status = self.application_service.delete_application(
            account=request.account, id=request.id
        )
        return CoreResponse(status=status)

    def create_company(
        self,
        account: Account,
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

        status = self.account_service.link_company(account=account, company=company)
        # TODO: what if error occurred during linking company with account

        return CoreResponse(status=status, response_content=company)

    def get_company(self, company_id: int) -> CoreResponse:
        company = self.company_service.get_company(company_id=company_id)
        if company is None:
            return CoreResponse(status=Status.COMPANY_DOES_NOT_EXIST)

        return CoreResponse(status=Status.OK, response_content=company)

    def update_company(
        self,
        account: Account,
        company_id: int,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> CoreResponse:
        status, company = self.company_service.update_company(
            account=account,
            company_id=company_id,
            name=name,
            website=website,
            industry=industry,
            organization_size=organization_size,
        )
        if company is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=company)

    def delete_company(self, account: Account, company_id: int) -> CoreResponse:
        status = self.company_service.delete_company(
            account=account, company_id=company_id
        )
        return CoreResponse(status=status)
