
```
 _  _   ___   __  __  ___  ___           ___  ___  __  __  ___  _     ___ 
| \| | / _ \ |  \/  |/   \|   \   ___   / __|/   \|  \/  || __|| |   / __|
| .  || (_) || |\/| || - || |) | |___| | (__ | - || |\/| || _| | |__ \__ \
|_|\_| \___/ |_|  |_||_|_||___/         \___||_|_||_|  |_||___||____||___/
```
# NOMAD-CAMELS
## Configurable Application for Measurements, Experiments and Laboratory-Systems  

NOMAD-CAMELS is a configurable measurement software, targeted towards the requirements of experimental solid-state physics. Here many experiments utilize a multitude of measurement devices used in dynamically changing setups. CAMELS will allow to define instrument control and measurement protocols using a graphical user interface (GUI). This provides a low entry threshold enabling the creation of new measurement protocols without programming knowledge or a deeper understanding of device communication. The GUI generates python code that interfaces with instruments and allows users to modify the code for specific applications and implementations of arbitrary devices if necessary. Even large-scale, distributed systems can be implemented. CAMELS is well suited to generate FAIR-compliant output data. Nexus standards, immediate NOMAD integration and hence a FAIRmat compliant data pipeline can be readily implemented.


## Documentation

For more information and documentation visit [this page](https://fau-lap.github.io/NOMAD-CAMELS/).

# Changelog

## 0.1.5
Fixed the 'Update CAMELS' tool.\
Renamed input and output to read and set in the 'Update CAMELS' tool.\
Small fix to the VISA device builder.

## 0.1.4
Added a timeout setting to all VISA instruments. Setting the timeout determines how long the instrument waits after sending a command before raising a timeout exception

## 0.1.3
First stable and working release

## 0.1.0 to 0.1.2 
&#9888; Broken releases due to minor bugs that were fixed in 0.1.3
