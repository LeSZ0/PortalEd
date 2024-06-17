from fastapi.testclient import TestClient
from portaled.main import app
from portaled.tests.conftest import override_get_db
from portaled.database.db import get_db, Base
from portaled.tests.conftest import engine


client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db


def create_db_tables():
    Base.metadata.create_all(bind=engine)


def drop_db_tables():
    Base.metadata.drop_all(bind=engine)
