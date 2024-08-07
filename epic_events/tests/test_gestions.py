import os
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
from ..database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ..models import User, Event, Contract

DATABASE_URL = os.environ.get("DATABASE_URL_TEST")
engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db_test():
    init_db()
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
def test_create_user(mock_prompt, mock_session):
    mock_prompt.side_effect = ["test@mail.com", "mdptest", "support"]
    runner = CliRunner()
    result = runner.invoke(create_user)
    assert (
        "Utilisateur 'test@mail.com' créé avec succès avec le département 'support'."
        in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
def test_update_user(mock_prompt, mock_session):
    user = User(
        email="test@mail.com", password="mdptest2", department="support"
    )
    mock_session.query.return_value.filter_by.return_value.first.return_value = user
    mock_prompt.side_effect = ["2", "test2@mail.com", "mdptest", "support"]
    runner = CliRunner()
    result = runner.invoke(update_user)
    assert (
        "Informations de l'utilisateur avec l'ID 2 mises à jour avec succès."
        in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
def test_fail_update_user(mock_prompt, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    mock_prompt.side_effect = ["5", "test2@mail.com", "mdptest", "support"]
    runner = CliRunner()
    result = runner.invoke(update_user)
    assert "L'utilisateur avec l'ID 5 n'existe pas." in result.output


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
@patch("click.confirm")
def test_delete_user(mock_confirm, mock_prompt, mock_session):
    user = User(
        email="test@mail.com", password="mdptest2", department="support"
    )
    mock_session.query.return_value.filter_by.return_value.first.return_value = user
    mock_confirm.return_value = True
    mock_prompt.side_effect = ["2"]
    runner = CliRunner()
    result = runner.invoke(delete_user)
    assert "L'utilisateur avec l'ID 2 a été supprimé avec succès." in result.output


@pytest.mark.usefixtures("db_test")

@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
def test_create_contract(mock_prompt, mock_session):
    mock_prompt.side_effect = ["1", "500", "250", False]
    runner = CliRunner()
    result = runner.invoke(create_contract)
    assert "Contrat crée avec succès." in result.output


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
def test_fail_create_contract(mock_prompt, mock_session):
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    mock_prompt.side_effect = ["4", "500", "250", False]
    runner = CliRunner()
    result = runner.invoke(create_contract)
    assert "Le client 4 n'existe pas." in result.output


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
def test_update_contract(mock_prompt, mock_session):
    contract = Contract(
        client_id="1", total_amount="500", remaining_amount="200", is_signed=True
    )
    mock_session.query.return_value.filter_by.return_value.first.return_value = contract
    mock_prompt.side_effect = ["1", "1", "500", "250", False]
    runner = CliRunner()
    result = runner.invoke(update_contract)
    assert (
        "Informations du contrat avec l'ID 1 mises à jour avec succès." in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
def test_add_user_to_event(mock_prompt, mock_session):
    event = Event(
        name="test event",
        contract_id="1",
        support_contact_id="1",
    )
    user = User(
        email="test@mail.com", password="mdptest2", department="support"
    )
    mock_session.query.return_value.filter_by.return_value.first.side_effect = [event, user]
    mock_prompt.side_effect = ["1", "1"]
    runner = CliRunner()
    result = runner.invoke(add_user_to_event)
    assert (
        "Le collaborateur de l'événement avec l'ID 1 mises à jour avec succès."
        in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.gestion_commands.session", autospec=True)
@patch("click.prompt")
def test_fail_add_user_to_event(mock_prompt, mock_session):
    event = Event(
        name="test event",
        contract_id="1",
        support_contact_id="1",
    )
    mock_session.query.return_value.filter_by.return_value.first.side_effect = [None, event, None]
    mock_prompt.side_effect = ["3", "1"]
    runner = CliRunner()
    result = runner.invoke(add_user_to_event)
    assert "L'événement avec l'ID 3 n'existe pas." in result.output

    mock_prompt.side_effect = ["1", "4"]
    result = runner.invoke(add_user_to_event)
    assert "L'utilisateur support 4 n'existe pas." in result.output
