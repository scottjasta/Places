import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader


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
#	created_at = db.DateTimeProperty(auto_now_add=True)
#	updated_at = db.DateTimeProperty(auto_now=True)



"""
class Place(db.Model):
	id = db.StringProperty()
	name = db.StringProperty()
	address = db.StringProperty
	address2  = db.StringProperty()
	city  = db.StringProperty()
	state = db.StringProperty()
	zip = db.StringProperty()
	phone = db.StringProperty()
	email = db.StringProperty()
	latitude = db.StringProperty()
	longitude = db.StringProperty()
	tag = db.StringProperty()
	notes = db.TextProperty()
	owner = db.StringProperty()
	rights = db.StringProperty()
	URL = db.StringProperty()
	created_at = db.DateTimeProperty(auto_now_add=True)
	updated_at = db.DateTimeProperty(auto_now=True)
"""


class PlaceLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Place',
                                   [('recordid', str),
                                    ('name', str),
									('address', str),
									('address2', str),
									('city', str),
									('state', str),
									('zip', str),
									('phone', str),
									('email', str),
									('latitude', str),
									('longitude', str),
									('tag', str.split),
									('notes', str),
									('owner', str),
									('rights', str),
									('URL', str)
#									('created_at', lambda x: datetime.datetime.strptime(x[:10], '%Y-%m-%d')),
#									('updated_at', lambda x: datetime.datetime.strptime(x[:10], '%Y-%m-%d'))
                                   ])

loaders = [PlaceLoader]

