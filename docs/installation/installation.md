---
layout: default
title: Installation
has_children: true
nav_order: 1
---


# CAMELS Installation

As NOMAD-CAMELS (from now on only 'CAMELS') is written in python it requires a working python environment to run properly.
The [installer.exe](#1-using-the-camels_installerexe) takes care of all of this for you.

With the correct python version (tested for 3.11.3 or newer) CAMELS can simply be installed using `pip`
(but this is not recommended! Try and use the installer if you are on Windows):
```bash
pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nomad-camels
```
> &#9888; You can try and see if CAMELS works for any python version that is 3.9.6 or higher but this might fail!

**This will install CAMELS in to your python environment but does not create all necessary folders (under %localappdata% for example).**\
It installs CAMELS as a python package into your package library (`\*env*\Lib\site-packages\NOMAD-CAMELS\`, where `*env*` is the path to the python environment used with the `pip install` command).


[comment]: <> (# Installing on Windows)

If you do not have python installed on your machine or a clean python environment you have two options:
1. [Using the installer](./installation_installer.html) (**RECOMENDED**, Windows only)
2. Custom installation for Windows, macOS, and UNIX



<p style="text-align:left;">
  <span style="color: grey;">
  <a href="../index.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="./installation_installer.html">Next &rarr;</a><br>
  </span>
</p>
