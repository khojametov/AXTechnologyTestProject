from calendar import timegm
from datetime import datetime, timedelta
from typing import Any, Sequence

from jose import JWTError, jwt
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from common.types import ClaimsDict
from config.settings import settings
from models import User


class TokenError(Exception):
    pass


class Token:
    """
    Base class for managing tokens with limited lifespan
    """

    is_abstract: bool = True

    token_type: str = "access"
    lifetime: timedelta = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    algorithm: str = settings.ALGORITHM
    algorithm_options: dict[str, bool | int] = {}

    required_claims: Sequence[str] = ("email",)

    signing_key: str = settings.SECRET_KEY
    error_message = "Token is invalid or expired"

    _token_string: str
    _claims: dict[str, Any]
    user: User

    def __init__(
        self,
        *,
        user: User,
        token_string: str,
        claims: ClaimsDict,
    ):
        self.user = user
        self._token_string = token_string
        self._claims = claims

    def __getitem__(self, key: str) -> Any:
        return self._claims[key]

    def __contains__(self, key: str) -> bool:
        return key in self._claims

    def __str__(self) -> str:
        return self._token_string

    @property
    def claims(self) -> ClaimsDict:
        return self._claims

    @classmethod
    def _calculate_exp(cls, from_time: datetime) -> int:
        dt = from_time + cls.lifetime
        return timegm(dt.utctimetuple())

    @classmethod
    def _encode(cls, claims: ClaimsDict) -> str:
        """
        Return token with claims
        """
        return jwt.encode(claims, cls.signing_key, algorithm=cls.algorithm)

    @classmethod
    def _decode(cls, token_string: str) -> ClaimsDict:
        """
        Decode claims from token_string
        """
        try:
            return jwt.decode(
                token_string,
                cls.signing_key,
                algorithms=cls.algorithm,
                options={"require_exp": True} | cls.algorithm_options,
            )
        except JWTError:
            raise TokenError(cls.error_message)

    @classmethod
    def _verify_claims(cls, claims: ClaimsDict) -> None:
        """
        Ensures all necessary claims are present and have correct values
        """
        try:
            token_type = claims["token_type"]
        except KeyError:
            raise TokenError(cls.error_message)

        if token_type != cls.token_type:
            raise TokenError(cls.error_message)

        required_claims = cls.required_claims or []
        for claim in required_claims:
            if claim not in claims:
                raise TokenError(cls.error_message)

    @classmethod
    def _get_user(cls, claims: ClaimsDict, session: Session) -> User:
        query = select(User).where(User.email == claims["email"])
        try:
            return session.exec(query).one()
        except NoResultFound:
            raise TokenError(cls.error_message)

    @classmethod
    def _get_claims(cls, *, user: User, from_time: datetime) -> ClaimsDict:
        return {
            "token_type": cls.token_type,
            "exp": cls._calculate_exp(from_time),
            "email": user.email,
        }

    @classmethod
    def get_user_from_string(cls, token_string: str, session: Session) -> User:
        """
        Verify given token_string and return user
        """
        claims = cls._decode(token_string)
        cls._verify_claims(claims)
        user = cls._get_user(claims, session)

        return user

    @classmethod
    def generate_token_for_user(
        cls, user: User, instantiation_time: datetime | None = None
    ) -> str:
        """
        Generate token for a given user
        """
        instantiation_time = instantiation_time or datetime.utcnow()
        claims = cls._get_claims(user=user, from_time=instantiation_time)
        token_string = cls._encode(claims)

        return token_string
