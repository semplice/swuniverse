#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# swuniverse - Semplice Software Universe
# Copyright (C) 2013  Semplice Project
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
# Authors:
#    Eugenio "g7" Paolantonio <me@medesimo.eu>
#

import apt

from gi.repository import Gtk
import quickstart, quickstart.scenes

@quickstart.builder.from_file("./swuniverse.glade")
class SoftwareStore:
	""" Main Interface """
	
	scenes_container = "scenes_container"
	scenes = {
		"loading":":0",
		"search":"swuniverse.scenes.search",
		"single":"swuniverse.scenes.single",
	}
	
	events = {
		"changed": (
			"search_box",
		),
		"clicked": (
			"featured_button",
		),
		"destroy": ("main",)
	}
	
	current_application = None
	
	cache = None
	
	@quickstart.threads.thread
	def open_apt_cache(self, callback=None):
		""" Opens the APT cache. """
		
		# We load things here to avoid slowing down when not needed...
		if not self.cache:
			self.cache = apt.cache.Cache()
		
		if callback: callback()
	
	def on_search_box_changed(self, widget):
		""" Fired when the search_box is changed. """
		
		if len(widget.get_text()) == 0:
			self.scene_manager.load("loading")
		else:
			self.scene_manager.load("search")
	
	def on_featured_button_clicked(self, button):
		""" Fired when the Featured button is clicked. """
		
		self.scene_manager.load("loading")
	
	def on_main_destroy(self, window):
		""" Called when destroying window. """
		
		Gtk.main_quit()
	
	def __init__(self):
		""" Initialize the interface """
		
		self.objects["main"].show_all()
		
		self.scene_manager = quickstart.scenes.initialize(self)
		
		self.scene_manager.load("loading")

quickstart.common.quickstart(SoftwareStore)
