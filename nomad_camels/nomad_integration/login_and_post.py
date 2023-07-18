import os.path

import requests

base_url = 'http://nomad-lab.eu/prod/v1/staging/api/v1'
new_url = 'https://nomad.eln.data.fau.de/nomad-oasis/api/v1'
base_url = new_url

password = ''
login = {'username': '',
         'password': ''}

response = requests.get(f'{base_url}/auth/token', params=login)
token = response.json()['access_token']
auth = {'Authorization': f'Bearer {token}'}
sig_token = requests.get(f'{base_url}/auth/signature_token', headers=auth)
print(sig_token.json())

resp = requests.get(f'{base_url}/uploads', headers=auth)
uploads = resp.json()['data']
print(uploads)

wanted_upload = 'testload'
upload_id = None
for upload in uploads:
    if upload['upload_name'] == wanted_upload:
        upload_id = upload['upload_id']
        break

entries = requests.get(f'{base_url}/uploads/{upload_id}/entries', headers=auth)
ents = entries.json()
print(ents)

response = requests.get(f'{base_url}/auth/token', params=login)
token = response.json()['access_token']

# f_path = r"C:\Users\od93yces\Downloads\pericles_251190441.bib"
# with open(f_path, 'rb') as f:
#     head = {'accept': 'application/json',
#             'Authorization': f'Bearer {token}'}
#     params = {
#         'overwrite_if_exists': 'true',
#         'wait_for_processing': 'false',
#         'include_archive': 'false',
#         'file_name': os.path.basename(f_path),
#         # 'token': '7q6MzUAEQEGMvempGr138w.bLHftZvbjC_U_Bof1uPUePGYST0'  # Replace with your valid token
#         # 'token': sig_token
#     }
#     a = requests.put(f'{base_url}/uploads/{upload_id}/raw/CAMELS_data', data=f, headers=head,
#                      params=params)
# print(a.json())

