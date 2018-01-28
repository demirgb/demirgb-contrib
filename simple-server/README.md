# DemiRGB Simple Server

## About

In contrast to the main DemiRGB firmware — which has a full HTTP server, web-based network setup, light state fading, demos, etc — this firmware was designed to be as simple as possible.  Send a UDP packet, set the R/G/B.

The server and client were written in about an hour, as a proof of concept and alternative to the full firmware.  They use JTLVI for the messages, a simple binary TLV message format.

## Installation

Starting from a fresh MicroPython installation on the ESP8266, configure networking, e.g.:

```python
import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('<your ESSID>', '<your password>')
```

Write `server.py` to the filesystem, and configure `boot.py` to do e.g.:

```python
import server
server.main()
```

When the ESP8266 is rebooted, it should do a short test startup sequence, lighting up red, green and blue each for one second.

## Usage

`client.py` accepts a target hostname/IP and either an HTML hex value:

```
./client.py 10.9.8.133 '#ff0000'  # Set to full red
```

Or a set of three numbers (red, green, blue), with a range of 0 through 1023 (10 bits) for greater granularity than the hex representation's 8 bits:

```
./client.py 10.9.8.133 843 138 833  # Set to a purple-ish
```


