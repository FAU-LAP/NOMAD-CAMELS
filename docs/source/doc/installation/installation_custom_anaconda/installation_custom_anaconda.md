# Installation of CAMELS Using Anaconda

This How-to-guide will teach how to install CAMELS if you already have [Anaconda](https://www.anaconda.com/) installed on your machine or want to use Anaconda to install the Python environment needed for CAMELS.

This guide is also useful if `pyenv` does not work on your machine due to restrictions set by your facility (package-filters, rights-problems, etc.).

## 0. Anaconda Installation

Do this if you do not have Anaconda installed yet:

Download [Anaconda](https://www.anaconda.com/download) and [install](https://docs.anaconda.com/anaconda/install/).

## 1. Create Environment

After successfully installing Anaconda continue here:

Set up the correct Python environment for CAMELS using Anaconda. For this open the `Anaconda Prompt` terminal. 

Run 

```bash
conda create -y --name desertenv python=3.11.3 
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

## 2. Install CAMELS

Now run the following command to install CAMELS from PyPI.

```bash
pip install nomad-camels
```


```{note}
<a href="../../tutorials/quick_start.html" style="display: inline-block; padding: 12px 20px; background-color: #ffffff; color: #4CAF50; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px; margin: 10px 0; font-weight: bold; border: 4px solid #4CAF50">
    Getting Started
</a><br>
When you are done with the installation, get started with our guide. 
```

## 3. Run CAMELS

You can then run

```bash
nomad-camels
```

 or  

```bash
python -m nomad_camels
```

to start CAMELS.

If this does not work for you you can try this.
CAMELS is a python package that is saved under the python environment created above. Python packages are typically saved under the path:

```bash
/<python_env>/Lib/site-packages/<package_name>
``` 

so in our case when using Anaconda on Windows it will be something like

```bash
C:\Users\<User_Name>\AppData\Local\conda\conda\envs\desertenv\Lib\site-packages
```

You can find the save location of your packages using 

```bash
pip list -v
```

which lists all the paths to your packages.

Now go to the `nomad-camels` package 

```bash
cd C:\Users\<User_Name>\AppData\Local\conda\conda\envs\desertenv\Lib\site-packages\nomad-camels\
```

and run

```bash
python CAMELS_start.py
```

this starts CAMELS.
