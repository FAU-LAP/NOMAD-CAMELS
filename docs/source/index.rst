.. image:: assets/camels-horizontal.svg

CAMELS - Configurable Application for Measurements, Experiments and Laboratory Systems
======================================================================================

CAMELS is a configurable measurement software, targeted towards the requirements of experimental solid-state physics. Here many experiments utilize a multitude of measurement devices used in dynamically changing setups. CAMELS will allow to define instrument control and measurement protocols using a graphical user interface (GUI). This provides a low entry threshold enabling the creation of new measurement protocols without programming knowledge or a deeper understanding of device communication.

The GUI generates python code that interfaces with instruments and allows users to modify the code for specific applications and implementations of arbitrary devices if necessary. Even large-scale, distributed systems can be implemented. CAMELS is well suited to generate FAIR-compliant output data. NeXus standards, immediate NOMAD integration and hence a FAIRmat compliant data pipeline can be readily implemented.

To learn more about NOMAD and FAIRmat visit the websites linked at the bottom or on the left.

https://github.com/FAU-LAP/CAMELS

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   Home <self>
   Installation <doc/installation/installation.md>
   Tutorial <doc/tutorials/quick_start.md>
   User's Guide <doc/users_guide.md>
   Instruments <doc/instruments/instruments.md>
   Programmer's Guide <doc/programmers_guide/programmers_guide.md>

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

.. toctree::
   :caption: Imprint
   :maxdepth: 1

   Imprint/Contact <https://www.lap.physik.nat.fau.de/impressum/>
   Data Privacy <data_privacy.md>