#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# FollowMe Butia
# Copyright (C) 2010, 2011
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
import gtk
import butiaAPI
import time
from gettext import gettext as _

# seteamos el tamaño de captura
tamanioc = (320, 240)

# velocidad anterior
vel_anterior_x = (0, 0, 0, 0)
vel_anterior_y = (0, 0, 0, 0)

class Captura(object):

    def __init__(self, tamanio):
        # iniciamos pygame
        pygame.init()
        # inicializamos el modulo pygame de la camara
        pygame.camera.init()
        # creamos una superfcie para usarla de pantalla
        self.pantalla = pygame.display.get_surface()
        # creamos una superficie para la captura
        self.captura = pygame.surface.Surface(tamanio, 0, self.pantalla)

        # inicializo en None la cámara
        self.cam = None
        # obtenemos la lista de camaras
        self.lcamaras = pygame.camera.list_cameras()
        # si no hay ninguna camara
        if self.lcamaras:
            # creamos la camara, con tamanio y modo color RGB
            self.cam = pygame.camera.Camera(self.lcamaras[0], tamanio, 'RGB')
            # obtengo la resolución de la cámara
            res = self.cam.get_size()
            # si no es 320, 240 (Sugar nuevo)
            if not (res == tamanioc):
                tamanio = (352, 288)
                # inicializo en 352, 288
                self.cam = pygame.camera.Camera(self.lcamaras[0], tamanio, 'RGB')
            try:
                # seteamos el brillo
                self.cam.set_controls(brightness = 129)
                # seteamos flip en horizontal, vertical false
                self.cam.set_controls(True, False)
                # iniciamos la camara
                self.cam.start()
                # obtengo el estado
                res = self.cam.get_controls()
                # guardo si el flip lo hace la cámara
                self.flip = res[0]
            except:
                print _('Error en la inicialización de la cámara')
            # calculamos las proporciones
            self.calc(tamanio)
            # por defecto no mostramos la grilla
            self.mostrar_grilla = False
        else:
            # mandamos el error correspondiente
            print _('No se encontro ninguna camara.')

    def calc(self, tamanio):
        # guardo tamanio en self.tamaniom
        self.tamaniom = tamanio
        # calculamos la proporcion en x
        self.c1 = (self.tamaniom[0] / tamanioc[0])
        # calculamos la proporcion en y
        self.c2 = (self.tamaniom[1] / tamanioc[1])
        # coordenada x calibrar
        self.xc = (tamanioc[0] - 50) / 2
        # coordenada y calibrar
        self.yc = (tamanioc[1] - 50) / 2
        # posicion desde el borde izquierdo en la pantalla
        self.xblit = (1200 - self.tamaniom[0]) / 2
        # posicion desde el borde superior de la pantalla
        self.yblit = (780 - self.tamaniom[1]) / 2
        # calculamos las divisiones en x
        self.txd = self.tamaniom[0] / 16
        # calculamos las divisiones en y
        self.tyd = self.tamaniom[1] / 3

    def calibrar(self):
        # guardamos una captura
        self.captura = self.cam.get_image(self.captura)
        # si el flip no lo hace la cámara
        if not(self.flip):
            # giramos la captura, en el horizontal
            self.captura = pygame.transform.flip(self.captura,True,False)
        # colocamos la captura en la pantalla
        self.pantalla.blit(self.captura, (0,0))
        # dibujamos un rectangulo en el centro de la pantalla
        rect = pygame.draw.rect(self.pantalla, (255,0,0), (self.xc,self.yc,50,50), 4)
        # obtenemos el color promedio dentro del rectangulo
        color = pygame.transform.average_color(self.captura, rect)
        # rellenamos la pantalla con un color homogeneo
        self.pantalla.fill((84,185,72))
        # escalamos captura al tamanio tamaniom
        self.captura2 = pygame.transform.scale(self.captura, (int(self.tamaniom[0]), int(self.tamaniom[1])))
        # colocamos la captura 2 en la pantalla
        self.pantalla.blit(self.captura2, (self.xblit, self.yblit))
        # dibujamos un rectangulo en el centro de la pantalla
        rect = pygame.draw.rect(self.pantalla, (255,0,0), (575,355,50,50), 4)
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
        # creamos una mascara con la captura con color y umbral especificados
        mascara = pygame.mask.from_threshold(self.captura, color, umbral)
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
        r4 = pygame.draw.line(self.captura2, (250, 40, 40), (7*self.txd, 0), (7*self.txd, self.tamaniom[1]), 3)
        r5 = pygame.draw.line(self.captura2, (250, 40, 40), (9*self.txd, 0), (9*self.txd, self.tamaniom[1]), 3)
        r6 = pygame.draw.line(self.captura2, (250, 40, 40), (12*self.txd, 0), (12*self.txd, self.tamaniom[1]), 3)
        r7 = pygame.draw.line(self.captura2, (250, 40, 40), (14*self.txd, 0), (14*self.txd, self.tamaniom[1]), 3)

    def limpiar(self):
        # relleno la pantalla con un color homogeneo
        self.pantalla.fill((84, 185, 72))


