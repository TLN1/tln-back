import uvicorn
from fastapi import FastAPI, Depends
from fastapi.openapi.models import Response

from app.core.core import Core

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


def get_core() -> Core:
    return Core()


@app.post(
    "/users",
    responses={
        201: {},
        500: {},
    },
)
def register_user(response: Response,
                  core: Core = Depends(get_core)) -> None:
    """
    - Registers user
    """

    response.status_code = 200
