# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

# WTForm is the form validation tool.

class Log(Document):
	text = StringField()
	timestamp = DateTimeField(default=datetime.now())

class Comment(EmbeddedDocument):
	name = StringField()
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())

class Sandwich(Document):
	# All we need is just change VERBOSE NAME!

	creator = StringField(max_length=120, required=True, verbose_name="First Name", help_text="Please enter your first name")
	title = StringField(max_length=120, required=True, verbose_name = "Name your sandwich")
	slug = StringField()
	sandwich = StringField(verbose_name="What is your sandwich?")

	# Category is a list of Strings
	bread = ListField(StringField(max_length=30))
	veggies = ListField(StringField(max_length=30))
	flavors = ListField(StringField(max_length=30))
	cheese = ListField(StringField(max_length=30))
	spread = ListField(StringField(max_length=30))
	inventive = ListField(StringField(max_length=30))

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

# this is creating a validation form from the Sandwich models
# We are creating a new WTForm object called SandwichForm.
#this will be used to validate toe form.
SandwichForm = model_form(Sandwich)