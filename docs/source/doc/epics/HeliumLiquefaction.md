# Helium Liquefaction Documentation

This Documentation shall explain how certain Device Drivers for the EPICS IOC for the Helium Liquefaction works.
It shall also serve as an example on how to set up records for interacting with Serial or Ethernet devices.
Therefor, for the sake of completeness, all other steps needed to setup the IOC are also included.
This IOC requires:

1. EPICS Base (version 7.x)
2. Support module [Asyn](https://github.com/epics-modules/asyn) to handle device connections
3. Support module [StreamDevice](https://paulscherrerinstitute.github.io/StreamDevice/) to handle device communication

For the rest of the documentation, the IOC will be named `HeliumLiquefaction`. For a differently named
IOC, `HeliumLiquefaction` will be needed to be replaced by the chosen name for the IOC.

# Table of Content

<!-- TOC -->
- [Helium Liquefaction Documentation](#helium-liquefaction-documentation)
- [Table of Content](#table-of-content)
- [Overview](#overview)
- [Section 1: Filllevel Calculation](#section-1-filllevel-calculation)
  - [Chapter 1: Creating the FillLevel.db and FillLevel.proto](#chapter-1-creating-the-fillleveldb-and-filllevelproto)
    - [Step 1: Reading the sensors](#step-1-reading-the-sensors)
          - [FillLevel.proto](#filllevelproto)
          - [FillLevel.db](#fillleveldb)
    - [Step 2: Fill level calculation](#step-2-fill-level-calculation)
    - [Step 3: Interpolation](#step-3-interpolation)
    - [Step 4: Entire FillLevel.db](#step-4-entire-fillleveldb)
    - [Step 5: Makefile changes](#step-5-makefile-changes)
  - [Chapter 2: Import of the Breakpoint Tables](#chapter-2-import-of-the-breakpoint-tables)
- [Section 2: Liquefier Data](#section-2-liquefier-data)
- [Section 3: Setting up st.cmd for a correct boot of the IOC](#section-3-setting-up-stcmd-for-a-correct-boot-of-the-ioc)
        - [Tips for an easier time working with IOCs](#tips-for-an-easier-time-working-with-iocs)
<!-- TOC -->

# Overview

Each different device has his own .db file and for device communication a .proto file with the same name.
In this documentation, the focus will lie on the two more complicated records:
<ul>
    <li>Calculation of the fill level of the Helium tank in Liters via Interpolation</li>
    <li>Handling unsolicitated Data from the Liquefier</li>
</ul>
The other records mostly using the same logic as the fill level one, in the sense of also being "talked to" via Serial Connection.

It is assumed a newly created, empty IOC is already set up with.



# Section 1: Filllevel Calculation

## Chapter 1: Creating the FillLevel.db and FillLevel.proto

First, a short explanation of how the fill level calculation works: Two sensors, being vertically offset and sensor 2 being the one closer to the bottom, cover the
entire tank and measure their percentage of being submerged in liquid helium, giving back a value of 100% if they are fully
submerged.
The height in millimeters is then calculated depending of the submersion:

If Sensor 2 reads 100%  *or* Sensor 1 reads 5% and Sensor 2 95%, then fill level
is `790 + 785 * <Sensor 1 value>`, else fill level is `785 * <Sensor 2 value>`.
Calculation of fill level in liters is then done via Interpolation.

The fill level record therefor needs to do the following:

1. Read both sensors
2. Calculate the fill level in millimeters
3. Interpolate

### Step 1: Reading the sensors

The first step is to understand the device protocoll, i.e. how to talk to it and how responses are formatted. Check the
device manual for instructions. Also, with programms like CuteCom ([their GitHub](https://github.com/oudream/cutecom))
communications can be tested with a graphical interface.

In this case, the device has only the two sensors connected and responds to the request (`R1 CR`) (asking for the sensor
1 value) with `R+<value> CR`.

 *`CR` stands for [carriage return](https://en.wikipedia.org/wiki/Carriage_return) and is in various combinations with `LF` ([line feed](https://en.wikipedia.org/wiki/Newline)) the way almost all serial devices mark the end of a message.*

If the sensor reads 5%, the return will look thusly: `R+00050 CR`.


###### FillLevel.proto
The `FillLevel.proto`, belonging inside the folder `HeliumLiquefaction/HeliumLiquefactionApp/Db`, for the fill level should look like this:

```
ReplyTimeout = 2000;
ReadTimeout = 100;
OutTerminator = CR;
InTerminator = CR;

sensor1
{
        out "R1";
        in "R+%d";
}
sensor2
{
        out "R2";
        in "R+%d";
}
```

An explanation for the 4 lines at the top can be
found [in the StreamDevice documentation](https://paulscherrerinstitute.github.io/StreamDevice/protocol.html#sysvar), they manage settings for device
communications.
`sensor1 {}` and `sensor2 {}` handle the device communication itself.

`out "R1"` sends (therefor `out`) a command `R1 CR` to the device. `CR` is appended by StreamDevice due to being set as
the `OutTerminator`. With `in "R+%d"` the input is processed. `R+` matches the `R+` at the start of the device reply, `%d` is then
set to the value sent, in the example return with 5% sensor reading it will be `50`. Thats the value (here an integer) returned to the
record in the `.db` file.

It is important to use `%d`, so an integer or `LONG` value here, not a `DOUBLE` value via `%f`. Otherwise, a needed value conversion explained in the following paragraph can not be done. The reason will be explained later [in the Chapter Interpolation](#step-3-interpolation). 

###### FillLevel.db
The two records for the sensors in the `FillLevel.db`, same folder as `FillLevel.proto` should look like this:

*For conciseness, only one record is written here, since they only differ by `sensor1` instead being `sensor2`.*
```
record(ai, FillLevel:sensor1)
{
        field (DESC, "Read Resistance of Sensor 1")
        field (DTYP, "stream")
        field (INP, "@FillLevel.proto sensor1 $(PORT)")
        field (SCAN, "Passive")
        field (LINR, "LINEAR")
        field (ASLO, 0.001)
        field (EGU, "%")
}
```
A very thorough explanation of the basics of the different fields and their possible values are found in the official [EPICS Documentation](https://epics.anl.gov/base/R7-0/6-docs/RecordReference.html).

In the context of this IOC, only why certain values are chosen will be explained:
* `DTYP` is set to `stream`, since StreamDevice is used for device communication.
* `INP` is used by the device support module, i.e. StreamDevice, to obtain the value. `@FillLevel.proto` specifies the file, `sensor1` the function inside the file.
* `SCAN` is set to `Passive`, since the later explained `calc-Record` will call these records and process them. *Be aware that the option `"Passive"` is case sensitive*.
* `ASLO` is needed, since the value returned by the device is off by a factor of 1000. A value of 5%, i.e. `0,05` is returned as `00050` from the device, so this record would be set to `50`.
* `LINR` hast to be set, otherwise `ASLO` is ignored. *Again, `"LINEAR"` is case sensitive*.
* `EGU` is set to `"%"` since `%` is the unit of the value.

With this, the sensor reading is complete.

### Step 2: Fill level calculation
To calculate the fill level, a `calcout` record is used. This record uses up to 12 inputs and writes the result of the calculation in another record.
The record should look like this:
```
record(calcout, FillLevel:heightcalc)
{
        field (DESC, "Calculates Filllevel")
        field (SCAN, "1 second")
        field (PINI, 1)
        field (CALC, "(((B)>=(1) || ((A)>=(0.05) && (B)>=(0.95)))?((785 * A) + 790):(785 * B))")
        field (INPA, "FillLevel:sensor1 PP")
        field (INPB, "FillLevel:sensor2 PP")
        field (OOPT, 1)
        field (OUT, "FillLevel:filllevelMM.VAL")
        field (DOPT, 0)
        field (LOPR, 0.0)
        field (HOPR, 1487.0)
        field (FLNK, "FillLevel:scaling")
}
```
* `SCAN` is set to `1 second`*(case sensitive)* to make the calculation every second. The other standard scan options (and how to create other time intervals) are listed in the [EPICS documentation](https://epics.anl.gov/base/R7-0/6-docs/menuScan.html).
* `PINI` should almost always be set to `1` if `SCAN` is set to a time period. This forces the record to be processed on IOC startup. Otherwise, the record is first processed after the time set in `SCAN`. While this doesn't matter too much for this short period, depending on the record this might be a long time.
* `INPA` and `INPB` tells this record where to get its values from, here from the records `FillLevel:sensor1` and `2`. With the option `PP`, these records are processed first before getting their values, to get present values and not old ones.
* `CALC` is the formula to calculate the fill level. `A` and `B` are replaced with the values from `INPA` and `INPB` respectively. Since the actual calculation depends on the sensor readings, firstly an if/else condition is set and then the correct calculation is made. 
  * The calculation logic is already [at the beginning of the chapter](#chapter-1-creating-the-fillleveldb-and-filllevelproto). The implementation with logical operators is explained in the [EPICS documentation](https://epics.anl.gov/base/R7-0/6-docs/calcoutRecord.html) for the `calcout` record, but should look familiar to anyone already knowledgeable with programming.
  * after the `?`, the different calculations are listed. If the if-condition is met, `(785 * A) + 790)` is used, otherwise the formula after the `:`, `(785 * B)` is used instead.
* `OUT` specifies the record that is written to, here to the field `VAL` of the record `FillLevel:filllevelMM`.
* `FLNK` calls the record `FillLevel:scaling` (explained later) to be processed after this one is finished with all calculations.

The record `FillLevel:filllevelMM` is more or less a dummy record, which only serves the purpose of saving the fill level in a concise way.
```
record(ai, FillLevel:filllevelMM)
{
        field (DESC, "Filllevel of the Heliumtank in mm")
        field (DTYP, "Soft Channel")
        field (SCAN, "Passive")
        field (EGU, "mm")
}
```
* `DTYP` is set to `Soft Channel`, a default device type.

Now, the record `FillLevel:filllevelMM` contains the current level of the helium tank in millimeters.

### Step 3: Interpolation
Theoretically, a single record would be all that is needed for the interpolation. It would read the value of the `FillLevel:filllevelMM` and interpolate with a breakpoint table.
However, non-linear interpolations with these values here are a bit tricky in EPICS and need a bit of a workaround.
Interpolation is a type of Linearization (used in the `FillLevel:sensor1` record to divide the value by 1000), that uses the RVAL field of a record.
The problem here is that the RVAL field can only be a `LONG` value, i.e. integers.
However, the way the fill level is calculated produces a `DOUBLE` value.
So here, both the `FillLevel:heightcalc` and `FillLevel:filllevelMM` records will have an `RVAL` value of `0`, and a `ai` record that uses their values as `INP` would also only save it in their `VAL` field
Any sort of Linearization will therefor return a value of `0`. Forcing the fill level to be an integer would lose all decimal digits, which in this application would mean during normal fill levels, only changes of more than 3 liters would be able to be detected.

To circument this, an Analog Output record (`ao`) is used that:
1. gets the value of `FillLevel:filllevelMM`.
2. multiplies it by a factor of 10<sup>n</sup>, `n` depending of the needed accuracy.
3. writes the new value to the `RVAL` field of an Analog Input record (`ai`), which then interpolates.

In this example, `n=3` is enough, shifting the comma of the float value by 3, since the fill level in mm can never have more than 3 decimal digits. 

*The lowest value of the sensors is 0,1%, i.e. 0,001. 785 \* 0,001 = 0,785, i.e. 3 decimal digits.*

The `ao` record should therefor look like this:
```
record(ao, FillLevel:scaling)
{
        field (DTYP, "Raw Soft Channel")
        field (OMSL, "closed_loop")
        field (SCAN, "Passive")
        field (OIF, "Full")
        field (DOL, "FillLevel:filllevelMM.VAL PP")
        field (OUT, "FillLevel:filllevelL.RVAL PP")
        field (LINR, "LINEAR")
        field (ASLO, 0.001)
}
```
* `DTYP` needs to be `Raw Soft Channel`, since the `RVAL` value is needed to be written to `OUT`.
* `OMSL` set to `closed_loop` enables the input field `DOL`.
* `OIF` is set to `Full` because otherwise the `VAL` field is always incremented.
* `DOL` is where the value is taken from, so comparable the `INP` field for `out` records.
* `OUT` is where is written to. Its important to write to the `RVAL` field to enable interpolation in the target record. The `PP` flag is set to process the receiving record.
* `LINR` needs to be set so `ASLO` is used.
* `ASLO` is set to 10<sup>-n</sup>. This is because the way this record works is by reading the field specified by the `DOL` field and saving that value in its `VAL` field. Then, due to being a `Raw Soft Channel`, calculates the outgoing `RVAL`. Since `VAL = RVAL * ASLO`, `RVAL = VAL / ASLO`.

The receiving record then should look like this:
```
record(ai, FillLevel:filllevelL)
{
        field (DESC, "Filllevel of the Heliumtank in L")
        field (DTYP, "Raw Soft Channel")
        field (SCAN, "Passive")
        field (LINR, "filllevel")
        field (EGU, "l")
}
```
* `LINR` set to `filllevel` tells the record to use the breakpoint table `filllevel`
* `DTYP` needs to be `Raw Soft Channel` again to use `RVAL`.

### Step 4: Entire FillLevel.db
The completed file should then look like this:
```
record(ai, FillLevel:sensor1)
{
        field (DESC, "Read Resistance of Sensor 1")
        field (DTYP, "stream")
        field (INP, "@FillLevel.proto sensor1 $(PORT)")
        field (SCAN, "Passive")
        field (LINR, "LINEAR")
        field (ASLO, 0.001)
        field (EGU, "%")
}
record(ai, FillLevel:sensor2)
{
        field (DESC, "Read Resistance of Sensor 2")
        field (DTYP, "stream")
        field (INP, "@FillLevel.proto sensor2 $(PORT)")
        field (SCAN, "Passive")
        field (LINR, "LINEAR")
        field (ASLO, 0.001)
        field (EGU, "%")
}

record(calcout, FillLevel:heightcalc)
{
        field (DESC, "Calculates Filllevel")
        field (SCAN, "1 second")
        field (PINI, 1)
        field (CALC, "(((B)>=(1)||((A)>=(0.05) && (B)>=(0.95)))?((785 * A) + 790):(785 * B))")
        field (INPA, "FillLevel:sensor1 PP")
        field (INPB, "FillLevel:sensor2 PP")
        field (OOPT, 1)
        field (OUT, "FillLevel:filllevelMM.VAL")
        field (DOPT, 0)
        field (LOPR, 0.0)
        field (HOPR, 1487.0)
        field (FLNK, "FillLevel:scaling")
}
record(ai, FillLevel:filllevelMM)
{
        field (DESC, "Filllevel of the Heliumtank in mm")
        field (DTYP, "Soft Channel")
        field (SCAN, "Passive")
        field (EGU, "mm")
}
record(ao, FillLevel:scaling)
{
        field (DTYP, "Raw Soft Channel")
        field (OMSL, "closed_loop")
        field (SCAN, "Passive")
        field (OIF, "Full")
        field (DOL, "FillLevel:filllevelMM.VAL PP")
        field (OUT, "FillLevel:filllevelL.RVAL PP")
        field (LINR, "LINEAR")
        field (ASLO, 0.001)
}
record(ai, FillLevel:filllevelL)
{
        field (DESC, "Filllevel of the Heliumtank in L")
        field (DTYP, "Raw Soft Channel")
        field (SCAN, "Passive")
        field (LINR, "filllevel")
        field (EGU, "l")
}
```

### Step 5: Makefile changes
The `Makefile` in this folder needs to be changed to include the newly created files, so add 
```
DB += FillLevel.db
DB += FillLevel.proto
```
underneath the lines 
```
# Create and install (or just install) into <top>/db
# databases, templates, substitutions like this
#DB += xxx.db
```

## Chapter 2: Import of the Breakpoint Tables
To make the breakpoint table used in the previously described record available, navigate to `HeliumLiquefaction/HeliumLiquefactionApp/src`.
Firstly, the basic steps needed to import `StreamDevice` and `asyn`:
Create a `drvHeliumLiquefaction.dbd` with the content
```
include "stream.dbd"
include "asyn.dbd"
include "drvAsynSerialPort.dbd"
registrar(drvAsynIPPortRegisterCommands)
registrar(drvAsynSerialPortRegisterCommands)
```

To make a breakpoint table available, two files need to be created. A breakpoint table and a file that makes the table
available as a breakpoint table to records.

For a breakpoint table, create a file named `<name>.dbd`, in this case called `filllevel.dbd`. The file should look like
this (shortened here for readability):
```
breaktable(filllevel) {
        0.0     0.0
        10000.0  1.0
        20000.0  3.0
        30000.0  6.0
...
...
        1470000.0        4231.0
        1480000.0        4237.0
        1487000.0        4239.8
}
```
This table represents fill levels in mm on the left and their respective values in liters on the right.
Please be aware that the values on the left need to be adjusted due to the steps taken during [Step 3: Interpolation](#step-3-interpolation).
Actually, `10 mm` are equivalent to `1 l`, `20 mm` to `3 l` etc.
However, the `mm` value  used for interpolation is multiplied by 10<sup>3</sup>. Therefor, all values representing mm in this breakpoint table also need to be multiplied by 10<sup>3</sup>.



Next, to make this breakpoint table available, copy `menuConvert.dbd` from the Epics installation folder `\EPICS\base-7.0\dbd` to here.
This table contains a list of all available breakpoint tables and their internal names. This is already filled with breakpoint tables for temperature interpolation.
The newly created table needs to be appended to the end of the list, so the entire file should look like this:
```
#*************************************************************************
# Copyright (c) 2013 UChicago Argonne LLC, as Operator of Argonne
#     National Laboratory.
# Copyright (c) 2002 The Regents of the University of California, as
#     Operator of Los Alamos National Laboratory.
# EPICS BASE is distributed subject to a Software License Agreement found
# in file LICENSE that is included with this distribution.
#*************************************************************************


menu(menuConvert) {
        choice(menuConvertNO_CONVERSION,"NO CONVERSION")
        choice(menuConvertSLOPE,"SLOPE")
        choice(menuConvertLINEAR,"LINEAR")
        choice(menuConverttypeKdegF,"typeKdegF")
        choice(menuConverttypeKdegC,"typeKdegC")
        choice(menuConverttypeJdegF,"typeJdegF")
        choice(menuConverttypeJdegC,"typeJdegC")
        choice(menuConverttypeEdegF,"typeEdegF(ixe only)")
        choice(menuConverttypeEdegC,"typeEdegC(ixe only)")
        choice(menuConverttypeTdegF,"typeTdegF")
        choice(menuConverttypeTdegC,"typeTdegC")
        choice(menuConverttypeRdegF,"typeRdegF")
        choice(menuConverttypeRdegC,"typeRdegC")
        choice(menuConverttypeSdegF,"typeSdegF")
        choice(menuConverttypeSdegC,"typeSdegC")
        choice(menuConverttypefilllevel,"filllevel")
}
```


Lastly, the `Makefile` needs to be changed.
As usual, the support applications and libraries needs to be added, and the `filllevel.dbd` as well. The `Makefile should`look like this:
```
TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = HeliumLiquefaction
# HeliumLiquefaction.dbd will be created and installed
DBD += HeliumLiquefaction.dbd

# HeliumLiquefaction.dbd will be made up from these files:
HeliumLiquefaction_DBD += base.dbd

# Include dbd files from all support applications:
#HeliumLiquefaction_DBD += xxx.dbd
HeliumLiquefaction_DBD += calc.dbd
HeliumLiquefaction_DBD += drvHeliumLiquefaction.dbd
HeliumLiquefaction_DBD += stream.dbd
HeliumLiquefaction_DBD += asyn.dbd
HeliumLiquefaction_DBD += drvAsynSerialPort.dbd
HeliumLiquefaction_DBD += drvAsynIPPort.dbd
DBD += filllevel.dbd

# Add all the support libraries needed by this IOC
#HeliumLiquefaction_LIBS += xxx
HeliumLiquefaction_LIBS += calc
HeliumLiquefaction_LIBS += stream
HeliumLiquefaction_LIBS += asyn

# HeliumLiquefaction_registerRecordDeviceDriver.cpp derives from HeliumLiquefaction.dbd
HeliumLiquefaction_SRCS += HeliumLiquefaction_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
HeliumLiquefaction_SRCS_DEFAULT += HeliumLiquefactionMain.cpp
HeliumLiquefaction_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#HeliumLiquefaction_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
HeliumLiquefaction_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
```

# Section 2: Liquefier Data

The main particularity of the Liquefier is that it doesnt wait to a value request and responds with the requested value, instead it periodically broadcasts all values.
These values consist of binary values `0` and `1` representing `Off` and `On` and analog values, for example Turbine Speed. Due to the values all being separated by long and different strings, records like `aai` or `waveform` are not advisable

Instead of showing the entire 160 line `Liquefier.db`, which mostly is the same for all records, two example records are instead listed and explained.


For binary values, lets consider 
```
record(bi, Liquefier:CompressorStatus)
{
        field (DTYP, "stream")
        field (INP, "@Liquefier.proto CompressorStatus $(PORT)")
        field (SCAN, "I/O Intr")
        field (ZNAM, "Off")
        field (ONAM, "On")

}
```
* `SCAN` is set to `"I/O Intr"` *(as always case sensitive)*. Record processing is now triggered whenever the device sends an input.
* `ZNAM` and `ONAM` represents the Zero Name, i.e. input is `0`, and every other value. Since a `0` means `Off` and otherwise its `On`, it is set here.

For analog values
```
record(ai, Liquefier:T1Speed)
{
        field (DTYP, "stream")
        field (INP, "@Liquefier.proto T1Speed $(PORT)")
        field (SCAN, "I/O Intr")
        field (EGU, "U/min")
}
```
* `EGU` is only allowed in analog records, since binary options oviously dont have an Engineering Unit. It is set for each value according to the value send by the Liquefier.

For the `Liquefier.proto`, again only the first function is explained, since they are all the same
```
ReadTimeout = 10000;
InTerminator = CR LF;
extrainput=ignore;


CompressorStatus
{
        in "%*/KOMPRESSOR STATUS   :/%i";
        in "%*/VAKUUM SYSTEM STATUS:/%*i";
        in "%*/LN2 SYSTEM STATUS   :/%*i";
        in "%*/ABKUHLEN            :/%*i";
        in "%*/IN BETRIEB          :/%*i";
        in "%*/REINIGER STATUS     :/%*i";
        in "%*/REINIGER ABKUHLEN   :/%*i";
        in "%*/REINIGER IN BETRIEB :/%*i";
        in "%*/REINIGER REGENER.   :/%*i";
        in "%*/FTX100 T1 DREHZAHL  :/%*f";
        in "%*/FTX101 T2 DREHZAHL  :/%*f";
        in "%*/TTX106 TURB.AUSG.TMP:/%*f";
        in "%*/TTX111 JT EING.TEMP :/%*f";
        in "%*/PTX102 T1 EING.DRUCK:/%*f";
        in "%*/PTX203 PUFFERDRUCK  :/%*f";
        in "%*/TTX104 REINIG.BETR. :/%*f";
        in "%*/TTX102 REINIG.REGEN.:/%*f";
        in "%*/TTX108 LN2 BETRIEBS :/%*f";
        in "%*/VPI103 CV103 V.POSN :/%*f";
        in "%*/VPI111 CV111 V.POSN :/%*f";
}
```
* `ReadTimout` is set rather high with 10 seconds, this is because the Liquefier sometimes takes very long to send the messages.
* `extrainput = ignore` so extra bytes arent considered errors
* `in "%*/KOMPRESSOR STATUS   :/%i";` takes in a line and looks for the string inside `/ /`, so here `KOMPRESSOR STATUS   :`. Due to `%*` in front of it, that part is ignored. The value after this is saved as an integer via `%i`
* in the next line, its the same with the value being matched, but it is ignored instead of saved. It is crucial for `StreamDevice` protocols where multiple values need to be saved from messages that every record "sees" every input but only matches the one actually needed for the record. Otherwise, record processing will not work correctly. It might seem as though values of records are updated, however monitoring of these records will fail.


# Section 3: Setting up st.cmd for a correct boot of the IOC
Now navigate to `/HeliumLiquefaction/iocBoot/iocHeliumLiquefaction`. There, edit the st.cmd to look like this:

*Note: for completeness sake, the entire `st.cmd` is included, which therefor contains files not explained here but necessary for the complete Helium Liquefaction driver. They are however commented out, so they should not cause problems*
```
#!../../bin/linux-x86_64/HeliumLiquefaction

#- You may have to change HeliumLiquefaction to something else
#- everywhere it appears in this file

< envPaths
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)/db")
epicsEnvSet "LIQUEFIERPORT" "$(TTY=/dev/tty<X>)"
epicsEnvSet "AGILENT34970APORT" "$(TTY=/dev/tty<X>)"
epicsEnvSet "OXFORDPORT" "$(TTY=/dev/tty<X>)"
epicsEnvSet "WIKA01PORT" "$(TTY=/dev/tty<X>)"
epicsEnvSet "WIKA02PORT" "$(TTY=/dev/tty<X>)"

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/HeliumLiquefaction.dbd"
HeliumLiquefaction_registerRecordDeviceDriver pdbbase

## Purity Sensor (MAC-Adress -> A8:61:0A:AE:F3:A6, IP-Adress -> 10.131.162.100)
#drvAsynIPPortConfigure("PURITY","lapheliumpurity1.physik.uni-erlangen.de:80 HTTP")
## Debug, show Asyn-Messages
#asynSetTraceMask("PURITY",-1,0x9)
#asynSetTraceIOMask("PURITY",-1,0x2)

## Liquefier
drvAsynSerialPortConfigure("LIQUEFIER","$(LIQUEFIERPORT)")
asynSetOption("LIQUEFIER", 1, "baud", "9600")
asynSetOption("LIQUEFIER", 1, "parity", "even")
asynSetOption("LIQUEFIER", 1, "bits", "7")
asynSetOption("LIQUEFIER", 1, "stop", "1")
## Debug, show Asyn-Messages
#asynSetTraceMask("LIQUEFIER",-1,0x9)
#asynSetTraceIOMask("LIQUEFIER",-1,0x2)

## Cooling Water
#drvAsynSerialPortConfigure("AGILENT34970A","$(AGILENT34970APORT)")
#asynSetOption("AGILENT34970A", 1, "baud", "9600")
#asynSetOption("AGILENT34970A", 1, "parity", "none")
#asynSetOption("AGILENT34970A", 1, "bits", "8")
#asynSetOption("AGILENT34970A", 1, "stop", "1")
## Debug, show Asyn-Messages
#asynSetTraceMask("AGILENT34970A",-1,0x9)
#asynSetTraceIOMask("AGILENT34970A",-1,0x2)

## Fill Level
drvAsynSerialPortConfigure("OXFORD","$(OXFORDPORT)")
asynSetOption("OXFORD", 1, "baud", "9600")
asynSetOption("OXFORD", 1, "parity", "none")
asynSetOption("OXFORD", 1, "bits", "8")
asynSetOption("OXFORD", 1, "stop", "2")
## Debug, show Asyn-Messages
#asynSetTraceMask("OXFORD",-1,0x9)
#asynSetTraceIOMask("OXFORD",-1,0x2)

## Dewar Pressure
#drvAsynSerialPortConfigure("WIKA01","$(WIKA01PORT)")
#asynSetOption("WIKA01", 1, "baud", "9600")
#asynSetOption("WIKA01", 1, "parity", "none")
#asynSetOption("WIKA01", 1, "bits", "8")
#asynSetOption("WIKA01", 1, "stop", "2")
## Debug, show Asyn-Messages
#asynSetTraceMask("WIKA01",-1,0x9)
#asynSetTraceIOMask("WIKA01",-1,0x2)

## Buffer Pressure
#drvAsynSerialPortConfigure("WIKA02","$(WIKA02PORT)")
#asynSetOption("WIKA02", 1, "baud", "9600")
#asynSetOption("WIKA02", 1, "parity", "none")
#asynSetOption("WIKA02", 1, "bits", "8")
#asynSetOption("WIKA02", 1, "stop", "2")
## Debug, show Asyn-Messages
#asynSetTraceMask("WIKA02",-1,0x9)
#asynSetTraceIOMask("WIKA02",-1,0x2)


## Load record instances
##dbLoadRecords("db/HeliumLiquefaction.db","user=epics")
#dbLoadRecords("db/Purity.db", "PORT=PURITY")
dbLoadRecords("db/Liquefier.db", "PORT=LIQUEFIER, TTY=$(LIQUEFIERPORT)")
#dbLoadRecords("db/CoolingWater.db", "PORT=AGILENT34970A, TTY=$(AGILENT34970APORT)")
dbLoadRecords("db/FillLevel.db", "PORT=OXFORD, TTY=$(OXFORDPORT)")
#dbLoadRecords("db/DewarPressure.db", "PORT=WIKA01, TTY=$(WIKA01PORT)")
#dbLoadRecords("db/BufferPressure.db", "PORT=WIKA02, TTY=$(WIKA02PORT)")

# Load FillLevel Conversion Table and set it to not be monotonic
var dbBptNotMonotonic 1
dbLoadRecords("dbd/filllevel.dbd")

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=epics"
```
* the lines after `<env Paths` are:
  * `epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)/db")` is always necessary.
  * `epicsEnvSet "LIQUEFIERPORT" "$(TTY=/dev/tty<X>)"` sets a variable `LIQUEFIERPORT` to `$(TTY=/dev/tty<X>)`. `TTY` means serial connection, `<X>` needs to be replaced with whatever serial port the device is plugged into. To find them, run `sudo dmesg | grep tty`, which should list all possible connections. After that, it might be a bit of trial and error to find the correct one, so probably use a tool like CuteCom to quickly find the correct port.
* `## Liquefier` is commented out to mark the beginning of settings regarding the Liquefier.
  * `drvAsynSerialPortConfigure("LIQUEFIER","$(LIQUEFIERPORT)")` makes `asyn` open a connection with the device under the address defined in `<envPath` and assigns that connection to the variable `LIQUEFIER`.
  * `asynSetOption` sets the options for the listed connection. These options are device specific and should be available in the manual.
  * `asynSetTraceMask` and `asynSetTraceIOMask` are debug options, that show every incoming and outcoming message on that port. As most debug options, they should stay commented out during normal operations.
* `## Load record instances` lists all loads the `.db` files via `dbLoadRecords()`.
  * `"db/FillLevel.db,"` names the `.db` actually being loaded.
  * `"PORT=LIQUEFIER"` makes a variable named `PORT` available to the records of that `.db`, with the value of `LIQUEFIER`, which itself is replaced with the serial connection from `drvAsynSerialPortConfigure`
  * Other variables can also be passed off to the records here, with the same syntax.
  * All these variables are referenced in the record via `$(<name>)`, so for example `$(PORT)`.
* `# Load FillLevel Conversion Table and set it to not be monotonic` does what it says
  * `var dbBptNotMonotonic 1` sets the breakpointtable below to be not monotonic.
  * `dbLoadRecords("dbd/filllevel.dbd")` loads the filllevel.dbd breakpoint table.


##### Tips for an easier time working with IOCs
Especially during working on a new `.db` and `.proto`, its often necessary to rebuild the IOC and restart it. To make that a bit faster, consider making an `mk.cmd` where the `st.cmd` is located with the following content:
```
#!/bin/bash
cd ../../
sudo make distclean
sudo make

cd iocBoot/iocHeliumLiquefaction
sudo ./st.cmd
```
this just paths to the main IOC folder, rebuilds it, navigates back to the `st.cmd` and starts it