from sqlalchemy import Column, INT, VARCHAR, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.settings import settings


class Base(DeclarativeBase):
    engine = create_engine(url=settings.DB_URL.unicode_string())
    session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'user'

    id = Column(INT, primary_key=True)
    email = Column(VARCHAR(128), unique=True, nullable=False)
    hashed_password = Column(VARCHAR(256), nullable=False)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return f'{self.email}'

    @property
    def identity(self) -> int:
        return self.id
