from sqlalchemy import (
    create_engine,
    Column,
    Table,
    Integer,
)
from sqlalchemy.orm import declared_attr, sessionmaker, scoped_session, DeclarativeBase
from config import settings as config


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        """ """
        return f"blog_{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self)


engine = create_engine(
    url=config.database_url_psycopg,
    echo=config.DB_ECHO,
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
