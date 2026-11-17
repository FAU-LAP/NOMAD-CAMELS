"""Settings and credentials for OASIS remote control.

The device token identifies this computer at the OASIS broker. On Windows it is
encrypted with DPAPI for the current Windows user, so a copy of the settings
file is useless on another account or computer. Other systems store it in a
file readable only by the owner.
"""

from __future__ import annotations

import base64
import json
import os
import socket
import ssl
import sys
from dataclasses import asdict, dataclass
from urllib.parse import urlsplit, urlunsplit

from nomad_camels.utility import load_save_functions

CONFIG_FILE = "remote_control.json"
REMOTE_PATH = "/camels-remote"


class RemoteConfigError(Exception):
    """Invalid remote-control settings or a failed pairing."""


@dataclass
class RemoteConfig:
    enabled: bool = False
    oasis_url: str = ""
    ca_file: str = ""
    device_id: str = ""
    device_name: str = ""
    token: dict | None = None  # {"scheme": "dpapi" | "file", "data": "..."}
    # Staff at the lab computer can pause remote control: CAMELS stays
    # connected and readable, but refuses operations that change anything.
    control_paused: bool = False

    @property
    def paired(self) -> bool:
        return bool(self.device_id and self.token)


def config_path() -> str:
    return os.path.join(load_save_functions.appdata_path, CONFIG_FILE)


def load_config() -> RemoteConfig:
    try:
        with open(config_path(), encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError):
        return RemoteConfig()
    known = RemoteConfig.__dataclass_fields__
    return RemoteConfig(**{key: value for key, value in data.items() if key in known})


def save_config(config: RemoteConfig) -> None:
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as file:
        json.dump(asdict(config), file, indent=2)
    if os.name != "nt":
        os.chmod(tmp_path, 0o600)
    os.replace(tmp_path, path)


# ----------------------------------------------------------------------
# Token protection
# ----------------------------------------------------------------------
def _dpapi(data: bytes, protect: bool) -> bytes:
    import ctypes
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    buffer = ctypes.create_string_buffer(data, len(data))
    blob_in = DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char)))
    entropy_bytes = b"NOMAD-CAMELS remote device token"
    entropy_buffer = ctypes.create_string_buffer(entropy_bytes, len(entropy_bytes))
    entropy = DATA_BLOB(len(entropy_bytes), ctypes.cast(entropy_buffer, ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()
    CRYPTPROTECT_UI_FORBIDDEN = 0x01
    function = crypt32.CryptProtectData if protect else crypt32.CryptUnprotectData
    ok = function(
        ctypes.byref(blob_in),
        None,
        ctypes.byref(entropy),
        None,
        None,
        CRYPTPROTECT_UI_FORBIDDEN,
        ctypes.byref(blob_out),
    )
    if not ok:
        raise RemoteConfigError("The device token could not be decrypted for this Windows user.")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData)
    finally:
        kernel32.LocalFree(blob_out.pbData)


def protect_token(token: str) -> dict:
    if sys.platform == "win32":
        encrypted = _dpapi(token.encode("utf-8"), protect=True)
        return {"scheme": "dpapi", "data": base64.b64encode(encrypted).decode("ascii")}
    return {"scheme": "file", "data": token}


def unprotect_token(stored: dict | None) -> str:
    if not stored:
        raise RemoteConfigError("This computer is not paired with OASIS.")
    if stored.get("scheme") == "dpapi":
        return _dpapi(base64.b64decode(stored["data"]), protect=False).decode("utf-8")
    if stored.get("scheme") == "file":
        return stored["data"]
    raise RemoteConfigError("Unknown token format.")


# ----------------------------------------------------------------------
# URLs and TLS
# ----------------------------------------------------------------------
def normalize_oasis_url(url: str) -> str:
    """Return ``https://host[:port]/base`` without a trailing slash.

    Plain HTTP is only accepted for this computer, for development.
    """
    url = url.strip().rstrip("/")
    if not url:
        raise RemoteConfigError("Enter the OASIS address.")
    if "://" not in url:
        url = "https://" + url
    parts = urlsplit(url)
    if parts.scheme not in ("https", "http") or not parts.hostname:
        raise RemoteConfigError("The OASIS address must start with https://.")
    if parts.scheme == "http" and parts.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise RemoteConfigError("The OASIS address must use https://, because the connection must be encrypted.")
    if parts.query or parts.fragment:
        raise RemoteConfigError("The OASIS address must not contain '?' or '#'.")
    path = parts.path.rstrip("/")
    if path.endswith(REMOTE_PATH):
        path = path[: -len(REMOTE_PATH)]
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def pair_url(oasis_url: str) -> str:
    return normalize_oasis_url(oasis_url) + REMOTE_PATH + "/pair"


def agent_url(oasis_url: str) -> str:
    base = normalize_oasis_url(oasis_url)
    scheme = "wss" if base.startswith("https://") else "ws"
    return scheme + base[base.index("://"):] + REMOTE_PATH + "/agent"


def ssl_context(ca_file: str = "") -> ssl.SSLContext:
    """TLS with certificate verification. ``ca_file`` adds a private CA."""
    context = ssl.create_default_context()
    if ca_file:
        if not os.path.isfile(ca_file):
            raise RemoteConfigError(f"The CA certificate file was not found: {ca_file}")
        context.load_verify_locations(cafile=ca_file)
    return context


# ----------------------------------------------------------------------
# Pairing
# ----------------------------------------------------------------------
def pair(oasis_url: str, pairing_code: str, ca_file: str = "") -> RemoteConfig:
    """Redeem a pairing code at OASIS and store the device token.

    The ``enabled`` setting is not changed.
    """
    import httpx
    from nomad_camels import __version__

    oasis_url = normalize_oasis_url(oasis_url)
    code = pairing_code.strip()
    if not code:
        raise RemoteConfigError("Enter the pairing code shown in OASIS.")
    verify = ssl_context(ca_file) if oasis_url.startswith("https://") else False
    try:
        response = httpx.post(
            pair_url(oasis_url),
            json={"pairing_code": code, "hostname": socket.gethostname(), "camels_version": __version__},
            verify=verify,
            timeout=20,
        )
    except httpx.HTTPError as exc:
        raise RemoteConfigError(f"OASIS could not be reached: {exc}") from exc
    if response.status_code in (400, 429):
        try:
            detail = response.json().get("detail")
        except ValueError:
            detail = None
        raise RemoteConfigError(detail or "The pairing code was rejected.")
    if response.status_code != 200:
        raise RemoteConfigError(
            f"OASIS answered with HTTP {response.status_code}. Check the address."
        )
    try:
        data = response.json()
        token = data["device_token"]
        device_id = data["device_id"]
    except (ValueError, KeyError) as exc:
        raise RemoteConfigError("OASIS returned an unexpected answer.") from exc

    config = load_config()
    config.oasis_url = oasis_url
    config.ca_file = ca_file
    config.device_id = device_id
    config.device_name = data.get("device_name", "")
    config.token = protect_token(token)
    save_config(config)
    return config


def unpair() -> RemoteConfig:
    """Forget the token on this computer. The device stays listed in OASIS."""
    config = load_config()
    config.enabled = False
    config.device_id = ""
    config.device_name = ""
    config.token = None
    save_config(config)
    return config
