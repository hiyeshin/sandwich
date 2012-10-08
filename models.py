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
	
	creator = StringField(max_length=120, required=True, verbose_name="Name", help_text="What's your name?")
	title = StringField(max_length=120,required=True)
	slug=StringField()
	#I would not have the 'idea' category
	
	#Category is a list of Strings
	bread = ListField(StringField(max_length=30))
	flavors = ListField(StringField(max_length = 30))
	cheese = ListField(StringField(max_length = 30))
	veggies = ListField(StringField(max_length = 30))
	spread = ListField(StringField(max_length = 30))
	
	#comments is a list of Document type defined above
	comments = ListField(EmbeddedDocumentField(Comment))
	
	timestamp = DateTimeField(default=datetime.now())
	
SandwichForm = model_form(Sandwich)