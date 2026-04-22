from marshmallow import Schema
from marshmallow.fields import Int, String, List, DateTime, Decimal


class WalletSchema(Schema):
    id = Int(dump_only=True)
    title = String()
    status = String()
    owned_by_user_id = Int(dump_only=True)
    users_ids_with_access = List(
        Int(), dump_only=True, attribute="users_ids_with_access"
    )


class TransactionSchema(Schema):
    id = Int(dump_only=True)
    wallet_id = Int(dump_only=True)
    timestamp = DateTime()
    amount = Decimal()
    currency = String()
    description = String()
