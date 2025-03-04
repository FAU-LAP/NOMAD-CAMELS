# MainWindow Documentation

The `MainWindow` class is the central hub of the NOMAD CAMELS application. It connects the graphical user interface (GUI) with the underlying functionality needed for running protocols, managing devices, handling user/sample data, integrating external extensions, and much more.

## Overview

At its core, the `MainWindow` is responsible for:

- **UI Initialization and Layout:**  
  Loads the user interface from a generated UI file, sets up widget layouts (including custom ones like the tag flow layout), applies window properties (title, icons, styling), and redirects console output to a dedicated text area.

- **Signal-Slot Connectivity:**  
  Connects user interface events (e.g., button clicks, combo box changes, keyboard shortcuts) to methods that perform actions such as adding protocols, managing instruments, and changing user or sample data.

- **Protocol Management:**  
  Enables users to add, import, build, run, pause, resume, and stop measurement protocols. Protocols are stored in an internal dictionary, and their execution is managed via the Bluesky RunEngine. Protocols can also be queued, and the system automatically triggers the next protocol when one completes.

- **Manual Control Management:**  
  Supports adding and configuring manual controls which allow direct device interaction. Manual controls are organized into tabs, and each control can be configured, started, or removed via dedicated UI elements.

- **Device Management:**  
  Maintains a list of active instruments. When a protocol is executed, the application instantiates the required devices (often in a separate thread), then passes these devices to the protocol. After the protocol runs, devices not in use are closed.

- **NOMAD Integration and Extension Handling:**  
  Integrates NOMAD functionality for user login, sample selection, and data upload. An embedded FastAPI server may be started for remote control, and external extensions can be loaded to add further features to the application.

- **State and Preferences Persistence:**  
  Loads user preferences and the current state at startup. The application automatically saves changes (with optional backups) and restores state when restarted.

---

## Detailed Components

### 1. UI Initialization and Layout

- **UI Setup:**  
  The `MainWindow` class inherits from both `QMainWindow` and a generated UI class (`Ui_MainWindow`). The `setupUi(self)` method initializes all widgets and lays them out according to the design specified in the UI file.

- **Widget Layouts and Styling:**  
  - The main window sets custom properties like the window title and icon.  
  - Layouts such as grid layouts and custom flow layouts (e.g., for displaying tags) are established to arrange the protocol buttons, manual controls, and the console output widget.
  - Console output is redirected to a dedicated text area by reassigning `sys.stdout` and `sys.stderr` to custom text writer objects.

### 2. Signal-Slot Connections

- **Event Handling:**  
  A wide variety of signals are connected to their respective slots. For example:
  - **User Interactions:** Button clicks for adding protocols, managing devices, and editing user/sample information.
  - **Shortcuts:** A `Ctrl+s` shortcut is connected to the state-saving method.
  - **Run Engine Feedback:** Signals such as `protocol_stepper_signal` update the progress bar during protocol execution.

- **Remote API Integration:**  
  If enabled, a FastAPI server is started on a separate thread. This server sends signals (for example, to start a protocol or update the user/sample information) that are connected to methods in the `MainWindow`.

### 3. Protocol Management

- **Adding and Importing Protocols:**  
  - **Adding New Protocols:** Users can open a protocol configuration dialog to define a new protocol. Once confirmed, the protocol is stored in an internal dictionary (`protocols_dict`) and a corresponding button is added to the measurement area.
  - **Importing Protocols:** Protocols can also be imported from external files. After import, they are opened in a configuration dialog and then added to the internal list.

- **Building Protocol Files:**  
  Before execution, protocols are built into Python files. This involves:
  - Capturing session details, tags, and file paths.
  - Calling an external protocol builder that writes a Python file with the protocol code.

- **Running Protocols:**  
  - The run process begins by ensuring that the Bluesky RunEngine is initialized.
  - Required devices are instantiated (using a separate thread to avoid UI blocking).
  - The protocol file is built and imported dynamically.
  - UI elements, such as progress bars and control buttons, are updated throughout the execution.
  - After running, protocols may be auto-uploaded to NOMAD if configured.

- **Pausing, Resuming, and Stopping:**  
  Dedicated methods allow users to pause, resume, or stop protocols. These actions update both the UI and the underlying RunEngine.

- **Queue Management:**  
  Protocols can be queued for sequential execution. The run queue widget monitors the execution state and automatically triggers the next protocol when the current one finishes.

### 4. Manual Control Management

- **Adding Manual Controls:**  
  Users can add manual controls through a dedicated dialog. The manual control data is stored in a dictionary (`manual_controls`), and a button representing the control is added to a separate UI area.

