import os
import subprocess
import suitcase.nomad_camels_hdf5
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Paths
output_dir = "./docs/source/"
module_path = suitcase.nomad_camels_hdf5.__path__[0]

# Run sphinx-apidoc
logging.info("Running sphinx-apidoc...")
result = subprocess.run(
    ["sphinx-apidoc", "-f", "-o", output_dir, module_path],
    capture_output=True,
    text=True,
)
if result.returncode != 0:
    logging.error(f"sphinx-apidoc failed: {result.stderr}")
    exit(1)
logging.info("sphinx-apidoc completed successfully.")


# Rename generated .rst files
def rename_file(name):
    old_filename = os.path.join(output_dir, f"{name}.rst")
    new_filename = os.path.join(output_dir, f"suitcase.{name}.rst")
    if os.path.exists(old_filename):
        logging.info(f"Renaming {old_filename} to {new_filename}...")
        os.rename(old_filename, new_filename)
        logging.info("File renamed successfully.")
    else:
        logging.warning(f"{old_filename} does not exist. Skipping renaming.")
    return new_filename


# Update content of .rst files
def update_rst_file(file_path):
    if os.path.exists(file_path):
        logging.info(f"Updating {file_path}...")
        with open(file_path, "r") as file:
            content = file.read()
        content = content.replace("nomad_camels_hdf5", "suitcase.nomad_camels_hdf5")
        with open(file_path, "w") as file:
            file.write(content)
        logging.info(f"{file_path} updated successfully.")
    else:
        logging.warning(f"{file_path} does not exist. Skipping update.")


# Update the renamed .rst file

new_filename = rename_file("nomad_camels_hdf5")
update_rst_file(new_filename)

new_filename = rename_file("nomad_camels_hdf5.tests")
update_rst_file(new_filename)
