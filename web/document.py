from mongoengine.django.auth import User
from mongoengine import fields, EmbeddedDocument, Document


class File(EmbeddedDocument):
	filename = fields.StringField(max_length=100)
	filepath = fields.StringField(max_length=150)
	filetype = fields.StringField(max_length=30)
	file = fields.FileField()
	
class Comment(EmbeddedDocument):
	body = fields.StringField()	
	
class Post(Document):
	post_id = fields.IntField(default='autoincrement')
	user = fields.ReferenceField(User)
	body = fields.StringField()
	comment = fields.ListField(fields.EmbeddedDocument(Comment))
	file = fields.EmbeddedDocument(File)

	def autoincrement(self):
		number = self.all().count() + 1
		return number
	
	
