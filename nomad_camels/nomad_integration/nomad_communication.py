"""This module provides functions for communicating with NOMAD."""

import os.path
import requests
from PySide6.QtWidgets import QDialog

from nomad_camels.nomad_integration.nomad_login import LoginDialog
from nomad_camels.utility.dict_recursive_string import dict_recursive_string
from nomad_camels.utility import variables_handling

# by default the url of the central NOMAD at first
central_url = 'http://nomad-lab.eu/prod/v1/staging/api/v1'
nomad_url = ''

token = ''
auth = {'Authorization': f'Bearer {token}'}


def login_to_nomad(parent=None):
    """Opens a login dialog and uses the resulting username/password to login to
    NOMAD. The recieved authentification token is saved to the module's global
    variable `token`.

    Parameters
    ----------
    parent : QWidget
        the parent widget for the login dialog

    Returns
    -------
    the authentification token
    """
    global token, auth, nomad_url
    dialog = LoginDialog(parent)
    if dialog.exec() != QDialog.Accepted:
        return
    nomad_url = dialog.url
    if not nomad_url:
        nomad_url = central_url
    if dialog.token:
        local_auth = {'Authorization': f'Bearer {dialog.token}'}
        response = requests.get(f'{nomad_url}/auth/signature_token',
                                headers=local_auth)
        check_response(response, 'Login failed!')
        token = dialog.token
    else:
        login = {'username': dialog.username,
                 'password': dialog.password}
        response = requests.get(f'{nomad_url}/auth/token', params=login)
        check_response(response, 'Login failed!')
        token = response.json()['access_token']
        auth = {'Authorization': f'Bearer {token}'}
    return token

def ensure_login(parent=None):
    """Is always the first function to be called. Thus this function updates
    possible changes in the used NOMAD URL. If the URL is different to the last
    used one, `logout_of_nomad` is called. Then, if `token` is empty,
    `login_to_nomad` is called.

    Parameters
    ----------
    parent : QWidget
        the parent widget for the login dialog of `login_to_nomad`"""
    global nomad_url
    if 'NOMAD_URL' in variables_handling.preferences:
        url = variables_handling.preferences['NOMAD_URL']
        if url and url != nomad_url:
            nomad_url = url
            logout_of_nomad()
    if not token:
        login_to_nomad(parent)

def check_response(response, fail_info=''):
    """Checks the given `response` from NOMAD and raises an Exception if the
    request did not work.

    Parameters
    ----------
    response : requests.Response
        Response from the server. Its status code will be checked.
    fail_info : str
        (Default value = '')
        If this string is not empty, it will display as the first part of the
        raised exception. Usefull to specify, what went wrong.
    """
    if response.status_code != 200:
        info = response.json()
        if fail_info:
            except_string = f'{fail_info}\n'
        else:
            except_string = ''
        except_string += dict_recursive_string(info)
        raise Exception(except_string)


def logout_of_nomad():
    """Resets the global `token` to an empty string, thus logging out of NOMAD."""
    global token, auth
    token = ''
    auth = {'Authorization': f'Bearer {token}'}

def get_user_uploads(parent=None):
    """Provides the uploads of the logged in user. If there is no login token, `login_to_nomad` will be called.

    Parameters
    ----------
    parent : QWidget
        the parent widget for the login dialog of `login_to_nomad`

    Returns
    -------
    the user's uploads
    """
    ensure_login(parent)
    response = requests.get(f'{nomad_url}/uploads', headers=auth)
    check_response(response, 'Could not get uploads!')
    return response.json()['data']


def get_user_upload_names(parent=None):
    """Provides a list of the uploads belonging to the logged in user by their
    name.

    Parameters
    ----------
    parent : QWidget
        the parent widget for the login dialog of `login_to_nomad`

    Returns
    -------
    list[str]
        the names of the uploads belonging to the user
    """
    uploads = get_user_uploads(parent)
    upload_names = []
    for upload in uploads:
        if 'upload_name' in upload:
            upload_names.append(upload['upload_name'])
        else:
            upload_names.append(upload['upload_id'])
    return upload_names

def upload_file(file, upload_name, upload_path='CAMELS_data',
                overwrite_if_exists=True, parent=None):
    """
    Uploads a file into a given NOMAD upload.

    Parameters
    ----------
    file : str, path
        the path of the file that should be uploaded
    upload_name : str
        the upload_name or upload_id of the upload, where the file should go
    upload_path : str
        (Default value = 'CAMELS_data')
        the path inside the upload on NOMAD where the file should go
    overwrite_if_exists : bool
        (Default value = True)
        if set to True , overwrites the file if it already exists
    parent : QWidget
        the parent widget for the login dialog of `login_to_nomad` (if needed)
    """
    uploads = get_user_uploads(parent)
    upload_id = None
    for upload in uploads:
        if 'upload_name' not in upload and upload['upload_id'] == upload_name:
            upload_id = upload_name
            break
        if upload['upload_name'] == upload_name:
            upload_id = upload['upload_id']
            break
    if not upload_id:
        raise Exception(f'Could not find upload {upload_name}!')
    params = {
        'overwrite_if_exists': 'true' if overwrite_if_exists else 'false',
        'file_name': os.path.basename(file),
    }
    head = {'accept': 'application/json'}
    head.update(auth)
    response = requests.put(f'{nomad_url}/uploads/{upload_id}/raw/{upload_path}',
                            data=f, headers=head, params=params)
    check_response(response, 'Failed to upload to NOMAD!')
    return response

def get_user_information(parent=None):
    """Retrieves the information of the logged in user.

    Parameters
    ----------
    parent : QWidget
        the parent widget for the login dialog of `login_to_nomad` (if needed)

    Returns
    -------
    the response's data, i.e. the user information
    """
    ensure_login(parent)
    response = requests.get(f'{nomad_url}/users/me', headers=auth)
    check_response(response, 'Could not get user information from NOMAD')
    return response.json()



if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # f = r"C:\Users\od93yces\Downloads\sic_TS.blend"
    # up = get_user_upload_names()[0]
    # dat = get_user_information()
    # print(dat)
    print(get_user_information())
