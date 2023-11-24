# Using the CAMELS Installer on Windows
Download the CAMELS installer (.exe file) from [GitHub](https://github.com/A-D-Fuchs/CAMELS_installer/blob/main/Output/NOMAD-CAMELS_installer.exe).\
Run the installer. Admin rights should not be required. 

The installer automatically does the following steps:
- Creates all necessary folders and files
- Installs pyenv to `%userprofile%/.pyenv/` if it is not already installed
- Installs Python 3.11.3. using pyenv
- Creates the correct python environment (called `.desertenv` using the pyenv 3.11.3 python version)
- Installs CAMELS (using pip in the `.desertenv` environment)

This takes about 2-3 minutes depending on your systems performance.

```{note}
  Try to always use this option as it minimizes any unwanted errors during setup and makes running and uninstalling easy.
```

If the installer fails or if you want more control over your installation you can also use [pyenv](installation_custom_windows.md) or [Anaconda](installation_custom_anaconda) to install CAMELS.

# Troubleshooting
If your installation fails randomly (setup of Python environment takes less than a few seconds) and you can't run CAMELS with the created shortcuts then it is possible that your pyenv PATH variables are not set correctly. Open powershell and  see if the `pyenv` command works.\
Set the correct PATH variables for pyenv and retry the installation again.\
**Alternative:**\
Remove pyenv by deleting the `/.pyenv/` folder or by running 

```bash
.\install-pyenv-win.ps1 -uninstall
```
  in the terminal. The `install-pyenv-win.ps1` script is located in `/.pyenv/pyenv-win/`.

  Remove the `/NOMAD-CAMELS/` folder as well and restart the installer.
