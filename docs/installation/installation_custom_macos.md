---
layout: default
title: Custom MacOS Installation
parent: Installation
nav_order: 4
---



<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>


# Custom macOS Installation 

## 1. Pyenv and Python Installation
This uses `homebrew` to install pyenv ([see here](https://brew.sh/) for more information on `homebrew`).
- Run
  ```bash
  brew update
  brew install pyenv
  ```
  to install pyenv.
- You need Xcode command line tools
  ```bash
  xcode-select --install
  ```
- Then install dependencies
  ```bash
  brew install openssl readline sqlite3 xz zlib
  ```  
## 2. Python Installation
- Restart terminal
- Type in to the terminal 
  ```
  pyenv install <python_version>
  ``` 
  for example `pyenv install 3.11.3`.\
`<python_version>` is the python version you want to install (3.11.3 or higher is suggested for NOMAD-CAMELS).  

## 3. Install CAMELS
- Create a folder where you want to install CAMELS (e.g. `\NOMAD-CAMELS\`)
- Type in your powershell `cd \NOMAD-CAMELS\;pyenv local <python_version> `
- If you have a working python environment (`python -V` in `/NOMAD-CAMELS/` returns `<python_version>`) then you can continue to install CAMELS.
- Now  run the command `python -m venv .desertenv` in this folder to create a virtual python environment (using the python version given by `pyenv local <python_version>`)
- Now  activate the environment with `.\.desertenv\Scripts\activate`
- Now type
  ```bash
  pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nomad-camels 
  ```
  to install CAMELS.
## 4. Run CAMELS
Go to `/.desertenv/Lib/site-packages/nomad_camels/` and run CAMELS using
```bash
python CAMELS_start.py
```



<p style="text-align:left;">
  <span style="color: grey;">
  <a href="./installation_custom_unix.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="./installation_bugs_errors.html">Next &rarr;</a><br>
  </span>
</p>
