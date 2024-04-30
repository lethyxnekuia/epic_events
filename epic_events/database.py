import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)


def sessionLocal(is_test=False):
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
