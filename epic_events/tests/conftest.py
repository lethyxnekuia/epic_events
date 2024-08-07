import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from epic_events.database import Base, sessionLocal

DATABASE_URL = "sqlite:///./dbtest.db"
engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def db_test():
    """Fixture pour configurer et nettoyer la base de données de test."""
    init_db()
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        SessionLocal.remove()
        Base.metadata.drop_all(bind=engine)