# Using the CAMELS Installer for Windows
 download the CAMELS installer (.exe file) from [here](https://github.com/A-D-Fuchs/CAMELS_installer/blob/main/Output/NOMAD-CAMELS_installer.exe)\
Run the installer. Admin rights should not be required. 

- Creates all necessary folders and files
- Installs pyenv to `%userprofile%/.pyenv/`
- Installs Python 3.11.3. using pyenv
- Creates the correct python environment (called `.desertenv` using the pyenv 3.11.3 python version)
- Installs CAMELS (using pip in the `.desertenv` environment)

This takes about 2-3 minutes depending on your systems performance.

> &#9888; Try to always use this option as it minimizes any unwanted errors during setup and makes running and removing/uninstalling easy.

You have the option to also perform a custom installation for windows described [here](installation_custom_windows.md).
