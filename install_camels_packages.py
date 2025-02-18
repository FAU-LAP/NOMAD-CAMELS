import xmlrpc.client
import subprocess
import importlib


def get_user_packages(username):
    # Base URL for PyPI XML-RPC API
    client = xmlrpc.client.ServerProxy("https://pypi.org/pypi")

    # Fetch the list of packages
    packages = client.user_packages(username)

    # Print the list of packages
    return [p[1].replace("-", "_") for p in packages]


camels_packages = get_user_packages("NOMAD-CAMELS")
res = subprocess.run(["pip", "install"] + camels_packages)
if res.returncode != 0:
    for package in camels_packages:
        print(f"Processing package: {package}")
        # install the package if not yet installed
        if not importlib.util.find_spec(package):
            res = subprocess.run(["pip", "install", "-U", package])
            print(f"Installing {package}...")
            if res.returncode != 0:
                print(f"Failed to install {package}")
                continue
