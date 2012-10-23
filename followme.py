#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# FollowMe Butia - FollowMe
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
from gettext import gettext as _


class FollowMe(object):

    def __init__(self, mode, parent):
        
        pygame.init()
        pygame.camera.init()
        if parent:
            self.display = pygame.display.get_surface()
        else:
            self.display = pygame.display.set_mode((1200, 900))
        self.use_threshold_view = True
        self.tamanioc = (320, 240)
        self.brightness = 128
        self.cam = None
        self.get_camera(mode)
        self.calc((960, 720))
        self.show_grid = False
    
    def get_camera(self, mode):
        if self.cam:
            try:
                self.cam.stop()
            except:
                print _('Error in stop camera')
        self.lcamaras = pygame.camera.list_cameras()
        if self.lcamaras:
            self.cam = pygame.camera.Camera(self.lcamaras[0], self.tamanioc, mode)
            try:
                self.cam.start()
                self.set_camera_flags()
                self.tamanioc = self.cam.get_size()
                self.captura = pygame.surface.Surface(self.tamanioc, 0, self.display)
                self.captura_aux = pygame.surface.Surface(self.tamanioc, 0, self.display)
                self.captura_aux2 = pygame.surface.Surface(self.tamanioc, 0, self.display)
                self.captura_to_show = pygame.surface.Surface(self.tamanioc, 0, self.display)
            except:
                print _('Error on initialization of the camera')
        else:
            print _('No cameras was found')

    def set_camera_flags(self):
        self.cam.set_controls(True, False, self.brightness)
        res = self.cam.get_controls()
        self.flip = res[0]

    def calc(self, tamanio):
        self.show_size = tamanio
        pantalla_x, pantalla_y = self.display.get_size()
        self.c1 = (self.show_size[0] / self.tamanioc[0])
        self.c2 = (self.show_size[1] / self.tamanioc[1])
        self.xc = (self.tamanioc[0] - 50) / 2.0
        self.yc = (self.tamanioc[1] - 50) / 2.0
        self.xcm = (pantalla_x - 50) / 2.0
        self.ycm = (pantalla_y - 50) / 2.0
        self.xblit = (pantalla_x - self.show_size[0]) / 2
        self.yblit = (pantalla_y - self.show_size[1]) / 2
        self.txd = self.show_size[0] / 15.0
        self.tyd = self.show_size[1] / 3.0
        self.x_c_square = int(self.tamanioc[0] / 2)
        self.y_c_square = int(self.tamanioc[1] / 2)

    def calibrate(self):
        self.captura = self.cam.get_image(self.captura)
        if not(self.flip):
            self.captura = pygame.transform.flip(self.captura,True,False)

        # Obtiene un color un poco mas "oscuro" que lo que es
        #color = pygame.transform.average_color(self.captura, (self.xc,self.yc,50,50))
        # Obtengo el color del pixel ubicado en el centro

        color = self.captura.get_at((self.x_c_square, self.y_c_square))

        self.display.fill((84,185,72))
        self.captura_to_show = pygame.transform.scale(self.captura, (int(self.show_size[0]), int(self.show_size[1])))
        self.display.blit(self.captura_to_show, (self.xblit, self.yblit))
        #FIXME: cambiar posición en función de la pantalla
        
        #rect = pygame.draw.rect(self.display, (255,0,0), (self.xcm,self.ycm,50,50), 4)
        pygame.draw.rect(self.display, (255,0,0), (self.xcm,self.ycm,50,50), 4)

        self.display.fill(color, (0,0,120,120))
        pygame.draw.rect(self.display, (0,0,0), (0,0,120,120), 4)
        return color

    def get_position(self, color, threshold, pixels):
        self.captura = self.cam.get_image(self.captura)

        if not(self.flip):
            self.captura = pygame.transform.flip(self.captura,True,False)
        
        if self.use_threshold_view:
            pygame.transform.threshold(self.captura_aux2, self.captura, color, (threshold[0],threshold[1], threshold[2]), (0,0,0))
            pygame.transform.threshold(self.captura_aux, self.captura_aux2, (0, 0, 0), (10, 10, 10), (255, 255, 255)) 
            mascara = pygame.mask.from_threshold(self.captura_aux, (255, 255, 255), (10, 10, 10))
        else:
            mascara = pygame.mask.from_threshold(self.captura, color, (10, 10, 10))
            
        conexa = mascara.connected_component()
        #conexa = mascara.connected_components(pixels)
        #print conexa

        """if conexa == []:
            return (-1)
        else:
            l = []
            for p in conexa:
                if p.count > pixels:
                    l.append(p)
            return l"""
        return conexa

    def show_position(self):
        

        if self.use_threshold_view:
            self.captura_to_show = pygame.transform.scale(self.captura_aux, (int(self.show_size[0]), int(self.show_size[1])))
        else:
            self.captura_to_show = pygame.transform.scale(self.captura, (int(self.show_size[0]), int(self.show_size[1])))

    def show_position2(self, pos, color):
   
        x, y = pos.centroid()

        pygame.draw.rect(self.captura_to_show, (255,0,0), (x*self.c1, y*self.c2, 20, 20), 16)
        self.show_outline(pos)
        self.show_rects(pos)

    def show_outline(self, pos):
        l = pos.outline()
        for i in l:
            pygame.draw.rect(self.captura_to_show, (0,0,255), (i[0]*self.c1, i[1]*self.c2, 5, 5), 5)

    def show_rects(self, pos):
        r = pos.get_bounding_rects()
        for i in r:
            pygame.draw.rect(self.captura_to_show, (0,255,0), (i[0]*self.c1, i[1]*self.c2, i[2]*self.c1, i[3]*self.c2), 5)

    def show_position3(self, color):
        self.display.fill((84,185,72))

        if (self.show_grid == True):
            self.draw_grid()
        self.display.blit(self.captura_to_show, (self.xblit, self.yblit))
        #self.display.fill(color, (0,0,120,120))
        pygame.draw.rect(self.display, (0,0,0), (0,0,120,120), 4)

    def draw_grid(self):
        # draw verticals
        pygame.draw.line(self.captura_to_show, (250, 40, 40), (0, self.tyd), (self.show_size[0],self.tyd), 3)
        pygame.draw.line(self.captura_to_show, (250, 40, 40), (0, 2*self.tyd), (self.show_size[0], 2*self.tyd), 3)
        # draw horizontals
        pygame.draw.line(self.captura_to_show, (250, 40, 40), (2*self.txd, 0), (2*self.txd, self.show_size[1]), 3)
        pygame.draw.line(self.captura_to_show, (250, 40, 40), (4*self.txd, 0), (4*self.txd, self.show_size[1]), 3)
        pygame.draw.line(self.captura_to_show, (250, 40, 40), (6*self.txd, 0), (6*self.txd, self.show_size[1]), 3)
        pygame.draw.line(self.captura_to_show, (250, 40, 40), (9*self.txd, 0), (9*self.txd, self.show_size[1]), 3)
        pygame.draw.line(self.captura_to_show, (250, 40, 40), (11*self.txd, 0), (11*self.txd, self.show_size[1]), 3)
        pygame.draw.line(self.captura_to_show, (250, 40, 40), (13*self.txd, 0), (13*self.txd, self.show_size[1]), 3)
        

    def clean(self):
        self.display.fill((84, 185, 72))




