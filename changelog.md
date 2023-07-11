# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.1.0](https://github.com/FAU-LAP/NOMAD-CAMELS/releases/tag/0.1.0) - 2023-07-11

<small>[Compare with first commit](https://github.com/FAU-LAP/NOMAD-CAMELS/compare/2c4b074c5232da26faf69756d940487b35b39419...0.1.0)</small>


## [v0.1.8](https://github.com/FAU-LAP/NOMAD-CAMELS/releases/tag/v0.1.8) - 2023-04-14

<small>[Compare with first commit](https://github.com/FAU-LAP/NOMAD-CAMELS/compare/d9f5b9051c351031b9c3e5fad624e304aa3fc22f...v0.1.8)</small>

### Added

- added working exe download link from repo ([2a22472](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/2a224721acd5b81ed1a0ec28c5104b402c148792) by A-D-Fuchs).
- adding logo ([c86729a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/c86729a2e28ca1b573d82aa79f2ed7d63d78603a) by Jo-Leh).
- added process_read_function, which passes the read value to the function and continues with the reult of the function (allows parsing of very long string data or any array data) ([8d672b4](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8d672b4e715b672beb4781ccbf6e358d81c95d19) by A-D-Fuchs).
- Added the labels dictionary to allow any string to be set as label for auto generated configs ([9d49c6c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9d49c6c370792fc76587bfcd8ea64702dcecee4c) by A-D-Fuchs).
- added inits ([15d01a9](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/15d01a9267d1721356de30fa13f4534e145da738) by Jo-Leh).
- added ui for stage_control ([df247eb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/df247eb5b87a75500c60ee6867dab847cd81812f) by Jo-Leh).
- added the set_value loopstep with popup ([04e4652](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/04e4652f3733b405760ffbe26ffa17e51116a270) by Jo-Leh).
- added test file for device communication with pyvisa ([6868109](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6868109391880add21162b581fcd5efb786f461a) by A-D-Fuchs).
- added K237 SweepMe driver ([a900b2f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a900b2fcdd20b5ae459e987b813185a1c155e9c1) by A-D-Fuchs).
- Added k237.py and ophyd files ([ed8233f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/ed8233f72b6c27ae4abcb3e3b1341e0172cf6b3d) by A-D-Fuchs).
- added set variable loop step, setting channels now also with variables ([221780e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/221780e5db0735af67f4e6a0e878429eb10adab7) by Jo-Leh).
- added turn on / off for pid ([b412faf](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b412faf6c8b1f47b084f9fa3a6abce519a129ef5) by Jo-Leh).
- added e5270b test file that runs a bluesky plan ([069914b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/069914ba1f5dc189d7d5727058fde08361a06802) by A-D-Fuchs).
- added units to channels (shown as attributes in hdf5), and possibility for metadata of channel in general ([fee59d1](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/fee59d1385d4d71d4dc67d00845d7df18ba0003c) by Jo-Leh).
- added py-script to file and context menu to channels_check_table ([557b568](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/557b568bfff72ac0b8fda027328f9192ec0ccd4b) by Jo-Leh).
- added idn to k2000, updated channel_check_table for renaming devices ([7245ef4](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/7245ef47a0a8689b632267c6952d7ae978b05ed3) by Jo-Leh).
- added overview of protocol to hdf5 ([a6cc1f6](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a6cc1f689cccd86ffc901937c41b3d9f2e6ffcfd) by Jo-Leh).
- added possible description for protocol, improved hdf5-export towards NX ([23171d8](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/23171d8661b853f68e68104d3e7f8eacdfdc608e) by Jo-Leh).
- added possibility to split triggering and reading of devices (usefull e.g. for spectra) ([0e23bd8](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/0e23bd821c6f510dc1afb315cf1ec23956eaf6ce) by Jo-Leh).
- added search function to read_channels step ([d213231](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d2132314e5251c19f47ab7ca33d9617614182be6) by Jo-Leh).
- added demo device, improved some fits ([a71beff](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a71beff50a891ea7019735eea51716689b5ed577) by Jo-Leh).
- added visa-signal, started with agilent b2912a ([a23fa7b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a23fa7be3e6629d5408db24f7509861d3a8caaf5) by Jo-Leh).
- added possibility of description for both devices and protocol-steps ([217cf35](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/217cf356550d3dc01b765ed2a2cf7ccb7e8b6c0b) by Jo-Leh).
- added documentation + bug report links for "help" ([809b11c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/809b11c1e58c0c5a144d5fea27d8be07cda05836) by Jo-Leh).
- added 2D-plot, fixed bugs in other plots ([90e546a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/90e546a942c15c59ff74f2e79ce9b5598194262a) by Jo-Leh).
- added current value-list to possible plot types ([5a379f7](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5a379f79b7aa1b935441bd67215096c24f48d0e6) by Jo-Leh).
- added possibility to run addons, like manual control of PID outside of a bluesky-script ([f3c466c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f3c466ca36d6f1e94e94396e5ac4ac4dd192bc78) by Jo-Leh).
- added USB-serial as communication type, added voltcraft_pps power supply ([e8bcb49](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e8bcb4937da2f81e3386e44cf44d1f0d54895650) by Jo-Leh).
- added custom daq device ([b306cb3](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b306cb3db8b399370dc5f80cfe5aaca806190b17) by Jo-Leh).
- added automatic configuration for databroker ([e6fac6e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e6fac6e9f1e60e61a51505e0be9d2ef775dcb40d) by Jo-Leh).
- added bruker magnet ([7f00c8f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/7f00c8f6682279dacb9d508d0464cd8b42f4ceb9) by Jo-Leh).
- added lmfit to requirements ([728de34](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/728de345bdb5ecd123bb52e8177ea814a382983a) by Jo-Leh).
- added loopstep to re-configure device during running protocol ([7387101](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/7387101889b8e46887f456772ae4c5a47c6081eb) by Jo-Leh).
- added a gradient-descent loopstep, updated some other things for that, added scipy to requirements, fixed error of config and settings ([2ebc564](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/2ebc5645f587a4ed15a5de67530e0725d78b6fae) by Jo-Leh).
- added possibility to have device in a different IOC ([a830d72](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a830d7293bec5e6aadc81e43c15f50288d3aeaf3) by Jo-Leh).
- added prompt loopstep, started subprotocol-step ([baa09ea](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/baa09ea40fe91361ac9701acdd549040a1334ed6) by Jo-Leh).
- added evaluation for loopsteps and variables into metadata ([a5e558b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a5e558b9cb2edd1654096fa77f00dcd253f37576) by Jo-Leh).
- Added GUI widget for B2912 ([3d56cbd](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/3d56cbd5dd1665ffc41e1e5498e9711503cd5306) by A-D-Fuchs).
- added usage of substitution-files for IOCs ([1778a2e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/1778a2ef573a54ebb81c9632ccdc3bf1d28adc09) by Jo-Leh).
- added readme as .docx for better readability ([f7ab5e7](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f7ab5e7d718a0d370770b7fca948b603b58c6b80) by A-D-Fuchs).
- Added Word file of rad me with better readability ([d12a639](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d12a63967d5dc413d64236a71c729853da792223) by A-D-Fuchs).
- Added install readme README_Install.txt ([8d53996](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8d53996c09df12b1d0926675c6593b1d098341e5) by A-D-Fuchs).
- added opening a protocol and usage of the "del" button to remove loopsteps ([6e3f576](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6e3f5769cce0be7b0cfe5f15fa69afea5050cc8f) by Jo-Leh).
- added status of running IOC, can now write to IOC ([803a9cb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/803a9cbefb5409287bca914f262c068538b556ff) by Jo-Leh).
- Added an if-step, updated the export towards nexus ([f9dfdf0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f9dfdf082865ef7c8e6270d69074dac62e21ba48) by Jo-Leh).
- added custom name for devices ([a066b52](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a066b52b0fdf3e1ca0db4b02da8f3150e78797b9) by Jo-Leh).
- added more documentation, updated mapping dictionary for nexus ([94bcb6d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/94bcb6def483b23f369f6add86edba724e516550) by Jo-Leh).
- added documentation to for and while loops ([f1e58a1](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f1e58a1025dd9de22a2396f22c671b8fca44ff36) by Jo-Leh).
- added doc for EPICS_handling ([ea8bb43](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/ea8bb434a9312fe9abc9cde5ad1b96b3f3db8889) by Jo-Leh).
- added documentation to frontpanels ([878f98c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/878f98c574161893dbba00459821a5af68cdd270) by Jo-Leh).
- added documentation for bluesky_handling ([993897b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/993897b4f947e3326ed8d54b0dd128df1cb88465) by Jo-Leh).
- added documentation for the modules under utility ([8a74282](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8a74282702ca92e647e52cf26b47c4d0aa91460e) by Jo-Leh).
- added further documentation ([2d0f9c9](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/2d0f9c9148b90eff6274a4a9e451073886540b37) by Jo-Leh).
- added documentation in the load_save_functions ([4f764f5](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4f764f5d3ec446797d25bb54ca25e14621559c36) by Jo-Leh).
- added documentation to the mainapp ([eb129c2](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/eb129c2306845e8d60217569a01fe55169c47107) by Jo-Leh).
- added loop step "wait" ([64ae09b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/64ae09b2af8f2e418c09bbc45e4dac8308d38e98) by Jo-Leh).
- added while loop, improved variable-box ([d16fa35](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d16fa35c2037d3e9c56d31dfc6e818776368558b) by Jo-Leh).
- added some docstrings ([6a4d917](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6a4d91721d007875a6c087f05186cfe7c46b75e5) by Jo-Leh).
- added a few devices and a rudimentary PID-controller ([a275fd0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a275fd021f6758f22a640efc1a8080cbe31bf060) by Jo-Leh).
- added first basics for handling bluesky-plans, starting to rework the device_class and adding functionality ([cf742db](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/cf742db5cc9acb8ed0fcdda9d1848a8987233889) by Jo-Leh).
- added copy / paste for loopsteps ([cb4acd3](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/cb4acd341269b91fbf520ef81f50b31e95b72327) by Jo-Leh).
- Added basic functionality for loop_steps ([654a5c7](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/654a5c75bcfe0749aae08677209740d3e6fc04de) by Jo-Leh).
- added docstrings ([54088ec](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/54088ecb4b391b9d3ef51a6b5d93c95d2bf8d5f8) by Jo-Leh).
- added first version of device-adding, rudementary ioc works ([f57c85e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f57c85e3c5f47c93af801e8e93d3440d75bd61eb) by Jo-Leh).
- added neccessary files ([9c553a8](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9c553a8a267bf671777e9009b0e39881adaf7a09) by Jo-Leh).

### Fixed

- fixed imports and built 0.1.6 version ([681b9ad](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/681b9ad4974377f0d72e3f3e26e4e6dde0e51ba9) by A-D-Fuchs).
- fixed backwards compatibility for material theme ([2b86edb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/2b86edb7a92cb78bcead14e5025ceb6a819520b2) by Jo-Leh).
- fixed some bugs with pyside6 ([550c6f5](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/550c6f55ed7f064ced1307add3318e6fb9018f1c) by Jo-Leh).
- fixed gap_burner and while loop ([5a03290](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5a032905c01fdfcd68f91d7f56e3b11bbf9565c7) by Jo-Leh).
- fixed error in saving when using a value-list "plot" ([9bdb804](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9bdb8041f4c1c2a49251db8dd0d1cc16840e18c7) by Jo-Leh).
- fixed channel 2 and 3 code. Everything should work now ([4f5a8ee](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4f5a8ee343181dde84c11857766a033e159b67cd) by A-D-Fuchs).
- fixed a bug with the fitting, when using more than one fit, added more documentation ([69cee31](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/69cee31e44539610d2d6aee02a1b80d008f1264d) by Jo-Leh).
- fixed bug in starting addons ([dbfe727](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/dbfe727dffe083a2cfda1ead71e9837c89c77cd4) by Jo-Leh).
- fixed typos of commands ([06ad4d9](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/06ad4d946afd4f47669a98d5ed6ec7ef35b38fd7) by A-D-Fuchs).
- fixed time weight for for-loop, added option to not play camel-sound ([6b39804](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6b398046bd83a2355d8cc01c900845f5927d941b) by Jo-Leh).
- fixed protocols not running outside the GUI anymore ([95da297](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/95da29799a5adadb63e27685809702e0260bcee8) by Jo-Leh).
- fixed bug for read-channels ([d4444af](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d4444af23d37fd9272087b54e531c21763872a90) by Jo-Leh).
- fixed not remembering last active user / sample ([17fea3d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/17fea3d0590b6d063d6028c43967a3d8e7fea5c6) by Jo-Leh).
- fixed bug for voltcraft ([e00ba62](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e00ba62c88622d1ecd9c62a0e193d2f02bf0c30e) by Jo-Leh).
- fixed bug regarding compliance in b2912 ([88a8b00](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/88a8b000a84a615668cace5d3c1158c3cf8412f3) by Jo-Leh).
- fixed bug with name of fit parameters in datafile ([6f15366](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6f1536676122f32ac06416ade825b484e118ba4d) by Jo-Leh).
- fixed bug that did not allow to have several protocols run after another ([f92ae9d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f92ae9dc79859c2d0ea5f8871415f511e6b10391) by Jo-Leh).
- fixed error with wrong labels for plot ([78e7cae](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/78e7caee35161243180145f87ebb7d4e3af472c9) by Jo-Leh).
- fixed issue for plots in simple_sweep, added empty line for each loopstep ([4bd05d4](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4bd05d480935e575371294b88d6e53ab4cfb3113) by Jo-Leh).
- fixed bug in chmod for usb-tty ([5589afb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5589afb1e82bb99555c2cff7b7415bcad2d6d43d) by Jo-Leh).
- fixed bug in DAQ_custom_device, removed some unnecessary files ([c9274e1](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/c9274e18b3c3392e627c0b3cf2546f9ec053735c) by Jo-Leh).
- fixed issue when not plotting anything ([5989703](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5989703b69cc880021eaf4d7fdf68a9f9c4bfb24) by Jo-Leh).
- fixed the issue with a new plot-table ([7cdb6cb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/7cdb6cb4ee95dc519b770c232789a437e75041ea) by Jo-Leh).
- fixed loading issues for for-loop and set-channels ([e4844df](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e4844dff2ed3142edfb12621c8f36d3c27b1d4dd) by Jo-Leh).
- fixed issue when running the protocol, set channels should work, as well as for loop ([71af765](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/71af765007d7874c58b00dbbff02c5bb67cf534d) by Jo-Leh).

### Changed

- changed all CAMELS references and string to nomad-camels or variants ([096d50c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/096d50cf0dcd7bad860aabca2c3cb170bfdd415b) by A-D-Fuchs).
- Changed the readme ([5327086](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5327086aa723cbc052e9844511235e410c8216d3) by A-D-Fuchs).
- Changed the "appdata path" from CAMELS to NOMAD-CAMELS' ([3e2be84](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/3e2be845fb93a694b2ef49a5d9a13e7118177697) by A-D-Fuchs).
- Changed settings combo boxes ([141a784](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/141a78454d5f9d519c4e526a6cacfea0c22d05ce) by A-D-Fuchs).
- changes to e5270 and comments ([5c73e22](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5c73e2280ebbb82c57c060db8bbbd8e1af56bb15) by A-D-Fuchs).
- changed default name of entry-group in h5-file to start-time of run ([7f4ab99](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/7f4ab999512ceb7a7e4a5469474cefd82e645c80) by Jo-Leh).
- changed two presets for meas / devies to only one for all ([8c0e717](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8c0e7170bbd43d3ef98e49dbc29aec53d702d423) by Jo-Leh).
- changed readme.md to the readme_install ([cfb4ec6](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/cfb4ec6c8c01901470c1c33337384d3b39707870) by A-D-Fuchs).
- changed name to CAMELS, added dark-mode ([8fd92f0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8fd92f016e11ee9f2dff198fb60f60ac0427df9e) by Jo-Leh).

### Removed

- removed old daq and visa signal files ([6514fcb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6514fcb8ff8a99ed91c10a0e341ddbe85eb4c8fa) by Jo-Leh).
- removed k237_visa_test.py to clean up the driver ([62a533a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/62a533a4a11d74891a5db75687896ef9a954c1fc) by A-D-Fuchs).
- removed unnecessary files ([f2a1dcb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f2a1dcb54cbdf0f42b93045488dcf540f4d21be6) by Jo-Leh).
- removed print from e5270 ([d0de451](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d0de451cd8f8403be7b56881210817ba1e3f1dca) by Jo-Leh).
- removed ophyd_fit from LiveFit_Eva, since it was no longer needed ([e221f9a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e221f9ad87b85ad12c7c1ac446aed171d466de93) by Jo-Leh).
- removed unneccessary images ([ccbcda1](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/ccbcda1b6b76210cdd4aa9e08c3c57ae3ebcfab7) by Jo-Leh).
- removed junk word file ([f4d258d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f4d258d741344b3dfc43eedc4be0bedfb29c4385) by A-D-Fuchs).

### Merged

- Merge branch 'development' ([b874aed](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b874aed420710cf478d388ea47b186b602f17465) by Jo-Leh).
- Merge branch 'development' of https://github.com/FAU-LAP/CAMELS into development ([3f26ba0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/3f26ba0b9cb1190c02fbe5b0450c26f72e4319ee) by Jo-Leh).
- Merge pull request #27 from FAU-LAP/pyside_switch ([5c7217d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5c7217dadaf0e28335fa978f83c26520e1ddad1f) by Jo-Leh).
- Merge pull request #26 from FAU-LAP/stage_control ([8f0f4ec](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8f0f4ec38e9101f4c133ad8e442780dded5e38db) by Jo-Leh).
- Merge pull request #25 from FAU-LAP/development ([ca4f4ff](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/ca4f4ff8f45eb01b1cec96c75162b933670585a0) by Jo-Leh).
- Merge pull request #24 from FAU-LAP/new_device_management ([1eaef47](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/1eaef47933f32e6d5a4ae68c07f7b7207267b36e) by Jo-Leh).
- Merge branch 'stage_control' of https://github.com/FAU-LAP/CAMELS into development ([04fa287](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/04fa287e496d64f842123fa8fe91a7fb67051ec9) by Jo-Leh).
- Merge pull request #22 from FAU-LAP/new_device_management ([4985b93](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4985b9380cfd4ca6ed331f07e23f51e9ea23ed0d) by Jo-Leh).
- Merge pull request #21 from FAU-LAP/k237_dev ([88fc1b8](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/88fc1b883aa83f918ce89e3052560a817ebb444a) by Jo-Leh).
- Merge branch 'main' into k237_dev ([f2d2321](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f2d2321c24c0c9f8cb01a669497d3165bb93a933) by Jo-Leh).
- Merge pull request #19 from FAU-LAP/development ([a345be4](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a345be467d46f9498373ab744cb9eb1327917057) by A-D-Fuchs).
- Merge pull request #18 from FAU-LAP/gap_burner_4_CAMELS ([e95139d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e95139de6dfa83540fb45e7afbcaad962835729f) by Jo-Leh).
- Merge pull request #17 from FAU-LAP/gap_burner_4_CAMELS ([b6f3664](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b6f366434c580b71ee7b3b794d750baec5f1b88e) by Jo-Leh).
- Merge branch 'k237_dev' of https://github.com/FAU-LAP/CAMELS into k237_dev ([b780cf6](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b780cf672e00508231a416f289a4c9186a5fd281) by A-D-Fuchs).
- Merge branch 'gap_burner_4_CAMELS' of https://github.com/FAU-LAP/CAMELS into gap_burner_4_CAMELS ([eae1f49](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/eae1f498626dcc219a86ae879d090523ebdf4ab2) by Jo-Leh).
- Merge pull request #16 from FAU-LAP/main ([eb1daa7](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/eb1daa7e22d0b12aae690b3b1162191303ae06e1) by Jo-Leh).
- Merge pull request #14 from FAU-LAP/e5270b_dev ([b1da37a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b1da37a305acbfef70aa184c8aa8dc7475a2777a) by Jo-Leh).
- Merge pull request #13 from FAU-LAP/development ([f74d81a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f74d81a2db933b025a3aae43162fc2b31425fc98) by Jo-Leh).
- Merge pull request #12 from FAU-LAP/main ([55f91d8](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/55f91d884cd223c8734477c568e55ccc612355b8) by Jo-Leh).
- Merge pull request #11 from FAU-LAP/threading_development ([bbd3aa1](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/bbd3aa125a8a98962486d1a5edc8202594834a5c) by Jo-Leh).
- Merge pull request #9 from FAU-LAP/measurement_developement ([c2fe75f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/c2fe75fae5b1fce56cd3cb94c9b56b1c98413348) by Jo-Leh).
- Merge pull request #8 from FAU-LAP/main ([f5850af](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f5850afb4c4e2cb382ce107143042bc2cd0a00f3) by Jo-Leh).
- Merge branch 'main' of https://github.com/FAU-LAP/CAMELS ([dcd8340](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/dcd834018b70c3c8498c96a9b166711fe7a0bea2) by Jo-Leh).
- Merge pull request #7 from FAU-LAP/device_developement ([f99d6ae](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f99d6ae231f81a3695a9b7c88b3ee67864af0a11) by Jo-Leh).
- Merge pull request #6 from FAU-LAP/main ([f6d269e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f6d269ed74c0461a669dde76ec94e932912eed55) by Jo-Leh).
- Merge pull request #5 from FAU-LAP/measurement_developement ([af50825](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/af508252d1571bd580636a3660bce433276ec177) by Jo-Leh).
- Merge pull request #4 from FAU-LAP/measurement_developement ([cbfedc1](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/cbfedc165b60a17cafba5c7f86830ac44749e636) by Jo-Leh).
- Merge pull request #3 from FAU-LAP/measurement_developement ([a80fd00](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a80fd003438bcd6cc1ec8fcecdb459e607e2474c) by Jo-Leh).

### Documented

- docs test ([629f0c3](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/629f0c34bafb2e8fc7d4a39e3d30ad3341cc6321) by Jo-Leh).
