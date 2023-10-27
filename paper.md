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

NOMAD-CAMELS is a configurable measurement software, that records fully self-describing experimental data. It has its origins in the field of experimental physics where a wide variety of measurement devices are used in rapidly changing experimental setups. CAMELS is designed with focus on full recording of data and metadata, allowing others to understand the data and the exact measurement procedure employed. CAMELS provides a user-friendly graphical user interface (GUI) which allows the user to define instrument control and measurement protocols. The GUI provides a low entry threshold enabling the creation of new measurement protocols without requiring programming knowledge or deep understanding of device communication. CAMELS generates python code to interface with instruments, allowing users to customize the code for specific applications and arbitrary device implementation if needed. Existing large-scale, distributed control systems using EPICS can be readily implemented. 
Researchers can take their first step towards a FAIR-data pipeline and reproducible science by utilizing CAMELS.


# Statement of need

In experimental physics many home-built, ad hoc measurement setups are used. Typically, a specific software is written to control each of these setups. Although there are already tools available (e.g. "SweepMe!" [@SweepMe]) to realise the control of different measurement instruments, they are usually not open source and their data output is not compliant to the FAIR principles [@Wilkinson2016].

With NOMAD CAMELS we develop a tool that is completely free to use for everybody and collects all the metadata of experiment, known to the computer, automatically for each measurement. By providing an easy to use graphical user interface, NOMAD CAMELS allows the collection of data and rich metadata even without programming knowledge. With the default output as a structured .hdf5 file, NOMAD CAMELS' measurement data stays as close to the NeXus format [@Konnecke2015] as possible, while staying agnostic of the measurement itself, complying with the FAIR principles.

Furthermore, NOMAD CAMELS provides a direct connection to NOMAD [@Draxl2019] (or NOMAD Oasis, a local installation) to make use of electronic lab notebook (ELN) features. The user can select sample-data from NOMAD to connect with the measurement and directly upload the measured data, providing a simple and fast workflow in the lab.

# NOMAD CAMELS

The functionalities of the main UI can be split into three parts, the instrument management, manual controls and measurement protocols. For instrument control and orchestration of measurements, NOMAD CAMELS uses bluesky and related packages [@Allan2019; @bluesky]. Using these packages, NOMAD CAMELS can easily communicate with EPICS [@Knott1994; @EPICS] and thus also supports large scale, distributed systems.

## Instrument Management
Instruments in NOMAD CAMELS can be added in two ways. The simple way is to add them via the instrument management in the software, which checks a curated list on our driver-repo [@CAMELS_drivers]. The drivers are installed to the python environment via pip, with each driver being represented by its own package.

The other way to add drivers is by placing them into the folder specified under NOMAD CAMELS' settings. This is the way to go for users who want to write their own drivers. Although it is possible to share them with the community by contributing to the drivers repo or uploading them to PyPI, sometimes it might be not possible to users, because of copyright reasons.

In general, a driver for NOMAD CAMELS is made up of two files: One containing the interface to the hardware and the bluesky-libraries, the other one containing mainly the user interface for settings that should be done inside NOMAD CAMELS. The Components / Signals from the bluesky-representation are recognized by NOMAD CAMELS and become settable and / or readable "channels", that can be used inside the protocols.

## Manual Controls
The manual controls inside NOMAD CAMELS are a kind of plugin. They provide functionalities to control the instruments of the setup without running a specific protocol. An example for this is a control window for motorized stages, e.g. to drive the investigated sample under a microscope.

Each instrument may provide its own manual control(s). This is for example used in PID-package.

## Measurement protocols
When a measurement is run from NOMAD CAMELS, a complete python file, that can also be executed on its own, outside the UI, is generated. This enables users who have more specific requirements than provided by NOMAD CAMELS to add further functions to their protocol. Furthermore, the files can be exported and imported at other PCs running NOMAD CAMELS, enabling users to share their protocols with colleagues.

A measurement protocol or recipe is made up of several single steps. These are pre-defined blocks in the generated script that cover things like setting or reading instrument channels (e.g. a voltage), but also more sophisticated, frequently used functions like sweeping over a value.  
Instrument drivers can bring their own steps. The PID package does this, for example, with a step that is used to wait until the PID indicates that it is stable.

## Data output
At the end of a protocol (or if it encounters an error), the data from NOMAD CAMELS is saved into an HDF5 file that is structured closely to the NeXus format [@Konnecke2015]. Exporting into csv for the data and into json for the metadata is also possible.

The raw data that should be collected is defined by the user, mainly with protocol steps like "Read_Channels". Additionally to that, NOMAD CAMELS collects the available metadata.
A big part of the metadata is all instrument settings of the instruments used. Further, information about user and investigated sample are added if provided.

It should be emphasized that the data file contains the complete python script that was used to create this data file. Additionally, the information about the python environment in which it was run is saved as well. This hugely simplifies reproducibility, since the measurement can be run the same way again, years later. 


# Acknowledgements

FAIRmat is funded by the the Deutsche Forschungsgemeinschaft ”DFG, German Re- search Foundation” – project 460197019.

# References