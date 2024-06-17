from portaled.auth.responses import TokenResponse
from fastapi.testclient import TestClient


def get_access_token(client: TestClient, username: str, password: str) -> TokenResponse:
    data = {"username": username, "password": password}
    return client.post("auth/token", json=data)


async def add_access_token_header(access_token: TokenResponse) -> dict | None:
    if not access_token:
        return

    return {"Authorization": f"{access_token.token_type} {access_token.access_token}"}
