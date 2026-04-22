from typing import Any

from flask import current_app, session
from sqlalchemy import exists
from wtforms import Form, StringField, EmailField
from wtforms.validators import InputRequired
from wtforms_alchemy import ModelForm

from my_wallet.blueprints.user.models.user import User


class RegistrationForm(Form):
    first_name = StringField(
        "First name", [InputRequired()], render_kw={"placeholder": "First name"}
    )
    last_name = StringField(
        "Last name", [InputRequired()], render_kw={"placeholder": "Last name"}
    )
    email = EmailField("Email", [InputRequired()], render_kw={"placeholder": "Email"})
    mobile = StringField(
        "Mobile phone", [InputRequired()], render_kw={"placeholder": "Mobile"}
    )

    def validate(self, extra_validators: Any = None) -> bool:
        """Validate registration form and reject duplicate email/mobile."""
        is_duplicates_exists = current_app.session.query(  # type: ignore[attr-defined]
            exists(User).where(
                User.email == self.email.data, User.mobile == self.mobile.data
            ),
        ).scalar()
        if is_duplicates_exists:
            self.email.errors = ("Please use another email/mobile pair",)
            return False
        return super().validate(extra_validators)


class RegistrationStep2Form(Form):
    email_code = StringField(
        "Email code", [InputRequired()], render_kw={"placeholder": "Email code"}
    )
    sms_code = StringField(
        "SMS code", [InputRequired()], render_kw={"placeholder": "SMS code"}
    )

    def validate(self, extra_validators: Any = None) -> bool:
        """Validate entered email and sms codes against stored ones."""
        all_codes_are_ok = True
        if session["email_code"] != self.email_code.data:
            self.email_code.errors = ("Wrong code",)
            all_codes_are_ok = False
        if session["sms_code"] != self.sms_code.data:
            self.sms_code.errors = ("Wrong code",)
            all_codes_are_ok = False
        if not all_codes_are_ok:
            return False
        return super().validate(extra_validators)


class LoginForm(Form):
    email = EmailField("Email", [InputRequired()], render_kw={"placeholder": "Email"})


class LoginVerifyForm(Form):
    email_code = StringField(
        "Email code", [InputRequired()], render_kw={"placeholder": "Email code"}
    )

    def validate(self, extra_validators: Any = None) -> bool:
        """Validate entered email code against the stored one."""
        if (
            not session["user_id"]
            or not session["email_code"]
            or session["email_code"] != self.email_code.data
        ):
            self.email_code.errors = ("Wrong code",)
            return False
        return super().validate(extra_validators)


class UserSettingsForm(ModelForm):
    class Meta:
        """ModelForm configuration."""

        model = User
        only = ["first_name", "last_name"]


class EmailChangeForm(Form):
    email = EmailField(
        "Email", [InputRequired()], render_kw={"placeholder": "New email"}
    )


class EmailChangeVerifyForm(Form):
    email_code = StringField(
        "Email code", [InputRequired()], render_kw={"placeholder": "Email code"}
    )

    def validate(self, extra_validators: Any = None) -> bool:
        """Validate email code for the email change flow."""
        if (
            not session["email_change_code"]
            or session["email_change_code"] != self.email_code.data
        ):
            self.email_code.errors = ("Wrong code",)
            return False
        return super().validate(extra_validators)


class MobileChangeForm(Form):
    mobile = StringField(
        "Mobile phone", [InputRequired()], render_kw={"placeholder": "New mobile"}
    )


class MobileChangeVerifyForm(Form):
    sms_code = StringField(
        "SMS code", [InputRequired()], render_kw={"placeholder": "SMS code"}
    )

    def validate(self, extra_validators: Any = None) -> bool:
        """Validate sms code for the mobile change flow."""
        if (
            not session["mobile_change_code"]
            or session["mobile_change_code"] != self.sms_code.data
        ):
            self.sms_code.errors = ("Wrong code",)
            return False
        return super().validate(extra_validators)
