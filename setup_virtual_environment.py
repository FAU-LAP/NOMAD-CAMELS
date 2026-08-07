"""Create and maintain the Python 3.11 virtual environment for NOMAD CAMELS.

Usage from any PowerShell directory::

    python C:\\NOMAD_CAMELS\\NOMAD-CAMELS\\setup_virtual_environment.py

Use ``--recreate`` only if the existing .venv is broken or has the wrong
Python version. The script installs requirements.txt and the local CAMELS
project. It cannot activate the parent PowerShell; VS Code activates the
configured .venv automatically for new terminals.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
PYTHON = VENV / "Scripts" / "python.exe"


def run(command: list[str]) -> None:
    print(">", subprocess.list2cmdline(command))
    subprocess.run(command, cwd=ROOT, check=True)


def python_is_311() -> bool:
    if not PYTHON.is_file():
        return False
    result = subprocess.run(
        [str(PYTHON), "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "3.11"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete and recreate .venv if it is broken or not Python 3.11.",
    )
    parser.add_argument(
        "--with-demo-drivers",
        action="store_true",
        help="Also install local demo SMU/DMM and PID drivers when available.",
    )
    args = parser.parse_args()

    if not python_is_311():
        if VENV.exists() and not args.recreate:
            parser.error(
                f"{VENV} is missing or is not Python 3.11. Run this script with --recreate."
            )
        if VENV.exists():
            print(f"Removing {VENV} ...")
            shutil.rmtree(VENV)
        run(["py", "-3.11", "-m", "venv", str(VENV)])

    run([str(PYTHON), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(PYTHON), "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")])
    run([str(PYTHON), "-m", "pip", "install", "-e", f"{ROOT}[api,dash,visa]"])

    if args.with_demo_drivers:
        drivers_root = Path(r"C:\Nomad_drivers\CAMELS_drivers")
        drivers = [
            drivers_root / "demo_source_measure_unit",
            drivers_root / "demo_digital_multimeter",
            drivers_root / "PID",
        ]
        missing = [path for path in drivers if not path.is_dir()]
        if missing:
            parser.error(f"Missing local driver directories: {', '.join(map(str, missing))}")
        run([str(PYTHON), "-m", "pip", "install", "-e", *map(str, drivers)])

    run([str(PYTHON), "-c", "import numpy, nomad_camels; print('Python environment is ready.')"])


if __name__ == "__main__":
    main()
