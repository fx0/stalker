#!/usr/bin/python2
import requests,urllib,ftplib
import re
import sys,getopt
import os,zipfile
import pygmaps
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

import urllib, urllib2
import json
# -*- coding: utf-8 -*-
#PROGRAM MADE BY PAU MUNOZ; DECEMBER 2013 GREETZ: lapipaplena.net; MOAB;TEMPLIX;STAREDSI  grayfx0@gmail.com
print"#############################################################"
print"#                         	     xxxxxxx                #"
print"#                               x xxxxxxxxxxxxx x           #"
print"#                            x     xxxxxxxxxxx     x        #"
print"#                                   xxxxxxxxx               #"
print"#                         x          xxxxxxx          x     #"
print"#                                     xxxxx                 #"
print"#                        x             xxx             x    #"
print"#                                       x                   #"
print"#        LOL!           xxxxxxxxxxxxxxx   xxxxxxxxxxxxxxx   #"
print"#                        xxxxxxxxxxxxx     xxxxxxxxxxxxx    #"
print"#                         xxxxxxxxxxx       xxxxxxxxxxx     #"
print"#                          xxxxxxxxx         xxxxxxxxx      #"
print"#                            xxxxxx           xxxxxx        #"
print"#                              xxx             xxx          #"
print"#                                  x         x              #"
print"#                                       x                   #"
print"#    >>Stalker 1.0   by Pau Munoz[fx0] [lapipaplena.net]    #"
print"#############################################################"  

#INITIAL VARS
user=''
password=''
profile=''
ftpserver =''
ftpuser = ''
ftppass = ''
counter = 0
gpscounter = 0
padress =''
#ZIP COMPRESSING
def zipfolder(foldername, target_dir):            
    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])
#GET PHOTO TEXT
def gtext(query):
	
	phototextsrc = re.search('<span class="hasCaption">(.+?)</span>', query)
	if phototextsrc != None:
		phototext = query[(phototextsrc.start()+31):-(len(query)-phototextsrc.end()+1)]
		return phototext.encode('utf8')
	else: 
		return ''

#GET PHOTO LOCATION
def glocation(query):
	if ('<span class="fbPhotoTagListTag withTagItem tagItem">' in query):
		query = query.encode('utf8')
		#in <span class="fbPhotoTagListTag withTagItem tagItem">
		flocationsrc = re.search('<span class="fbPhotoTagListTag withTagItem tagItem">(.+?)/a>', query)#59 4
		if flocationsrc != None:
			flocationstring = query[(flocationsrc.start()+58):-(len(query)-flocationsrc.end()+3)]
			#flocationstring = flocationstring.encode('utf8')
			
			locationsrc = re.search('data-hovercard-instant="1">(.+?)<', flocationstring)
			locationstring = flocationstring[(locationsrc.start()+27):-(len(flocationstring)-locationsrc.end()+1)]
			return locationstring

	else:
		return ''

#GET FIRST URL
def firstimg(query):
	imgsrc = re.search('id="fbPhotoImage" src="(.+?)"', query)
	imgurl = query[(imgsrc.start()+23):-(len(query)-imgsrc.end()+1)]
	imgurl = imgurl.encode('utf8')
	return imgurl
#GET NEXT URL
def gnexturl(query):
	nextsrc = re.search('<a class="photoPageNextNav"(.+?)<', fphoto)
	if nextsrc != None:
		nexturl = fphoto[(nextsrc.start()+27):-(len(fphoto)-nextsrc.end()+1)]
		nexturls = nexturl[nexturl.find("href=\"")+6:nexturl.find("\">")]
		return nexturls
	else:
		return ' '
#GET ALBUM
def galbums(query):
	final = query[(m.start()+32):-(len(query)-m.end()+1)]
	link=final[final.find("=")+1:final.find("&")]
	link=profile+'/media_set?set='+link+'&type=3'
	return link
#GET ALBUM TITLE
def galbumtitle(query):
	titlesrc = re.search('class="fbPhotoAlbumTitle">(.+?)<', query)
	albumtitle = query[(titlesrc.start()+26):-(len(query)-titlesrc.end()+1)]
	return albumtitle
#GET TAGS
def gtags(query):
	#<span class="fbPhotoTagListTag tagItem"> i .</span
	withsrc = re.search('<span class="fbPhotoTagListTag tagItem">(.+?).</span>', query)
	if withsrc != None:
		withtext = query[(withsrc.start()+40):-(len(query)-withsrc.end()+8)]
		return withtext
	else:
		return ''
#TRANSLATE AN ADDRESS TO GPS COORDINATES
def getcoordinates( address ):
	urlParams = {
                'address': address,
                'sensor': 'false',
        }  
	url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode( urlParams )
	response = urllib2.urlopen( url )
	responseBody = response.read()
 
	body = StringIO.StringIO( responseBody )
	result = json.load( body )
	if 'status' not in result or result['status'] != 'OK':
		return None
	else:
		return  str((result['results'][0]['geometry']['location']['lat']))+','+ str((result['results'][0]['geometry']['location']['lng']))
