# James Dickson 2016
# Just creates a javascript array from geoip-data for plotting in google maps.
import urllib2
import json
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='This is only for creating javascript object for google maps from ip-addresses.')
parser.add_argument('-input', action="store", default='iplist.txt')
parser.add_argument('-output', action="store", default='staticlocations2.js')
parser.add_argument('-geoipservice', action="store", default='http://freegeoip.net/json/')
parseResults = parser.parse_args()

# Parameters
strInputFile = parseResults.input  			# 'iplist.txt'
strGeoIPService = parseResults.geoipservice # 'http://freegeoip.net/json/'
strOutputFile = parseResults.output 		# 'staticlocations2.js'

# Open the javascript file that we want to store location info in.
f = open(strOutputFile, 'w')
f.write('/* James 2016 - visit https://www.wallparse.com for more free tools and happy coding... */ \n function getLocations() {')
f.write('var locations = [')

# Used for javascript creation
bFirst = True

# Read line by line from ip list file
with open(strInputFile, "r") as fin:
	for line in fin:
		
		# Download Geoip-info
		strIP = line.splitlines()[0]
		print strIP		
		
		try:
			response = urllib2.urlopen(strGeoIPService + line)
			html = response.read()
		except:
			print 'Could not get info regarding: ' + strIP
			continue

		# Parse json
		j = json.loads(html)
		print j['latitude']
		print j['longitude']
		print j['city']
		print j['region_name']
		print j['country_name']

		# Write javascript info
		if(bFirst):
			bFirst = False		
		else:
			f.write(',')
		
		# Format: [[country, region, city, latitude, longitude, ip ]]
		f.write( '[\'' + j['country_name'].encode('ascii', 'ignore') + ' - ' + j['region_name'].encode('ascii', 'ignore') + ' - ' + j['city'].encode('ascii', 'ignore') + '\', ' )
		f.write(str(j['latitude']) + ', ' + str(j['longitude']) + ',\'' +  strIP + '\']')
		

# Write end clauses and close file
f.write(']; ')
f.write('return locations; }')
f.close()

