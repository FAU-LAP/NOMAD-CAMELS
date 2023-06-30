# Custom UNIX Installation Using Pyenv

## 1. Pyenv Installation
See the [official Pyenv installation guide](https://github.com/pyenv/pyenv#installation) for more details and the most recent version.

- Install pyenv to install the necessary Python version (you do not need to do this if you already have the correct Python version installed):
  ```bash
  sudo apt-get install git
  curl https://pyenv.run | bash
  ```
- For **bash**:\
Stock Bash startup files vary widely between distributions in which of them source which, under what circumstances, in what order and what additional configuration they perform. As such, the most reliable way to get Pyenv in all environments is to append Pyenv configuration commands to both `.bashrc` (for interactive shells) and the profile file that Bash would use (for login shells).

  First, add the commands to `~/.bashrc` by running the following in your terminal:
  ```bash
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
  echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
  echo 'eval "$(pyenv init -)"' >> ~/.bashrc
  ```
- Then, if you have `~/.profile`, `~/.bash_profile` or `~/.bash_login`, add the commands there as well. If you have none of these, add them to `~/.profile`.
- To add to `~/.profile`:  
  ```bash
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
  echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
  echo 'eval "$(pyenv init -)"' >> ~/.profile
  ```
- To add to `~/.bash_profile`:  
  ```bash
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
  echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
  echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
  ```
- For **Zsh** and **Fish shell** see [official guide](https://github.com/pyenv/pyenv#installation)
- Restart your shell for the `PATH` changes to take effect:
  ```bash
  exec "$SHELL"
  ```
- Install Python [build dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) before attempting to install a new Python version.
- **You can now begin using Pyenv.**
## 2. Python Installation
- Type in to the terminal 
  ```
  pyenv install <python_version>
  ``` 
  for example `pyenv install 3.11.3`.\
`<python_version>` is the python version you want to install (3.11.3 or higher is suggested for NOMAD-CAMELS).
## 3. Install CAMELS
- Create a folder where you want to install CAMELS (e.g. `\NOMAD-CAMELS\`)
- Type in your powershell `cd \NOMAD-CAMELS\;pyenv local <python_version> `
- If you have a working Python environment (`python -V` in `/NOMAD-CAMELS/` returns `<python_version>`) then you can continue to install CAMELS.
- Now  run the command `python -m venv .desertenv` in this folder to create a virtual Python environment (using the Python version given by `pyenv local <python_version>`)
- Now  activate the environment with `.\.desertenv\Scripts\activate`
- Now type
```bash
pip install nomad-camels 
```
   to install CAMELS.
## 4. Run CAMELS
Go to `/.desertenv/Lib/site-packages/nomad_camels/` and run CAMELS using
```bash
python CAMELS_start.py
```
