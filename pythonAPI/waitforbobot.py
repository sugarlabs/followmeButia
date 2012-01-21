#!/usr/bin/python
###########################################
# This program is part of butiaAPI Toolkit
# License: GPL
#
# wait a litles seconds for bobot to connect correctly to butia
#
##########################################


import butiaAPI
import time


butiabot = butiaAPI.robot()

print "waiting for bobot..."
for seconds in range(10): 
	butiabot.reconnect("localhost",2009)
	modulos = butiabot.listarModulos()
	if modulos == -1:
		print "waiting..."
	else:	
		print "bobot OK! ; after " + str(seconds) + " seconds"
		butiabot.cerrar()
		exit(0)
	time.sleep(1)

butiabot.cerrar()
print "bobot is down or not responding!"
exit(-1)

