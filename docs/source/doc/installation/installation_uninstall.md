# Uninstalling CAMELS
## Windows Installer
To remove CAMELS simply run the uninstaller. This is only possible if you used the installer.exe to install CAMELS in the first place.

The uninstaller does not remove your Presets and Backups (of the presets) under `%localappdata%\NOMAD-CAMELS` manually delete these files if you are sure you don't need them anymore. 

The `.pyenv` folder and any python versions installed with pyenv are **NOT** removed when uninstalling.

`.pyenv` can be found in `%userprofile%`. Manually remove this if you do not need it anymore.

**Beware that removing this might break OTHER applications or scripts that rely on python versions installed with pyenv!**

## Pyenv & Anaconda
If you used pyenv or Anaconda to install CAMELS, simply run  
```bash
pip uninstall nomad-camels
```
with the correct environment activated.
You can also simply delete the entire folder containing the python environment.
The data and presets folders must be deleted manually.

