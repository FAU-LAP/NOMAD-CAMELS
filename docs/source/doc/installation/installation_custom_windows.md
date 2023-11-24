# Windows - Installation Using Pyenv

## 1. Pyenv Installation

- Install pyenv to install necessary Python version (you do not need to do this if you already have a Python versioning software like Anaconda installed):
- To install pyenv run in the powershell:
```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
## 2. Python Installation
- Restart the powershell
- Then run in the powershell 
```
pyenv install <python_version>
``` 
for example 
```
pyenv install 3.11.3
```
`<python_version>` is the Python version you want to install (3.11.3 or higher is suggested for NOMAD-CAMELS).
## 3. Install CAMELS
- Create a folder where you want to install CAMELS (e.g. `\NOMAD-CAMELS\`)
- Run in your powershell 
  ```
  cd \NOMAD-CAMELS\;pyenv local <python_version>
  ```
- If you have a working Python environment (`python -V` in `/NOMAD-CAMELS/` returns `<python_version>`) then you can continue to install CAMELS.
- Now  run the command 
  ```
  python -m venv .desertenv
  ``` 
  in this folder to create a virtual Python environment (using the Python version given by `pyenv local <python_version>`)
- Activate the environment with 
   ```bash
  .\.desertenv\Scripts\activate
  ```
- Now type
  ```bash
  pip install nomad-camels 
  ```
   to install CAMELS.
## 4. Run CAMELS
Go to `/.desertenv/Lib/site-packages/nomad_camels/` and run CAMELS using
```bash
python .\CAMELS_start.py
```