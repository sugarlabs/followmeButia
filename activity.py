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


import os
import sys
sys.path.insert(0, "lib")
import re
import gtk
import pygame
import pygame.camera
from sugar.activity import activity
from sugar.graphics.toolbutton import ToolButton
import sugargame.canvas
import followme
from gettext import gettext as _

class Activity(activity.Activity):

    def __init__(self, handle, create_jobject=True):
        # iniciamos la actividad
        activity.Activity.__init__(self, handle, False)
        # inicializamos el bobot-server
        #self.bobot_launch()
        # seteamos el objeto calibrando
        self.calibrando = True
        # guardo el umbral por defecto
        self.umbral = (25, 25, 25)
        # guardo color calibrado por defecto 'blanco'
        self.colorc = (255, 255, 255)
        # cantidad de pixeles de la mancha
        self.pixeles = 10
        # seteo el tamanio inicial de muestra
        self.tamaniom = (960.0, 720.0)
        # por defecto no se muestra la grilla
        self.mostrar_grilla = False
        # por defecto mostramos la captura en pantalla
        self.mostrar = True
        # creamos una instancia del FollowMe, le pasamos el activity
        self.actividad = followme.FollowMe(self)
        # construimos la barra
        self.build_toolbar()
        # construimos el PygameCanvas
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        # set_canvas implicitamente llama a read_file cuando se llama desde el diario
        self.set_canvas(self._pygamecanvas)
        # comenzamos la actividad (self.game.run es llamada cuando constructor de la actividad vuelve)
        self._pygamecanvas.run_pygame(self.actividad.run)

    def close(self, skip_save=False):
        # evito la entrada al diario
        activity.Activity.close(self, True)

    def build_toolbar(self):
        # obtengo la caja de la actividad
        caja = activity.ActivityToolbox(self)
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

        #####Calibrar#####
        # obtenemos la barra
        barraCalibrar = gtk.Toolbar()

        # creamos el primer item
        item0 = gtk.ToolItem()
        # creamos la etiqueta para calibrar
        self.etiqueta0 = gtk.Label()
        # le ponemos el texto Calibrar/Seguir
        self.etiqueta0.set_text(' ' + _('Calibrate/Follow') + ' ')
        # agrego la etiqueta al item
        item0.add(self.etiqueta0)
        # inserto el item en la barra
        barraCalibrar.insert(item0, 0)

        # ponemos un boton de parar de calibrar
        parar = ToolButton('media-playback-stop')
        # ponemos como mensaje Parar
        parar.set_tooltip(_('Stop'))
        # ponemos la combinacion Ctrl + Espacio
        parar.set_accelerator('<ctrl>space')
        # conectamos el boton con el evento click
        parar.connect('clicked', self.parar_ejecutar)
        # insertamos el boton parar
        barraCalibrar.insert(parar, 1)

        # creo un separador
        separador2 = gtk.SeparatorToolItem()
        # que tenga una linea dibujada
        separador2.props.draw = True
        # inserto el separador
        barraCalibrar.insert(separador2, 2)

        # creamos el segundo item
        item3 = gtk.ToolItem()
        # creo la etiqueta de los pixeles
        self.etiqueta3 = gtk.Label()
        # le coloco el texto Pixeles
        self.etiqueta3.set_text(' ' + _('Calibrated color:') + ' ' + _('Red') + ' ')
        # agrego la etiqueta al item
        item3.add(self.etiqueta3)
        # coloco el item en la barra
        barraCalibrar.insert(item3, 3)

        # creo el sexto item
        item4 = gtk.ToolItem()
        # creo un cuadro para el Rojo
        self.crojoc = gtk.SpinButton()
        # le coloco rango de 0 a 255
        self.crojoc.set_range(0, 255)
        # coloco un incremento de 1
        self.crojoc.set_increments(1, 10)
        # al comienzo tiene el valor rojo del umbral
        self.crojoc.props.value = self.colorc[0]
        #conecto el cuadro con crojoc_valor
        self.crojoc_handler = self.crojoc.connect('notify::value', self.crojoc_valor)
        # coloco el cuadro en el item
        item4.add(self.crojoc)
        # coloco el item en la barra
        barraCalibrar.insert(item4, 4)

        # creo el septimo item
        item5 = gtk.ToolItem()
        # creo la etiqueta para el verde
        self.etiqueta5 = gtk.Label()
        # le coloco G de verde
        self.etiqueta5.set_text(' ' + _('Green') + ' ')
        # coloco la etiqueta en el item
        item5.add(self.etiqueta5)
        # coloco el item en la barra
        barraCalibrar.insert(item5, 5)

        # creo el octavo item
        item6 = gtk.ToolItem()
        # creo el cuadro para el verde
        self.cverdec = gtk.SpinButton()
        # coloco el rango 0 a 255
        self.cverdec.set_range(0, 255)
        # coloco el incremento de a 1
        self.cverdec.set_increments(1, 10)
        # pongo al comienzo el valor del verde del umbral
        self.cverdec.props.value = self.colorc[1]
        # conecto el cuadro con el evento verde_valor
        self.cverdec_handler = self.cverdec.connect('notify::value', self.cverdec_valor)
        # coloco el cuadro en el item
        item6.add(self.cverdec)
        # coloco el item en la barra
        barraCalibrar.insert(item6, 6)

        # creo el septimo item
        item7 = gtk.ToolItem()
        # creo la etiqueta para el verde
        self.etiqueta7 = gtk.Label()
        # le coloco G de verde
        self.etiqueta7.set_text(' ' + _('Blue') + ' ')
        # coloco la etiqueta en el item
        item7.add(self.etiqueta7)
        # coloco el item en la barra
        barraCalibrar.insert(item7, 7)

        # creo el decimo item
        item8 = gtk.ToolItem()
        # creo un cuadro para el azul
        self.cazulc = gtk.SpinButton()
        # coloco el rango 0 a 255
        self.cazulc.set_range(0, 255)
        # coloco el incremento en 1
        self.cazulc.set_increments(1, 10)
        # al comienzo coloco azul del umbral
        self.cazulc.props.value = self.colorc[2]
        # conecto el cuadro al evento cazul_valor
        self.cazulc_handler = self.cazulc.connect('notify::value', self.cazulc_valor)
        # agrego el cuadro al item
        item8.add(self.cazulc)
        # inserto el item en la barra
        barraCalibrar.insert(item8, 8)

        # a la caja le agregamos nuestra barra de Calibrar
        caja.add_toolbar(_('Calibrate'), barraCalibrar)

        #####Opciones#####
        # obtenemos la barra
        barraOpciones = gtk.Toolbar()

        # creamos el primer item
        item9 = gtk.ToolItem()
        # creo la etiqueta de los pixeles
        self.etiqueta9 = gtk.Label()
        # le coloco el texto Pixeles
        self.etiqueta9.set_text(' ' + _('Pixels') + ' ')
        # agrego la etiqueta al item
        item9.add(self.etiqueta9)
        # coloco el item en la barra
        barraOpciones.insert(item9, 0)

        # creo el segundo item
        item10 = gtk.ToolItem()
        # creo un cuadro para el Rojo
        self.cpixeles = gtk.SpinButton()
        # le coloco rango de 0 a 255
        self.cpixeles.set_range(0, 1000)
        # coloco un incremento de 1
        self.cpixeles.set_increments(1, 10)
        # al comienzo tiene el valor rojo del umbral
        self.cpixeles.props.value = self.pixeles
        #conecto el cuadro con crojo_valor
        self.cpixeles_handler = self.cpixeles.connect('notify::value', self.pixeles_valor)
        # coloco el cuadro en el item
        item10.add(self.cpixeles)
        # coloco el item en la barra
        barraOpciones.insert(item10, 1)

        # creo un separador
        separador11 = gtk.SeparatorToolItem()
        # que tenga una linea
        separador11.props.draw = True
        # inserto el separador
        barraOpciones.insert(separador11, 2)

        # creo el cuarto item
        item12 = gtk.ToolItem()
        # creo la etiqueta para umbral
        self.etiqueta12 = gtk.Label()
        # le coloco el texto Umbral
        self.etiqueta12.set_text(' ' + _('Threshold:') + ' ' + _('Red') + ' ')
        # agrego la etiqueta al item
        item12.add(self.etiqueta12)
        # inserto el item en la barra
        barraOpciones.insert(item12, 3)

        # creo el quinto item
        item13 = gtk.ToolItem()
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
        item13.add(self.crojo)
        # coloco el item en la barra
        barraOpciones.insert(item13, 4)

        # creo el sexto item
        item14 = gtk.ToolItem()
        # creo la etiqueta para el verde
        self.etiqueta14 = gtk.Label()
        # le coloco G de verde
        self.etiqueta14.set_text(' ' + _('Green') + ' ')
        # coloco la etiqueta en el item
        item14.add(self.etiqueta14)
        # coloco el item en la barra
        barraOpciones.insert(item14, 5)

         # creo el septimo item
        item15 = gtk.ToolItem()
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
        item15.add(self.cverde)
        # coloco el item en la barra
        barraOpciones.insert(item15, 6)

        # creo el octavo item
        item16 = gtk.ToolItem()
        # creo la etiqueta para el azul
        self.etiqueta16 = gtk.Label()
        # coloco el texto B
        self.etiqueta16.set_text(' ' + _('Blue') + ' ')
        # inserto la etiqueta en el item
        item16.add(self.etiqueta16)
        # inserto el item en la barra
        barraOpciones.insert(item16, 7)

        # creo el noveno item
        item17 = gtk.ToolItem()
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
        item17.add(self.cazul)
        # inserto el item en la barra
        barraOpciones.insert(item17, 8)

        # a la caja le agregamos nuestra barra de Opciones
        caja.add_toolbar(_('Options'), barraOpciones)

        #####Resolucion#####
        # obteenmos la barra
        barraResolucion = gtk.Toolbar()

        # creamos el primer item
        it1 = gtk.ToolItem()
        # creamos la etiqueta para calibrar
        self.et1 = gtk.Label()
        # le ponemos el texto Calibrar
        self.et1.set_text(' ' + _('Show size') + ' ')
        # agrego la etiqueta al item
        it1.add(self.et1)
        # inserto el item en la barra
        barraResolucion.insert(it1, 0)
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
        barraResolucion.insert(it2, 1)
        # creamos el primer item
        it3 = gtk.ToolItem()
        # creamos la etiqueta para calibrar
        self.et2 = gtk.Label()
        # le ponemos el texto Calibrar
        self.et2.set_text(' X ')
        # agrego la etiqueta al item
        it3.add(self.et2)
        # inserto el item en la barra
        barraResolucion.insert(it3, 2)
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
        barraResolucion.insert(it4, 3)
        # creamos el quinto item
        it5 = gtk.ToolItem()
        # creamos la etiqueta para mostrar lineas
        self.et5 = gtk.Label()
        # le ponemos el texto
        self.et5.set_text(' ' + _('Show grid'))
        # agrego la etiqueta al item
        it5.add(self.et5)
        # inserto el item en la barra
        barraResolucion.insert(it5, 4)
        # creo un boton para la grilla
        self.grilla = ToolButton('grid-icon')
        # conecto el evento click y el procedimiento
        self.grilla_handler = self.grilla.connect('clicked', self.grilla_click)
        # inserto el boton grilla en la barra 2
        barraResolucion.insert(self.grilla, 5)
        # creamos el sexto item
        it6 = gtk.ToolItem()
        # creamos la etiqueta para mostrar en pantalla
        self.et6 = gtk.Label()
        # le ponemos el texto
        self.et6.set_text(' ' + _('Show captures') + ' ')
        # agrego la etiqueta al item
        it6.add(self.et6)
        # inserto el item en la barra
        barraResolucion.insert(it6, 6)
        # ponemos un boton de parar de mostrar captura
        parar2 = ToolButton('media-playback-stop')
        # conectamos el boton con el evento click
        parar2.connect('clicked', self.parar_muestra)
        # ponemos como mensaje Ocultar
        parar2.set_tooltip(_('Hide'))
        # insertamos el boton en la barra
        barraResolucion.insert(parar2, 7)

        # agrego la barra2 a la caja (toolbar)
        caja.add_toolbar(_('Resolution'), barraResolucion)

        # la mostramos
        caja.show_all()
        # le ponemos la caja
        self.set_toolbox(caja)

    def acolor(self, color):
        # actualizo la variable local
        self.colorc = color
        # cambio el cuadro rojo
        self.crojoc.props.value = self.colorc[0]
        # cambio el cuadro azul
        self.cverdec.props.value = self.colorc[1]
        # cambio el cuadro verde
        self.cazulc.props.value = self.colorc[2]

    def pixeles_valor(self, pixeles, value):
        # guardo el valor del cuadro
        self.pixeles = int(pixeles.props.value)
        # cambio en FolloMe el umbral
        self.actividad.poner_pixeles(self.pixeles)

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

    def crojoc_valor(self, rojo, value):
        # guardo el valor del cuadro
        r = int(rojo.props.value)
        # si no estoy calibrando
        if not (self.calibrando):
            # actualizo el valor del umbral
            self.colorc = (r, self.colorc[1], self.colorc[2])
            # cambio en FolloMe el umbral
            self.actividad.poner_colorc(self.colorc)

    def cverdec_valor(self, verde, value):
        # guardo el valor del cuadro
        v = int(verde.props.value)
        # si no estoy calibrando
        if not (self.calibrando):
            # actualizo el valor del umbral
            self.colorc = (self.colorc[0], v, self.colorc[2])
            # cambio en FollowMe el umbral
            self.actividad.poner_colorc(self.colorc)

    def cazulc_valor(self, azul, value):
        # guardo el valor del cuadro
        a = int(azul.props.value)
        # si no estoy calibrando
        if not (self.calibrando):
            # actualizo el umbral
            self.colorc = (self.colorc[0], self.colorc[1], a)
            # cambio en FollowMe el valor del umbral
            self.actividad.poner_colorc(self.colorc)

    def tmx_mod(self, tmx, value):
        # guardo el valor del cuadro
        x = float(tmx.props.value)
        # actualizo el tamanio m
        self.tamaniom = (x, float(self.tamaniom[1]))
        # cambio en FollowMe el valor del tamanio
        self.actividad.poner_tamaniom(self.tamaniom)

    def tmy_mod(self, tmy, value):
        # guardo el valor del cuadro
        y = float(tmy.props.value)
        # actualizo el tamanio m
        self.tamaniom = (float(self.tamaniom[0]), y)
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
            boton.set_tooltip(_('Start'))
        else:
            # ponemos parar
            boton.set_icon('media-playback-stop')
            # con el tolltip Detener
            boton.set_tooltip(_('Stop'))

    def grilla_click(self, widget):
        # cambio la variable mostrar_grilla
        self.mostrar_grilla = not self.mostrar_grilla
        # cambio dentro del codigo del FollowMe
        self.actividad.poner_grilla(self.mostrar_grilla)

    def parar_muestra(self, boton):
        #cambio el mostrar
        self.mostrar = not self.mostrar
        # si no mostrar
        if not self.mostrar:
            # ponemos mostrar
            boton.set_icon('media-playback-start')
            # ponemos como mensaje Mostrar
            boton.set_tooltip(_('Show'))
        else:
            # ponemos ocultar
            boton.set_icon('media-playback-stop')
            # ponemos como mensaje Ocultar
            boton.set_tooltip(_('Hide'))
        #actualizo el FollowMe
        self.actividad.poner_muestra(self.mostrar)


