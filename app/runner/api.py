import uvicorn
from fastapi import Depends, FastAPI, Response

from app.core.constants import STATUS_HTTP_MAPPING
from app.core.core import Core
from app.core.request import RequestRegister

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


def get_core() -> Core:
    return Core()


@app.post(
    "/register",
    responses={
        201: {},
        500: {},
    },
)
def register(
    response: Response, username: str, password: str, core: Core = Depends(get_core)
) -> None:
    """
    - Registers user
    - Returns token for subsequent requests
    """

    register_response = core.register(RequestRegister(username, password))
    response.status_code = STATUS_HTTP_MAPPING[register_response.status_code]
