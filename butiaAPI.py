#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 
# ButiaAPI
# Copyright (c) 2009, 2010, 2011, 2012 Butiá Team butia@fing.edu.uy 
# Butia is a free open plataform for robotics projects
# www.fing.edu.uy/inco/proyectos/butia
# Facultad de Ingenieria - Universidad de la República - Uruguay
#
# Implements abstractions for the comunications with the bobot-server
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import socket
import string
import math
import threading

ERROR_SENSOR_READ = -1 

BOBOT_HOST = 'localhost'
BOBOT_PORT = 2009

class robot:
    

    def __init__(self, host = BOBOT_HOST, port = BOBOT_PORT):
        """
        init the robot class
        """
        self.lock = threading.Lock()
        self.host = host
        self.port = port
        self.client = None
        self.fclient = None
        self.reconnect()

       
    def doCommand(self, msg):
        """
        Executes a command in butia.
        @param msg message to be executed
        """
        msg = msg +'\n'
        ret = -1
        self.lock.acquire()
        try:     
            self.client.send(msg) 
            ret = self.fclient.readline()
            ret = ret[:-1]
        except:
            ret = ERROR_SENSOR_READ # Doesn't return here to release the lock
        self.lock.release()
        
        if ((ret == 'nil value') or (ret == None) or (ret == 'fail') or (ret == 'missing driver')):
            ret = ERROR_SENSOR_READ
        return ret
          
    # connect o reconnect the bobot
    def reconnect(self):
        self.close()
        try:
            self.client = socket.socket()
            self.client.connect((self.host, self.port))  
            self.fclient = self.client.makefile()
            msg = 'INIT'
            #bobot server instance is running, but we have to check for new or remove hardware
            self.doCommand(msg)
        except:
            return -1
        return 0

    # ask bobot for refresh is state of devices connected
    def refresh(self):
        msg = 'INIT'
        #bobot server instance is running, but we have to check for new or remove hardware
        result = self.doCommand(msg)
        if (result == ERROR_SENSOR_READ):
                result = self.reconnect()
        #return result


    # close the comunication with the bobot
    def close(self):
        try:
            if self.fclient != None:
                self.fclient.close()
                self.fclient = None
            if self.client != None:
                self.client.close()
                self.client = None
        except:
            return -1
        return 0

    #######################################################################
    ### Operations to the principal module
    #######################################################################

    # open the module 'modulename'
    def openModule(self, modulename):
        msg = 'OPEN ' + modulename
        return self.doCommand(msg)

    # call the module 'modulename'
    def callModule(self, modulename, function , params = ''):
        msg = 'CALL ' + modulename + ' ' + function
        if params != '' :
            msg += ' ' + params
        return self.doCommand(msg)

    # Close bobot service
    def closeService(self):
        msg = 'QUIT'
        return self.doCommand(msg)

    #######################################################################
    ### Useful functions 
    #######################################################################

    # returns if the module_name is present
    def isPresent(self, module_name):
        module_list = self.get_modules_list()
        return (module_name in module_list)

    # returns a list of modules
    def get_modules_list(self):
        msg = 'LIST'
        ret = self.doCommand(msg)
        if not (ret == '' or ret == -1):
            return ret.split(',')
        else:
           return []

    # loopBack: send a message to butia and wait to recibe the same
    def loopBack(self, data):
        msg = 'lback send ' + data
        ret = self.doCommand(msg)
        if ret != -1 :
            return self.callModule('lback', 'read')
        else:
            return -1
            

    #######################################################################
    ### Operations for motores.lua driver
    #######################################################################

    def set2MotorSpeed(self, leftSense = '0', leftSpeed = '0', rightSense = '0', rightSpeed = '0'):
            msg = leftSense + ' ' + leftSpeed + ' ' + rightSense + ' ' + rightSpeed
            return self.callModule('motores', 'setvel2mtr', msg)
     
    def setMotorSpeed(self, idMotor = '0', sense = '0', speed = '0'):
            msg = idMotor + ' ' + sense + ' ' + speed
            return self.callModule('motores', 'setvelmtr', msg)

    #######################################################################
    ### Operations for butia.lua driver
    #######################################################################

    def ping(self):
        return self.callModule('placa', 'ping')

    # returns the approximate charge of the battery        
    def getBatteryCharge(self):
        bat = ERROR_SENSOR_READ
        try:
            bat = self.callModule('butia', 'get_volt')
            bat = int(bat)
        except:
            pass
        return bat

    # returns the firmware version 
    def getVersion(self):
        return self.callModule('butia', 'read_ver')
    
    # set de motor idMotor on determinate angle
    def setPosition(self, idMotor = 0, angle = 0):
        msg = str(idMotor) + ' ' + str(angle)
        return self.callModule('placa', 'setPosicion' , msg )
    
    # return the value of button: 1 if pressed, 0 otherwise
    def getButton(self, number=''):
        return self.callModule('boton' + str(number), 'getBoton')
    
    # return the value en ambient light sensor
    def getAmbientLight(self, number=''):
        return self.callModule('luz' + str(number), 'getLuz')

    # return the value of the distance sensor
    def getDistance(self, number=''):
        return self.callModule('dist' + str(number), 'getDistancia')
    
    # return the value of the grayscale sensor
    def getGrayScale(self, number=''):
        return self.callModule('grises' + str(number), 'getLevel')

    # return the value of the temperature sensor
    def getTemperature(self, number=''):
        return self.callModule('temp' + str(number), 'getTemp')

    # return the value of the vibration sensor
    def getVibration(self, number=''):
        return self.callModule('vibra' + str(number), 'getVibra')

    # return the value of the tilt sensor
    def getTilt(self, number=''):
        return self.callModule('tilt' + str(number), 'getTilt')

    # FIXME: the name of the module and the function...
    # return the value of the capacitive touch sensor
    def getCapacitive(self, number=''):
        return self.callModule('capacitive' + str(number), 'getCapa')

    # return the value of the magnetic induction sensor
    def getMagneticInduction(self, number=''):
        return self.callModule('magnet' + str(number), 'getCampo')

    # set the led intensity
    def setLed(self, number= '', nivel = 255):
        return self.callModule('led' + str(number), 'setLight', str(math.trunc(nivel)))

    # FIXME: check the lenght of text?
    # write a text in LCD display
    def writeLCD(self, text):
        text = str(text)
        text = text.replace(' ', '_')
        self.callModule('display', 'escribir' , text)

