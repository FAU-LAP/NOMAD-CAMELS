---
layout: default
title: Errors and Bugs during Installation
parent: Installation
nav_order: 5
---

# Errors and Bugs
As CAMELS is currently under development errors and bugs can occur. We are working hard to keep the number of bugs small.\
Here are some Errors and ways you might be able to fix them
- **CATALOG_KEY_ERROR:**\
This mostly occurs when starting CAMELS for the first time and is caused by a missing catalog file (for bluesky) in your folders. CAMELS normaly creates this file when you start it for the first time and you simply need to restart CAMELS again for it to work
- **PRESETS folder missing:**\
This occurs when CAMELS can't find `%localappdata%\NOMAD-CAMELS\Presets\Backup` where all your settings are stored.\
If this error occurs then simply add these folders (`Presets` and `Backup`) to `%localappdata%`.
- **Install fails randomly**\
If your installation fails randomly (setup of python environment takes less than a few seconds) and you can't run CAMELS with the created shortcuts then it is poissible that your pyenv PATH variables are not set correctly. Open powershell and  see if the `pyenv` command works.\
Set the correct PATH variables for pyenv and retry the installation again.\
**Alternative:**\
You can remove pyenv by deleting the `/.pyenv/` folder or running 
    ```powershell
    .\install-pyenv-win.ps1 -uninstall
    ``` 
  The `install-pyenv-win.ps1` script is located in `/.pyenv/pyenv-win/`.


<p style="text-align:left;">
  <span style="color: grey;">
  <a href="./installation_custom_macos.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="./installation_uninstall.html">Next &rarr;</a><br>
  </span>
</p>
