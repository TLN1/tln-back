from dataclasses import dataclass, field
from datetime import timedelta, datetime
from typing import Optional, Annotated, Callable

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from app.core.application_context import IApplicationContext
from app.core.models import Account, TokenData
from app.core.repository.account_repository import IAccountRepository
from app.infra.auth_utils import oauth2_scheme


@dataclass
class InMemoryApplicationContext(IApplicationContext):
    active_accounts: dict[str, str] = field(default_factory=dict)

    def is_user_logged_in(self, username: str) -> bool:
        for active_username in self.active_accounts.values():
            if active_username == username:
                return True

        return False

    def get_account(self, token: str) -> Optional[str]:
        return self.active_accounts.get(token)

    def login_user(self, username: str, token: str) -> None:
        self.active_accounts[token] = username

    def logout_user(self, token: str) -> None:
        del self.active_accounts[token]


# TODO: move secret key somewhere safe?
@dataclass
class InMemoryOauthApplicationContext(IApplicationContext):
    account_repository: IAccountRepository
    hash_verifier: Callable[[str, str], bool]
    secret_key: str = "1ac93dcf0709667ebc635b3547a76af1f824ca43646241cfb4640cf21b940112"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    def __verify_password(self, plain_password: str, hashed_password) -> bool:
        return self.hash_verifier(plain_password, hashed_password)
        # pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> Account:
        user = self.account_repository.get_account(username)
        authentication_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user is None:
            # return None
            raise authentication_exception
        if not self.__verify_password(password, user.password):
            # return None
            raise authentication_exception
        return user

    def create_access_token(self, account: Account) -> str:
        data: dict = {"sub": account.username}
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def get_current_user(self, token: str | None = Annotated[str, Depends(oauth2_scheme)]) -> Account:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.account_repository.get_account(token_data.username)
        if user is None:
            raise credentials_exception
        return user
