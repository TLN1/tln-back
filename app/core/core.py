from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Industry, OrganizationSize
from app.core.requests import LoginRequest, LogoutRequest, RegisterRequest
from app.core.responses import CoreResponse, TokenResponse
from app.core.services.account_service import AccountService
from app.core.services.company_service import CompanyService


@dataclass
class Core:
    account_service: AccountService
    company_service: CompanyService

    def register(self, request: RegisterRequest) -> CoreResponse:
        status, account = self.account_service.register(
            username=request.username, password=request.password
        )
        if status != Status.OK or account is None:
            return CoreResponse(status=status)

        status, token = self.account_service.login(
            username=account.username, password=account.password
        )
        if status != Status.OK or token is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=TokenResponse(token=token))

    def login(self, request: LoginRequest) -> CoreResponse:
        status, token = self.account_service.login(
            username=request.username, password=request.password
        )
        if status != Status.OK or token is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=TokenResponse(token=token))

    def logout(self, request: LogoutRequest) -> CoreResponse:
        status = self.account_service.logout(token=request.token)
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
