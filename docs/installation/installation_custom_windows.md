---
layout: default
title: Custom Windows Installation
parent: Installation
nav_order: 2
---

## Table of contents
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

# Custom Windows Installation

## 1. Pyenv Installation

- Install pyenv to install necessary python version (you do not need to do this if you already have a python versioning software like Anaconda installed):
- Type in to the powershell:
```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
## 2. Python Installation
- Restart the powershell
- Then type in to the powershell `pyenv install <python_version>` for example `pyenv install 3.11.3`.
`<python_version>` is the python version you want to install (3.11.3 or higher is suggested for NOMAD-CAMELS).
## 3. Install CAMELS
- Create a folder where you want to install CAMELS (e.g. `\NOMAD-CAMELS\`)
- Type in your powershell `cd \NOMAD-CAMELS\;pyenv local <python_version> `
- If you have a working python environment (`python -V` in `/NOMAD-CAMELS/` returns `<python_version>`) then you can continue to install CAMELS.
- Now  run the command `python -m venv .desertenv` in this folder to create a virtual python environment (using the python version given by `pyenv local <python_version>`)
- Activate the environment with `.\.desertenv\Scripts\activate`
- Now type
  ```bash
  pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nomad-camels 
  ```
   to install CAMELS.
## 4. Run CAMELS
Go to `/.desertenv/Lib/site-packages/nomad_camels/` and run CAMELS using
```bash
python .\CAMELS_start.py
```


<p style="text-align:left;">
  <span style="color: grey;">
  <a href="./installation_installer.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="./installation_custom_unix.html">Next &rarr;</a><br>
  </span>
</p>
