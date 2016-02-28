import requests
import urllib
import lxml
from lxml import html
import os
import re

searchQuery=raw_input('Enter the movie')
searchQueryList= searchQuery.split(" ")
i=0
#autosuggesting the approximate correct name of the movie if user misspelled the name
url="http://google.com/complete/search?client=chrome&q="
for query in searchQueryList:
	if i==0:
		url=url+query
		i=i+1
	else:
		url=url+"+"+query
suggestionFile = urllib.URLopener()
suggestionFile.retrieve(url, "s.txt")
suggestionFile=open('s.txt','r')
data=suggestionFile.read()
suggestedMovie=data.split(",[\"")[1].split("\"]")[0]
if '","'in suggestedMovie:
	suggestedMovie=suggestedMovie.split('","')[0]
searchQueryList= suggestedMovie.split(" ")

print "Suggested movie: "+suggestedMovie


#generating torrent search link
i=0
url="http://torrentz"
url=url+".eu/search?q="
for query in searchQueryList:
	if i==0:
		url=url+query
		i=i+1
	else:
		url=url+"+"+query

print url
torrentsResults=requests.get(url)
torrentsResultsHtmlTree= html.fromstring(torrentsResults.content)
movieLinks=torrentsResultsHtmlTree.xpath('//dt/a/@href')

#filtering movie links from all links(that may contain ad links) using regularExpression
r=re.compile(r'^/\w+')
filteredLinks=filter(r.match,movieLinks)

if not filteredLinks:
	print "sorry! :( I've tried hard, but failed to find the torrent. bye have a nice day"
	exit()
#checking each link for best torrent 


for link in filteredLinks:

	s1=True;        
	url='http://torrentz'+'.eu'+link 
	print url
	torrentsResults= requests.get(url)
	torrentTree=html.fromstring(torrentsResults.content)	
	#checking if the filelist has a file with extension mp4 or avi !!!! you know other video formats? just add a or case.
	fileList=torrentTree.xpath('//div[@class="files"]/ul/li/ul/li/text()')
	valid=0
	for tFile in fileList:
		if '.avi' in tFile or '.mp4' in tFile or '.mkv' in tFile:
			valid=1
	if valid==1:		
		#checkin number of good votes for torrent
		verifiedAsGood=torrentTree.xpath('//div[@class="votebox"]/a/text()') 
		if 'Verify as a good' in verifiedAsGood[0]:
			positive=int(verifiedAsGood[0].split("(")[1].split(")")[0]) 
			fake=0	
			#adding all the -ve votes like spam,password, virus
			fakesList=links=torrentTree.xpath('//div[@class="votebox"]/span/a/text()')
			for s in fakesList:
		     		check=s.split(" ")
		     		if len(check)==2 and check[1]!="":
			     		fake=fake+int(check[1]) #adding all the -ve votes like spam,password, virus
			total=positive+fake;
			print total
			#moves forward only if total number of votes==0 (or) the positive vote percent is > 90 
			if total==0 or (float(positive)/total)*100>=90: 
				#collecting all links 
				links=torrentTree.xpath('//dt/a/@href')
				for link2 in links:
					print link2
					#checking for kat site
					if 'https://kat' in link2:
						while True:
							print "in the loop"
							katLink=link2
							finalPage=requests.get(katLink,verify=False)
							finalTree=html.fromstring(finalPage.content)

							"""for using magnet link"""
							torrentLinkList=finalTree.xpath('//a[@class="kaGiantButton "]/@href')
							os.system(' xdg-open '+torrentLinkList[0])
							s=1
							break
							#for downlading torrent file uncomment next multiline comment
							"""torrentFile=finalTree.xpath('//a[@class="kaGiantButton siteButton iconButton"]/@href')
							if len(torrentFile)==1:
								downloadLink="https:"+torrentFile[0]
								inc=3221
								output="%s"%inc+"tor.torrent"
								os.system("wget --no-check-certificate --output-document "+output+" "+downloadLink)
								os.system(' xdg-open  '+output);
								inc=inc+1
								print s1"""
						
					if s==1:
						break
	if s==1:
		break
	


		














