import pytest
from fastapi.testclient import TestClient
from fastapi import status, Depends, HTTPException
from unittest.mock import patch, MagicMock
from nomad_camels.api.api import FastapiThread, validate_credentials
from fastapi.security import HTTPBasicCredentials, HTTPBasic


# Mocked dependency to replace validate_credentials during tests
def mock_validate_credentials(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    # Check if the provided password is "valid_api_key"
    if credentials.password == "valid_api_key":
        return "mock_api_key"
    else:
        # Raise HTTP 401 Unauthorized if the password is invalid
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )


# Fixture to set up the TestClient and FastapiThread for testing
@pytest.fixture()
def client_and_thread():
    # Mock the main_window with a predefined protocols_dict
    main_window_mock = MagicMock()
    main_window_mock.protocols_dict = {"protocol1": "details1", "protocol2": "details2"}

    # Create and start a FastapiThread instance with the mocked main_window
    thread = FastapiThread(main_window_mock, api_port=12345)
    thread.start()

    # Get the FastAPI app and set up the TestClient
    app = thread.app
    client = TestClient(app)

    # Override the validate_credentials dependency with the mock
    app.dependency_overrides[validate_credentials] = mock_validate_credentials

    # Mock the start_protocol signal
    thread.start_protocol_signal = MagicMock()

    # Provide the client and thread to the test
    yield client, thread

    # Stop the server after tests are done
    thread.stop_server()


# Test to check if the root URL redirects to the documentation page
def test_root_redirect(client_and_thread):
    client, thread = client_and_thread
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert str(response.url).endswith("/docs")


# Test to check if the /protocols endpoint returns the correct protocols
def test_get_protocols(client_and_thread):
    client, thread = client_and_thread
    response = client.get("/api/v1/protocols", auth=("user", "valid_api_key"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Protocols": ["protocol1", "protocol2"]}


# Test to check if a protocol can be run with a valid API key
def test_run_protocol(client_and_thread):
    client, thread = client_and_thread
    protocol_name = "protocol1"

    # Patch the emit method of the start_protocol signal
    with patch.object(thread.start_protocol_signal, "emit") as mock_emit:
        response = client.get(
            f"/api/v1/actions/run/protocols/{protocol_name}",
            auth=("user", "valid_api_key"),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "success"}
        mock_emit.assert_called_once_with(protocol_name)


# Test to check if accessing /protocols with an invalid API key returns 401
def test_invalid_api_key(client_and_thread):
    client, thread = client_and_thread
    response = client.get("/api/v1/protocols", auth=("user", "invalid_api_key"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid API Key"}


# Test to check if the /favicon.ico endpoint returns the favicon correctly
def test_favicon(client_and_thread):
    client, thread = client_and_thread
    response = client.get("/favicon.ico")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] in [
        "image/x-icon",
        "image/vnd.microsoft.icon",
    ]