#GET LATITUDE
def getlat(coordinates):
	lat = float((coordinates[:coordinates.find(",")]))
	return lat
#GET LONGITUDE
def getlong(coordinates):
	longi = float(((coordinates[coordinates.find(",")+1:])))
	return longi
#TRANSLATE FACEBOOK ADDRESS TO GOOGLE MAPS ADDRESS
def gmapsite(query):
	#<span class="pp-place-title"><span> <
	sitesrc = re.search('<span class="pp-headline-item pp-headline-address"> <span>(.+?)<', query)
	if sitesrc != None:
		sitetext = query[(sitesrc.start()+58):-(len(query)-sitesrc.end()+1)]
		return sitetext.encode('utf8')
	else: 
		return 'notfound'
#GET PHOTO DATE
def getphotodate(query):
	#<abbr title="
	datesrc = re.search('<abbr title="(.+?)"', query)
	if datesrc != None:
		datetext = query[(datesrc.start()+13):-(len(query)-datesrc.end()+1)]
		return datetext.encode('utf8')
	else: 
		return 'notfound'
#GET FB NAME
def getfbname(url):
	urlsrc = re.search('https://www.facebook.com/(.+?)', url)
	urltext = url[(urlsrc.start()+25):]
	return urltext
#THE PROGRAM STARTS HERE
try:
	myopts, args = getopt.getopt(sys.argv[1:],"u:p:l:i:U:P:")
except getopt.GetoptError as e:
	print (str(e))
	print("Usage: %s -u username -p password -l profileUrl" % sys.argv[0])
	sys.exit(2)
for o, a in myopts:
	if o == '-u':
		user=str(a)
	elif o == '-p':
		password=str(a)
	elif o == '-l':
		profile=str(a)
	elif o == '-i':
		ftpserver =str(a)
	elif o == '-U':
		ftpuser = str(a)
	elif o == '-P':
		ftppass = str(a)
	else:
		print("Usage: %s -u username -p password -l profileUrl" % sys.argv[0])
		sys.exit(2)
#LOGIN PAYLOAD
login = {
	'lsd':'AVor5-oE',
	'legacy_return':'1',
	'trynum':'1',
	'timezone':'300',
	'lgnrnd':'055114_HsTO',
	'lgnjs':'1385128284',
        'email':''+user+'',
        'pass':''+password+'',
        'default_persistent':'0',
}

#CHECK PARAMS AND CONNECT TO FACEBOOK
if user != '' and password != '' and profile != '':
	s = requests.Session()
	s.post('https://www.facebook.com/login.php?login_attempt=1', data=login)
	s.post('https://www.facebook.com/login.php?login_attempt=1', data=login)
	r = s.get(profile+'/photos_albums')
	albums = r.text
	if not os.path.isdir(getfbname(profile)):
		os.mkdir(getfbname(profile))
	of = getfbname(profile)+"/report.html"
	outfile = open(of, 'a') 
	outfile.write('<html><head><title>Super secret report for: '+getfbname(profile)+'</title><style type="text/css">body{color:white; background-color:black;} </style> <meta name="report"  content="text/html;" http-equiv="content-type" charset="utf-8"></head><body><center><font size="14">#Report for: '+getfbname(profile)+'#</font><hr>'+'\n')

else:
	print("Usage: %s -u username -p password -l profileUrl" % sys.argv[0])
	print "Example: ./stalker.py -u superagent@NSA.gov -p s3cr3t -l https://www.facebook.com/osamabinsalami -i FTP.NSA.GOV -U 007 -P ftppassword"
	sys.exit(2)

