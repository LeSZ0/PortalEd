from portaled.tests.conftest import TestSessionLocal
import pytest
from unittest import TestCase
from fastapi import HTTPException
from portaled.tests.api import client, create_db_tables, drop_db_tables
from portaled.schemas.profile import (
    ProfileCreateSchema,
    ProfileUpdateSchema,
    ProfilePartialUpdateSchema,
)
from portaled.queries.profile import create_profile
from portaled.queries.user import create_user, get_user
from portaled.schemas.user import UserCreateSchema
from portaled.tests.utils import get_access_token, add_access_token_header
from portaled.utils.errors import AlreadyExistError


class TestProfileApi(TestCase):
    profile_id = "12b282fe-b464-491a-9363-45c4208d0abc"
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
        except AlreadyExistError:
            db_user = get_user(db=session, user_id=user.id)

        self.profile = ProfileCreateSchema(
            id=self.profile_id,
            full_name="fake_diego",
            dni="1111111111",
            birth_date="1900-12-22",
            role="teacher",
            is_active=True,
            user_id=db_user.id,
        )

        create_profile(db=session, profile=self.profile)
        session.close()
        self.token = get_access_token(
            client=client,
            username=user.username,
            password=user.password.get_secret_value(),
        )

    def tearDown(self):
        drop_db_tables()

    async def test_get_profiles(self):
        response = client.get(
            url="/apis/profiles", headers=await add_access_token_header(self.token)
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_get_profile_by_id(self):
        response = client.get(
            url=f"/apis/profiles/{self.profile_id}",
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["dni"] == "1111111111"

    async def test_get_profile_by_id_err_profile_not_found(self):
        response = client.get(
            url=f"/apis/profiles/12b282fe-b464-491a-9363-45c4208d0123",
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 404
        assert {"detail": "Profile not found"} == response.json()

    async def test_update_profile(self):
        data = ProfileUpdateSchema(
            full_name=self.profile.full_name,
            birth_date=self.profile.birth_date,
            dni=self.profile.dni,
            role="student",
        )
        response = client.put(
            url=f"/apis/profiles/{self.profile_id}",
            json=data.model_dump(mode="json"),
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["role"] == "student"

    async def test_patch_profile(self):
        data = ProfilePartialUpdateSchema(
            full_name=self.profile.full_name,
            birth_date="1990-05-21",
            dni=self.profile.dni,
            role=self.profile.role,
        )
        response = client.patch(
            url=f"/apis/profiles/{self.profile_id}",
            json=data.model_dump(mode="json"),
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["birth_date"] == data.birth_date.strftime("%Y-%m-%d")

    async def test_create_profile(self):
        session = TestSessionLocal()
        user = UserCreateSchema(
            id="15282feb-b464-491a-9363-45c4208d0bfe",
            username="fake_user_db",
            password="averyweakpassword",
            email="a_real_user@email.com",
        )

        db_user = create_user(db=session, user=user)
        session.refresh(db_user)
        data = ProfileCreateSchema(
            id="aab282ce-b464-491a-9363-45c4208d0123",
            full_name="real_diego",
            dni="222222222",
            birth_date="1994-12-22",
            role="student",
            is_active=True,
            user_id=db_user.id,
        )
        response = client.post(
            url=f"/apis/profiles",
            json=data.model_dump(mode="json"),
            headers=await add_access_token_header(self.token),
        )
        session.refresh(db_user)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["id"] == "aab282ce-b464-491a-9363-45c4208d0123"
        assert db_user.profile.id == data.id
        session.close()

    async def test_delete_profile(self):
        response = client.delete(
            url=f"/apis/profiles/{self.profile_id}",
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 202
        assert "Profile deleted successfuly" in response.json()

    async def test_delete_profile_failed(self):
        response = client.delete(
            url=f"/apis/profiles/aab282ce-b464-491a-9363-45c4208d0123",
            headers=await add_access_token_header(self.token),
        )
        assert response.status_code == 404
        assert {"detail": "Profile not found"} == response.json()
