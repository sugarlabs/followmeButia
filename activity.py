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


import sys
sys.path.insert(0, '/home/olpc/Activities/FollowMe.activity')
import re
import gtk
import pygame
import pygame.camera
from sugar.activity import activity
import sugar.graphics.toolbutton
import sugargame.canvas
import followme


class Activity(activity.Activity):

	def __init__(self, handle):
		# iniciamos la actividad
		activity.Activity.__init__(self, handle)        
		# seteamos el objeto calibrando
		self.calibrando = True
		# guardo el umbral por defecto
		self.umbral = (25, 25, 25)
		# seteo el tamanio inicial de muestra
		self.tamaniom = (960, 720)
		# creamos una isntancia del FollowMe
		self.actividad = followme.FollowMe()
		# construimos la barra
		self.build_toolbar()
		# construimos el PygameCanvas
		self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
		# set_canvas implicitamente llama a read_file cuando se llama desde el diario
		self.set_canvas(self._pygamecanvas)
		# comenzamos la actividad (self.game.run es llamada cuando constructor de la actividad vuelve)
		self._pygamecanvas.run_pygame(self.actividad.run)

	def build_toolbar(self):        
		# ponemos un boton de parar de calibrar
		parar = sugar.graphics.toolbutton.ToolButton('media-playback-stop')
		# ponemos como mensaje Parar
		parar.set_tooltip("Parar")
		# ponemos la combinacion Ctrl + Espacio
		parar.set_accelerator(('<ctrl>space'))
		# conectamos el boton con el evento click
		parar.connect('clicked', self.parar_ejecutar)
		# obteenmos la barra
		barra = gtk.Toolbar()
		# creamos el primer item
		item1 = gtk.ToolItem()
		# creamos la etiqueta para calibrar
                self.etiqueta1 = gtk.Label()
		# le ponemos el texto Calibrar
                self.etiqueta1.set_text(' Calibrar ')
		# agrego la etiqueta al item
		item1.add(self.etiqueta1)
		# inserto el item en la barra
                barra.insert(item1, 0)
		# insertamos el boton parar
		barra.insert(parar, 1)
		# creamos el segundo item
		item2 = gtk.ToolItem()
		# creo la etiqueta de los pixeles
		self.etiqueta2 = gtk.Label()
		# le coloco el texto Pixeles
		self.etiqueta2.set_text(' Pixeles ')
		# agrego la etiqueta al item
		item2.add(self.etiqueta2)
		# coloco el item en la barra
		barra.insert(item2, 2)
		# creo el tercer item
		item3 = gtk.ToolItem()
		# creo un cuadro de entrada
		self.pixeles = gtk.Entry()
		# colocamos 10 al comienzo
                self.pixeles.set_text('10')
		# ponemos alineacion derecha
                self.pixeles.set_alignment(1)
		# ponemos ancho de 3 caracteres
                self.pixeles.set_width_chars(3)
		# conectamos el cuadro con el evento insertar
		self.pixeles.connect('insert-text', self.pixeles_insertar)
		# conectamos el cuadro con el elemento activar
        	self.pixeles.connect('activate', self.pixeles_activar)
		# agrego el cuadro al item
		item3.add(self.pixeles)
		# inserto el item en la barra
		barra.insert(item3, 3)
		# creo un separador
		separador = gtk.SeparatorToolItem()
		# que tenga una linea
                separador.props.draw = True
		# inserto el separador
                barra.insert(separador, 4)
		# creo el item 5
		item5 = gtk.ToolItem()
		# creo la etiqueta para umbral
                self.etiqueta5 = gtk.Label()
		# le coloco el texto Umbral
                self.etiqueta5.set_text(' Umbral:  Rojo ')
		# agrego la etiqueta al item
                item5.add(self.etiqueta5)
		# inserto el item en la barra
                barra.insert(item5, 5)
		# creo el sexto item
		item6 = gtk.ToolItem()
		# creo un cuadro para el Rojo
		self.crojo = gtk.SpinButton()
		# le coloco rango de 0 a 255
		self.crojo.set_range(0, 255)
		# coloco un incremento de 1
		self.crojo.set_increments(1, 10)
		# al comienzo tiene el valor rojo del umbral
		self.crojo.props.value = self.umbral[0]
		#conecto el cuadro con crojo_valor
		self.crojo_handler = self.crojo.connect('notify::value', self.crojo_valor)
		# coloco el cuadro en el item
		item6.add(self.crojo)
		# coloco el item en la barra
		barra.insert(item6, 6)
		# creo el septimo item
		item7 = gtk.ToolItem()
		# creo la etiqueta para el verde
                self.etiqueta7 = gtk.Label()
		# le coloco G de verde
		self.etiqueta7.set_text('  Verde ')
		# coloco la etiqueta en el item
		item7.add(self.etiqueta7)
		# coloco el item en la barra
                barra.insert(item7, 7)
 		# creo el octavo item
		item8 = gtk.ToolItem()
		# creo el cuadro para el verde
                self.cverde = gtk.SpinButton()
		# coloco el rango 0 a 255
                self.cverde.set_range(0, 255)
		# coloco el incremento de a 1
                self.cverde.set_increments(1, 10)
		# pongo al comienzo el valor del verde del umbral
		self.cverde.props.value = self.umbral[1]
		# conecto el cuadro con el evento verde_valor
		self.cverde_handler = self.cverde.connect('notify::value', self.cverde_valor)
		# coloco el cuadro en el item
		item8.add(self.cverde)
		# coloco el item en la barra
		barra.insert(item8, 8)
		# creo el noveno item
		item9 = gtk.ToolItem()
		# creo la etiqueta para el azul
                self.etiqueta9 = gtk.Label()
		# coloco el texto B
                self.etiqueta9.set_text('  Azul ')
                # inserto la etiqueta en el item
		item9.add(self.etiqueta9)
		# inserto el item en la barra
                barra.insert(item9, 9)
		# creo el decimo item
		item10 = gtk.ToolItem()
		# creo un cuadro para el azul
                self.cazul = gtk.SpinButton()
		# coloco el rango 0 a 255
                self.cazul.set_range(0, 255)
		# coloco el incremento en 1
                self.cazul.set_increments(1, 10)
		# al comienzo coloco azul del umbral
		self.cazul.props.value = self.umbral[2]
		# conecto el cuadro al evento cazul_valor
		self.cazul_handler = self.cazul.connect('notify::value', self.cazul_valor)
		# agrego el cuadro al item
		item10.add(self.cazul)
		# inserto el item en la barra
                barra.insert(item10, 10)
		# obtengo la caja de la actividad
		caja = sugar.activity.activity.ActivityToolbox(self)
		# obtengo la barra de Actividad
		barra_actividad = caja.get_activity_toolbar()
		# le saco la opcion guardar
		barra_actividad.remove(barra_actividad.keep)
		# le coloco none
		barra_actividad.keep = None
		# le saco el boton compartir actividad
		barra_actividad.remove(barra_actividad.share)
		# le coloco none
		barra_actividad.share = None
                # alacaja le agregamos nuestra barra de Opciones
                caja.add_toolbar("Opciones", barra)
		# obteenmos la barra
                barra2 = gtk.Toolbar()
                # creamos el primer item
                it1 = gtk.ToolItem()
                # creamos la etiqueta para calibrar
                self.et1 = gtk.Label()
                # le ponemos el texto Calibrar
                self.et1.set_text(' Tamaño muestra ')
                # agrego la etiqueta al item
                it1.add(self.et1)
                # inserto el item en la barra
                barra2.insert(it1, 0)
                # creo el decimo item
                it2 = gtk.ToolItem()
                # creo un cuadro para el azul
                self.tmx = gtk.SpinButton()
                # coloco el rango 0 a 255
                self.tmx.set_range(160, 1200)
                # coloco el incremento en 1
                self.tmx.set_increments(1, 10)
                # al comienzo coloco azul del umbral
                self.tmx.props.value = 960
                # conecto el cuadro al evento cazul_valor
                self.tamx = self.tmx.connect('notify::value', self.tmx_mod)
                # agrego el cuadro al item
                it2.add(self.tmx)
		# inserto el item a la barra
		barra2.insert(it2, 1)
		# creamos el primer item
                it3 = gtk.ToolItem()
                # creamos la etiqueta para calibrar
                self.et2 = gtk.Label()
                # le ponemos el texto Calibrar
                self.et2.set_text(' X ')
                # agrego la etiqueta al item
                it3.add(self.et2)
                # inserto el item en la barra
                barra2.insert(it3, 2)
		# creo el decimo item
                it4 = gtk.ToolItem()
                # creo un cuadro para el azul
                self.tmy = gtk.SpinButton()
                # coloco el rango 0 a 255
                self.tmy.set_range(120, 900)
                # coloco el incremento en 1
                self.tmy.set_increments(1, 10)
                # al comienzo coloco azul del umbral
                self.tmy.props.value = 720
                # conecto el cuadro al evento cazul_valor
                self.tamy = self.tmy.connect('notify::value', self.tmy_mod)
                # agrego el cuadro al item
                it4.add(self.tmy)
                # inserto el item a la barra
                barra2.insert(it4, 3)
		# agrego la barra2 a la caja (toolbar)
		caja.add_toolbar("Resolución", barra2)
		# la mostramos
                caja.show_all()
                # le ponemos la caja
                self.set_toolbox(caja)

	def pixeles_insertar(self, entry, text, length, position):
		# si no es un numero
		if not re.match('[0-9]', text):
			# no ingreso datos
			entry.emit_stop_by_name('insert-text')
			# devuelvo True
			return True
		# devuelvo False
		return False

	def pixeles_activar(self, entry):
		# si no esta vacio
		if entry.props.text:
			# guardo el numero ingresado
			p = int(entry.props.text)
		else:
			# sino guardo 0
			p = 0
		# cambio en FollowMe la cantidad de pixeles a seguir
		self.actividad.poner_pixeles(p)

	def crojo_valor(self, rojo, value):
		# guardo el valor del cuadro
		r = int(rojo.props.value)
		# actualizo el valor del umbral
		self.umbral = (r, self.umbral[1], self.umbral[2])
		# cambio en FolloMe el umbral
		self.actividad.poner_umbral(self.umbral)

	def cverde_valor(self, verde, value):
		# guardo el valor del cuadro
		v = int(verde.props.value)
		# actualizo el valor del umbral
		self.umbral = (self.umbral[0], v, self.umbral[2])
		# cambio en FollowMe el umbral
		self.actividad.poner_umbral(self.umbral)

	def cazul_valor(self, azul, value):
		# guardo el valor del cuadro
		a = int(azul.props.value)
		# actualizo el umbral
		self.umbral = (self.umbral[0], self.umbral[1], a)
		# cambio en FollowMe el valor del umbral		
		self.actividad.poner_umbral(self.umbral)

	def tmx_mod(self, tmx, value):
                # guardo el valor del cuadro
                x = int(tmx.props.value)
                # actualizo el tamanio m
                self.tamaniom = (x, self.tamaniom[1])
                # cambio en FollowMe el valor del tamanio
                self.actividad.poner_tamaniom(self.tamaniom)

	def tmy_mod(self, tmy, value):
                # guardo el valor del cuadro
                y = int(tmy.props.value)
                # actualizo el tamanio m
                self.tamaniom = (self.tamaniom[0], y)
                # cambio en FollowMe el valor del tamanio
                self.actividad.poner_tamaniom(self.tamaniom)

	def parar_ejecutar(self, boton):
		# activamos o desactivamos el modo calibrar
		self.calibrando = not self.calibrando
		# seteamos el modo dentro de la actividad
		self.actividad.modocalibrando(self.calibrando)
		# actualizamos la barra para el siguiente evento
		if not self.calibrando:
			# ponemos ejecutar
			boton.set_icon('media-playback-start')
			# con el tolltip Empezar
			boton.set_tooltip("Empezar")
		else:
			# ponemos parar
			boton.set_icon('media-playback-stop')
			# con el tolltip Detener
			boton.set_tooltip("Detener")
