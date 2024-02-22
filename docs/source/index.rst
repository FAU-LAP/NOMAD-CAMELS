.. image:: assets/camels-horizontal.svg

NOMAD CAMELS - Your Simple Path to FAIR Experimental Data
######################################################################################

What is NOMAD CAMELS?
===============
**CAMELS** (\ **C**\ onfigurable \ **A**\ pplication for \ **M**\ easurements, \ **E**\ xperiments and \ **L**\ aboratory \ **S**\ ystems) is an open-source measurement software, targeted towards the requirements of experimental physics. Ease of use, rich metadata and FAIR-compliant data are at the heart of CAMELS design.


CAMELS provides a graphical user interface (GUI) that can be used to setup instrument control and measurement protocols. The GUI then generates Python code that interfaces with `bluesky <https://blueskyproject.io/>`_ to communicate with the instruments and orchestrate the measurement. CAMELS can also be used to communicate with large-scale, distributed systems implemented with `EPICS <https://epics-controls.org/>`_.

Why CAMELS?
===========
In experimental physics many experiments utilize a multitude of different measurement devices used in dynamically changing setups where changing measurement procedures or adding new devices is often cumbersome and difficult as it often requires advanced programming knowledge. CAMELS will allow you to define instrument control and measurement protocols using a graphical user interface (GUI) where each measurement step can be added with the click of a button. This provides a low entry-threshold enabling the creation of new and sophisticated measurement protocols without programming knowledge or a deeper understanding of device communication.

Who is CAMELS for?
==================
CAMELS is suited for any researcher not wanting to deal with measurement orchestration and device communication while still having full control and sophisticated data and metadata saving. Implementing new instruments can be done by any one and can be shared with the community.
As CAMELS takes care of saving all available metadata, you can share understandable measurement data with colleagues and other researchers with just a few clicks.


How to get started?
===================
To get started with CAMELS first `install <https://fau-lap.github.io/NOMAD-CAMELS/doc/installation/installation.html>`_ it and learn how to use it with our "Getting started" `tutorial <https://fau-lap.github.io/NOMAD-CAMELS/doc/tutorials/quick_start.html>`_.


Project and Community
=====================
CAMELS is being developed in the framework of the NFDI consortium `FAIRmat <https://www.fairmat-nfdi.eu/fairmat/>`_.

The CAMELS software can be viewed here https://github.com/FAU-LAP/CAMELS. We invite you to open issues on GitHub if you encounter any problems or bugs.

Contact
=======
If you have any questions or feedback you can reach the development team of CAMELS via:

E-mail `nomad-camels@fau.de <mailto:nomad-camels@fau.de>`_

Join the discussion on `GitHub <https://github.com/FAU-LAP/NOMAD-CAMELS/discussions>`_

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   Home <self>
   Installing CAMELS <doc/installation/installation.md>
   Getting Started <doc/tutorials/quick_start.md>
   Handling HDF5 Files <doc/handling_hdf5.md>

.. toctree::
   :maxdepth: 2
   :caption: Instruments

   Available Instruments <doc/instruments/instruments.md>
   Create New Instrument Drivers <doc/programmers_guide/instrument_drivers.md>

.. toctree::
   :maxdepth: 2
   :caption: Combine with EPICS

   Create New EPICS IOC <doc/epics/new_ioc.md>
   Run IOCs <doc/epics/procServ.md>
   Archiver Appliance <doc/epics/ArchiverAppliance.md>
   Example Setups <doc/epics/examples.md>
   

.. toctree::
   :maxdepth: 2
   :caption: Maintaining CAMELS Project

   Maintain CAMELS <doc/programmers_guide/programmers_guide.md>

.. toctree::
   :maxdepth: 1
   :caption: Contribute to CAMELS

   Running Tests <doc/contribute/running_tests.md>
   General Process <doc/contribute/general_process.md>
   Code of Conduct <doc/contribute/code_of_conduct.md>

.. toctree::
   :maxdepth: 2
   :caption: Code Reference

   nomad-camels <nomad_camels.rst>
   genindex


.. toctree::
   :caption: Links

   Find us on GitHub <https://github.com/FAU-LAP/NOMAD-CAMELS>
   NOMAD Website <https://nomad-lab.eu/nomad-lab/>
   FAIRmat Website <https://www.fairmat-nfdi.eu/fairmat>
   FAU/LAP Website <https://www.lap.physik.nat.fau.eu/>

.. toctree::
   :caption: Imprint/Contact
   :maxdepth: 1

   Imprint <https://www.lap.physik.nat.fau.de/impressum/>
   Contact <contact.md>
   Data Privacy <data_privacy.md>
