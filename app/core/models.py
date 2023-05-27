from dataclasses import dataclass, field
from enum import Enum

from pydantic import BaseModel

# TODO: ADD VALUES


class Industry(Enum):
    SOFTWARE_ENGINEERING = "Software Engineering"


# TODO: ADD VALUES
class OrganizationSize(Enum):
    SMALL = "1-10 employees"


class Company(BaseModel):
    id: int
    name: str
    website: str
    industry: Industry
    organization_size: OrganizationSize


@dataclass
class Account:
    id: int
    username: str
    password: str
    companies: list[int] = field(default_factory=list)

    def link_company(self, company: Company) -> None:
        self.companies.append(company.id)
