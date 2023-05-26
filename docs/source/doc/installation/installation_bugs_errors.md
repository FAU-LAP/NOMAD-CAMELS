# Errors and Bugs
As CAMELS is currently under development errors and bugs can occur. We are working hard to keep the number of bugs small.\
Here are some Errors and ways you might be able to fix them

- **Windows Installer fails randomly**\
If your installation fails randomly (setup of python environment takes less than a few seconds) and you can't run CAMELS with the created shortcuts then it is possible that your pyenv PATH variables are not set correctly. Open powershell and  see if the `pyenv` command works.\
Set the correct PATH variables for pyenv and retry the installation again.\
**Alternative:**\
Remove pyenv by deleting the `/.pyenv/` folder or by running 
    ```bash
    .\install-pyenv-win.ps1 -uninstall
    ```
  in the terminal. The `install-pyenv-win.ps1` script is located in `/.pyenv/pyenv-win/`.

  Remove the `/NOMAD-CAMELS/` folder as well and restart the installer.


## Fixed
_Fixed issues. Kept for completeness._
- **PRESETS folder missing:**\
This occurs when CAMELS can't find `%localappdata%\NOMAD-CAMELS\Presets\Backup` where all your settings are stored.\
If this error occurs then  add these folders (`Presets` and `Backup`) to `%localappdata%`.
- **CATALOG_KEY_ERROR:**\
  This mostly occurs when starting CAMELS for the first time and is caused by a missing catalog file (for bluesky) in your folders. CAMELS normally creates this file when you start it for the first time and you need to restart CAMELS again for it to work
