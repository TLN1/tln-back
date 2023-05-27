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
        )

        self.applications[application_id] = application
        return application

    def get_application(self, id: int) -> Optional[Application]:
        return self.applications.get(id)

    def _next_id(self) -> int:
        self._application_id += 1
        return self._application_id
