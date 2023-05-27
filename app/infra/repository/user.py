from dataclasses import dataclass, field
from typing import Optional

from app.core.models import User
from app.core.repository.user_repository import IUserRepository


@dataclass
class InMemoryUserRepository(IUserRepository):
    users: dict[str, User] = field(default_factory=dict)

    def create_user(self, username: str) -> Optional[User]:
        self.users[username] = User(username=username)
        return self.users[username]

    def update_user(self, username: str, user: User) -> Optional[User]:
        user = User(
            username=username,
            skills=user.skills,
            preference=user.preference,
            education=user.education,
            experience=user.experience,
        )
        self.users[username] = user
        return user

    def get_user(self, username: str) -> User:
        return self.users[username]

    def has_user(self, username: str) -> bool:
        return username in self.users
