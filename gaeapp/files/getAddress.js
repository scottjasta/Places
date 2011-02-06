function getAddress() {
	if (document.body.getAttribute('id') == 'yelp_main_body') {
		getYelpAddress();
	} else {
		getHTML5Org();
	}
}

function getHTML5Org() {
	var fn, address, locality, region, postalcode, tel, url, latitude, longitude, geocode;
	var divXML = document.getElementsByTagName('div');
	for (i=0;i< divXML.length;i++) {
		if (!(divXML[i].getAttribute('itemscope') == null)){
			if (divXML[i].getAttribute('itemtype') == 'http://data-vocabulary.org/Organization') {
				var orgXML = divXML[i].getElementsByTagName("*");
				for (j=0;j< orgXML.length;j++) {
//							alert(orgXML[j].nodeName);
					if (orgXML[j].nodeType == 1) {
						if (!(orgXML[j].getAttribute('itemprop') == null)){
							var itemprop = orgXML[j].getAttribute('itemprop');							
//							alert(itemprop);
							switch (itemprop) {
							case 'name':
								fn = getText(orgXML[j]);
								break;
							case 'street-address':
								address = getText(orgXML[j]).replace(/^\s+|\s+$/g,"");
								break;
							case 'tel':
								tel = getText(orgXML[j]);
								break;
							case 'url':
								url = getText(orgXML[j]);
								break;
							case 'locality':
								locality = getText(orgXML[j]);
								break;
							case 'region':
								region = getText(orgXML[j]);
								break;
							case 'postal-code':
								postalcode = getText(orgXML[j]);
								break;
							case 'geo':
								geocode = getGeoCode();
								break;
							};
						};
					};
				};
			};
		};
		updatePlaces(fn, address, locality, region, postalcode, geocode, tel, url);
	};
}

function getGeoCode() {
//hack to search entire DOM as firefox moves the META tags under HEAD (yes this took a while to figure out)
var geoXML = document.getElementsByTagName('*');
var lat, lon
for (j=0;j< geoXML.length;j++) {
	if (geoXML[j].nodeType == 1) {
		if (!(geoXML[j].getAttribute('itemprop') == null)){
			var itemprop = geoXML[j].getAttribute('itemprop');							
			if ( itemprop == 'latitude' ) {
				lat = geoXML[j].getAttribute('content');};
			if ( itemprop == 'longitude' ) {
				lon = geoXML[j].getAttribute('content');};
		}
	}
}
return (lat + ', ' + lon)
}
function updatePlaces(fn, adr_street_address, adr_locality, adr_region, adr_postalcode, geo, tel, url) {
        var URLlist = "fn="+encodeURI(fn)+"&adr-street-address="+encodeURI(adr_street_address);
        URLlist += "&adr-region="+encodeURI(adr_region)+"&adr-locality="+encodeURI(adr_locality);
        URLlist += "&adr-postalcode="+encodeURI(adr_postalcode)+"&geo="+encodeURI(geo);
        URLlist += "&url="+encodeURI(url)+"&tel="+encodeURI(tel);
        placesURL = 'http://scottjastaplaces.appspot.com/api/addform.html?' + URLlist;
        window.open(placesURL,'placesadd','width=500,height=500,scrollbars=yes,resizable=yes');
}


function getYelpAddress() {
	var addressXML = document.getElementsByTagName('address');
	var yelpmetadata = document.getElementsByTagName('meta');
	var addresslines, address, locality, region, postalcode;
	var biztelephone, bizurl;
	var business, latitude, longitude;
	for (i=0;i< yelpmetadata.length;i++) {
		prop = yelpmetadata[i].getAttribute('property');
		if (prop == 'og:title') {business = yelpmetadata[i].getAttribute('content')};
		if (prop == 'og:latitude') {latitude = yelpmetadata[i].getAttribute('content')};
		if (prop == 'og:longitude') {longitude = yelpmetadata[i].getAttribute('content')};
	};
	var yelpphonedata = document.getElementsByTagName('span');
	for (i=0;i< yelpphonedata.length;i++) {
		prop = yelpphonedata[i].getAttribute('class');
		if (prop == 'tel') {biztelephone = getText(yelpphonedata[i])};
	};
	var yelpurldata = document.getElementsByTagName('a');
	for (i=0;i< yelpurldata.length;i++) {
		prop = yelpurldata[i].getAttribute('class');
		if (prop == 'url') {bizurl = getText(yelpurldata[i])};
	};


	if (addressXML.length > 0){
		if (addressXML[0].getAttribute('class') == 'adr') {
			addresslines = addressXML[0].getElementsByTagName('span');
		for (i=0;i< addresslines.length;i++) {
				aclass = addresslines[i].getAttribute('class');
				if (aclass == 'street-address') {address = getText(addresslines[i])};
				if (aclass == 'locality') {locality = getText(addresslines[i])};
				if (aclass == 'region') {region = getText(addresslines[i])};
				if (aclass == 'postal-code') {postalcode = getText(addresslines[i])};
			};
		}; 
	};
	var geo = latitude + ', ' + longitude
	updatePlaces(business, address, locality, region, postalcode, geo, biztelephone, bizurl)
}
function getText(node) {
var textNodeContents = [];
for(var chld = node.firstChild; chld; chld = chld.nextSibling) {
	if (chld.nodeType == 3) { // text node
	textNodeContents.push(chld.nodeValue);}}

	var text = textNodeContents.join('');

	return text
}


