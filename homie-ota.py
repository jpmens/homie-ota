#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = 'Jan-Piet Mens <jpmens()gmail.com> & Ben Jones'
__copyright__ = 'Copyright 2016 Jan-Piet Mens'

# wget http://bottlepy.org/bottle.py
# ... or ... pip install bottle
from bottle import get, route, request, run, static_file, HTTPResponse, template
import paho.mqtt.client as paho   # pip install paho-mqtt
import StringIO
import os
import sys
import logging
import ConfigParser
import atexit
from persist import PersistentDict
import json
import fileinput
import time
import re


# Script name (without extension) used for config/logfile names
APPNAME = os.path.splitext(os.path.basename(__file__))[0]
INIFILE = os.getenv('INIFILE', APPNAME + '.ini')
LOGFILE = os.getenv('LOGFILE', APPNAME + '.log')

# Read the config file
config = ConfigParser.RawConfigParser()
config.read(INIFILE)

# Use ConfigParser to pick out the settings
DEBUG = config.getboolean("global", "DEBUG")

OTA_HOST = config.get("global", "OTA_HOST")
OTA_PORT = config.getint("global", "OTA_PORT")
OTA_ENDPOINT = config.get("global", "OTA_ENDPOINT")
OTA_FIRMWARE_ROOT = config.get("global", "OTA_FIRMWARE_ROOT")

MQTT_HOST = config.get("mqtt", "MQTT_HOST")
MQTT_PORT = config.getint("mqtt", "MQTT_PORT")
MQTT_USERNAME = None
MQTT_PASSWORD = None
MQTT_CAFILE = None
try:
    MQTT_USERNAME = config.get("mqtt", "MQTT_USERNAME")
except:
    pass
try:
    MQTT_PASSWORD = config.get("mqtt", "MQTT_PASSWORD")
except:
    pass
try:
    MQTT_CAFILE = config.get("mqtt", "MQTT_CAFILE")
except:
    pass
MQTT_SENSOR_PREFIX = config.get("mqtt", "MQTT_SENSOR_PREFIX")


# Initialise logging
LOGFORMAT = '%(asctime)-15s %(levelname)-5s %(message)s'

if DEBUG:
    logging.basicConfig(filename=LOGFILE,
                        level=logging.DEBUG,
                        format=LOGFORMAT)
else:
    logging.basicConfig(filename=LOGFILE,
                        level=logging.INFO,
                        format=LOGFORMAT)

logging.info("Starting " + APPNAME)
logging.info("INFO MODE")
logging.debug("DEBUG MODE")
logging.debug("INIFILE = %s" % INIFILE)

# MQTT client
mqttc = paho.Client("%s-%d" % (APPNAME, os.getpid()), clean_session=True, userdata=None, protocol=paho.MQTTv311)

# Persisted inventory store
db = PersistentDict(os.path.join(OTA_FIRMWARE_ROOT, 'inventory.json'), 'c', format='json')


def exitus():
    db.sync()
    db.close()
    logging.debug("CIAO")

def uptime(seconds=0):
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    seconds = int(seconds)

    days    = int( seconds / DAY )
    hours   = int( ( seconds % DAY ) / HOUR )
    minutes = int( ( seconds % HOUR ) / MINUTE )
    seconds = int( seconds % MINUTE )

    string = ""
    if days > 0:
        string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "

    string = string + "%d:%02d:%02d" % (hours, minutes, seconds)

    return string


@get('/blurb')
def blurb():
    text =  """Homie OTA server running.
    OTA endpoint is: http://{host}:{port}/{endpoint}
    Firmware root is {fwroot}\n""".format(host=OTA_HOST,
            port=OTA_PORT, endpoint=OTA_ENDPOINT, fwroot=OTA_FIRMWARE_ROOT)

    for root, dirs, files in os.walk(OTA_FIRMWARE_ROOT):
        path = root.split('/')
        text = text + "\t%s %s\n" % ((len(path) - 1) * '--', os.path.basename(root))
        for file in files:
            if file[0] == '.':
                continue
            text = text + "\t\t%s %s\n" % (len(path) * '---', file)

    return text

@get('/firmware')
def firmware():
    fw = scan_firmware()
    print json.dumps(fw, indent=4)
    return template('templates/firmware', fw=fw)

