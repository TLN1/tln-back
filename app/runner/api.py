import uvicorn
from fastapi import Depends, FastAPI, Response

from app.core.application_context import InMemoryApplicationContext
from app.core.constants import STATUS_HTTP_MAPPING
from app.core.core import Core
from app.core.request import RequestRegister
from app.core.response import RegisterResponse, ResponseContent
from app.infra.repository.account import InMemoryRepositoryAccount
from app.infra.token import Token

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


def get_core() -> Core:
    account_repository = InMemoryRepositoryAccount()
    return Core(
        account_repository=account_repository,
        token_generator=Token.generate_token,
        application_context=InMemoryApplicationContext(
            account_repository=account_repository
        ),
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

    register_response = core.register(RequestRegister(username, password))
    response.status_code = STATUS_HTTP_MAPPING[register_response.status]
    return register_response.response_content
