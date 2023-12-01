# How to create a new IOC
This guide demonstrates how to create a new IOC from scratch to be able to communicate with basic serial devices or web servers/IP addresses.

We assume that you have installed `EPICS` as well as the `asyn` and `stream` support modules. 

This can be achieved by following our guide on How to install EPICS.
## EPICS Installation for UNIX
It is best to use a clean Debian installation for new IOCs.
It also makes things easier if you already created a user called `epics` with sudoers privileges and run all commands with this user.\
Make sure you have `git`, `python3` and `python3-requests` installed via 
```
sudo apt install git python3 python3-requests
```
Clone the epics-edge-setup from the [FHI GitLab](https://gitlab.fhi.mpg.de/epics-tools/epics-edge-setup).
```
git clone https://gitlab.fhi.mpg.de/epics-tools/epics-edge-setup.git
```

Then run the python installer with
```
sudo python3 debian-setup.py
```
Answer the following questions like this:

| Question | Answer                                                                     |
| -------- |----------------------------------------------------------------------------|
|create user 'epics'? | N (Y if you did not create the user `epics` yet)                           |
| upgrade installed software packages? | Y                                                                          |
|continue?| Y                                                                          |
|enable root ssh login? | N                                                                          |
|install basic dnsmasq config for DHCP and DNS?| N                                                                          |
|install procServ to /opt ?| Y (this allows you to easily start IOCs in the background)                 |
|install EPICS base?| Y (this is the core of the installtion)                                    |
|install FHI support modules compilation ?| Y (this installes important support modules rquired for basic use of IOCs) |
|install ca-gateway to /opt/?| N                                                                          |
|create FHI folder for user epics?| Y (this creates a folder with the correct `RELEASE.local` file in it)      |
Reboot your system so that all path variables are set correctly.

The installation of the support modules will most likely have failed as the asyn module does not build properly out of the box. To fix this we now need to correctly rebuild the support modules (especially asyn). For this navigate to `/EPICS/epics-support/asyn/configure/` and modify the `CONFIG_SITE` file.\
You must set `TIRPC` to `YES` so it should look like this 
```
...
# Some linux systems moved RPC related symbols to libtirpc
# To enable linking against this library, uncomment the following line
TIRPC=YES
...
```
navigate to `/EPICS/epics-support/` and run 
```
python3 BuildAll.py make
```

You should now have a running EPICS environment and can create your IOCs.



## Create folder structure for IOC
To at first create a basic IOC with no functionality create a folder on the same level as the `EPICS` folder with the name `IOCs`. This folder will contain any number of IOCs you will create. In this folder create a file called `RELEASE.local`. Into this file write:
```
#
# can not use ${HOME} due to auto generation on
# some submodules
SUPPORT=/home/epics/EPICS/epics-support

#  IPAC is only necessary if support for Greensprings IP488 is required
#  IPAC release V2-7 or later is required.
IPAC=$(SUPPORT)/ipac

# If CALC was built with SSCAN support then SSCAN must be defined for testEpicsApp
SSCAN=$(SUPPORT)/sscan

# SEQ is required for testIPServer
SNCSEQ=$(SUPPORT)/seq-2.2.8

## For sCalcout support in asynOctet - applications include asynCalc.dbd
CALC=$(SUPPORT)/calc

AUTOSAVE=$(SUPPORT)/autosave
BUSY=$(SUPPORT)/busy
IP=$(SUPPORT)/ip

ASYN=$(SUPPORT)/asyn
MOTOR=$(SUPPORT)/motor

MODBUS=$(SUPPORT)/modbus

DEVLIB=$(SUPPORT)/devlib2

STREAM=$(SUPPORT)/StreamDevice
# actively empty the PCRE variable since it otherwise tries to include the epics module PCRE instead of the system one
PCRE=
PCRE_LIB=/usr/lib/x86_64-linux-gnu/
PCRE_INCLUDE=/usr/include/

RECCASTER=$(SUPPORT)/recsync/client

#  EPICS_BASE 3.14.6 or later is required
EPICS_BASE=/home/epics/EPICS/epics-base
```
Make sure that the paths all exist. If you do not have or need all these modules in the support folder then remove the lines in this file. 

Now create a folder with the name of your IOC (or any name you like).
```
mkdir <ioc_name>
``` 
and go to this folder.

## Create an Empty IOC

In the empty folder we will now create a basic IOC with no functionality. Run following command

```
makeBaseApp.pl -t ioc <ioc_name>
makeBaseApp.pl -i -t ioc <ioc_name>
```

you do not need to give the IOC an additional name when you are prompted, simply hit _enter_.

Your folder structure should now look something like this:

```
/home/epics/
└─> IOCs/ 
    └─> <ioc_name>/
        └─> Makefile
        └─> configure/
        └─> iocBoot/
        └─> <ioc_name>App/
```

## Change Configuration Files
Now we have to make some changes to several configuration files.

### SRC Makefile
Open `/<ioc_name>App/src/Makefile` and add all the required *.dbd files. This is mainly `asyn`, `streamdevice`, `drvAsynSerialPort.dbd` and `drvAsynIPPort.dbd`. 

It should look something like this. Check the lines for `<-- add this` to see where you need to change the file.

```
TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = <ioc_name>
# <ioc_name>.dbd will be created and installed
DBD += <ioc_name>.dbd

# <ioc_name>.dbd will be made up from these files:
<ioc_name>_DBD += base.dbd

# Include dbd files from all support applications:
#<ioc_name>_DBD += xxx.dbd
<ioc_name>_DBD += calc.dbd <-- add this !!!
<ioc_name>_DBD += drv<ioc_name>.dbd <-- add this !!!
<ioc_name>_DBD += stream.dbd <-- add this !!!
<ioc_name>_DBD += asyn.dbd <-- add this !!!
<ioc_name>_DBD += drvAsynSerialPort.dbd <-- add this !!!
<ioc_name>_DBD += drvAsynIPPort.dbd <-- add this !!!


# Add all the support libraries needed by this IOC
<ioc_name>_LIBS += calc <-- add this !!!
<ioc_name>_LIBS += stream <-- add this !!!
<ioc_name>_LIBS += asyn <-- add this !!!
# <ioc_name>_registerRecordDeviceDriver.cpp derives from <ioc_name>.dbd
<ioc_name>_SRCS += <ioc_name>_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
<ioc_name>_SRCS_DEFAULT += <ioc_name>Main.cpp
<ioc_name>_SRCS_vxWorks += -nil-

# Add support from b<ioc_name>e/src/vxWorks if needed
#<ioc_name>_OBJS_vxWorks += $(EPICS_B<ioc_name>E_BIN)/vxComLibrary

# Finally link to the EPICS B<ioc_name>e libraries
<ioc_name>_LIBS += $(EPICS_B<ioc_name>E_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
```
### SRC drv file
In the same `/src/` folder create a file called `drv<ioc_name>.dbd` and write the following into it:
```
include "stream.dbd"
include "asyn.dbd"
include "drvAsynSerialPort.dbd"
registrar(drvAsynIPPortRegisterCommands)
registrar(drvAsynSerialPortRegisterCommands)
```
This file can be named different, but then you must also change the name in the `/src/Makefile ` where we have the line `<ioc_name>_DBD += drv<ioc_name>.dbd`.

## Create Device Driver
Now we want to implement the actual device communication. For this we create two files: `<instrument>.db` and `<instrument>.proto` in `/<ioc_name>/<ioc_name>App/Db/`.

The `*.db` file is the database file that describes and defines the EPICS process variables (PVs) of the instrument. Each physical entity is described by one PV.
Each PV is described in the `*.db` file with a `record` object. Here you can see the content of a simple database file. 
```
record(ai, <instrument_name>:readTc)
{
        field (DESC, "Read Temperature in degrees Celsius")
        field (DTYP, "stream")
        field (INP, "@<instrument>.proto readTc $(PORT)")
        field (SCAN, "1 second")
        field (PINI, "1")
        field (MDEL, "0.5")
}
```
The actual device communication is defined in the `<instrument>.proto` file. The record reads from a webserver and parses the returned string to get the temperature in degrees Celsius.
Here is an exemplary `*.proto` file:
```
ReplyTimeout = 2000;
ReadTimeout = 100;
OutTerminator = "\r\n\r\n";

readTc
{
        extrainput = ignore;
        out "GET ";
        in "%*/Tc = /%f";
}
```
After adding the two files we must now change the `Makefile` in the same directory and add the two new files so that they are included in the IOC. For this simply add these two lines
```
DB += <instrument>.db
DB += <instrument>.proto
```
below the `#DB += xxx.db` line.

## Rebuild the IOC
To rebuild the IOC and implement all the changes we just made you must run following commands in the top `<ioc_name>/` folder:
```
make distclean
make
```

## Modify the Startup File
The `st.cmd` file in `IOCs/<ioc_name>/iocBoot/ioc<ioc_name>/` starts and runs the IOC. We now change the `st.cmd` file so that the IOC is configured correctly.
### Changing Permissions
If you can not execute the `st.cmd` file you must first change the permissions of the file.
```
chmod 777 st.cmd
```
This gives everybody all permissions! If this is not what you want, modify the `chmod` command as you wish.

### Change File Content
Open the `st.cmd` file and add the following line below the `< envPaths` line
```
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)/db")
```
Then add all asyn port configuration lines above the `## Load record instances` line. Here is an example for communication with a webserver which provides an html page:
```
# Asyn Port Configuration
drvAsynIPPortConfigure("LAP1",webserver.physik.uni-erlangen.de:80 HTTP")
```

Below the `## Load record instances` line you add all the `*.db` files you need. So for our simple example:
```
dbLoadRecords("db/<instument>.db", "PORT = LAP1")
```

Then you can run the startup file with
````
./st.cmd
````
and you should have a functional IOC.

To run your IOC in production we recommend to use procServ. [Here](procServ.md) you can find out how to setup procServ.



