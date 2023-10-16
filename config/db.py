from sqlmodel import Session, create_engine

from config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
    connect_args={"check_same_thread": False},
)


def get_session():
    with Session(engine) as session:
        yield session