class Robot(object):

    def __init__(self):
        # calculamos la zona 1 en x
        self.z1 = tamanioc[0] / 16
        # calculamos la zona 2 en y
        self.z2 = tamanioc[1] / 3
        # obtenemos el robot
        self.butiabot = butiaAPI.robot()
        wait_counter = 20
        module_list = self.butiabot.listarModulos()
        while((wait_counter > 0) and (module_list == -1)):
            self.butiabot.cerrar()
            self.butiabot = butiaAPI.robot()
            module_list = self.butiabot.listarModulos()
            print("waiting...")
            wait_counter = wait_counter - 1
            time.sleep(0.5)
        if(wait_counter > 0):
            print("bobot OK! ; after " + str(WAIT_FOR_BOBOT - wait_counter) + " trys") 
        else:
            print("bobot NOT OK!") 
        # listamos los modulos
        self.modulos = self.butiabot.listarModulos()
        # si hay modulos
        if (self.modulos != -1):
            # imprimimos la lista de modulos
            print self.modulos
            # abrimos los sensores
            self.butiabot.abrirSensor()
            # abrimos los motores
            self.butiabot.abrirMotores()
        else:
            # sino se encuentra
            print _('No se detecto al robot Butia.')

    def mover_robot(self, pos):
        # asigno las coordenadas
        x,y = pos
        # por defecto espero
        espera = True
        # si esta ligeramente a la izquierda
        if (x > (4*self.z1)) and (x <= (7*self.z1)):
            # me muevo a la derecha v = 300
            vel_actual_x = (1, 300, 0, 300)
        # si esta bastante hacia la izquierda
        elif (x > (2*self.z1)) and (x <= (4*self.z1)):
            # me muevo a la derecha v = 600
            vel_actual_x = (1, 600, 0, 600)
        # si esta a la iquierda
        elif (x <= (2*self.z1)) and (x >= 0):
            # me muevo a la derecha v = 900
            vel_actual_x = (1, 900, 0, 900)
        # si esta ligeramente a la derecha
        elif (x >= (9*self.z1)) and (x < (12*self.z1)):
            # me muevo a la izquierda v = 300
            vel_actual_x = (0, 300, 1, 300)
        # si esta bastante hacia la derecha
        elif (x >= 12*self.z1) and (x < 14*self.z1):
            # me muevo a la izquierda v = 600
            vel_actual_x = (0, 600, 1, 600)
        # si esta a la derecha
        elif (x >= (14*self.z1)):
            # me muevo a la izquierda v = 900
            vel_actual_x = (0, 900, 1, 900)
        # si esta en la zona muerta
        elif (x > 7*self.z1) and (x < 9*self.z1):
            # no espero
            espera = False


        # para evitar envios de velocidad (eje X) innecesarios al robot
        if not(vel_actual_x == vel_anterior_x):
            vel_anterior_x = vel_actual_x
            self.butiabot.setVelocidadMotores(vel_actual_x[0], vel_actual_x[1], vel_actual_x[2], vel_actual_x[4])
            # si hay espera
            if (espera == True):
                # giro durante 0.1 segundos
                time.sleep(0.1)
        # devuelvo el valor de espera
        espera = True
        # si esta abajo
        if (y <= self.z2) and (y >= 0):
            # me muevo hacia adelante
            vel_actual_y = (1, 500, 1, 500)
        # si esta ariba
        elif (y >= 2*self.z2):
            # me muevo hacia atras
            vel_actual_y = (0, 500, 0, 500)
        # si esta en la zona muerta
        elif (y > self.z2) and (y < 2*self.z2):
            # no espero
            espera = False

        # para evitar envios de velocidad (eje Y) innecesarios al robot
        if not(vel_actual_y == vel_anterior_y):
            vel_anterior_y = vel_actual_y
            self.butiabot.setVelocidadMotores(vel_actual_y[0], vel_actual_y[1], vel_actual_y[2], vel_actual_y[4])
            # si hay espera
            if (espera == True):
                # giro durante 0.1 segundos
                time.sleep(0.1)



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

    def modocalibrando(self, calibrando):
        # seteo el calibrando local
        self.calibrando = calibrando
        # si estoy calibrando
        if self.calibrando:
            # detengo el robot
            self.butiabot.setVelocidadMotores(0, 0, 0, 0)
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

    def run(self):
        # creamos el robot
        r = Robot()
        # establecemos un valor de umbral de color
        self.umbral = (25, 25, 25)
        # establecemos un color a seguir
        self.colorc = (255, 255, 255)
        # establezco un numero de pixeles inicial
        self.pixeles = 10
        # establezco un tamaño incial para mostrar
        self.tamanioi = (960.0, 720.0)
        # establezco un tamaño incial para capturar
        self.tamanioc = tamanioc
        # por defecto se muestra la captura
        self.mostrar = True
        # creamos una captura, inicializamos la camara
        self.c = Captura(self.tamanioc)
        # si se deteco alguna camara
        if (self.c.cam == None):
            while gtk.events_pending():
                gtk.main_iteration()
            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # salgo
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
        else:
            # mientras True
            while True:
                # Pump GTK messages.
                while gtk.events_pending():
                    gtk.main_iteration()
                # Pump PyGame messages.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # salgo
                        return
                    elif event.type == pygame.VIDEORESIZE:
                        pygame.display.set_mode(event.size, pygame.RESIZABLE)
                # si es calibrar
                if (self.calibrando):
                    # calibro la camara
                    self.colorc = self.c.calibrar()
                    # actualizo el color en el activity
                    self.parent.acolor(self.colorc)
                else:
                    # obtengo la posicion
                    pos = self.c.obtener_posicion(self.colorc, self.umbral, self.pixeles)
                    # si hay que mostrar la captura en pantalla
                    if self.mostrar:
                        # muestro la posicion en pantalla
                        self.c.mostrar_posicion(pos, self.colorc)
                    # si esta el butia conectado
                    if (r.modulos != -1):
                        # movemos el robot
                        r.mover_robot(pos)
                # actualizo la pantalla
                pygame.display.flip()
                # seteo a 10 CPS (CuadrosPorSegundo)
                self.clock.tick(10)
