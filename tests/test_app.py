""" Test src.server.app """

from src.server import app


def test_read_root():
    assert app.read_root() == {"Hello": "World"}
