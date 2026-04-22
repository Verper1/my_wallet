import datetime

from flask import Flask, current_app
from requests import post  # type: ignore[import-untyped]

from my_wallet.blueprints.statistics.custom_types import ReportData
from my_wallet.blueprints.statistics.report_generators import (
    generate_expenses_by_type_report,
)
from my_wallet.blueprints.user.fetchers import fetch_all_users_with_configured_telegram
from my_wallet.blueprints.user.models import User
from my_wallet.blueprints.wallet.fetchers import fetch_wallets_for


def compose_stat_message(report_data: ReportData, user: User, last_days: int) -> str:
    total_spent = sum(r[1] for r in report_data.data)
    return (
        f"{user.first_name}, here are your expenses in last {last_days} days grouped by expense type: \n"
        + "\n".join([f"{r[0]}: {r[1]}" for r in report_data.data])
        + f"\nIn total you spent {total_spent}."
    )


def send_message_to_telegram(message: str, chat_id: str) -> None:
    token = current_app.config["TELEGRAM_BOT_TOKEN"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    post(url, data=data)


def run(app: Flask) -> None:
    last_days = 7
    for user in fetch_all_users_with_configured_telegram():
        wallets_ids = [w.id for w in fetch_wallets_for(user)]
        report_data = generate_expenses_by_type_report(
            date_from=datetime.datetime.now() - datetime.timedelta(days=last_days),
            date_to=datetime.datetime.now(),
            wallets_ids=wallets_ids,
        )
        message = compose_stat_message(report_data, user, last_days)
        send_message_to_telegram(message, chat_id=user.telegram_chat_id)
