import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

STUDENT_INFORMATION = ["XXXXXXXXX", "XXXXXXXXXX"]

def getDateString():

    month = time.strftime("%B")
    
    day = time.strftime("%d")
           
    dateString = month + " " + "21"

    return dateString

def requestTimeFromUser():

    return "Time: 8:00 PM. Room no.: LIB303"

def checkConsecutiveFreeTime():
    return true

def checkIfTimeSlotIsFree():
    return true

def clickLinkByTitle(title):
    driver.find_element_by_css_selector("a[title='" + title  + "']").click() 

def fillInForm(studentNo, password):
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

###########################################################################

datePickingURL = "https://rooms.library.dc-uoit.ca/uoit_studyrooms/calendar.aspx"

try:

    driver = webdriver.Chrome()

except:

    print "A connection error occured"

driver.get(datePickingURL)

try:


    element = WebDriverWait(driver, 10).until(

        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_LabelInitialMessage"))
)

except:

    print "Error loading inital page"

dateSelection = getDateString()

#time.sleep(1)

clickLinkByTitle(dateSelection)

timeSelection = requestTimeFromUser()

#time.sleep(1)

clickLinkByTitle(timeSelection)

try:

    element = WebDriverWait(driver, 10).until(

        EC.presence_of_element_located((By.CLASS_NAME, "SiteFooter"))
    )

except:

    print "Error following first link/loading second page"

fillInForm(STUDENT_INFORMATION[0], STUDENT_INFORMATION[1])
