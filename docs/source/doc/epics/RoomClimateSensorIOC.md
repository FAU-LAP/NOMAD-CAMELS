# How To Connect EPICS with an Arduino Nano that reads Room Climate info via a BME280-Sensor

## Arduino Setup

After physically setting up the Arduino, write the Code so that the Arduino responds with an HTML-Page
to a GET-Request. In this case, as the Ethernet-Library, `<UIPEthernet.h>` is needed, since the Nano Ethernet Shield V1.0
uses a ENC28J60 network module and the standard library does not support that module. Note that this library already includes `<SPI.h>`.

```{cpp}
#include <UIPEthernet.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
Adafruit_BME280 bme;

//choose a MAC-address you know is not in use in your network
//be aware that the two lowest bits of the first hex do have a meaning
//the lowest bit defines multicast (1) or unicast (0)
//the second lowest bit should always be 1, since
//that means the address is locally administered (otherwise, you shouldn't set it here)
byte mac[] = { 0x02, 0x4c, 0x41, 0x50, 0x00, 0x01 };

//defines the port, 80 is standard for HTML
EthernetServer server(80);
```

the void setup() should start a Serial-Connection for possible USB readouts and the server
```{cpp}
void setup() {
	//Set Baud-Rate
	Serial.begin(9600);
	
	//wait for the Serial to start
	while (!Serial) {
		;
	}

	//Server-Startup with DCHP
	Ethernet.begin(mac);
	delay(500);

	server.begin();
	//print IP to Serial
	Serial.println(Ethernet.localIP());

	//give the server some time to start
	delay(1000);

	//BME280-Sensor Startup
	bme.begin(0x76);
}
```

as already written, the void loop should sends back an HTML-Page with the sensor values


```{cpp}
void loop() {
	EthernetClient client = server.available();
	if (client) {
		
		Serial.print("neuer Client: ");
		Serial.println(client.remoteIP());
		// an http request ends with a blank line
		boolean currentLineIsBlank = true;
		while (client.connected()) {
			if (client.available()) {
				char c = client.read();

				if (c == '\n' && currentLineIsBlank) {
					// send a standard http response header
					client.println("HTTP/1.0 200 OK");
					client.println("Content-Type: text/html");
					client.println();
					
					//HTML-Tags
					client.println("<!DOCTYPE HTML>");
					client.println("<html>");

					// ein meta refresh tag, refresht den browser alle 5 Sekunden:
					client.println("<meta http-equiv=\"refresh\" content=\"5\">");

					//client.print("<font face=\"Arial\"><h1>LAP ClimateSensor V0.1</h1><br>");

					//temperature in degrees Celsius
					client.print("Tc = ");
					float tC = bme.readTemperature();
					client.print(tC);
					client.println("<br>");

					//temperature in Kelvin
					tC = tC + 273.15;
					client.print("Tk = ");
					client.print(tC);
					client.println("<br>");
					
					//relative Humidity in %
					client.print("H = ");
					client.print(bme.readHumidity());
					client.println("<br>");

					//Pressure in Pascal
					client.print("P = ");
					client.print(bme.readPressure());

					//HTML-Tags
					client.println("</html>");
					break;
				}
				
				//this is to check if the GET-Request is finished
				if (c == '\n') {

					currentLineIsBlank = true;
				} else if (c != '\r') {

					currentLineIsBlank = false;
				}
			}
		}

		// give the client time, to receive the data
		delay(250);

		// close the connection
		client.stop();
		Serial.println(F("Verbindung geschlossen."));
	}
}
```


```{attention}
This code reads the sensor on every HTTP GET-Request. Therefor, if two sources simultaneously ask vor values, they will get different results.
So if, for example, an EPICS-IOC and a logger both request values, they will always differ, although by a small amount. 
```

## EPICS

