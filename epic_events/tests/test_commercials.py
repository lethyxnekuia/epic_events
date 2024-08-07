from unittest.mock import patch
from ..events.commercial_commands import (
    create_client,
    create_event,
    update_client,
    update_contract,
)
from click.testing import CliRunner
import pytest
from ..models import User, Contract, Client
from datetime import datetime


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.commercial_commands.session", autospec=True)
@patch("click.prompt")
def test_create_client(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    mock_prompt.side_effect = ["Jean test", "jeantest@test.com", "0345151515", "Test"]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(create_client, obj=ctx_mock)
    assert "Client creé avec succès" in result.output


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.commercial_commands.session", autospec=True)
@patch("click.prompt")
def test_update_client(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    client = Client(
        full_name="Jean test",
        email="jeantest@test.com",
        phone="0345151515",
        company_name="Test",
        creation_date=datetime.now(),
        last_contact_date=datetime.now(),
        commercial_contact_id=1
    )

    mock_session.query.return_value.filter_by.return_value.first.return_value = client
    mock_prompt.side_effect = [
        "1",
        "Jean test 2",
        "jeantest@test.com",
        "0345151515",
        "Test",
    ]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(update_client, obj=ctx_mock)
    assert "Le client avec l'ID 1 mises à jour avec succès." in result.output


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.commercial_commands.session", autospec=True)
@patch("click.prompt")
def test_success_create_event(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    user = User(id=1, email="test1@example.com", password="password", department="support")

    contract = Contract(
        client_id="1", total_amount="500", remaining_amount="200", is_signed=True
    )
    client = Client(
        full_name="Jean test",
        email="jeantest@test.com",
        phone="0345151515",
        company_name="Test",
        creation_date=datetime.now(),
        last_contact_date=datetime.now(),
        commercial_contact_id=1
    )

    mock_session.query.return_value.filter_by.return_value.first.side_effect = [contract, client, user]
    mock_prompt.side_effect = [
        "1",
        "1",
        "Test",
        "Lieu",
        "50",
        "test",
        "2025-06-06",
        "2025-06-07",
    ]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(create_event, obj=ctx_mock)
    assert "Evenement creé avec succès" in result.output


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.commercial_commands.session", autospec=True)
@patch("click.prompt")
def test_fail_create_event(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    mock_prompt.side_effect = [
        "2",
        "1",
        "Test",
        "Lieu",
        "50",
        "test",
        "2025-06-06",
        "2025-06-07",
    ]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(create_event, obj=ctx_mock)
    assert "Le contrat 2 n'existe pas." in result.output

    contract = Contract(client_id="1", total_amount="500", remaining_amount="200")
    mock_session.query.return_value.filter_by.return_value.first.return_value = contract
    mock_prompt.side_effect = [
        "2",
        "1",
        "Test",
        "Lieu",
        "50",
        "test",
        "2025-06-06",
        "2025-06-07",
    ]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(create_event, obj=ctx_mock)
    assert "Le contrat 2 n'est pas signé." in result.output

    contract = Contract(
        client_id="1",
        total_amount="500",
        remaining_amount="200",
        is_signed=True
    )
    client = Client(
        full_name="Jean test",
        email="jeantest@test.com",
        phone="0345151515",
        company_name="Test",
        creation_date=datetime.now(),
        last_contact_date=datetime.now(),
        commercial_contact_id=1
    )
    mock_session.query.return_value.filter_by.return_value.first.side_effect = [
        contract,
        client,
        None
    ]
    mock_prompt.side_effect = [
        "1",
        "3",
        "Test",
        "Lieu",
        "50",
        "test",
        "2025-06-06",
        "2025-06-07",
    ]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(create_event, obj=ctx_mock)
    assert "L'utilisateur support 3 n'existe pas." in result.output


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.commercial_commands.session", autospec=True)
@patch("click.prompt")
def test_update_contract(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    contract = Contract(
        client_id="1",
        total_amount="500",
        remaining_amount="200",
        is_signed=True
    )
    client = Client(
        full_name="Jean test",
        email="jeantest@test.com",
        phone="0345151515",
        company_name="Test",
        creation_date=datetime.now(),
        last_contact_date=datetime.now(),
        commercial_contact_id=1
    )
    mock_session.query.return_value.filter_by.return_value.first.side_effect = [
        contract,
        client,
        None
    ]
    mock_prompt.side_effect = ["1", "600", "300", True]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(update_contract, obj=ctx_mock)
    assert (
        "Informations du contrat avec l'ID 1 mises à jour avec succès." in result.output
    )


@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.commercial_commands.session", autospec=True)
@patch("click.prompt")
def test_fail_update_contract(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    mock_prompt.side_effect = ["3", "600", "300", True]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(update_contract, obj=ctx_mock)
    assert "Le contrat avec l'ID 3 n'existe pas." in result.output
