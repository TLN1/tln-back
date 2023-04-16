from dataclasses import dataclass

from app.core.request import RequestRegister
from app.core.response import ResponseRegister


@dataclass
class Core:
    def register(self, request: RequestRegister) -> ResponseRegister:
        return ResponseRegister()
