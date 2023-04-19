import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response

from app.core.application_context import InMemoryApplicationContext
from app.core.constants import STATUS_HTTP_MAPPING
from app.core.core import Core
from app.core.request import RegisterRequest
from app.core.response import CoreResponse, ResponseContent
from app.infra.repository.account import InMemoryAccountRepository
from app.core.request import RequestRegister
from app.core.response import RegisterResponse, ResponseContent
from app.infra.repository.account import InMemoryRepositoryAccount
from app.infra.token import Token

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

in_memory_account_repository = InMemoryAccountRepository()
in_memory_application_context = InMemoryApplicationContext(
    account_repository=in_memory_account_repository
)


def get_core() -> Core:
    return Core(
        account_repository=in_memory_account_repository,
        token_generator=Token.generate_token,
        application_context=in_memory_application_context,
    )


def handle_response_status_code(
    response: Response, core_response: CoreResponse
) -> None:
    response.status_code = STATUS_HTTP_MAPPING[core_response.status]

    if response.status_code // 100 != 2:
        raise HTTPException(
            status_code=response.status_code, detail=core_response.message
        )


@app.post(
    "/register",
    responses={
        201: {},
        500: {},
    },
    response_model=RegisterResponse,
)
def register(
    response: Response, username: str, password: str, core: Core = Depends(get_core)
) -> ResponseContent:
    """
    - Registers user
    - Returns token for subsequent requests
    """

    register_response = core.register(RegisterRequest(username, password))
    handle_response_status_code(response, register_response)
    print(register_response.response_content)
    return register_response.response_content
