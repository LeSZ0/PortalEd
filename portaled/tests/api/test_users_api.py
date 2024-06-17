from portaled.queries.user import create_user, get_user
from portaled.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema,
    UserPartialUpdateSchema,
)
from portaled.tests.conftest import TestSessionLocal
from unittest import TestCase
from portaled.tests.api import client, create_db_tables, drop_db_tables
from portaled.tests.utils import get_access_token, add_access_token_header
from portaled.utils.errors import AlreadyExistError, NotFoundError


class TestUserApi(TestCase):
    user_id = "12b282fe-b464-491a-9363-45c4208d0bfe"

    def setUp(self):
        create_db_tables()
        user = UserCreateSchema(
            id=self.user_id,
            username="fake_user_db",
            password="averyweakpassword",
            email="fake@email.com",
        )
        session = TestSessionLocal()
        try:
            db_user = create_user(db=session, user=user)
            session.add(db_user)
            session.commit()
            session.close()
        except:
            db_user = get_user(db=session, user_id=user.id)
        self.token = get_access_token(
            client, username=user.username, password=user.password.get_secret_value()
        )

    def tearDown(self):
        drop_db_tables()

    async def test_get_users(self):
        response = client.get(
            url="/apis/users", headers=await add_access_token_header(self.token)
        )
        assert response.status_code == 200

    async def test_get_user_by_id(self):
        response = client.get(
            url=f"/apis/users/{self.user_id}",
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 200

    async def test_update_user(self):
        data = UserUpdateSchema(username="fake_user_updated", email="fake@email.com")
        response = client.put(
            url=f"/apis/users/{self.user_id}",
            json=data.model_dump(),
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["username"] == "fake_user_updated"

    async def test_patch_user(self):
        data = UserPartialUpdateSchema(
            username="fake_user", email="fake_updated@email.com"
        )
        response = client.patch(
            url=f"/apis/users/{self.user_id}",
            json=data.model_dump(),
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["email"] == "fake_updated@email.com"

    async def test_delete_user(self):
        response = client.delete(
            url=f"/apis/users/{self.user_id}",
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 202
        assert "User deleted successfuly" in response.json()

    async def test_delete_user_failed(self):
        response = client.delete(
            url=f"/apis/users/12b282fe-b464-491a-9363-45c4208d0abc",
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 404
        assert {"detail": "User not found"} == response.json()
