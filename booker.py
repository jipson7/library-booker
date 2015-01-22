import time
import datetime
import sys
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 

STUDENT_INFORMATION = [["XXXXXXXXX", "XXXXXXXXX"],["testtest", "testtest"]]

TIME_SELECTION = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM",
        "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM",
        "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM",
        "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM",
        "9:30 PM", "10:00 PM", "10:30 PM", "11:00 PM"]

ROOM_SELECTION = ["LIB310", "LIB309", "LIB307", "LIB306", "LIB305", "LIB304", 
        "LIB303", "LIB202C", "LIB202B", "LIB202A"]

datePickingURL = "https://rooms.library.dc-uoit.ca/uoit_studyrooms/calendar.aspx"

userSelectedTime = ""

userSelectedDate = ""

scriptSelectedRoom = ""

def askUserQuestions():

    global userSelectedDate

    global userSelectedTime
    
    print "Are you booking for (1) Today or (2) Tomorrow"

    while (True):

        userDay = raw_input("(Select 1 or 2): ")

        if (userDay == "1"):

            userSelectedDate = getDateString(userDay)

            break

        elif (userDay == "2"):
            
            userSelectedDate = getDateString(userDay)

            break

    print "\nWhat time would you like to book for?"

    while(True):

        userSelectedTime = raw_input("(Ex. 10:00 AM or 8:00 PM): ")

        if userSelectedTime in TIME_SELECTION:

            break

        else:

            print "Invalid entry, try again (Ex. 5:00 PM)"
    

def getDateString(stringDay):

    intDay = int(stringDay)

    dateString = "";

    if (intDay == 1):
        
        month = time.strftime("%B")
        
        day = time.strftime("%d")


        dateString = month + " " + day

    elif (intDay == 2):

        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tm_stme = datetime.time(0, 0, 0)
        tm_stdate = datetime.datetime.combine(tomorrow, tm_stme)

        day = tm_stdate.strftime('%d')

        month = tm_stdate.strftime('%B')

        dateString = month + " " + day

    else:
        print "Error in getting Date String"
        return

    return dateString

def getOpenRoomTag():

   global scriptSelectedRoom

   for room in ROOM_SELECTION:
       
       if checkConsecutiveFreeTime(userSelectedTime, room):

           scriptSelectedRoom = room

           return buildTimeRoomTag(userSelectedTime, room)

   print "No available rooms at the specified time"

   driver.close()

   sys.exit()

def checkConsecutiveFreeTime(userTime, room):

    timeLocation = TIME_SELECTION.index(userTime)
        
    for ii in range(4):

        if not checkIfTimeSlotIsFree(TIME_SELECTION[ii], room):

            return False

    return True

def checkIfTimeSlotIsFree(userTime, room):
  

   try:
       driver.find_element_by_css_selector(
               "img[title='" + buildTimeRoomTag(userTime, room) + "']")
   
   except NoSuchElementException:

       return False

   return True

def buildTimeRoomTag(userTime, room):
    
    return ("Time: " + userSelectedTime + ". Room no.: " + room)

def clickLinkByTitle(title):
    driver.find_element_by_css_selector("a[title='" + title  + "']").click() 

def fillInFormInitial(studentNo, password):
   studentElement =  driver.find_element_by_css_selector(
           "input[name='ctl00$ContentPlaceHolder1$TextBoxStudentID']")

   passwordElement = driver.find_element_by_css_selector(
           "input[name='ctl00$ContentPlaceHolder1$TextBoxPassword']")

   groupNameElement = driver.find_element_by_css_selector(
           "input[name='ctl00$ContentPlaceHolder1$TextBoxName']")

   durationElement = driver.find_element_by_css_selector(
           "#ContentPlaceHolder1_RadioButtonListDuration_3")

   institutionElement = driver.find_element_by_css_selector(
           "#ContentPlaceHolder1_RadioButtonListInstitutions_1")

   groupCodeElement = driver.find_element_by_css_selector(
           "#ContentPlaceHolder1_TextBoxGroupCode")

   submitButton = driver.find_element_by_css_selector(
           "#ContentPlaceHolder1_ButtonReserve")

   studentElement.send_keys(studentNo)

   passwordElement.send_keys(password)

   groupNameElement.send_keys("CSCI")

   durationElement.click()

   institutionElement.click()

   groupCodeElement.send_keys("3334")

   submitButton.click()

    

   if not checkIfPageLoadByID("ContentPlaceHolder1_LabelMessage"):

      driver.close()
      sys.exit()

def checkIfPageLoadByID(elementID):

    try:


        element = WebDriverWait(driver, 10).until(

            EC.presence_of_element_located((By.ID, elementID))
        )
    except:
        print "Error loading page"
        return False
    
    return True


def getToTimetable():


   driver.get(datePickingURL)

   if not checkIfPageLoadByID("ContentPlaceHolder1_LabelInitialMessage"):
     
      driver.close()
      sys.exit()
   
   clickLinkByTitle(userSelectedDate)


def addAdditionalUsers(studentNo, studentPass):

    getToTimetable()

    clickLinkByTitle(secondTimeLink)

    if not checkIfPageLoadByID("ContentPlaceHolder1_RadioButtonListJoinOrCreateGroup_1"):

        driver.close()
        sys.exit()

    joinButton = driver.find_element_by_css_selector(
            "#ContentPlaceHolder1_ButtonJoinOrCreate")

    radioNext = driver.find_element_by_css_selector(
            "#ContentPlaceHolder1_RadioButtonListJoinOrCreateGroup_1")

    radioNext.click()

    joinButton.click()

    if not checkIfPageLoadByID("ContentPlaceHolder1_ButtonJoin"):

        driver.close()
        sys.exit()
   
    studentNoElement = driver.find_element_by_css_selector(
            "#ContentPlaceHolder1_TextBoxID")

    studentPassElement = driver.find_element_by_css_selector(
            "#ContentPlaceHolder1_TextBoxPassword")

    joinSubmitButton = driver.find_element_by_css_selector(
            "#ContentPlaceHolder1_ButtonJoin")

    studentNoElement.send_keys(studentNo)

    studentPassElement.send_keys(studentPass)

    #joinSubmitButton.click()

    ######Add check to see if user was added succesfully, and print message to console

###########################################################################

askUserQuestions()


try:

    driver = webdriver.Chrome()

except:

    print "A connection error occured"

getToTimetable()

timeSelection = getOpenRoomTag()

clickLinkByTitle(timeSelection)

if not checkIfPageLoadByID("ContentPlaceHolder1_RadioButtonListDuration_3"):

    driver.close()
    sys.exit()

fillInFormInitial(STUDENT_INFORMATION[0][0], STUDENT_INFORMATION[0][1])

print ("\nInitial booking of " + scriptSelectedRoom + " at " + userSelectedTime + " on " + 
        userSelectedDate + " was successful")

###########################################################################
#The Following code is to add other people to group#######################

secondTimeLink = userSelectedTime + " / " + scriptSelectedRoom + ". Incomplete reservation. This slot is open for reservation"

addAdditionalUsers(STUDENT_INFORMATION[1][0], STUDENT_INFORMATION[1][1])
#driver.close()








