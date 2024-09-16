<style>
.box-container {
  display: flex;
  gap: 16px;
  justify-content: start;
  flex-wrap: wrap;
}

.box {
  border: 1px solid #e0e0e0;
  padding: 16px;
  border-radius: 8px;
  min-width: 200px;
  max-width: 300px;
  flex-grow: 1;
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, max-height 0.3s ease; /* Add transition for height */
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column; /* Arrange content in a column */
  justify-content: flex-start; /* Align items at the start */
}

.box:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.box-title {
  font-size: 16px;
  font-weight: bold;
  color: #2d64f2;
  text-decoration: none;
  margin-bottom: 8px;
  display: block;
}

.box-content {
  font-size: 14px;
  color: #555;
  max-height: 92px; /* Initial height when not expanded */
  overflow: hidden;
  transition: max-height 0.3s ease; /* Smooth transition for expansion */
}

.box-content.expanded {
  max-height: 500px; /* Expand height when clicked */
}

/* .more-link {
  color: #2d64f2;
  cursor: pointer;
  margin-top: 2px;
  align-self: flex-start;
} */
.more-link {
  color: #ffffff; /* Change text color to white for contrast */
  background-color: #2d64f2; /* Button background color */
  padding: 8px 12px; /* Add padding for button-like appearance */
  margin-top: 8px; /* Add margin to separate it from content */
  border: none; /* Remove default border */
  border-radius: 4px; /* Round the corners */
  cursor: pointer; /* Show pointer cursor on hover */
  font-size: 14px; /* Adjust font size if necessary */
  text-align: center; /* Center the text */
  text-decoration: none; /* Remove underline */
  align-self: flex-start; /* Align to the start of the flex container */
}

.more-link:hover {
  color: #c2c6cf; /* Change text color on hover */
  text-decoration: underline; /* Add underline on hover */
  /* You can add more styles like background color, font weight, etc. */
}
</style>

<script>
function toggleContent(event, element) {
  event.preventDefault(); // Prevent the default link action
  event.stopPropagation(); // Prevent the click from bubbling up to the anchor
  const content = element.previousElementSibling;
  if (content.classList.contains('expanded')) {
    content.classList.remove('expanded');
    element.textContent = 'More';
  } else {
    content.classList.add('expanded');
    element.textContent = 'Less';
  }
}
</script>

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
