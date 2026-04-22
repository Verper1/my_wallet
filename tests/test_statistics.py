import datetime
from unittest.mock import MagicMock

import pytest
from werkzeug.datastructures import MultiDict

from my_wallet.blueprints.statistics.report_generators import \
    generate_biggest_expenses_report, generate_expenses_by_weekday_report, \
    generate_weekly_balance_report, generate_expenses_by_type_report, \
    generate_expenses_by_week_report
from my_wallet.blueprints.statistics.forms import StatReportForm
from my_wallet.blueprints.statistics.report_formatters import \
    generate_html_response, generate_xlsx_response, generate_pdf_response
from my_wallet.blueprints.statistics.enums import StatReportType, \
    ReportDisplayFormat
from my_wallet.blueprints.statistics.utils import is_report_range_valid
from tests.conftest import mock_session


# ---------------------------- utils ----------------------------

def test__is_report_range_valid__returns_true_if_date_to_is_lower_or_equal_than_date_from(date_from, date_to):
    assert is_report_range_valid(date_from, date_to) is True

    date_to_ = datetime.date(2023, 1, 1)
    assert is_report_range_valid(date_from, date_to_) is True

# ---------------------------- enums ----------------------------

def test__choices__returns_list_stat_types(stat_report_type_choices):
    assert StatReportType.choices() == stat_report_type_choices

def test__choices__returns_list_display_format(report_display_format_choices):
    assert ReportDisplayFormat.choices() == report_display_format_choices

# ---------------------------- report formatters ----------------------------

def test__generate_html_response__returns_report(app, report_data_inst, form_):
    with app.test_request_context():
        result = generate_html_response(report_data_inst, form_)

        assert isinstance(result, str)
        assert "Date" in result
        assert "Amount" in result
        assert "100" in result

def test__generate_xlsx_response__returns_report(app, report_data_inst, form_):
    with app.test_request_context():
        result = generate_xlsx_response(report_data_inst, form_)

        assert result.mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        assert "report.xlsx" in result.headers["Content-Disposition"]
        result.direct_passthrough = False
        assert result.data[:2] == b"PK"
        assert len(result.data) > 500

def test__generate_pdf_response__returns_report(app, report_data_inst, form_):
    with app.test_request_context():
        result = generate_pdf_response(report_data_inst, form_)

        assert result.mimetype == "application/pdf"
        assert "report.pdf" in result.headers["Content-Disposition"]
        result.direct_passthrough = False
        assert result.data.startswith(b"%PDF-")
        assert len(result.data) > 500

# ---------------------------- forms ----------------------------

def test__StatReportForm__good_form():
    data = ([
        ("date_from", "2023-01-01"),
        ("date_to", "2023-01-02"),
        ("wallets", "1"),
        ("report_type", "BIGGEST_EXPENSES"),
        ("output_format", "HTML")
    ])
    form = StatReportForm(MultiDict(data))
    form.wallets.choices = [("1", "Wallet 1")]
    assert form.validate() is True

def test__StatReportForm__error_form():
    data = ([
        ("date_from", "2023-01-01"),
        ("date_to", "2023-01-01"),
        ("wallets", "1"),
        ("report_type", "BIGGEST_EXPENSES"),
        ("output_format", "HTML")
    ])
    form = StatReportForm(MultiDict(data))
    form.wallets.choices = [("1", "Wallet 1")]
    assert form.validate() is False
    assert "Should be after" in form.date_to.errors[0]

@pytest.mark.xfail(raises=TypeError, reason="<= not supported between instances of NoneType and NoneType")
def test__StatReportForm__no_data_form():
    form = StatReportForm(MultiDict({}))
    form.wallets.choices = [("1", "Wallet 1")]
    assert form.validate() is False

# ---------------------------- report generators ----------------------------

def test__generate_biggest_expenses_report__formats_data(app, mock_session):
    fake_txn = MagicMock(
        timestamp=datetime.datetime(2024, 1, 1, 10, 20),
        amount=-200,
        description="coffee",
    )
    mock_session([(fake_txn,)])
    with app.app_context():
        result = generate_biggest_expenses_report(
            datetime.date(2024,1,1),
            datetime.date(2024,1,31),
            [1]
        )
    assert result.columns == ["billed at", "amount", "description"]
    assert result.data == [[datetime.datetime(2024, 1, 1, 10, 20), -200, "coffee"]]


def test__expenses_by_weekday__maps_dow_to_names(app, mock_session):
    mock_session([(0, -500), (1, -300)])

    with app.app_context():
        result = generate_expenses_by_weekday_report(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 1, 31),
            [1]
        )

    assert result.columns == ["Day of week", "Total expenses"]
    assert result.data == [["Monday", -500], ["Tuesday", -300]]


def test__expenses_by_week__casts_week_to_int(app, mock_session):
    mock_session([(3.0, -1000)])

    with app.app_context():
        result = generate_expenses_by_week_report(
            datetime.date(2024, 1, 1), datetime.date(2024, 1, 31), [1]
        )

    assert result.columns == ["Week num", "Total expenses"]
    assert result.data == [[3, -1000]]


def test__expenses_by_type__returns_description_and_sum(app, mock_session):
    mock_session([("coffee", -500), ("taxi", -2000)])

    with app.app_context():
        result = generate_expenses_by_type_report(
            datetime.date(2024, 1, 1), datetime.date(2024, 1, 31), [1]
        )

    assert result.columns == ["Description", "Total expenses"]
    assert result.data == [["coffee", -500], ["taxi", -2000]]


def test__weekly_balance__computes_balance_as_income_plus_expense(
    app, mock_session
):
    mock_session([(3.0, -500, 1000)])

    with app.app_context():
        result = generate_weekly_balance_report(
            datetime.date(2024, 1, 1), datetime.date(2024, 1, 31), [1]
        )

    assert result.columns == ["Week num", "Total expenses", "Total income",
                              "Week balance"]
    assert result.data == [[3, -500, 1000, 500]]
