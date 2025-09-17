import base64

import requests
import iugupy


def test_client_auth_and_headers() -> None:
    cfg = iugupy.IuguConfig(api_token="test_token", client_id="client-123", base_url="https://api.example.com/v1")
    client = iugupy.IuguClient(cfg)

    # Verify base_url normalization
    assert client.base_url == "https://api.example.com/v1/"

    # Verify default headers include JSON and UA
    headers = client.session.headers
    assert headers.get("Accept") == "application/json"
    assert headers.get("Content-Type") == "application/json"
    assert "User-Agent" in headers

    # Verify Basic Auth uses token with blank password
    # requests stores auth on session; we can craft a prepared request to inspect Authorization
    req = client.session.prepare_request(
        requests.Request("GET", "https://api.example.com/")
    )
    # Manually apply auth to the prepared request using the session's auth handler
    client.session.auth(req)
    auth_header = req.headers.get("Authorization")
    assert auth_header is not None and auth_header.startswith("Basic ")
    # Decode the basic token
    token_b64 = auth_header.split()[1]
    decoded = base64.b64decode(token_b64).decode()
    assert decoded == "test_token:"  # username:password (blank password)
