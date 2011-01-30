import operator
import sys
import xml.dom.minidom
import cgi
import geoutil
import urllib2
import html5lib
import xml.etree
from datetime import datetime
from placesinclude import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from html5lib import treebuilders, treewalkers, serializer
from html5lib.filters import sanitizer

def addrecord():
	thisplace = Place()
	thisplace.recordid = '1'
	thisplace.name = 'Dana Thomas House'
	thisplace.address = '301 East Lawrence Avenue'
	thisplace.address2 = ''
	thisplace.city  = 'Springfield'
	thisplace.state = 'IL'
	thisplace.zip = '62703'
	thisplace.phone = '+1 217 782-6776'
	thisplace.email = '' 
	thisplace.latitude = '39.793850'
	thisplace.longitude = '-89.651999'
	thisplace.tag = ['architecture','flw','wright']
	thisplace.notes = '' 
	thisplace.owner = 'scottj@asta.chicago.il.us'
	thisplace.URL = ''
	thisplace.created_at = datetime.strptime("2008-07-05 05:26:36", "%Y-%m-%d %H:%M:%S")
	thisplace.put()

	thisplace2 = Place()
	thisplace2.recordid = '2'
	thisplace2.name = 'Frank Smith Bank'
	thisplace2.address = '122 West Main Street'
	thisplace2.address2 = ''
	thisplace2.city  = 'Dwight'
	thisplace2.state = 'IL'
	thisplace2.zip = ''
	thisplace2.phone = ''
	thisplace2.email = '' 
	thisplace2.latitude = '41.092510'
	thisplace2.longitude = '-88.428204'
	thisplace2.tag = ['hotdog','food','flw']
	thisplace2.notes = '1905' 
	thisplace2.owner = 'scottj@asta.chicago.il.us'
	thisplace2.URL = ''
	thisplace2.created_at = datetime.strptime("2008-07-05 05:26:36", "%Y-%m-%d %H:%M:%S")
	thisplace2.put()


def ddrecord():
	thisplace = Place()
	thisplace.name = 'Dana-Thomas House'
	address = ''
	address2 =''
	city  = ''
	state = ''
	zip =  ''
	phone = ''
	email = ''
	Latitude ='' 
	Longitude = ''
	tag = ''
	notes = ''
	owner = ''
	URL = ''
	created_at = '2008-07-05 05:26:36'

def hcardEncode(aplace):
	ret = '<span style="display:inline;" class="vcard">'
	ret = ret + '<span class="fn org">' + str(aplace.name) + '</span><br />'
	ret = ret + '<span class="adr">'
	ret = ret + '<span class="street-address">' + str(aplace.address) + '</span><br />'
	ret = ret + '<span class="locality">' + str(aplace.city) + '</span>, '
	ret = ret + '<span class="region">' + str(aplace.state) + '</span> '
	ret = ret + '<span class="postal-code">' + str(aplace.zip) + '</span> '
	ret = ret + '<span class="country-name">USA</span><br />'
	ret = ret + '</span>'
	ret = ret + '<span class="tel"><span class="value">' + xformat(aplace.phone) + '</span></span> '
	ret = ret + '<span class="email"><span class="value">' + xformat(aplace.email) + '</span></span> '
	ret = ret + '<span class="url">' + xformat(aplace.URL) + '</span>'
	ret = ret + '<span class="geo"><br />' 
	ret = ret + '(<span class="latitude">' + str(aplace.latitude) + '</span>,'
	ret = ret + '<span class="longitude">' + str(aplace.longitude) + '</span>) - '
	ret = ret + '<distance>' + cgi.escape(str(aplace.distance)) + '</distance> miles'
	ret = ret + '<br /><tags>' + ' '.join(aplace.tag) + '</tags>'
	ret = ret + '</span>'
	return ret

def xformat(value, tag=None, default=''):
	if value is None:
		val = default
	else:
		val = str(value)
	ret = ''
	if tag is not None:
		ret = ret + '<' + tag + '>'
	ret = ret + cgi.escape(val)
	if tag is not None:
		ret = ret + '</' + tag + '>'
	return ret


