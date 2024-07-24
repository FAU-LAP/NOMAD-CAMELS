import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status, Depends, HTTPException
from unittest.mock import patch, MagicMock
from nomad_camels.api.api import FastapiThread, validate_credentials
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import typing


def mock_validate_credentials(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    if credentials.password == "valid_api_key":
        return "mock_api_key"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )


@pytest.fixture
def client_and_thread():
    # Mocking the main_window with protocols_dict
    main_window_mock = MagicMock()
    main_window_mock.protocols_dict = {"protocol1": "details1", "protocol2": "details2"}

    # Create an instance of FastapiThread and start the server in a background thread
    thread = FastapiThread(main_window_mock, api_port=12345)
    thread.start()
    app = thread.app
    client = TestClient(app)
    app.dependency_overrides[validate_credentials] = mock_validate_credentials
    # Mock the start_protocol signal
    thread.start_protocol = MagicMock()
    yield client, thread

    thread.stop_server()


def test_root_redirect(client_and_thread):
    client, thread = client_and_thread
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert str(response.url).endswith("/docs")


def test_get_protocols(client_and_thread):
    client, thread = client_and_thread
    response = client.get("/protocols", auth=("user", "valid_api_key"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Protocols": ["protocol1", "protocol2"]}


def test_run_protocol(client_and_thread):
    client, thread = client_and_thread
    protocol_name = "protocol1"
    # Test with a valid API key
    with patch.object(thread.start_protocol, 'emit') as mock_emit:
        response = client.get(f"/protocols/{protocol_name}", auth=("user", "valid_api_key"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "success"}
        mock_emit.assert_called_once_with(protocol_name)



def test_invalid_api_key(client_and_thread):
    client, thread = client_and_thread
    response = client.get("/protocols", auth=("user", "invalid_api_key"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid API Key"}


def test_favicon(client_and_thread):
    client, thread = client_and_thread
    response = client.get("/favicon.ico")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/x-icon"
