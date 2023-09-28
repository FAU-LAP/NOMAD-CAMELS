import requests

# Your Keycloak configuration
keycloak_token_url = "https://nomad.eln.data.fau.de/keycloak/auth/realms/nomad/protocol/openid-connect/token"
client_id = "nomad_public"
client_secret = "your-client-secret"  # Replace with your client secret

# Refresh token (if available)
refresh_token = "your-refresh-token"

# Function to refresh the access token
def refresh_access_token(refresh_token):
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(keycloak_token_url, data=token_data)
    token_response = response.json()

    access_token = token_response.get("access_token")
    new_refresh_token = token_response.get("refresh_token")  # Optional

    return access_token, new_refresh_token

# Check if access token is expired or close to expiration
if token_expiration_is_near():
    new_access_token, new_refresh_token = refresh_access_token(refresh_token)

    if new_access_token:
        # Update token and refresh token in your application's storage
        access_token = new_access_token
        refresh_token = new_refresh_token  # Optional