@get('/')
def inventory():
    fw = scan_firmware()
    return template('templates/inventory', db=db, fw=fw)

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@get('/<filename:re:.*\.png>')
def png(filename):
    return static_file(filename, root='static/img')

@get('/<filename:re:.*\.js>')
def javascript(filename):
    return static_file(filename, root='static/js')

@get('/log')
def showlog():
    logdata = open(LOGFILE, "r").read()
    return template('templates/log', data=logdata)

@route('/upload', method='POST')
def upload():
    '''Accept an uploaded, compiled binary sketch and obtain the firmware's
       name and version from the magic described in
       https://github.com/jpmens/homie-ota/issues/1
       Store the binary firmware into a corresponding subdirectory in firmwares/
       '''

    upload = request.files.upload

    if upload and upload.file:
        firmware_binary = upload.file.read()
        filename = upload.filename

        regex_name = re.compile(b"\xbf\x84\xe4\x13\x54(.+)\x93\x44\x6b\xa7\x75")
        regex_version = re.compile(b"\x6a\x3f\x3e\x0e\xe1(.+)\xb0\x30\x48\xd4\x1a")

        regex_name_result = regex_name.search(firmware_binary)
        regex_version_result = regex_version.search(firmware_binary)

        if not regex_name_result or not regex_version_result:
            resp = "No valid firmware in %s" % filename
            logging.info(resp)
            return resp

        fwname = regex_name_result.group(1)
        fwversion = regex_version_result.group(1)

        firmware_path = os.path.join(OTA_FIRMWARE_ROOT, fwname)
        fwfile = fwname + '-' + fwversion + '.bin'
        firmware_file = os.path.join(firmware_path, fwfile)

        if not os.path.exists(firmware_path):
            os.mkdir(firmware_path)

        try:
            f = open(firmware_file, "wb")
            f.write(firmware_binary)
            f.close()
        except Exception, e:
            resp = "Cannot write %s: %s" % (firmware_file, str(e))
            logging.info(resp)
            return resp

        resp = "Firmware from %s uploaded as %s" % (filename, firmware_file)
        logging.info(resp)
        return resp

    return "File is missing"

@route('/update', method='POST')
def update():
    device = request.forms.get('device')
    firmware = request.forms.get('firmware')
    version = request.forms.get('version')

    # we store the selected firmware and version in our device db
    # so when the OTA request arrives we can validate and also
    # allow firmware overrides (i.e. change from fw1 -> fw2)
    db[device]['otafirmware'] = firmware
    db[device]['otaversion'] = version

    topic = "%s/%s/$ota" % (MQTT_SENSOR_PREFIX, device)
    (res, mid) =  mqttc.publish(topic, payload=version , qos=1, retain=False)

    info = "OTA request sent to device %s for update to %s v%s" % (device, firmware, version)
    logging.info(info)

    return info

def scan_firmware():
    fw = {}
    for firmware in os.listdir(OTA_FIRMWARE_ROOT):
        firmware_path = os.path.join(OTA_FIRMWARE_ROOT, firmware)
        if not os.path.isdir(firmware_path):
            continue

        for filename in os.listdir(firmware_path):
            firmware_file = os.path.join(firmware_path, filename)
            if not os.path.isfile(firmware_file):
                continue

            if firmware_file not in fw:
                fw[firmware_file] = {}

            # parse the version number (<fwname>-x.x.x.bin)
            version = filename[len(firmware) + 1:-4]

            fw[firmware_file]['firmware'] = firmware
            fw[firmware_file]['filename'] = filename
            fw[firmware_file]['version'] = version

            stat = os.stat(firmware_file)
            fw[firmware_file]['size'] = stat.st_size

    return fw

# X-Esp8266-Ap-Mac = 1A:FE:34:CF:3A:07
# X-Esp8266-Sta-Mac = 18:FE:34:CF:3A:07
# X-Esp8266-Free-Space = 684032
# X-Esp8266-Chip-Size = 4194304
# X-Esp8266-Mode = sketch
# Content-Length =
# X-Esp8266-Sdk-Version = 1.5.2(7eee54f4)
# Host = 192.168.1.130
# X-Esp8266-Sketch-Size = 360872
# Connection = close
# User-Agent = ESP8266-http-Update
# X-Esp8266-Version = cf3a07e0=h-sensor=1.0.1=1.0.2
# Content-Type = text/plain

