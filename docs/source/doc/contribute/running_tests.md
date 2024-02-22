# Running Tests

When contributing to NOMAD CAMELS, or as a new user, it is useful to run the provided tests and see whether they all pass. If any fail and you cannot find a simple reason for it in your environment, please post an [issue on GitHub](https://github.com/FAU-LAP/NOMAD-CAMELS/issues) to help us improve.

## Requirements for the tests
The tests can be run using `pytest`. It is not included in the requirements to run NOMAD CAMELS, so you have to install it:
```bash
pip install pytest pytest-qt
```
The extension `pytest-qt` is required as well for testing UI features.

## Run the tests
To run the tests navigate to the `nomad_camels` directory and run
```bash
pytest -v
```
The argument `-v` will give you a verbose output of the tests.