#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# FollowMe Butia - Main
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

import gtk
import pygame
import robot
from robot import Robot
import followme
from followme import FollowMe
from gettext import gettext as _

class Main:

    def __init__(self, parent):
        self.parent = parent
        self.clock = pygame.time.Clock()
        self.calibrating = True
        self.show_size = (960.0, 720.0)
        self.r = None
        self.c = None

    def mode_calibrating(self, calibrating):
        self.calibrating = calibrating
        if self.calibrating:
            if (self.r != None and self.r.modules != []):
                self.r.butia.set2MotorSpeed('0', '0', '0', '0')
        if (self.show == False):
            self.c.limpiar()

    def put_threshold(self, threshold):
        self.threshold = threshold

    def put_colorC(self, colorC):
        if (self.calibrating == False):
            self.colorC = colorC

    def put_pixels(self, pixels):
        self.pixels = pixels

    def put_show_size(self, show_size):
        self.show_size = show_size
        self.c.calc(self.show_size)

    def put_grid(self, grid):
        self.c.show_grid = grid

    def put_show(self, show):
        self.show = show
        if (self.show == False):
            self.c.clean()

    def put_color_mode(self, mode):
        self.mode = mode
        self.c.get_camera(self.mode)

    def put_threshold_view(self, view):
        self.c.use_threshold_view = view

    def put_brightness(self, brightness):
        self.c.brightness = brightness
        self.c.set_camera_flags()

    def run(self):
        self.r = Robot((320, 240))
        self.threshold = (25, 25, 25)
        self.colorC = (255, 255, 255)
        self.pixels = 10
        self.show_size = (960, 720)
        self.show = True
        self.mode = 'RGB'
        self.c = FollowMe(self.mode, self.parent)
        if (self.c.cam == None):
            while gtk.events_pending():
                gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # salgo
                    break
                #elif event.type == pygame.VIDEORESIZE:
                #    pygame.display.set_mode(event.size, pygame.RESIZABLE)
        else:
            run = True            
            while run:
                while gtk.events_pending():
                    gtk.main_iteration()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    #elif event.type == pygame.VIDEORESIZE:
                    #    pygame.display.set_mode(event.size, pygame.RESIZABLE)

                if (self.calibrating):
                    self.colorC = self.c.calibrate()
                    if self.parent:
                        self.parent.put_color(self.colorC)
                else:
                    pos = self.c.get_position(self.colorC, self.threshold, self.pixels)
                    self.c.show_position()
                    if self.show and not(pos == -1):
                        #for p in pos:
                        self.c.show_position2(pos, self.colorC)
                    self.c.show_position3(self.colorC)
                    if (self.r != None and self.r.modules != []):
                        self.r.move_robot(pos)

                pygame.display.flip()
                self.clock.tick(10)

        if self.r:
            if self.r.butia:
                self.r.butia.close()
                self.r.butia.closeService()
            if self.r.bobot:
                self.r.bobot.kill()
        if self.c.cam:
            try:
                self.cam.stop()
            except:
                pass


