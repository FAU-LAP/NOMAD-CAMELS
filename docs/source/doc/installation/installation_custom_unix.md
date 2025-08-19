# Linux Installation

NOMAD CAMELS is a Python package. We suggest to install CAMELS into a new Python environment to prevent it from interfering with other packages and dependencies.

An easy way to install a specific Python version and create a virtual environment is using `pyenv`.

If you already have a Python environment you want to install CAMELS into you can directly go to [chapter 4](#4-install-nomad-camels).

## 1. Pyenv Installation
See the [official Pyenv installation guide](https://github.com/pyenv/pyenv#installation) for more details and the most recent version.

- Install pyenv to install the necessary Python version 
  
  ```{attention}
  you do not need to do this if you already have the correct Python version installed:
  ```

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

- Run the following command
  ```
  pyenv install <python_version>
  ``` 
  for example `pyenv install 3.11.3`.\
`<python_version>` is the Python version you want to install (3.11.3 or higher is suggested for NOMAD-CAMELS).

## 3. Create Virtual Environment

- Create a folder where you want to install CAMELS (e.g. `\NOMAD-CAMELS\`)
- Type in your shell 
  ```
  cd \NOMAD-CAMELS\;pyenv local <python_version> 
  ```
- If you have a working Python environment (`python -V` in `/NOMAD-CAMELS/` returns `<python_version>`) then you can continue to install CAMELS.
- Now  run the command 
  ```
  python -m venv .desertenv
  ``` 
  in this folder to create a virtual Python environment (using the Python version given by `pyenv local <python_version>`)
- Now  activate the environment with 
  ```
  source ./.desertenv/bin/activate
  ```

## 4. Install NOMAD CAMELS

To install CAMELS run this command:

```bash
pip install nomad-camels 
```

```{note}
<a href="../tutorials/quick_start.html" style="display: inline-block; padding: 12px 20px; background-color: #ffffff; color: #4CAF50; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px; margin: 10px 0; font-weight: bold; border: 4px solid #4CAF50">
    Getting Started
</a><br>
When you are done with the installation, get started with our guide. 
```

## 5. Run CAMELS

You can then run 

```bash
nomad-camels
```

 or  

```bash
python -m nomad_camels
```

to start CAMELS.

If this does not work for you you can go to `/.desertenv/Lib/site-packages/nomad_camels/` and run CAMELS using

```bash
python .\CAMELS_start.py
```

or run:

```bash
python ./desertenv/lib/python<version>/site-packages/nomad_camels/CAMELS_start.py
```

```{attention}
If you have trouble starting CAMELS due to Qt issues like: 

    `Could not load the Qt platform plugin 'xcb'` 

check to see if our [troubleshooting](#6-troubleshooting) step can solve this for you.
```



## 6. Troubleshooting
Sometimes packages that are needed to run the `Qt` libraries used for the GUI need to be installed additionally. The following should install all necessary packages:
```bash
sudo apt-get install build-essential libssl-dev libffi-dev libegl1 libdbus-1-3 libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcb-xinput0 libxcb-xfixes0 x11-utils libxcb-cursor0 libopengl0 libegl1-mesa libgl1-mesa-glx libpulse0
```
