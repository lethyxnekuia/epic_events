from unittest.mock import patch
from unittest.mock import MagicMock
from ..events.support_commands import (
    update_event,
)
from click.testing import CliRunner
import pytest
from ..models import Contract, Event



@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.support_commands.session", autospec=True)
@patch("click.prompt")
def test_update_event(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    contract = Contract(
        client_id="1", total_amount="500", remaining_amount="200", is_signed=True
    )
    db_test.add(contract)

    event = Event(
        name="test event",
        contract_id="1",
        support_contact_id="1",
    )
    db_test.add(event)
    db_test.commit()

    mock_session.query.return_value.filter_by.return_value.first.return_value = event

    mock_prompt.side_effect = [
        "1",
        "test name",
        "test location",
        "200",
        "test_notes",
        "2026-04-04",
        "2026-04-05"
    ]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(update_event, obj=ctx_mock)
    assert "L'événement avec l'ID 1 mises à jour avec succès." in result.output

@pytest.mark.usefixtures("db_test")
@patch("epic_events.events.support_commands.session", autospec=True)
@patch("click.prompt")
def test_fail_update_event(mock_prompt, mock_session, db_test):
    mock_session.return_value = db_test
    contract = Contract(
        client_id="1", total_amount="500", remaining_amount="200", is_signed=True
    )
    db_test.add(contract)

    event = Event(
        name="test event",
        contract_id="1",
        support_contact_id="1",
    )
    db_test.add(event)
    db_test.commit()

    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    mock_prompt.side_effect = [
        "23",
    ]
    ctx_mock = {"user_id": 1}
    runner = CliRunner()
    result = runner.invoke(update_event, obj=ctx_mock)
    assert "L'événement avec l'ID 23 n'existe pas." in result.output

    mock_session.query.return_value.filter_by.return_value.first.return_value = event

    mock_prompt.side_effect = [
        "1",
    ]
    ctx_mock = {"user_id": 4}
    runner = CliRunner()
    result = runner.invoke(update_event, obj=ctx_mock)
    assert "Vous n'etes pas responsable de cet événement" in result.output
