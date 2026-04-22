import datetime
import random

from flask import Flask

from my_wallet.blueprints.wallet.changers import create
from my_wallet.blueprints.wallet.enums import WalletStatus
from my_wallet.blueprints.wallet.models import Wallet, Transaction


def run(app: Flask) -> None:
    for_user_id = 2
    transactions_num = 20

    wallet = create(
        Wallet(
            title=f"Test wallet {random.randint(1, 1000)}",
            status=WalletStatus.ACTIVE,
            owned_by_user_id=for_user_id,
        )
    )
    for _ in range(transactions_num):
        create(
            Transaction(
                wallet_id=wallet.id,
                timestamp=(
                    datetime.datetime.now()
                    - datetime.timedelta(
                        days=random.randint(1, 300), hours=random.randint(1, 24)
                    )
                ),
                amount=random.randint(-2000, 2000),
                currency="USD",
                description=random.choice(["SUPERMARKET LTD", "IE HOMESTUFF", "CAFE"]),
            )
        )
