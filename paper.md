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

In experimental physics many custom-built measurement setups are controlled by a very specific software written by individual researchers. This results in a fully heterogeneous landscape of software solutions for measurements written in many different languages and with often poor documentation, making it almost impossible for other researchers to extend or alter it. The degree to which the saved raw data is understandable varies greatly but is often unintelligible even for researchers from same lab. The recording of metadata such as instrument settings or the actual measurement steps performed to obtain the final raw data are almost never recorded. Resulting in raw data that can only be understood by individual researchers or a very specific group of people, standing in the way towards FAIR research data. Although there are some tools available (e.g. "SweepMe!" [@SweepMe], iC [@pernstich2012]) to realise the control of different measurement instruments, they are usually not open-source or their data output is not compliant to the FAIR principles. 



# NOMAD CAMELS
CAMELS is completely open-source and collects all experimental metadata automatically for every measurement. By providing an easy to use graphical user interface, it allows creating and customizing measurements without programming knowledge. The default data output is a structured HDF5-file, staying as close to the NeXus format [@Konnecke2015] as possible, while still being agnostic to the exact measurement performed. The final HDF5-file contains the actual measurement data as well as the metadata in a single file, complying with the FAIR principles. 

Furthermore, CAMELS provides a direct connection to the online repository _NOMAD_ [@Draxl2019] or a local database installation called _NOMAD Oasis_ enabling the use of their electronic lab notebook (ELN) capabilities. The user can select sample-data from _NOMAD_ and link it with the measurement to then directly upload the measured data, providing a simple and stream-lined data workflow.

The orchestration of measurements is performed by _bluesky_ [@Allan2019; @bluesky], initially developed for the control of instruments at large-scale research institutions using EPICS [@Knott1994; @EPICS]. This allows CAMELS to natively/seamlessly integrate with any existing measurement infrastructure running EPICS.

CAMELS functionalities can be split into three main parts, the instrument management, measurement protocols and manual controls. 

## Instrument Management
Instruments in NOMAD CAMELS can be added in two ways. The simple way is to add them via the instrument management in the software, which checks a curated list on our driver-repo [@CAMELS_drivers]. The drivers are installed to the python environment via pip, with each driver being represented by its own package.

The other way to add drivers is by placing them into the folder specified under NOMAD CAMELS' settings. This is the way to go for users who want to write their own drivers. Although it is possible to share them with the community by contributing to the drivers repo or uploading them to PyPI, sometimes it might be not possible to users, because of copyright reasons.

In general, a driver for NOMAD CAMELS is made up of two files: One containing the interface to the hardware and the bluesky-libraries, the other one containing mainly the user interface for settings that should be done inside NOMAD CAMELS. The Components / Signals from the bluesky-representation are recognized by NOMAD CAMELS and become settable and / or readable "channels", that can be used inside the protocols.

## Measurement protocols
When a measurement is run from NOMAD CAMELS, a complete python file, that can also be executed on its own, outside the UI, is generated. This enables users who have more specific requirements than provided by NOMAD CAMELS to add further functions to their protocol. Furthermore, the files can be exported and imported at other PCs running NOMAD CAMELS, enabling users to share their protocols with colleagues.

A measurement protocol or recipe is made up of several single steps. These are pre-defined blocks in the generated script that cover things like setting or reading instrument channels (e.g. a voltage), but also more sophisticated, frequently used functions like sweeping over a value.  
Instrument drivers can bring their own steps. The PID package does this, for example, with a step that is used to wait until the PID indicates that it is stable.

## Manual Controls
The manual controls inside NOMAD CAMELS are a kind of plugin. They provide functionalities to control the instruments of the setup without running a specific protocol. An example for this is a control window for motorized stages, e.g. to drive the investigated sample under a microscope.

Each instrument may provide its own manual control(s). This is for example used in PID-package.
## Data output
At the end of a protocol (or if it encounters an error), the data from NOMAD CAMELS is saved into an HDF5 file that is structured closely to the NeXus format [@Konnecke2015]. Exporting into csv for the data and into json for the metadata is also possible.

The raw data that should be collected is defined by the user, mainly with protocol steps like "Read_Channels". Additionally to that, NOMAD CAMELS collects the available metadata.
A big part of the metadata is all instrument settings of the instruments used. Further, information about user and investigated sample are added if provided.

It should be emphasized that the data file contains the complete python script that was used to create this data file. Additionally, the information about the python environment in which it was run is saved as well. This hugely simplifies reproducibility, since the measurement can be run the same way again, years later. 


# Acknowledgements

FAIRmat is funded by the the Deutsche Forschungsgemeinschaft ”DFG, German Re- search Foundation” – project 460197019.

# References