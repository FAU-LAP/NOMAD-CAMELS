import pytest
from fastapi.testclient import TestClient
from fastapi import status, Depends, HTTPException
from unittest.mock import patch, MagicMock
from nomad_camels.api.api import FastapiThread, validate_credentials
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import socket
import time
import re


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


def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def get_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# Fixture to set up the TestClient and FastapiThread for testing
@pytest.fixture(scope="module")
def client_and_thread():
    # Mock the main_window with a predefined protocols_dict
    main_window_mock = MagicMock()
    main_window_mock.protocols_dict = {"protocol1": "details1", "protocol2": "details2"}

    port = get_available_port()
    # Create and start a FastapiThread instance with the mocked main_window
    thread = FastapiThread(main_window_mock, api_port=port)
    thread.start()
    # Get the FastAPI app and set up the TestClient
    while (app := thread.app) is None:
        time.sleep(0.1)
    client = TestClient(app)
    # Wait for the server to start
    timeout = 10  # seconds
    start_time = time.time()
    while True:
        try:
            response = client.get("/")
            if response.status_code == status.HTTP_200_OK:
                break
        except:
            pass
        if time.time() - start_time > timeout:
            raise TimeoutError("Server did not start within the timeout period")
        time.sleep(0.1)  # wait for 100ms before retrying

    # Override the validate_credentials dependency with the mock
    app.dependency_overrides[validate_credentials] = mock_validate_credentials

    # Mock the start_protocol signal
    thread.start_protocol_signal = MagicMock()

    # Provide the client and thread to the test
    yield client, thread

    # Stop the server after tests are done
    thread.stop_server()


# Test to check if the root URL redirects to the documentation page
@pytest.mark.order(-1)
def test_root_redirect(client_and_thread):
    client, thread = client_and_thread
    # Ensure the client exists
    assert client is not None, "Client is not initialized"

    # Ensure the thread exists and is running
    assert thread is not None, "Thread is not initialized"
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert str(response.url).endswith("/docs")


# Test to check if the /protocols endpoint returns the correct protocols
@pytest.mark.order(-1)
def test_get_protocols(client_and_thread):
    client, thread = client_and_thread
    # Ensure the client exists
    assert client is not None, "Client is not initialized"

    # Ensure the thread exists and is running
    assert thread is not None, "Thread is not initialized"
    response = client.get("/api/v1/protocols", auth=("user", "valid_api_key"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Protocols": ["protocol1", "protocol2"]}


# Test to check if a protocol can be run with a valid API key
@pytest.mark.order(-1)
def test_run_protocol(client_and_thread):
    client, thread = client_and_thread
    # Ensure the client exists
    assert client is not None, "Client is not initialized"

    # Ensure the thread exists and is running
    assert thread is not None, "Thread is not initialized"
    protocol_name = "protocol1"

    # Patch the emit method of the start_protocol signal
    with patch.object(thread.start_protocol_signal, "emit") as mock_emit:
        response = client.get(
            f"/api/v1/actions/run/protocols/{protocol_name}",
            auth=("user", "valid_api_key"),
        )
        assert response.status_code == status.HTTP_200_OK
        # Check if the response contains the expected URL with a UUID4 string
        response_json = response.json()
        assert "check protocol status here" in response_json
        url = response_json["check protocol status here"]
        uuid_pattern = re.compile(
            r"^/api/v1/protocols/results/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        )
        assert uuid_pattern.match(url), f"URL does not match expected pattern: {url}"
        # Extract the UUID from the URL
        uuid = url.split("/")[-1]
        # Update the mock_emit assertion to include the additional parameters
        mock_emit.assert_called_once_with(protocol_name, uuid, None)


# Test to check if accessing /protocols with an invalid API key returns 401
@pytest.mark.order(-1)
def test_invalid_api_key(client_and_thread):
    client, thread = client_and_thread
    # Ensure the client exists
    assert client is not None, "Client is not initialized"

    # Ensure the thread exists and is running
    assert thread is not None, "Thread is not initialized"
    response = client.get("/api/v1/protocols", auth=("user", "invalid_api_key"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid API Key"}


# Test to check if the /favicon.ico endpoint returns the favicon correctly
@pytest.mark.order(-1)
def test_favicon(client_and_thread):
    client, thread = client_and_thread
    # Ensure the client exists
    assert client is not None, "Client is not initialized"

    # Ensure the thread exists and is running
    assert thread is not None, "Thread is not initialized"
    response = client.get("/favicon.ico")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] in [
        "image/x-icon",
        "image/vnd.microsoft.icon",
    ]
