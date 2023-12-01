# Run IOCs with procServ

```{note}
It is best-practice to **always** run your IOCs using procServ as it you to run IOC without using active terminals that shut off the IOC when they are closed (by accident). 
```

You can use **procServ** to run IOCs in the background while still having access to them via `ssh`. You can also configure your IOC to automatically start when the host UNIX machine is turned on.

This guide is for setting up procServ on a Linux-Server.
It is assumed you already have installed EPICS and created a IOC that you now want to run (in the background).

## Step 1: Install procServ

To install procServ, simply run `sudo apt install procserv` and also install the suggested package telnet via `sudo apt install telnet`.

## Step 2: Starting an IOC via procServ

To start an IOC via procServ, ssh to the server and `cd` to the IOC's boot directory.

The command to start could look like this:

```
procServ -n "IOCname" -i ^D^C 20000 ./st.cmd
```

- `"IOCname"` should be replaced with a descriptive name of the IOC.
- `-i ^D^C"` blocks certain chars from being processed by the IOC. the `^` means control character, so `^C` disables `Ctrl + C`. This is useful to prevent the connected client from shutting down the IOC, since the IOC should not be terminated on its own, instead the entire procServ instance should be ended via `Ctrl + X`.
- `20000` specifies the telnet port, choose whatever is not used already.

For more commands and their explanation, see [this documentation](https://linux.die.net/man/1/procserv).

By default, this procServ instance will automatically restart the IOC. To change this, connect to the procServ instance and press `Ctrl + T` to cycle through the autorestart options.

To end the procServ instance and therefor the IOC, turn off autorestart and then pres `Ctrl + X`. By pressing `Ctrl + T` again or with `Ctrl + R`, the procServ instance and thereby the IOC will restart, which is useful if the IOC was changed and a reload was in order.

## Step 3: Connection to the procServ/IOC

To connect to the IOC, run the following (example) command:

```
ssh -t <user>@<procservhost> telnet localhost 20000
```

Replace `<user>` with the username of the server defined in `<procservhost>`, for example `epics@myprocserv`.
The port, `20000`, should be replaced with whatever port was chosen during the IOC boot.