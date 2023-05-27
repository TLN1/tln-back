import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel

from app.core.constants import STATUS_HTTP_MAPPING
from app.core.core import Core
from app.core.models import Company, Industry, OrganizationSize
from app.core.requests import LoginRequest, LogoutRequest, RegisterRequest
from app.core.responses import CoreResponse, TokenResponse
from app.core.services.account_service import AccountService
from app.core.services.company_service import CompanyService
from app.infra.application_context import InMemoryApplicationContext
from app.infra.repository.account import InMemoryAccountRepository
from app.infra.repository.company import InMemoryCompanyRepository
from app.infra.token import Token

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

in_memory_account_repository = InMemoryAccountRepository()
in_memory_application_context = InMemoryApplicationContext()
in_memory_company_repository = InMemoryCompanyRepository()


def get_core() -> Core:
    return Core(
        account_service=AccountService(
            account_repository=in_memory_account_repository,
            application_context=in_memory_application_context,
            token_generator=Token.generate_token,
        ),
        company_service=CompanyService(
            company_repository=in_memory_company_repository,
        ),
    )


def handle_response_status_code(
    response: Response, core_response: CoreResponse
) -> None:
    response.status_code = STATUS_HTTP_MAPPING[core_response.status]

    if response.status_code // 100 != 2:
        raise HTTPException(
            status_code=response.status_code, detail=core_response.status.value
        )


@app.post(
    "/register",
    responses={
        201: {},
        500: {},
    },
    response_model=TokenResponse,
)
def register(
    response: Response, username: str, password: str, core: Core = Depends(get_core)
) -> BaseModel:
    """
    - Registers user
    - Returns token for subsequent requests
    """

    token_response = core.register(RegisterRequest(username, password))
    handle_response_status_code(response, token_response)
    return token_response.response_content


@app.post("/login", response_model=TokenResponse)
def login(
    response: Response, username: str, password: str, core: Core = Depends(get_core)
) -> BaseModel:
    """
    - Logs user in
    - Returns token for subsequent requests
    """

    token_response = core.login(LoginRequest(username, password))
    handle_response_status_code(response, token_response)
    return token_response.response_content


@app.post("/logout", response_model=BaseModel)
def logout(response: Response, token: str, core: Core = Depends(get_core)) -> BaseModel:
    """
    - Logs user out
    """

    logout_response = core.logout(LogoutRequest(token))
    handle_response_status_code(response, logout_response)
    return logout_response.response_content


@app.post(
    "/company",
    responses={
        200: {},
        401: {},
        500: {},
    },
    response_model=Company,
)
def create_company(
    response: Response,
    token: str,
    name: str,
    website: str,
    industry: Industry,
    organization_size: OrganizationSize,
    core: Core = Depends(get_core),
) -> BaseModel:
    """
    - Registers company
    - Returns created company
    """

    company_response = core.create_company(
        token=token,
        name=name,
        website=website,
        industry=industry,
        organization_size=organization_size,
    )
    handle_response_status_code(response, company_response)
    return company_response.response_content


# TODO: authenticate user
@app.get(
    "/company/{company_id}",
    responses={
        200: {},
        404: {},
    },
    response_model=Company,
)
def get_company(
    response: Response,
    token: str,
    company_id: int,
    core: Core = Depends(get_core),
) -> BaseModel:
    company_response = core.get_company(company_id=company_id)
    handle_response_status_code(response, company_response)
    return company_response.response_content


@app.put(
    "/company/{company_id}",
    responses={200: {}, 404: {}, 500: {}},
    response_model=Company,
)
def update_company(
    response: Response,
    token: str,
    company_id: int,
    name: str,
    website: str,
    industry: Industry,
    organization_size: OrganizationSize,
    core: Core = Depends(get_core),
) -> BaseModel:
    company_response = core.update_company(
        token=token,
        company_id=company_id,
        name=name,
        website=website,
        industry=industry,
        organization_size=organization_size,
    )
    handle_response_status_code(response, company_response)

    return company_response.response_content


@app.delete(
    "/company/{company_id}",
    responses={200: {}, 404: {}, 500: {}},
)
def delete_company(
    response: Response, token: str, company_id: int, core: Core = Depends(get_core)
) -> None:
    delete_response = core.delete_company(token=token, company_id=company_id)
    handle_response_status_code(response, delete_response)
