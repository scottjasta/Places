import operator
import sys
import xml.dom.minidom
import cgi
import geoutil
import urllib2
from placeskeys import *
from datetime import datetime
from datetime import timedelta
from placesinclude import *
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

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
	ret = ret + '<span class="geo">' 
	ret = ret + '(<span class="latitude">' + str(aplace.latitude) + '</span>,'
	ret = ret + '<span class="longitude">' + str(aplace.longitude) + '</span>) '
	ret = ret + '</span>'
	return ret

def fstr(thing, default=''):
	if thing is None:
		return default
	return thing

def placeFormPageNew(aplace, user, formAction='', returnURL='/'):
	if aplace.name is None:
		keyparam = "0"
	else:
		keyparam = str(aplace.key())
	ret	= '<html><head><title>Place</title>\r'
	ret = ret + '<link href=\"/files/webgui.css\" rel=\"stylesheet\" type=\"text/css\" />\r'
	ret = ret + '<script type=\"text/javascript\" src=\"/files/jquery-1.4.1.js\"></script>\r'
	ret = ret + '<script type=\"text/javascript\" src=\"/files/jquery.jeditable.js\"></script>\r'
	ret = ret + '<script type="text/javascript">\r' 
	ret = ret + '$(document).ready(function() {\r'
	ret = ret + "$('.edit').editable('/web/updateone', {\r"
	ret = ret + "     indicator : 'Saving...',\r"
	ret = ret + '     submitdata: {key: \"' + keyparam + '\"},\r'
	ret = ret + "     tooltip   : 'Click to edit...'\r"
	ret = ret + " });\r"
	ret = ret + " $('.edit_area').editable('/web/updateone', { \r"
	ret = ret + "     type      : 'textarea',\r"
	ret = ret + "     cancel    : 'Cancel',\r"
	ret = ret + "     submit    : 'OK',\r"
	ret = ret + "     indicator : '<img src=\"img/indicator.gif\">',\r"
	ret = ret + "     tooltip   : 'Click to edit...'\r"
	ret = ret + "     });\r"
	ret = ret + " });\r"
	ret = ret + " </script>\r"
	ret = ret + "</head><body>"
	ret = ret + "<div class=\"edit\" id=\"name\">" + fstr(aplace.name) + "</div>"
	ret = ret + "<div class=\"edit\" id=\"address\">" + fstr(aplace.address) + "</div>"
	ret = ret + '		</body>'
	ret = ret + '</html>'
	
	return ret

