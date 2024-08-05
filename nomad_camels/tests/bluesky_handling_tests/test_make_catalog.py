import os
import pathlib
import pytest
from unittest.mock import patch, mock_open, MagicMock
from nomad_camels.bluesky_handling.make_catalog import make_yml


@pytest.fixture
def mock_dependencies():
    with (
        patch("os.makedirs") as mock_makedirs,
        patch("os.path.isdir", return_value=False) as mock_isdir,
        patch("builtins.open", new_callable=mock_open) as mock_file,
        patch(
            "databroker.catalog_search_path", return_value=["/mock/catalog/path"]
        ) as mock_catalog_search_path,
        patch("databroker.catalog.force_reload") as mock_force_reload,
        patch("databroker.catalog", new_callable=MagicMock) as mock_catalog,
    ):
        yield {
            "mock_makedirs": mock_makedirs,
            "mock_isdir": mock_isdir,
            "mock_file": mock_file,
            "mock_catalog_search_path": mock_catalog_search_path,
            "mock_force_reload": mock_force_reload,
            "mock_catalog": mock_catalog,
        }


def test_make_yml_creates_files_and_directories(mock_dependencies):
    datapath = "/mock/data/path"
    catalog_name = "TEST_CATALOG"

    make_yml(datapath, catalog_name)

    mock_dependencies["mock_makedirs"].assert_any_call(
        pathlib.Path("/mock/catalog/path")
    )
    mock_dependencies["mock_makedirs"].assert_any_call(
        pathlib.Path(datapath) / "databroker" / catalog_name
    )

    mock_dependencies["mock_file"].assert_called_once_with(
        pathlib.Path("/mock/catalog/path/TEST_CATALOG.yml"), "w", encoding="utf-8"
    )
    expected_content = (
        "sources:\n"
        f"  {catalog_name}:\n"
        '    driver: "bluesky-msgpack-catalog"\n'
        "    args:\n"
        "      paths:\n"
        f'        - "{(pathlib.Path(datapath) / "databroker" / catalog_name).as_posix()}/*.msgpack"'
    )
    mock_dependencies["mock_file"].return_value.write.assert_called_once_with(
        expected_content
    )


@patch("nomad_camels.bluesky_handling.make_catalog.WarnPopup")
@patch("nomad_camels.bluesky_handling.make_catalog.update_camels.restart_camels")
def test_make_yml_warns_if_catalog_not_loaded(
    mock_restart_camels, mock_warn_popup, mock_dependencies
):
    mock_dependencies["mock_catalog"].__contains__.side_effect = lambda x: False
    datapath = "/mock/data/path"
    catalog_name = "TEST_CATALOG"

    make_yml(datapath, catalog_name, ask_restart=True)

    mock_warn_popup.assert_called_once()
    mock_restart_camels.assert_called_once_with(ask_restart=True)


def test_make_yml_pathlib_conversion(mock_dependencies):
    datapath = "/mock/data/path"
    catalog_name = "TEST_CATALOG"

    make_yml(datapath, catalog_name)

    assert isinstance(pathlib.Path(datapath), pathlib.Path)
    assert isinstance(
        pathlib.Path(mock_dependencies["mock_catalog_search_path"].return_value[0]),
        pathlib.Path,
    )
