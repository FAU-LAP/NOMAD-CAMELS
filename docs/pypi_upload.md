---
layout: default
title: PyPi Upload
parent: Programmer's Guide
nav_order: 1
---
# Uploading a new NOMAD-CAMELS version to PyPi
The "backbone" of creating the PyPi project is the `pyproject.toml` file located in the root directory. Here almost all important settings are configured. The dependencies on other python packages is maintained with the `requirements.txt` file. \
The `MANIFEST.in` file contains information about static non-python files that should be included (e.g. folders of images). 

## Upload Workflow
1. Make your desired changes in the `nomad_camels` folder (the main app folder). 
2. Run 
   ```bash
   python -m build
   ``` 
   in the folder where the `pyproject.toml` file is located (should be located in the parent folder of the `nomad_camels` folder). This creates the successful builds (`nomad_camels-X.Y.Z.tar.gz` and `nomad_camels-X.Y.Z-py3-none-any.whl`) in `/dist/`.  \
   The folder structure should look something like this:
   ```
   main_folder/
   |--- dist/
         |--- nomad_camels-X.Y.Z.tar.gz
         |--- nomad_camels-X.Y.Z-py3-none-any.whl
   |--- pyproject.toml
   |--- requirements.txt
   |--- MANIFEST.in
   |--- nomad_camels/
         |--- MainApp.py
         |--- 'many other files ...' 
   ```
   where X.Y.Z is the version number (MAJOR.MINOR.PATCH) given in the `.toml` file. 
3. To upload the builds to PyPi (**!currently uploads to TestPyPi as it is under development!**) run:
    ```bash
    python -m twine upload --repository testpypi dist/nomad*
    ```

   > &#x26A0; Make sure there are only the newly built files in `dist/` that match `nomad*`. If you have multiple build files in `dist/` the upload might not work as desired.
   
   Now enter `__token__` as the username and enter your saved API token as the password to complete the upload.
4. The new version should then be available on https://test.pypi.org/project/nomad-camels/

## Install
To install the most recent version of NOMAD-CAMELS into your python environment run
```bash
    pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nomad-camels
```
The `--extra-index-url` flag allows dependencies to be installed from PyPi.\
The `--no-cache-dir` flag prevents any locally saved NOMAD-CAMELS version to be installed instead of the most recent remote version. 
<p style="text-align:left;">
  <span style="color: grey;">
  <a href="../index.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="quick_start.html">Next &rarr;</a><br>
  </span>
</p>