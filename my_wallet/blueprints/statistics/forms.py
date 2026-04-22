from typing import Any

from wtforms import Form, DateField, SelectMultipleField, SelectField
from wtforms.validators import InputRequired

from my_wallet.blueprints.statistics.enums import StatReportType, ReportDisplayFormat
from my_wallet.blueprints.statistics.utils import is_report_range_valid


class StatReportForm(Form):
    date_from = DateField("Date from", [InputRequired()])
    date_to = DateField("Date to", [InputRequired()])
    wallets = SelectMultipleField("Wallets", [InputRequired()])
    report_type = SelectField(
        "Report type", [InputRequired()], choices=StatReportType.choices()
    )
    output_format = SelectField(
        "Display format",
        [InputRequired()],
        choices=ReportDisplayFormat.choices(),
        default=ReportDisplayFormat.HTML,
    )

    def validate(self, extra_validators: Any = None) -> bool:
        """Validate form fields and the date range."""
        if is_report_range_valid(self.date_from.data, self.date_to.data):
            self.date_to.errors = (f"Should be after {self.date_from.data}",)
            return False
        return super().validate(extra_validators)
