<style>
.box-container {
  display: flex;
  gap: 16px;
  justify-content: start;
}

.box {
  border: 1px solid #e0e0e0;
  padding: 16px;
  border-radius: 8px;
  width: 200px;
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.box:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.box-title {
  font-size: 16px;
  font-weight: bold;
  color: #2d64f2; /* Adjust color as needed */
  text-decoration: none;
  margin-bottom: 8px;
  display: block;
}

.box-content {
  font-size: 14px;
  color: #555;
}
</style>

# Getting Started

After successful [installation](../installation/installation.md) of CAMELS you are ready to start your experiments.

<div class="box-container">
  <a href="quick_start_install.md" class="box">
    <span class="box-title">How to Add and Configure Instruments</span>
    <p class="box-content">The easiest way to get comfortable with CAMELS is to first learn how to add and configure already implemented instruments.</p>
  </a>
  <a href="quick_start_protocols.md" class="box">
    <span class="box-title">How to Setup Measurement Protocols</span>
    <p class="box-content">Learn how to setup measurement protocols. Use the instruments you configured in measurement sequences.</p>
  </a>
  <a href="../protocol_steps/protocol_steps_landing.md" class="box">
    <span class="box-title">Protocol Steps Explained</span>
    <p class="box-content">You can learn which protocol steps exists and how to use them. Protocol steps are the actions you can perform during a measurement sequence, like setting and reading an instrument channel, or creating a loop, waiting for a specified time, </p>
  </a>
</div>

### How to Add and Configure Instruments

The easiest way to get comfortable with CAMELS is to first learn [how to add and configure](quick_start_install.md) already implemented instruments.

---

### How to Setup Measurement Protocols

Learn how to [setup measurement protocols](quick_start_protocols.md). Use the instruments you configured in measurement sequences.

---

### Protocol Steps Explained

You can learn which protocol steps exists and how to use them [here](../protocol_steps/protocol_steps_landing.md). Protocol steps are the actions you can perform during a measurement sequence, like setting and reading an instrument channel, or creating a loop, waiting for a specified time, 

---

### Hot to Use the CAMELS API

If you want to control your CAMELS software with another program you can use [CAMELS' API](../api/api_landing.md). This is especially useful if you have existing scripts but now want to control specific (new) aspects with CAMELS while still using the script you already have.

---

### List of Available Instruments

[Here](../instruments/instruments.rst) you find a list of available instruments that are already implemented.

---

### How to Write New Drivers for Your Instruments

You can add your own instruments that have not yet been implemented by writing your **own drivers**.

You can follow our [step-by-step guide](../programmers_guide/drivers/drivers_tutorial.md) for writing drivers or start with the [new driver documentation](../programmers_guide/instrument_drivers.md) directly.