def xmlEncode(aplace):
	ret = '<place>'
	ret = ret + xformat(aplace.name, 'fn')
	ret = ret + '<adr>'
	ret = ret + xformat(aplace.address, 'street-address')
	ret = ret + xformat(aplace.city, 'locality')
	ret = ret + xformat(aplace.state, 'region')
	ret = ret + xformat(aplace.zip, 'postal-code')
	ret = ret + '<country-name>USA</country-name>'
	ret = ret + '</adr>'
	ret = ret + '<tel>'
	ret = ret + xformat(aplace.phone, 'value')
	ret = ret + '</tel>'
	ret = ret + '<email>'
	ret = ret + xformat(aplace.email, 'value')
	ret = ret + '</email>'
	ret = ret + xformat(aplace.URL, 'url')
	ret = ret + '<geo>' 
	ret = ret + xformat(aplace.latitude, 'latitude')
	ret = ret + xformat(aplace.longitude, 'longitude')
	ret = ret + '</geo>'
	ret = ret + xformat(aplace.distance, 'distance')
	ret = ret + '<tags>'
	for placetag in aplace.tag:
		ret = ret + xformat(placetag, 'tag')
	ret = ret + '</tags>'
	ret = ret + xformat(aplace.owner, 'owner')
	ret = ret + xformat(aplace.notes, 'notes')
	ret = ret + '</place>'
	return ret

def is_number(s):
	try:
		float(s)
		return True
	except (ValueError, TypeError):
		return False


def searchplaces(tag, latitude, longitude, radius=50, owner=None):
	if owner is not None:
		ownerclause = 'owner = :owner'
	else:
		ownerclause = ''
	if tag is not None:
		tagclause = 'tag = :search'
	else:
		tagclause = ''
	baseSelect = 'SELECT * FROM Place'
	print >>sys.stderr, baseSelect
	if owner is not None:
		if tag is not None:
			placeclause = baseSelect + ' WHERE ' + ownerclause + ' AND ' + tagclause
			places = db.GqlQuery(placeclause, search = tag, owner = owner)
		else:
			places = db.GqlQuery(baseSelect + ' WHERE ' + ownerclause, owner = owner)
	else:
		if tag is not None:
			places = db.GqlQuery(baseSelect + ' WHERE ' + tagclause, search = tag)
		else:
			places = db.GqlQuery(baseSelect )
	dist = []
	for place in places:
		if (place.latitude == '') or (place.longitude == ''):
			distance = 1000
		else:
			distance = float(geoutil.calcDistance(latitude, longitude, float(place.latitude), float(place.longitude)))
		if is_number(radius):
			radius = float(radius)
		else:
			radius = 50
		if (distance < radius):
			dist.append(place)
			dist[-1].distance = distance
	return dist
#	return 'test'

class addform(webapp.RequestHandler):
	def get(self):
		place = Places()
		place.name = self.request.get('name')
		place.latitude, place.longitude = self.request.get('location').split(',')
		place.address = self.request.get('address')
		place.city = self.request.get('locality')
		place.state = self.request.get('region')
		place.zip = self.request.get('postalcode') 
		self.response.headers['Content-Type'] = 'text/html'
		html
		self.response.out.write('location: ' + str(latitude) + ',' + str(longitude) +  '\r')
		self.response.out.write('<hr>')
		self.response.out.write(business)
		self.response.out.write('<hr>')
		self.response.out.write(address)
		self.response.out.write('<hr>')
		self.response.out.write(locality)
		self.response.out.write('<hr>')

