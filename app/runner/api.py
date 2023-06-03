from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.application_context import IApplicationContext
from app.core.constants import STATUS_HTTP_MAPPING
from app.core.core import Core
from app.core.models import (
    Application,
    ApplicationId,
    Benefit,
    Company,
    Education,
    Experience,
    ExperienceLevel,
    Industry,
    JobLocation,
    JobType,
    OrganizationSize,
    Preference,
    Requirement,
    Skill,
    InMemoryToken,
    User, Token, Account,
)
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
from app.infra.application_context import InMemoryApplicationContext, InMemoryOauthApplicationContext
from app.infra.auth_utils import pwd_context, oauth2_scheme
from app.infra.repository.account_repository import InMemoryAccountRepository
from app.infra.repository.application_repository import InMemoryApplicationRepository
from app.infra.repository.company import InMemoryCompanyRepository
from app.infra.repository.user import InMemoryUserRepository
from app.infra.token_generator import TokenGenerator

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

in_memory_account_repository = InMemoryAccountRepository()
in_memory_application_repository = InMemoryApplicationRepository()
in_memory_user_repository = InMemoryUserRepository()
in_memory_application_context = InMemoryApplicationContext()
in_memory_company_repository = InMemoryCompanyRepository()
in_memory_oauth_application_context = InMemoryOauthApplicationContext(
    account_repository=in_memory_account_repository,
    hash_verifier=pwd_context.verify)


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


def get_application_context() -> IApplicationContext:
    return in_memory_oauth_application_context


def get_core() -> Core:
    return Core(
        account_service=AccountService(
            account_repository=in_memory_account_repository,
            application_context=in_memory_application_context,
            token_generator=TokenGenerator.generate_token,
            hash_function=pwd_context.hash
        ),
        application_service=ApplicationService(
            application_repository=in_memory_application_repository,
            application_context=in_memory_application_context,
        ),
        user_service=UserService(
            user_repository=in_memory_user_repository,
            application_context=in_memory_application_context,
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


@app.get("/users/me")
async def read_users_me(
        # current_user: Annotated[User, Depends(get_current_user)]):
        token: Annotated[str, Depends(oauth2_scheme)],
        application_context: IApplicationContext = Depends(get_application_context)):
    return await application_context.get_current_user(token)


@app.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        application_context: IApplicationContext = Depends(get_application_context)
):
    user = application_context.authenticate_user(form_data.username, form_data.password)
    access_token = application_context.create_access_token(account=user)

    return {"access_token": access_token, "token_type": "bearer"}


# TODO document response codes for other api methods
@app.post(
    "/register",
    responses={
        201: {},
        500: {},
    },
    response_model=Account,
)
def register(
    response: Response, username: str, password: str, core: Core = Depends(get_core)
) -> BaseModel:
    """
    - Registers user
    - Returns token for subsequent requests
    """

    account_response = core.register(RegisterRequest(username, password))
    # account = application_context.authenticate_user(username=username, password=password)
    # token_response = application_context.create_access_token(account)
    handle_response_status_code(response, account_response)
    return account_response.response_content


@app.post("/login", response_model=InMemoryToken)
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


@app.post("/logout")
def logout(response: Response, token: str, core: Core = Depends(get_core)) -> BaseModel:
    logout_response = core.logout(LogoutRequest(token))
    handle_response_status_code(response, logout_response)
    return logout_response.response_content


@app.get("/user/{username}", response_model=UserResponse)
def get_user(
    response: Response, username: str, core: Core = Depends(get_core)
) -> BaseModel:
    get_user_response = core.get_user(GetUserRequest(username=username))
    handle_response_status_code(response, get_user_response)
    return get_user_response.response_content


@app.put("/user/{username}", response_model=UserResponse)
def update_user(
    response: Response,
    username: str,
    education: list[Education],
    skills: list[Skill],
    experience: list[Experience],
    preference: Preference,
    core: Core = Depends(get_core),
) -> BaseModel:
    setup_user_response = core.update_user(
        SetupUserRequest(
            username=username,
            user=User(
                username=username,
                education=education,
                skills=skills,
                experience=experience,
                preference=preference,
            ),
        )
    )
    handle_response_status_code(response, setup_user_response)
    return setup_user_response.response_content


@app.post("/application/create", response_model=ApplicationId)
def create_application(
    response: Response,
    token: str,
    location: JobLocation,
    job_type: JobType,
    experience_level: ExperienceLevel,
    requirements: list[Requirement],
    benefits: list[Benefit],
    core: Core = Depends(get_core),
) -> BaseModel:
    """
    - Creates application
    - Returns application id for subsequent requests
    """
    create_application_response = core.create_application(
        CreateApplicationRequest(
            token=token,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            requirements=requirements,
            benefits=benefits,
        )
    )

    handle_response_status_code(response, create_application_response)
    return create_application_response.response_content


@app.get("/application/get/{application_id}", response_model=Application)
def get_application(
    response: Response, application_id: int, token: str, core: Core = Depends(get_core)
) -> BaseModel:
    """
    - Obtains application with application id
    """
    get_application_response = core.get_application(
        GetApplicationRequest(token=token, id=application_id)
    )

    handle_response_status_code(response, get_application_response)
    return get_application_response.response_content


@app.put("/application/update/{application_id}")
def update_application(
    response: Response,
    application_id: int,
    token: str,
    location: JobLocation,
    job_type: JobType,
    experience_level: ExperienceLevel,
    requirements: list[Requirement],
    benefits: list[Benefit],
    core: Core = Depends(get_core),
) -> BaseModel:
    """
    - Update application
    """
    update_application_response = core.update_application(
        UpdateApplicationRequest(
            token=token,
            id=application_id,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            requirements=requirements,
            benefits=benefits,
        )
    )

    handle_response_status_code(response, update_application_response)
    return update_application_response.response_content


@app.put("/application/interaction/{application_id}")
def application_interaction(
    response: Response, application_id: int, token: str, core: Core = Depends(get_core)
) -> BaseModel:
    """
    - Saves interaction with application
    """
    application_interaction_response = core.application_interaction(
        ApplicationInteractionRequest(id=application_id, token=token)
    )

    handle_response_status_code(response, application_interaction_response)
    return application_interaction_response.response_content


@app.delete("/application/delete/{application_id}")
def delete_application(
    response: Response, application_id: int, token: str, core: Core = Depends(get_core)
) -> BaseModel:
    """
    - Deletes application
    """
    delete_application_response = core.delete_application(
        DeleteApplicationRequest(token=token, id=application_id)
    )

    handle_response_status_code(response, delete_application_response)
    return delete_application_response.response_content


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
