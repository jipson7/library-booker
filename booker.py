import mechanize
import re
import urllib2
import time
from bs4 import BeautifulSoup, SoupStrainer


def makeList(table):
    result = []
    allrows = table.findAll('tr')
    for row in allrows:
        result.append([])
        allcols = row.findAll('td')
        for col in allcols:
            thestrings = [unicode(s) for s in col.findAll(text=True)]
            thetext = ''.join(thestrings)
            result[-1].append(thetext)
    return result

def getDateString():
    
    month = time.strftime("%B")
    
    day = time.strftime("%d")
   
    dateString = month + " " + day

    return dateString

def innerHTML(element):
    return element.decode_contents(formatter="html")

def searchThirdFloor(time):
    for ii in thirdFloorRooms:
        domTitle = "Time: " + time + ". Room no.: " + ii
        matchingLinks = tableLinkSoup.find_all(attrs={"title" : domTitle})
        for testLink in matchingLinks:
            imgString = innerHTML(testLink)
            if "images/open.gif" in imgString:
                print imgString

dateString = getDateString()

try :
    web_page = urllib2.urlopen("https://rooms.library.dc-uoit.ca/uoit_studyrooms/calendar.aspx").read()
    soup = BeautifulSoup(web_page)
    dateTag = soup.find("a", {"title" : dateString})

except urllib2.HTTPError :

    print("HTTPERROR!")

except urllib2.URLError :

    print("URLERROR!")

dateUrl = dateTag.get('href')

firstParam = dateUrl[25:-9]

secondParam = dateUrl[-6:-2]

br = mechanize.Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open("https://rooms.library.dc-uoit.ca/uoit_studyrooms/calendar.aspx")

br.select_form(nr=0)
br.set_all_readonly(False)
br["__EVENTTARGET"] = firstParam
br["__EVENTARGUMENT"] = secondParam
response = br.submit()


tableHtml = response.read()

tableLinkSoup = BeautifulSoup(tableHtml, parse_only=SoupStrainer('a'))

userSelectedTime = "8:00 PM"

thirdFloorRooms = ['LIB303', 'LIB304', 'LIB305', 'LIB306', 'LIB307', 'LIB309', 'LIB310']

secondFloorRooms = ['LIB202A', 'LIB202B', 'LIB202C']

searchThirdFloor(userSelectedTime)
