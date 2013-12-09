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

from gi.repository import Gtk
import xapian
import quickstart

@quickstart.builder.from_file("./scenes/single.glade")
class Scene(quickstart.scenes.BaseScene):
	""" The Search scene. """
	
	def prepare_scene(self):
		
		self.scene_container = self.objects["single"]
		
		
		# Ensure we show up the container
		self.scene_container.show_all()
		
	def on_scene_called(self):
		
		# Alias the current application for our convenience
		self.app = self.parent.current_application
		
		# Set title
		self.objects["name"].set_text(self.app["name"])
		
		# Set short description
		self.objects["description_short"].set_text(self.app["description_short"])
		
		# Set description
		self.objects["description"].set_text(self.app["version"].description)
		

