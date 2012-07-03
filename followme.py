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

    def __init__(self, tamanio, modo, parent):
        # iniciamos pygame
        pygame.init()
        # inicializamos el modulo pygame de la camara
        pygame.camera.init()
        # creamos una superfcie para usarla de pantalla
        if parent:
            self.pantalla = pygame.display.get_surface()
        else:
            self.pantalla = pygame.display.set_mode((1200, 900))
        # creamos una superficie para la captura
        self.captura = pygame.surface.Surface(tamanio, 0, self.pantalla)
        # creamos una superficie actualizar
        self.captura2 = pygame.surface.Surface(tamanio, 0, self.pantalla)
        # que no use la vista
        self.use_threshold_view = False
        # inicializo en None la cámara
        self.cam = None
        # obtenemos la camara
        self.get_camera(tamanio, modo)
        # calculamos las proporciones
        self.calc((960, 720))
        # por defecto no mostramos la grilla
        self.mostrar_grilla = False
    
    def get_camera(self, tamanio, modo):
        # detengo la cámara
        if self.cam:
            try:
                self.cam.stop()
            except:
                pass
        
        # obtenemos la lista de camaras
        self.lcamaras = pygame.camera.list_cameras()
        # si no hay ninguna camara
        if self.lcamaras:
            # creamos la camara, con tamanio y modo color RGB
            self.cam = pygame.camera.Camera(self.lcamaras[0], tamanio, modo)
            # obtengo la resolución de la cámara
            res = self.cam.get_size()
            # si no es 320, 240 (Sugar nuevo)
            if not (res == tamanioc):
                tamanio = (352, 288)
                # inicializo en 352, 288
                self.cam = pygame.camera.Camera(self.lcamaras[0], tamanio, modo)
            try:
                # seteamos el brillo
                #self.cam.set_controls(brightness = 129)
                # seteamos flip en horizontal, vertical false
                self.cam.set_controls(True, False)
                # iniciamos la camara
                self.cam.start()
                # obtengo el estado
                res = self.cam.get_controls()
                # guardo si el flip lo hace la cámara
                self.flip = res[0]
            except:
                print _('Error on initialization of the camera')

        else:
            # mandamos el error correspondiente
            print _('No cameras was found')

    def calc(self, tamanio):
        # guardo tamanio en self.tamaniom
        self.tamaniom = tamanio
        # guardo el tamaño de la pantalla
        pantalla_x, pantalla_y = self.pantalla.get_size()
        # calculamos la proporcion en x
        self.c1 = (self.tamaniom[0] / tamanioc[0])
        # calculamos la proporcion en y
        self.c2 = (self.tamaniom[1] / tamanioc[1])
        # coordenada x calibrar
        self.xc = (tamanioc[0] - 50) / 2.0
        # coordenada y calibrar
        self.yc = (tamanioc[1] - 50) / 2.0
        self.xcm = (pantalla_x - 50) / 2.0
        self.ycm = (pantalla_y - 50) / 2.0
        # posicion desde el borde izquierdo en la pantalla
        self.xblit = (pantalla_x - self.tamaniom[0]) / 2
        # posicion desde el borde superior de la pantalla
        self.yblit = (pantalla_y - self.tamaniom[1]) / 2
        # calculamos las divisiones en x
        self.txd = self.tamaniom[0] / 15.0
        # calculamos las divisiones en y
        self.tyd = self.tamaniom[1] / 3.0

    def calibrar(self):
        # guardamos una captura
        self.captura = self.cam.get_image(self.captura)
        # si el flip no lo hace la cámara
        if not(self.flip):
            # giramos la captura, en el horizontal
            self.captura = pygame.transform.flip(self.captura,True,False)
        # obtenemos el color promedio dentro del rectangulo
        color = pygame.transform.average_color(self.captura, (self.xc,self.yc,50,50))
        # rellenamos la pantalla con un color homogeneo
        self.pantalla.fill((84,185,72))
        # escalamos captura al tamanio tamaniom
        self.captura2 = pygame.transform.scale(self.captura, (int(self.tamaniom[0]), int(self.tamaniom[1])))
        # colocamos la captura 2 en la pantalla
        self.pantalla.blit(self.captura2, (self.xblit, self.yblit))
        # dibujamos un rectangulo en el centro de la pantalla
        #FIXME: cambiar posición en función de la pantalla
        
        rect = pygame.draw.rect(self.pantalla, (255,0,0), (self.xcm,self.ycm,50,50), 4)
        # rellenamos la esquina superior con el color calibrado
        self.pantalla.fill(color, (0,0,120,120))
        # recuadramos el color para resaltarlo
        rect = pygame.draw.rect(self.pantalla, (0,0,0), (0,0,120,120), 4)
        # devuelvo el color
        return color

    def obtener_posicion(self, color, umbral, pixeles):
        # guardamos una captura
        self.captura = self.cam.get_image(self.captura)
        # si el flip no lo hace la cámara
        if not(self.flip):
            # giro la captura en el horizontal
            self.captura = pygame.transform.flip(self.captura,True,False)

        
        if self.use_threshold_view:
            pygame.transform.threshold(self.captura2, self.captura, color, (umbral[0],umbral[1], umbral[2]), (0,0,0), 2)
            self.captura = self.captura2

        # creamos una mascara con la captura con color y umbral especificados
        mascara = pygame.mask.from_threshold(self.captura, color, (10, 10, 10))
        # dejamos la mancha conexa mas grande
        conexa = mascara.connected_component()


        # si la mancha tiene al menos tantos pixeles
        if (conexa.count() > pixeles):
            # devolvemos el centro de la mancha
            return mascara.centroid()
        else:
            # sino devolvemos un centro ficticio
            return (-1,-1)

    def mostrar_posicion(self, pos, color):
        # guardo en x e y la posicion
        x, y = pos
        # escalo la captura para mostrar
        self.captura2 = pygame.transform.scale(self.captura, (int(self.tamaniom[0]), int(self.tamaniom[1])))
        # si es una posicion valida
        if (x != -1):
            # creo un punto para mostrar la posicion
            rect = pygame.draw.rect(self.captura2, (255,0,0), (x*self.c1, y*self.c2, 20, 20), 16)
        # rellenamos la pantalla con un color homogeneo
        self.pantalla.fill((84,185,72))
        # si hay que mostrar la grilla
        if (self.mostrar_grilla == True):
            # dibujo la grilla
            self.dibujar_grilla()
        # muestro la captura en pantalla
        self.pantalla.blit(self.captura2, (self.xblit, self.yblit))
        # rellenamos la esquina superior con el color calibrado
        self.pantalla.fill(color, (0,0,120,120))
        # recuadramos el color para resaltarlo
        rect = pygame.draw.rect(self.pantalla, (0,0,0), (0,0,120,120), 4)

    def dibujar_grilla(self):
        # dibujo las zonas verticales
        r0 = pygame.draw.line(self.captura2, (250, 40, 40), (0, self.tyd), (self.tamaniom[0],self.tyd), 3)
        r1 = pygame.draw.line(self.captura2, (250, 40, 40), (0, 2*self.tyd), (self.tamaniom[0], 2*self.tyd), 3)
        # dibujo las zonas horizontales
        r2 = pygame.draw.line(self.captura2, (250, 40, 40), (2*self.txd, 0), (2*self.txd, self.tamaniom[1]), 3)
        r3 = pygame.draw.line(self.captura2, (250, 40, 40), (4*self.txd, 0), (4*self.txd, self.tamaniom[1]), 3)
        r4 = pygame.draw.line(self.captura2, (250, 40, 40), (6*self.txd, 0), (6*self.txd, self.tamaniom[1]), 3)
        r5 = pygame.draw.line(self.captura2, (250, 40, 40), (9*self.txd, 0), (9*self.txd, self.tamaniom[1]), 3)
        r6 = pygame.draw.line(self.captura2, (250, 40, 40), (11*self.txd, 0), (11*self.txd, self.tamaniom[1]), 3)
        r7 = pygame.draw.line(self.captura2, (250, 40, 40), (13*self.txd, 0), (13*self.txd, self.tamaniom[1]), 3)
        

    def limpiar(self):
        # relleno la pantalla con un color homogeneo
        self.pantalla.fill((84, 185, 72))


