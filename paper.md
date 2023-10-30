---
title: 'NOMAD-CAMELS: Configurable Application for Measurements, Experiments and Laboratory Systems'
tags:
   - Python

authors:
   - name: Alexander D. Fuchs
     orcid: 0000-0003-1896-9242
     equal-contrib: true
     affiliation: "1, 2" # (Multiple affiliations must be quoted)
   - name: Johannes A. F. Lehmeyer
     orcid: 0000-0003-2041-9987
     equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
     affiliation: "1, 2"
   - name: Heiko B. Weber
     orcid: 0000-0002-6403-9022
     affiliation: 1
   - name: Michael Krieger
     orcid: 0000-0003-1480-9161
     corresponding: true # (This is how to denote the corresponding author)
     affiliation: 1

affiliations:
   - name: Lehrstuhl für Angewandte Physik, Friedrich-Alexander Universität Erlangen-Nürnberg, Germany
     index: 1
   - name: FAIRmat, Humboldt-Universität zu Berlin, Germany
     index: 2
date: 13 July 2023
bibliography: paper.bib

---

# Summary

NOMAD CAMELS is a configurable, open-source measurement software, that records fully self-describing experimental data. It has its origins in the field of experimental physics where a wide variety of measurement devices are used in rapidly changing experimental setups. CAMELS is designed with focus on full recording of data and metadata, allowing others to understand the data and the exact measurement procedure employed. CAMELS provides a user-friendly graphical user interface (GUI) which allows the user to define instrument control and measurement protocols. The GUI provides a low entry threshold enabling the creation of new measurement protocols without requiring programming knowledge or deep understanding of device communication. CAMELS generates python code to interface with instruments, allowing users to customize the code for specific applications and arbitrary device implementation if needed. Existing large-scale, distributed control systems using EPICS can be natively implemented. 
CAMELS allows researchers to take their first steps towards a FAIR-data pipeline and reproducible science.


# Statement of need
Research data management has peaked greater and greater interest in recent years with large research funding agencies emphasizing the importance of well-founded research data strategies in their treatment of proposals. The key goal is to create research data following the **FAIR** (**f**indable, **a**ccessible, **i**nteroperable and **r**e-usable) principles [@Wilkinson2016] and thereby improve world-wide research.
While electronic lab notebooks are an important step towards FAIR data it is equally important to start recording FAIR measurement data as early as possible in the research workflow. 

In experimental physics many custom-built measurement setups are controlled by a very specific software written by individual researchers. This results in a fully heterogeneous landscape of software solutions for measurements written in many different languages and with often poor documentation, making it almost impossible for other researchers to extend or alter it. The degree to which the saved raw data is understandable varies greatly but is often unintelligible even for researchers from same lab. The recording of metadata such as instrument settings or the actual measurement steps performed to obtain the final raw data are almost never recorded. Resulting in raw data that can only be understood by individual researchers or a very specific group of people, standing in the way towards FAIR research data. Although there are some tools available (e.g. _SweepMe!_ [@SweepMe], _iC_ [@pernstich2012]) to realise the control of different measurement instruments, they are usually not open-source or their data output is not compliant to the FAIR principles. 



# NOMAD CAMELS
CAMELS is completely open-source and collects all experimental metadata automatically for every measurement. By providing an easy to use graphical user interface, it allows creating and customizing measurements without programming knowledge. The default data output is a structured HDF5-file, staying as close to the NeXus format [@Konnecke2015] as possible, while still being agnostic to the exact measurement performed. The final HDF5-file contains the actual measurement data as well as the metadata in a single file, complying with the FAIR principles. 

Furthermore, CAMELS provides a direct connection to the online repository _NOMAD_ [@Draxl2019] or a local database installation called _NOMAD Oasis_ enabling the use of their electronic lab notebook (ELN) capabilities. The user can select sample-data from _NOMAD_ and link it with the measurement to then directly upload the measured data, providing a simple and stream-lined data workflow.

The orchestration of measurements is performed by _bluesky_ [@Allan2019; @bluesky], initially developed for the control of instruments at large-scale research institutions using EPICS [@Knott1994; @EPICS]. This allows CAMELS to natively/seamlessly integrate with any existing measurement infrastructure running EPICS.

CAMELS functionalities can be split into three main parts, the instrument management, measurement protocols and manual controls. 

## Instrument Management
Instruments can be added to NOMAD CAMELS in two ways. First, instruments for which drivers already exist can be added using the _instrument manager_, which gets the available ones from the curated/official driver repository [@CAMELS_drivers]. Drivers are then installed to the python environment via _pip_ [@PipDocumentationV23], with each driver being packaged individually.

Second, you can add drivers by creating the necessary files locally and placing them in the folder specified in the NOMAD CAMELS settings. To make this easier CAMELS offers a _driver builder_ that automatically generates the core structure and boilerplate code. This is the recommended approach for users creating their own drivers. As CAMELS is an open-source project by and for the community it is encouraged to share new drivers with others by creating pull requests on the driver repository.

In general, a driver for CAMELS is made up of two files: One containing the interface to the hardware, the other one defining the available instrument settings. Instruments consist of _channels_ that can be set and read and correspond to an individual functionality or physical property of the instrument.


## Measurement protocols
Coming from experimental physics the general concept of a _measurement protocol_ in CAMELS is a unique sequence of setting and measuring instruments. This results in a 'recipe-style' measurement where after the successful completion of one step the next step is then executed.   

CAMELS translates the protocol created in the GUI into a Python script and then executes it. This means that the script can also be modified and run without CAMELS and allows for 
complex modification of the measurement if necessary. Furthermore, the scripts can be exported and imported on different systems running CAMELS, enabling users to share entire measurement procedures with others.

The individual steps of the protocol are predefined building blocks with various functions such as writing commands to the instruments, reading from instruments or even creating sophisticated parametrized measurement scans. But individual instrument drivers can even add customized steps like a PID-controller adding the functionality of waiting for the desired value to be stable.

## Manual Controls
Some devices need to be controlled manually before complex measurement routines can be started, such as moving stages or setting specific temperatures. _Manual controls_ allow you to control individual instruments without having to create an entire protocol first.
Every instrument can provide its own manual controls.
## Data output
After execution of the measurement protocol the obtained data is saved into an HDF5-file that is structured closely to the NeXus format [@Konnecke2015]. Data can also be exported as CSV, while the metadata can be exported as JSON, allowing for existing workflows to be still used. 

The raw data that should be collected is defined by the user, mainly with protocol steps like "Read_Channels". Additionally to that, NOMAD CAMELS collects the available metadata.
A big part of the metadata is all instrument settings of the instruments used. Further, information about user and investigated sample are added if provided.

It should be emphasized that the data file contains the complete python script that was used to create this data file. Additionally, the information about the python environment in which it was run is saved as well. This hugely simplifies reproducibility, since the measurement can be run the same way again, years later. 


# Acknowledgements

FAIRmat is funded by the the Deutsche Forschungsgemeinschaft ”DFG, German Re- search Foundation” – project 460197019.

# References