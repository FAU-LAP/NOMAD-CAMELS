import requests
import os
import time

url = "https://raw.githubusercontent.com/FAU-LAP/CAMELS_drivers/driver_list/driver_list.txt"

for i in range(10):
    try:
        response = requests.get(url).text
        break
    except:
        time.sleep(1)

devices = {}


def agilent_keysight_combi(s):
    if s.lower() in ["agilent", "keysight"]:
        return "Keysight / Agilent"
    return s


def capital_first_letter(s):
    return s[0].upper() + s[1:] if s else s


for line in response.split("\n"):
    if not line:
        continue
    full_name, version = line.split("==")
    try:
        manufacturer, name = full_name.split("_", 1)
    except ValueError:
        manufacturer = ""
        name = full_name
    manufacturer = capital_first_letter(manufacturer)
    manufacturer = agilent_keysight_combi(manufacturer)
    name = capital_first_letter(name)
    devices[full_name] = {
        "manufacturer": manufacturer,
        "name": name,
        "version": version,
    }

sweep_me_version = ""
if "SweepMe_device" in devices:
    sweep_me_version = devices.pop("SweepMe_device")["version"]

url = "https://api.github.com/repos/SweepMe/instrument-drivers/contents/src"
for i in range(10):
    try:
        response = requests.get(url).json()
        test_var = response[0]["type"]
        break
    except:
        time.sleep(1)

sweep_me_devices = {}

for item in response:
    if item["type"] == "dir":  # A type of 'dir' indicates a directory (folder)
        device_type, full_name = item["name"].split("-", 1)
        manufacturer, name = full_name.split("_", 1)
        # make first letter caps
        manufacturer = manufacturer.capitalize()
        manufacturer = agilent_keysight_combi(manufacturer)
        name = name.capitalize()
        sweep_me_devices[full_name] = {
            "type": device_type,
            "name": name,
            "url": item["html_url"],
            "manufacturer": manufacturer,
        }


with open("./docs/source/doc/instruments/instruments.rst", "w", encoding="utf-8") as f:
    f.write(
        """
===========
Instruments
===========

Below is a list of instruments that have drivers for NOMAD CAMELS. The table is sortable by clicking on the column headers. You can also search for specific instruments using the search bar.

Please note that this page is currently under construction and the information may not be up-to-date.

The table includes instruments from SweepMe! as well. These instruments are not all tested with NOMAD CAMELS yet, if you find any issues, please let us know.

.. raw:: html

    <style>
        table.sortable {
            border-collapse: collapse;
            width: 100%;
        }
        table.sortable th, table.sortable td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        table.sortable th {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }
        /* Add styles for the sorting arrows */
        table.sortable th::after {
            content: " ▼▲";
            color: #ddd;
        }
        table.sortable th.sorttable_sorted::after,
        table.sortable th.sorttable_sorted_reverse::after {
            color: #000;
        }
    </style>
    <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>
    <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for instruments..">
    <table class="sortable" id="instrumentTable">
        <thead>
            <tr>
                <th>Manufacturer</th>
                <th>Instrument</th>
                <th>Type</th>
                <th>Version</th>
            </tr>
        </thead>
        <tbody>"""
    )
    for device in devices:
        if os.path.exists(f"./docs/source/doc/instruments/{device}"):
            f.write(
                f"""
            <tr>
                <td>{devices[device]['manufacturer']}</td>
                <td><a href='{device}/{device}'>{devices[device]['name']}</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-{device.replace('_', '-')}'>{devices[device]['version']}</a></td>
            </tr>"""
            )
        else:
            f.write(
                f"""
            <tr>
                <td>{devices[device]['manufacturer']}</td>
                <td>{devices[device]['name']}</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-{device.replace('_', '-')}'>{devices[device]['version']}</a></td>
            </tr>"""
            )
    for device in sweep_me_devices:
        f.write(
            f"""
            <tr>
                <td>{sweep_me_devices[device]['manufacturer']} (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>{sweep_me_devices[device]['name']}</a></td>
                <td>{sweep_me_devices[device]['type']}</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>{sweep_me_version}</a></td>
            </tr>"""
        )
    f.write(
        """
        </tbody>
    </table>
    <script>
        function searchTable() {
            var input, filter, table, tr, td, i, j, txtValue;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase().split(' ');  // Split the filter into words
            table = document.getElementById("instrumentTable");
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td");
                var rowText = '';
                for (j = 0; j < td.length; j++) {
                    if (td[j]) {
                        rowText += ' ' + (td[j].textContent || td[j].innerText);
                    }
                }
                rowText = rowText.toUpperCase();
                // Check if all words in the filter are present in the row
                if (filter.every(function(word) { return rowText.indexOf(word) > -1; })) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    </script>
    <script>
        window.onload = function() {
            var th = document.querySelector('#instrumentTable th');
            var evt = new window.MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true
            });
            th.dispatchEvent(evt);
        };
    </script>
    
.. toctree::
    :maxdepth: 2
    :hidden:
    SweepMe <SweepMe_drivers.md>
    Cam-Control by PyLabLib <cam_control_pylablib/cam_control_pylablib.md>
    """
    )
