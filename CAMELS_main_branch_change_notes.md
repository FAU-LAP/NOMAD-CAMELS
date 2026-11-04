# CAMELS Changes Compared with `origin/main`

Source diff: [`CAMELS_main_branch_changes.patch`](CAMELS_main_branch_changes.patch)

This document explains the CAMELS branch changes file by file. It currently
starts with `.gitignore` and can be extended with the remaining files.

## `.gitignore`

### Line 18: virtual-environment rebuild logs

```gitignore
.venv-rebuild-logs/
```

Ignore temporary local virtual-environment rebuild logs.

## `nomad_camels/MainApp_v2.py`

### Step 1 -- Line 8: threading support

Import `threading` for synchronized API/GUI state access.

### Step 2 -- Line 118: application icon

Replace the PNG window icon with the high-resolution ICO asset.

### Step 3 -- Lines 142--153: measurement-status snapshot

Create a lock-protected plain-Python copy of the GUI measurement status. The
API thread reads this snapshot instead of reading Qt widgets directly.

### Step 4 -- Lines 406--409: API-to-GUI signals

Connect API requests for closing plots and saving protocol variables to GUI
thread handlers.

### Step 5 -- Lines 427--447: save protocol variables

Persist API-provided variables in the protocol, its `.cprot` file, and the
CAMELS state so parameter changes survive a restart.

### Step 6 -- Lines 779--786: remote plot cache

Register a compatible live plot cache when a plot window opens and unregister
it when the window closes.

### Step 7 -- Lines 2054--2071: first filename formatting path

Allow protocol and loop variables in measurement filename templates. Keep
unknown placeholders unchanged instead of failing the run.

### Step 8 -- Lines 2158--2165 and 2223: preparing and failure states

Publish `Preparing` before device setup and `Failed` when preparation raises
an exception.

### Step 9 -- Lines 2254--2256: active API run ID

Store the API run ID while the protocol is active so OASIS can associate the
remote run with its Dashboard state.

### Step 10 -- Lines 2329--2332 and 2673--2677: completion states

Publish `Finished`, 100% progress, and zero remaining time after normal run
completion and during the final cleanup path.

### Step 11 -- Lines 2719--2734: live progress access

Publish `Running` progress and timing updates, and add synchronized helper
methods for updating and reading the status snapshot.

### Step 12 -- Lines 2803--2820: second filename formatting path

Apply the same variable-aware, safe filename formatting when saving protocol
state through the second CAMELS save path.

## `nomad_camels/api/api.py`

### Step 1 -- Lines 1--18: proxy and service-information imports

Add request forwarding, thread synchronization, hostname, and start-time
support for remote OASIS access.

### Step 2 -- Lines 86--96: stable run response

Return `run_id`, `status_url`, and `result_url` after a protocol starts while
retaining the earlier status-link field for compatibility.

### Step 3 -- Lines 133--151: API-key protocol scope

Read the optional `protocol_name` scope from the API-key database. Older keys
without this column, or keys with a null scope, remain global keys.

### Step 4 -- Lines 154--199: run-status protocol ownership

Store the protocol name with each API run status and migrate existing status
databases by adding the column when necessary.

### Step 5 -- Lines 257--267: return the validated key

Return the validated API-key value to route handlers so they can apply its
protocol scope instead of receiving only `True`.

### Step 6 -- Lines 296--341: GUI signals and plot-cache registry

Add GUI-thread signals for closing plots and saving variables. Register only
plain-Python plot-cache snapshots for safe API access.

### Step 7 -- Lines 406--470: exposed-protocol and service helpers

Allow remote access only to protocols with `oasis_remote_control` enabled and
within the API-key scope. Add health and authenticated service-info endpoints.

### Step 8 -- Lines 483--548: read and save protocol parameters

List only exposed protocols, return the editable parameter names and current
defaults requested by the Dashboard, and save validated parameter defaults
through the GUI thread.

### Step 9 -- Lines 550--587: protect protocol JSON and global settings

Apply protocol exposure checks to protocol JSON. Restrict installation-wide
settings access to global API keys.

### Step 10 -- Lines 589--643: GUI monitoring and control endpoints

Expose open-plot count, thread-safe measurement status, plot-cache snapshots,
plot closing, and active PID plot data for the Dashboard.

### Step 11 -- Lines 645--704: authenticated Browser Plot proxy

Forward an authorized active Browser Plot from CAMELS localhost to OASIS. Only
ports created by the active protocol are accepted.

### Step 12 -- Lines 706--839: authorized protocol runs and results

Require exposed-protocol authorization when starting a run, save its protocol
ownership, return the stable run response, and restrict result/status access
for protocol-scoped keys.

### Step 13 -- Lines 907--945: active-run plot URLs

Provide Browser Plot data and HTML endpoints only while the requested API run
is the active CAMELS run.

### Step 14 -- Lines 950--1359: legacy global-control endpoints

Keep queue, sample, user, and session endpoints, but reject protocol-scoped
keys because these operations control the whole CAMELS installation.

## `nomad_camels/bluesky_handling/helper_functions.py`

### Lines 389--391: clear the paired Browser Plot

Clear the linked Browser Plot callback whenever CAMELS clears its matching Qt
plot.

## `nomad_camels/frontpanels/plot_definer.py`

