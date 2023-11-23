# Drivers for PyPi
If you want to share your driver with others, all you have to do is create a PyPi package out of the folder you created above. 

You can of course also fork our [driver repository](https://github.com/FAU-LAP/CAMELS_drivers) and create a pull request with the new driver you wrote and we will be happy to add your driver to PyPi for you. 

Or you can also send us the files via [email](mailto:nomad-camels@fau.de) and we will add them to the repository and PyPi for you.

---

To create a PyPi package for your driver you should have the following folder structure:
```
<driver_name>
└─> dist (this is automatically created by python -m build)
    └─> nomad_camels_driver_<driver_name>-X.Y.Z.tar.gz
    └─> nomad_camels_driver_<driver_name>-X.Y.Z-py3-none-any.whl
└─> nomad_camels_driver_<driver_name> (contains the actual device communication files)
    └─> <driver_name>.py
    └─> <driver_name>_ophyd.py
└─> LICENSE.txt
└─> pyproject.toml
└─> README.md
```

The `pyproject.toml` file contains most of the relevant information concerning the package that will be uploaded to PyPi (see the [setuptools page](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)).

&#9888; Most importantly the project name and version must be set in the `pyproject.toml` file.


---

Here is an exemplary .toml file:

<details>
  <summary>Code example: pyproject.toml file for the  Keithley 237</summary>

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "nomad_camels_driver_keithley_237"
version = "0.1.4"
authors = [
    { name="FAIRmat - HU Berlin", email="nomad-camels@fau.de" }
]
description = "Instrument driver for the Keithley 237 SMU."
readme = "README.md"
requires-python = ">=3.9.6"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
    "Operating System :: Microsoft :: Windows",
]
dependencies = [
    "pyvisa",
    "pyvisa-py"
]
[project.urls]
"GitHub Page" = "https://github.com/FAU-LAP/NOMAD-CAMELS"
"Documentation" = "https://fau-lap.github.io/NOMAD-CAMELS/"
```

</details>

---

## 1. Building the Instrument Package
To create a new package that can be installed via pip from PyPi or testPyPi follow these steps.
1. Make sure you have `build` and `twine` installed into your python environment with
   ```
   pip install build
   ``` 
   and 
   ```
   pip install twine
   ``` 

2. Go to the `<driver_name>` directory of the driver. So the parent directory containing the pyproject.toml
3. Set the correct version number and metadata in your `pyproject.toml` file
4. Run the build command : 
   ```
   python -m build
   ```
   This creates the `dist/` folder and the distributions to upload to PyPi
5. Upload to PyPi with
    ```console
    python -m twine upload dist/nomad*
    ```

---

## 2. Automated Build and Upload
You can run the following script using microsoft PowerShell in the `$rootFolder` containing multiple instrument drivers in subdirectories.\
It runs the `python -m build` and `python -m twine upload dist/nomad*` commands in each subdirectory containing a `pyproject.toml` file.

```powershell
$rootFolder = "C:\Path\To\Root\Folder"
Get-ChildItem $rootFolder -Recurse -Directory | ForEach-Object {
    if (Test-Path "$($_.FullName)\pyproject.toml") {
        Push-Location $_.FullName
        python -m build
        python -m twine upload dist/nomad*
        Pop-Location
    }
}
```


---

## 3. Install Instrument Package
To install  run
```console
pip install nomad_camels_driver_<driver_name>
```
where `nomad_camels_driver_<driver_name>` is the driver name you gave your folder and project.