# macOS - Installation Using Pyenv

## 1. Pyenv and Python Installation

Use `homebrew` to install pyenv ([see here](https://brew.sh/) for more information on how to install `homebrew`).

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
  for example `pyenv install 3.9`.\
`<python_version>` is the Python version you want to install (3.9 or higher is suggested for NOMAD-CAMELS).  

## 3. Install CAMELS
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

## 4. Run CAMELS

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

