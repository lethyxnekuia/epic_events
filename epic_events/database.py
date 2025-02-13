import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def sessionLocal(engine_test=None):
    if engine_test:
        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_test))
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
