#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Chotox utility for debug
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


import os
import imp
import inspect
from functions import ButiaFunctions
import random

ERROR = -1

class Chotox(ButiaFunctions):

    def __init__(self, debug=False, get_modules=True, chotox=False):
        self._debug_flag = debug
        self._hotplug = []
        self._openables = []
        self._drivers_loaded = {}
        self._get_all_drivers()
        self.devices = {0:'admin', 2:'button', 4:'grey', 5:'distanc', 7:'pnp'}
        self._openables_loaded = ['admin', 'pnp']
        if get_modules:
            self.getModulesList(refresh=False)

    def _debug(self, message, err=''):
        if self._debug_flag:
            print message, err

    def getButiaCount(self):
        """
        Gets the number of boards detected
        """
        return 1

    def getModulesList(self, normal=True, refresh=True):
        """
        Get the list of modules loaded in the board
        """
        self._debug('=Listing Devices')
        modules = []
        self._debug('===board', 0)
        for i in range(12):
            if self.devices.has_key(i):
                module_name = self.devices[i]
            elif i < 7:
                module_name = 'port'
            if self.devices.has_key(i) or (i < 7):
                complete_name = module_name + ':' +  str(i)
                modules.append(complete_name)
                self._debug('=====module ' + module_name + (9 - len(module_name)) * ' ' + complete_name)

        return modules

    def _get_all_drivers(self):
        """
        Load the drivers for the differents devices
        """
        # current folder
        path_drivers = os.path.join(os.path.dirname(__file__), 'drivers')
        self._debug('Searching drivers in: ', str(path_drivers))
        # normal drivers
        tmp = os.listdir(path_drivers)
        tmp.sort()
        for d in tmp:
            if d.endswith('.py'):
                name = d.replace('.py', '')
                self._openables.append(name)
                self._get_driver(path_drivers, name)
        # hotplug drivers
        path = os.path.join(path_drivers, 'hotplug')
        tmp = os.listdir(path)
        tmp.sort()
        for d in tmp:
            if d.endswith('.py'):
                name = d.replace('.py', '')
                self._hotplug.append(name)
                self._get_driver(path, name)

    def _get_driver(self, path, driver):
        """
        Get a specify driver
        """
        self._debug('Loading driver %s...' % driver)
        abs_path = os.path.abspath(os.path.join(path, driver + '.py'))
        try:
            self._drivers_loaded[driver] = imp.load_source(driver, abs_path)
        except:
            self._debug('ERROR:usb4butia:_get_driver cannot load %s' % driver, abs_path)
        
    def callModule(self, modulename, board_number, number, function, params = [], ret_type = int):
        """
        Call one function: function for module: modulename in board: board_name
        with handler: number (only if the module is pnp, else, the parameter is
        None) with parameteres: params
        """
        self._open_or_validate(modulename, board_number)

        #print modulename, function

        if modulename == 'butia' and function == 'getVolt':
            return 10.5
        elif modulename == 'motors' and function == 'getType':
            return 1

        if function == 'getValue':
            if modulename == 'button':
                return random.randrange(0, 2)
            elif modulename == 'grey' or modulename == 'distanc':
                return random.randrange(0, 65536)
            else:
                return ERROR
        elif function == 'getVersion':
            if modulename == 'admin':
                return 6
            else:
                return 1
        else:
            return ERROR

    def refresh(self):
        """
        Search for connected USB4Butia boards and open it
        """
        pass

    def close(self):
        """
        Closes all open baseboards
        """
        pass

    def moduleOpen(self, mod):
        """
        Open the module mod
        """
        split = self._split_module(mod)
        modulename = split[1]
        b = int(split[2])
        if len(self._bb) < (b + 1):
            return ERROR
        board = self._bb[b]
        return self._open_or_validate(modulename, board)

    def _open_or_validate(self, modulename, board):
        """
        Open o check if modulename module is open in board: board
        """
        if modulename in self._openables:
            if modulename in self._openables_loaded:
                return self._get_handler(modulename)
            else:
                m = self._max_handler()
                m = m + 1
                self.devices[m] = modulename
                self._openables_loaded.append(modulename)
                return m
        return ERROR

    def moduleClose(self, mod):
        """
        Close the module mod
        """
        split = self._split_module(mod)
        modulename = split[1]
        if modulename in self._openables:
            b = int(split[2])
            if len(self._bb) < (b + 1):
                return ERROR
            board = self._bb[b]
            if modulename in board.get_openables_loaded():
                number = board.get_device_handler(modulename)
                try:
                    res = board.devices[number].moduleClose()
                    if res == 1:
                        board.remove_openable_loaded(modulename)
                        return res
                except Exception, err:
                    self._debug('ERROR:usb4butia:moduleClose', err)
                    return ERROR
            else:
                self._debug('cannot close no opened module')
                return ERROR
        else:
            self._debug('cannot close no openable module')
        return ERROR

    def getListi(self, board_number=0):
        listi = ['admin', 'pnp', 'port', 'ax', 'button', 'hackp', 'motors', 'butia', 'led']
        listi = listi + ['grey', 'light', 'res', 'volt', 'temp', 'distanc']
        return listi

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
        funcs = []
        d = {}
        if self._drivers_loaded.has_key(mod):
            driver = self._drivers_loaded[mod]
            a = dir(driver)
            flag = False
            for p in a:
                if p == '__package__':
                    flag = True
                if flag:
                    funcs.append(p)
            funcs.remove('__package__')
            for f in funcs:
                h = getattr(driver, f)
                i = inspect.getargspec(h)
                parameters = i[0]
                if 'dev' in parameters:
                    parameters.remove('dev')
                d[f] = parameters
        return d

    def _get_handler(self, name):
        for e in self.devices:
            if self.devices[e] == name:
                return e
        return ERROR

    def _max_handler(self):
        m = ERROR
        for e in self.devices:
            if e > m:
                m = e
        return m

        