@get(OTA_ENDPOINT)
def ota():

    headers = request.headers
    for k in headers:
        logging.debug(k + ' = ' + headers[k])

    # TODO: check free space vs .bin file on disk and refuse

    try:
        device, firmware_name, have_version, want_version = headers.get('X-Esp8266-Version', None).split('=')
    except:
        logging.warn("Can't find X-Esp8266-Version in headers; returning 403")
        return HTTPResponse(status=403, body="Not permitted")

    logging.info("Homie firmware=%s, have=%s, want=%s on device=%s" % (firmware_name, have_version, want_version, device))

    if not db[device]:
        logging.warn("OTA update request received for device %s which is not in our inventory" % (device))
        return HTTPResponse(status=403, body="Not permitted")

    if not db[device]['otafirmware'] or not db[device]['otaversion']:
        logging.warn("OTA update request received for device %s which has no current OTA update scheduled" % (device))
        return HTTPResponse(status=403, body="Not permitted")

    # TODO: ignore selected firmware and just attempt same-fw update
    #otafirmware = db[device]['otafirmware']
    #otaversion = db[device]['otaversion']
    otafirmware = firmware_name
    otaversion = want_version

    # <firmware_root>/<firmware_name>/<firmware_name-x.x.x.bin
    # e.g. './h-sensor/h-sensor-1.0.3.bin'
    firmware_path = "%s/%s" % (OTA_FIRMWARE_ROOT, otafirmware)
    binary = "%s-%s.bin" % (otafirmware, otaversion)
    binary_path = "%s/%s" % (firmware_path, binary)

    if not os.path.exists(binary_path):
        logging.warn("%s not found; returning 403" % (binary_path))
        return HTTPResponse(status=403, body="Firmware not found")

    logging.info("Return OTA firmware %s" % (binary_path))
    return static_file(binary, root=firmware_path)


def on_connect(mosq, userdata, rc):
    for suffix in [ '$localip', '$signal', '$uptime', '$name', '$online', '$fwname', '$fwversion' ]:
        mqttc.subscribe("%s/+/%s" % (MQTT_SENSOR_PREFIX, suffix), 0)

def on_message(mosq, userdata, msg):
    logging.debug("%s (qos=%s, r=%s) %s" % (msg.topic, str(msg.qos), msg.retain, str(msg.payload)))

    t = str(msg.topic)
    t = t[len(MQTT_SENSOR_PREFIX) + 1:]      # remove MQTT_SENSOR_PREFIX/ from begining of topic
    
    device, key = t.split('/')
    key = key[1:]                       # remove '$'
    
    if device not in db:
        db[device] = {}
    db[device][key] = str(msg.payload)

    if key == 'uptime':
        db[device]['human_uptime'] = uptime( db[device].get('uptime', 0) )

def on_disconnect(mosq, userdata, rc):
    reasons = {
       '0' : 'Connection Accepted',
       '1' : 'Connection Refused: unacceptable protocol version',
       '2' : 'Connection Refused: identifier rejected',
       '3' : 'Connection Refused: server unavailable',
       '4' : 'Connection Refused: bad user name or password',
       '5' : 'Connection Refused: not authorized',
    }
    reason = reasons.get(rc, "code=%s" % rc)
    logging.debug("Disconnected: ", reason)

def on_log(mosq, userdata, level, string):
    logging.debug(string)

if __name__ == '__main__':

    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_message = on_message
    # mqttc.on_log = on_log

    if MQTT_CAFILE:
        mqttc.tls_set(MQTT_CAFILE)

    if MQTT_USERNAME:
        mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    logging.debug("Attempting connection to MQTT broker at %s:%d..." % (MQTT_HOST, MQTT_PORT))
    try:
        mqttc.connect(MQTT_HOST, MQTT_PORT, 60)
    except Exception, e:
        logging.error("Cannot connect to MQTT broker at %s:%d: %s" % (MQTT_HOST, MQTT_PORT, str(e)))
        sys.exit(2)

    mqttc.loop_start()

    atexit.register(exitus)

    try:
        run(host=OTA_HOST, port=OTA_PORT, debug=DEBUG)
    except KeyboardInterrupt:
        mqttc.loop_stop()
        mqttc.disconnect()
        sys.exit(0)
    except:
        raise
