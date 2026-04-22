import datetime

import pytest
from unittest.mock import MagicMock

from my_wallet.blueprints.statistics.forms import StatReportForm
from my_wallet.app import compose_app

from my_wallet.blueprints.statistics.custom_types import ReportData


@pytest.fixture
def config():
    config_ = {
        "POSTGRES_USER": "test",
        "POSTGRES_PASSWORD": "test",
        "POSTGRES_HOST": "test",
        "POSTGRES_PORT": "test",
        "POSTGRES_DBNAME": "test"
    }
    return config_

@pytest.fixture
def date_from():
    return datetime.date(2023, 1, 2)

@pytest.fixture
def date_to():
    return datetime.date(2023, 1, 1)

@pytest.fixture
def stat_report_type_choices():
    choices = [
        ('BIGGEST_EXPENSES', 'Biggest expenses'),
        ('EXPENSES_BY_WEEKDAY', 'Expenses by weekday'),
        ('EXPENSES_BY_WEEK', 'Expenses by week'),
        ('EXPENSES_BY_TYPE', 'Expenses by type'),
        ('WEEKLY_BALANCE', 'Weekly balance')
    ]
    return choices

@pytest.fixture
def report_display_format_choices():
    return [("HTML", "Html"), ("XLSX", "Xlsx"), ("PDF", "Pdf")]

@pytest.fixture
def report_data_inst():
    columns = ["Date", "Amount"]
    data = [
        ["01-01-2024", 100],
        ["02-01-2024", 50]
    ]
    return ReportData(columns=columns, data=data)

@pytest.fixture
def form_():
    return StatReportForm()

@pytest.fixture(autouse=True)
def _patch_external_clients(monkeypatch):
    monkeypatch.setattr("my_wallet.app.Client", MagicMock())
    monkeypatch.setattr("my_wallet.app.Mailgun", MagicMock())

@pytest.fixture
def app(_patch_external_clients):
    app = compose_app()
    app.config["TESTING"] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_session(app):
    def _install(rows):
        fake_exec = MagicMock()
        fake_exec.fetchall.return_value = rows
        app.session = MagicMock(execute=MagicMock(return_value=fake_exec))
        return app.session
    return _install
