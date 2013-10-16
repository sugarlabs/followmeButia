#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Abstract class with common functions
#
# Copyright (c) 2012-2013 Alan Aguiar alanjas@hotmail.com
# Copyright (c) 2012-2013 Butiá Team butia@fing.edu.uy 
# Butia is a free and open robotic platform
# www.fing.edu.uy/inco/proyectos/butia
# Facultad de Ingeniería - Universidad de la República - Uruguay
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


class ButiaFunctions:

    def isPresent(self, module_name):
        """
        Check if module: module_name is present
        """
        module_list = self.get_modules_list()
        return (module_name in module_list)

    def loopBack(self, data, board='0'):
        """
        LoopBack command: send data to the board and get the result. If all is ok
        the return must be exactly of the data parameter
        """
        msg = [str(data)]
        return self.callModule('lback', str(board), '0', 'send', msg, ret_type=str)

    ############################## Movement calls ##############################

    def set2MotorSpeed(self, leftSense='0', leftSpeed='0', rightSense='0', rightSpeed='0', board='0'):
        """
        Set the speed of 2 motors. The sense is 0 or 1, and the speed is
        between 0 and 1023
        """
        msg = [str(leftSense), str(leftSpeed), str(rightSense), str(rightSpeed)]
        return self.callModule('motors', str(board), '0', 'setvel2mtr', msg)

    def setMotorSpeed(self, idMotor='0', sense='0', speed='0', board='0'):
        """
        Set the speed of one motor. idMotor = 0 for left motor and 1 for the
        right motor. The sense is 0 or 1, and the speed is between 0 and 1023
        """
        msg = [str(idMotor), str(sense), str(speed)]
        return self.callModule('motors', str(board), '0', 'setvelmtr', msg)

    def getMotorType(self, board='0'):
        """
        If AX-12 motors present returns 1. If there are a shield "cc" returns 2
        """
        return self.callModule('motors', str(board), '0', 'getType')

    ##################### Operations for ax.lua driver #########################

    def writeInfo(self, idMotor, regstart, value, board='0'):
        """
        Writes the motor: idMotor in the registry: regstart with value: value
        """
        msg = [str(idMotor), str(regstart), str(value)]
        return self.callModule('ax', str(board), '0', 'writeInfo', msg)

    def readInfo(self, idMotor, regstart, length='1', board='0'):
        """
        Reads the motor: idMotor in the registry: regstart
        """
        msg = [str(idMotor), str(regstart), str(length)]
        return self.callModule('ax', str(board), '0', 'writeInfo', msg)

    def sendPacket(self, msg, board='0'):
        """
        Send a raw packet to ax module
        """
        msg_s = [str(i) for i in msg]
        return self.callModule('ax', str(board), '0', 'sendPacket', msg_s, ret_type=str)

    def wheelMode(self, idMotor='0', board='0'):
        """
        Sets the motor: idMotor in wheel mode (continuos rotation)
        """
        msg = [str(idMotor)]
        return self.callModule('ax', str(board), '0', 'wheelMode', msg)
     
    def jointMode(self, idMotor='0', _min='0', _max='1023', board='0'):
        """
        Sets the motor: idMotor in servo mode
        """
        msg = [str(idMotor), str(_min), str(_max)]
        return self.callModule('ax', str(board), '0', 'jointMode', msg)

    def setPosition(self, idMotor='0', pos='0', board='0'):
        """
        Sets the position: pos of the motor: idMotor
        """
        msg = [str(idMotor), str(pos)]
        return self.callModule('ax', str(board), '0', 'setPosition', msg)

    def getPosition(self, idMotor='0', board='0'):
        """
        Gets the position of motor: idMotor
        """
        msg = [str(idMotor)]
        return self.callModule('ax', str(board), '0', 'getPosition', msg)

    def setSpeed(self, idMotor='0', speed='0', board='0'):
        """
        Set the speed: speed to the motor: idMotor
        """
        msg = [str(idMotor), str(speed)]
        return self.callModule('ax', str(board), '0', 'setSpeed', msg)

    ############################### General calls ##############################
     
    def getBatteryCharge(self, board='0'):
        """
        Gets the battery level charge
        """
        return self.callModule('butia', str(board), '0', 'getVolt', ret_type=float)

    def getVersion(self, board='0'):
        """
        Gets the version of Butiá module. 22 for new version
        """
        return self.callModule('butia', str(board), '0', 'getVersion')

    def getFirmwareVersion(self, board='0'):
        """
        Gets the version of the Firmware
        """
        return self.callModule('admin', str(board), '0', 'getVersion')

    ############################### Sensors calls ###############################

    def getButton(self, port, board='0'):
        """
        Gets the value of the button connected in port
        """
        return self.callModule('button', str(board), str(port), 'getValue')
    
    def getLight(self, port, board='0'):
        """
        Gets the value of the light sensor connected in port
        """
        return self.callModule('light', str(board), str(port), 'getValue')

    def getDistance(self, port, board='0'):
        """
        Gets the value of the distance sensor connected in port
        """
        return self.callModule('distanc', str(board), str(port), 'getValue')

    def getGray(self, port, board='0'):
        """
        Gets the value of the gray sensor connected in port
        """
        return self.callModule('grey', str(board), str(port), 'getValue')

    def getResistance(self, port, board='0'):
        """
        Gets the value of the resistance sensor connected in port
        """
        return self.callModule('res', str(board), str(port), 'getValue', ret_type=float)

    def getVoltage(self, port, board='0'):
        """
        Gets the value of the voltage sensor connected in port
        """
        return self.callModule('volt', str(board), str(port), 'getValue', ret_type=float)

    def getTemperature(self, port, board='0'):
        """
        Gets the value of the temperature sensor connected in port
        """
        return self.callModule('temp', str(board), str(port), 'getValue', ret_type=float)

    def setLed(self, port, on_off, board='0'):
        """
        Sets on or off the LED connected in port (0 is off, 1 is on)
        """
        return self.callModule('led', str(board), str(port), 'turn', [str(on_off)])

    ################################ Extras ################################

    def modeHack(self, pin, mode, board='0'):
        """
        Sets the mode of hack pin. If mode 0 = input, mode 1 = output
        """
        msg = [str(pin), str(mode)]
        return self.callModule('hackp', str(board), '0', 'setMode', msg)

    def setHack(self, pin, value, board='0'):
        """
        Sets the value of hack pin configured as output. Value is 0 or 1
        """
        msg = [str(pin), str(value)]
        return self.callModule('hackp', str(board), '0', 'write', msg)

    def getHack(self, pin, board='0'):
        """
        Gets the value of hack pin configured as input. Returns 0 or 1
        """
        return self.callModule('hackp', str(board), '0', 'read', [str(pin)])

    ############################# Generic modules #############################

    def getModuleA(self, port, board='0'):
        """
        Gets the value of the generic sensor ModuleA connected in port
        """
        return self.callModule('moduleA', str(board), str(port), 'getValue')

    def getModuleB(self, port, board='0'):
        """
        Gets the value of the generic sensor ModuleB connected in port
        """
        return self.callModule('moduleB', str(board), str(port), 'getValue')

    def getModuleC(self, port, board='0'):
        """
        Gets the value of the generic sensor ModuleC connected in port
        """
        return self.callModule('moduleC', str(board), str(port), 'getValue')

    def setModuleA(self, port, on_off, board='0'):
        """
        Sets on or off the generic module A
        """
        return self.callModule('modSenA', str(board), str(port), 'turn', [str(on_off)])

    def setModuleB(self, port, on_off, board='0'):
        """
        Sets on or off the generic module B
        """
        return self.callModule('modSenB', str(board), str(port), 'turn', [str(on_off)])

    def setModuleC(self, port, on_off, board='0'):
        """
        Sets on or off the generic module C
        """
        return self.callModule('modSenC', str(board), str(port), 'turn', [str(on_off)])

