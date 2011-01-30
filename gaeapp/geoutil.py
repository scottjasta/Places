import math
nauticalMilePerLat = 60.00721
nauticalMilePerLongitude = 60.10793
rad = math.pi / 180.0
milesPerNauticalMile = 1.15078

def calcDistance(lat1p, lon1p, lat2p, lon2p):                      
	"""
	Caclulate distance between two lat lons in NM
	print >>sys.stderr, lat1
	print >>sys.stderr, lon1
	print >>sys.stderr, lat2
	print >>sys.stderr, lon2
	"""
	lat1 = float(lat1p)
	lat2 = float(lat2p)
	lon1 = float(lon1p)
	lon2 = float(lon2p)
	yDistance = (lat2 - lat1) * nauticalMilePerLat
	xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * (nauticalMilePerLongitude / 2)
	distance = math.sqrt( yDistance**2 + xDistance**2 )
	return distance * milesPerNauticalMile