def placeFormPage(aplace, user, formAction='', returnURL='/'):
	ret = '<html><head><title>Place</title>'
	ret += '<link href=\"/files/webgui.css\" rel=\"stylesheet\" type=\"text/css\" />\r'
	ret += '</head><body>\r'
	ret += '<form class=\"editform\" action="' + formAction + '" method="post" name="placeForm">'
	ret += '<input name="returnURL" value="' + returnURL + '" type=\"hidden\">'
	ret += '<fieldset>\r'
	ret += '<legend>Place Information</legend>'
	ret += '<ol class=\"editform\">\r'
	ret += '<li>'
	ret += '<label for="name">Name<em>*</em></label>'
	ret += '<input class=\"editform\" name="name" id="name" placeholder="Business or other name" value="' + fstr(aplace.name) + '"/>'
	ret += '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="address">Address<em></em></label>'
	ret = ret + '<input class=\"editform\" name="address" id="address" placeholder="Street address" value="' + fstr(aplace.address) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="address2"><em></em></label>'
	ret = ret + '<input class=\"editform\" name="address2" id="address2" placeholder="Additional street address" value="' + fstr(aplace.address2) + '">'
	ret += '</li>\r'
	ret += '<li class=\"editformsameline\">'
	ret += '<label for="city" style=\"display: none;\">City<em></em></label>'
	ret += '<input class=\"editformcity\" name="city" id="city" placeholder="City" value="'+ fstr(aplace.city) + '">'
	ret += '</li>\r'

	ret += '<li class=\"editformsameline\">'
	ret += '<label for="state" style=\"display: none\">State<em></em></label>'
	ret += '<input class=\"editformstate\" name="state" id="state" placeholder="State" value="' + fstr(aplace.state) + '">'
	ret += '</li>\r'

	ret += '<li>'
	ret += '<label for="zip" style=\"display: none;\">Zip<em></em></label>'
	ret += '<input class=\"editformzip\" name="zip" id="zip" placeholder="Zip code" value="' + fstr(aplace.zip) + '">'
	ret += '</li>\r'
	ret += '<li class="editformsameline">'
	ret += '<label for="latitude">Geocode<em></em></label>'
	ret += '<input class="editformlat" name="latitude" id="latitude" placeholder="Latitude (decimal)" value="' + fstr(aplace.latitude) + '">'
	ret += '</li>\r'
	ret += '<li>'
	ret += '<label for="longitude" style="display:none;">Longitude<em></em></label>'
	ret += '<input class="editformlong" name="longitude" id="longitude" placeholder="Longitude (decimal)" value="' + fstr(aplace.longitude) + '">'
	ret += '</li>\r'
	ret += '<li>'
	ret += '<label for="phone">Phone<em></em></label>'
	ret += '<input class=\"editform\" name="phone" id="phone" placeholder="Telephone number" value="' + fstr(aplace.phone) + '" >'
	ret += '</li>\r'
	ret += '<li>'
	ret += '<label for="email">Email<em></em></label>'
	ret += '<input class=\"editform\" name="email" id="email" placeholder="Email address for Place" value="' + fstr(aplace.email) + '">'
	ret += '</li>\r'
	ret += '<li>'
	ret += '<label for="url">URL<em></em></label>'
	ret += '<input class=\"editform\" name="url" id="url" placeholder="URL" value="' + fstr(aplace.URL) + '">'
	ret += '</li>\r'
	ret += '<li>'
	ret += '<label for="tag">Tag<em></em></label>'
	ret += '<input class=\"editform\" name="tag" id="tag" placeholder="Tags (separated by spaces)" value="' + ' '.join(aplace.tag) + '"'	
	if aplace.name is not None:
		ret += ' autofocus '
	ret += '>'
	ret += '</li>\r'
	ret += '<li>'
	ret += '<label for="notes">Notes<em></em></label>'
	ret += '<textarea class=\"editform\" name="notes" placeholder="Notes" id="notes">' + fstr(aplace.notes) + '</textarea>'
	ret += '</li>\r'
	ret += '<li>'
	ret += '<label for="owner">Owner<em></em></label>'
	ret += '<input class="editform" name="owner" id="owner" placeholder="Places Database Owner" value="' + fstr(aplace.owner, user.email()) + '">'
	ret += '</li>\r'
	ret += '<li>'
	ret += '<label for="rights">Rights<em></em></label>'
	ret += '<input class="editform" name="rights" id="rights" placeholder="Places Database Rights" value="' + str(aplace.rights) + '">'
	ret += '</li>\r'
	ret = ret + '</ol>\r'
	ret = ret + '</fieldset>\r'
	ret = ret + '<button type="submit">Save</button>\r'
#	if aplace.name is not None:
#	if aplace.key is not None:
	if aplace.is_saved():
		ret = ret + '<a href=\"/web/delete?key=' + str(aplace.key()) + '&returnURL=' + returnURL + '\">delete</a>'
		ret = ret + '<input name="key" type=\"hidden\" value="' 
		ret = ret + str(aplace.key()) 
		ret = ret + '">'
	ret = ret + '</form>\r'
	ret = ret + '</body>\r'
	ret = ret + '</html>'
	return ret


