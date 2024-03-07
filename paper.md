---
title: 'NOMAD CAMELS: Configurable Application for Measurements, Experiments and Laboratory Systems'
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
   - name: Heinz Junkes
     orcid: 0000-0002-0218-4873
     affiliation: 3
   - name: Heiko B. Weber
     orcid: 0000-0002-6403-9022
     affiliation: 1
   - name: Michael Krieger
     orcid: 0000-0003-1480-9161
     corresponding: true # (This is how to denote the corresponding author)
     affiliation: 1

affiliations:
   - name: Lehrstuhl für Angewandte Physik, Department Physik, Friedrich-Alexander Universität Erlangen-Nürnberg, Germany.
     index: 1
   - name: Physics Department and CSMB, Humboldt-Universität zu Berlin, Berlin, Germany.
     index: 2
   - name: Fritz-Haber-Institut, Berlin, Germany.
     index: 3
date: 20 November 2023
bibliography: paper.bib

---

# Summary

NOMAD CAMELS (short: CAMELS) is a configurable, open-source measurement software that records fully self-describing experimental data. It has its origins in the field of experimental physics where a wide variety of measurement instruments are used in frequently changing experimental setups and measurement protocols. CAMELS provides a graphical user interface (GUI) which allows the user to configure experiments without the need of programming skills or deep understanding of instrument communication. CAMELS translates user-defined measurement protocols into stand-alone executable Python code for full transparency of the actual measurement sequences. Existing large-scale, distributed control systems using e.g. EPICS can be natively implemented. CAMELS is designed with focus on full recording of data and metadata. When shared with others, data produced with CAMELS allow full understanding of the measurement and the resulting data in accordance with the **FAIR** (**F**indable, **A**ccessible, **I**nteroperable and **R**e-usable) principles [@Wilkinson2016].


# Statement of need
Research data management has piqued greater and greater interest in recent years. Today, research funding agencies demand sustainable research data strategies. The key criterion is to create research data following the FAIR principles and thereby improve world-wide data-driven research [@DFG_position_paper].
While one ingredient, electronic lab notebooks, are an important step towards FAIR data, it is equally important to record the measurement data and related metadata along FAIR principles as early as possible in the research workflow. 

In experimental physics many custom-built measurement setups are controlled by very specific software written by individual researchers.
This results in a heterogeneous landscape of software fragments for measurements written in many different languages and with often incomplete documentation, making it almost impossible for other researchers to extend existing code.
The degree to which the stored raw data is understandable varies greatly but is often unintelligible even for researchers from the same lab.
Important metadata such as instrument settings or the actual measurement steps performed to obtain the final raw data are rarely recorded, making it virtually impossible to reproduce experiments. Therefore, the documentation of experiments is incomplete preventing FAIR research data.
Although there are some tools available (e.g. _SweepMe!_ [@SweepMe], _iC_ [@pernstich2012], PyMoDAQ [@PyMoDAQ]) to realise control of arbitrary measurement instruments, they are frequently not open-source or their data output is not compliant with the FAIR principles.

![Visualization of CAMELS functionality and workflow. CAMELS connects directly with local instruments and/or large-scale lab infrastructure running network protocols, e.g. EPICS. Customizable measurements protocols are translated into Python code and executed. The output is FAIR-compliant measurement data. \label{fig:camels_overview}](pictures/Bild_CAMELS.png){ width=80% }

# NOMAD CAMELS
CAMELS is an open-source tool that automatically collects all computer-accessible experimental metadata. It features a user-friendly graphical interface that enables the creation and customization of measurements without the need for programming knowledge. By default, the data is stored in a structured HDF5 file format that closely resembles the structure of the NeXus standard [@Konnecke2015; @FAIRmatNeXusProposal].
The final HDF5 file contains both the actual measurement data and metadata in a single file, compliant to the FAIR principles. 

CAMELS is a stand-alone desktop application. It allows for direct access to the _NOMAD_ repository [@scheidgenFAIRResearchData2023], [@scheidgenNOMADDistributedWebbased2023] or its on-premise installation called _NOMAD Oasis_ enabling direct linking to electronic lab notebook (ELN) entries. The user can for example connect measurements to previous experiment workflows documented in _NOMAD_ ELNs. CAMELS can subsequently upload measurement results directly into the ELN providing a simple and stream-lined data workflow.

