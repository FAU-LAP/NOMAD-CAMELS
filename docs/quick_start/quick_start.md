---
layout: default
title: Quick Start
has_children: false
nav_order: 2
---

## Table of contents
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

# Quick Start Guide
This guide should help you get to know the main functionalities of NOMAD-CAMELS (short: CAMELS) after a successful [installation](https://fau-lap.github.io/NOMAD-CAMELS/docs/installation.html).



## 1. Installing and Configuring Instruments
### 1.1. Installing Instruments
When you first start up NOMAD-CAMELS, you should see something like the following:  
![Initial window on start up](img.png)
Clicking on the "Manage Instruments" button will open a dialog where you can install available instruments from the CAMELS repository (PyPi).\
For this tutorial we use the "demo_device".

<p float="left">
  <img src="img_1.png" width="49%" />
  <img src="img_3.png" width="49%" /> 
</p>

On the left we can see the instrument selection window. 
- Simply check the instruments you want to install. 
- Then click _Install / update Selected_ to install the most recent version of the instrument from PyPi via a simple `pip install <instrument_name>`

On the right you can see the screen after successful installation of the instruments. 

---

<img align="right" src="img_2.png" width="55%" alt="My Image">

You can also filter the instruments by their name using the _Search name_ field as you see here in the right image.

<br/><br/><br/><br/>

### 1.2. Configuring Instruments

After successful installation you can switch to the "Configure Instruments" tab.\
Here all the available instruments are listed as well as the number of instances (so 'actual' instruments) you have added of the installed instrument type.\
For this simply select the instrument type you want to add and click the &#10133; symbol under _Configure_.

<p float="left">
  <img src="img_4.png" width="49%" />
  <img src="img_5.png" width="49%" /> 
</p>

After adding the instrument a new instance of this instrument type is created. You can add as many instances of devices as you like by simply pushing the &#10133; symbol. This adds additional tabs with the _Custom name_ you gave the instrument. By default, the naming simply increments a number after the device name.

---

You can then change the instrument settings as you wish.\
You can also add a plain text description of the instrument and what you are planning to do with it. This is added to the metadata of your measurement when the instrument is used. This can help you better understand what the instrument does for larger project and allows others to better understand your measurement data.

<p float="left">
  <img src="img_6.png" width="49%" />
  <img src="img_7.png" width="49%" /> 
</p>

---

When you are happy with the instruments settings and have added all the instruments required for your measurements you can simply click _OK_ to save all the instruments and settings to CAMELS.

# Using Instruments
After adding at least one instrument to CAMELS you now have two ways to control the instrument: 
1. [_Measurement Protocols_](#2-measurement-protocols) Use it in sophisticated measurement procedures.
2. [_Manual Control_](#3-manual-control) Manual change individual 
![img_8.png](img_8.png)

## 2. Measurement Protocols
Measurement protocols are the main way in which CAMELS performs measurements. It can be understood as something similar to a _measurement recipe_ where a step for step guide is given to different instruments to perform a measurement procedure.

A good example of such a measurement procedure is a temperature dependant current-voltage (IV) measurement. Here the temperature of a sample is set to a specific value with a PID controller and waits for the temperature to be stable. Then it performs an IV-sweep, so it sets a voltage and measures the accompanying current for a given range of voltage values (often something like 100 points between -1 V and +1V).\
The temperature set-points are also varied to values in a given range (for example from 295K to 320K in 25 steps).\
So one would need to nest different loops (one for setting teh temperature and one for setting the voltage). This can be done quite simply using CAMELS.

### 2.1. Simple Start with _demo_device_
But let's start very simple with the _demo_device_ which is a pure software implementation of an instrument. 

Start by clicking the large &#10133; symbol next to _Measurement Protocols_. This opens up and empty protocol window.
![img_9.png](img_9.png)

Here you can fully configure the measurement routine you want to perform. Give the protocol a custom name using _Protocol Name_. With _Filename_ you set the name of data file that is created during the measurement. You can also add a custom description to describe what your measurement protocol does.

One key part of this window is the _Sequence_ element on the left.
Here you will configure the individual steps of the measurement procedure.

Simply right click into the empty space (left image below) or use the small &#10133; symbol in the top right to add a new step (right image below). 

<p float="left">
  <img src="img_10.png" width="48%" />
  <img src="img_11.png" width="50.3%" /> 
</p>

---

We can now add two of the most important steps:
- **Set Channels**
- **Read Channels**
 
![img_12.png](img_12.png)

Each device has specific _channels_ which can be read and set (changed) or only read.
Depending on the exact implementation of the instruments channels they are either 'software channels' so they themselves do not actually require device communication but store important values or settings, or they are 'instrument channels' and either _read from_ or _write to_ the instrument (or both). 

Below you can see the readable and the settable channels of a single _demo_device_. 

<p float="left">
  <img src="img_13.png" width="53%" />
  <img src="img_14.png" width="46%" /> 
</p>

### 2.2. Single Set and Read
Lets see how you can set and read individual cahnnels.
#### Set
We can now configure the protocol so that first each motor channel (`X`,`Y`,`Z`) are set to a value (in this case `1`,`2`,`3`).

<p float="left">
  <img src="img_15.png" width="49%" />
  <img src="img_16.png" width="49%" /> 
</p>

The green background of the `value` field tells you that CAMELS understands the entry as it expects to see a number (float) here. If you enter a value which CAMELS can not convert to float it will change the background to red (see image on the right).

&#9888; You can use variables instead of 'hard-coding' values.\
&#9888; You can use most symbolic math operations in the value field to perform calculations before setting the result of the calculation.\
For this simply add a variable on the bottom right of the protocol screen with the &#10133; symbol

<p float="left">
  <img src="img_17.png" width="49%" />
  <img src="img_18.png" width="49%" /> 
</p>

and change the `Name` and `Value` to what ever you need. The `Data-Type` will change depending on the value you input and can be used to make sure that CAMELS correctly 'understands' the value.

To use this variable in the protocol (here in `Set Channels`) simply right-click the value field and _insert_ or _append_ the desired variable you created.\
![img_19](img_19.png)

- _Insert_ will overwrite any existing value in the field 
- _Append_ will add the string name of the variable at the end of the value field. This is useful when creating longer functions with multiple variables.

You can use math notation as you would in a normal pythons script (you can use `np.*` variables; like `np.sin(1)`) to perform calculations before setting the value:\
![img_22.png](img_22.png)\
This should evaluate to `(1+1)*2=4`. You can also insert or append 
- functions
- operators 
- channel values

#### Read
To read the channels we just set, simply configure the `Read Channels` step to read the three motor channels:\
![img_23.png](img_23.png)\
You can now run the protocol by confirming the configuration with `OK` and then pressing the `run` button.\
![img_24.png](img_24.png)\
This should build the protocol (converts your recipe to a python script that uses [Bluesky](https://blueskyproject.io/) to orchestrate the measurement) and run it; resulting in information about the run in the log on the right side of the window.\
![img_25.png](img_25.png)\

This creates a HDF5 file in the location specified by the data saving location set in `Settings` and the user and sample name. This file contains all the read data and all the metadata known to CAMELS.\
![img_26.png](img_26.png)\
We can see that the `motorX` was set correctly to a value of 4.








### 2.3. Sweeping using a _For-loop_ step


## 3. Manual Control



<p style="text-align:left;">
  <span style="color: grey;">
  <a href="installation.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="users_guide.html">Next &rarr;</a><br>
  </span>
</p>