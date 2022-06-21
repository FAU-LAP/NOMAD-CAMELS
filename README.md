# CAMELS  
## Configurable Application for MEasurement- and Laboratory-Systems  


Temperature dependent current-voltage (IV) sweeps  
Measurement procedure:  
Have a temperature (or list of temperatures) for which you want to perform a voltage-current sweep measurement. This is typically done for semiconductor samples.   
Requirements:  
Running the measurement software:  
•	PC with Windows 10, Version 2004 or higher  
•	Install WSL 1 Ubuntu (WSL 1 is required for USB-serial connections!)  

### WSL  
Enable WSL on your PC: open Windows PowerShell as administrator and enter  
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux  
Open the now available Ubuntu WSL Terminal (should open automatically) and enter:  
wsl --set-default-version 1  
wsl --install -d Ubuntu  
If you have more than the installed Ubuntu wsl (show installed WSLs with wsl –l -v) make sure the default WSL is the installed Ubuntu. Enter:  
wsl --setdefault Ubuntu  
UNIX username: epics  
New Password: <Password>  
•	Install Basic EPICS distribution  
sudo apt-get update  
sudo apt-get upgrade  
Restart Ubuntu-Terminal  
git clone https://gitlab.fhi.mpg.de/epics-tools/epics-edge-setup.git  
(From https://gitlab.fhi.mpg.de/epics-tools/epics-edge-setup)  
sudo python3 debian-setup.py  
Default answers:  
“create user 'epics'? (y/n):n #answer y if you don’t have a linux user called “epics”  
upgrade installed software packages? (y/n):y  
save the IPv4 and IPv6 rules  
enable root ssh login? (y/n): y  
install basic dnsmasq config for DHCP and DNS? (y/n): n  
install procServ to /opt ? (y/n): y  
install EPICS base? (y/n): y #important  
install FHI support modules compilation ? (y/n): y #important  
install ca-gateway to /opt/? (y/n): y”  
Restart Ubuntu Terminal  

### Install CAMELS measurement software  
Create a Folder called CAMELS in %appdata%/local/CAMELS/ and add the empty file logging.log #this might not be necessary depending on the github version of CAMELS  
In Windows PowerShell go the Windows folder you want CAMELS to be installed in and enter:  
git config --global core.eol lf  
git config --global core.autocrlf input  
(this is so that all line endings are in UNIX format)  
git clone https://github.com/FAU-LAP/CAMELS.git  

To be able to use a PID controller go to EPICS/epics-support/ and enter  
git clone https://github.com/epics-modules/std.git  

If you are using a different WSL than Ubuntu (for example Ubuntu20.04 or Debian) you have to change the epics_path in EPICS_handling/make_ioc.py to the correct path.  
Create a sym-link from  
/home/epics/EPICS/epics-support/RELEASE.local  
to  
/home/epics/IOCs/RELEASE.local  
Run  
import databroker  
print(databroker.catalog_search_path())  
to see where CAMELS saves the catalog (measurement runs). Create the necessary folders (ex. C:/Users/<User>/Anaconda3/envs/olaf/share/intake) and create a file called CATALOG_NAME.yml in which following code should be written:  
sources:  
  CATALOG_NAME:  
    driver: "bluesky-msgpack-catalog"  
    args:  
      paths:  
        - "DESTINATION_DIRECTORY/*.msgpack"  
DESTINATION_DIRECTORY is the directory you want the data to be saved to.  

### Setting up CAMELS  
Enter the desired user name and sample ID at the top. Use the “+” under “Devices” to add the required devices. For our case, it is the Keithley E5270B and the Agilent 34401A, as well as the virtual PID device.  
Then add a new measurement procedure (now called protocol) using the “+” under “Protocols”. Rename the protocol as desired. When clicking on the added protocol one can see below “Sequence” the measurement sequence (setting, reading, waiting, …) that will be performed when the measurement protocol is run. Steps in the sequence can be added by right clicking or using the “+” symbol.  
Measurement devices:  
•	Voltage source (IV-sweep)  
Any voltage-sourcing device can be used. We use the Keithley E5270B SMU with 5271B insert for setting the voltage (and measuring the current).  
•	Current measurement (IV-sweep)  
Any current-sourcing device can be used. We use the Keithley E5270B SMU with 5271B insert for (setting the voltage and) measuring the current.  
•	Heating current (sample)  
The sample is heated by electrical current supplied by a current source. In our case this is done by a second channel of the E5270B SMU.  
•	Temperature measurement  
The temperature of the sample must be measured. In our case this is done by reading the resistance value of a Pt1000 (Resistance Temperature Detector: RTD) and then converting the measured resistance to a temperature. We measure the resistance with a digital multi meter: Agilent 34401A.  
•	PID  
The heating current is controlled by a virtual PID device (internally in EPICS). The input value for the PID is the measured temperature of the sample. The output of the PID is the heating current.  
Device communication:  
We communicate with the devices via GPIB-Ethernet (LAN) adapter from Prologix. In general any communication type (serial, LAN, …) can be used. This option will be implemented in a more mature version of CAMELS.  
Device prices:  
•	E5270B with 2 slots: 15.000€  
Any voltage source can be used instead of the expensive E5270B: for example Keysight Technologies U2722A/U2723A USB Modular Source Measure Unit (~2.000€)  
•	Agilent 34401A: 1000€  
•	Pt1000: 2€  
•	Prologix GPIB-Ethernet (LAN) Controller: 500€  
•	Hint: Any device that can supply +-5V can be used as a voltage sweep source. This then needs to be combined with any current measuring device.  




### Environment

download python from Web, then:  
python-3.9.13-amd64.exe Include_tcltk=0 /passive  
pip3.9 install virtualenv  

inside CAMELS-folder:
virtualenv -p python3 camelsEnv
camelsEnv/Scripts/activate
camelsEnv/Scripts/pip install -r requirements.txt