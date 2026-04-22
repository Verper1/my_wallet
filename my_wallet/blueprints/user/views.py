import logging
from typing import Any

from flask import render_template, request, session, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from my_wallet.blueprints.user.changers import create_user, update_user
from my_wallet.blueprints.user.fetchers import fetch_user_by
from my_wallet.blueprints.user.forms import (
    RegistrationForm,
    RegistrationStep2Form,
    LoginForm,
    LoginVerifyForm,
    UserSettingsForm,
    EmailChangeForm,
    EmailChangeVerifyForm,
    MobileChangeForm,
    MobileChangeVerifyForm,
)
from my_wallet.blueprints.user.services.verification import (
    generate_email_code,
    generate_sms_code,
    send_verification_email,
    send_verification_sms,
)


logger = logging.getLogger(__name__)


def register() -> Any:
    """Show the registration form and start the registration flow."""
    form = (
        RegistrationForm(request.form)
        if request.method == "POST"
        else RegistrationForm()
    )
    if request.method == "POST" and form.validate():
        user = create_user(
            email=form.email.data,
            mobile=form.mobile.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        session["user_id"] = user.id
        session["email_code"] = generate_email_code()
        session["sms_code"] = generate_sms_code()
        logger.info(
            f"Verification codes: sms {session['sms_code']}, email {session['email_code']}"
        )
        send_verification_email(user.email, code=session["email_code"])
        send_verification_sms(user.mobile, code=session["sms_code"])
        return redirect(url_for(".verify"))
    return render_template("register_step1.html", form=form)


def verify() -> Any:
    """Verify email and sms codes for the registration flow."""
    form = (
        RegistrationStep2Form(request.form)
        if request.method == "POST"
        else RegistrationStep2Form()
    )
    if request.method == "POST" and form.validate():
        user = fetch_user_by(user_id=session["user_id"])
        login_user(user)
        return redirect(url_for(".settings"))
    return render_template("register_step2.html", form=form)


def login() -> Any:
    """Show the login form and start the login flow."""
    form = LoginForm(request.form) if request.method == "POST" else LoginForm()
    if request.method == "POST" and form.validate():
        user = fetch_user_by(email=form.email.data)
        session["user_id"] = user.id if user else None
        if user:
            session["email_code"] = generate_email_code()
            send_verification_email(user.email, code=session["email_code"])
        return redirect(url_for(".login_verify"))
    return render_template("login_step1.html", form=form)


def login_verify() -> Any:
    """Verify email code for the login flow."""
    form = (
        LoginVerifyForm(request.form) if request.method == "POST" else LoginVerifyForm()
    )
    if request.method == "POST" and form.validate():
        user = fetch_user_by(user_id=session["user_id"])
        login_user(user)
        return redirect(url_for(".settings"))
    return render_template("login_step2.html", form=form)


def logout() -> Any:
    """Log the current user out."""
    logout_user()
    return redirect(url_for(".login"))


@login_required
def settings() -> Any:
    """Show the user settings form and save changes."""
    form = (
        UserSettingsForm(request.form)
        if request.method == "POST"
        else UserSettingsForm(
            first_name=current_user.first_name, last_name=current_user.last_name
        )
    )
    if request.method == "POST" and form.validate():
        update_user(
            user_id=current_user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        flash("Saved")
        return redirect(url_for(".settings"))
    return render_template("settings.html", form=form)


@login_required
def change_email() -> Any:
    """Show the email change form and start the email change flow."""
    form = (
        EmailChangeForm(request.form) if request.method == "POST" else EmailChangeForm()
    )
    if request.method == "POST" and form.validate():
        session["email_change_code"] = generate_email_code()
        session["new_email"] = form.email.data
        send_verification_email(session["new_email"], code=session["email_change_code"])
        return redirect(url_for(".verify_change_email"))
    return render_template("change_email.html", form=form)


@login_required
def verify_change_email() -> Any:
    """Verify email code for the email change flow."""
    form = (
        EmailChangeVerifyForm(request.form)
        if request.method == "POST"
        else EmailChangeVerifyForm()
    )
    if request.method == "POST" and form.validate():
        update_user(
            user_id=current_user.id,
            email=session["new_email"],
        )
        flash(f"Email changed to {session['new_email']}")
        return redirect(url_for(".settings"))
    return render_template("verify_change_email.html", form=form)


@login_required
def change_mobile() -> Any:
    """Show the mobile change form and start the mobile change flow."""
    form = (
        MobileChangeForm(request.form)
        if request.method == "POST"
        else MobileChangeForm()
    )
    if request.method == "POST" and form.validate():
        session["mobile_change_code"] = generate_sms_code()
        session["new_mobile"] = form.mobile.data
        send_verification_sms(session["new_mobile"], code=session["mobile_change_code"])
        return redirect(url_for(".verify_change_mobile"))
    return render_template("change_mobile.html", form=form)


@login_required
def verify_change_mobile() -> Any:
    """Verify sms code for the mobile change flow."""
    form = (
        MobileChangeVerifyForm(request.form)
        if request.method == "POST"
        else MobileChangeVerifyForm()
    )
    if request.method == "POST" and form.validate():
        update_user(
            user_id=current_user.id,
            mobile=session["new_mobile"],
        )
        flash(f"Mobile changed to {session['new_mobile']}")
        return redirect(url_for(".settings"))
    return render_template("verify_change_mobile.html", form=form)
