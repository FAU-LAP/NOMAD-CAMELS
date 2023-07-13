# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## Unreleased

<small>[Compare with latest](https://github.com/FAU-LAP/NOMAD-CAMELS/compare/v0.1.8...HEAD)</small>

### Added

- added documentation to wait loop step ([a605684](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a6056848b1b93377c7cfd74145616fa507d249cb) by Jo-Leh).
- added fixture that should be able to accept failing messageboxes, so the tests don't run forever ([18995fb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/18995fb88fd3cd9142e9592f52bd05936efa7edf) by Jo-Leh).
- added variables from fits for nd-sweep, documented simple_sweep ([29abc1f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/29abc1f5a5a2f3b6bb3262c21fbbe6f6c1a32c7f) by Jo-Leh).
- added timeout for visa_device ([6120592](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6120592bfab42c763dc6f7a4a133cc6ca6afbd3f) by Jo-Leh).
- added documentation for change_sequence ([387e844](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/387e844b130e6112f9e11afe1ceed1c4cea1a164) by Jo-Leh).
- added documentation to the protocol builder ([4bcbb89](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4bcbb896d97529ffa4b3b16c57ff63d382a49f57) by Jo-Leh).
- added documentation for bluesky_handling/make_catalog ([a647842](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a6478426122eb3cd0dea1e8bc7ba5b2340236370) by Jo-Leh).
- added new builds ([7e9709e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/7e9709e78bc4b6f25a3609be17f380ab095ceecc) by A-D-Fuchs).
- added documentation to evaluation_helper ([74716a6](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/74716a60ebc7adb857f14b194ee231661317a2e7) by Jo-Leh).
- added documentation to custom_function_signal ([9c3b24d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9c3b24d1e5ad9ffb6bf538b8660472f621901df8) by Jo-Leh).
- added documentation to builder_helper_functions ([883e30b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/883e30bf8941679a3dca4486bd8d22c9051c9eb8) by Jo-Leh).
- added autosave before run features ([d4c6ec1](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d4c6ec1dec275dc357b0a4ee0babb46c4bc692dc) by Jo-Leh).
- added first working version for the VISA driver builder ([a50a9bd](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a50a9bdcead37c16d99e4787d4dbba599fcc2e8e) by Jo-Leh).
- added a tooltip for the metadata of channels ([d5b98da](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d5b98dabfdddd0861fecf9b8a9515be0c28021fb) by Jo-Leh).
- added functionality to export data from databroker in CAMELS-style ([459e4ab](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/459e4ab4572157e3b9dacce81d58fb47f990b6aa) by Jo-Leh).
- added question to restart on first install, built 0.1.22 ([6f24e7c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6f24e7c0e0e1db963f635bbd55bac1a7b8bb49e3) by A-D-Fuchs).
- added a simple export run function, should be added to GUI at some point ([b0c4962](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b0c4962532ccb0e26c91cb100b37e55bb6991317) by Jo-Leh).
- added read string from channel ([8a55b0d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8a55b0d85fd7be19d1ae0918ac73122015db666a) by A-D-Fuchs).
- added installation using anaconda ([73e161c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/73e161c4412cceeddd72587db6ba6c5164505d89) by A-D-Fuchs).
- added grand_parent ([6ab5e7a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6ab5e7ace5ec831271f9a65acfabd3eace797fef) by A-D-Fuchs).
- added small bug addition ([27f6bb0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/27f6bb08b2788bcde934cd05672be5e73c608442) by A-D-Fuchs).
- added test for simple sweep, with plot and fit ([aecf891](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/aecf8912fe877953755b17426a87ca74ba8cee05) by Jo-Leh).
- added test for while loop, fixed test for trigger ([9ed438e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9ed438e4a27ffb2fdfc2703bbc4b877f2c4031a5) by Jo-Leh).
- added test for trigger ([4e76b19](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4e76b195f00ad73daac3ff184e40419eac425ffa) by Jo-Leh).
- added set_variables to if test, now a test for two steps ([a6c232b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a6c232bb0745fc06a2fe88d0d1ebffb1b75e939a) by Jo-Leh).
- added code signing guide ([ef39332](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/ef3933205f6d3b836013db6f308ff266006296a6) by A-D-Fuchs).
- added test for If ([5626401](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/56264018e142d5b96c7980261c607b7ff66c220e) by Jo-Leh).
- added test for gradient descent ([799d37e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/799d37e1eef0b0cdfb712280f85444f0087e057c) by Jo-Leh).
- added for loop test ([a98ab07](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a98ab074c5a8d19cdf771dac5b3c2f460d65aae9) by Jo-Leh).
- added test for set channels ([8abc865](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8abc865b529760bdba56718f72e1f445756f4c63) by Jo-Leh).
- added test for change device config step ([8687c5b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8687c5b1b482b54ac60fd51ec658c916faa7dcd2) by Jo-Leh).
- added fallback temp databroker catalog ([b7076e4](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b7076e4372bf66869c9260acd85cf70ba3049c1d) by Jo-Leh).
- added fixed section ([1219a7b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/1219a7b6645a6a82ae4ff70c1c4b0221d26826d1) by A-D-Fuchs).
- added children true ([376abd9](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/376abd957ca8f1bcae20c413104f097356cf9b82) by A-D-Fuchs).
- added working next and back buttons and small fixes ([9cc949e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9cc949ebe597fb111aabdf2408e41568be99ba5f) by A-D-Fuchs).
- added plot info to quick guide ([d9598c2](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d9598c2959f96f275714a999e18d0b958bed8558) by A-D-Fuchs).
- added first test, maybe with CI to run automatically on github ([9e1ede6](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9e1ede61813ede61741857e21b974922a3c4d350) by Jo-Leh).
- added blue highlight for light mode ([d182139](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d182139e8f34f15f625e7c25a168d95cafc4911d) by A-D-Fuchs).
- added new instruments ([63d4380](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/63d4380e1c44a9dc9d08030e127003a33e0b1719) by A-D-Fuchs).
- added automated build and upload guide ([c34cdea](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/c34cdea937717f4d8e15d7d6c9c680588be81cd6) by A-D-Fuchs).
- added more descriptive code headlines ([f9e434a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f9e434abe125a904b805194099f36e760b64b31e) by A-D-Fuchs).
- added the functionality to update camels ([a92d9a3](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a92d9a3d54a2556beddb5b1bb090b49fe27d26e1) by Jo-Leh).
- added table of contents ([e1a9cdf](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e1a9cdf01d7c2b5c938da61c567a99dacea4161e) by A-D-Fuchs).
- added docu for changing camels installer ([7edba43](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/7edba43a9ed9260fe0d05abe1e59cfbab91822c6) by A-D-Fuchs).
- added python version warning ([e315b27](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e315b27ecf8d5db431073c1e8cd4cf376ab58e8e) by A-D-Fuchs).
- added HDF5 viewer info ([0be1f1a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/0be1f1a7d3e7f6567d347cd33cd123bdfc8c0298) by A-D-Fuchs).
- added script to read hdf5 file to dictionary ([a1673ec](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a1673ec3f8818c49e540ff48fab5c51ffe7256be) by A-D-Fuchs).
- added more headers to k237 docu ([65701d8](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/65701d8f25dff75c08c4947afad07bef2fc6c011) by A-D-Fuchs).
- added data to k237 docu ([9c49d57](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9c49d5753d3f8e703f48d4fada0b74aa2a2fd4e4) by A-D-Fuchs).
- added docu for k237 ([1655435](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/1655435604fe89ba23bddc2d75fde12eb86d9211) by A-D-Fuchs).
- added pip install twine ([526adf7](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/526adf7fba926ea6b908b343e69716bf07a1fde5) by A-D-Fuchs).
- added process_read_function to VISA_signal_read class. takes the read val and converts it with an arbitrary function given to process_read_function ([36aa7cd](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/36aa7cd992a5b83ca05d1294a408a6e2dbe01de1) by A-D-Fuchs).
- added repo link to camels_drivers ([e2bfd94](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e2bfd945128be2878a37a32c1dc1afc5c7278f66) by A-D-Fuchs).
- added in-page navigation ([a2c9c51](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a2c9c512271b1383b1c4dbe18bd89738c07f2b71) by A-D-Fuchs).
- added in-page navigation test ([5ae8da0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5ae8da0e5c9839b1abf08d7a0a30b1aa76a7df67) by A-D-Fuchs).
- added gem rough ([b849f69](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b849f69d574c84f7b03be9ae941fcae86834dd37) by A-D-Fuchs).
- added  syntax highlights ([c253b13](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/c253b13c21dc1ad748cd58013198ee5b3431b3b5) by A-D-Fuchs).
- added instrument drivers docu and changed nav_order ([14537d8](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/14537d8dbbaf8b5cf5c0977b8b9a8dcbf893021d) by A-D-Fuchs).
- added nomad_camels to packagename start ([c60bc8f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/c60bc8f03b399b3c1f707275b503b84885c10089) by A-D-Fuchs).
- added visa_signal.py to blueksy_handeling folder ([a3a6156](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a3a615631cc2f3cb7a521337a217233622529f6d) by A-D-Fuchs).
- added dist/nomad* to twine upload ([e457bc0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e457bc021d5bb21fa2073726f49ad859aee9f915) by A-D-Fuchs).
- added correct twine upload ([fa130c7](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/fa130c779be84e98d70ae38a0d29afecd589c56b) by A-D-Fuchs).
- added syntax highlights for code blocks , all as bash ([dbbf895](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/dbbf89546875520b6a129b8bfbc41db6106a01fe) by A-D-Fuchs).
- added syntax highlights for code blocks ([9f9fe98](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9f9fe9827767983c7492c28e503cbf9deb72e234) by A-D-Fuchs).
- Added .md file on how to upload to pypi ([5919bc6](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5919bc675e771c43ccd38446b181068a1d4b7c7c) by A-D-Fuchs).
- Added information install fails because of pyenv PATH missing ([99eb63c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/99eb63ca0492e7f3b71f449a56046f7d543c010e) by A-D-Fuchs).
- Added information about uninstalling ([0f8e0f0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/0f8e0f06220693043fbf7ef62242009f11fb92c7) by A-D-Fuchs).
- Added more information as well as simple debugging ([76a155a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/76a155a9f3365d4147f7d69dd6b08e332ff2cc3b) by A-D-Fuchs).

### Fixed

- fixed CAMELS update string ([b6e1745](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b6e1745a2c2ba12e492dd6488f4de2510433ddc4) by A-D-Fuchs).
- fixed icon for driver builders ([8521a5e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/8521a5e7baccb996ded44ce3e196e9a6c3d8a7f7) by Jo-Leh).
- fixed issue of connection settings not saved and not used ([64f2598](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/64f259839a131078a173385fc89e5a651567930b) by Jo-Leh).
- fixed simple sweep test ([0f0556a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/0f0556a5043c3fb3e2dabdf1208ac988d64d77da) by Jo-Leh).
- fixed that plots that should be on the right axis show on the left axis ([d783546](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d783546b669c24036215b864912db103af86ce80) by Jo-Leh).
- fixed downloaded instrument drivers showing as "local" ([26fc500](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/26fc500fb2e1753d99984debcb11caef85fe0763) by Jo-Leh).
- Fixed the issue of not all plots and windows closing when called ([fe8518b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/fe8518b90864e15d94bbd300d84b19d83d20d564) by Jo-Leh).
- fixed broken local driver import ([2a5b9de](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/2a5b9de74c7cb8bd3c67866113140bc028d8071b) by A-D-Fuchs).
- fixed back to top ([343a652](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/343a6520d8d2ae36217ada8ccaacf3bef7b2c9aa) by A-D-Fuchs).
- fixed link ([aa1c43f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/aa1c43f5dd34f3a5468c874e6b3a8d445d434eb4) by A-D-Fuchs).
- fix for next buttons to new pages ([56d2c91](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/56d2c913f8eabff122c47734ac51f33698996ddf) by A-D-Fuchs).
- fixed writing python environment to hdf5 ([277df64](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/277df64dc3ff24b0c225d6e12031363a180c2edd) by A-D-Fuchs).
- fixed simple config combo boxes. now saves the set values ([9b1e9a4](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9b1e9a42e184deaccf0c6748eb2e168243331539) by A-D-Fuchs).
- fixed missing nomad string at beginning ([6bda973](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6bda973e1b6c0400636f2d83079ce32c56af2f80) by A-D-Fuchs).
- fixed the creation of automatic simple config. fixed labeling of widgets ([1f6ceea](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/1f6ceeacd8177004e73d3b7dc636b37d70b60c85) by A-D-Fuchs).
- fixed uninstall and added returncode check on subprocces call ([57a5060](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/57a506039ffe206cc03799b8465c7bebc20fce24) by A-D-Fuchs).
- fixed typo ([7ab219c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/7ab219c71de9f97be2c415e46866f03c1437587f) by A-D-Fuchs).
- fixed merge conf and added working unicode emoji ([9de3a98](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9de3a98e3df29d6608030980d9041e74ba538856) by A-D-Fuchs).

### Changed

- changed update to pypi from testpypi ([32acd44](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/32acd443452b68cf2364a5aac744fb5ab7b68cc1) by A-D-Fuchs).
- changed tests to "demo_instrument" as well ([42bf635](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/42bf63504ea4200d2fffce8f114d1ffb52498372) by Jo-Leh).
- changed read process_read_function priority ([874ae65](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/874ae65a44b581fec66be5831af16272c6ba4e56) by A-D-Fuchs).
- changed encoding to utf8 for most (all?) opened files ([03b6905](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/03b6905863360c66a9ae07a65c14c069aa1c9f10) by Jo-Leh).
- changed pypi upload section ([6a491c9](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6a491c94f9d4aa8b49c53af0e5584a507e005840) by A-D-Fuchs).
- changed numbering headers ([4a400e2](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4a400e2e648c417ff52e7ffa39cf9353621aee3e) by A-D-Fuchs).
- changed instrument driver creation guide. added more detail and usage of template files ([867d952](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/867d9523eecda337bbf28b514641a40cf563b3e9) by A-D-Fuchs).
- changed driver docu, added link to template and restructured ([a3714ea](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a3714ea5817ce8814bc62a391bd02986a117c817) by A-D-Fuchs).
- changes ([34686cf](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/34686cff96db80dfec750ab6f3cc6d215c8b01c3) by A-D-Fuchs).
- changed numbering ([56e7d48](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/56e7d4821234feb11729a32c7f9d14c5146eca37) by A-D-Fuchs).
- changed instrument installer ([e4cbfeb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e4cbfeb7a232df8d9950f6645abbbcc121b1c2f6) by A-D-Fuchs).
- changed folder startswith from camels_driver to nomad_camels_driver ([fd4d8cb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/fd4d8cb660c4948eb9c68c5385218e496003a2a5) by A-D-Fuchs).
- changed header ([3aa12a0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/3aa12a056a81f614c156adea09076e2986ee0460) by A-D-Fuchs).
- changed folder structure ([9dcfa0d](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9dcfa0d069d71e3179296ed6d1ee78bc6aeaf241) by A-D-Fuchs).
- Changed label of read freq of stage control ([d15a124](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d15a1244f9270463765f558a26ab86f58378bd52) by A-D-Fuchs).
- changes to quick guide ([9cb7abb](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9cb7abb5ef4d2b5daffbff20c76c197068bff2e7) by A-D-Fuchs).
- changed the way themes are applied. Fixed dark on dark highlight for Fusion theme ([b3911fc](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b3911fca30bdfcf296f6a462d0707facc4380089) by A-D-Fuchs).
- changed title of page ([49ccf22](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/49ccf22ebbc53e5c5fd63d8d6585a443d45b86c6) by A-D-Fuchs).
- changed plus button to smaller size ([5ce2846](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/5ce2846018d485d4d7db6a6bdda43c2b477a7baf) by A-D-Fuchs).
- changed python version number ([da0e528](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/da0e52829966dc1178556ca37e0835cf43a152d0) by A-D-Fuchs).
- changed packages.txt ([00276c1](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/00276c11a22db663c61f6764647be1b7a4210389) by A-D-Fuchs).
- changed default branch to main without directory ([3353e1c](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/3353e1c79c1bb6cb6409525f9aff4bda52e3ba87) by A-D-Fuchs).
- changed heading order ([30ad80b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/30ad80b6e5d60fefa0425cf939b62a753e0d8b32) by A-D-Fuchs).
- Changed default driver list location to https://github.com/FAU-LAP/CAMELS_drivers ([e9b6791](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e9b6791bd7548a57deb6b1d1f111bae3dcbacd9d) by A-D-Fuchs).
- changed device install to testPyPi ([edba5f2](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/edba5f237ee2d80f2a5caabd19e82539bc37a403) by A-D-Fuchs).
- changed contact email address ([6c5ee2a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/6c5ee2ae8de5cbff09f9d481f02b6be42054bbea) by A-D-Fuchs).
- changed debug info ([b8c3a85](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b8c3a85d35ae98797c05c5c2ae2c4350a2b696bf) by A-D-Fuchs).

### Removed

- removed .egg folder ([4f01590](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4f015909655f7b4b64bf530e4343b15e473d6852) by A-D-Fuchs).
- removed windows classifier ([b1db9e7](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b1db9e78bf0207509b996119628d8f638b1408e5) by A-D-Fuchs).
- removed EPICS, also from instruments ([81f71d4](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/81f71d4b34a39184f9e3609ed4a1e963868144bf) by Jo-Leh).
- removed "insert operator" menu ([774563b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/774563bea9700327ff033264d0fd637e76d798ce) by Jo-Leh).
- removed unneccessary, improved check in epics builder ([83be41b](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/83be41b75c7fdcefe04c7be3636faefcafdbc099) by Jo-Leh).
- removed unneccessary .patch files? ([4fefc3a](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4fefc3a0df80608410758aa3880fbf2a2d09cab6) by Jo-Leh).
- removed toc ([d8123a8](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d8123a80e23d1bdaf16dc0ca72d2593e59c79182) by A-D-Fuchs).
- removed most cases of 'simply' ([f627d7e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/f627d7e363d0e65e4b3927f44e3b5e14692aee64) by A-D-Fuchs).
- removed a lot of unnecessary content ([986cdae](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/986cdae5941feadb925c359311bc88947d659ea9) by A-D-Fuchs).
- removed 0 from TOC ([2de56e7](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/2de56e74143cf36bfd5e0a2eda3c80847c455462) by A-D-Fuchs).
- removed single large quick start guide ([9586c08](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9586c0893f4f5232332863d5288a269f146ee7a2) by A-D-Fuchs).
- removed hard coded python 3.9.6 values with variable ([23653d0](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/23653d0a7c1f223f2e08fbde65d9187625e87e7b) by A-D-Fuchs).
- removed unneccessarry buttons if no instruments ([145a25e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/145a25e48f1c2ceb550236c93ca4375b89bf8b6a) by Jo-Leh).
- removed header text ([4c8be0f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/4c8be0f3fc50f9e2eae2dc59d19a86b91635db01) by A-D-Fuchs).

### Merged

- Merge branch 'development' of https://github.com/FAU-LAP/NOMAD-CAMELS into development ([e55f3b3](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/e55f3b325b6a1bf2d77a2b6969b3ba7699ed0cc7) by Jo-Leh).
- Merge branch 'development' of https://github.com/FAU-LAP/CAMELS into development ([d8de741](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/d8de741ff806f313ec6b1ae1556155dfcd908a5b) by A-D-Fuchs).
- Merge branch 'main' into development ([db1d5d9](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/db1d5d93bf33e70adc30860abfb12692892f6463) by Jo-Leh).
- Merge pull request #41 from FAU-LAP/instrument_revamp ([cdd16e5](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/cdd16e5815a2e7a22a09d63954a5b395dcff39ce) by Jo-Leh).
- Merge branch 'development' into instrument_revamp ([b0a04b9](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b0a04b90e2d395055022d74e54e937e049893259) by Jo-Leh).
- Merge pull request #37 from FAU-LAP/A-D-Fuchs-patch-1 ([bd5713f](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/bd5713fa0ebaa50069bbdb0f5c31bd921dc60c1e) by Jo-Leh).
- Merge pull request #35 from FAU-LAP/development ([678f72e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/678f72e4844eff4e38a557aafa50f703c9ac55fd) by A-D-Fuchs).
- Merge branch 'documentation' into development ([65d9971](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/65d99718930bbb032b2b3606a3e156f167c5fbf3) by Jo-Leh).
- Merge pull request #33 from FAU-LAP/testing ([b33a343](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/b33a34350436097a691d4b6cdf5a365800c6979c) by Jo-Leh).
- Merge pull request #30 from FAU-LAP/development ([a4e3044](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/a4e304467db514b7f8d1bbf31b917deedc53b585) by Jo-Leh).
- Merge branch 'documentation' of https://github.com/FAU-LAP/NOMAD-CAMELS into documentation ([3d69992](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/3d699926a8cabaee4e0a29bb1544be7148a18c60) by A-D-Fuchs).
- Merge branch 'documentation' of https://github.com/FAU-LAP/CAMELS into documentation ([9f8196e](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/9f8196e90badf194e53a1025f46686aae0aedc9d) by Jo-Leh).

### Documented

- documentation for gradient_descent ([8226771](https://github.com/FAU-LAP/NOMAD-CAMELS/commit/82267717c5a1744f877efac753a601bc968a63d3) by Jo-Leh).

<!-- insertion marker -->
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
