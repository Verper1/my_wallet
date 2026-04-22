from flask import Blueprint

from my_wallet.blueprints.user.views import (
    register,
    verify,
    login,
    login_verify,
    logout,
    settings,
    change_email,
    verify_change_email,
    change_mobile,
    verify_change_mobile,
)


def configure_routes(blueprint: Blueprint) -> None:
    blueprint.add_url_rule("/register/", view_func=register, methods=["GET", "POST"])
    blueprint.add_url_rule("/verify/", view_func=verify, methods=["GET", "POST"])

    blueprint.add_url_rule("/login/", view_func=login, methods=["GET", "POST"])
    blueprint.add_url_rule(
        "/login/verify/", view_func=login_verify, methods=["GET", "POST"]
    )
    blueprint.add_url_rule("/logout/", view_func=logout, methods=["GET"])

    blueprint.add_url_rule(
        "/email/change/", view_func=change_email, methods=["GET", "POST"]
    )
    blueprint.add_url_rule(
        "/email/change/verify/", view_func=verify_change_email, methods=["GET", "POST"]
    )
    blueprint.add_url_rule(
        "/mobile/change/", view_func=change_mobile, methods=["GET", "POST"]
    )
    blueprint.add_url_rule(
        "/mobile/change/verify/",
        view_func=verify_change_mobile,
        methods=["GET", "POST"],
    )

    blueprint.add_url_rule("/settings/", view_func=settings, methods=["GET", "POST"])
