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


import os
import sys
sys.path.insert(0, "lib")
import re
import gtk
import pygame
import pygame.camera
from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbarbox import ToolbarButton
import sugargame.canvas
import followme
from gettext import gettext as _

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1
        self.pixels = 10
        self.threshold = (25, 25, 25)
        self.colorC = (255, 255, 255)
        self.show_size = (960.0, 720.0)
        self.show_grid = False
        self.show_capture = True
        self.calibrating = True
        self.use_threshold_view = True
        self.mode = 'RGB'

        self.followme_activity = followme.FollowMe(self)
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.run_pygame(self.followme_activity.run)


    def build_toolbar(self):

        toolbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()


        ############################## Calibrate ##############################

        calibrate_bar = gtk.Toolbar()

        item1 = gtk.ToolItem()
        label1 = gtk.Label()
        label1.set_text(' ' + _('Calibrate/Follow') + ' ')
        item1.add(label1)
        calibrate_bar.insert(item1, -1)

        stop_calibrate = ToolButton('media-playback-stop')
        stop_calibrate.set_tooltip(_('Stop'))
        stop_calibrate.set_accelerator('<ctrl>space')
        stop_calibrate.connect('clicked', self.stop_execute)
        calibrate_bar.insert(stop_calibrate, -1)

        separator1 = gtk.SeparatorToolItem()
        separator1.props.draw = True
        calibrate_bar.insert(separador1, -1)

        item3 = gtk.ToolItem()
        label3 = gtk.Label()
        label3.set_text(' ' + _('Calibrated color:') + ' ' + _('Red') + ' ')
        item3.add(label3)
        calibrate_bar.insert(item3, -1)

        item4 = gtk.ToolItem()
        self.red_spin = gtk.SpinButton()
        self.red_spin.set_range(0, 255)
        self.red_spin.set_increments(1, 10)
        self.red_spin.props.value = self.colorC[0]
        self.red_spin.connect('notify::value', self.red_spin_color)
        item4.add(self.red_spin)
        calibrate_bar.insert(item4, -1)

        item5 = gtk.ToolItem()
        label5 = gtk.Label()
        label5.set_text(' ' + _('Green') + ' ')
        item5.add(label5)
        calibrate_bar.insert(item5, -1)

        item6 = gtk.ToolItem()
        self.green_spin = gtk.SpinButton()
        self.green_spin.set_range(0, 255)
        self.green_spin.set_increments(1, 10)
        self.green_spin.props.value = self.colorC[1]
        self.green_spin.connect('notify::value', self.green_spin_color)
        item6.add(self.green_spin)
        calibrate_bar.insert(item6, -1)

        item7 = gtk.ToolItem()
        label7 = gtk.Label()
        label7.set_text(' ' + _('Blue') + ' ')
        item7.add(label7)
        calibrate_bar.insert(item7, -1)

        item8 = gtk.ToolItem()
        self.blue_spin = gtk.SpinButton()
        self.blue_spin.set_range(0, 255)
        self.blue_spin.set_increments(1, 10)
        self.blue_spin.props.value = self.colorC[2]
        self.blue_spin.connect('notify::value', self.blue_spin_color)
        item8.add(self.blue_spin)
        calibrate_bar.insert(item8, -1)

        calibrate_bar.show_all()
        calibrate_button = ToolbarButton(label=_('Calibrate'),
                page=calibrate_bar,
                icon_name='preferences-system')
        toolbox.toolbar.insert(calibrate_button, -1)
        calibrate_button.show()


        ############################### Options ###############################

        options_bar = gtk.Toolbar()

        item1 = gtk.ToolItem()
        label1 = gtk.Label()
        label1.set_text(' ' + _('Pixels') + ' ')
        item1.add(label1)
        options_bar.insert(item1, -1)

        item2 = gtk.ToolItem()
        pixels = gtk.SpinButton()
        pixels.set_range(0, 1000)
        pixels.set_increments(1, 10)
        pixels.props.value = self.pixels
        pixels.connect('notify::value', self.pixels_value)
        item2.add(pixels)
        options_bar.insert(item2, -1)

        separator1 = gtk.SeparatorToolItem()
        separator1.props.draw = True
        options_bar.insert(separator1, -1)

        item3 = gtk.ToolItem()
        label3 = gtk.Label()
        label3.set_text(' ' + _('Threshold:') + ' ' + _('Red') + ' ')
        item3.add(label3)
        options_bar.insert(item3, -1)

        item4 = gtk.ToolItem()
        red_spin = gtk.SpinButton()
        red_spin.set_range(0, 255)
        red_spin.set_increments(1, 10)
        red_spin.props.value = self.threshold[0]
        red_spin.connect('notify::value', self.red_spin_threshold)
        item4.add(red_spin)
        options_bar.insert(item4, -1)

        item5 = gtk.ToolItem()
        label5 = gtk.Label()
        label5.set_text(' ' + _('Green') + ' ')
        item5.add(label5)
        options_bar.insert(item5, -1)

        item6 = gtk.ToolItem()
        green_spin = gtk.SpinButton()
        green_spin.set_range(0, 255)
        green_spin.set_increments(1, 10)
        green_spin.props.value = self.threshold[1]
        green_spin.connect('notify::value', self.green_spin_threshold)
        item6.add(green_spin)
        options_bar.insert(item6, -1)

        item7 = gtk.ToolItem()
        label7= gtk.Label()
        label7.set_text(' ' + _('Blue') + ' ')
        item7.add(label7)
        options_bar.insert(item7, -1)

        item8 = gtk.ToolItem()
        blue_spin = gtk.SpinButton()
        blue_spin.set_range(0, 255)
        blue_spin.set_increments(1, 10)
        blue_spin.props.value = self.threshold[2]
        blue_spin.connect('notify::value', self.blue_spin_threshold)
        item8.add(blue_spin)
        options_bar.insert(item8, -1)

        options_bar.show_all()
        options_button = ToolbarButton(label=_('Options'),
                page=options_bar,
                icon_name='view-source')
        toolbox.toolbar.insert(options_button, -1)
        options_button.show()


        ############################## Resolution #############################

        resolution_bar = gtk.Toolbar()

        item1 = gtk.ToolItem()
        label1 = gtk.Label()
        label1.set_text(' ' + _('Show size') + ' ')
        item1.add(label1)
        resolution_bar.insert(item1, -1)

        item2 = gtk.ToolItem()
        x_size_spin = gtk.SpinButton()
        x_size_spin.set_range(160, 1200)
        x_size_spin.set_increments(1, 10)
        x_size_spin.props.value = int(self.show_size[0])
        x_size_spin.connect('notify::value', self.x_size_spin_change)
        item2.add(x_size_spin)
        resolution_bar.insert(item2, -1)

        item3 = gtk.ToolItem()
        label3 = gtk.Label()
        label3.set_text(' X ')
        item3.add(label2)
        resolution_bar.insert(item3, -1)

        item4 = gtk.ToolItem()
        y_size_spin = gtk.SpinButton()
        y_size_spin.set_range(120, 900)
        y_size_spin.set_increments(1, 10)
        y_size_spin.props.value = int(self.show_size[1])
        y_size_spin.connect('notify::value', self.y_size_spin_change)
        item4.add(y_size_spin)
        resolution_bar.insert(item4, -1)

        separator1 = gtk.SeparatorToolItem()
        separator1.props.draw = True
        resolution_bar.insert(separator1, -1)

        item5 = gtk.ToolItem()
        label5 = gtk.Label()
        label5.set_text(' ' + _('Show grid'))
        item5.add(label5)
        resolution_bar.insert(item5, -1)

        grid = ToolButton('grid-icon')
        grid.connect('clicked', self.grid_click)
        resolution_bar.insert(grid, -1)

        separador2 = gtk.SeparatorToolItem()
        separador2.props.draw = True
        resolution_bar.insert(separador2, -1)

        item6 = gtk.ToolItem()
        label6 = gtk.Label()
        label6.set_text(' ' + _('Show captures') + ' ')
        item6.add(label6)
        resolution_bar.insert(item6, -1)

        stop_show = ToolButton('media-playback-stop')
        stop_show.connect('clicked', self.stop_show)
        stop_show.set_tooltip(_('Hide'))
        resolution_bar.insert(stop_show, -1)

        resolution_bar.show_all()
        resolution_button = ToolbarButton(label=_('Resolution'),
                page=resolution_bar,
                icon_name='camera')
        toolbox.toolbar.insert(resolution_button, -1)
        resolution_button.show()

        #######################################################################

        barra_colors = gtk.Toolbar()

        item1 = gtk.ToolItem()
        label1 = gtk.Label()
        label1.set_text(_('Color mode'))
        item1.add(label1)
        barra_colors.insert(item1, -1)

        item2 = gtk.ToolItem()
        combo = Combo()
        item2.add(combo)
        combo.connect('changed', self.change_combo)
        barra_colors.insert(item2, -1)

        separator1 = gtk.SeparatorToolItem()
        separator1.props.draw = True
        barra_colors.insert(separator1, -1)

        item3 = gtk.ToolItem()
        label3 = gtk.Label()
        label3.set_text(_('Show threshold view'))
        item3.add(label3)
        barra_colors.insert(item3, -1)

        threshold_view = ToolButton('media-playback-stop')
        threshold_view.connect('clicked', self.threshold_view)
        threshold_view.set_tooltip(_('Yes'))
        barra_colors.insert(threshold_view, -1)

        colors_button = ToolbarButton(label=_('Colors'),
                page=barra_colors,
                icon_name='toolbar-colors')
        toolbox.toolbar.insert(colors_button, -1)
        colors_button.show()

        barra_colors.show_all()

        #######################################################################

        separador13 = gtk.SeparatorToolItem()
        separador13.props.draw = False
        separador13.set_expand(True)
        toolbox.toolbar.insert(separador13, -1)

        stop_button = StopButton(self)
        stop_button.props.accelerator = _('<Ctrl>Q')
        toolbox.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbox(toolbox)
        toolbox.show()

        self.show_all()

    def change_combo(self, combo):
        self.mode = combo.get_active_text()        
        self.followme_activity.put_color_mode(self.mode)

    def threshold_view(self, button):
        self.use_threshold_view = not self.use_threshold_view
        self.followme_activity.put_threshold_view(self.use_threshold_view)
        if not self.use_threshold_view:
            button.set_icon('media-playback-start')
            button.set_tooltip(_('Yes'))
        else:
            button.set_icon('media-playback-stop')
            button.set_tooltip(_('No'))

    def put_color(self, color):
        self.colorC = color
        self.red_spin.props.value = self.colorC[0]
        self.green_spin.props.value = self.colorC[1]
        self.blue_spin.props.value = self.colorC[2]

    def pixels_value(self, pixels, value):
        self.pixels = int(pixels.props.value)
        self.followme_activity.put_pixels(self.pixels)

    # THRESHOLDS
    def red_spin_threshold(self, red, value):
        r = int(red.props.value)
        self.threshold = (r, self.threshold[1], self.threshold[2])
        self.followme_activity.put_threshold(self.threshold)

    def green_spin_threshold(self, green, value):
        g = int(green.props.value)
        self.threshold = (self.threshold[0], g, self.threshold[2])
        self.followme_activity.put_threshold(self.threshold)

    def blue_spin_threshold(self, blue, value):
        b = int(red.props.value)
        self.threshold = (self.threshold[0], self.threshold[1], b)
        self.followme_activity.put_threshold(self.threshold)

    # COLOR
    def red_spin_color(self, red, value):
        r = int(red.props.value)
        if not (self.calibrating):
            self.colorC = (r, self.colorC[1], self.colorC[2])
            self.followme_activity.put_colorC(self.colorC)

    def green_spin_color(self, green, value):
        g = int(green.props.value)
        if not (self.calibrating):
            self.colorC = (self.colorC[0], g, self.colorC[2])
            self.followme_activity.put_colorC(self.colorC)

    def blue_spin_color(self, blue, value):
        b = int(blue.props.value)
        if not (self.calibrating):
            self.colorC = (self.colorC[0], self.colorC[1], b)
            self.followme_activity.put_colorC(self.colorC)

    # SIZE
    def x_size_spin_change(self, spin, value):
        x = float(spin.props.value)
        self.show_size = (x, self.show_size[1])
        self.followme_activity.put_show_size(self.show_size)

    def y_size_spin_change(self, spin, value):
        y = float(spin.props.value)
        self.show_size = (self.show_size[0], y)
        self.followme_activity.put_show_size(self.show_size)

    def stop_execute(self, button):
        self.calibrating = not self.calibrating
        self.actividad.modocalibrando(self.calibrando)
        if not self.calibrando:
            boton.set_icon('media-playback-start')
            boton.set_tooltip(_('Start'))
        else:
            boton.set_icon('media-playback-stop')
            boton.set_tooltip(_('Stop'))

    def grilla_click(self, button):
        self.show_grid = not self.show_grid
        self.followme_activity.put_grid(self.show_grid)

    def parar_muestra(self, button):
        self.mostrar = not self.mostrar
        if self.mostrar:
            boton.set_icon('media-playback-stop')
            boton.set_tooltip(_('Hide'))
        else:
            boton.set_icon('media-playback-start')
            boton.set_tooltip(_('Show'))
        self.actividad.poner_muestra(self.mostrar)


class Combo(gtk.ComboBox):

    def __init__(self):

        self.liststore = gtk.ListStore(str)

        modes = ('RGB', 'YUV', 'HSV')
        for m in modes:
            self.liststore.append([m])

        gtk.ComboBox.__init__(self, self.liststore)

        cell = gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, 'text', 0)

        self.set_active(0)

