---
layout: default
title: Installation
nav_order: 1
---



# CAMELS Installation

As NOMAD-CAMELS (from now on only 'CAMELS') is written in python it requires a working python environment to run properly.
The [installer.exe](#1-using-the-camels_installerexe) takes care of all of this for you.

With the correct python version (>=3.9.6) CAMELS can simply be installed using `pip`
(but this is not recommended! Try and use the installer if possible):
```bash
pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nomad-camels
```
**This will install CAMELS in to your python environment but does not create all necessary folders under %localappdata% for example. Only use this if you know what you are doing!**\
This installs CAMELS as a python package into your package library (`\*env*\Lib\site-packages\NOMAD-CAMELS\`, where `*env*` is the path to the python environment used with the `pip install` command).


[comment]: <> (# Installing on Windows)

If you do not have python installed on your machine or a clean python environment you have two options:
1. [Using the installer](#1-using-the-camels_installerexe) (**RECOMENDED**, Windows only)
2. [Custom installation](#2-custom-installation)


## 1. Using the CAMELS_installer.exe (Windows)
Simply download the CAMELS installer (.exe) from *[here](https://github.com/A-D-Fuchs/CAMELS_installer/blob/main/Output/NOMAD-CAMELS_installer.exe)*\
Run the installer. Admin rights should not be required. 

- Creates all necessary folders and files
- This installes pyenv to `%userprofile%\.pyenv\`
- Installes Python 3.9.6. using pyenv
- Creates the correct python environment (called .desertenv using the pyenv 3.9.6 python version)
- Installs CAMELS (using pip in the .desertenv environment)

This takes about 2-3 minutes depending on your machine.\
Try to always use this option as it minimizes any unwanted errors during setup and makes running and removing/uninstalling easy.

## 2. Custom Installation

### 2.1 Install python

- Install pyenv to install any python version (you do not need to do this if you already have a python versioning software like Anaconda installed):
- Type in to the powershell:
```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
- Then type in to the powershell `pyenv install <python_version>` for example `pyenv install 3.9.6`.
`<python_version>` is the python version you want to use that is 3.9.6 or higher.
### 2.2 Install CAMELS
- Create a folder where you want to install CAMELS (e.g. `\NOMAD-CAMELS\`)
- Type in your powershell `cd \NOMAD-CAMELS\;pyenv local <python_version> `
- If you have a working python environment (`python -V` in `/NOMAD-CAMELS/` returns `<python_version>`) then you can continue to install CAMELS.
- Now simply run the command `python -m venv .desertenv` in this folder to create a virtual python environment (using the python version given by `pyenv local <python_version>`)
- Now simply activate the environment with `.\.desertenv\Scripts\activate`
- Now type
```bash
pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nomad-camels 
```
   to install CAMELS.

### 2.3 Create necessary folders
- Create the folder `%localappdata%\CAMELS\Presets\Backup` manually

## 3. Errors and Bugs
As CAMELS is currently under development errors and bugs can occur. We are working hard to keep the number of bugs small.\
Here are some Errors and ways you might be able to fix them
- **CATALOG_KEY_ERROR:**\
This mostly occurs when starting CAMELS for the first time and is caused by a missing catalog file (for bluesky) in your folders. CAMELS normaly creates this file when you start it for the first time and you simply need to restart CAMELS again for it to work
- **PRESETS folder missing:**\
This occurs when CAMELS can't find `%localappdata%\NOMAD-CAMELS\Presets\Backup` where all your settings are stored.\
If this error occurs then simply add these folders (`Presets` and `Backup`) to `%localappdata%`.
- **Install fails randomly**\
If your installation fails randomly (setup of python environment takes less than a few seconds) and you can't run CAMELS with the created shortcuts then it is poissible that your pyenv PATH variables are not set correctly. Open powershell and  see if the `pyenv` command works.\
Set the correct PATH variables for pyenv and retry the installation again.
## 4. Uninstalling CAMELS
To remove CAMELS simply run the uninstaller. This is only possible if you used the installer.exe to install CAMELS in the first place.\
The uninstaller does not remove your Presets and Backups (of the presets) under `%localappdata%\NOMAD-CAMELS` manually delete these files if you are sure you don't need them anymore. \
The `.pyenv` folder and any python versions installed with pyenv are **NOT** removed when uninstalling.\
`.pyenv` can be found in `%userprofile%`. Manually remove this if you do not need it anymore.\
**Beware that removing this might break OTHER applications or scripts that rely on python versions installed with pyenv!**


<p style="text-align:left;">
  <span style="color: grey;">
  <a href="../index.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="quick_start.html">Next &rarr;</a><br>
  </span>
</p>