class Robot(object):

    def __init__(self):
        # calculamos la zona 1 en x
        self.z1 = tamanioc[0] / 15.0
        # calculamos la zona 2 en y
        self.z2 = tamanioc[1] / 3.0
        # inicializamos la velocidades
        self.vel_anterior = (0, 0, 0, 0)
        # lanzamos el bobot
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

        self.modulos = self.butia.get_modules_list()
        # si hay modulos
        if (self.modulos != []):
            # imprimimos la lista de modulos
            print self.modulos
        else:
            # sino se encuentra
            print _('Butia robot was not detected')

    def mover_robot(self, pos):
        # asigno las coordenadas
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
            #self.butiabot.setVelocidadMotores(vel_actual[0], vel_actual[1], vel_actual[2], vel_actual[3])
            self.butia.set2MotorSpeed(str(vel_actual[0]), str(vel_actual[1]), str(vel_actual[2]), str(vel_actual[3]))
    

        # detengo al robot
        #self.butiabot.setVelocidadMotores("0","0", "0", "0")

 




class FollowMe:

    def __init__(self, parent):
        # guardo referencia al padre
        self.parent = parent
        # para manejar la tasa de refresco
        self.clock = pygame.time.Clock()
        # comienzo calibrando
        self.calibrando = True
        # seteamos el tamanio de muestra
        self.tamaniom = (960.0, 720.0)
        
        # creo el robot vacio
        self.r = None
        self.c = None

    def modocalibrando(self, calibrando):
        # seteo el calibrando local
        self.calibrando = calibrando
        # si estoy calibrando
        if self.calibrando:
            # si esta el robot
            if (self.r != None and self.r.modulos != []):
                # detengo el robot
                self.r.butia.set2MotorSpeed('0', '0', '0', '0')
        # si no hay que mostrar
        if (self.mostrar == False):
            # limpio la pantalla
            self.c.limpiar()

    def poner_umbral(self, umbral):
        # guardo el umbral en el local
        self.umbral = umbral

    def poner_colorc(self, colorc):
        # guardo el color calibrado en el local
        if (self.calibrando == False):
            self.colorc = colorc

    def poner_pixeles(self, pixeles):
        # seteo la cantidad de pixeles local
        self.pixeles = pixeles

    def poner_tamaniom(self, tam):
        # seteo el tamanio local con tam
        self.tamaniom = tam
        # recalculo la grilla
        self.c.calc(tam)

    def poner_grilla(self, grilla):
        # seteo la variable local
        self.c.mostrar_grilla = grilla

    def poner_muestra(self, muestra):
        # seteo la variable local
        self.mostrar = muestra
        # si no hay que mostrar
        if (self.mostrar == False):
            # limpio la pantalla
            self.c.limpiar()

    def poner_modo_color(self, modo):
        self.modo = modo
        self.c.get_camera(self.tamanioc, self.modo)

    def poner_threshold_view(self, view):
        self.c.use_threshold_view = view

    def run(self):
        # creamos el robot
        self.r = Robot()
        # establecemos un valor de umbral de color
        self.umbral = (25, 25, 25)
        # establecemos un color a seguir
        self.colorc = (255, 255, 255)
        # establezco un numero de pixeles inicial
        self.pixeles = 10
        # establezco un tamaño incial para mostrar
        self.tamaniom = (960, 720)
        # establezco un tamaño incial para capturar
        self.tamanioc = tamanioc
        # por defecto se muestra la captura
        self.mostrar = True
        # default mode RGB
        self.modo = 'RGB'
        # creamos una captura, inicializamos la camara
        self.c = Captura(self.tamanioc, self.modo, self.parent)
        # si se deteco alguna camara
        if (self.c.cam == None):
            while gtk.events_pending():
                gtk.main_iteration()
            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # salgo
                    break
                #elif event.type == pygame.VIDEORESIZE:
                #    pygame.display.set_mode(event.size, pygame.RESIZABLE)
        else:
            # mientras run
            run = True            
            while run:
                # Pump GTK messages.
                while gtk.events_pending():
                    gtk.main_iteration()
                # Pump PyGame messages.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # salgo
                        run = False
                    #elif event.type == pygame.VIDEORESIZE:
                    #    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                # si es calibrar
                if (self.calibrando):
                    # calibro la camara
                    self.colorc = self.c.calibrar()
                    # actualizo el color en el activity
                    if self.parent:
                        self.parent.acolor(self.colorc)
                else:
                    # obtengo la posicion
                    pos = self.c.obtener_posicion(self.colorc, self.umbral, self.pixeles)
                    # si hay que mostrar la captura en pantalla
                    if self.mostrar:
                        # muestro la posicion en pantalla
                        self.c.mostrar_posicion(pos, self.colorc)
                    # si esta el butia conectado
                    if (self.r != None and self.r.modulos != []):
                        # movemos el robot
                        self.r.mover_robot(pos)
                # actualizo la pantalla
                pygame.display.flip()
                # seteo a 10 CPS (CuadrosPorSegundo)
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

