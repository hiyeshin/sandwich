# -*- coding: utf-8 -*-

import os, datetime
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort

#Let's import mongoengine
from mongoengine import *
from flask.ext.mongoengine import mongoengine

#let's import data structure
import models

app = Flask(__name__) #we're creating our new flask app
app.config["CSRF_ENABLED"] = False

#Let's connect to MongoLab's database
mongoengine.connect("mydata", host=os.environ.get("MONGOLAB_URI"))
app.logger.debug("Connecting to MongoLabs")

#categories = ["bread", "veggies", "cheese", "spread"]
#sandwich subcategories borrowed from subway.com
bread = ["white bread", "wheat", "whole grain", "flatbread"]
flavors = ["ham","chicken", "turkey", "egg","roast beef","falafel", "tofu" ]
cheese = ["cheddar","american","brie","goat"]
veggies = ["lettuce", "onions", "tomato","kale"]
spread = ["pesto", "ketchup"]

# setup is done
#####################################################
# Routes

#this is our main page
@app.route("/", methods = ["GET", "POST"])
def index():
	# this is for debugging
	app.logger.debug(request.form.getlist("bread"))
	app.logger.debug(request.form.getlist("flavors"))
	app.logger.debug(request.form.getlist("cheese"))
	app.logger.debug(request.form.getlist("veggies"))
	app.logger.debug(request.form.getlist("spread"))
	
	#let's bring Sandwiches from models.py
	sandwich_form = models.SandwichForm(request.form)
	
	if request.method == "POST" and sandwich_form.validate():
		
		#get form data and create new sandwich
		# we're bring these from the models.py file
		sandwich = models.Sandwich()
		sandwich.creator = request.form.get("creator", "anonymous")
		sandwich.title = request.form.get("title", "no title")
		sandwich.slug = slugify(sandwich.title + " " + sandwich.creator)
		sandwich.bread = request.form.getlist("bread")
		sandwich.flavors = request.form.getlist("flavors")
		sandwich.cheese = request.form.getlist("cheese")
		sandwich.veggies = request.form.getlist("veggies")
		sandwich.spread = request.form.getlist("spread") 
		
		sandwich.save()
		
		return redirect("/sandwiches/%s" % sandwich.slug)
		
	else:
		
		if request.form.getlist("bread"):
			for b in request.form.getlist("bread"):
				sandwich_form.bread.append_entry(b)
				
		elif request.form.getlist("flavors"):
			for f in request.form.getlist("flavors"):
				sandwich_form.flavors.append_entry(f)
				
		elif request.form.getlist("cheese"):
			for c in request.form.getlist("cheese"):
				sandwich_form.cheese.append_entry(c)
				
		elif request.form.getlist("veggies"):
			for v in request.form.getlist("veggies"):
				sandwich_form.veggies.append_entry(v)
				
		elif request.form.getlist("spread"):
			for s in request.form.getlist("spread"):
				sandwich_form.spread.append_entry(s)
				
		templateData = {
			"sandwiches": models.Sandwich.objects(),
			"bread": bread,
			"flavors": flavors,
			"cheese": cheese,
			"veggies": veggies,
			"spread": spread,
			"form": sandwich_form		
		}
		
		return render_template("main.html", **templateData)
		
@app.route("/sandwich/<sandwich_lover>")
def by_sandwich(sandwich_lover):
	try:
		sandwiches = models.Sandwich.objects(sandwiches = sandwich_lover)
	except: 
		abort(404)
		
	templateData = {
		"current_sandwich":{
		"slug": sandwich_lover,
		"name": sandwich_lover("_", " ")
		},
		"sandwiches": sandwiches,
		"bread": bread,
		"flavors": flavors,
		"cheese": cheese,
		"veggies": veggies,
		"spread": spread,
		"form": sandwich_form
		}
		
	return render_template("sandwich_listing.html", **templateData)
		
@app.route("/sandwiches/<sandwich_slug>")
def sandwich_display(sandwich_slug):
	#get the sandwich by sandwich_slug
	try:
		sandwich = models.Sandwich.objects.get(slug = sandwich_slug)
	except:
		abort(404)
		
	#prepare template data
	templateData = {
		"sandwich": sandwich	
	}
	
	#render and return the template
	return render_template("sandwich_entry.html", **templateData)
	

@app.route("/sandwiches/<sandwich_id>/comment", methods = ["POST"])
def sandwich_comment(sandwich_id):
	name = request.form.get("name")
	comment = request.form.get("comment")
	
	if name =="" or comment =="":
		# if there's no name or comment, return to page
		return redirect(request.referrer)
		
	# get the sandwich by id
	try:
		sandwich = models.Sandwich.objects.get(id = sandwich_id)
	except:
		#error, then return to where we were before
		return redirect(request.referrer)
		
	# Let's create comment
	comment = models.Comment()
	comment.name = request.form.get("name")
	comment.comment = request.form.get("comment")
	
	#append comment to sandwich
	sandwich.comments.append(comment)
	
	#save it
	sandwich.save()
	
	return redirect("/sandwiches/%s" % sandwich.slug)
	
@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html"), 404
	
#Below is 'slugifying' function from title input
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text,delim=u"-"):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))
	
####################################################
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get("PORT", 5000)) # this is for local port 5000
	app.run(host="0.0.0.0", port = port)
	
				
		
	