#BASEURL https://rooms.library.dc-uoit.ca/uoit_studyrooms/temp.aspx
#starttime=11:30%20AM
#room=LIB202B
#next=viewleaveorjoin.aspx #This one doesn't change.


import mechanize
import re
import urllib2
import time
import Cookie
import cookielib
from bs4 import BeautifulSoup, SoupStrainer

cookiejar =cookielib.LWPCookieJar()

BASEURL = "https://rooms.library.dc-uoit.ca/uoit_studyrooms/"

BROWSER_HEADERS = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

thirdFloorRooms = ['LIB303', 'LIB304', 'LIB305', 'LIB306', 'LIB307', 'LIB309', 'LIB310']

secondFloorRooms = ['LIB202A', 'LIB202B', 'LIB202C']

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

#The following function is broken... It needs to be fixed post testing
def getDateString():
    
    month = time.strftime("%B")
    
    day = time.strftime("%d")
   
    dateString = month + " " + "14"

    return dateString

def innerHTML(element):
    return element.decode_contents(formatter="html")

def incrementTime(time):
    if time[-2]=="0":
        time[-2] = "3"
        return time
    else:
        if time[-4] != "9":
            time[-4] = str(int(time[-4] + 1))
            return time
        else:
            time = time[1:]
            time = "10" + time
            return time


def searchThirdFloor(time):
    for ii in thirdFloorRooms:
        domTitle = "Time: " + time + ". Room no.: " + ii
        matchingLinks = tableLinkSoup.find_all(attrs={"title" : domTitle})
        for testLink in matchingLinks:
            imgString = innerHTML(testLink)
            if "images/open.gif" in imgString:
                return testLink['href']

dateString = getDateString()

try :
    web_page = urllib2.urlopen(BASEURL + "calendar.aspx").read()
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

br.set_cookiejar(cookiejar)
cookie = cookielib.Cookie(version=0, name='PON', value="xxx.xxx.xxx.111", expires=365, port=None, port_specified=False, domain='xxxx', domain_specified=True, domain_initial_dot=False, path='/', path_specified=True, secure=True, discard=False, comment=None, comment_url=None, rest={'HttpOnly': False}, rfc2109=False)
cookiejar.set_cookie(cookie)

br.addheaders = BROWSER_HEADERS

response = br.open(BASEURL + "calendar.aspx")

br.select_form(nr=0)

br.set_all_readonly(False)

br["__EVENTTARGET"] = firstParam

br["__EVENTARGUMENT"] = secondParam

response = br.submit()

tableHtml = response.read()

tableLinkSoup = BeautifulSoup(tableHtml, parse_only=SoupStrainer('a'))

userSelectedTime = "8:00 PM"


backOfBookingLink= (searchThirdFloor(userSelectedTime)).replace(" ", "%20")

linkToBook = BASEURL + backOfBookingLink

print linkToBook

br.open(linkToBook)

print br.geturl()


#maybe create a fake GET form to fake sending the data????
