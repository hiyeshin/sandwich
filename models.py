# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

class Log(Document):
	text = StringField()
	timestamp = DateTimeField(default=datetime.now())

class Comment(EmbeddedDocument):
	name = StringField()
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())

class Sandwich(Document):
	
	creator = StringField(max_length=120, required=True, verbose_name="First name", help_text="Please enter your first name")
	title = StringField(max_length=120, required=True)
	slug = StringField()
	sandwich = StringField(required=True, verbose_name="What is your sandwich?")

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

	
SandwichForm = model_form(Sandwich)