def placeFormPageWorking(aplace, user, formAction='', returnURL='/'):
	ret = '<html>'
	ret = ret + '<head>'
	ret = ret + '<title>Form Test</title>'
	ret = ret + '<link href=\"/files/webgui.css\" rel=\"stylesheet\" type=\"text/css\" />\r'
	ret = ret + '</head>'
	ret = ret + '<body>\r'
	ret = ret + '<form class=\"editform\" action="' + formAction + '" method="post" name="placeForm">'
	ret = ret + '<input name="returnURL" value="' + returnURL + '" type=\"hidden\">'
	ret = ret + '<fieldset>\r'
	ret = ret + '<legend>Place Information</legend>'
	ret = ret + '<ol class=\"editform\">\r'
	ret = ret + '<li>'
	ret = ret + '<label for="name">Name<em>*</em></label>'
	ret = ret + '<input class=\"editform\" name="name" id="name" value="' + fstr(aplace.name) + '"/>'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="address">Address<em></em></label>'
	ret = ret + '<input class=\"editform\" name="address" id="address" value="' + fstr(aplace.address) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="address2"><em></em></label>'
	ret = ret + '<input class=\"editform\" name="address2" id="address2" value="' + fstr(aplace.address2) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li class=\"editformsameline\">'
	ret = ret + '<label for="city" style=\"display: none;\">City<em></em></label>'
	ret = ret + '<input class=\"editformcity\" name="city" id="city" value="'+ fstr(aplace.city) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li class=\"editformsameline\">'
	ret = ret + '<label for="state" style=\"display: none\">State<em></em></label>'
	ret = ret + '<input class=\"editformstate\" name="state" id="state" value="' + fstr(aplace.state) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="zip" style=\"display: none;\">Zip<em></em></label>'
	ret = ret + '<input class=\"editformzip\" name="zip" id="zip" value="' + fstr(aplace.zip) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="phone">Phone<em></em></label>'
	ret = ret + '<input class=\"editform\" name="phone" id="phone" value="' + fstr(aplace.phone) + '" >'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="email">Email<em></em></label>'
	ret = ret + '<input class=\"editform\" name="email" id="email" value="' + fstr(aplace.email) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="tag">Tag<em></em></label>'
	ret = ret + '<input class=\"editform\" name="tag" id="tag"  value="' + ' '.join(aplace.tag) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="notes">Notes<em></em></label>'
	ret = ret + '<textarea class=\"editform\" name="notes" id="notes">' + fstr(aplace.notes) + '</textarea>'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="url">URL<em></em></label>'
	ret = ret + '<input class=\"editform\" name="url" id="url" value="' + fstr(aplace.URL) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="owner">Owner<em></em></label>'
	ret = ret + '<input name="owner" id="owner" value="' + fstr(aplace.owner, user.email()) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="rights">Rights<em></em></label>'
	ret = ret + '<input name="rights" id="rights" value="' + str(aplace.rights) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="latitude">Latitude<em></em></label>'
	ret = ret + '<input name="latitude"  id="latitude" value="' + fstr(aplace.latitude) + '">'
	ret = ret + '</li>\r'
	ret = ret + '<li>'
	ret = ret + '<label for="longitude">Longitude<em></em></label>'
	ret = ret + '<input name="longitude" id="longitude" value="' + fstr(aplace.longitude) + '">'
	ret = ret + '</li>\r'
	ret = ret + '</ol>\r'
	ret = ret + '</fieldset>\r'
	ret = ret + '<button type="submit">Save</button>\r'
#	if aplace.name is not None:
#	if aplace.key is not None:
	if aplace.is_saved():
		ret = ret + '<a href=\"/web/delete?key=' + str(aplace.key()) + '&returnURL=' + returnURL + '\">delete</a>'
		ret = ret + '<input name="key" type=\"hidden\" value="' 
		ret = ret + str(aplace.key()) 
		ret = ret + '">'
	ret = ret + '</form>\r'
	ret = ret + '</body>\r'
	ret = ret + '</html>'
	return ret

