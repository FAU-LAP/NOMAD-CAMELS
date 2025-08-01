#!/usr/bin/env python3

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from packaging.version import Version
from packaging.specifiers import SpecifierSet
from packaging.markers import Marker
import logging
import time
import toml

# set log file
logging.basicConfig(filename="test_log.txt", level=logging.INFO)


last_package = None
last_dir = None
last_python = None


###############################################################################
# 1. Get all versions of a package from PyPI (requires pip >= 22.3)
###############################################################################
def get_available_versions(package):
    """
    Uses 'pip index versions <package>' to list all known versions on PyPI.
    Returns a list of version strings (e.g. ["2.25.0", "2.25.1", ...]).
    """
    # Run pip index command
    try:
        output = subprocess.check_output(
            [sys.executable, "-m", "pip", "index", "versions", package], text=True
        )
    except subprocess.CalledProcessError:
        logging.error(f"Could not run 'pip index versions' for {package}.")
        return []

    # Parse lines that look like "  2.25.0 ..." for version numbers
    versions = []
    for line in output.splitlines():
        if not line.startswith("Available versions:"):
            continue
        text = line.split(":", 1)[1].strip()
        for v in text.split(","):
            versions.append(v.strip())
    return versions


###############################################################################
# 2. Test if installing a specific version (plus other constraints) can pass tests
###############################################################################
def make_venv(python_exe):
    logging.info("making venv")
    temp_dir = tempfile.mkdtemp(prefix="shared_venv_")
    venv_dir = Path(temp_dir) / "venv"
    subprocess.run([python_exe, "-m", "venv", str(venv_dir)], check=True)
    venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    subprocess.run(
        [venv_python, "-m", "pip", "install", "--upgrade", "pip", "wheel"], check=True
    )

    return temp_dir


