---
layout: default
title: Changing CAMELS Installer
parent: Programmer's Guide
nav_order: 2
---



<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

# Changing CAMELS Installer
Installs CAMELS software and all required packages

The relevant installer [NOMAD-CAMELS_installer.exe](/Output/NOMAD-CAMELS_installer.exe) 
file is located in [Output](/Output/)

Visit the [CAMELS Homepage](https://fau-lap.github.io/CAMELS/) for more information

## 1. Workflow
Brief description of the workflow when the installer should be updated.
1. Change python code in `/Python_code/setup_camels.py` (see [here](#21-changes-to-python-or-environment))
2. Create .exe file from the python code. To do this run following code in `/Python_code/`
    ```bash
    pyinstaller --onefile --nowindow setup.py
    ```
   This creates the `setup_camels.exe` file under `/Python_code/dist/`
3. Change `"\run\runCamels.bat"` to change the way CAMELS is launched (see [here](#22-changes-to-the-way-camels-is-started-via-shortcuts))
4. Convert the bat file to an exe file (using for example [Bat To Exe Converter](https://bat-to-exe-converter-x64.de.softonic.com/))
5. Open the `CAMELS_installer.iss` file and perform any required changes. Then compile the exe.\
The final file `NOMAD-CAMELS_installer.exe` can be found under `/Output/`


## 2. What can be changed?
Brief description of the possible (and most likely) changes.
### 2.1. Changes to python or environment
If you want to perform changed regarding the NOMAD-CAMELS version that is installed or 
changes to pyenv (python version) or the python environment then you have to perform 
changes in the python code of the [setup.py](/Python_code/setup_camels.py) file. Here the python version is currently hard-coded as `3.11.3`. The `pip install` command uses the most current version of NOMAD-CAMELS and ignores locally available versions with `--no-cache-dir`.
### 2.2. Changes to the way CAMELS is started (via shortcuts)
If you want to change the way CAMELS is startet you must modify the installation.exe file by modifying the InnoSetup file `.iss`. Here you can alter the shortcuts under `[Icons]`. 
The shortcuts execute the NOMAD-CAMELS.exe which is a simple exe convertion of the batch file `runCamels.bat`. This  reads  the `NOMAD-CAMELS.ini` and reads the paths to the exe and the installation path from it. You can change these two paths manually to change the python environment that should start CAMELS. 
### 2.3. Changes to the supporting folders
For this you must modify the `.iss` file.\
The installer creates the folder `%localappdata%\nomad_camels\Presets\Backup` where all the settings presets (user info, sample info, used devices, etc.) are saved. Change the entry under `[Dirs]` to change the location of this folder.
## 3. Code Signing
To prevent an `Unknown Publisher` error when executing the `NOMAD-CAMELS_installer.exe` one has to sign the `exe` before publishing (pushing to the GitHub repo).
### 3.1. Using Windows Signtool
You can use Windows Signtool from the Windows SDK to sign your executables. 

You will need a `.pfx` certificate and the corresponding password (called `<your_pfx_password>` below).

You should `cd` into the folder where the `signtool.exe` is located. This is often in a path similar to `C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64`. 
> If you do not have a `signtool.exe` then you must install it from the [Windows SDK installer](https://developer.microsoft.com/de-de/windows/downloads/windows-sdk/). 

If you have the `signtool.exe` and are in its folder then run this in your PowerShell with **admin rights**:

```powershell
.\signtool.exe sign /f "/path/to/certificate/certificate.pfx" /p "<your_pfx_password>" /fd sha256 /t http://timestamp.sectigo.com "/path/to/NOMAD-CAMELS/installer/NOMAD-CAMELS_installer.exe"
```

For more information on the options look [here](https://learn.microsoft.com/en-us/dotnet/framework/tools/signtool-exe#sign).

The executable should now be signed and you are ready to publish the new version.

