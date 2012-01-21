#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# FollowMe
# Copyright (C) 2010
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

# seteamos el tamaño de captura
tamanioc = (320, 240)

class Captura(object):

        def __init__(self, tamaniom):
                # creamos una superfcie para usarla de pantalla
		self.pantalla = pygame.display.get_surface()		
		# creamos una superficie para la captura
		self.captura = pygame.surface.Surface(tamanioc, 0, self.pantalla)
                # inicializamos el modulo pygame de la camara
                pygame.camera.init()
                # obtenemos la lista de camaras
                self.lcamaras = pygame.camera.list_cameras()
                # si no hay ninguna camara
                if not self.lcamaras:
                        # mandamos el error correspondiente
                        raise ValueError("No  se encontro ninguna camara.")
                else:
                        # creamos la camara, con tamanio y modo color RGB
                        self.cam = pygame.camera.Camera(self.lcamaras[0], tamanioc, 'RGB')
       			# iniciamos la camara
			self.cam.start()
			self.calc(tamaniom)

	def calc(self, tamaniom):
		# calculamos la proporcion en x
		self.c1 = tamaniom[0] / 320
		# calculamos la proporcion en y
		self.c2 = tamaniom[1] / 240
		# coordenada x calibrar
		self.xc = (tamanioc[0] - 50) / 2
		# coordenada y calibrar
		self.yc = (tamanioc[1] - 50) / 2
		# posicion desde el borde izquierdo en la pantalla
		self.xblit = (1200 - tamaniom[0]) / 2
		# posicion desde el borde superior de la pantalla
		self.yblit = (780 - tamaniom[1]) / 2

	def calibrar(self, tamaniom):
                # guardamos una captura
                self.captura = self.cam.get_image(self.captura)
                # giramos la captura, en el horizontal
                self.captura = pygame.transform.flip(self.captura,True,False)
		# colocamos la captura en la pantalla
                self.pantalla.blit(self.captura, (0,0))
                # dibujamos un rectangulo en el centro de la pantalla
                rect = pygame.draw.rect(self.pantalla, (255,0,0), (self.xc,self.yc,50,50), 4)
                # obtenemos el color promedio dentro del rectangulo
                self.color = pygame.transform.average_color(self.captura, rect)
                # rellenamos la pantalla con un color homogeneo
                self.pantalla.fill((84,185,72))
		# escalamos captura al tamanio tamaniom
		self.captura2 = pygame.transform.scale(self.captura, tamaniom)
                # colocamos la captura 2 en la pantalla
                self.pantalla.blit(self.captura2, (self.xblit, self.yblit))
                # dibujamos un rectangulo en el centro de la pantalla
                rect = pygame.draw.rect(self.pantalla, (255,0,0), (575,355,50,50), 4)
		# rellenamos la esquina superior con el color calibrado
                self.pantalla.fill(self.color, (0,0,120,120))
		# recuadramos el color para resaltarlo
		rect = pygame.draw.rect(self.pantalla, (0,0,0), (0,0,120,120), 4)

	def obtener_posicion(self, umbral, pixeles):
                # guardamos una captura
                self.captura = self.cam.get_image(self.captura)
		# giro la captura en el horizontal
                self.captura = pygame.transform.flip(self.captura,True,False)
                # creamos una mascara con la captura con color y umbral especificados
                mascara = pygame.mask.from_threshold(self.captura, self.color, umbral)
                # dejamos la mancha conexa mas grande
                conexa = mascara.connected_component()
                # si la mancha tiene al menos tantos pixeles
                if (conexa.count() > pixeles):
                        # devolvemos el centro de la mancha
                        return mascara.centroid()
                else:
                        # sino devolvemos un centro ficticio
			return (-1,-1)

	def mostrar_posicion(self, pos, tamaniom):
		# guardo en x e y la posicion
		x, y = pos
		# escalo la captura para mostrar
		self.captura2 = pygame.transform.scale(self.captura, tamaniom)
                # si es una posicion valida
                if (x != -1):
                        # creo un punto para mostrar la posicion
        		rect = pygame.draw.rect(self.captura2, (255,0,0), (x*self.c1, y*self.c2, 20, 20), 16)
		# rellenamos la pantalla con un color homogeneo
		self.pantalla.fill((84,185,72))
		# muestro la captura en pantalla
		self.pantalla.blit(self.captura2, (self.xblit, self.yblit))
		# rellenamos la esquina superior con el color calibrado
                self.pantalla.fill(self.color, (0,0,120,120))
		# recuadramos el color para resaltarlo
                rect = pygame.draw.rect(self.pantalla, (0,0,0), (0,0,120,120), 4)


