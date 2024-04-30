from unittest.mock import patch
from unittest.mock import MagicMock
from ..events.gestion_commands import (
    create_user,
    update_user,
    delete_user,
    create_contract,
    update_contract,
    add_user_to_event,
)
from click.testing import CliRunner
import pytest
from ..database import Base, sessionLocal, engine


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
def test_create_user(mock_prompt, db_test):
    mock_prompt.side_effect = ["test@mail.com", "mdptest", "support"]
    runner = CliRunner()
    result = runner.invoke(create_user)
    assert (
        "Utilisateur 'test@mail.com' créé avec succès avec le département 'support'."
        in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_update_user(mock_prompt, db_test):
    mock_prompt.side_effect = ["2", "test2@mail.com", "mdptest", "support"]
    runner = CliRunner()
    result = runner.invoke(update_user)
    assert (
        "Informations de l'utilisateur avec l'ID 2 mises à jour avec succès."
        in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_fail_update_user(mock_prompt, db_test):
    mock_prompt.side_effect = ["5", "test2@mail.com", "mdptest", "support"]
    runner = CliRunner()
    result = runner.invoke(update_user)
    assert "L'utilisateur avec l'ID 5 n'existe pas." in result.output


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
@patch("click.confirm", return_value=True)
def test_delete_user(mock_confirm, mock_prompt, db_test):
    mock_prompt.side_effect = ["2"]
    runner = CliRunner()
    result = runner.invoke(delete_user)
    assert "L'utilisateur avec l'ID 2 a été supprimé avec succès." in result.output


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_create_contract(mock_prompt, db_test):
    mock_prompt.side_effect = ["1", "500", "250", False]
    runner = CliRunner()
    result = runner.invoke(create_contract)
    assert "Contrat crée avec succès." in result.output


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_fail_create_contract(mock_prompt, db_test):
    mock_prompt.side_effect = ["4", "500", "250", False]
    runner = CliRunner()
    result = runner.invoke(create_contract)
    assert "Le client 4 n'existe pas." in result.output


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_update_contract(mock_prompt, db_test):
    mock_prompt.side_effect = ["1", "1", "500", "250", False]
    runner = CliRunner()
    result = runner.invoke(update_contract)
    assert (
        "Informations du contrat avec l'ID 1 mises à jour avec succès." in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_add_user_to_event(mock_prompt, db_test):
    mock_prompt.side_effect = ["1", "1"]
    runner = CliRunner()
    result = runner.invoke(add_user_to_event)
    assert (
        "Le collaborateur de l'événement avec l'ID 1 mises à jour avec succès."
        in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("click.prompt")
def test_fail_add_user_to_event(mock_prompt, db_test):
    mock_prompt.side_effect = ["3", "1"]
    runner = CliRunner()
    result = runner.invoke(add_user_to_event)
    assert "L'événement avec l'ID 3 n'existe pas." in result.output

    mock_prompt.side_effect = ["1", "4"]
    result = runner.invoke(add_user_to_event)
    assert "L'utilisateur support 4 n'existe pas." in result.output
