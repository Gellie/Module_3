import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Thesis(ndb.Model):
	year = ndb.StringProperty(indexed=True)
	Title = ndb.StringProperty(indexed=True)
	abstract = ndb.StringProperty(indexed=True)
	adviser = ndb.StringProperty(indexed=True)
	section = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('create.html')
        self.response.write(template.render())

class APIThesis(webapp2.RequestHandler):
	def get(self):
		thesis = Thesis.query().order(-Thesis.date).fetch()
		thesis_list = []

		for entry in thesis:
			thesis_list.append({
				'id': entry.key.urlsafe(),
				'year': entry.year,
				'Title': entry.Title,
				'abstract': entry.abstract,
				'adviser': entry.adviser,
				'section': entry.section
			})

		response = {
        	'result': 'OK',
        	'data': thesis_list
        }

	        self.response.headers['Content-Type'] = 'application/json'
	        self.response.out.write(json.dumps(response))

	def post(self):
		thesis = Thesis()
		thesis.year = self.request.get('year')
		thesis.Title = self.request.get('Title')
		thesis.abstract = self.request.get('abstract')
		thesis.adviser = self.request.get('adviser')
		thesis.section = self.request.get('section')
		thesis.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
		    'result': 'OK',
		        'data': {
		            'id': thesis.key.urlsafe(),
		            'year': thesis.year,
		            'Title': thesis.Title,
		            'abstract': thesis.abstract,
		            'adviser': thesis.adviser,
		            'section': thesis.section
		        }
		}
		self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
    ('/home', MainPageHandler),
    ('/', MainPageHandler),
    ('/api/thesis', APIThesis)
], debug=True)
