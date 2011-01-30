from google.appengine.ext import db


class UserInfo(db.Model):
	user = db.UserProperty()
	email = db.StringProperty()

class Place(db.Model):
	recordid = db.StringProperty()
	name = db.StringProperty()
	address = db.StringProperty()
	address2  = db.StringProperty()
	city  = db.StringProperty()
	state = db.StringProperty()
	zip = db.StringProperty()
	phone = db.StringProperty()
	email = db.StringProperty()
	latitude = db.StringProperty()
	longitude = db.StringProperty()
#	tag = db.StringProperty()
	tag = db.StringListProperty()
	notes = db.TextProperty()
	owner = db.StringProperty()
	rights = db.StringProperty()
	URL = db.StringProperty()
	created_at = db.DateTimeProperty(auto_now_add=True)
	updated_at = db.DateTimeProperty(auto_now=True)



