from my_wallet.utils.config import get_connection_dsn

def test__get_connection_dsn__returns_dsn(config):
    dsn = get_connection_dsn(config)
    assert dsn == "postgresql://test:test@test:test/test"
