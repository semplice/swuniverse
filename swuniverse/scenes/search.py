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

@quickstart.builder.from_file("./scenes/search.glade")
class Scene(quickstart.scenes.BaseScene):
	""" The Search scene. """
	
	events = {
		"cursor-changed": ("results",)
	}
	
	def build_current_application(self):
		""" Builds self.parent.current_application. """

		model, iter = self.objects["results"].get_selection().get_selected()
		# 0 = name shown, 1 = package name, 2 = package description
		package = self.parent.cache[model.get_value(iter, 1)]
		version = package.candidate
		self.parent.current_application = {
			"name": model.get_value(iter, 1),
			"package": package,
			"version": version,
			"description_short": model.get_value(iter, 2)
		}
				
		self.parent.scene_manager.load("single")

	def on_results_cursor_changed(self, treeview):
		""" Fired when results's cursor-changed signal has been emitted. """
		
		if not self.parent.cache:
			self.parent.scene_manager.load("loading")
			self.parent.open_apt_cache(callback=self.build_current_application)
		else:
			self.build_current_application()
		
	def prepare_scene(self):
		
		self.scene_container = self.objects["search"]
		
		
		# Ensure we show up the container
		self.scene_container.show_all()
		
		# Create store
		self.model = Gtk.ListStore(str, str, str)
		# And link the TreeView to it...
		self.objects["results"].set_model(self.model)
		
		# Create cellrenderers...
		self.cell_name = Gtk.CellRendererText()
		# Create columns...
		self.column_name = Gtk.TreeViewColumn("Name", self.cell_name, text=0)
		self.objects["results"].append_column(self.column_name)
		
		# Open apt-xapian database...
		self.database = xapian.Database("/var/lib/apt-xapian-index/index")
		
		# Create stemmer
		self.stemmer = xapian.Stem("english")
		
		# Alias the searchbox for our convenience
		self.search_box = self.parent.objects["search_box"]

		# Parse xapian values
		self.values = {}
		with open("/var/lib/apt-xapian-index/values") as f:
			for line in f.readlines():
				if not line.startswith("#") and not line.replace("\n","") == "":
					line = line.split("\t")
					self.values[line[0]] = int(line[1])
		
	def on_scene_called(self):
		
		terms = []
		for word in self.search_box.get_text().split(" "):
			if word.islower() and word.find("::") != -1:
				# tag
				terms.append("XT"+word)
			else:
				# normal
				word = word.lower()
				terms.append(word)
				stem = self.stemmer(word)
				if stem != word:
					terms.append("Z"+stem)

		query = xapian.Query(xapian.Query.OP_OR, terms)

		enquire = xapian.Enquire(self.database)
		enquire.set_query(query)

		# Display the top 20 results, sorted by how well they match
		matches = enquire.get_mset(0, 60)
		
		
		self.model.clear()
		for m in matches:
			self.model.append(
				(m.document.get_data() + " - " + m.document.get_value(self.values["display_name"]),
					m.document.get_data(),
					m.document.get_value(self.values["display_name"])
				)
			)