CAMELS builds on _bluesky_ [@Allan2019; @bluesky] initially developed to control instruments at large-scale research institutions using EPICS [@Knott1994; @EPICS]. In CAMELS, _bluesky_ is employed to orchestrate the instrument communication either directly (e.g. via PyVISA [@PyVISA])
or via using network protocols. Existing lab infrastructure controlled by EPICS is therefore immediately accessible. A schematic overview of the functionality of CAMELS is displayed in \autoref{fig:camels_overview}.

CAMELS provides a comprehensive set of functionalities that can be split into three primary components: instrument management, measurement protocols and manual controls. 

![**(a)** The instrument manager allows to install and configure instrument drivers from the curated instrument driver library or the user's hard drive. **(b)** The measurement protocol editor allows users to configure arbitrary measurement sequences. \label{fig:manager_protocols}](pictures/CAMELS_manager_protocol.png)

## Instrument Management
Scientific instruments can be added to CAMELS in two ways: The first involves the _instrument manager_ (c.f. \autoref{fig:manager_protocols}a) to add instruments from the official curated driver repository [@CAMELS_drivers]. These drivers are installed into the Python environment via _pip_ [@PipDocumentationV23] with each driver being packaged individually.

The second way is to add self-built drivers by creating the necessary files locally and placing these in the directory specified in the CAMELS settings. To facilitate this process CAMELS provides a _driver builder_ that automatically generates the essential structure and boilerplate code. As CAMELS is an open-source project developed by and for the community, users are encouraged to contribute to the driver library by creating pull requests for new drivers on the GitHub repository [@CAMELS_drivers].

In general, a CAMELS driver comprises two files: One containing the hardware interface communication, the other one defining the available instrument settings. Data communication to instruments is handled via _channels_ that can be set and/or read; they correspond to an instrument's individual functionality or physical property.


## Measurement protocols
In CAMELS a _measurement protocol_ is a distinctive sequence of individual steps including setting and reading instrument channels (see \autoref{fig:manager_protocols}b), loops, conditional execution, running sub-protocols, PID control, etc. This yields a measurement in a 'recipe-style' format, where the next step is usually executed after the successful completion of the preceding step. Asynchronous data acquisition is supported.

CAMELS translates the protocol created in the GUI into a Python script, which is then executed. The script can be viewed, run independently of CAMELS, and modified if required. CAMELS protocols and settings can be stored and shared with colleagues enabling easy repeatability of experiments. 



## Manual controls
Certain scientific instruments require manual control before starting predefined measurement routines, e.g. adjusting stages, controlling temperature, valves, pumps, etc. In CAMELS this is achieved through the _manual controls_ functionality which can be applied to any writable instrument channel.

## Data output

![CAMELS stores measurement data together with rich metadata collected automatically into a structured HDF5 file by default. This includes **(a)** a human readable measurement protocol summary and **(b)** the executable Python script that was used to actually record the data. This allows others to understand the data acquisition and to reproduce the experiment. \label{fig:h5_data}](pictures/h5_data.png)

After executing the measurement protocol, the time-stamped data is by default saved to an HDF5 file with a structure similar to the NeXus standard [@Konnecke2015]. Data can also be exported in CSV format with the metadata exported in JSON.

The stored data can be divided into distinct sections:

- Time-stamped raw data obtained during the execution of the measurement protocol.
- Instrument settings.
- Human-readable summary of the measurement protocol information (see \autoref{fig:h5_data}a).
- Complete Python script that recorded the data (see \autoref{fig:h5_data}b) as well as information on the Python environment, i.e. a list of used packages and versions.
- User-defined metadata, e.g. sample and user information.

## Documentation
In-depth documentation and guides for installing, using and troubleshooting can be found on the [CAMELS documentation webpage](https://fau-lap.github.io/NOMAD-CAMELS/) [@fuchsCAMELSConfigurableApplication].

# Acknowledgements
We thank Patrick Oppermann (Fritz-Haber-Institut der Max-Planck-Gesellschaft) for valuable discussions.

NOMAD CAMELS is being developed within the NFDI consortium _FAIRmat_ funded by the Deutsche Forschungsgemeinschaft "DFG, German Research Foundation", project 460197019.

# References