This guide assumes you got basic EPICS set up and running. See [here](new_ioc.md) to do this.\
Also needed are StreamDevice ([their Github-Page](https://github.com/paulscherrerinstitute/StreamDevice)) and asyn, also [from GitHub](https://github.com/epics-modules/asyn)

In Essence, this [FAIRmat-guide](https://op.fhi.mpg.de/projects/fairmat-task-d5-configurable-data-acquisition-system/wiki/add-new-serial-connection-to-ioc-example-asynserial) covers the procedure already, there are just minor adjustments needed.

### Step 2

Add the following configuration to `<TOP>/iocBoot/ioc*/st.cmd`

```
drvAsynIPPortConfigure("LAP1","*Arduino-Address*:*Port* HTTP")
```
Example:
```
drvAsynIPPortConfigure("LAP1","lap.physik.nat.fau.de:80 HTTP")
```

you need to actually load the `.db` being created in [Step 4](step_four)

```
dbLoadRecords("db/??.db", "PORT = LAP1")
```

replace `??` with the chosen name for the `.db`

### Step 3

Add the required `.dbd` to `<TOP>/*App/src/Makefile`
```
XXX += drvAsynIPPort.dbd
```

(step_four)=
### Step 4

Create a `.db` and `.proto` in `<TOP>/*App/Db/`

The `.db` includes the (in this case 4) records.
To minimize the amount of connections needed to the Arduino, instead of all records requesting the entire HMTL-Page,
only the first record scans the HTML-Page every x seconds while the other records use I/O event scanning (for an explanation read this [GitHub-Page](https://paulscherrerinstitute.github.io/StreamDevice/processing.html#iointr))

The `.db` should look like this (with `??` replaced by a chosen name).
The `readTc`, `readTk`, etc. can also be chosen at will, they just need to be the same as the ones chosen in the `.proto`

`PINI` forces the record to immediately initialize on startup. Otherwise, for a SCAN-value of lets say 10 minutes, the first 10 minutes all values would be 0.

Setting `EGU` to the unit the record provides and `PREC` to the precision (amount of decimal digits) makes it easier to later log the values.

```
record(ai, ??:readTc)
{
        field (DESC, "Read Temperature in degrees Celsius")
        field (DTYP, "stream")
        field (INP, "@??.proto readTc $(PORT)")
        field (SCAN, "1 second")
        field (PINI, "1")
        field (EGU, "Celsius")
        field (PREC, 2)
}

record(ai, ??:readTk)
{
        field (DESC, "Read Temperature in Kelvin")
        field (DTYP, "stream")
        field (INP, "@??.proto readTk $(PORT)")
        field (SCAN, "I/O Intr")
        field (EGU, "Kelvin")
        field (PREC, 2)
}

record(ai, ??:readH)
{
        field (DESC, "Read Relative Humidity in Percent")
        field (DTYP, "stream")
        field (INP, "@??.proto readH $(PORT)")
        field (SCAN, "I/O Intr")
        field (EGU, "%")
        field (PREC, 2)
}

record(ai, ??:readP)
{
        field (DESC, "Read Pressure in Pascal")
        field (DTYP, "stream")
        field (INP, "@??.proto readP $(PORT)")
        field (SCAN, "I/O Intr")
        field (EGU, "Pascal")
        field (PREC, 2)
}
```

The `.proto` should include certain parameters at the top.
The ones used are explained [here](https://paulscherrerinstitute.github.io/StreamDevice/protocol.html#sysvar).

Since only `readTc` actually scans, it is the only one needed to send a GET-Request, while the other functions receive the same value, i.e. the HTML-Page.
For the `in` parameter, it is required to filter for the value actually needed. These might change depending on the HMTL-Page received.
To do this, the code scans and discards everything via `%*` and then stops that at the *identifier*, i.e. what is written right before the value that the function is supposed to look up.
For all records to process correctly, each function needs to read every value. This seems to be a quirk of StreamDevice.
Therefor, look for all values needed, but only actually save the one needed while discarding the others with `*`.
Lastly, the InTerminator should be set to where to stop reading. Since here, the HTML-Page gets read to the end, the easiest way is to stop on the `</html>` tag, since that will always be at the end of the page.
For the HMTL-Page created with this Arduino code, the following `.proto` can be used.

For some more explanation, see [here](https://paulscherrerinstitute.github.io/StreamDevice/tipsandtricks.html#web).

```
ReplyTimeout = 2000;
ReadTimeout = 1000;
OutTerminator = " \r\n\r\n";
InTerminator = "</html>";

readTc
{
        extrainput = ignore;
        out "GET ";
        in "%*/Tc = /%f%*/Tk = /%*f%*/H = /%*f%*/P = /%*f";
}

readTk
{
        in "%*/Tc = /%*f%*/Tk = /%f%*/H = /%*f%*/P = /%*f";
}

readH
{
        in "%*/Tc = /%*f%*/Tk = /%*f%*/H = /%f%*/P = /%*f";
}

readP
{
        in "%*/Tc = /%*f%*/Tk = /%*f%*/H = /%*f%*/P = /%f";
}
```

