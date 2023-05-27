from dataclasses import dataclass
from typing import Optional

from app.core.application_context import IApplicationContext
from app.core.constants import Status
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
class ApplicationService:
    application_repository: IApplicationRepository
    application_context: IApplicationContext

    def create_application(
        self,
        token: str,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> tuple[Status, Optional[int]]:
        username = self.application_context.get_account(token=token)
        if username is None or not self.application_context.is_user_logged_in(
            username=username
        ):
            return Status.USER_NOT_LOGGED_IN, None

        application = self.application_repository.create_application(
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            requirements=requirements,
            benefits=benefits,
        )

        if application is None:
            return Status.APPLICATION_CREATE_ERROR, None

        return Status.OK, application.id

    def get_application(
        self, token: str, id: int
    ) -> tuple[Status, Optional[Application]]:
        username = self.application_context.get_account(token=token)
        if username is None or not self.application_context.is_user_logged_in(
            username=username
        ):
            return Status.USER_NOT_LOGGED_IN, None

        application = self.application_repository.get_application(id=id)
        if application is None:
            return Status.APPLICATION_DOES_NOT_EXIST, None

        return Status.OK, application

    def update_application(
        self,
        token: str,
        id: int,
        location: JobLocation,
        job_type: JobType,
        experience_level: ExperienceLevel,
        requirements: list[Requirement],
        benefits: list[Benefit],
    ) -> Status:
        username = self.application_context.get_account(token=token)
        if username is None or not self.application_context.is_user_logged_in(
            username=username
        ):
            return Status.USER_NOT_LOGGED_IN

        if not self.application_repository.has_application(id=id):
            return Status.APPLICATION_DOES_NOT_EXIST

        if not self.application_repository.update_application(
            id=id,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            requirements=requirements,
            benefits=benefits,
        ):
            return Status.APPLICATION_UPDATE_ERROR

        return Status.OK

    def application_interaction(self, token: str, id: int) -> Status:
        username = self.application_context.get_account(token=token)
        if username is None or not self.application_context.is_user_logged_in(
            username=username
        ):
            return Status.USER_NOT_LOGGED_IN

        if not self.application_repository.has_application(id=id):
            return Status.APPLICATION_DOES_NOT_EXIST

        if not self.application_repository.application_interaction(id=id):
            return Status.APPLICATION_INTERACTION_ERROR

        return Status.OK
