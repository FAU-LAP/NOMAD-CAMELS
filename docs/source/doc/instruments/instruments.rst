
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
        <tbody>
            <tr>
                <td>Keysight / Agilent</td>
                <td>33220a</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-agilent-33220a'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent</td>
                <td><a href='agilent_34401a/agilent_34401a'>34401a</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-agilent-34401a'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent</td>
                <td>34970</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-agilent-34970'>0.1.3</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent</td>
                <td>E363x</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-agilent-e363x'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Andor</td>
                <td><a href='andor_newton/andor_newton'>Newton</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-andor-newton'>0.1.4</a></td>
            </tr>
            <tr>
                <td>Andor</td>
                <td>Shamrock_500</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-andor-shamrock-500'>0.1.3</a></td>
            </tr>
            <tr>
                <td>Cam</td>
                <td><a href='cam_control_pylablib/cam_control_pylablib'>Control_pylablib</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-cam-control-pylablib'>0.1.4</a></td>
            </tr>
            <tr>
                <td>Cryovac</td>
                <td>Tic_500</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-cryovac-tic-500'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Demo</td>
                <td>Digital_multimeter</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-demo-digital-multimeter'>0.1.3</a></td>
            </tr>
            <tr>
                <td>Demo</td>
                <td>Instrument</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-demo-instrument'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Demo</td>
                <td>Source_measure_unit</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-demo-source-measure-unit'>0.1.6</a></td>
            </tr>
            <tr>
                <td>Epics</td>
                <td>Instrument</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-epics-instrument'>0.1.2</a></td>
            </tr>
            <tr>
                <td>Eurotherm</td>
                <td>Bisynch</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-eurotherm-bisynch'>0.1.0</a></td>
            </tr>
            <tr>
                <td>IBeam</td>
                <td>Smart</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-iBeam-smart'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td><a href='keithley_2000/keithley_2000'>2000</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-2000'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>2182a</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-2182a'>0.0.2</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td><a href='keithley_237/keithley_237'>237</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-237'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>2400</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-2400'>0.1.2</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>6221</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-6221'>0.0.2</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent</td>
                <td><a href='keysight_b2912a/keysight_b2912a'>B2912a</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keysight-b2912a'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent</td>
                <td><a href='keysight_e5270b/keysight_e5270b'>E5270b</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keysight-e5270b'>0.1.2</a></td>
            </tr>
            <tr>
                <td>Lakeshore</td>
                <td>F41</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-lakeshore-f41'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Leybold</td>
                <td>C_move_1250</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-leybold-c-move-1250'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Mechonics</td>
                <td>Cu30cl</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-mechonics-cu30cl'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Ni</td>
                <td>Daq</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-ni-daq'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Opc</td>
                <td>Ua_instrument</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-opc-ua-instrument'>0.1.6</a></td>
            </tr>
            <tr>
                <td></td>
                <td><a href='PID/PID'>PID</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-PID'>0.1.10</a></td>
            </tr>
            <tr>
                <td>Pi</td>
                <td>Stage_e709</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-pi-stage-e709'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Rhode</td>
                <td>And_schwarz_smp_02</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-rhode-and-schwarz-smp-02'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Swabianinstruments</td>
                <td>Timetagger</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-swabianinstruments-timetagger'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Thorlabs</td>
                <td>Ddr_25</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-thorlabs-ddr-25'>0.0.2</a></td>
            </tr>
            <tr>
                <td>Thorlabs</td>
                <td>K10CR1</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-thorlabs-K10CR1'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Thorlabs</td>
                <td>MFF</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-thorlabs-MFF'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Thorlabs</td>
                <td>TLPM</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-thorlabs-TLPM'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Trinamic</td>
                <td>Tmcm_1110</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-trinamic-tmcm-1110'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Voltcraft</td>
                <td><a href='voltcraft_pps/voltcraft_pps'>Pps</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-voltcraft-pps'>0.1.2</a></td>
            </tr>
            <tr>
                <td>Voltcraft</td>
                <td>Psp</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-voltcraft-psp'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Zaber</td>
                <td>Rst240b_e08</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-zaber-rst240b-e08'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Zurich</td>
                <td>Instruments_mfli</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-zurich-instruments-mfli'>0.1.0</a></td>
            </tr>
            <tr>
                <td>Basler (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Pylon</a></td>
                <td>Camera</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Formfactor (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Velox</a></td>
                <td>WaferProber</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Webcam</a></td>
                <td>Camera</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Deviceclass (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Template</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hp (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4284a</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hameg (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Hm8118</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4200-scs</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>590</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>E498xa</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Metrohm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Autolabpgstat</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Simulation (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Driver</a></td>
                <td>WaferProber</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Zurichinstruments (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mfia</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Signalrecovery (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>7265dsp</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Signalrecovery (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>7280dsp</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Stanford (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Sr830</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Stanford (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Sr86x</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Zurichinstruments (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mfli</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Accurion (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ep4</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Advantest (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>R6552</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Allpins</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Dhtxx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ds18x20</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Gy-521</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Inputs</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Pulsecount</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Calliope (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mini3</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Creaphys (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Rcu001</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Datron (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>10x1</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Deviceclass (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Template-minimal</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Fluke (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>8842a</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Gps (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ericssonf5521gw</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Gq (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Gmc-300e</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hp (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>3456a</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hp (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>3457a</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hamamatsu (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>C12918</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ic5</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Sqc-310c</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Sqm-160</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Stm-2xm</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Xtm2</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Jyetech (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Capmeter</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>2000</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>2700</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>3706a</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>617</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>6485</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>6514</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>6517</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>740</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Kern (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Balance</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>34401a</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>3441xa</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>532xx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>8163x</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>N774x</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Lumiloop (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Lspm</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Labjack (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>T-series-adc</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Labjack (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>T-series-counter</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Lauda (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ecolinere3xx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Leap (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Motion</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Leybold (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Combivaccm31</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Mcc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Daq</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Minolta (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Cs100a</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Ni (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Virtualbench</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Newport (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>1835c</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Opsenssolutions (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Coresens</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Optris (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ct</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Cpu-memory</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Gamepad</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Joystick</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Microphone</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Midi</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mouse</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Screenshot</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Time</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Websocket</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Phyphox</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pcsensor (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Hidtemper</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Prevac (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Tm1x</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Prevac (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Tmc13</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pfeiffervacuum (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Tpgxxx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Photoresearch (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Pr-655</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pyroscience (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Firesting-o2</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Racaldana (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>90x5a</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rigol (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Dm30xx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Nrt-zxx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Nrt</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Rtx</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Simulation (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Multimeter</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Solartron (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>70x1</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Sycon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Stm-100</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Tektronix (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Dposeries</a></td>
                <td>Scope</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Thorlabs (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Pm100</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Unitrend (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ut61e-usb</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Voltcraft (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>K204</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Voltcraft (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Vc840</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-0-10v-rx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-4-20ma-rx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-light-v3</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-meteo-v2</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-pt100</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-pressure</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-thermocouple</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-volt</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Bentham (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Tmc300</a></td>
                <td>Monochromator</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Newport (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Orielcornerstone260</a></td>
                <td>Monochromator</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Quantumdesign (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Msh-300</a></td>
                <td>Monochromator</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>E507x</a></td>
                <td>NetworkAnalyzer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Pna</a></td>
                <td>NetworkAnalyzer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Znl</a></td>
                <td>NetworkAnalyzer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Cnc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Grbl</a></td>
                <td>Robot</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Dobot (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mg400</a></td>
                <td>Robot</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Dobot (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Magician</a></td>
                <td>Robot</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rotrics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Dexarm</a></td>
                <td>Robot</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>415x</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>B1500</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>B29xx</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>N6705a</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Aimtti (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Cpxseries</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Bkprecision (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>178x</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Ea (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ps2000</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hp (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4141b</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hp (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4142b</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hp (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4145</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Korad (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Kd3005p</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Korad (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Kwr100</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>236</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>2400</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>2450</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>26xx</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>E3631a</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>E3632a</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>N6705</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Manson (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Hcs-3xxx</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rs (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Rspd3303c</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Hmp4000</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ngx</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Simulation (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Diode</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Tdklambda (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Genesys</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Aspectsystems (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Idsmux</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Exr</a></td>
                <td>Scope</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Redpitaya (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Stemlab</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rigol (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Dhoseries</a></td>
                <td>Scope</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Hmo3004</a></td>
                <td>Scope</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>33220a</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>33600a</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Aimtti (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Tgp3122</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Hp (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>8114a</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>81150a</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Smb100a</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Siglent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Sdg2000x</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Stanford (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Dg535</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Labsphere (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Cds6x0</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Oceanoptics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Nirquest</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Oceanoptics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Oceandirect</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Oceanoptics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Usb4000</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rgbphotonics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Qwave</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Rohde&schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Fpcseries</a></td>
                <td>SpectrumAnalyzer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Ar (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Amplifier</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Acton (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Fa-448</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mcp4728</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Outputs</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Pwm</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Servo</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Stepmotor</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Steppermotor</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Bentham (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>418f</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Bentham (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>610</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Biophysicaltools (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>P2cs</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Bronkhorst (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Propar</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Cts (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Cs</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Coherent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Chameleon</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Exfo (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mxs-9100</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Ftdi (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ftd2xx</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Festo (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Edrive</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>707a</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>707b</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>7x7x</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>34980a</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>815xxa</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>819xxa</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>B2200a</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>E5250a</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Keysight / Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>N777x</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Labjack (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>T-series-ttl</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Landgrafhll (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>La-1xx</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Mbraun (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Scu101</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Nf (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ca5351</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Nanotec (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Smci</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Newport (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>3502</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Owis (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ps10-32</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Oceancontrols (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ktx-290</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Omnicure (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>S2000</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Optem (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Lamplink2ps</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Parallelport</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Variablewait</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Pc (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Winsound</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Prevac (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Tmc13-shutter</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Picardindustries (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Usb-filterwheel</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Stanford (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Sr570</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Tofra (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Filterwheel</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Thorlabs (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Fw102c</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Thorlabs (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>K10cr1</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-0-10v-tx</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-maxipowerrelay</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-relay</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Zaber (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Motion</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Mbtechnologies (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Hvm</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Accretech (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Ufseries</a></td>
                <td>WaferProber</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Belektronig (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Btc-lab</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Belektronig (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Btc-lab</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Belektronig (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Hatcontrol</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Eurotherm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>22xx</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Eurotherm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>24xx</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Eurotherm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>32xx</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Eurotherm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>350x</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Lakeshore (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Model32x</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Lakeshore (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Model33x</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Linkam (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>T95</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Oxfordinstruments (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mercuryitc</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Scientificinstruments (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Model9700</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Cascade (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Nucleus</a></td>
                <td>WaferProber</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
            </tr>
            <tr>
                <td>Mpi (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Sentio</a></td>
                <td>WaferProber</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.2.0</a></td>
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
    