def update_venv(
    python_executable,
    dependency,
    version,
    other_constraints=None,
    test_command=None,
    force_new=False,
):
    global last_package, last_dir, last_python
    if other_constraints is None:
        other_constraints = []
    constraints = [x.split(">=")[0] if ">=" in x else x for x in other_constraints]
    if dependency in constraints:
        index = constraints.index(dependency)
        new_other_constraints = (
            other_constraints[:index] + other_constraints[index + 1 :]
        )
    else:
        new_other_constraints = other_constraints
    if test_command is None:
        # Example: run pytest on a 'tests' directory
        test_command = ["pytest", "tests"]
    if last_python != python_executable:
        if last_dir is not None:
            shutil.rmtree(last_dir)
        last_python = python_executable
        tmpdir = make_venv(python_executable)
        last_dir = tmpdir
    else:
        tmpdir = last_dir
    venv_dir = os.path.join(tmpdir, "venv")

    # Construct paths for python/pip inside this venv
    if os.name == "nt":
        # Windows
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
        test_exe = os.path.join(venv_dir, "Scripts", test_command[0] + ".exe")
    else:
        # Unix/macOS
        pip_exe = os.path.join(venv_dir, "bin", "pip")
        test_exe = os.path.join(venv_dir, "bin", test_command[0])

    if force_new or last_package != dependency:
        # Remove the venv's site-packages directory if we're testing a new package
        # also remove directory if not empty
        logging.info("removing site packages")
        result = subprocess.run(
            [pip_exe, "freeze"],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        installed_packages = result.stdout.strip().split("\n")

        # Step 2: Filter out pip, setuptools, and wheel
        filtered_packages = [
            pkg
            for pkg in installed_packages
            if pkg and not pkg.startswith(("pip==", "setuptools==", "wheel=="))
        ]

        if filtered_packages:
            uninstall_cmd = [pip_exe, "uninstall", "-y"] + filtered_packages
            subprocess.run(uninstall_cmd, check=True)

    # 1) Install pinned version of the target dependency
    # 2) Install all other constraints
    # 3) Install your test framework (pytest, etc.)
    # 4) (Optionally) install your actual project
    # install quietly, no output
    install_cmd = [pip_exe, "install", f"{dependency}=={version}", "--quiet"]
    if last_package != dependency or force_new:
        install_cmd += new_other_constraints
        install_cmd += ["--no-cache-dir"]
    last_package = dependency
    subprocess.run(install_cmd, check=True)
    return test_exe


def test_dependency_version(
    python_executable, dependency, version, other_constraints=None, test_command=None
):
    """
    Creates a temporary venv, installs `dependency==version` plus
    any other constraints (e.g., "requests>=2.0,<3.0" for the rest),
    and runs tests.

    Returns True if tests pass, False otherwise.
    """
    global last_python
    try:
        test_exe = update_venv(
            python_executable=python_executable,
            dependency=dependency,
            version=version,
            other_constraints=other_constraints,
            test_command=test_command,
        )
    except Exception as e:
        logging.error(f"Could not set up venv for {dependency}=={version}.\n\t{e}")
        logging.info("forcing new try with reinstalled packages")
        last_python = None
        try:
            test_exe = update_venv(
                python_executable=python_executable,
                dependency=dependency,
                version=version,
                other_constraints=other_constraints,
                test_command=test_command,
                force_new=True,
            )
        except Exception as e:
            logging.error(f"Could not set up venv for {dependency}=={version}.\n\t{e}")
            last_python = None
            with open("test_output.txt", "a") as f:
                f.write(f"{dependency}=={version} - Install failed\n")
            return False

    # Optionally install your project:
    # subprocess.run([pip_exe, "install", "-e", "."], check=True)
    if not os.path.exists(test_exe):
        last_python = None
        try:
            test_exe = update_venv(
                python_executable=python_executable,
                dependency=dependency,
                version=version,
                other_constraints=other_constraints,
                test_command=test_command,
                force_new=True,
            )
        except Exception as e:
            logging.error(f"Could not set up venv for {dependency}=={version}.")
            last_python = None
            with open("test_output.txt", "a") as f:
                f.write(f"{dependency}=={version} - Install failed\n")
            return False
        if not os.path.exists(test_exe):
            logging.error(f"Test executable not found for {dependency}=={version}.")
            with open("test_output.txt", "a") as f:
                f.write(f"{dependency}=={version} - Executable not found\n")
            return False

    # Finally, run tests
    for i in range(3):
        ret = run_test(test_command, test_exe)
        if ret != 3221225477:
            break
        logging.info("retrying test, got 3221225477")
    with open("test_output.txt", "a") as f:
        f.write(f"{dependency}=={version} - {ret}\n")
    if ret != 0:
        logging.info("forcing new try with reinstalled packages")
        if ret == 3221225477:
            last_python = None
        try:
            test_exe = update_venv(
                python_executable=python_executable,
                dependency=dependency,
                version=version,
                other_constraints=other_constraints,
                test_command=test_command,
                force_new=True,
            )
        except Exception as e:
            logging.error(f"Could not set up venv for {dependency}=={version}.")
            last_python = None
            with open("test_output.txt", "a") as f:
                f.write(f"{dependency}=={version} - Reinstall failed\n")
            return False
        for i in range(2):
            ret = run_test(test_command, test_exe)
            if ret != 3221225477:
                break
            last_python = None
            try:
                test_exe = update_venv(
                    python_executable=python_executable,
                    dependency=dependency,
                    version=version,
                    other_constraints=other_constraints,
                    test_command=test_command,
                    force_new=True,
                )
            except Exception as e:
                logging.error(f"Could not set up venv for {dependency}=={version}.")
                last_python = None
                with open("test_output.txt", "a") as f:
                    f.write(f"{dependency}=={version} - Reinstall failed\n")
                return False
        if ret != 0:
            logging.error(f"Tests failed for {dependency}=={version}.")
        with open("test_output.txt", "a") as f:
            f.write(f"{dependency}=={version} - {ret}\n")
    return ret == 0


def run_test(test_command, test_exe):
    overall_timeout = 600
    if len(test_command) == 1:
        command = [test_exe]
    else:
        command = [test_exe] + test_command[1:]
    process = subprocess.Popen(
        command,
        cwd=os.getcwd(),
        text=True,
    )
    start_time = time.time()
    while ret := process.poll() is None:
        # Check if the overall timeout has been exceeded
        if time.time() - start_time > overall_timeout:
            # Kill the process if it exceeds the overall timeout
            process.kill()
            print("Overall timeout exceeded. Tests were terminated.")
            break
        time.sleep(0.1)
    ret = process.wait()
    return ret


###############################################################################
# 3. Find the actual min & max versions that pass
###############################################################################
def find_min_version_going_down(
    python_executable,
    dependency,
    broad_spec,
    other_constraints=None,
    test_command=None,
    check_below_valid=False,
):
    """
    1) Get all available versions of `dependency`.
    2) Filter them to those matching broad_spec (e.g. '>=2.0,<3.0').
    3) From oldest to newest, find the first that passes (min).
    4) From newest to oldest, find the first that passes (max).
    """

    all_versions = get_available_versions(dependency)
    if not all_versions:
        return None

    spec = SpecifierSet(broad_spec)
    # Filter only those that are valid and in the broad spec
    valid_versions = []
    for v_str in all_versions:
        try:
            v_obj = Version(v_str)
            if v_obj in spec:
                valid_versions.append(v_str)
        except:
            pass

    # Sort them as Version objects
    valid_versions.sort(key=lambda x: Version(x))

    if not valid_versions:
        return None

    # Find min: earliest version that passes
    min_version = None
    if not check_below_valid:
        for v in valid_versions[::-1]:
            logging.info(
                f"Testing {dependency}=={v} on {python_executable} ... (min candidate)"
            )
            if not test_dependency_version(
                python_executable, dependency, v, other_constraints, test_command
            ):
                logging.info(f"  --> FAILED at {v}")
                break
            min_version = v
    else:
        v = valid_versions[0]
        logging.info(
            f"Testing {dependency}=={v} on {python_executable} ... (min candidate)"
        )
        if not test_dependency_version(
            python_executable, dependency, v, other_constraints, test_command
        ):
            logging.info(f"  --> FAILED at {v}")
            return find_min_version_going_up(
                python_executable,
                dependency,
                broad_spec,
                other_constraints,
                test_command,
            )
        min_version = v
        broad_spec = f"<{v}"
        spec = SpecifierSet(broad_spec)
        # Filter only those that are valid and in the broad spec
        valid_versions = []
        for v_str in all_versions:
            try:
                v_obj = Version(v_str)
                if v_obj in spec:
                    valid_versions.append(v_str)
            except:
                pass
        for v in valid_versions:
            logging.info(
                f"Testing {dependency}=={v} on {python_executable} ... (min candidate)"
            )
            if not test_dependency_version(
                python_executable, dependency, v, other_constraints, test_command
            ):
                logging.info(f"  --> FAILED at {v}")
                break
            min_version = v

    return min_version


def find_max_version_going_down(
    python_executable,
    dependency,
    broad_spec,
    other_constraints=None,
    test_command=None,
):
    """
    1) Get all available versions of `dependency`.
    2) Filter them to those matching broad_spec (e.g. '>=2.0,<3.0').
    3) From oldest to newest, find the first that passes (min).
    4) From newest to oldest, find the first that passes (max).
    """
    all_versions = get_available_versions(dependency)
    if not all_versions:
        return None

    spec = SpecifierSet(broad_spec)
    # Filter only those that are valid and in the broad spec
    valid_versions = []
    for v_str in all_versions:
        try:
            v_obj = Version(v_str)
            if v_obj in spec:
                valid_versions.append(v_str)
        except:
            pass

    # Sort them as Version objects
    valid_versions.sort(key=lambda x: Version(x))

    if not valid_versions:
        return None

    # Find max: earliest version that passes
    for v in valid_versions[::-1]:
        logging.info(
            f"Testing {dependency}=={v} on {python_executable} ... (max candidate)"
        )
        print(
            f"\nTesting {dependency}=={v} on {python_executable} ... (max candidate)\n"
        )
        if test_dependency_version(
            python_executable, dependency, v, other_constraints, test_command
        ):
            logging.info(f"  --> WORKED at {v}")
            print(f"\n  --> WORKED at {v}\n")
            return v
    return None


def find_min_version_going_up(
    python_executable, dependency, broad_spec, other_constraints=None, test_command=None
):
    """
    1) Get all available versions of `dependency`.
    2) Filter them to those matching broad_spec (e.g. '>=2.0,<3.0').
    3) From oldest to newest, find the first that passes (min).
    4) From newest to oldest, find the first that passes (max).
    """
    all_versions = get_available_versions(dependency)
    if not all_versions:
        return None

    spec = SpecifierSet(broad_spec)
    # Filter only those that are valid and in the broad spec
    valid_versions = []
    for v_str in all_versions:
        try:
            v_obj = Version(v_str)
            if v_obj in spec:
                valid_versions.append(v_str)
        except:
            pass

    # Sort them as Version objects
    valid_versions.sort(key=lambda x: Version(x))

    if not valid_versions:
        return None

    # Find min: earliest version that passes
    for v in valid_versions:
        logging.info(
            f"Testing {dependency}=={v} on {python_executable} ... (min candidate)"
        )
        print(
            f"\nTesting {dependency}=={v} on {python_executable} ... (min candidate)\n"
        )
        if test_dependency_version(
            python_executable, dependency, v, other_constraints, test_command
        ):
            logging.info(f"  --> WORKED at {v}")
            print(f"\n  --> WORKED at {v}\n")
            return v
    return None


# ###############################################################################
# # 4. Main driver - example usage
# ###############################################################################
# def main():
#     """
#     Example usage: For each Python version in `python_versions`,
#     check the min and max supported versions of each dependency in `dependencies`.
#     """
#     python_versions = [
#         r"C:\Users\od93yces\.pyenv\pyenv-win\versions\3.11.9\python.exe",
#         r"C:\Users\od93yces\.pyenv\pyenv-win\versions\3.12.4\python.exe",
#         r"C:\Users\od93yces\.pyenv\pyenv-win\versions\3.10.11\python.exe",
#         r"C:\Users\od93yces\.pyenv\pyenv-win\versions\3.9.13\python.exe",
#     ]  # Adjust for your environment
#     # under the broad constraints below:
#     dependencies = {
#         "PySide6": ">=6.6.0",
#         "numpy": ">=1.22.0",
#         "bluesky": ">=1.9.0",
#         "ophyd": ">=1.6.4",
#         "lmfit": ">=1.0.2",
#         "pyyaml": ">=3.10",
#         "requests": ">=2.26.0",
#         "databroker": ">=1.2.5",
#         "setuptools": ">=36.0.1",
#         "matplotlib": ">=3.6.2",
#         "pyqtgraph": ">=0.13.3",
#         "fastapi": ">=0.110.1",
#         "uvicorn": ">=0.19.0",
#         "httpx": ">=0.21.0",
#         "pytest": ">=7.0.0",
#         "pytest-qt": ">=4.2.0",
#         "pytest-order": ">=0.7.1",
#         "pytest-mock": ">=0.4.0",
#         "pytest-timeout": ">=1.3.1",
#         "pytest-cov": ">=6.0.0",
#         "pyvisa": ">=1.12.0",
#         "pyvisa-py": ">=0.5.3",
#         "pyzmq": ">=22.1.0",
#     }

#     # You might also have a broad constraint for your other dependencies,
#     # so that they get installed in each environment as well. For instance:
#     other_constraints = [
#         "suitcase-nomad-camels-hdf5>=0.6.3",
#         "PySide6",
#         "numpy",
#         "bluesky",
#         "ophyd",
#         "lmfit",
#         "pyyaml",
#         "requests",
#         "databroker",
#         "setuptools",
#         "matplotlib",
#         "pyqtgraph",
#         "fastapi",
#         "uvicorn",
#         "httpx",
#         "pytest",
#         "pytest-qt",
#         "pytest-order",
#         "pytest-mock",
#         "pytest-timeout",
#         "pyvisa",
#         "pyvisa-py",
#         "pytest-cov",
#         "pyzmq",
#     ]
#     # In a real scenario, you might want to exclude the package you're testing from `other_constraints`
#     # or maintain a more granular matrix. This is just an example for demonstration.

#     # A test command, e.g. "pytest" on a 'tests' folder:
#     test_command = ["pytest", "--timeout=60"]

#     results = {}

#     for py_exe in python_versions:
#         logging.info(f"Testing on {py_exe}")
#         print(f"\n===== Testing on {py_exe} =====\n")
#         for dep, broad_spec in dependencies.items():
#             min_v = find_min_version_going_up(
#                 python_executable=py_exe,
#                 dependency=dep,
#                 broad_spec=broad_spec,
#                 other_constraints=other_constraints,
#                 test_command=test_command,
#                 # check_below_valid=True,
#             )
#             print(f"\nResult for {dep} on {py_exe}:")
#             print(f"  Minimum passing version: {min_v}")
#             max_v = min_v
#             # max_v = find_max_version_going_down(
#             #     python_executable=py_exe,
#             #     dependency=dep,
#             #     broad_spec=broad_spec,
#             #     other_constraints=other_constraints,
#             #     test_command=test_command,
#             # )
#             # print(f"\nResult for {dep} on {py_exe}:")
#             # print(f"  Maximum passing version: {max_v}")
#             results[(py_exe, dep)] = (min_v, max_v)
#         logging.info(f"Finished testing on {py_exe}\n\n")

#     # After the loop, you could print a summary or write the results to a file
#     print("\n===== FINAL RESULTS =====")
#     for (py_exe, dep), (mn, mx) in results.items():
#         print(f"{py_exe} - {dep}: min={mn}, max={mx}")


def resolve_constraint(constraint, current_python_version):
    """
    Given a dependency constraint (which can be a string, dict, or list),
    returns the version constraint that applies for the current Python version.
    If the constraint has a marker (like "sys_platform == 'linux'") that is not
    satisfied, returns an empty string.
    current_python_version: string, e.g. "3.10"
    """
    current_ver = Version(current_python_version)
    if isinstance(constraint, str):
        return constraint
    elif isinstance(constraint, dict):
        # If there is a marker and it doesn't evaluate to True, skip this dependency.
        if "markers" in constraint:
            m = Marker(constraint["markers"])
            if not m.evaluate():
                return "skip!"
        return constraint.get("version", "")
    elif isinstance(constraint, list):
        for entry in constraint:
            # Check marker if it exists.
            if "markers" in entry:
                m = Marker(entry["markers"])
                if not m.evaluate():
                    continue
            py_spec = entry.get("python", "")
            if py_spec:
                spec = SpecifierSet(py_spec)
                if current_ver in spec:
                    return entry.get("version", "")
        # Fallback: return the version from the first entry (even if its marker is false)
        return constraint[0].get("version", "")
    return ""


def main():
    """
    Reads package constraints from pyproject.toml and then tests each dependency using the current Python.

    You can pass a command-line argument:
       --mode=min   (default) test for the lowest possible passing version.
       --mode=max   test for the highest possible passing version.

    The constraints are read from the [tool.poetry.dependencies] section of pyproject.toml.
    """
    # Use the python that is running this script
    python_executable = sys.executable
    current_python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

    # Determine mode from command-line
    mode = "min"
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("--mode=max", "--mode=maximal", "--max"):
            mode = "max"

    # Read pyproject.toml for dependencies
    pyproj = toml.load("pyproject.toml")
    # Access dependencies under tool.poetry.dependencies
    poetry_deps = pyproj.get("tool", {}).get("poetry", {}).get("dependencies", {})
    # Remove "python" dependency – we use the current interpreter.
    poetry_deps.pop("python", None)

    # For clarity, we also extract other constraints from the extras or elsewhere as needed
    # (Here we simply use all dependencies as constraints for demonstration)
    other_constraints = []  # You can modify this list if you need extra constraints

    # add optional dependencies to poetry_deps
    optional_deps = (
        pyproj.get("tool", {}).get("poetry", {}).get("optional-dependencies", {})
    )
    for opt_name, opt_deps in optional_deps.items():
        for dep, constraint in opt_deps.items():
            if dep not in poetry_deps:
                poetry_deps[dep] = constraint

    # add all packages without constraints to other_constraints
    for dep, constraint in poetry_deps.items():
        if isinstance(constraint, str) and constraint.startswith("=="):
            # If the constraint is a specific version, we can add it to other_constraints
            other_constraints.append(f"{dep}{constraint}")
        elif isinstance(constraint, dict):
            # If it's a dict (e.g., with extras), we can add the version if available
            version = constraint.get("version", "")
            if version:
                other_constraints.append(f"{dep}{version}")
        else:
            # Otherwise, just add the package name
            other_constraints.append(dep)

    # Print out resolved dependencies based on the current Python version:
    print(f"Current Python version: {current_python_version}")
    print("Resolved dependency constraints from pyproject.toml:")
    for dep, constraint in poetry_deps.items():
        resolved = resolve_constraint(constraint, current_python_version)
        print(f"  {dep}: {resolved}")

    # A test command – adjust if needed.
    test_command = ["pytest", "--timeout=60"]

    print(f"found the following dependencies in pyproject.toml:\n{poetry_deps}")

    results = {}

    logging.info(
        f"\n===== Testing dependencies with mode '{mode}' using {python_executable} =====\n"
    )
    print(
        f"\n===== Testing dependencies with mode '{mode}' using {python_executable} =====\n"
    )
    for dep, constraint in poetry_deps.items():
        # 'constraint' may be a simple version string or a dict with markers – we assume simple version strings.
        # If it is a dict, pick the constraint that applies (this example is simplistic).
        broad_spec = resolve_constraint(constraint, current_python_version)
        if broad_spec == "skip!":
            logging.info(f"Skipping {dep} due to marker constraints.")
            print(f"Skipping {dep} due to marker constraints.")
            continue

        logging.info(f"\nTesting dependency: {dep} with broad spec '{broad_spec}'")
        print(f"\nTesting dependency: {dep} with broad spec '{broad_spec}'")
        if mode == "min":
            version_found = find_min_version_going_up(
                python_executable, dep, broad_spec, other_constraints, test_command
            )
        else:
            version_found = find_max_version_going_down(
                python_executable, dep, broad_spec, other_constraints, test_command
            )
        results[dep] = version_found
        logging.info(f"Result for {dep}: Passing version: {version_found}\n")
        print(f"Result for {dep}: Passing version: {version_found}\n")

    logging.info("\n===== FINAL RESULTS =====")
    print("\n===== FINAL RESULTS =====")
    for dep, ver in results.items():
        logging.info(f"{dep}: {ver}")
        print(f"{dep}: {ver}")
    logging.info("\n===== Testing Completed =====\n")
    print("\n===== Testing Completed =====\n")


if __name__ == "__main__":
    main()
