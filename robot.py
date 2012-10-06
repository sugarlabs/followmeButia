#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# FollowMe Butia - Robot
# Copyright (C) 2010, 2011, 2012
# This program was created to use with the robot Butia.
# Butia is a project from Facultad de Ingenieria - Uruguay
# Facultad de Ingenieria web site: <http://www.fing.edu.uy/>
# Butia project web site: <http://www.fing.edu.uy/inco/proyectos/butia/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Alan Aguiar <alanjas@gmail.com>
# Aylen Ricca <ar18_90@hotmail.com>
# Rodrigo Dearmas <piegrande46@hotmail.com>



class Robot(object):

    def __init__(self, tamanioc):
        self.z1 = tamanioc[0] / 15.0
        self.z2 = tamanioc[1] / 3.0
        self.vel_anterior = (0, 0, 0, 0)
        self.butia = None
        self.bobot = None
        self.bobot_launch()

    def bobot_launch(self):

        print 'Initialising butia...'
        output = commands.getoutput('ps -ax | grep lua')
        if 'bobot-server' in output:
            print 'bobot is alive!'
        else:
            try:
                print 'creating bobot'
                self.bobot = subprocess.Popen(['./lua', 'bobot-server.lua'], cwd='./lib/butia_support')
            except:
                print 'ERROR creating bobot'

        time.sleep(1)

        self.butia = butiaAPI.robot()

        self.modules = self.butia.get_modules_list()

        if (self.modules != []):
            print self.modules
        else:
            print _('Butia robot was not detected')

    def move_robot(self, pos):

        x,y = pos

        vel_actual = (0, 0, 0, 0)

        if (x >= 0) and (x <= (2*self.z1)):
            if (y >= 0) and (y <= self.z2) :
                vel_actual = (1, 900, 1, 600)
            elif (y > self.z2) and (y < 2*self.z2):
                vel_actual = (0, 900, 1, 900)
            elif (y >= 2*self.z2):
                vel_actual = (0, 900, 0, 600)

        elif (x > (2*self.z1)) and (x <= (4*self.z1)):
            if (y >= 0) and (y <= self.z2) :
                vel_actual = (1, 600, 1, 300)
            elif (y > self.z2) and (y < 2*self.z2):
                vel_actual = (0, 600, 1, 600)
            elif (y >= 2*self.z2):
                vel_actual = (0, 600, 0, 600)


        elif (x > (4*self.z1)) and (x <= (6*self.z1)):
            if (y >= 0) and (y <= self.z2) :
                vel_actual = (1, 300, 1, 0)
            elif (y > self.z2) and (y < 2*self.z2):
                vel_actual = (0, 300, 1, 300)
            elif (y >= 2*self.z2):
                vel_actual = (0, 300, 0, 0)

        elif (x > 6*self.z1) and (x < 9*self.z1):
            if (y >= 0) and (y <= self.z2) :
                vel_actual = (1, 300, 1, 300)
            elif (y > self.z2) and (y < 2*self.z2):
                vel_actual = (0, 0, 0, 0)
            elif (y >= 2*self.z2):
                vel_actual = (0, 300, 0, 300)


        elif (x >= (9*self.z1)) and (x < (11*self.z1)):
            if (y >= 0) and (y <= self.z2) :
                vel_actual = (1, 0, 1, 300)
            elif (y > self.z2) and (y < 2*self.z2):
                vel_actual = (0, 300, 1, 300)
            elif (y >= 2*self.z2):
                vel_actual = (0, 0, 0, 300)


        elif (x >= 11*self.z1) and (x < 13*self.z1):
            if (y >= 0) and (y <= self.z2) :
                vel_actual = (1, 300, 1, 600)
            elif (y > self.z2) and (y < 2*self.z2):
                vel_actual = (0, 600, 1, 600)
            elif (y >= 2*self.z2):
                vel_actual = (0, 300, 0, 600)


        elif (x >= (13*self.z1)):
            if (y >= 0) and (y <= self.z2) :
                vel_actual = (1, 600, 1, 900)
            elif (y > self.z2) and (y < 2*self.z2):
                vel_actual = (0, 900, 1, 900)
            elif (y >= 2*self.z2):
                vel_actual = (0, 600, 0, 900)


        # para evitar envios de velocidad innecesarios al robot
        if not(vel_actual == self.vel_anterior):
            self.vel_anterior = vel_actual
            self.butia.set2MotorSpeed(str(vel_actual[0]), str(vel_actual[1]), str(vel_actual[2]), str(vel_actual[3]))