#START BROWSING FACEBOOK
if ('logout' in r.text):
	print 'Login Successful'
	for m in re.finditer('<a class="photoTextTitle" href="(.+?)"', albums):	
		album = (s.get(galbums(albums))).text
		counter = 0
		#GET ALBUM TITLE
		albumtitle=galbumtitle(album)
		albumtitle = albumtitle.encode('utf8')
		print "Downloading images from: >>"+albumtitle
		if not os.path.isdir(getfbname(profile)+'/'+albumtitle):
			os.mkdir(getfbname(profile)+'/'+albumtitle)
		outfile.write('<a href="'+albumtitle+'/report.html">'+albumtitle+'</a>'+'\n')
		albumreport = open(getfbname(profile)+'/'+albumtitle+'/report.html', 'a') 
		albumreport.write('<html><head><title>'+albumtitle+'</title><style type="text/css">body{color:white; background-color:black;} img {width:270px; heigth:270px;} table{border-color:white;}</style> <meta name="album"  content="text/html;" http-equiv="content-type" charset="utf-8"> </head><body><center><table border="1"><font size="15">'+albumtitle+'</font>'+'\n')
		#GO TO THE FIRST URL OF THE ALBUM
		starter = re.search('<a class="uiMediaThumb _6i9 uiMediaThumbMedium" href="(.+?)"', album)
		if starter != None:
			starterurl = album[(starter.start()+54):-(len(album)-starter.end()+1)]
			fphoto = s.get(starterurl).text
			actualurl = ""
			
			#GET FIRST IMAGE
			starterimgurl = firstimg(fphoto)
			#GET NEXT IMAGE
			actualurl = gnexturl(fphoto)
			actualimgurl = ""
			#DO
			imgfile = "./"+getfbname(profile)+'/'+albumtitle+"/"+str(counter) +".jpg"
			print "Saving: "+imgfile
			urllib.urlretrieve(firstimg(fphoto),imgfile)
			albumreport.write('<tr><td><a href="'+str(counter)+'.jpg"><img src="'+str(counter)+'.jpg"></a></td> <td>Location: <a href="https://maps.google.com/maps?q='+glocation(fphoto)+'">'+glocation(fphoto)+'</a></td><td>Text: '+gtext(fphoto)+'</td><td>Date: '+getphotodate(fphoto)+'</td><td>Tags: '+gtags(fphoto)+'</td></tr>')
			gmapsfoto = s.get('https://maps.google.com/maps?q='+glocation(fphoto)).text
			direction = gmapsite(gmapsfoto)
			if direction != 'notfound':
				latitud = getlat(getcoordinates(direction))
				longitud = getlong (getcoordinates(direction))
				gpscounter = gpscounter +1
				if gpscounter == 1:
					mymap = pygmaps.maps(latitud,longitud, 10)
				mymap.addradpoint(latitud,longitud, 130, "#FF0000")
				mymap.addpoint(latitud,longitud, "#0000FF",getphotodate(fphoto))
				if padress != '':
					path = [(getlat(getcoordinates(padress)),getlong(getcoordinates(padress))),(getlat(getcoordinates(direction)), getlong(getcoordinates(direction)))]
					mymap.addpath(path,"#00FF00")
				padress=direction			
			counter = counter +1
			firstimage = firstimg(fphoto)
			#WHILE
			while actualimgurl != starterimgurl:
				if actualurl != ' ':
					fphoto = s.get(actualurl).text
					imgurl = firstimg(fphoto)
				else:
					break
				#PHOTO LOCATION
				gmapsfoto = s.get('https://maps.google.com/maps?q='+glocation(fphoto)).text
				print 'https://maps.google.com/maps?q='+glocation(fphoto)
				direction = gmapsite(gmapsfoto)
				if direction != 'notfound':
					latitud = getlat(getcoordinates(direction))
					longitud = getlong (getcoordinates(direction))
					gpscounter = gpscounter +1
					if gpscounter == 1:
						mymap = pygmaps.maps(latitud,longitud, 10)
					mymap.addradpoint(latitud,longitud, 130, "#FF0000")
					mymap.addpoint(latitud,longitud, "#0000FF",getphotodate(fphoto))
					if padress != '':
						path = [(getlat(getcoordinates(padress)),getlong(getcoordinates(padress))),(getlat(getcoordinates(direction)), getlong(getcoordinates(direction)))]
						mymap.addpath(path,"#00FF00")
					padress=direction

				#DOWNLOAD IMAGE
				if imgurl != firstimage:
					imgfile = "./"+getfbname(profile)+'/'+albumtitle+"/"+str(counter) +".jpg"
					print "Saving: "+imgfile
					urllib.urlretrieve(imgurl,imgfile)
					#WRITE REPORT LINE
					albumreport.write('<tr><td><a href="'+str(counter)+'.jpg"><img src="'+str(counter)+'.jpg"></a></td> <td>Location: <a href="https://maps.google.com/maps?q='+glocation(fphoto)+'">'+glocation(fphoto)+'</a></td><td>Text: '+gtext(fphoto)+'</td><td>Date: '+getphotodate(fphoto)+'</td><td>Tags: '+gtags(fphoto)+'</td></tr>')
				
				counter = counter +1
				actualurl = gnexturl(fphoto)
				actualimgurl = imgurl
			albumreport.write('</table></center></body></html>'+'\n')
			albumreport.close()
else:
	print 'Login failed'
of = getfbname(profile)+"/report.html"
outfile = open(of, 'a') 
outfile.write('<br> <br><a href="'+profile+'/map">search map in facebook</a> <br><br><iframe width="700" height="500" src="mymap.html"></iframe> </center></body></html>'+'\n')
try:
	mymap.draw(getfbname(profile)+'/mymap.html')
except:
	print 'no map generated'
	mapfile = open(getfbname(profile)+'/mymap.html', 'a') 
	mapfile.write('<center><font color="red"><b>NO GPS DATA FOUND</b></font></center>')
	mapfile.close()
outfile.close()
#ZIP COMPRESS
zipfolder(getfbname(profile)+'_report', getfbname(profile))
#SEND VIA FTP
if ftpuser != '' and ftppass != '' and ftpserver != '':
	session = ftplib.FTP(ftpserver,ftpuser,ftppass)
	report = open(getfbname(profile)+'_report.zip','rb')     
	print 'Uploading the report to the ftp server'            
	session.storbinary('STOR '+getfbname(profile)+'_report.zip', report)   
	report.close()                                   
	session.quit()
else:
	print 'error uploading the report, check the args'
