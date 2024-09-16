# CAMELS Installation

CAMELS is written in Python and requires the correct Python environment to run properly. There are several ways to set up the correct Python environment and install CAMELS depending on your operating system:

<div class="box-container">
  <a href="installation_installer.html" class="box">
    <span class="box-title">Windows Installer</span>
    <p class="box-content">We recommend to install CAMELS with the installer if you are using <strong>Windows</strong>. This will install Python 3.11 and create the required Python environment for you.</p>
  </a>
  <a href="installation_custom_unix.html" class="box">
    <span class="box-title">Manual Installation on Linux</span>
    <p class="box-content">Installation guide for Linux-type systems like Ubuntu, Debian and CentOS. Install Python, setup the environment and run CAMELS.</p>
  </a>
  <a href="installation_custom_macos.html" class="box">
    <span class="box-title">Manual Installation on macOS</span>
    <p class="box-content">Installation guide for systems running macOS. Install Python, setup the environment and run CAMELS.</p>
  </a>

  <a href="installation_custom_windows.html" class="box">
    <span class="box-title">Manual Installation on Windows</span>
    <p class="box-content">If you are familiar with Python and Python environments you can manually install CAMELS. Install Python, setup the environment and run CAMELS.</p>
  </a>

  <a href="installation_custom_anaconda.html" class="box">
    <span class="box-title">Manual Installation using Anaconda</span>
    <p class="box-content">If you already have Anaconda installed on your machine you can use it to install CAMELS.</p>
  </a>

</div>

In the most basics cases a simple installation using _pip_ is sufficient. To install CAMELS to an existing Python environment (must be Python version 3.11.3 or newer) simply run

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

```{warning}
Some of the drivers do not support Python 3.12 yet, so we suggest to stay with Python 3.11.
```