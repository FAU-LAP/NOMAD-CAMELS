---
title: Home
layout: home
---
![Logo](assets/camels-horizontal.svg)

# CAMELS
## Configurable Application for Measurements, Experiments and Laboratory Systems

CAMELS is a configurable measurement software, targeted towards the requirements of experimental solid-state physics. Here many experiments utilize a multitude of measurement devices used in dynamically changing setups. CAMELS will allow to define instrument control and measurement protocols using a graphical user interface (GUI). This provides a low entry threshold enabling the creation of new measurement protocols without programming knowledge or a deeper understanding of device communication.

The GUI generates python code that interfaces with instruments and allows users to modify the code for specific applications and implementations of arbitrary devices if necessary. Even large-scale, distributed systems can be implemented. CAMELS is well suited to generate FAIR-compliant output data. NeXus standards, immediate NOMAD integration and hence a FAIRmat compliant data pipeline can be readily implemented.

# CAMELS Installer
test2
As CAMELS is written in python it requires a working python environment to run properly. 

With the correct python version (>3.9.6) CAMELS can simply be installed using `pip` 
(but this is not recomended! Try and use the installer if possible):

    pip install git+https://github.com/FAU-LAP/CAMELS.git

This installs CAMELS as a python package into your package library (`\*env*\Lib\site-packages\CAMELS\`, where `*env*` is the path to the python environment used with the `pip install` command).

# Installing on Windows

If you do not have python installed on your machine or a clean python environment you have two options: 
1. Using the installer (**RECOMENDED**)
2. Custom installation


## 1. Using the CAMELS_installer.exe
Simply download the CAMELS installer (.exe) from the *[Homepage](https://fau-lap.github.io/CAMELS/)*

Run the installer. Admin rights should not be rquired.

- Creates all necessary folders and files
- This installes pyenv to `%userprofile%\.pyenv\`
- Installes Python 3.9.6. using pyenv
- Creates the correct python environment (called .desertenv using the pyenv 3.9.6 python version)
- Installs CAMELS (using pip in the .desertenv environment)

This takes about 2-3 minutes depending on your machine.

Try to always use this option as it minimizes any unwanted errors during setup and makes running and removing/uninstalling easy.

## 2. Custom Installation 

### Install python

- Install pyenv to install any python version (you do not need to do this if you already have a python versioning software like Anaconda installed):
- Type in to the powershell:
  `Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"`
- Then type in to the powershell `pyenv install 3.9.6`
- Create a folder where you want to install CAMELS (e.g. `\NOMAD-CAMELS\`)
- Type in your powershell `cd \NOMAD-CAMELS\;pyenv local 3.9.6. `
- Now simply run the command `python -m venv .desertenv` in this folder to create a virtual python environment (using the python version given by `pyenv local <version>`)
- Now simply activate the environment with `.\.desertenv\Scripts\activate`
- Now type `pip install git+https://github.com/FAU-LAP/CAMELS.git@development` to install CAMELS
- Create the folder `%localappdata%\CAMELS\Presets\Backup` manually

