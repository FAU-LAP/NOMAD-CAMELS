import os.path
import requests
from PySide6.QtWidgets import QDialog

from nomad_camels.ui_widgets.login_dialog import LoginDialog


base_url = 'http://nomad-lab.eu/prod/v1/staging/api/v1'

token = ''
token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJmb1hmZnM5QlFQWHduLU54Yk5PYlExOFhnZnlKU1FNRkl6ZFVnWjhrZzdVIn0.eyJqdGkiOiJlMjllYTdjYS0yYTkyLTQxODMtODc3ZS1mMDExZTkyOWI2YmMiLCJleHAiOjE2ODk4NjMzNjgsIm5iZiI6MCwiaWF0IjoxNjg5Nzc2OTY4LCJpc3MiOiJodHRwczovL25vbWFkLWxhYi5ldS9mYWlyZGkva2V5Y2xvYWsvYXV0aC9yZWFsbXMvZmFpcmRpX25vbWFkX3Byb2QiLCJzdWIiOiJlZWFlOGNjZC00MDA0LTQwNDEtOGNiZC1lOWE5MWFiZDc3ZjMiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJub21hZF9wdWJsaWMiLCJhdXRoX3RpbWUiOjAsInNlc3Npb25fc3RhdGUiOiI2NGRkODA2OC1kZmRmLTQxMDEtOTk1NS1hNzFmM2VkYzRkMTQiLCJhY3IiOiIxIiwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJKb2hhbm5lcyBMZWhtZXllciIsInByZWZlcnJlZF91c2VybmFtZSI6ImpvLWxlaCIsImdpdmVuX25hbWUiOiJKb2hhbm5lcyIsImZhbWlseV9uYW1lIjoiTGVobWV5ZXIiLCJlbWFpbCI6ImpvaGFubmVzLmxlaG1leWVyQGZhdS5kZSJ9.epcIv-RHYLLs2OjCwH1zqA-0Ogj5t34hY4riDMA_41RWcnPZITgs0ZFYN5kvCyTAlM-0qLAOMD2FCp7sdvkR_WfTAfR48XwPLhRSvWn73cS7sncLXlr5sONdfdmQgiclSDvws_MkvAqG_O5SqLJyNcHrRPUo3E-_LSnbR6z65ATGPcK_ER79Nh_Ght4Q_2YfUqtALvEpx4oeWkKZovPxOpzcf2BzLhNc5RXi_dvqCWUsd4NjM1Au-BngV4bOJGdXT0nKqcEDYPxNYoNTNQXVyPmaSlXvVxmwVMm6Vky-_D7u4p6XXwKGia2Ngj4iey-_tM3ZTheOEOWqBSxTiOlC8A'
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
    global token, auth
    dialog = LoginDialog(parent)
    if dialog.exec() != QDialog.Accepted:
        return
    login = {'username': dialog.username,
             'password': dialog.password}
    response = requests.get(f'{base_url}/auth/token', params=login)
    token = response.json()['access_token']
    auth = {'Authorization': f'Bearer {token}'}
    return token

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
    if not token:
        login_to_nomad(parent)
    response = requests.get(f'{base_url}/uploads', headers=auth)
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
    return requests.put(f'{base_url}/uploads/{upload_id}/raw/{upload_path}',
                        data=f, headers=head, params=params)





if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    f = r"C:\Users\od93yces\Downloads\sic_TS.blend"
    up = get_user_upload_names()[0]
    print(upload_file(f, up).json())

