#!/usr/bin/env python
import urllib
import sys
import time

def readipfromfile(filename):
	lines = []
	try:
		with open(filename) as f:
			lines = [line.rstrip(' \n') for line in f]
	except:
		print 'Error: ' + '"' + filename +'"' + ' File not found';
		lines = []
	return lines

def getestimatetime(len):	
	nbrsec = len / 2
	nbrhour = (nbrsec / 3600) % 24
	nbrmin = (nbrsec / 60) % 60
	nbrsec = nbrsec % 60
	return str(nbrhour) + 'h ' + str(nbrmin) + 'm ' + str(nbrsec)

class SolvedIp:
	ip = ""
	latitude = 0.0
	longitude = 0.0


def askipandparse(ip):
	solvedip = SolvedIp()
	solvedip.ip = ip
	htmldate = urllib.urlopen('http://ip-api.com/xml/' + ip).read()
	totallen = len(htmldate)
	isla = htmldate.find('<lat><![CDATA[')
	idla = htmldate.find(']]></lat>', isla + 14)
	islo = htmldate.find('<lon><![CDATA[')
	idlo = htmldate.find(']]></lon>', islo + 14)
	if isla == -1:
		solvedip.latitude = str(0);
		solvedip.longitude = str(0);
	else:
		solvedip.latitude = htmldate[isla + 14: - (totallen - idla)]
		solvedip.longitude = htmldate[islo + 14: - (totallen - idlo)]
	return solvedip

def resolvips(ips):
	i = 0
	totallen = len(ips)
	solved = [];
	for ip in ips:
		if i % 2 == 0 and i != 0:
			time.sleep(1)
			print 'Resolving... (' + str(i) + '/' + str(totallen) + ')'
		solved.append(askipandparse(ip));
		i = i + 1
	print 'Resolving... (' + str(i) + '/' + str(totallen) + ')'
	return solved

def writesolvedinfile(solved):
	totallen = len(solved)
	cursor = 0
	content = 'var locs = ['
	print 'Writing solved ip in file...'
	for i in solved:
		if cursor != 0:
			content = content + ', '
		cursor = cursor + 1
		content = content + '{ "ip" : "'+ i.ip +'", "lat" : ' + i.latitude + ' , "lng" : ' + i.longitude + ' }' 
	content = content + ']'
	outf = open('solved.js', 'w')
	outf.write(content)
	outf.close()
	print 'File saved'


print '{Python 2.7 script, ip to lat/long v1}\n--------------------------------------\n'
ips = readipfromfile('iplist.txt')
print 'Read ips fromfile: ' + ('OK' if len(ips) > 0 else 'KO')
if len(ips) == 0 :
	sys.exit(1)
print 'Infos: This script use the api from the website "http://ip-api.com"'
print 'free version allow only 150requests per min (without ban)'
print 'Estimate time to resolve the ' + str(len(ips)) + ' ip adresses: ' + getestimatetime(len(ips))
solved = resolvips(ips)
writesolvedinfile(solved)
print 'Everything is done, you can open visualiser.html'