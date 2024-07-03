
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
                <th>Type</th>
                <th>Version</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>agilent</td>
                <td><a href='agilent_34401a/agilent_34401a'>34401a</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-agilent-34401a'>0.1.1</a></td>
            </tr>
            <tr>
                <td>andor</td>
                <td><a href='andor_newton/andor_newton'>newton</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-andor-newton'>0.1.0</a></td>
            </tr>
            <tr>
                <td>andor</td>
                <td>shamrock_500</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-andor-shamrock-500'>0.1.0</a></td>
            </tr>
            <tr>
                <td>cam</td>
                <td><a href='cam_control_pylablib/cam_control_pylablib'>control_pylablib</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-cam-control-pylablib'>0.1.4</a></td>
            </tr>
            <tr>
                <td>demo</td>
                <td>digital_multimeter</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-demo-digital-multimeter'>0.1.2</a></td>
            </tr>
            <tr>
                <td>demo</td>
                <td>instrument</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-demo-instrument'>0.1.1</a></td>
            </tr>
            <tr>
                <td>demo</td>
                <td>source_measure_unit</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-demo-source-measure-unit'>0.1.5</a></td>
            </tr>
            <tr>
                <td>keithley</td>
                <td><a href='keithley_2000/keithley_2000'>2000</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-2000'>0.1.0</a></td>
            </tr>
            <tr>
                <td>keithley</td>
                <td>2182a</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-2182a'>0.0.2</a></td>
            </tr>
            <tr>
                <td>keithley</td>
                <td><a href='keithley_237/keithley_237'>237</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-237'>0.1.1</a></td>
            </tr>
            <tr>
                <td>keithley</td>
                <td>2400</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-2400'>0.1.1</a></td>
            </tr>
            <tr>
                <td>keithley</td>
                <td>6221</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keithley-6221'>0.0.2</a></td>
            </tr>
            <tr>
                <td>keysight</td>
                <td><a href='keysight_b2912a/keysight_b2912a'>b2912a</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keysight-b2912a'>0.1.0</a></td>
            </tr>
            <tr>
                <td>keysight</td>
                <td><a href='keysight_e5270b/keysight_e5270b'>e5270b</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-keysight-e5270b'>0.1.1</a></td>
            </tr>
            <tr>
                <td>lakeshore</td>
                <td>f41</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-lakeshore-f41'>0.1.0</a></td>
            </tr>
            <tr>
                <td>mechonics</td>
                <td>cu30cl</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-mechonics-cu30cl'>0.1.0</a></td>
            </tr>
            <tr>
                <td>ni</td>
                <td>daq</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-ni-daq'>0.1.1</a></td>
            </tr>
            <tr>
                <td></td>
                <td><a href='PID/PID'>daq</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-PID'>0.1.8</a></td>
            </tr>
            <tr>
                <td>pi</td>
                <td>stage_e709</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-pi-stage-e709'>0.1.1</a></td>
            </tr>
            <tr>
                <td>rhode</td>
                <td>and_schwarz_smp_02</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-rhode-and-schwarz-smp-02'>0.1.0</a></td>
            </tr>
            <tr>
                <td>swabianinstruments</td>
                <td>timetagger</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-swabianinstruments-timetagger'>0.1.1</a></td>
            </tr>
            <tr>
                <td>thorlabs</td>
                <td>ddr_25</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-thorlabs-ddr-25'>0.0.2</a></td>
            </tr>
            <tr>
                <td>thorlabs</td>
                <td>K10CR1</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-thorlabs-K10CR1'>0.1.0</a></td>
            </tr>
            <tr>
                <td>thorlabs</td>
                <td>MFF</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-thorlabs-MFF'>0.1.0</a></td>
            </tr>
            <tr>
                <td>thorlabs</td>
                <td>TLPM</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-thorlabs-TLPM'>0.1.0</a></td>
            </tr>
            <tr>
                <td>trinamic</td>
                <td>tmcm_1110</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-trinamic-tmcm-1110'>0.1.0</a></td>
            </tr>
            <tr>
                <td>voltcraft</td>
                <td><a href='voltcraft_pps/voltcraft_pps'>pps</a></td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-voltcraft-pps'>0.1.1</a></td>
            </tr>
            <tr>
                <td>zaber</td>
                <td>rst240b_e08</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-zaber-rst240b-e08'>0.1.0</a></td>
            </tr>
            <tr>
                <td>zurich</td>
                <td>instruments_mfli</td>
                <td></td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-zurich-instruments-mfli'>0.1.0</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Webcam</a></td>
                <td>Camera</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>DeviceClass (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>template</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>HP (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4284A</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Hameg (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>HM8118</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>E498xA</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>ZurichInstruments (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>MFIA</a></td>
                <td>LCRmeter</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>SignalRecovery (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>7265DSP</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>SignalRecovery (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>7280DSP</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Stanford (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SR830</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Stanford (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SR86x</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>ZurichInstruments (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>MFLI</a></td>
                <td>LockIn</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Accurion (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>EP4</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Advantest (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>R6552</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>AllPins</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>DHTxx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>DS18x20</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>GY-521</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Inputs</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>PulseCount</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>CreaPhys (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>RCU001</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>DeviceClass (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>template-minimal</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Fluke (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>8842A</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>GPS (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>EricssonF5521gw</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>GQ (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>GMC-300E</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Hamamatsu (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>C12918</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>IC5</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SQC-310C</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SQM-160</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>STM-2XM</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Inficon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>XTM2</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Jyetech (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Capmeter</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>2000</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>2700</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>3706A</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>617</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>6485</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>6514</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>6517</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>740</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Kern (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Balance</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>532xx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>8163x</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>N774x</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Labjack (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>T-Series-ADC</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Labjack (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>T-Series-Counter</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Lauda (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>EcolineRE3xx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Leap (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Motion</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Leybold (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>CombivacCM31</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>MCC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>DAQ</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Minolta (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>CS100A</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>NI (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>VirtualBench</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Newport (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>1835C</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>OpsensSolutions (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>CoreSens</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Optris (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>CT</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>CPU-Memory</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Gamepad</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Joystick</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Microphone</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Midi</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Mouse</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Screenshot</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Time</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>WebSocket</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>phyphox</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PCsensor (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>HidTEMPer</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PREVAC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>TMC13</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PfeifferVacuum (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>TPGxxx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PhotoResearch (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>PR-655</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PyroScience (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>FireSting-O2</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Rigol (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>DM30xx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Sycon (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>STM-100</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Thorlabs (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>PM100</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>UniTrend (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>UT61E-USB</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Voltcraft (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>K204</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Voltcraft (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>VC840</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-0-10V-Rx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-4-20mA-Rx</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-Light-V3</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-Meteo-V2</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-PT100</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-Pressure</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-Thermocouple</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-Volt</a></td>
                <td>Logger</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Bentham (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>TMc300</a></td>
                <td>Monochromator</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Newport (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>OrielCornerstone260</a></td>
                <td>Monochromator</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>QuantumDesign (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>MSH-300</a></td>
                <td>Monochromator</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>E507x</a></td>
                <td>NetworkAnalyzer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>PNA</a></td>
                <td>NetworkAnalyzer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>ZNL</a></td>
                <td>NetworkAnalyzer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>CNC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Grbl</a></td>
                <td>Robot</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Dobot (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>MG400</a></td>
                <td>Robot</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Dobot (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Magician</a></td>
                <td>Robot</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Rotrics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>DexArm</a></td>
                <td>Robot</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>415x</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>B1500</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>B29xx</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>N6705A</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>BKPrecision (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>178x</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>HP (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4142B</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>HP (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4145</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>KORAD (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>KD3005P</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>KORAD (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>KWR100</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>236</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>2400</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>2450</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>26xx</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>4200-SCS</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>N6705</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Manson (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>HCS-3xxx</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>RS (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>RSPD3303C</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>HMP4000</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>NGx</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Simulation (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Diode</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>TDKLambda (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Genesys</a></td>
                <td>SMU</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>RedPitaya (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>STEMlab</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>HMO3004</a></td>
                <td>Scope</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>RTE</a></td>
                <td>Scope</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Tektronix (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>DPO7000</a></td>
                <td>Scope</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>33220A</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Agilent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>33600A</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>AimTTi (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>TGP3122</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>HP (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>8114A</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>81150A</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Siglent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SDG2000X</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Stanford (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>DG535</a></td>
                <td>Signal</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Labsphere (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>CDS6x0</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>OceanOptics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>NIRQuest</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>OceanOptics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>USB4000</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>RGBphotonics (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Qwave</a></td>
                <td>Spectrometer</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Acton (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>FA-448</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>MCP4728</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Outputs</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>PWM</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Servo</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>StepMotor</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Arduino (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>StepperMotor</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Bentham (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>418F</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Bentham (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>610</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>BiophysicalTools (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>P2CS</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Bronkhorst (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Propar</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>CTS (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>CS</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Coherent (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Chameleon</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>EXFO (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>MXS-9100</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>FTDI (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>FTD2xx</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Festo (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>edrive</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>707B</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keithley (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>7x7x</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>34980A</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>815xxA</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>819xxA</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>B2200A</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>E5250A</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Keysight (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>N777x</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Labjack (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>T-Series-TTL</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>LandgrafHLL (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>LA-1xx</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>MBRAUN (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SCU101</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>NF (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>CA5351</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Nanotec (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SMCI</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Newport (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>3502</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>OWIS (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>PS10-32</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>OceanControls (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>KTx-290</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Omnicure (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>S2000</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>ParallelPort</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>VariableWait</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PC (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Winsound</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>PicardIndustries (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>USB-Filterwheel</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Stanford (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SR570</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>TOFRA (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Filterwheel</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Thorlabs (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>FW102C</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Thorlabs (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>K10CR1</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-0-10V-Tx</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-MaxiPowerRelay</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Yoctopuce (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Yocto-Relay</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Zaber (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Motion</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>mbTechnologies (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>HVM</a></td>
                <td>Switch</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Accretech (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>UFseries</a></td>
                <td>WaferProber</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>BELEKTRONIG (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>BTC-LAB</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>BelektroniG (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>BTC-LAB</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>BelektroniG (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>HATControl</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Eurotherm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>22xx</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Eurotherm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>24xx</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Eurotherm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>32xx</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Eurotherm (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>350x</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>LakeShore (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Model33x</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Linkam (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>T95</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>OxfordInstruments (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>MercuryiTC</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>ScientificInstruments (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Model9700</a></td>
                <td>Temperature</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>Cascade (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>Nucleus</a></td>
                <td>WaferProber</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
            </tr>
            <tr>
                <td>MPI (<a href='SweepMe_drivers'>SweepMe!</a>)</td>
                <td>SENTIO</a></td>
                <td>WaferProber</td>
                <td><a href='https://pypi.org/project/nomad-camels-driver-SweepMe-device'>0.1.1</a></td>
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