import json
import os
import tempfile

import pytest
from app import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path
    })

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def problems():
    with open(os.path.join(os.path.dirname(__file__), '.problems'), 'rt') as f:
        return json.load(f)
