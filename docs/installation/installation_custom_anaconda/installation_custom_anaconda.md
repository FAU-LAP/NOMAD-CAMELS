---
layout: default
title: How to install CAMELS using Anaconda
parent: Installation
nav_order: 2
---



<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

# How to install CAMELS using Anaconda
This How-to-guide will teach how to install CAMELS if you already have installed [Anaconda](https://www.anaconda.com/) on your machine or want to use Anaconda to install the python environment needed for CAMELS. 

This guide is also useful if `pyenv` does not work on your machine due to restrictions set by your facility (package-filters, rights-problems, etc.). 

## 1. Anaconda Installation
Download [Anaconda](https://www.anaconda.com/download) and install. 
## 2. Create Environment
Now set up the correct python environment for CAMELS using Anaconda. For this open the `Anaconda Prompt` terminal (use Windows search to find it). 

<p float="left">
  <img src="img.png" width="40%" />
</p>

Run 

```bash
conda create --name desertenv python=3.11.3 
```
and then activate the environment you just created using

```bash
activate desertenv
```
The beginning of a line in your terminal should look something like this  
```
(desertenv) C:\WINDOWS\system32> 
```
indicating that you are currently using the `desertenv` python environment.
## 3. Install CAMELS
Now run the following command to install CAMELS from PyPi (currently from testPyPi, this will be changed in the future).

```bash
pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nomad-camels
```

## 4. Run CAMELS
CAMELS is a python package that is saved under the python environment created above. Python packages are typically saved under the path:
```
/<python_env>/Lib/site-packages/<package_name>
``` 
so in our case when using Anaconda on Windows it will be something like

```
C:\Users\<User_Name>\AppData\Local\conda\conda\envs\desertenv\Lib\site-packages
```

You can find the save location of your packages using 

```bash
pip list -v
```
which lists all the paths to your packages.

Now go to the `nomad-camels` package 
```
cd C:\Users\<User_Name>\AppData\Local\conda\conda\envs\desertenv\Lib\site-packages\nomad-camels\
```
and run 
```bash
python CAMELS_start.py
```
this starts CAMELS.

> &#9888; You might receive a `CATALOG ERROR`.\
> If you do, then re-run the command `python CAMELS_start.py`. This should fix the error.
