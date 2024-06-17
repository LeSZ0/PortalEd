from portaled.queries.user import create_user
from portaled.schemas.post import PostCreateSchema, PostUpdateSchema
from portaled.schemas.user import UserCreateSchema
from portaled.tests.conftest import TestSessionLocal
from unittest import TestCase
from portaled.tests.api import client, create_db_tables, drop_db_tables
from portaled.queries.post import create_post
from portaled.tests.utils import get_access_token, add_access_token_header


class TestPostApi(TestCase):
    user_id = "12b282fe-b464-491a-9363-45c4208d0bfe"

    def setUp(self):
        create_db_tables()
        self.user = UserCreateSchema(
            id=self.user_id,
            username="fake_user_db",
            password="averyweakpassword",
            email="fake@email.com",
        )
        self.post = PostCreateSchema(
            title="A fake post",
            slug="a-fake-post",
            body="This is a fake body for the fake post.",
            tags=["A new tag"],
            author=self.user_id,
        )
        session = TestSessionLocal()
        self.db_user = create_user(db=session, user=self.user)
        self.db_post = create_post(db=session, post=self.post, user_id=self.db_user.id)
        session.close()

        self.access_token = get_access_token(
            client,
            username=self.user.username,
            password=self.user.password.get_secret_value(),
        )

    def tearDown(self):
        drop_db_tables()

    async def test_get_posts(self):
        response = client.get(
            url="/apis/posts", headers=await add_access_token_header(self.access_token)
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_get_post_by_id(self):
        response = client.get(
            url=f"/apis/posts/{self.db_post.id}",
            headers=await add_access_token_header(self.access_token),
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["slug"] == "a-fake-post"

    async def test_create_post(self):
        post_data = PostCreateSchema(
            title="This is a new post",
            slug="this-is-a-new-post",
            body="This is a fake body for the new post.",
            tags=["fake", "new"],
            author=self.user_id,
        )

        response = client.post(
            url="/apis/posts",
            json=post_data.model_dump(mode="json"),
            headers=await add_access_token_header(self.access_token),
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["slug"] == "this-is-a-new-post"

    async def test_update_post(self):
        post_updated_data = PostUpdateSchema(
            title="This is a new post updated",
            slug="this-is-a-new-post-updated",
            body="This is a fake body for the new post.",
        )
        response = client.put(
            url=f"/apis/posts/{self.db_post.id}",
            json=post_updated_data.model_dump(mode="json"),
            headers=await add_access_token_header(self.access_token),
        )
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["slug"] == "this-is-a-new-post-updated"

    async def test_delete_post(self):
        response = client.delete(
            url=f"/apis/posts/{self.db_post.id}",
            headers=await add_access_token_header(self.access_token),
        )
        assert response.status_code == 202
        assert "Post deleted" in response.json()
