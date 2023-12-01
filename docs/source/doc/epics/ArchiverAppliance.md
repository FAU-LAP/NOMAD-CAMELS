# How To Setup the EPICS Archiver Appliance
This guide is for setting up a site specific install of the EPICS Archiver Appliance (for their GitHub see [here](https://slacmshankar.github.io/epicsarchiver_docs/index.html))

## Step 1: Install Debian
The first step is to setup a Server running Debian 11.7 ("Bullseye") (the install script currently does **not** support a higher version of Debian).
The official download link can be found [on the official Debian website](https://www.debian.org/releases/bullseye/debian-installer/).
For 'normal' PCs running a x86-64 instruction set, download the full DVD set `amd64`. 
Next, use a software to create a bootable USB drive like [Rufus](https://rufus.ie) by selecting your USB drive and the freshly downloaded `debian-11.7.0-amd64-DVD-1.iso`. 
Contrary to the [official installation guide](https://wiki.debian.org/DebianInstall), `ISO` writing mode works just as well and is therefor recommended.

During the installation, make sure to check the box to install the SSH server and webserver, so you dont have to do that later.
As username, choose something like archiver.

## Step 2: Debian Settings
The first step after installation is to add the user to sudoers.
for this, open up a terminal and switch to root with `su - root`, open the sudoers file with `sudo nano /etc/sudoers` and add the username to the file under `root  ALL=(ALL:ALL) ALL` with the line `<username> ALL=(ALL:ALL) ALL`, replacing `<username>` with the name chosen during installation .

Next, to get `apt update` working, changes need to be made to `/etc/apt/sources.list`.
Either delete or comment the third line (the one starting with `cdrom:`), otherwise Debian expects every package to be installed and updated from a DVD.
Lastly, run `sudo apt update` and `sudo apt upgrade` just to be sure the system is up to date.

## Step 3: EPICS Archiver Appliance
To get started, install the packages required for this installation, so:
```
sudo apt install default-jdk
sudo apt install python3
sudo apt install python3-requests
```
Be sure to install the Java JDK, *not* JRE.

To run the site specific installation described in the archiver appliance [here](https://slacmshankar.github.io/epicsarchiver_docs/installguide.html),
firstly run `git clone https://github.com/jeonghanlee/epicsarchiverap-env`, then follow the installation guide for Debian 10/11 described [on their GitHub](https://github.com/jeonghanlee/epicsarchiverap-env).



## Step 4: Settings
Go to the installation folder `cd /opt/epicsarchiverap` and change the permissions of `appliances.xml` via `sudo chmod 777 appliances.xml` to be able to change it.
In the file, you need to change all but one `localhost` with the hostname of the server, which is whatever the command `hostname -f` returns.
Now, open the file, e.g. via `nano appliances.xml` and change `localhost` to the server hostname everywhere expect the `<retrieval_url>` line.
If this is the second installation, it might be necessary to change `<identity>appliance0</identity>` to `<identity>appliance1</identity>`.

The complete file should look like this (with `webserver.uni-erlangen.de` replaced with the server hostname)
```
<?xml version='1.0' encoding='utf-8'?>
<!--
  Took the contents from single\_machine\_install.sh, and modified
  them according to our configuration.
-->
<appliances>
   <appliance>
     <identity>appliance0</identity>
     <cluster_inetport>webserver.uni-erlangen.de:16670</cluster_inetport>
     <mgmt_url>http://webserver.uni-erlangen.de:17665/mgmt/bpl</mgmt_url>
     <engine_url>http://webserver.uni-erlangen.de:17666/engine/bpl</engine_url>
     <etl_url>http://webserver.uni-erlangen.de:17667/etl/bpl</etl_url>
     <retrieval_url>http://localhost:17668/retrieval/bpl</retrieval_url>
     <data_retrieval_url>http://webserver.uni-erlangen.de:17668/retrieval</data_retrieval_url>
   </appliance>
</appliances>
```

## Step 5: (Auto-)Start Archiver Appliance
To start the Archiver, run `sudo systemctl start epicsarchiverap.service`, to stop it `sudo systemctl stop epicsarchiverap.service`. To restart, run `sudo systemctl restart epicsarchiverap.service`.

After (re-)startin the server, wait around 10 seconds for the server to start up, which should then be reachable via `http://<<hostname>>:17665/mgmt/ui/index.html` 

To set the Archiver to autostart on system boot, run `sudo systemctl enable epicsarchiverap.service`, to remove the Archiver from autostart run `sudo systemctl disable epicsarchiverap.service` instead.

## (Optional) Step 6: Auto Login on Server Restart
Its possible to set Debian to automatically login on (re-)boot. This might be desirable for user comfort, since its only necessary to press the Power Button of the Server for the Archiver Appliance to get going again. On the other hand, this might introduce a security risk, since the Server will automatically log into a normally password protected account.

To do it though, open a terminal and run `sudo nano /etc/gdm3/daemon.conf`, uncomment or set the line `AutomaticLoginEnable = 1`, and set `AutomaticLogin = <username>`, where <username> is the user which runs the Archiver Appliance.

## Conclusion
This should leave you with a functioning Archiver Appliance, which should be reachable from within the local network via `http://<IPADRESS/HOSTNAME>:17665/mgmt/ui/index.html`.