def showMainPage():
	ret = '<html>'
	ret = ret + '<head>'
	ret = ret + '<title>Places</title>'
	ret = ret + '<link href=\"/files/webgui.css\" rel=\"stylesheet\" type=\"text/css\" />\r'
	ret = ret + '</head>'
	ret = ret + '<body>'
	ret = ret + '<h1>Places Database</h1>\r'
	ret = ret + '<h2>Recent Additions</h2>\r'
#	t = datetime(2010,1,1)
	n = datetime.today()
	t = n - timedelta(days=14)
	places = db.GqlQuery("SELECT * FROM Place WHERE created_at > :datespec ORDER by created_at DESC", datespec = t)
	q = getListHTML(places)
	ret = ret + q
	ret = ret + '<h2>Commands</h2>\r'
	ret = ret + '<ul>\r'
	ret = ret + '<li><a href=\"/files/test.html\" class="placelink">Map</a></li>\r'
	ret = ret + '<li><a href=\"/web/list\" class="placelink">List</a></li>\r'
	ret = ret + '<li><a href=\"/web/add\" class="placelink">Add</a></li>\r'
	ret = ret + '<li><a href=\"/search?tag=hotdog\" class="placelink">search</a></li>\r'
	ret = ret + '<li><a href=\"/search.xml?tag=hotdog\" class="placelink">search (xml)</a></li>\r'
	ret = ret + '</ul>\r'
	ret += '<h2><a href="/files/aboutmisc.html">Misc</a></h2>\r'
	return ret


def getListHTML(places, returnURL = '/'):
	ret = '<ul>\r'
	for place in places:
		ret = ret + getListEntryHTML(place , '/web/edit', returnURL) + '\r'
	ret = ret + '</ul>'
	return ret

def getYahooGeoCode(place):
	YGEO_QUERY_URL = 'http://local.yahooapis.com/MapsService/V1/geocode?appid=' + YGEO_API_KEY 

	location = fstr(place.address) + ' ' + fstr(place.city) + ' '
	location = location + fstr(place.state) + ' ' + fstr(place.zip)
	yahoourl = YGEO_QUERY_URL + '&location=' + '%20'.join(location.split(' '))
	yahooxml = urllib2.urlopen(yahoourl).read()
	dom = xml.dom.minidom.parseString(yahooxml)
	place.latitude = dom.getElementsByTagName("Latitude")[0].firstChild.wholeText
	place.longitude = dom.getElementsByTagName("Longitude")[0].firstChild.wholeText
	place.put()

def updatePlaceColumn(key, elementid, value):
	F = 0

class geotag(webapp.RequestHandler):
	def get(self):
		places = db.GqlQuery("SELECT * FROM Place WHERE latitude = ''")
		for place in places:
			if fstr(place.address) <> '':
				self.response.out.write(place.name)
				getYahooGeoCode(place)
				self.response.out.write(place.latitude)
				self.response.out.write('<hr>')

class updatePlaceOne(webapp.RequestHandler):
	def post(self):
		key_name = self.request.get('key')
		elementid = cgi.escape(self.request.get('id'))
		value = cgi.escape(self.request.get('value'))
		updatePlaceColumn(key, elementid, value)

class updatePlace(webapp.RequestHandler):
	def post(self):
		key_name = self.request.get('key')
		returnURL = self.request.get('returnURL', '/')
		if key_name == '':
			place = Place()
		else:
			place = db.get(db.Key(key_name))
		place.name = cgi.escape(self.request.get('name'))
		place.address = cgi.escape(self.request.get('address'))
		place.address2 = cgi.escape(self.request.get('address2'))
		place.city = cgi.escape(self.request.get('city'))
		place.state = cgi.escape(self.request.get('state'))
		place.zip = cgi.escape(self.request.get('zip'))
		place.phone = cgi.escape(self.request.get('phone'))
		place.email = cgi.escape(self.request.get('email'))
		place.latitude = cgi.escape(self.request.get('latitude'))
		place.longitude = cgi.escape(self.request.get('longitude'))
		place.notes = cgi.escape(self.request.get('notes'))
		place.URL = cgi.escape(self.request.get('url'))
		place.tag = cgi.escape(self.request.get('tag')).split()
		place.put()
		self.redirect(returnURL)

