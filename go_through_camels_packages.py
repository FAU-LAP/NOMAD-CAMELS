import xmlrpc.client
import subprocess
import sys
import os
import importlib
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_user_packages(username):
    # Base URL for PyPI XML-RPC API
    client = xmlrpc.client.ServerProxy("https://pypi.org/pypi")

    # Fetch the list of packages
    packages = client.user_packages(username)

    # Print the list of packages
    return [p[1].replace("-", "_") for p in packages]


# Replace 'NOMAD-CAMELS' with the actual PyPI username
camels_packages = get_user_packages("NOMAD-CAMELS")

helping_str = "Helping Packages\n"
helping_str += "================\n\n"
helping_str += ".. toctree::\n"
helping_str += "   :maxdepth: 4\n\n"
helping_str += "   suitcase.nomad_camels_hdf5\n"

driver_str = "Drivers\n"
driver_str += "=======\n\n"
driver_str += ".. toctree::\n"
driver_str += "   :maxdepth: 4\n\n"

extension_str = "Extensions\n"
extension_str += "==========\n\n"
extension_str += ".. toctree::\n"
extension_str += "   :maxdepth: 4\n\n"


for package in camels_packages:
    logging.info(f"Processing package: {package}")
    if package == "suitcase_nomad_camels_hdf5":
        continue
    # install the package if not yet installed
    if not importlib.util.find_spec(package):
        logging.info(f"Installing {package}...")
        res = subprocess.run(["pip", "install", package])
        if res.returncode != 0:
            logging.error(f"Failed to install {package}")
            continue
    # import the package
    importlib.import_module(package)
    # get the package path
    package_path = importlib.util.find_spec(package).submodule_search_locations[0]
    # add the package path to sys.path
    sys.path.insert(0, package_path)
    if not os.path.isfile(f"{package_path}/__init__.py"):
        with open(f"{package_path}/__init__.py", "w") as file:
            pass

    output_dir = "./docs/source/"

    result = subprocess.run(
        ["sphinx-apidoc", "-f", "-o", output_dir, package_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        continue
    if package.startswith("nomad_camels_driver"):
        driver_str += f"   {package}\n"
    elif package.startswith("nomad_camels_extension"):
        extension_str += f"   {package}\n"
    else:
        helping_str += f"   {package}\n"
    logging.info(f"{package} successful")

# Write the helping packages to the docs
with open("./docs/source/helping_packages.rst", "w") as file:
    file.write(helping_str)

# Write the drivers to the docs
with open("./docs/source/drivers.rst", "w") as file:
    file.write(driver_str)

# Write the extensions to the docs
with open("./docs/source/extensions.rst", "w") as file:
    file.write(extension_str)
