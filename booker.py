import time
import datetime
import sys
import os
import io
from random import randint
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 

STUDENT_INFORMATION = []

ROOMTYPE = 0

NUMBER_OF_CREDENTIALS = 0

GROUP_CODE = "9435"

TIME_SELECTION = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM",
        "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM",
        "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM",
        "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM",
        "9:30 PM", "10:00 PM", "10:30 PM", "11:00 PM"]

ROOM_SELECTION = ["LIB310", "LIB309", "LIB307", "LIB306", "LIB305", "LIB304", 
        "LIB303", "LIB202C", "LIB202B", "LIB202A"]

datePickingURL = "https://rooms.library.dc-uoit.ca/uoit_studyrooms/calendar.aspx"

driver = 0

userSelectedDate = ""

userSelectedTime = ""

scriptSelectedRoom = ""

roomTagToClick = ""

conflictedRoom = False

def loadUserData():

    global STUDENT_INFORMATION

    global NUMBER_OF_CREDENTIALS

    userFile = open("studentInfo.txt", "r")

    for line in iter(userFile):

       NUMBER_OF_CREDENTIALS = NUMBER_OF_CREDENTIALS + 1

       STUDENT_INFORMATION.append(line.split()) 

    userFile.close()

def askUserQuestions():

    global userSelectedDate

    global userSelectedTime

    global ROOMTYPE
    
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

    while(True):

    	ROOMTYPE = raw_input(
    		"\nWhich type of room would you like to book, (2) Person or (3) Person ")

    	if ((ROOMTYPE == "2") | (ROOMTYPE == "3")):
    		break

    	else:

    		print "Invalid selection, try again"


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

def createWebDriver():

	global driver

	try:

         driver = webdriver.Chrome()

	except:

    	 print "A connection error occured"

    	 return


def getToTimetable():

    driver.get(datePickingURL)

    if not checkIfPageLoadByID("ContentPlaceHolder1_LabelInitialMessage"):
     
       	exitProgram() 
       
    clickLinkByTitle(userSelectedDate)

def checkIfPageLoadByID(elementID):

    try:

        element = WebDriverWait(driver, 10).until(

            EC.presence_of_element_located((By.ID, elementID))
        )
    except:

        return False
    
    return True

def clickLinkByTitle(title):
    driver.find_element_by_css_selector("a[title='" + title  + "']").click()

def clickRadioByID(idVal):
    driver.find_element_by_css_selector("input[title='" + idVal  + "']").click()

def findOpenRoom():

	global scriptSelectedRoom

	for room in ROOM_SELECTION:

		if ((ROOMTYPE == "2") & (room[3] == "3")):

			continue

		if checkConsecutiveFreeTime(userSelectedTime, room):

			scriptSelectedRoom = room

			return True

	print "No Rooms available at specified time"

	return False

def checkConsecutiveFreeTime(userTime, room):

	global roomTagToClick

	global conflictedRoom
	timeLocation = TIME_SELECTION.index(userTime)

	if not checkIfTimeSlotIsFree(TIME_SELECTION[timeLocation], room):

		return False



	try:
		driver.find_element_by_css_selector(
			"img[title='" + buildTimeRoomTag(userTime, room) + "']")

		roomTagToClick = "img[title='" + buildTimeRoomTag(userTime, room) + "']"
   
	except NoSuchElementException:
       
		roomTagToClick = "img[title='" + buildTimeRoomTagConflicted(userTime, room) +"']"

		conflictedRoom = True
        
	for ii in range(3):

		if not checkIfTimeSlotIsFree(TIME_SELECTION[timeLocation + ii + 1], room):

			return False

	return True

def checkIfTimeSlotIsFree(userTime, room):
  

   try:
       driver.find_element_by_css_selector(
               "img[title='" + buildTimeRoomTag(userTime, room) + "']")
   
   except NoSuchElementException:
       
       try:
           driver.find_element_by_css_selector(
                   "img[title='" + buildTimeRoomTagConflicted(userTime, room) +"']")

       except NoSuchElementException:

           return False

   return True

def buildTimeRoomTag(userTime, room):

    return ("Time: " + userTime + ". Room no.: " + room)

def buildTimeRoomTagConflicted(userTime, room):

    return (userTime + " / " + room + 
            ". Incomplete reservation. This slot is open for reservation")

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

   groupCodeElement.send_keys(GROUP_CODE)

   submitButton.click()

def addAdditionalUsers(studentNo, studentPass):

	getToTimetable()

	clickLinkByTitle(buildTimeRoomTagConflicted(userSelectedTime, scriptSelectedRoom))

	if not checkIfPageLoadByID(
		"ContentPlaceHolder1_RadioButtonListJoinOrCreateGroup_1"):

		exitProgram()

	joinButton = driver.find_element_by_css_selector(
		"#ContentPlaceHolder1_ButtonJoinOrCreate")

	radioNext = driver.find_element_by_css_selector(
		"input[value='" + str(GROUP_CODE) + "']")

	radioNext.click()

	joinButton.click()

	if not checkIfPageLoadByID("ContentPlaceHolder1_ButtonJoin"):

		exitProgram()

	studentNoElement = driver.find_element_by_css_selector(
		"#ContentPlaceHolder1_TextBoxID")

	studentPassElement = driver.find_element_by_css_selector(
		"#ContentPlaceHolder1_TextBoxPassword")

	joinSubmitButton = driver.find_element_by_css_selector(
		"input[name='ctl00$ContentPlaceHolder1$ButtonJoin']")

	studentNoElement.send_keys(studentNo)

	studentPassElement.send_keys(studentPass)

	joinSubmitButton.click()

def main():

	createWebDriver()

	getToTimetable()

	if (findOpenRoom()):

		 driver.find_element_by_css_selector(roomTagToClick).click()

	else:

		exitProgram()

	if (conflictedRoom):

		if(checkIfPageLoadByID("ContentPlaceHolder1_RadioButtonListJoinOrCreateGroup_0")):
  			
			clickRadioByID("ContentPlaceHolder1_RadioButtonListJoinOrCreateGroup_0")

			print "checking if conflicted loads"

		else:

  			exitProgram()


	if not checkIfPageLoadByID("ContentPlaceHolder1_RadioButtonListDuration_3"):

		exitProgram()


	fillInFormInitial(STUDENT_INFORMATION[0][0], STUDENT_INFORMATION[0][1])

	try:

		driver.find_element_by_css_selector("#ContentPlaceHolder1_LabelError");

		driver.close()

		print "Changing group code"

		changeGroupCode()

		print ("Code Changed to " + str(GROUP_CODE))

		main()

	except NoSuchElementException:

		print "Initial form filling successful for user " + STUDENT_INFORMATION[0][0]

	if (ROOMTYPE == "3"):

		for ii in range(2):

			jj = ii + 1

			addAdditionalUsers(STUDENT_INFORMATION[jj][0], STUDENT_INFORMATION[jj][1])

			print ("User " + STUDENT_INFORMATION[jj][0] + " was registered successfully.\n")

	else:

		addAdditionalUsers(STUDENT_INFORMATION[1][0], STUDENT_INFORMATION[1][1])

		print ("User " + STUDENT_INFORMATION[1][0] + " was registered successfully.\n")


	print ("Booking of " + scriptSelectedRoom + " at " + 
		userSelectedTime + " on " + userSelectedDate + " was successful")

	time.sleep(3)

	exitProgram();


def exitProgram():

    driver.close()
    sys.exit()

def changeGroupCode():

	global driver

	global GROUP_CODE

	driver = 0

	GROUP_CODE = randint(1000, 9999)

loadUserData()

askUserQuestions()

main()








