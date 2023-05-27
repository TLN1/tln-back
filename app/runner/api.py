import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel

from app.core.constants import STATUS_HTTP_MAPPING
from app.core.core import Core
from app.core.models import Education, Experience, Preference, Skill, User
from app.core.requests import (
    GetUserRequest,
    LoginRequest,
    LogoutRequest,
    RegisterRequest,
    SetupUserRequest,
)
from app.core.responses import CoreResponse, TokenResponse, UserResponse
from app.core.services.account_service import AccountService
from app.core.services.user_service import UserService
from app.infra.application_context import InMemoryApplicationContext
from app.infra.repository.account import InMemoryAccountRepository
from app.infra.repository.user import InMemoryUserRepository
from app.infra.token import Token

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

in_memory_account_repository = InMemoryAccountRepository()
in_memory_user_repository = InMemoryUserRepository()
in_memory_application_context = InMemoryApplicationContext()


def get_core() -> Core:
    return Core(
        account_service=AccountService(
            account_repository=in_memory_account_repository,
            application_context=in_memory_application_context,
            token_generator=Token.generate_token,
        ),
        user_service=UserService(
            user_repository=in_memory_user_repository,
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
