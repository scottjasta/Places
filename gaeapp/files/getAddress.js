
function getHTML5Org() {
}

function updatePlaces(fn, adr-street-address, adr-locality, adr-region, adr-postalcode, geo, tel, url) {
        var URLlist = "fn="+encodeURI(fn)+"&adr-street-address="+encodeURI(adr-street-address);
        URLlist += "&adr-region="+encodeURI(adr-region)+"&adr-locality="+encodeURI(adr-locality);
        URLlist += "&adr-postalcode="+encodeURI(adr-postalcode)+"&geo="+encodeURI(geo);
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
	updatePlaces(business, address, locality, region, postalcode, geo, tel, url)
}
function getText(node) {
var textNodeContents = [];
for(var chld = node.firstChild; chld; chld = chld.nextSibling) {
	if (chld.nodeType == 3) { // text node
	textNodeContents.push(chld.nodeValue);}}

	var text = textNodeContents.join('');

	return text
}