class Robot(object):   

	def __init__(self):
		# calculamos la zona 1 en x
		self.z1 = tamanioc[0] / 16
		# calculamos la zona 2 en y
		self.z2 = tamanioc[1] / 3
		# obtenemos el robot
		self.butiabot = butiaAPI.robot()
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
                        print "No se detecto al Butia."

	def mover_robot(self, pos):
		# asigno las coordenadas		
		x,y = pos
		# si el robot se encuentra
		if (self.modulos != -1):
			# por defecto espero
			espera = True
			# si esta ligeramente a la izquierda
			if (x > (4*self.z1)) and (x <= (7*self.z1)):
				# me muevo a la derecha v = 300
				self.butiabot.setVelocidadMotores("1","300", "0", "300")
			# si esta bastante hacia la izquierda
			elif (x > (2*self.z1)) and (x <= (4*self.z1)):
				# me muevo a la derecha v = 600
				self.butiabot.setVelocidadMotores("1","600", "0", "600")
			# si esta a la iquierda
			elif (x <= (2*self.z1)) and (x >= 0):
				# me muevo a la derecha v = 900
				self.butiabot.setVelocidadMotores("1","900", "0", "900")
			# si esta ligeramente a la derecha
			elif (x >= (9*self.z1)) and (x < (12*self.z1)):
				# me muevo a la izquierda v = 300
				self.butiabot.setVelocidadMotores("0","300", "1", "300")
			# si esta bastante hacia la derecha
			elif (x >= 12*self.z1) and (x < 14*self.z1):
				# me muevo a la izquierda v = 600
				self.butiabot.setVelocidadMotores("0","600", "1", "600")
			# si esta a la derecha
			elif (x >= (14*self.z1)):
				# me muevo a la izquierda v = 900
				self.butiabot.setVelocidadMotores("0","900", "1", "900")
			# si esta en la zona muerta
			elif (x > 7*self.z1) and (x < 9*self.z1):
				# no espero
				espera = False
			# si hay espera
			if (espera == True):
				# giro durante 0.1 segundos
				time.sleep(0.1)
			# devuelvo el valor de espera
			espera = True
			# si esta abajo
			if (y <= self.z2) and (y >= 0):
				# me muevo hacia adelante				
				self.butiabot.setVelocidadMotores("1","500", "1", "500")
			# si esta ariba			
			elif (y >= 2*self.z2):
				# me muevo hacia atras				
				self.butiabot.setVelocidadMotores("0","500", "0", "500")
			# si esta en la zona muerta
			elif (y > self.z2) and (y < 2*self.z2):
				# no espero
				espera = False
			# si hay espera
			if (espera == True):
				# me muevo durante 0.1 segundos			
				time.sleep(0.1)
			# detengo al robot
			self.butiabot.setVelocidadMotores("0","0", "0", "0")


class FollowMe:

    def __init__(self):
        # para manejar la tasa de refresco
        self.clock = pygame.time.Clock()
	# comienzo calibrando
        self.calibrando = True

    def modocalibrando(self, calibrando):
	# seteo el calibrando local        
	self.calibrando = calibrando

    def poner_umbral(self, umbral):
	# guardo el umbral en el local
        self.umbral = umbral
  
    def poner_pixeles(self, pixeles):
	# seteo la cantidad de pixeles local
        self.pixeles = pixeles

    def poner_tamaniom(self, tam):
	# seteo el tamanio local con tam
        self.tamaniom = tam
	self.c.calc(tam)

    def run(self):
	# creamos el robot
        r = Robot()
        # establecemos un valor de umbral de color
        self.umbral = (25, 25, 25)
	# establezco un numero de pixeles inicial
	self.pixeles = 10
	# establezco un tamaño incial
	self.tamaniom = (960, 720)
        # creamos una captura
        self.c = Captura(self.tamaniom)
        # obligamos a que se ejecute el while
        ejecutar = True
        # mientras ejecutar
	while ejecutar:
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
			self.c.calibrar(self.tamaniom)
		else:
			# obtengo la posicion
			pos = self.c.obtener_posicion(self.umbral, self.pixeles)
			# muestro la posicion en pantalla
			self.c.mostrar_posicion(pos, self.tamaniom)
			# movemos el robot
			r.mover_robot(pos)
		# actualizo la pantalla
		pygame.display.flip()              
		# seteo a 10 CPS (CuadrosPorSegundo)
		self.clock.tick(10)