### Lines 326--510: assign Browser Plot ports

Accept a caller-defined starting port and assign each new plot the first unused
local port. New Browser Plot output remains disabled until the user enables it.

### Lines 874--1118: keep port fields visible

Keep the Browser Plot port visible even when Show plot in browser is unchecked,
so the user can configure the port before enabling output.

### Lines 1399--1468: pass the configured port range through the overview

Preserve the caller's Browser Plot port range when reopening the plot editor.

## `nomad_camels/frontpanels/protocol_config.py`

### Lines 129--132 and 927: preserve exposure changes correctly

Pass the source protocol to General Settings so OASIS exposure takes effect
immediately for the running API. Restore the original exposure value if the
user discards the protocol editor changes.

## `nomad_camels/frontpanels/settings_window.py`

### Lines 24--54: create scoped API-key records

Centralize API-key generation and database migration. Store only a key hash,
optionally with a protocol scope, and return the plaintext key only once.

### Lines 399 and 551--557: reuse the shared key helper

Make the Settings API-key button use the common helper and allow database
records to store an optional protocol name.

## Protocol exposure configuration UI

### `nomad_camels/gui/general_protocol_settings.ui`, lines 4--224

Widen and reorganize General Settings. Add the Expose this protocol to OASIS
remote control checkbox, an OASIS URL field, and a button to open that URL.
Extend the filename help text with protocol-variable examples.

### `nomad_camels/gui/general_protocol_settings.py`, generated from the UI

Regenerate the Python Qt form for the updated `.ui` layout and controls. This
generated file should not be edited manually.

### `nomad_camels/gui/Ui_general_protocol_settings.py`, generated form

Add the corresponding generated Qt form module for the revised General
Settings UI. It mirrors the `.ui` file and should be regenerated, not manually
maintained, after future Designer changes.

## `nomad_camels/main_classes/protocol_class.py`

### Line 90: persisted OASIS exposure flag

Add `oasis_remote_control`, defaulting to `False`, to each measurement
protocol. A protocol must opt in before OASIS can discover or run it.

### Lines 567--613: editor source tracking and port range

Track the source protocol while editing and use Browser Plot ports starting at
8150 for General Configuration plots, separate from sequence plot ports.

### Lines 636--887: expose-to-OASIS UI behavior

Synchronize the checkbox with the protocol flag immediately, restore it on a
discarded edit, and show an OASIS navigation URL when enabled. The current
design uses one global key from Settings > API; the old protocol-specific-key
creation path is deliberately disabled.

## `nomad_camels/main_classes/plot_proxy.py`

### Lines 1--61: use the explicit `zmq` module

Replace obsolete `self.zmq` references with imported `zmq` constants and
functions so the stoppable ZeroMQ proxy can close reliably.

## `nomad_camels/main_classes/plot_plotly.py`

### Lines 123--184: Browser Plot snapshots and clearing

Add CORS headers, a read-only `/data` endpoint with optional bounded sampling,
and a `/clear_data` endpoint for 1D Browser Plots. Stored fit results are also
included and sampled.

### Lines 428--594: reliable 1D Dash lifecycle and data forwarding

Stop an earlier Dash process before reusing its port, ignore duplicate run
starts, forward already evaluated Qt data to the Browser Plot, and clear the
Dash data when its paired plot is cleared.

### Lines 674--990: equivalent 2D Browser Plot support

Add clear requests, reliable process shutdown, duplicate-start protection, and
clear synchronization for 2D Browser Plots.

## `nomad_camels/main_classes/plot_pyqtgraph.py`

### Lines 199--245: `RemotePlotCache`

Maintain a thread-safe, Qt-independent copy of 1D plot traces for OASIS API
consumers, including secondary-axis information.

### Lines 310--328: pair Qt and Browser Plot callbacks

Attach a Browser Plot callback to a Qt plot and make it reuse the Qt plot's
already evaluated values.

### Lines 869--1156: update remote and Browser Plot data together

Create the remote cache for each live plot, refresh it after every data update
or clear, and forward the same evaluated values to the paired Browser Plot.

## `nomad_camels/tests/api_test.py`

### Lines 36--145: test exposed-protocol filtering

Replace string fixtures with protocol-like objects, verify that only exposed
protocols are listed, verify editable-parameter responses, and verify that a
local-only protocol returns 404.

## `nomad_camels/utility/device_handling.py`

### Lines 24, 96--106, and 127--137: quiet optional-driver discovery

Suppress warnings only while discovering optional local drivers and log failed
optional imports at debug level instead of printing startup noise. Explicitly
configured unsupported drivers still fail normally.

## `setup_virtual_environment.py`

### Lines 1--87: local Python 3.11 environment helper

Add a Windows-oriented setup script that checks or recreates `.venv`, installs
CAMELS dependencies and editable extras, optionally installs demo drivers, and
verifies that CAMELS can be imported. It is a local development helper, not a
CAMELS runtime feature.

## `nomad_camels/bluesky_handling/builder_helper_functions.py`

### Lines 220 and 237: link GUI plots to Browser Plot callbacks

When generating a protocol with Show plot in browser enabled, attach the
created Plotly callback to its corresponding 1D or 2D CAMELS plot widget.
This lets the GUI clear or update the matching Browser Plot for the same run.
