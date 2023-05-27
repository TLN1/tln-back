from dataclasses import dataclass, field
from typing import Optional

from app.core.models import (
    Application,
    Benefit,
    ExperienceLevel,
    JobLocation,
    JobType,
    Requirement,
)
from app.core.repository.application_repository import IApplicationRepository


@dataclass
class InMemoryApplicationRepository(IApplicationRepository):
    applications: dict[int, Application] = field(default_factory=dict)
    _application_id: int = 0

    def _next_id(self) -> int:
        self._application_id += 1
        return self._application_id

    def create_application(
        self,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> Optional[Application]:
        application_id = self._next_id()
        application = Application(
            id=application_id,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            requirements=requirements,
            benefits=benefits,
            views=0,
        )

        self.applications[application_id] = application
        return application

    def get_application(self, id: int) -> Optional[Application]:
        return self.applications.get(id)

    def has_application(self, id: int) -> bool:
        return self.get_application(id=id) is not None

    def update_application(
        self,
        id: int,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> bool:
        if not self.has_application(id=id):
            return False

        self.applications[id].update(
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            requirements=requirements,
            benefits=benefits,
        )
        return True

    def application_interaction(self, id: int) -> bool:
        if not self.has_application(id=id):
            return False

        self.applications[id].views += 1
        return True