- **Configuring and Running Controls:**  
  Each manual control button is connected to functions that:
  - Open a configuration dialog,
  - Start the manual control,
  - Allow the control to be removed or moved to a different tab.

- **Tab Organization:**  
  Manual control buttons are grouped into tabs for better organization. Users can move controls between tabs using a move dialog.

### 5. Device Management

- **Active Instruments:**  
  The `active_instruments` dictionary keeps track of devices currently in use. This list is used during protocol execution to determine which devices need to be instantiated.

- **Managing Instruments:**  
  An instrument management dialog allows users to add or remove devices. After the dialog is closed, the `active_instruments` dictionary is updated, and the UI is refreshed accordingly.

- **Device Instantiation:**  
  When a protocol runs, the application instantiates the required devices in a separate thread. Once the devices are ready, they are passed to the protocol execution routines.

- **Resource Cleanup:**  
  After protocols finish executing, devices that are no longer needed are closed. This is particularly important when multiple protocols are queued.

### 6. NOMAD Integration and Extension Handling

- **User and Sample Management:**  
  - Users can log in to NOMAD, which adjusts the UI to show NOMAD-specific controls.  
  - Sample selection dialogs allow the user to select a NOMAD sample, and the selected sample data is integrated into the application.

- **API Server:**  
  A FastAPI server can be started in a separate thread to enable remote control of the application. The API server sends signals to the MainWindow (such as starting a protocol or setting user data), which are then handled by the appropriate methods.

- **Extensions:**  
  - External extensions are loaded based on the preferences.
  - Extensions are given required contexts (such as the ELN context) so that they integrate smoothly with the application.
  - The extension manager dialog allows users to manage and update extensions. Some changes may require a restart of the application.

- **Watchdog Functionality:**  
  Watchdogs monitor specific conditions during protocol execution. When a watchdog condition is met, the protocol may be paused and a special watchdog protocol is triggered.

### 7. State and Preferences Persistence

- **Preferences Loading:**  
  User preferences (including theme, file paths, autosave settings, etc.) are loaded at startup and applied across the application. Changes in preferences trigger updates (e.g., restarting the API server if the port changes).

- **State Saving and Loading:**  
  The current state of the application—including protocols, manual controls, and active instruments—is saved to preset files. These files are automatically reloaded on startup, ensuring that the user’s working state is preserved.

- **Auto-Save and Backups:**  
  The system supports auto-saving and can create backups of the current preset. This helps prevent data loss in case of unexpected shutdowns.

---

## Component Interaction Flow

1. **Startup:**
   - The MainWindow is instantiated and the UI is initialized.
   - Preferences and the last saved state are loaded.
   - Console output is redirected and initial instrument, protocol, and manual control areas are prepared.
   - If enabled, the FastAPI server is started for remote control.

2. **User Interaction:**
   - The user may add a new protocol or import an existing one.
   - Manual controls can be added and configured via dialogs.
   - Instruments are managed through a dedicated dialog.
   - NOMAD login and sample selection allow integration with remote data storage and management.
   - Preferences can be changed, which updates the UI and functionality immediately.

3. **Protocol Execution:**
   - When a protocol is started, the application builds a Python file for the protocol and instantiates the required devices.
   - The protocol is executed using the Bluesky RunEngine.
   - Progress is shown via the progress bar, and controls allow pausing, resuming, or stopping the protocol.
   - Upon completion, the state is saved, and if additional protocols are queued, the next protocol begins automatically.
   - Optionally, data may be auto-uploaded to NOMAD.

4. **Extensions and Watchdogs:**
   - Extensions are loaded and initialized at startup, adding extra functionality.
   - Watchdogs are monitored during protocol execution. If a condition is met, the protocol is paused and a watchdog-specific routine is executed.

5. **Shutdown:**
   - On closing the MainWindow, all open dialogs and windows are closed.
   - The API server is stopped and the current state is saved.
   - Devices are properly closed to free resources.

---

## Conclusion

The `MainWindow` serves as the command center for the NOMAD CAMELS application, tying together a wide range of functionalities such as protocol management, manual control handling, device management, NOMAD integration, and state persistence. Through an intricate network of signals and slots, it provides a responsive user interface that can adapt to diverse experimental requirements. The modular design not only facilitates robust operation during live experiments but also supports easy extension and integration with external systems such as FastAPI and NOMAD.

This detailed breakdown should help you understand how the various components within `MainWindow` interact and work together to provide a cohesive user experience in NOMAD CAMELS.

---