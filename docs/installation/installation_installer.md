---
layout: default
title: Using the Windows Installer
parent: Installation
nav_order: 1
---

# Using the CAMELS Installer for Windows
Simply download the CAMELS installer (.exe file) from [here](https://github.com/A-D-Fuchs/CAMELS_installer/blob/main/Output/NOMAD-CAMELS_installer.exe)\
Run the installer. Admin rights should not be required. 

- Creates all necessary folders and files
- Installs pyenv to `%userprofile%/.pyenv/`
- Installs Python 3.11.3. using pyenv
- Creates the correct python environment (called `.desertenv` using the pyenv 3.11.3 python version)
- Installs CAMELS (using pip in the `.desertenv` environment)

This takes about 2-3 minutes depending on your systems performance.

> &#9888; Try to always use this option as it minimizes any unwanted errors during setup and makes running and removing/uninstalling easy.

You have the option to also perform a custom installation for windows described [here](https://fau-lap.github.io/NOMAD-CAMELS/docs/installation/installation_custom_windows.html).


<p style="text-align:left;">
  <span style="color: grey;">
  <a href="./installation.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="./installation_custom_windows.html">Next &rarr;</a><br>
  </span>
</p>
