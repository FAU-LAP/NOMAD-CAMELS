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
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>PC</td>
                <td>Webcam</td>
                <td>Camera</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Camera-PC_Webcam'>GitHub</a></td>
            </tr>
            <tr>
                <td>DeviceClass</td>
                <td>template</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-DeviceClass_template'>GitHub</a></td>
            </tr>
            <tr>
                <td>HP</td>
                <td>4284A</td>
                <td>LCRmeter</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LCRmeter-HP_4284A'>GitHub</a></td>
            </tr>
            <tr>
                <td>Hameg</td>
                <td>HM8118</td>
                <td>LCRmeter</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LCRmeter-Hameg_HM8118'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>E498xA</td>
                <td>LCRmeter</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LCRmeter-Keysight_E498xA'>GitHub</a></td>
            </tr>
            <tr>
                <td>ZurichInstruments</td>
                <td>MFIA</td>
                <td>LCRmeter</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LCRmeter-ZurichInstruments_MFIA'>GitHub</a></td>
            </tr>
            <tr>
                <td>SignalRecovery</td>
                <td>7265DSP</td>
                <td>LockIn</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LockIn-SignalRecovery_7265DSP'>GitHub</a></td>
            </tr>
            <tr>
                <td>SignalRecovery</td>
                <td>7280DSP</td>
                <td>LockIn</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LockIn-SignalRecovery_7280DSP'>GitHub</a></td>
            </tr>
            <tr>
                <td>Stanford</td>
                <td>SR830</td>
                <td>LockIn</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LockIn-Stanford_SR830'>GitHub</a></td>
            </tr>
            <tr>
                <td>Stanford</td>
                <td>SR86x</td>
                <td>LockIn</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LockIn-Stanford_SR86x'>GitHub</a></td>
            </tr>
            <tr>
                <td>ZurichInstruments</td>
                <td>MFLI</td>
                <td>LockIn</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/LockIn-ZurichInstruments_MFLI'>GitHub</a></td>
            </tr>
            <tr>
                <td>Accurion</td>
                <td>EP4</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Accurion_EP4'>GitHub</a></td>
            </tr>
            <tr>
                <td>Advantest</td>
                <td>R6552</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Advantest_R6552'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>AllPins</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Arduino_AllPins'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>DHTxx</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Arduino_DHTxx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>DS18x20</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Arduino_DS18x20'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>GY-521</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Arduino_GY-521'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>Inputs</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Arduino_Inputs'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>PulseCount</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Arduino_PulseCount'>GitHub</a></td>
            </tr>
            <tr>
                <td>CreaPhys</td>
                <td>RCU001</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-CreaPhys_RCU001'>GitHub</a></td>
            </tr>
            <tr>
                <td>DeviceClass</td>
                <td>template-minimal</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-DeviceClass_template-minimal'>GitHub</a></td>
            </tr>
            <tr>
                <td>Fluke</td>
                <td>8842A</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Fluke_8842A'>GitHub</a></td>
            </tr>
            <tr>
                <td>GPS</td>
                <td>EricssonF5521gw</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-GPS_EricssonF5521gw'>GitHub</a></td>
            </tr>
            <tr>
                <td>GQ</td>
                <td>GMC-300E</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-GQ_GMC-300E'>GitHub</a></td>
            </tr>
            <tr>
                <td>Hamamatsu</td>
                <td>C12918</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Hamamatsu_C12918'>GitHub</a></td>
            </tr>
            <tr>
                <td>Inficon</td>
                <td>IC5</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Inficon_IC5'>GitHub</a></td>
            </tr>
            <tr>
                <td>Inficon</td>
                <td>SQC-310C</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Inficon_SQC-310C'>GitHub</a></td>
            </tr>
            <tr>
                <td>Inficon</td>
                <td>SQM-160</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Inficon_SQM-160'>GitHub</a></td>
            </tr>
            <tr>
                <td>Inficon</td>
                <td>STM-2XM</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Inficon_STM-2XM'>GitHub</a></td>
            </tr>
            <tr>
                <td>Inficon</td>
                <td>XTM2</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Inficon_XTM2'>GitHub</a></td>
            </tr>
            <tr>
                <td>Jyetech</td>
                <td>Capmeter</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Jyetech_Capmeter'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>2000</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keithley_2000'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>2700</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keithley_2700'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>3706A</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keithley_3706A'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>617</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keithley_617'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>6485</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keithley_6485'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>6514</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keithley_6514'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>6517</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keithley_6517'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>740</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keithley_740'>GitHub</a></td>
            </tr>
            <tr>
                <td>Kern</td>
                <td>Balance</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Kern_Balance'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>532xx</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keysight_532xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>8163x</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keysight_8163x'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>N774x</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Keysight_N774x'>GitHub</a></td>
            </tr>
            <tr>
                <td>Labjack</td>
                <td>T-Series-ADC</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Labjack_T-Series-ADC'>GitHub</a></td>
            </tr>
            <tr>
                <td>Labjack</td>
                <td>T-Series-Counter</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Labjack_T-Series-Counter'>GitHub</a></td>
            </tr>
            <tr>
                <td>Lauda</td>
                <td>EcolineRE3xx</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Lauda_EcolineRE3xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Leap</td>
                <td>Motion</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Leap_Motion'>GitHub</a></td>
            </tr>
            <tr>
                <td>Leybold</td>
                <td>CombivacCM31</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Leybold_CombivacCM31'>GitHub</a></td>
            </tr>
            <tr>
                <td>MCC</td>
                <td>DAQ</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-MCC_DAQ'>GitHub</a></td>
            </tr>
            <tr>
                <td>Minolta</td>
                <td>CS100A</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Minolta_CS100A'>GitHub</a></td>
            </tr>
            <tr>
                <td>NI</td>
                <td>VirtualBench</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-NI_VirtualBench'>GitHub</a></td>
            </tr>
            <tr>
                <td>Newport</td>
                <td>1835C</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Newport_1835C'>GitHub</a></td>
            </tr>
            <tr>
                <td>OpsensSolutions</td>
                <td>CoreSens</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-OpsensSolutions_CoreSens'>GitHub</a></td>
            </tr>
            <tr>
                <td>Optris</td>
                <td>CT</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Optris_CT'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>CPU-Memory</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PC_CPU-Memory'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>Gamepad</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PC_Gamepad'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>Joystick</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PC_Joystick'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>Microphone</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PC_Microphone'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>Midi</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-PC_Midi'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>Mouse</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-PC_Mouse'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>Screenshot</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PC_Screenshot'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>Time</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PC_Time'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>WebSocket</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PC_WebSocket'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>phyphox</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PC_phyphox'>GitHub</a></td>
            </tr>
            <tr>
                <td>PCsensor</td>
                <td>HidTEMPer</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PCsensor_HidTEMPer'>GitHub</a></td>
            </tr>
            <tr>
                <td>PREVAC</td>
                <td>TMC13</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PREVAC_TMC13'>GitHub</a></td>
            </tr>
            <tr>
                <td>PfeifferVacuum</td>
                <td>TPGxxx</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PfeifferVacuum_TPGxxx'>GitHub</a></td>
            </tr>
            <tr>
                <td>PhotoResearch</td>
                <td>PR-655</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PhotoResearch_PR-655'>GitHub</a></td>
            </tr>
            <tr>
                <td>PyroScience</td>
                <td>FireSting-O2</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-PyroScience_FireSting-O2'>GitHub</a></td>
            </tr>
            <tr>
                <td>Rigol</td>
                <td>DM30xx</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Rigol_DM30xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Sycon</td>
                <td>STM-100</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Sycon_STM-100'>GitHub</a></td>
            </tr>
            <tr>
                <td>Thorlabs</td>
                <td>PM100</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Thorlabs_PM100'>GitHub</a></td>
            </tr>
            <tr>
                <td>UniTrend</td>
                <td>UT61E-USB</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-UniTrend_UT61E-USB'>GitHub</a></td>
            </tr>
            <tr>
                <td>Voltcraft</td>
                <td>K204</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Voltcraft_K204'>GitHub</a></td>
            </tr>
            <tr>
                <td>Voltcraft</td>
                <td>VC840</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Voltcraft_VC840'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-0-10V-Rx</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Yoctopuce_Yocto-0-10V-Rx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-4-20mA-Rx</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Yoctopuce_Yocto-4-20mA-Rx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-Light-V3</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Yoctopuce_Yocto-Light-V3'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-Meteo-V2</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Yoctopuce_Yocto-Meteo-V2'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-PT100</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Yoctopuce_Yocto-PT100'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-Pressure</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Yoctopuce_Yocto-Pressure'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-Thermocouple</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Yoctopuce_Yocto-Thermocouple'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-Volt</td>
                <td>Logger</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Logger-Yoctopuce_Yocto-Volt'>GitHub</a></td>
            </tr>
            <tr>
                <td>Bentham</td>
                <td>TMc300</td>
                <td>Monochromator</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Monochromator-Bentham_TMc300'>GitHub</a></td>
            </tr>
            <tr>
                <td>Newport</td>
                <td>OrielCornerstone260</td>
                <td>Monochromator</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Monochromator-Newport_OrielCornerstone260'>GitHub</a></td>
            </tr>
            <tr>
                <td>QuantumDesign</td>
                <td>MSH-300</td>
                <td>Monochromator</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Monochromator-QuantumDesign_MSH-300'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>E507x</td>
                <td>NetworkAnalyzer</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/NetworkAnalyzer-Keysight_E507x'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>PNA</td>
                <td>NetworkAnalyzer</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/NetworkAnalyzer-Keysight_PNA'>GitHub</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz</td>
                <td>ZNL</td>
                <td>NetworkAnalyzer</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/NetworkAnalyzer-Rohde&Schwarz_ZNL'>GitHub</a></td>
            </tr>
            <tr>
                <td>CNC</td>
                <td>Grbl</td>
                <td>Robot</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Robot-CNC_Grbl'>GitHub</a></td>
            </tr>
            <tr>
                <td>Dobot</td>
                <td>MG400</td>
                <td>Robot</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Robot-Dobot_MG400'>GitHub</a></td>
            </tr>
            <tr>
                <td>Dobot</td>
                <td>Magician</td>
                <td>Robot</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Robot-Dobot_Magician'>GitHub</a></td>
            </tr>
            <tr>
                <td>Rotrics</td>
                <td>DexArm</td>
                <td>Robot</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Robot-Rotrics_DexArm'>GitHub</a></td>
            </tr>
            <tr>
                <td>Agilent</td>
                <td>415x</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Agilent_415x'>GitHub</a></td>
            </tr>
            <tr>
                <td>Agilent</td>
                <td>B1500</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Agilent_B1500'>GitHub</a></td>
            </tr>
            <tr>
                <td>Agilent</td>
                <td>B29xx</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Agilent_B29xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Agilent</td>
                <td>N6705A</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Agilent_N6705A'>GitHub</a></td>
            </tr>
            <tr>
                <td>BKPrecision</td>
                <td>178x</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-BKPrecision_178x'>GitHub</a></td>
            </tr>
            <tr>
                <td>HP</td>
                <td>4142B</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-HP_4142B'>GitHub</a></td>
            </tr>
            <tr>
                <td>HP</td>
                <td>4145</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-HP_4145'>GitHub</a></td>
            </tr>
            <tr>
                <td>KORAD</td>
                <td>KD3005P</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-KORAD_KD3005P'>GitHub</a></td>
            </tr>
            <tr>
                <td>KORAD</td>
                <td>KWR100</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-KORAD_KWR100'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>236</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Keithley_236'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>2400</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Keithley_2400'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>2450</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Keithley_2450'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>26xx</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Keithley_26xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>4200-SCS</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-Keithley_4200-SCS'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>N6705</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-Keysight_N6705'>GitHub</a></td>
            </tr>
            <tr>
                <td>Manson</td>
                <td>HCS-3xxx</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Manson_HCS-3xxx'>GitHub</a></td>
            </tr>
            <tr>
                <td>RS</td>
                <td>RSPD3303C</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-RS_RSPD3303C'>GitHub</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz</td>
                <td>HMP4000</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Rohde&Schwarz_HMP4000'>GitHub</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz</td>
                <td>NGx</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Rohde&Schwarz_NGx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Simulation</td>
                <td>Diode</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-Simulation_Diode'>GitHub</a></td>
            </tr>
            <tr>
                <td>TDKLambda</td>
                <td>Genesys</td>
                <td>SMU</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/SMU-TDKLambda_Genesys'>GitHub</a></td>
            </tr>
            <tr>
                <td>RedPitaya</td>
                <td>STEMlab</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-RedPitaya_STEMlab'>GitHub</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz</td>
                <td>HMO3004</td>
                <td>Scope</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Scope-Rohde&Schwarz_HMO3004'>GitHub</a></td>
            </tr>
            <tr>
                <td>Rohde&Schwarz</td>
                <td>RTE</td>
                <td>Scope</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Scope-Rohde&Schwarz_RTE'>GitHub</a></td>
            </tr>
            <tr>
                <td>Tektronix</td>
                <td>DPO7000</td>
                <td>Scope</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Scope-Tektronix_DPO7000'>GitHub</a></td>
            </tr>
            <tr>
                <td>Agilent</td>
                <td>33220A</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-Agilent_33220A'>GitHub</a></td>
            </tr>
            <tr>
                <td>Agilent</td>
                <td>33600A</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-Agilent_33600A'>GitHub</a></td>
            </tr>
            <tr>
                <td>AimTTi</td>
                <td>TGP3122</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-AimTTi_TGP3122'>GitHub</a></td>
            </tr>
            <tr>
                <td>HP</td>
                <td>8114A</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-HP_8114A'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>81150A</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-Keysight_81150A'>GitHub</a></td>
            </tr>
            <tr>
                <td>Siglent</td>
                <td>SDG2000X</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-Siglent_SDG2000X'>GitHub</a></td>
            </tr>
            <tr>
                <td>Stanford</td>
                <td>DG535</td>
                <td>Signal</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Signal-Stanford_DG535'>GitHub</a></td>
            </tr>
            <tr>
                <td>Labsphere</td>
                <td>CDS6x0</td>
                <td>Spectrometer</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Spectrometer-Labsphere_CDS6x0'>GitHub</a></td>
            </tr>
            <tr>
                <td>OceanOptics</td>
                <td>NIRQuest</td>
                <td>Spectrometer</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Spectrometer-OceanOptics_NIRQuest'>GitHub</a></td>
            </tr>
            <tr>
                <td>OceanOptics</td>
                <td>USB4000</td>
                <td>Spectrometer</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Spectrometer-OceanOptics_USB4000'>GitHub</a></td>
            </tr>
            <tr>
                <td>RGBphotonics</td>
                <td>Qwave</td>
                <td>Spectrometer</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Spectrometer-RGBphotonics_Qwave'>GitHub</a></td>
            </tr>
            <tr>
                <td>Acton</td>
                <td>FA-448</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Acton_FA-448'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>MCP4728</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Arduino_MCP4728'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>Outputs</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Arduino_Outputs'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>PWM</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Arduino_PWM'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>Servo</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Arduino_Servo'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>StepMotor</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Arduino_StepMotor'>GitHub</a></td>
            </tr>
            <tr>
                <td>Arduino</td>
                <td>StepperMotor</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Arduino_StepperMotor'>GitHub</a></td>
            </tr>
            <tr>
                <td>Bentham</td>
                <td>418F</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Bentham_418F'>GitHub</a></td>
            </tr>
            <tr>
                <td>Bentham</td>
                <td>610</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Bentham_610'>GitHub</a></td>
            </tr>
            <tr>
                <td>BiophysicalTools</td>
                <td>P2CS</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-BiophysicalTools_P2CS'>GitHub</a></td>
            </tr>
            <tr>
                <td>Bronkhorst</td>
                <td>Propar</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Bronkhorst_Propar'>GitHub</a></td>
            </tr>
            <tr>
                <td>CTS</td>
                <td>CS</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-CTS_CS'>GitHub</a></td>
            </tr>
            <tr>
                <td>Coherent</td>
                <td>Chameleon</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Coherent_Chameleon'>GitHub</a></td>
            </tr>
            <tr>
                <td>EXFO</td>
                <td>MXS-9100</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-EXFO_MXS-9100'>GitHub</a></td>
            </tr>
            <tr>
                <td>FTDI</td>
                <td>FTD2xx</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-FTDI_FTD2xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Festo</td>
                <td>edrive</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Festo_edrive'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>707B</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keithley_707B'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keithley</td>
                <td>7x7x</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keithley_7x7x'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>34980A</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keysight_34980A'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>815xxA</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keysight_815xxA'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>819xxA</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keysight_819xxA'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>B2200A</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keysight_B2200A'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>E5250A</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keysight_E5250A'>GitHub</a></td>
            </tr>
            <tr>
                <td>Keysight</td>
                <td>N777x</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Keysight_N777x'>GitHub</a></td>
            </tr>
            <tr>
                <td>Labjack</td>
                <td>T-Series-TTL</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Labjack_T-Series-TTL'>GitHub</a></td>
            </tr>
            <tr>
                <td>LandgrafHLL</td>
                <td>LA-1xx</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-LandgrafHLL_LA-1xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>MBRAUN</td>
                <td>SCU101</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-MBRAUN_SCU101'>GitHub</a></td>
            </tr>
            <tr>
                <td>NF</td>
                <td>CA5351</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-NF_CA5351'>GitHub</a></td>
            </tr>
            <tr>
                <td>Nanotec</td>
                <td>SMCI</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Nanotec_SMCI'>GitHub</a></td>
            </tr>
            <tr>
                <td>Newport</td>
                <td>3502</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Newport_3502'>GitHub</a></td>
            </tr>
            <tr>
                <td>OWIS</td>
                <td>PS10-32</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-OWIS_PS10-32'>GitHub</a></td>
            </tr>
            <tr>
                <td>OceanControls</td>
                <td>KTx-290</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-OceanControls_KTx-290'>GitHub</a></td>
            </tr>
            <tr>
                <td>Omnicure</td>
                <td>S2000</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Omnicure_S2000'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>ParallelPort</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-PC_ParallelPort'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>VariableWait</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-PC_VariableWait'>GitHub</a></td>
            </tr>
            <tr>
                <td>PC</td>
                <td>Winsound</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-PC_Winsound'>GitHub</a></td>
            </tr>
            <tr>
                <td>PicardIndustries</td>
                <td>USB-Filterwheel</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-PicardIndustries_USB-Filterwheel'>GitHub</a></td>
            </tr>
            <tr>
                <td>Stanford</td>
                <td>SR570</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Stanford_SR570'>GitHub</a></td>
            </tr>
            <tr>
                <td>TOFRA</td>
                <td>Filterwheel</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-TOFRA_Filterwheel'>GitHub</a></td>
            </tr>
            <tr>
                <td>Thorlabs</td>
                <td>FW102C</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Thorlabs_FW102C'>GitHub</a></td>
            </tr>
            <tr>
                <td>Thorlabs</td>
                <td>K10CR1</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Thorlabs_K10CR1'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-0-10V-Tx</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Yoctopuce_Yocto-0-10V-Tx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-MaxiPowerRelay</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Yoctopuce_Yocto-MaxiPowerRelay'>GitHub</a></td>
            </tr>
            <tr>
                <td>Yoctopuce</td>
                <td>Yocto-Relay</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Yoctopuce_Yocto-Relay'>GitHub</a></td>
            </tr>
            <tr>
                <td>Zaber</td>
                <td>Motion</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-Zaber_Motion'>GitHub</a></td>
            </tr>
            <tr>
                <td>mbTechnologies</td>
                <td>HVM</td>
                <td>Switch</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Switch-mbTechnologies_HVM'>GitHub</a></td>
            </tr>
            <tr>
                <td>Accretech</td>
                <td>UFseries</td>
                <td>WaferProber</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/WaferProber-Accretech_UFseries'>GitHub</a></td>
            </tr>
            <tr>
                <td>BELEKTRONIG</td>
                <td>BTC-LAB</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-BELEKTRONIG_BTC-LAB'>GitHub</a></td>
            </tr>
            <tr>
                <td>BelektroniG</td>
                <td>BTC-LAB</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-BelektroniG_BTC-LAB'>GitHub</a></td>
            </tr>
            <tr>
                <td>BelektroniG</td>
                <td>HATControl</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-BelektroniG_HATControl'>GitHub</a></td>
            </tr>
            <tr>
                <td>Eurotherm</td>
                <td>22xx</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-Eurotherm_22xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Eurotherm</td>
                <td>24xx</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-Eurotherm_24xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Eurotherm</td>
                <td>32xx</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-Eurotherm_32xx'>GitHub</a></td>
            </tr>
            <tr>
                <td>Eurotherm</td>
                <td>350x</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-Eurotherm_350x'>GitHub</a></td>
            </tr>
            <tr>
                <td>LakeShore</td>
                <td>Model33x</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-LakeShore_Model33x'>GitHub</a></td>
            </tr>
            <tr>
                <td>Linkam</td>
                <td>T95</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-Linkam_T95'>GitHub</a></td>
            </tr>
            <tr>
                <td>OxfordInstruments</td>
                <td>MercuryiTC</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-OxfordInstruments_MercuryiTC'>GitHub</a></td>
            </tr>
            <tr>
                <td>ScientificInstruments</td>
                <td>Model9700</td>
                <td>Temperature</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/Temperature-ScientificInstruments_Model9700'>GitHub</a></td>
            </tr>
            <tr>
                <td>Cascade</td>
                <td>Nucleus</td>
                <td>WaferProber</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/WaferProber-Cascade_Nucleus'>GitHub</a></td>
            </tr>
            <tr>
                <td>MPI</td>
                <td>SENTIO</td>
                <td>WaferProber</td>
                <td>Via<a href='https://sweep-me.net/devices'>SweepMe!</a>, see <a href='https://github.com/SweepMe/instrument-drivers/tree/main/src/WaferProber-MPI_SENTIO'>GitHub</a></td>
            </tr>
        </tbody>
    </table>
    <script>
        function searchTable() {
            var input, filter, table, tr, td, i, j, txtValue;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase();
            table = document.getElementById("instrumentTable");
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td");
                for (j = 0; j < td.length; j++) {
                    if (td[j]) {
                        txtValue = td[j].textContent || td[j].innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                            break;
                        } else {
                            tr[i].style.display = "none";
                        }
                    }
                }
            }
        }
    </script>
