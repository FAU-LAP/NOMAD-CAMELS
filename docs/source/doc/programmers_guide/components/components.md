# Code Description

CAMELS builds upon well established Python packages. The GUI uses [PySide6](https://doc.qt.io/qtforpython-6/index.html) to provide a platform independent user interface with Qt. The orchestration of measurements is handled with [bluesky](https://blueskyproject.io/bluesky/main/index.html) and the abstraction of instrument communication with [ophyd](https://blueskyproject.io/ophyd/).

From the main window, all other UI elements are spawned. Up until a manual control or a protocol are started, CAMELS does _NOT_ communicate with any instruments. The only exception may be in some special cases where a first communication is necessary for the configuration settings of a specific instrument. In general, all configurations are only saved in CAMELS and only send to the instruments when a protocol is started.

When starting a protocol, a Python script is generated that runs this protocol. The protocol is provided as a [bluesky plan](https://blueskyproject.io/bluesky/main/plans.html), which runs with the specified instruments, represented by their [ophyd Devices](https://blueskyproject.io/ophyd/user/tutorials/device.html) from the respective driver.
The protocols run with the bluesky RunEngine, which is also spawned from the main window.


<p style="font-size: 1.5em; font-weight: bold; margin-top: 1em; margin-bottom: 0.5em; padding-bottom: 0.25em;">Project Structure</p>

- **Core Classes** (nomad_camels/main_classes)  
These files define the core classes, for example, the protocol class and main class for all steps in the protocol.

- **GUI Components** (nomad_camels/gui)  
This directory holds the graphical interface code. These .py files are generated from the QtDesigner .ui files by the pyside6-uic command.

- **Loop Steps** (nomad_camels/loop_steps)  
This submodule implements the various building blocks for the measurement protocols. Each class represents a different step in a protocol.

- **NOMAD Integration** (nomad_camels/nomad_integration)  
This section deals with communication and integration with [NOMAD](https://nomad-lab.eu) as an ELN.

- **Bluesky Handling** (nomad_camels/bluesky_handling)  
This module is dedicated to building and running the actual measurement protocols. 

- **Utilities** (nomad_camels/utility/)  
Supporting modules here include functionality for handling variables, device instantiation for example. These utilities support both protocol construction and GUI behavior.

Overall, the application is built around the idea of assembling a measurement protocol from modular "steps" (each implemented in the loop_steps package) managed by core classes and presented to the user via a rich GUI. The protocol is then converted into a Python script by the bluesky_handling code and executed to perform experiments.

Each module is interconnected: the GUI components let users configure and arrange steps; the loop_steps classes represent these steps; the main_classes hold their core behavior; and the bluesky_handling builds and executes the protocol that ultimately drives the measurement.

This layered and modular design helps keep code for UI, protocol building, and external system communications separate while still forming a cohesive measurement application.

__In more detail:__

```{toctree}
:maxdepth: 1

MainWindow <mainWindow_docs.md>
```