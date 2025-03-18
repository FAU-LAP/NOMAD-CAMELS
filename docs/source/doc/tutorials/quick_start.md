# Getting Started

After successful [installation](../installation/installation.md) of CAMELS you are ready to start your experiments.

<div class="box-container">
  <a href="quick_start_install.html" class="box">
    <span class="box-title">How to Add and Configure Instruments</span>
    <p class="box-content">The easiest way to get comfortable with CAMELS is to first learn how to add and configure already implemented instruments.</p>
  </a>

  <a href="quick_start_protocols.html" class="box">
    <span class="box-title">How to Setup Measurement Protocols</span>
    <p class="box-content">Learn how to setup measurement protocols. Use the instruments you configured in measurement sequences.</p>
  </a>

  <a href="quick_start_plots.html" class="box">
    <span class="box-title">How to Add Plots to a Protocol</span>
    <p class="box-content">Learn how to configure live plots for the the measurement sequence you configured.</p>
  </a>

  <a href="quick_start_manual_controls.html" class="box">
    <span class="box-title">Using Manual Controls</span>
    <p class="box-content">Apart from a protocol, learn how to use your instruments manually, e.g. for testing or setting the conditions for your measurement.</p>
  </a>

  <a href="../protocol_steps/protocol_steps_landing.html" class="box">
    <span class="box-title">Protocol Steps Explained</span>
    <p class="box-content">You can learn which protocol steps exist and how to use them. Protocol steps are the actions you can perform during a measurement sequence, like setting and reading an instrument channel, or creating a loop, waiting for a specified time.</p>
    <span class="more-link" onclick="toggleContent(event, this)">More</span>
  </a>

  <a href="../api/api_landing.html" class="box">
    <span class="box-title">How to Use the CAMELS API</span>
    <p class="box-content">If you want to control your CAMELS software with another program you can use CAMELS' API. This is especially useful if you have existing scripts but now want to control specific (new) aspects with CAMELS while still using the script you already have.</p>
    <span class="more-link" onclick="toggleContent(event, this)">More</span>
  </a>

  <a href="../instruments/instruments.html" class="box">
    <span class="box-title">List of Available Instruments</span>
    <p class="box-content">Here you find a list of available instruments that are already implemented.</p>
  </a>

  <a href="../programmers_guide/drivers/drivers_tutorial.html" class="box">
    <span class="box-title">How to Write New Drivers for Your Instruments</span>
    <p class="box-content">You can add your own instruments that have not yet been implemented by writing your own drivers. You can follow our step-by-step guide for writing drivers or start with the new driver documentation directly.</p>
    <span class="more-link" onclick="toggleContent(event, this)">More</span>
  </a>
</div>


```{eval-rst}
.. toctree::
   :hidden:
   :maxdepth: 2

   Adding Instruments <quick_start_install.md>
   Measurement Protocols <quick_start_protocols.md>
   Plots in Measurements <quick_start_plots.md>
   Manual Controls <quick_start_manual_control.md>
```


<!-- 
### How to Add and Configure Instruments

The easiest way to get comfortable with CAMELS is to first learn [how to add and configure](quick_start_install.md) already implemented instruments.

---

### How to Setup Measurement Protocols

Learn how to [setup measurement protocols](quick_start_protocols.md). Use the instruments you configured in measurement sequences.

---

### Protocol Steps Explained

You can learn which protocol steps exists and how to use them [here](../protocol_steps/protocol_steps_landing.md). Protocol steps are the actions you can perform during a measurement sequence, like setting and reading an instrument channel, or creating a loop, waiting for a specified time, 

---

### How to Use the CAMELS API

If you want to control your CAMELS software with another program you can use [CAMELS' API](../api/api_landing.md). This is especially useful if you have existing scripts but now want to control specific (new) aspects with CAMELS while still using the script you already have.

---

### List of Available Instruments

[Here](../instruments/instruments.rst) you find a list of available instruments that are already implemented.

---

### How to Write New Drivers for Your Instruments

You can add your own instruments that have not yet been implemented by writing your **own drivers**.

You can follow our [step-by-step guide](../programmers_guide/drivers/drivers_tutorial.md) for writing drivers or start with the [new driver documentation](../programmers_guide/instrument_drivers.md) directly. -->
