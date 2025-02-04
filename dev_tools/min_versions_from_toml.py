import toml
from packaging.specifiers import SpecifierSet
from packaging.version import Version
import os

file_path = os.path.abspath(__file__)


def extract_min_versions(pyproject_path="pyproject.toml", python_versions=None):
    """Extracts the minimum versions of dependencies for each given Python version."""
    if python_versions is None:
        python_versions = ["3.8", "3.9", "3.10", "3.11", "3.12"]

    # Load pyproject.toml
    with open(pyproject_path, "r", encoding="utf-8") as f:
        pyproject_data = toml.load(f)

    dependencies = (
        pyproject_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    )

    # Dictionary to store min versions per Python version
    min_versions_by_python = {py_ver: {} for py_ver in python_versions}

    for package, constraint in dependencies.items():
        if package.lower() == "python":
            continue  # Skip Python version itself

        # Handle different constraint formats
        if isinstance(constraint, str):
            # Simple constraint: ">=6.0"
            specifier_set = SpecifierSet(constraint)
            min_version = min(
                (
                    Version(spec.version)
                    for spec in specifier_set
                    if spec.operator in (">=", ">", "==")
                ),
                default=None,
            )
            if min_version:
                for py_ver in python_versions:
                    min_versions_by_python[py_ver][package] = str(min_version)

        elif isinstance(constraint, list):
            # List-based constraints with Python version conditions
            for entry in constraint:
                version_spec = entry.get("version", "")
                py_spec = entry.get("python", "")

                specifier_set = SpecifierSet(version_spec)
                min_version = min(
                    (
                        Version(spec.version)
                        for spec in specifier_set
                        if spec.operator in (">=", ">", "==")
                    ),
                    default=None,
                )

                if min_version:
                    # Apply only to matching Python versions
                    for py_ver in python_versions:
                        if not py_spec or SpecifierSet(py_spec).contains(py_ver):
                            if (
                                package not in min_versions_by_python[py_ver]
                                or Version(min_versions_by_python[py_ver][package])
                                > min_version
                            ):
                                min_versions_by_python[py_ver][package] = str(
                                    min_version
                                )

        elif isinstance(constraint, dict):
            # Dictionary-based constraints (e.g., with extras)
            version_spec = constraint.get("version", "")
            specifier_set = SpecifierSet(version_spec)
            min_version = min(
                (
                    Version(spec.version)
                    for spec in specifier_set
                    if spec.operator in (">=", ">", "==")
                ),
                default=None,
            )

            if min_version:
                for py_ver in python_versions:
                    min_versions_by_python[py_ver][package] = str(min_version)
            else:
                for py_ver in python_versions:
                    min_versions_by_python[py_ver][package] = ""

    return min_versions_by_python


def print_requirements_txt(min_versions_by_python):
    """Prints the minimum dependency versions in a requirements.txt format for each Python version."""
    for py_ver, min_versions in min_versions_by_python.items():
        with open(
            os.path.join(
                os.path.dirname(file_path), f"req_min_{py_ver.replace('.', '_')}.txt"
            ),
            "w",
        ) as f:
            for package, version in min_versions.items():
                if version:
                    f.write(f"{package}=={version}\n")
                else:
                    f.write(f"{package}\n")


if __name__ == "__main__":
    python_versions = ["3.9", "3.10", "3.11", "3.12", "3.13"]
    min_versions_by_python = extract_min_versions(python_versions=python_versions)
    print_requirements_txt(min_versions_by_python)
