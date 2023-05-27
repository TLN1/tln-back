from typing import Any

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response

from app.core.constants import STATUS_HTTP_MAPPING
from app.core.core import Core
from app.core.models import (
    Application,
    ApplicationId,
    Benefit,
    ExperienceLevel,
    JobLocation,
    JobType,
    Requirement,
    Token,
)
from app.core.requests import (
    CreateApplicationRequest,
    GetApplicationRequest,
    LoginRequest,
    LogoutRequest,
    RegisterRequest,
)
from app.core.responses import CoreResponse
from app.core.services.account_service import AccountService
from app.core.services.application_service import ApplicationService
from app.infra.application_context import InMemoryApplicationContext
from app.infra.repository.account_repository import InMemoryAccountRepository
from app.infra.repository.application_repository import InMemoryApplicationRepository
from app.infra.token_generator import TokenGenerator

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

in_memory_account_repository = InMemoryAccountRepository()
in_memory_application_repository = InMemoryApplicationRepository()

in_memory_application_context = InMemoryApplicationContext()


def get_core() -> Core:
    return Core(
        account_service=AccountService(
            account_repository=in_memory_account_repository,
            application_context=in_memory_application_context,
            token_generator=TokenGenerator.generate_token,
        ),
        application_service=ApplicationService(
            application_repository=in_memory_application_repository,
            application_context=in_memory_application_context,
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


# TODO document response codes for other api methods
@app.post(
    "/register",
    responses={
        201: {},
        500: {},
    },
    response_model=Token,
)
def register(
    response: Response, username: str, password: str, core: Core = Depends(get_core)
) -> Any:
    """
    - Registers user
    - Returns token for subsequent requests
    """

    token_response = core.register(RegisterRequest(username, password))
    handle_response_status_code(response, token_response)
    return token_response.response_content


@app.post("/login", response_model=Token)
def login(
    response: Response, username: str, password: str, core: Core = Depends(get_core)
) -> Any:
    """
    - Logs user in
    - Returns token for subsequent requests
    """

    token_response = core.login(LoginRequest(username, password))
    handle_response_status_code(response, token_response)
    return token_response.response_content


@app.post("/logout")
def logout(response: Response, token: str, core: Core = Depends(get_core)) -> Any:
    logout_response = core.logout(LogoutRequest(token))
    handle_response_status_code(response, logout_response)
    return logout_response.response_content


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
) -> Any:
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


@app.get("/application/get", response_model=Application)
def get_application(
    response: Response, token: str, application_id: int, core: Core = Depends(get_core)
) -> Any:
    get_application_response = core.get_application(
        GetApplicationRequest(token=token, id=application_id)
    )

    handle_response_status_code(response, get_application_response)
    return get_application_response.response_content
