===========
Instruments
===========

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
        }
    </style>
    <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>
    <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for instruments..">
    <table class="sortable" id="instrumentTable">
        <thead>
            <tr>
                <th>Manufacturer</th>
                <th>Instrument</th>
                <th>Description</th>
                <th>Type</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Keysight / Agilent</td>
                <td><a href="agilent_34401a/agilent_34401a">34401A</a></td>
                <td>Digital Multimeter</td>
                <td>DMM</td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>2000</td>
                <td>Digital Multimeter</td>
                <td>DMM</td>
            </tr>
            <tr>
                <td>Andor</td>
                <td>Newton CCD</td>
                <td>Andor</td>
                <td>Camera</td>
            </tr>
            <tr>
                <td>PC mouse</td>
                <td>Generic</td>
                <td>PC mouse (provided by <a href="https://sweep-me.net/">SweepMe!</a>)</td>
                <td>Mouse</td>
            </tr>
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