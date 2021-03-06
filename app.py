# -*- coding: utf-8 -*-

import os, datetime
import re 
# re is for importing regex (regular expression thingy)
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort
from mongoengine import *
from flask.ext.mongoengine import mongoengine

import models

# creating flask app
app = Flask(__name__)
app.config['CSRF_ENABLED'] = False # it works without saying this line
# If we want to debug, we can set it to "TRUE"
connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")

bread = ["plain", "whole grain", "wheat", "rosmary", "bagel"]
veggies = ["lettuce","spinach", "tomato", "potato"]
flavors = ["chicken", "turkey", "ham", "roast beef", "falafel", "tofu"]
cheese = ["cheddar", "mozzarella", "goat", "brie", "ricotta"]
spread = ["mayo", "hummus", "pesto", "peanut butter", "jelly", "cream cheese"]
inventive = ["chocolate","gummy", "oreo", "udon", "rice"]

# this is our main page
# if there's any incoming request under the form of POST, create a new sandwich
# Else, just display the main.html template
@app.route("/", methods=['GET','POST'])
def index(): # if there's any request on "/", this index would appear

	#app.logger.debug(request.form.getlist('bread'))
	# get Idea form from models.py
	sandwich_form = models.SandwichForm(request.form)
	# this will hold all the functions for form display and validations

	if request.method == "POST" and sandwich_form.validate():

		# get form data - create new idea
		# bring from the models.py file
		sandwich = models.Sandwich()
		sandwich.creator = request.form.get('creator','anonymous')
		sandwich.title = request.form.get('title','no title')
		sandwich.slug = slugify(sandwich.title + " " + sandwich.creator)
	#	sandwich.sandwich = request.form.get('sandwich','sandwich')
		sandwich.bread = request.form.getlist('bread')
		sandwich.veggies = request.form.getlist('veggies')
		sandwich.flavors = request.form.getlist('flavors')
		sandwich.cheese = request.form.getlist('cheese')
		sandwich.spread = request.form.getlist('spread')
		sandwich.inventive = request.form.getlist('inventive')

		sandwich.save() # if it is valid, it saves the idea and redirect to the new page

		return redirect('/sandwiches/%s' % sandwich.slug)

	else: # this means that our form is not valid
		# we'll check the categories checkboxes
		if request.form.getlist('bread'):
			for b in request.form.getlist('bread'):
				sandwich_form.bread.append_entry(b)

		elif request.form.getlist('veggies'):
			for v in request.form.getlist('veggies'):
				sandwich_form.veggies.append_entry(v)

		elif request.form.getlist('flavors'):
			for f in request.form.getlist('flavors'):
				sandwich_form.flavors.append_entry(f)

		elif request.form.getlist('cheese'):
			for c in request.form.getlist('cheese'):
				sandwich_form.cheese.append_entry(c)

		elif request.form.getlist('spread'):
			for s in request.form.getlist('spread'):
				sandwich_form.spread.append_entry(s)

		elif request.form.getlist('inventive'):
			for i in request.form.getlist('inventive'):
				sandwich_form.inventive.append_entry(i)		


		# Build the templateData and return it to the user
		templateData = {
			'sandwiches' : models.Sandwich.objects(),
			'bread' : bread,
			'veggies': veggies,
			'flavors': flavors,
			'cheese': cheese,
			'spread': spread,
			#'inventive': inventive,
			'form' : sandwich_form
		}

		return render_template("main.html", **templateData)

@app.route("/sammie/<sandwich_lover>")
def by_sammie(sandwich_lover):

	try:
		sandwiches = models.Sandwich.objects(bread=sandwich_lover)
	except:
		abort(404)

	templateData = {
		'current_sammie' : {
			'slug' : sandwich_lover,
			'name' : sandwich_lover.replace('_',' ')
		},
		'sandwiches' : sandwiches,
		'bread' : bread,
		'veggies' : veggies,
		'flavors' : flavors,
		'cheese' : cheese,
		'spread' : spread,
		'inventive' : inventive,
		}

	return render_template('sammie_listing.html', **templateData)



@app.route("/sandwiches/<sandwich_slug>")
def sandwich_display(sandwich_slug):

	# get idea by idea_slug
	try:
		sandwich = models.Sandwich.objects.get(slug=sandwich_slug)
	except:
		abort(404)

	# prepare template data
	templateData = {
		'sandwich' : sandwich
	}

	# render and return the template
	return render_template('sandwich_entry.html', **templateData)

@app.route("/sandwiches/<sandwich_id>/comment", methods=['POST'])
def sandwich_comment(sandwich_id):

	name = request.form.get('name')
	comment = request.form.get('comment')

	if name == '' or comment == '':
		# no name or comment, return to page
		return redirect(request.referrer)


	#get the idea by id
	try:
		sandwich = models.Sandwich.objects.get(id=sandwich_id)
	except:
		# error, return to where you came from
		return redirect(request.referrer)


	# create comment
	comment = models.Comment()
	comment.name = request.form.get('name')
	comment.comment = request.form.get('comment')

	# append comment to idea
	sandwich.comments.append(comment)

	# save it
	sandwich.save()

	return redirect('/sandwiches/%s' % sandwich.slug)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# slugify the title 
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True

	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)