def getListEntryHTML(place, targetURL = '/web/edit', returnURL = '/'):
	ret = '<li>'
	ret = ret + '<a href="' + targetURL + '?key=' + str(place.key()) + '&returnURL=' + returnURL + '" class="placelink">'
	ret = ret + str(place.name) + ' - ' + str(place.address) 
	ret = ret + ' ' + str(place.city) + ' ' + str(place.state) 
	ret = ret + '</a>'
	ret = ret + '</li>'
	return ret

class addform(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			place = Place()
			place.name = self.request.get('fn')
			place.latitude, place.longitude = self.request.get('geo').split(',')
			place.address = self.request.get('adr-street-address')	
			place.city = self.request.get('adr-locality')
			place.state = self.request.get('adr-region')
			place.zip = self.request.get('adr-postalcode') 
			place.phone = self.request.get('tel') 
			place.URL = self.request.get('url') 
			html = placeFormPage(place, user, '/web/update', self.request.get('returnURL', '/web/list'))
			self.response.out.write(html)
		else:
			self.redirect(users.create_login_url(self.request.uri))

class showList(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		places = db.GqlQuery("SELECT * FROM Place ORDER BY name")
		addURL = self.request.application_url + '/web/add'
		html = '<html><head>'
		html += '<title>Places List</title>'
		html += '<link href=\"/files/webgui.css\" rel=\"stylesheet\" type=\"text/css\" />\r'
		html += '</head><body>'
		html += '<a href="' + addURL + '">add</a>'
		html += getListHTML(places,  self.request.application_url + '/web/list')
		html += '<a href="' + addURL + '">add</a>'
		html += '<hr />'
		self.response.out.write(html)

#		key_name = self.request.get('key')
#		place = db.get(db.Key(key_name))


def editaddPlace(webapp, mode):
	user = users.get_current_user()
	if user:
		webapp.response.headers['Content-Type'] = 'text/html'
		if mode == 1:
			place = Place()
		else:
			key_name = webapp.request.get('key')
			place = db.get(db.Key(key_name))
		html = placeFormPage(place, user, '/web/update', webapp.request.get('returnURL', '/web/list'))
		webapp.response.out.write(html)
	else:
		webapp.redirect(users.create_login_url(webapp.request.uri))

class xeditPlace(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		key_name = self.request.get('key')
		place = db.get(db.Key(key_name))
		html = placeFormPage(place, '/web/update', self.request.get('returnURL', '/'))
		self.response.out.write(html)

class showMain(webapp.RequestHandler):
	def get(self):
		html = showMainPage()
		self.response.out.write(html)


class showTest(webapp.RequestHandler):
	def get(self):
		a = 1

class addPlace(webapp.RequestHandler):
	def get(self):
		editaddPlace(self, 1)

class editPlace(webapp.RequestHandler):
	def get(self):
		editaddPlace(self, 0)

class deletePlace(webapp.RequestHandler):
	def get(self):
		key_name = self.request.get('key')
		place = db.get(db.Key(key_name))
		place.delete()
		self.redirect(self.request.get('returnURL', '/'))
		
application = webapp.WSGIApplication([
		('/', showMain),
		('/web/test', showTest),
		('/web/list', showList),
		('/web/update', updatePlace),
		('/web/updateone', updatePlaceOne),
		('/web/add', addPlace),
		('/web/geo', geotag),
		('/web/delete', deletePlace),
		('/api/addform', addform),
		('/api/addform.html', addform),
		('/web/edit', editPlace)
		], 
		debug=True)


def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()


