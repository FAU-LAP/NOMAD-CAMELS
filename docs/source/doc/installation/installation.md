# CAMELS Installation

CAMELS is written in Python and requires the correct Python environment to run properly.

In the most basics cases a simple installation using _pip_ is sufficient. To install CAMELS to an existing Python environment (must be Python version 3.9.6 or newer) simply run

```bash
pip install nomad-camels
```

You can then run 

```bash
nomad-camels
```

 or  

```bash
python -m nomad_camels
```

to start CAMELS.

If this does not work you can go to `/.desertenv/Lib/site-packages/nomad_camels/` and run

```bash
python .\CAMELS_start.py
```


There are several ways to set up the correct Python environment and install CAMELS depending on your operating system:
```{toctree}
:maxdepth: 2

Windows Installer <installation_installer.md>
pyenv on Windows <installation_custom_windows.md>
pyenv on Linux <installation_custom_linux.md>
pyenv on macOS <installation_custom_macos.md>
Anaconda <installation_custom_anaconda/installation_custom_anaconda.md>
```
