.. image:: assets/camels-horizontal.svg

NOMAD CAMELS - Your Simple Path to FAIR Experimental Data
######################################################################################

What is NOMAD CAMELS?
=========================



**CAMELS** (\ **C**\ onfigurable \ **A**\ pplication for \ **M**\ easurements, \ **E**\ xperiments and \ **L**\ aboratory \ **S**\ ystems) is an open-source measurement software, targeted towards the requirements of experimental physics. Ease of use, rich metadata and FAIR-compliant data are at the heart of CAMELS design.


.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/rVmxgwhoEVg" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" allow="autoplay" frameborder="0" allowfullscreen></iframe>
    </div>

.. raw:: html

    <br><br>

CAMELS provides a graphical user interface (GUI) that can be used to setup instrument control and measurement protocols. The GUI then generates Python code that interfaces with `bluesky <https://blueskyproject.io/>`_ to communicate with the instruments and orchestrate the measurement. CAMELS can also be used to communicate with large-scale, distributed systems implemented with `EPICS <https://epics-controls.org/>`_.

Learn more about CAMELS in our peer-reviewed paper

.. image:: https://joss.theoj.org/papers/10.21105/joss.06371/status.svg
   :target: https://doi.org/10.21105/joss.06371

Why CAMELS?
===========

.. raw:: html

    <div class="box-container">

        <div class="box">
            <div class="box-title">Smooth installation</div>
            <div class="box-content">
                CAMELS is a Python package distributed via PyPI. It is easily installable on any computer. On Windows, let the installer do all the work for you.
            </div>
        </div>

        <div class="box">
            <div class="box-title">Easy to use</div>
            <div class="box-content">
                No programming skills required. Just configure your measurement and process protocols. Get it done within minutes.
            </div>
        </div>

        <div class="box">
            <div class="box-title">FAIR data</div>
            <div class="box-content">
                Automatically store FAIR data with rich metadata that lets you and others understand your experiment in detail. Optionally connect directly with your NOMAD Oasis.
            </div>
        </div>

        <div class="box">
            <div class="box-title">Flexible and extendable</div>
            <div class="box-content">
                Add further instruments to your setup at will. Reuse and adapt existing measurements quickly.
            </div>
        </div>

        <div class="box">
            <div class="box-title">Scalable</div>
            <div class="box-content">
                Work with small setups using directly connected instruments. Or connect to large distributed systems using advanced protocols like EPICS.
            </div>
        </div>

        <div class="box">
            <div class="box-title">Community driven</div>
            <div class="box-content">
                Contribute to CAMELS and add further instruments on GitHub. CAMELS comes with an instrument driver wizard that helps you implement new instruments.
            </div>
        </div>

    </div>

In experimental sciences experiments often utilize a multitude of different measurement devices used in dynamically changing setups. Changing measurement procedures or adding new devices is often cumbersome and difficult as it often requires advanced programming knowledge. CAMELS allows you to define instrument control and measurement protocols using a graphical user interface (GUI) where each measurement step can be added with the click of a button. This provides a low entry-threshold enabling the creation of new and sophisticated measurement protocols without programming knowledge or a deeper understanding of device communication.

Who is CAMELS for?
==================
CAMELS is suited for any researcher not wanting to deal with measurement orchestration and device communication while still having full control and sophisticated data and metadata saving. Implementing new instruments can be done by any one and can be shared with the community.
As CAMELS takes care of saving all available metadata, you can share understandable measurement data with colleagues and other researchers with just a few clicks.


How to get started?
===================
To get started with CAMELS first `install <https://fau-lap.github.io/NOMAD-CAMELS/doc/installation/installation.html>`_ it and learn how to use it with our "Getting started" `tutorial <https://fau-lap.github.io/NOMAD-CAMELS/doc/tutorials/quick_start.html>`_.


Project and Community
=====================

If you have questions or problems with CAMELS we invite you to contact us via 

.. raw:: html


    <a href="https://discord.gg/Gyzx3ukUw8" target="_blank">
        <img src="https://cdn.prod.website-files.com/6257adef93867e50d84d30e2/636e0b52aa9e99b832574a53_full_logo_blurple_RGB.png" alt="Discord Logo" style="width: 127px; height: 24px; vertical-align: bottom;">
        Discord
    </a>

or by opening a

.. raw:: html


    <a href="https://github.com/FAU-LAP/NOMAD-CAMELS/issues" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo" style="width: 24px; height: 24px; vertical-align: bottom;">
        GitHub Issue
    </a>

CAMELS is being developed in the framework of the NFDI consortium `FAIRmat <https://www.fairmat-nfdi.eu/fairmat/>`_.

The source code of CAMELS is hosted on

.. raw:: html


    <a href="https://github.com/FAU-LAP/NOMAD-CAMELS" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo" style="width: 24px; height: 24px; vertical-align: bottom;">
        GitHub 
    </a>


We invite you to open issues on GitHub if you encounter any problems or bugs.

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
   Protocol Steps Explained <doc/protocol_steps/protocol_steps_landing.md>
   Handling HDF5 Files <doc/handling_hdf5.md>
   FAQ <doc/faq/faq.md>

.. toctree::
   :maxdepth: 2
   :caption: Instruments

   Available Instruments <doc/instruments/instruments.rst>
   Create New Instrument Drivers <doc/programmers_guide/instrument_drivers.md>

.. toctree::
   :maxdepth: 2
   :caption: API

   CAMELS API Overview <doc/api/api_landing.md>
   

.. toctree::
   :maxdepth: 2
   :caption: Combine with EPICS

   Create New EPICS IOC <doc/epics/new_ioc.md>
   Run IOCs <doc/epics/procServ.md>
   Archiver Appliance <doc/epics/ArchiverAppliance.md>
   Example Setups <doc/epics/examples.md>

.. toctree::
   :maxdepth: 2
   :caption: Videos

   User Feedback <doc/videos/user_feedback.md>
   Developer Statements <doc/videos/developer_statements.md>

.. toctree::
   :maxdepth: 2
   :caption: Maintaining CAMELS Project

   Maintain CAMELS <doc/programmers_guide/programmers_guide.md>

.. toctree::
   :maxdepth: 1
   :caption: Contribute to CAMELS

   General Process <doc/contribute/general_process.md>
   Running Tests <doc/contribute/running_tests.md>
   Code of Conduct <doc/contribute/code_of_conduct.md>

.. toctree::
   :maxdepth: 2
   :caption: Code Reference

   nomad-camels <code/nomad_camels.rst>
   helping packages <code/helping_packages.rst>
   drivers <code/drivers.rst>
   extensions <code/extensions.rst>
   genindex


.. toctree::
   :caption: Links

   Find us on GitHub <https://github.com/FAU-LAP/NOMAD-CAMELS>
   Cite NOMAD CAMELS <https://joss.theoj.org/papers/10.21105/joss.06371>
   NOMAD Website <https://nomad-lab.eu/nomad-lab/>
   FAIRmat Website <https://www.fairmat-nfdi.eu/fairmat>
   FAU/LAP Website <https://www.lap.physik.nat.fau.eu/>

.. toctree::
   :caption: Imprint/Contact
   :maxdepth: 1

   Imprint <https://www.lap.physik.nat.fau.de/impressum/>
   Contact <contact.md>
   Data Privacy <data_privacy.md>
