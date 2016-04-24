#include <Homie.h>

#define FW_NAME "example-firmware"
#define FW_VERSION "1.0.5"

/* Magic sequence for Autodetectable Binary Upload */
const char *__FLAGGED_FW_NAME = "\xbf\x84\xe4\x13\x54" FW_NAME "\x93\x44\x6b\xa7\x75";
const char *__FLAGGED_FW_VERSION = "\x6a\x3f\x3e\x0e\xe1" FW_VERSION "\xb0\x30\x48\xd4\x1a";
/* End of magic sequence for Autodetectable Binary Upload */

void setup()
{
	Homie.setFirmware(FW_NAME, FW_VERSION);
	Homie.setup();
}

void loop()
{
	Homie.loop();
}
