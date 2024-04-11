import requests

url = "https://api.github.com/repos/SweepMe/instrument-drivers/contents/src"
response = requests.get(url).json()

devices = {}

for item in response:
    if item["type"] == "dir":  # A type of 'dir' indicates a directory (folder)
        device_type, full_name = item["name"].split("-", 1)
        manufacturer, name = full_name.split("_", 1)
        devices[full_name] = {
            "type": device_type,
            "name": name,
            "url": item["html_url"],
            "manufacturer": manufacturer,
        }

with open("instruments_table_test.rst", "w") as f:
    f.write("===========\nInstruments\n===========\n\n")
    f.write(".. raw:: html\n\n")
    f.write("    <style>\n")
    f.write("        table.sortable {\n")
    f.write("            border-collapse: collapse;\n")
    f.write("            width: 100%;\n")
    f.write("        }\n")
    f.write("        table.sortable th, table.sortable td {\n")
    f.write("            border: 1px solid #ddd;\n")
    f.write("            padding: 8px;\n")
    f.write("        }\n")
    f.write("        table.sortable th {\n")
    f.write("            background-color: #4CAF50;\n")
    f.write("            color: white;\n")
    f.write("        }\n")
    f.write("    </style>\n")
    f.write(
        '<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>\n'
    )
    f.write(
        '<input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for instruments..">\n'
    )
    f.write('<table class="sortable" id="instrumentTable">\n')
    f.write("    <thead>\n")
    f.write("        <tr>\n")
    f.write("            <th>Manufacturer</th>\n")
    f.write("            <th>Instrument</th>\n")
    f.write("            <th>Type</th>\n")
    f.write("            <th>Description</th>\n")
    f.write("        </tr>\n")
    f.write("    </thead>\n")
    f.write("    <tbody>\n")
    for device in devices:
        f.write(
            f"        <tr>\n"
            f"            <td>{devices[device]['manufacturer']}</td>\n"
            f"            <td>{devices[device]['name']}</td>\n"
            f"            <td>{devices[device]['type']}</td>\n"
            f"            <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='{devices[device]['url']}'>GitHub</a></td>\n"
            f"        </tr>\n"
        )
    f.write("    </tbody>\n")
    f.write("</table>\n")
    f.write("<script>\n")
    f.write("    function searchTable() {\n")
    f.write("        var input, filter, table, tr, td, i, j, txtValue;\n")
    f.write('        input = document.getElementById("searchInput");\n')
    f.write("        filter = input.value.toUpperCase();\n")
    f.write('        table = document.getElementById("instrumentTable");\n')
    f.write('        tr = table.getElementsByTagName("tr");\n')
    f.write("        for (i = 0; i < tr.length; i++) {\n")
    f.write('            td = tr[i].getElementsByTagName("td");\n')
    f.write("            for (j = 0; j < td.length; j++) {\n")
    f.write("                if (td[j]) {\n")
    f.write("                    txtValue = td[j].textContent || td[j].innerText;\n")
    f.write("                    if (txtValue.toUpperCase().indexOf(filter) > -1) {\n")
    f.write('                        tr[i].style.display = "";\n')
    f.write("                        break;\n")
    f.write("                    } else {\n")
    f.write('                        tr[i].style.display = "none";\n')
    f.write("                    }\n")
    f.write("                }\n")
    f.write("            }\n")
    f.write("        }\n")
    f.write("    }\n")
    f.write("</script>\n")
