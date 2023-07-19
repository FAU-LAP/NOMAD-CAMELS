import requests

realm_url = 'https://nomad.eln.data.fau.de/keycloak/auth/realms/nomad'
well_known_url = f'{realm_url}/.well-known/openid-configuration'

response = requests.get(well_known_url)
config = response.json()

auth_url = config['authorization_endpoint']
token_url = config['token_endpoint']


