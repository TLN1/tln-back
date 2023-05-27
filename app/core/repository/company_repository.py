from typing import Optional, Protocol

from app.core.models import Company, Industry, OrganizationSize


class ICompanyRepository(Protocol):
    def get_company(self, company_id: int) -> Optional[Company]:
        pass

    def create_company(
        self,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> Optional[Company]:
        pass

    def update_company(
        self,
        company_id: int,
        name: str,
        website: str,
        industry: Industry,
        organization_size: OrganizationSize,
    ) -> Optional[Company]:
        pass

    def delete_company(self, company_id: int) -> bool:
        pass
