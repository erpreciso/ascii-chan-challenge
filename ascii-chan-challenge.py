#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 erpreciso <erpreciso@erpreciso-laptop>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
		autoescape = True)
	
class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def render_front(self, title = "", art = "", error = ""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
		self.render("front.html", title = title, art = art, error = error, arts = arts)

	def get(self):
		self.render_front()
	
	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")
		
		if title and art:
			a = Art(title = title, art = art)
			a.put()
			self.redirect("/")
		else:
			error = "we need both a title and some artwork!"
			self.render_front(error = error, title = title, art = art)
			
app = webapp2.WSGIApplication([('/', MainPage)], debug = True)
