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
                <td>Keysight</td>
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
                <td>Andor Newton</td>
                <td>CCD Camera</td>
                <td>Camera</td>
                <td>Andor</td>
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
            var input, filter, table, tr, td, i, txtValue;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase();
            table = document.getElementById("instrumentTable");
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td")[0];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }       
            }
        }
    </script>