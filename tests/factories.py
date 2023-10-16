import factory

from models import User
from tests.session import TestSession


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = TestSession
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    email: str = factory.Sequence(lambda n: f"{n}@test.com")
    password = "test_password"
    is_admin = False

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs["password"] = User.hash_password(kwargs["password"])
        return super()._create(model_class, *args, **kwargs)
