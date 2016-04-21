#!/usr/bin/env python

# wget http://bottlepy.org/bottle.py
# ... or ... pip install bottle
from bottle import get, request, run, static_file, HTTPResponse
import StringIO
import os

firmware_root = '.'

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

@get('/ota')
def ota():

    headers = request.headers
    for k in headers:
        print k, '=', headers[k]

    # TODO: check free space vs .bin file on disk and refuse

    try:
        device, firmware, have_version, want_version = headers.get('X-Esp8266-Version', None).split('=')
    except:
        print "Can't find X-Esp8266-Version in headers"
        return HTTPResponse(status=403, body="Not permitted")

    print "Homie firmware=%s, have=%s, want=%s on device=%s" % (firmware, have_version, want_version, device)

    # h-sensor/h-sensor-1.0.3.bin
    binary = "%s/%s/%s-%s.bin" % (firmware_root, firmware, firmware, want_version)

    if os.path.exists(binary):
        print "Return OTA firmware %s" % (binary)
        return static_file(binary, root='.')

    print "%s not found; returning 403" % binary
    return HTTPResponse(status=403, body="Firmware not found")

run(host='0.0.0.0', port=9080, debug=True)
