#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# FollowMe Butia
# Copyright (C) 2010-2013
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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbarbox import ToolbarButton
import sugargame.canvas
import main
import pygame
from gettext import gettext as _

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1
        self.pixels = 10
        self.brightness = 128
        self.threshold = (25, 25, 25)
        self.colorC = (255, 255, 255)
        self.show_size = (960.0, 720.0)
        self.show_grid = False
        self.calibrating = True
        self.use_threshold_view = True
        self.use_outline_view = True
        self.use_rects_view = True
        self.mode = 'RGB'

        self.followme_activity = main.Main(self)
        self.followme_activity.canvas = sugargame.canvas.PygameCanvas(
                self,
                main=self.followme_activity.run,
                modules=[pygame.display, pygame.font])
        self.set_canvas(self.followme_activity.canvas)
        self.build_toolbar()

    def build_toolbar(self):

        toolbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()

        self.build_calibrate_toolbar(toolbox)
        self.build_options_toolbar(toolbox)
        self.build_resolution_toolbar(toolbox)
        self.build_colors_toolbar(toolbox)

        separador13 = Gtk.SeparatorToolItem()
        separador13.props.draw = False
        separador13.set_expand(True)
        toolbox.toolbar.insert(separador13, -1)

        stop_button = StopButton(self)
        stop_button.props.accelerator = _('<Ctrl>Q')
        toolbox.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbox)
        toolbox.show()

        self.show_all()

    def build_calibrate_toolbar(self, toolbox):

        calibrate_bar = Gtk.Toolbar()

        item1 = Gtk.ToolItem()
        label1 = Gtk.Label()
        label1.set_text(' ' + _('Calibrate/Follow') + ' ')
        item1.add(label1)
        calibrate_bar.insert(item1, -1)

        stop_calibrate = ToolButton('media-playback-stop')
        stop_calibrate.set_tooltip(_('Stop'))
        stop_calibrate.set_accelerator('<ctrl>space')
        stop_calibrate.connect('clicked', self.stop_execute)
        calibrate_bar.insert(stop_calibrate, -1)

        separator1 = Gtk.SeparatorToolItem()
        separator1.props.draw = True
        calibrate_bar.insert(separator1, -1)

        item3 = Gtk.ToolItem()
        self.label_color_red = Gtk.Label()
        self.label_color_red.set_text(' ' + _('Calibrated color:') + ' ' + _('Red') + ' ')
        item3.add(self.label_color_red)
        calibrate_bar.insert(item3, -1)

        item4 = Gtk.ToolItem()
        self.red_spin = Gtk.SpinButton()
        self.red_spin.set_range(0, 255)
        self.red_spin.set_increments(1, 10)
        self.red_spin.props.value = self.colorC[0]
        self.red_spin.connect('notify::value', self.red_spin_color)
        item4.add(self.red_spin)
        calibrate_bar.insert(item4, -1)

        item5 = Gtk.ToolItem()
        self.label_color_green = Gtk.Label()
        self.label_color_green.set_text(' ' + _('Green') + ' ')
        item5.add(self.label_color_green)
        calibrate_bar.insert(item5, -1)

        item6 = Gtk.ToolItem()
        self.green_spin = Gtk.SpinButton()
        self.green_spin.set_range(0, 255)
        self.green_spin.set_increments(1, 10)
        self.green_spin.props.value = self.colorC[1]
        self.green_spin.connect('notify::value', self.green_spin_color)
        item6.add(self.green_spin)
        calibrate_bar.insert(item6, -1)

        item7 = Gtk.ToolItem()
        self.label_color_blue = Gtk.Label()
        self.label_color_blue.set_text(' ' + _('Blue') + ' ')
        item7.add(self.label_color_blue)
        calibrate_bar.insert(item7, -1)

        item8 = Gtk.ToolItem()
        self.blue_spin = Gtk.SpinButton()
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


    def build_options_toolbar(self, toolbox):

        options_bar = Gtk.Toolbar()

        item1 = Gtk.ToolItem()
        label1 = Gtk.Label()
        label1.set_text(' ' + _('Pixels') + ' ')
        item1.add(label1)
        options_bar.insert(item1, -1)

        item2 = Gtk.ToolItem()
        pixels = Gtk.SpinButton()
        pixels.set_range(0, 1000)
        pixels.set_increments(1, 10)
        pixels.props.value = self.pixels
        pixels.connect('notify::value', self.pixels_value)
        item2.add(pixels)
        options_bar.insert(item2, -1)

        separator1 = Gtk.SeparatorToolItem()
        separator1.props.draw = True
        options_bar.insert(separator1, -1)

        item3 = Gtk.ToolItem()
        self.label_threshold_red = Gtk.Label()
        self.label_threshold_red.set_text(' ' + _('Threshold:') + ' ' + _('Red') + ' ')
        item3.add(self.label_threshold_red)
        options_bar.insert(item3, -1)

        item4 = Gtk.ToolItem()
        red_spin = Gtk.SpinButton()
        red_spin.set_range(0, 255)
        red_spin.set_increments(1, 10)
        red_spin.props.value = self.threshold[0]
        red_spin.connect('notify::value', self.red_spin_threshold)
        item4.add(red_spin)
        options_bar.insert(item4, -1)

        item5 = Gtk.ToolItem()
        self.label_threshold_green = Gtk.Label()
        self.label_threshold_green.set_text(' ' + _('Green') + ' ')
        item5.add(self.label_threshold_green)
        options_bar.insert(item5, -1)

        item6 = Gtk.ToolItem()
        green_spin = Gtk.SpinButton()
        green_spin.set_range(0, 255)
        green_spin.set_increments(1, 10)
        green_spin.props.value = self.threshold[1]
        green_spin.connect('notify::value', self.green_spin_threshold)
        item6.add(green_spin)
        options_bar.insert(item6, -1)

        item7 = Gtk.ToolItem()
        self.label_threshold_blue = Gtk.Label()
        self.label_threshold_blue.set_text(' ' + _('Blue') + ' ')
        item7.add(self.label_threshold_blue)
        options_bar.insert(item7, -1)

        item8 = Gtk.ToolItem()
        blue_spin = Gtk.SpinButton()
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


    def build_resolution_toolbar(self, toolbox):

        resolution_bar = Gtk.Toolbar()

        item1 = Gtk.ToolItem()
        label1 = Gtk.Label()
        label1.set_text(' ' + _('Show size') + ' ')
        item1.add(label1)
        resolution_bar.insert(item1, -1)

        item2 = Gtk.ToolItem()
        x_size_spin = Gtk.SpinButton()
        x_size_spin.set_range(160, 1200)
        x_size_spin.set_increments(1, 10)
        x_size_spin.props.value = int(self.show_size[0])
        x_size_spin.connect('notify::value', self.x_size_spin_change)
        item2.add(x_size_spin)
        resolution_bar.insert(item2, -1)

        item3 = Gtk.ToolItem()
        label3 = Gtk.Label()
        label3.set_text(' X ')
        item3.add(label3)
        resolution_bar.insert(item3, -1)

        item4 = Gtk.ToolItem()
        y_size_spin = Gtk.SpinButton()
        y_size_spin.set_range(120, 900)
        y_size_spin.set_increments(1, 10)
        y_size_spin.props.value = int(self.show_size[1])
        y_size_spin.connect('notify::value', self.y_size_spin_change)
        item4.add(y_size_spin)
        resolution_bar.insert(item4, -1)

        separator1 = Gtk.SeparatorToolItem()
        separator1.props.draw = True
        resolution_bar.insert(separator1, -1)

        item5 = Gtk.ToolItem()
        label5 = Gtk.Label()
        label5.set_text(' ' + _('Show grid'))
        item5.add(label5)
        resolution_bar.insert(item5, -1)

        grid = ToolButton('grid-icon')
        grid.connect('clicked', self.grid_click)
        resolution_bar.insert(grid, -1)

        resolution_bar.show_all()
        resolution_button = ToolbarButton(label=_('Resolution'),
                page=resolution_bar,
                icon_name='camera')
        toolbox.toolbar.insert(resolution_button, -1)
        resolution_button.show()

    def build_colors_toolbar(self, toolbox):

        barra_colors = Gtk.Toolbar()

        item1 = Gtk.ToolItem()
        label1 = Gtk.Label()
        label1.set_text(_('Color mode') + ' ')
        item1.add(label1)
        barra_colors.insert(item1, -1)

        item2 = Gtk.ToolItem()
        modes = ('RGB', 'YUV', 'HSV')
        combo = Combo(modes)
        item2.add(combo)
        combo.connect('changed', self.change_combo)
        barra_colors.insert(item2, -1)

        separator1 = Gtk.SeparatorToolItem()
        separator1.props.draw = True
        barra_colors.insert(separator1, -1)

        item_l = Gtk.ToolItem()
        label4 = Gtk.Label()
        label4.set_text(_('Brightness') + ' ')
        item_l.add(label4)
        barra_colors.insert(item_l, -1)
        
        item = Gtk.ToolItem()
        brightness_spin = Gtk.SpinButton()
        brightness_spin.set_range(-1, 255)
        brightness_spin.set_increments(1, 10)
        brightness_spin.props.value = int(self.brightness)
        brightness_spin.connect('notify::value', self.brightness_spin_change)
        item.add(brightness_spin)
        barra_colors.insert(item, -1)

        separator2 = Gtk.SeparatorToolItem()
        separator2.props.draw = True
        barra_colors.insert(separator2, -1)

        item3 = Gtk.ToolItem()
        label3 = Gtk.Label()
        label3.set_text(_('Threshold view'))
        item3.add(label3)
        barra_colors.insert(item3, -1)

        threshold_view = ToolButton('media-playback-stop')
        threshold_view.connect('clicked', self.threshold_view)
        threshold_view.set_tooltip(_('Yes'))
        barra_colors.insert(threshold_view, -1)

        separator3 = Gtk.SeparatorToolItem()
        separator3.props.draw = True
        barra_colors.insert(separator3, -1)

        item4 = Gtk.ToolItem()
        label4 = Gtk.Label()
        label4.set_text(_('Outline'))
        item4.add(label4)
        barra_colors.insert(item4, -1)

        outline_view = ToolButton('media-playback-stop')
        outline_view.connect('clicked', self.outline_view)
        outline_view.set_tooltip(_('Yes'))
        barra_colors.insert(outline_view, -1)

        separator4 = Gtk.SeparatorToolItem()
        separator4.props.draw = True
        barra_colors.insert(separator4, -1)

        item5 = Gtk.ToolItem()
        label5 = Gtk.Label()
        label5.set_text(_('Rects'))
        item5.add(label5)
        barra_colors.insert(item5, -1)

        rects_view = ToolButton('media-playback-stop')
        rects_view.connect('clicked', self.rects_view)
        rects_view.set_tooltip(_('Yes'))
        barra_colors.insert(rects_view, -1)

        barra_colors.show_all()
        colors_button = ToolbarButton(label=_('Colors'),
                page=barra_colors,
                icon_name='toolbar-colors')
        toolbox.toolbar.insert(colors_button, -1)
        colors_button.show()

    def change_combo(self, combo):
        self.mode = combo.get_active_text()
        if self.mode == 'RGB':
            self.label_color_red.set_text(' ' + _('Calibrated color:') + ' ' + _('Red') + ' ')
            self.label_color_green.set_text(' ' + _('Green') + ' ')
            self.label_color_blue.set_text(' ' + _('Blue') + ' ')

            self.label_threshold_red.set_text(' ' + _('Threshold:') + ' ' + _('Red') + ' ')
            self.label_threshold_green.set_text(' ' + _('Green') + ' ')
            self.label_threshold_blue.set_text(' ' + _('Blue') + ' ')

        elif self.mode == 'YUV':
            self.label_color_red.set_text(' ' + _('Calibrated color:') + ' ' + _('Luma') + ' ')
            self.label_color_green.set_text(' ' + _('U') + ' ')
            self.label_color_blue.set_text(' ' + _('V') + ' ')

            self.label_threshold_red.set_text(' ' + _('Threshold:') + ' ' + _('Luma') + ' ')
            self.label_threshold_green.set_text(' ' + _('U') + ' ')
            self.label_threshold_blue.set_text(' ' + _('V') + ' ')

        elif self.mode == 'HSV':
            self.label_color_red.set_text(' ' + _('Calibrated color:') + ' ' + _('Hue') + ' ')
            self.label_color_green.set_text(' ' + _('Saturation') + ' ')
            self.label_color_blue.set_text(' ' + _('Value') + ' ')

            self.label_threshold_red.set_text(' ' + _('Threshold:') + ' ' + _('Hue') + ' ')
            self.label_threshold_green.set_text(' ' + _('Saturation') + ' ')
            self.label_threshold_blue.set_text(' ' + _('Value') + ' ')

        self.followme_activity.put_color_mode(self.mode)

    def threshold_view(self, button):
        self.use_threshold_view = not self.use_threshold_view
        self.followme_activity.put_threshold_view(self.use_threshold_view)
        if not self.use_threshold_view:
            button.set_icon_name('media-playback-start')
            button.set_tooltip(_('Yes'))
        else:
            button.set_icon_name('media-playback-stop')
            button.set_tooltip(_('No'))

    def outline_view(self, button):
        self.use_outline_view = not self.use_outline_view
        self.followme_activity.put_outline_view(self.use_outline_view)
        if not self.use_outline_view:
            button.set_icon_name('media-playback-start')
            button.set_tooltip(_('Yes'))
        else:
            button.set_icon_name('media-playback-stop')
            button.set_tooltip(_('No'))

    def rects_view(self, button):
        self.use_rects_view = not self.use_rects_view
        self.followme_activity.put_rects_view(self.use_rects_view)
        if not self.use_rects_view:
            button.set_icon_name('media-playback-start')
            button.set_tooltip(_('Yes'))
        else:
            button.set_icon_name('media-playback-stop')
            button.set_tooltip(_('No'))

    def put_color(self, color):
        self.colorC = color
        self.red_spin.props.value = self.colorC[0]
        self.green_spin.props.value = self.colorC[1]
        self.blue_spin.props.value = self.colorC[2]

    def pixels_value(self, pixels, value):
        self.pixels = int(pixels.props.value)
        self.followme_activity.put_pixels(self.pixels)

    # BRIGHTNESS
    def brightness_spin_change(self, spin, value):
        b = int(spin.props.value)
        self.brightness = b
        self.followme_activity.put_brightness(self.brightness)

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
        b = int(blue.props.value)
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
        self.followme_activity.mode_calibrating(self.calibrating)
        if not self.calibrating:
            button.set_icon_name('media-playback-start')
            button.set_tooltip(_('Start'))
        else:
            button.set_icon_name('media-playback-stop')
            button.set_tooltip(_('Stop'))

    def grid_click(self, button):
        self.show_grid = not self.show_grid
        self.followme_activity.put_grid(self.show_grid)


class Combo(Gtk.ComboBox):

    def __init__(self, options):

        self.liststore = Gtk.ListStore(str)

        for o in options:
            self.liststore.append([o])

        GObject.GObject.__init__(self)

        cell = Gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, 'text', 0)

        self.set_active(0)

