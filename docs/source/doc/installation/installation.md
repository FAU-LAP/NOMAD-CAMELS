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
  color: #1a46c0; /* Change text color on hover */
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

# CAMELS Installation

CAMELS is written in Python and requires the correct Python environment to run properly.

<div class="box-container">
  <a href="installation_installer.html" class="box">
    <span class="box-title">Windows Installer</span>
    <p class="box-content">We recommend to install CAMELS with the installer if you are using <strong>Windows</strong>. This will install Python 3.11 and create the required Python environment for you.</p>
  </a>
  <a href="installation_custom_unix.html" class="box">
    <span class="box-title">Manual Installation on Linux</span>
    <p class="box-content">Installation guide for Linux-type systems like Ubuntu, Debian and CentOS. Install Python, setup the environment and run CAMELS.</p>
  </a>
  <a href="installation_custom_macos.html" class="box">
    <span class="box-title">Manual Installation on macOS</span>
    <p class="box-content">Installation guide for systems running macOS. Install Python, setup the environment and run CAMELS.</p>
  </a>

  <a href="installation_custom_windows.html" class="box">
    <span class="box-title">Manual Installation on Windows</span>
    <p class="box-content">If you are familiar with Python and Python environments you can manually install CAMELS. Install Python, setup the environment and run CAMELS.</p>
  </a>
<br><br>
</div>

In the most basics cases a simple installation using _pip_ is sufficient. To install CAMELS to an existing Python environment (must be Python version 3.11.3 or newer) simply run

```bash
pip install nomad-camels
```

You can then run 

```bash
nomad-camels
```

 or  

```bash
python -m nomad_camels
```

to start CAMELS.

```{warning}
Some of the drivers do not support python 3.12 yet, so we suggest to stay with python 3.11.
```

If this does not work you can go to `/.desertenv/Lib/site-packages/nomad_camels/` and run

```bash
python .\CAMELS_start.py
```

There are several ways to set up the correct Python environment and install CAMELS depending on your operating system: