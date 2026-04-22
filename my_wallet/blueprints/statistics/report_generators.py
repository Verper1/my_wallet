import datetime

from flask import current_app
from sqlalchemy import select, func, case

from my_wallet.blueprints.statistics.custom_types import ReportData
from my_wallet.blueprints.wallet.models import Transaction


def generate_biggest_expenses_report(
    date_from: datetime.date,
    date_to: datetime.date,
    wallets_ids: list[int],
    top_transactions_amount: int = 20,
) -> ReportData:
    """Return the top N biggest expenses for the given wallets and period."""
    transactions_rows = current_app.session.execute(  # type: ignore[attr-defined]
        select(Transaction)
        .where(
            Transaction.wallet_id.in_(wallets_ids),
            Transaction.timestamp.between(date_from, date_to),
            Transaction.amount < 0,
        )
        .order_by(Transaction.amount)
        .limit(top_transactions_amount)
    ).fetchall()
    transactions = [w[0] for w in transactions_rows]

    return ReportData(
        columns=["billed at", "amount", "description"],
        data=[[t.timestamp, t.amount, t.description] for t in transactions],
    )


def generate_expenses_by_weekday_report(
    date_from: datetime.date,
    date_to: datetime.date,
    wallets_ids: list[int],
) -> ReportData:
    """Return total expenses grouped by day of week."""
    dow_names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    transactions_rows = current_app.session.execute(  # type: ignore[attr-defined]
        select(
            func.extract("dow", Transaction.timestamp).label("dow"),
            func.sum(Transaction.amount).label("total_expense"),
        )
        .where(
            Transaction.wallet_id.in_(wallets_ids),
            Transaction.timestamp.between(date_from, date_to),
            Transaction.amount < 0,
        )
        .group_by(func.extract("dow", Transaction.timestamp))
        .order_by(func.extract("dow", Transaction.timestamp))
    ).fetchall()

    return ReportData(
        columns=["Day of week", "Total expenses"],
        data=[[dow_names[int(r[0])], r[1]] for r in transactions_rows],
    )


def generate_expenses_by_week_report(
    date_from: datetime.date,
    date_to: datetime.date,
    wallets_ids: list[int],
) -> ReportData:
    """Return total expenses grouped by week number."""
    transactions_rows = current_app.session.execute(  # type: ignore[attr-defined]
        select(
            func.date_part("week", Transaction.timestamp).label("week_num"),
            func.sum(Transaction.amount).label("total_expense"),
        )
        .where(
            Transaction.wallet_id.in_(wallets_ids),
            Transaction.timestamp.between(date_from, date_to),
            Transaction.amount < 0,
        )
        .group_by(func.date_part("week", Transaction.timestamp))
        .order_by(func.date_part("week", Transaction.timestamp))
    ).fetchall()

    return ReportData(
        columns=["Week num", "Total expenses"],
        data=[[int(r[0]), r[1]] for r in transactions_rows],
    )


def generate_expenses_by_type_report(
    date_from: datetime.date,
    date_to: datetime.date,
    wallets_ids: list[int],
) -> ReportData:
    """Return total expenses grouped by description."""
    transactions_rows = current_app.session.execute(  # type: ignore[attr-defined]
        select(
            Transaction.description,
            func.sum(Transaction.amount).label("total_expense"),
        )
        .where(
            Transaction.wallet_id.in_(wallets_ids),
            Transaction.timestamp.between(date_from, date_to),
            Transaction.amount < 0,
        )
        .group_by(
            Transaction.description,
        )
        .order_by(
            func.sum(Transaction.amount),
        )
    ).fetchall()

    return ReportData(
        columns=["Description", "Total expenses"],
        data=[[r[0], r[1]] for r in transactions_rows],
    )


def generate_weekly_balance_report(
    date_from: datetime.date,
    date_to: datetime.date,
    wallets_ids: list[int],
) -> ReportData:
    """Return weekly expenses, income and balance."""
    transactions_rows = current_app.session.execute(  # type: ignore[attr-defined]
        select(
            func.date_part("week", Transaction.timestamp).label("week_num"),
            func.sum(
                case(
                    (Transaction.amount < 0, Transaction.amount),
                    else_=0,
                )
            ).label("total_expense"),
            func.sum(
                case(
                    (Transaction.amount > 0, Transaction.amount),
                    else_=0,
                )
            ).label("total_income"),
        )
        .where(
            Transaction.wallet_id.in_(wallets_ids),
            Transaction.timestamp.between(date_from, date_to),
        )
        .group_by(func.date_part("week", Transaction.timestamp))
        .order_by(func.date_part("week", Transaction.timestamp))
    ).fetchall()

    return ReportData(
        columns=["Week num", "Total expenses", "Total income", "Week balance"],
        data=[[int(r[0]), r[1], r[2], r[2] + r[1]] for r in transactions_rows],
    )
