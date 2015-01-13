import mechanize
import re
import urllib2
import time
from bs4 import BeautifulSoup

month = time.strftime("%B")
day = time.strftime("%d")

dateString = month + " " + day

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

print br

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open("https://rooms.library.dc-uoit.ca/uoit_studyrooms/calendar.aspx")

html = response.read()

br.select_form(nr=0)
br.set_all_readonly(False)
br["__EVENTTARGET"] = firstParam
br["__EVENTARGUMENT"] = secondParam
response = br.submit()

#mnext = re.search("""<a href="javascript:__doPostBack('(.*?)','(.*?)')" style="color:Black" title="January 13">13""", html)

tableHtml = response.read()

tableUrl = response.geturl()

print tableHtml
