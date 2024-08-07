from unittest.mock import patch
from ..users.users_commands import login
from click.testing import CliRunner
import pytest
from ..models import User
import bcrypt


@pytest.mark.usefixtures("db_test")
@patch("epic_events.users.users_commands.session", autospec=True)
@patch("click.prompt")
def test_login_success(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test

    password_plain = "password"
    hashed_password = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt())

    mock_session.query.return_value.filter_by.return_value.first.return_value = User(
        email="test@example.com",
        password=hashed_password,
        department="commercial",
        id=1
    )

    mock_prompt.side_effect = ["test@example.com", password_plain]

    user = User(
        email="test@example.com",
        password=hashed_password,
        department="commercial"
    )
    db_test.add(user)
    db_test.commit()

    runner = CliRunner()
    result = runner.invoke(login)

    assert "Connecté avec succès" in result.output


@pytest.mark.usefixtures("db_test")
@patch("epic_events.users.users_commands.session", autospec=True)
@patch("click.prompt")
def test_login_fail(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    mock_prompt.side_effect = ["test@example.com", "wrongpassword"]

    runner = CliRunner()
    result = runner.invoke(login)

    assert "Email ou mot de passe incorrect." in result.output
