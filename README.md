# homie-ota

This is a small OTA (Over the Air) "server" for the excellent [Homie-ESP8266][Homie] framework for ESP8266 modules. In addition to providing OTA over HTTP/HTTPS, homie-ota also provides device inventory and firmware management with an explicitly retro-style Web interface (the KISS layout reminds us of the fact we're dealing with $4 IoT devices ...)

![homie-ota](assets/jmbp-2708.png)

homie-ota contains a built-in HTTP server powered by [Bottle]; this is the bit that a Homie device talks to in order to obtain OTA firmware. On the other hand, homie-ota connects to your MQTT broker in order to obtain an inventory of Homie devices (current status (`$online`), firmware (`$fwname`) and firmware version (`$fwversion`), device name (`$name`), etc. These values are collected by homie-ota and stored in a JSON data structure in the file system.

## Features

* OTA firmware server for [Homie] devices.
* Upload new firmware to the firmware store.
* Trigger OTA firmware update by MQTT publish to a Homie device
* Logging
* View device details

## Firmwares

Firmware files are uploaded into homie-ota via its Web interface, and they must contain the magic tokens in order for homie-ota to correctly process them. (See below for how to create those.) All firmware files are stored in the `OTA_FIRMWARE_ROOT` directory as `<name>@<version>`, with _name_ being the name of the firmware and _version_ it's semantic version number (e.g. `dual-relay@1.0.5`).

homie-ota makes it easy to deploy a different firmware onto an ESP8266 device: simply select the firmware you want on the device and queue the OTA request. As per the [Homie Convention][convention], this request is published over MQTT, however note that homie-ota does **not** currently publish this message retained which means, that if the device is currently not online, it will miss an update. (This is by design to avoid OTA loops.)

## Installation

Obtain homie-ota and its [requirements](requirements.txt). Copy the exmple configuration file to `homie-ota.ini` and adjust, creating the `OTA_FIRMWARE_ROOT` firmware directory if it doesn't yet exist.

Launch `homie-ota.py`.

Configure your [Homie] devices to actually use homie-ota by providing the appropriate settings in [their configuration](https://github.com/marvinroger/homie-esp8266/blob/master/docs/5.-JSON-configuration-file.md):

![Homie config](assets/jmbp-2687.png)

![ESP8266 Arduino](assets/jmbp-2686.png)


## Preparing the firmware

In order to use the Autodetectable Binary Upload™, your Homie sketch should contain a magic expression in it as shown in the [example sketch](assets/example.ino). When you're ready, compile the binary. To upload it: under the `Sketch` menu in the Arduino IDE, select `Export compiled Binary`; the binary `.bin` will be placed in the sketch's directory, and you upload that file to homie-ota; it will detect the firmware name and version, store it into the correct directory, and make it available in the list of upgradable firmware files.

```
Firmware from ed-relay.ino.d1_mini.bin uploaded as firmwares/dual-relay/dual-relay-1.0.2.bin
```


  [Homie]: https://github.com/marvinroger/homie-esp8266
  [Bottle]: http://bottlepy.org/docs/dev/index.html
  [convention]: https://github.com/marvinroger/homie
