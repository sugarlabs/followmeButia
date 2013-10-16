#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Client for pybot_server
#
# Copyright (c) 2012-2013 Alan Aguiar alanjas@hotmail.com
# Copyright (c) 2009-2013 Butiá Team butia@fing.edu.uy 
# Butia is a free and open robotic platform
# www.fing.edu.uy/inco/proyectos/butia
# Facultad de Ingeniería - Universidad de la República - Uruguay
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
import threading
import errno
from functions import ButiaFunctions

ERROR = -1

PYBOT_HOST = 'localhost'
PYBOT_PORT = 2009

class robot(ButiaFunctions):
    
    def __init__(self, host=PYBOT_HOST, port=PYBOT_PORT, auto_connect=True):
        """
        init the robot class
        """
        self._lock = threading.Lock()
        self._host = host
        self._port = port
        self._client = None
        if auto_connect:
            self.reconnect()
       
    def _doCommand(self, msg, ret_type = str):
        """
        Executes a command in butia.
        @param msg message to be executed
        """
        msg = msg + '\n'
        ret = ERROR
        self._lock.acquire()
        try:     
            self._client.send(msg)
            ret = self._client.recv(1024)
            ret = ret[:-1]
        except Exception, e:
            if hasattr(e, 'errno'):
                if e.errno == errno.EPIPE:
                    self.reconnect()
            self._lock.release()
            return ERROR
        try:
            ret = ret_type(ret)
        except:
            ret = ERROR
        self._lock.release()
        return ret

    def reconnect(self):
        """
        connect o reconnect the bobot
        """
        self.close()
        try:
            self._client = socket.socket()
            self._client.connect((self._host, self._port))
        except:
            return ERROR
        return 0

    def refresh(self):
        """
        ask bobot for refresh is state of devices connected
        """
        self._doCommand('REFRESH')

    def close(self):
        """
        close the comunication with pybot
        """
        try:
            self._client.close()
            self._client = None
        except:
            return ERROR
        return 0

    def callModule(self, modulename, board_number, number, function, params = [], ret_type = int):
        """
        call the module 'modulename'
        """
        msg = 'CALL ' + modulename + '@' + str(board_number) + ':' + str(number) + ' ' + function
        if not(params == []):
            msg = msg + ' ' + ' '.join(params)
        return self._doCommand(msg, ret_type)

    def closeService(self):
        """
        Close bobot service
        """
        return self._doCommand('QUIT')

    def getButiaCount(self):
        """
        Gets the number of boards detected
        """
        return self._doCommand('BUTIA_COUNT', int)

    def getModulesList(self):
        """
        returns a list of modules
        """
        ret = self._doCommand('LIST')
        if (ret == ERROR) or (ret == ''):
            return []
        else:
            return ret.split(',')

    def getListi(self, board_number=0):
        """
        returns a list of instanciables modules
        """
        ret = self._doCommand('LISTI ' + str(board_number))
        if (ret == ERROR) or (ret == ''):
            return []
        else:
            return ret.split(',')

    def _split_module(self, mbn):
        """
        Split a modulename: module@board:port to (number, modulename, board)
        """
        board = '0'
        number = '0'
        if mbn.count('@') > 0:
            modulename, bn = mbn.split('@')
            if bn.count(':') > 0:
                board, number = bn.split(':')
            else:
                board = bn
        else:
            if mbn.count(':') > 0:
                modulename, number = mbn.split(':')
            else:
                modulename = mbn
        return (number, modulename, board)

    def describe(self, mod):
        """
        Describe the functions of a modulename
        """
        split = self._split_module(mod)
        mod = split[1]
        ret = self._doCommand('DESCRIBE ' + mod)
        return ret

    def moduleOpen(self, mod):
        """
        Open the module mod
        """
        return self._doCommand('OPEN ' + mod, int)

    def moduleClose(self, mod):
        """
        Close the module mod
        """
        return self._doCommand('CLOSE ' + mod, int)

if __name__ == "__main__":
    c = robot()
    run = True
    while run:
        m = raw_input("> ")
        ret = c._doCommand(m)
        print ret
        if m == "QUIT":  
            run = False
    c.close()