class searchxml(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/xml'
		currlocationlat = 41.99765
		currlocationlong = -87.6745
		tag = self.request.get('tag', None)
		if self.request.get('LatLngBounds')=='':
			radius = self.request.get('radius', 3)
		else:
			lat_lo, lng_lo, lat_hi, lng_hi = self.request.get('LatLngBounds').split(',')
			distance = float(geoutil.calcDistance(float(lat_lo), float(lng_lo), float(lat_hi), float(lng_hi)))
			radius = distance / 2
#		self.response.out.write('radius: ' + radius + '\r')
		if self.request.get('location') == '':
			latitude = self.request.get('latitude', currlocationlat)
			longitude = self.request.get('longitude', currlocationlong)
		else:
			latitude, longitude = self.request.get('location').split(',')
#		self.response.out.write('location: ' + str(latitude) + ',' + str(longitude) +  '\r')
		dist = searchplaces(tag, latitude, longitude, radius, self.request.get('owner', None))
		self.response.out.write('<places>')
		self.response.out.write('<version>1.1.3</version>')
		self.response.out.write('<version-date>2010-08-17</version-date>')
		for place in sorted(dist, key=operator.attrgetter('distance')):
			ret = xmlEncode(place)
##			self.response.out.write(place.name) 
##			self.response.out.write(place.distance) 
##			self.response.out.write(place.recordid)
#			self.response.out.write('<hr>')
			self.response.out.write(ret)
		self.response.out.write('</places>')


class search(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		currlocationlat = 41.99765
		currlocationlong = -87.6745
		dist = searchplaces(self.request.get('tag', 'hotdog'), self.request.get('latitude', currlocationlat),self.request.get('longitude', currlocationlong), self.request.get('radius', None), self.request.get('owner', None))
		for place in sorted(dist, key=operator.attrgetter('distance')):
			ret = hcardEncode(place)
##			self.response.out.write(place.name) 
##			self.response.out.write(place.distance) 
##			self.response.out.write(place.recordid)
#			self.response.out.write('<hr>')
			self.response.out.write(ret)
			self.response.out.write('<hr>')
		self.response.out.write('<hr>')


		

class display(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		places = db.GqlQuery("SELECT * FROM Place WHERE recordid = :id", id = self.request.get('id', 2))
		#places = db.GqlQuery("SELECT * FROM Place")
		self.response.out.write('id = ')
		self.response.out.write(self.request.get('id', 3))
		self.response.out.write(places[0].name)

		for place in places:
			ret = hcardEncode(place)
			self.response.out.write(place.name)
			self.response.out.write(place.recordid)
			self.response.out.write('<hr>')
			self.response.out.write(ret)
		self.response.out.write('<hr>')

class save(webapp.RequestHandler):
	def get(self):
		weburl = self.request.get('url', None)
		selection = self.request.get('selection', None)
		self.response.out.write('testing')
		self.response.out.write('<hr>')
		if(weburl is not None):
			self.response.out.write(weburl)
			webhtml = urllib2.urlopen(weburl).read()
			p = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))
			doc = p.parse(webhtml)
			self.response.out.write(xml.etree.ElementTree.dump(doc))
#			walker = treewalkers.getTreeWalker("etree")
#			stream = walker(doc)
#			s = serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False)
#			output_generator = s.serialize(stream)
#			for item in output_generator:
#				print item
#			divs = doc.getElementsByTagName('div')
#			for div in divs:
#				if div.getAttribute('class') == 'vcard':
#					self.response.out.write('vcard')
		self.response.out.write('<hr>')
		if(selection is not None):
			self.response.out.write(selection)
			

class delete(webapp.RequestHandler):
	def get(self):
		q = db.GqlQuery("SELECT * FROM Place")
#		for result in q:
#			result.delete()

class listAll(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		places = db.GqlQuery("SELECT * FROM Place")
		for place in places:
			self.response.out.write(place.name)
			self.response.out.write(' ')
			self.response.out.write(place.address)
			self.response.out.write('(')
			self.response.out.write(place.latitude)
			self.response.out.write(',')
			self.response.out.write(place.longitude)
			self.response.out.write(')<br />')
		self.response.out.write('<hr>')

	


class showTest(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write('<hr>')
		addrecord()
		self.response.out.write('added')
		self.response.out.write('<hr>')

	

application = webapp.WSGIApplication([
		('/test', showTest),
		('/list', listAll),
		('/delete', delete),
		('/search', search),
		('/search.xml', searchxml),
		('/save', save),
		('/addform', addform),
		('/display', display)
		], 
		debug=True)


def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()

