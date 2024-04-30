from unittest.mock import patch
from ..users.users_commands import login
from click.testing import CliRunner
import pytest
from ..database import Base, sessionLocal, engine
from ..models import User


def init_db():
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db_test():
    try:
        init_db()
        SessionLocal = sessionLocal(True)
        yield SessionLocal
    finally:
        SessionLocal().close()
        Base.metadata.drop_all(bind=engine)


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_login_success(mock_prompt, db_test):
    session = db_test()

    user = User(email="test@example.com", password="password", department="commercial")
    session.add(user)
    session.commit()

    mock_prompt.side_effect = ["test@example.com", "password"]

    runner = CliRunner()
    result = runner.invoke(login)

    assert "Connecté avec succès" in result.output


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_login_fail(mock_prompt, db_test):

    mock_prompt.side_effect = ["test@example.com", "password1"]

    runner = CliRunner()
    result = runner.invoke(login)

    assert "Email ou mot de passe incorrect." in result.output
