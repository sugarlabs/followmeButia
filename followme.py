#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# FollowMe Butia
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


import pygame
import pygame.camera
import gtk
import butiaAPI
import time
import subprocess
import commands
from gettext import gettext as _

# seteamos el tamaño de captura
tamanioc = (320, 240)


class Captura(object):

    def __init__(self, mode, parent):
        
        pygame.init()
        pygame.camera.init()
        if parent:
            self.display = pygame.display.get_surface()
        else:
            self.display = pygame.display.set_mode((1200, 900))
        self.use_threshold_view = True
        self.cam = None
        self.get_camera(mode)
        self.calc((960, 720))
        self.show_grid = False
    
    def get_camera(self, mode):
        global tamanioc
        if self.cam:
            try:
                self.cam.stop()
            except:
                print _('Error in stop camera')
        self.lcamaras = pygame.camera.list_cameras()
        if self.lcamaras:
            self.cam = pygame.camera.Camera(self.lcamaras[0], tamanioc, mode)
            tamanioc = self.cam.get_size()
            if not (tamanioc == (320, 240)):
                self.cam = pygame.camera.Camera(self.lcamaras[0], (352, 288), mode)
            try:
                #self.cam.set_controls(brightness = 129)
                self.cam.set_controls(True, False)
                self.cam.start()
                res = self.cam.get_controls()
                self.flip = res[0]
                tamanioc = self.cam.get_size()
                self.captura = pygame.surface.Surface(tamanioc, 0, self.display)
                self.captura_aux = pygame.surface.Surface(tamanioc, 0, self.display)
                self.captura_to_show = pygame.surface.Surface(tamanioc, 0, self.display)
            except:
                print _('Error on initialization of the camera')
        else:
            print _('No cameras was found')

    def calc(self, tamanio):
        self.show_size = tamanio
        pantalla_x, pantalla_y = self.display.get_size()
        self.c1 = (self.show_size[0] / tamanioc[0])
        self.c2 = (self.show_size[1] / tamanioc[1])
        self.xc = (tamanioc[0] - 50) / 2.0
        self.yc = (tamanioc[1] - 50) / 2.0
        self.xcm = (pantalla_x - 50) / 2.0
        self.ycm = (pantalla_y - 50) / 2.0
        self.xblit = (pantalla_x - self.show_size[0]) / 2
        self.yblit = (pantalla_y - self.show_size[1]) / 2
        self.txd = self.show_size[0] / 15.0
        self.tyd = self.show_size[1] / 3.0

    def calibrate(self):
        self.captura = self.cam.get_image(self.captura)
        if not(self.flip):
            self.captura = pygame.transform.flip(self.captura,True,False)
        color = pygame.transform.average_color(self.captura, (self.xc,self.yc,50,50))
        self.display.fill((84,185,72))
        self.captura_to_show = pygame.transform.scale(self.captura, (int(self.show_size[0]), int(self.show_size[1])))
        self.display.blit(self.captura_to_show, (self.xblit, self.yblit))
        #FIXME: cambiar posición en función de la pantalla
        
        rect = pygame.draw.rect(self.display, (255,0,0), (self.xcm,self.ycm,50,50), 4)
        self.display.fill(color, (0,0,120,120))
        rect = pygame.draw.rect(self.display, (0,0,0), (0,0,120,120), 4)
        return color

    def get_position(self, color, threshold, pixels):
        self.captura = self.cam.get_image(self.captura)

        if not(self.flip):
            self.captura = pygame.transform.flip(self.captura,True,False)
        
        if self.use_threshold_view:
            pygame.transform.threshold(self.captura_aux, self.captura, color, (threshold[0],threshold[1], threshold[2]), (0,0,0), 2)
            mascara = pygame.mask.from_threshold(self.captura_aux, color, (10, 10, 10))
        else:
            mascara = pygame.mask.from_threshold(self.captura, color, (10, 10, 10))
            
        conexa = mascara.connected_component()

        if (conexa.count() > pixels):
            return mascara.centroid()
        else:
            return (-1,-1)

    def show_position(self, pos, color):
        x, y = pos

        if self.use_threshold_view:
            self.captura_to_show = pygame.transform.scale(self.captura_aux, (int(self.show_size[0]), int(self.show_size[1])))
        else:
            self.captura_to_show = pygame.transform.scale(self.captura, (int(self.show_size[0]), int(self.show_size[1])))
        if (x != -1):
            rect = pygame.draw.rect(self.captura_to_show, (255,0,0), (x*self.c1, y*self.c2, 20, 20), 16)
        self.display.fill((84,185,72))

        if (self.show_grid == True):
            self.draw_grid()
        self.display.blit(self.captura_to_show, (self.xblit, self.yblit))
        self.display.fill(color, (0,0,120,120))
        rect = pygame.draw.rect(self.display, (0,0,0), (0,0,120,120), 4)

    def draw_grid(self):
        # draw verticals
        r0 = pygame.draw.line(self.captura_to_show, (250, 40, 40), (0, self.tyd), (self.show_size[0],self.tyd), 3)
        r1 = pygame.draw.line(self.captura_to_show, (250, 40, 40), (0, 2*self.tyd), (self.show_size[0], 2*self.tyd), 3)
        # draw horizontals
        r2 = pygame.draw.line(self.captura_to_show, (250, 40, 40), (2*self.txd, 0), (2*self.txd, self.show_size[1]), 3)
        r3 = pygame.draw.line(self.captura_to_show, (250, 40, 40), (4*self.txd, 0), (4*self.txd, self.show_size[1]), 3)
        r4 = pygame.draw.line(self.captura_to_show, (250, 40, 40), (6*self.txd, 0), (6*self.txd, self.show_size[1]), 3)
        r5 = pygame.draw.line(self.captura_to_show, (250, 40, 40), (9*self.txd, 0), (9*self.txd, self.show_size[1]), 3)
        r6 = pygame.draw.line(self.captura_to_show, (250, 40, 40), (11*self.txd, 0), (11*self.txd, self.show_size[1]), 3)
        r7 = pygame.draw.line(self.captura_to_show, (250, 40, 40), (13*self.txd, 0), (13*self.txd, self.show_size[1]), 3)
        

    def clean(self):
        self.display.fill((84, 185, 72))


class Robot(object):

    def __init__(self):
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
    

class FollowMe:

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

    def run(self):
        self.r = Robot()
        self.threshold = (25, 25, 25)
        self.colorC = (255, 255, 255)
        self.pixels = 10
        self.show_size = (960, 720)
        self.show = True
        self.mode = 'RGB'
        self.c = Captura(self.mode, self.parent)
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

                    if self.show:
                        self.c.show_position(pos, self.colorC)
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


if __name__ == "__main__":
    f = FollowMe(None)
    f.run()

