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
   - name: FAIRmat, Humboldt-Universität zu Berlin
     index: 2
date: 13 July 2023
bibliography: paper.bib

---

# Summary

NOMAD-CAMELS is a configurable measurement software, targeted towards the requirements of experimental solid-state physics. Here many experiments utilize a multitude of measurement devices used in dynamically changing setups. CAMELS will allow to define instrument control and measurement protocols using a graphical user interface (GUI). This provides a low entry threshold enabling the creation of new measurement protocols without programming knowledge or a deeper understanding of device communication. The GUI generates python code that interfaces with instruments and allows users to modify the code for specific applications and implementations of arbitrary devices if necessary. Even large-scale, distributed systems can be implemented. CAMELS is well suited to generate FAIR-compliant output data. Nexus standards, immediate NOMAD integration and hence a FAIRmat compliant data pipeline can be readily implemented.

# Statement of need

In experimental physics many home-built, ad hoc measurement setups are used. Typically, a specific software is written to control each of these setups. Although there are already tools available (e.g. "SweepMe!" [@SweepMe]) to realise the control of different measurement instruments, they are usually not open source and their data output is not compliant to the FAIR principles [@Wilkinson2016].

With NOMAD CAMELS we develop a tool that is completely free to use for everybody and collects all the metadata of experiment, known to the computer, automatically for each measurement. By providing an easy to use graphical user interface, NOMAD CAMELS allows the collection of data and rich metadata even without programming knowledge. With the default output as a structured .hdf5 file, NOMAD CAMELS' measurement data stays as close to the NeXus format [@Konnecke2015] as possible, while staying agnostic of the measurement itself, complying with the FAIR principles.

Furthermore, NOMAD CAMELS provides a direct connection to NOMAD [@Draxl2019] (or NOMAD Oasis, a local installation) to make use of electronic lab notebook (ELN) features. The user can select sample-data from NOMAD to connect with the measurement and directly upload the measured data, providing a simple and fast workflow in the lab.

# Acknowledgements

FAIRmat is funded by the the Deutsche Forschungsgemeinschaft ”DFG, German Re- search Foundation” – project 460197019.

# References