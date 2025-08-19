# macOS - Installation

```{warning}
NOMAD CAMELS might not work on Apple Silicon devices like the M1, M2, etc.
```

## 1. Python Installation

There are two ways to install Python on your mac:

1. Direct Python installtion using homebrew
2. Installation using Pyenv

```{note}
Use Pyenv if you want to be abl to easily manage different Python versions (for example 3.9 and 3.11) on your system at the same time.
```

### 1.1 Install homebrew

[See here](https://brew.sh/) for information on how to install `homebrew`.

### 1.2 Direct Installation

After you installed `homebrew` and simply want a single Python version to run on your system run this command in the terminal:

```
brew install python
```

### 1.3 Using Pyenv

Use `homebrew` to install [pyenv](https://github.com/pyenv/pyenv). 

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
#### 1.3.1 Python Installation
- Restart terminal
- Type in to the terminal 
  ```
  pyenv install <python_version>
  ``` 
  for example `pyenv install 3.9`.\
`<python_version>` is the Python version you want to install (3.9 or higher is suggested for NOMAD-CAMELS).  

## 2. Install CAMELS

### 2.1 Using Direct Install

You can simply run

```bash
pip3 install nomad-camels
```

### 2.2 Using Pyenv

- Create a folder where you want to install CAMELS (e.g. `NOMAD-CAMELS/`)
- Type in your terminal
   ```bash
   cd NOMAD-CAMELS
   pyenv local <python_version>
   ```
- If you have a working Python environment (`python3 -V` in `/NOMAD-CAMELS/` returns `<python_version>`) then you can continue to install CAMELS.
- Now  run the command 
    ```
    python3 -m venv .desertenv
    ``` 
    in this folder to create a virtual Python environment (using the Python version given by `pyenv local <python_version>`)
- Now  activate the environment with 
   ```bash
   source .desertenv/bin/activate
   ```
- Now type 
  ```bash
  pip install nomad-camels 
  ```

  to install CAMELS.


```{note}
<a href="../tutorials/quick_start.html" style="display: inline-block; padding: 12px 20px; background-color: #ffffff; color: #4CAF50; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px; margin: 10px 0; font-weight: bold; border: 4px solid #4CAF50">
    Getting Started
</a><br>
When you are done with the installation, get started with our guide. 
```

## 3. Run CAMELS

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
python3 .\CAMELS_start.py
```

or run:

```bash
python3 ./desertenv/lib/python<version>/site-packages/nomad_camels/CAMELS_start.py
```

