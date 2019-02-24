from selenium.webdriver.common.action_chains import ActionChains
 
 
from base import *
import clsTestService
import enums
from selenium.webdriver.common.keys import Keys
from general import General



class  Recscheduling(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #================================
    #=============================================================================================================
    #General locators: 
    #=============================================================================================================
    SCHEDULE_PAGE_TITLE                                 = ('xpath', "//h1[@class='inline' and text()='My Schedule']")
    USER_MENU_MY_SCHEDULE_BUTTON                        = ('xpath', "//a[@role='menuitem' and text()='My Schedule']")
    SCHEDULE_CREATE_EVENT_BUTTON                        = ('xpath', "//a[@id='create-event-btn']")
    SCHEDULE_CREATE_EVENT_PAGE_TITLE                    = ('xpath', "//h1[@class='inline' and contains(text(),'Create Event')]")
    SCHEDULE_EVENT_TITLE                                = ('xpath', "//input[@id='CreateEvent-eventTitle']")
    SCHEDULE_EVENT_ORGANIZER                            = ('xpath', "//input[@id='CreateEvent-eventOrganizer']")
    SCHEDUL_EVENT_START_TIME                            = ('xpath', "//input[@id='rsStartTime-rsStartTime_time']")
    SCHEDUL_EVENT_END_TIME                              = ('xpath', "//input[@id='rsEndTime-rsEndTime_time']")
    SCHEDULE_EVENT_DESCRIPTION                          = ('xpath', "//textarea[@id='CreateEvent-eventDescription']")
    SCHEDULE_EVENT_INPUT_TAGS                           = ('xpath', "//input[contains(@id,'s2id_autogen') and contains(@class, '-input')]")
    SCHEDULE_EVENT_TAGS                                 = ('xpath', "//div[@id='s2id_CreateEvent-tags']")
    SCHEDULE_SAVE_EVENT                                 = ('xpath', "//button[@id='CreateEvent-btnSave' and contains(text(),'Save')]")
    SCHEDULE_SAVE_AND_EXIT_EVENT                        = ('xpath', "//button[@id='CreateEvent-btnCreateEvent' and contains(text(),'Save and Exit')]")
    SCHEDULE_CREATE_EVENT_SUCCESS_MESSAGE               = ('xpath', "//p[contains(text(),'Event created successfully.')]")
    SCHEDULE_EVENT_RESOURCES                            = ('xpath', "//input[@placeholder='Click here to search resource']")
    SCHEDULE_EVENT_RESOURCE                             = ('xpath', "//div[@class='sol-label-text' and contains(text(),'RESOURCE_NAME')]")
    #=============================================================================================================
    
    # @Author: Michal Zomper 
    def navigateToMySchedule(self, forceNavigate=False):
        # Check if we are already in my media page
        if forceNavigate == False:
            if self.wait_element(self.SCHEDULE_PAGE_TITLE, 5) == True:
                writeToLog("INFO","Already in My Schedule")
                return True

        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False

        # Click on My Media
        if self.click(self.USER_MENU_MY_SCHEDULE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on My Schedule from the user menu")
            return False

        if self.wait_element(self.SCHEDULE_PAGE_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to My Schedule page")
            return False

        return True
    
    
    # @Author: Michal Zomper 
    # The function create new reschedule event 
    def createRescheduleEvent(self, title, startDate, endDate, startTime, endTime, description, tags, CopyDetailsEventToRecording, resources='', eventOrganizer='', isRecurrence=False, exitEvent=False):
        if self.createRescheduleEventWithoutRecurrence(title, startDate, endDate, startTime, endTime, description, tags, CopyDetailsEventToRecording, resources='', eventOrganizer='', exitEvent=False) == False:
            writeToLog("INFO","FAILED to create schdule event")
            return False
            
        if isRecurrence == True:
            writeToLog("INFO","FAILED to create schdule event")
            
            
            
            
            
    
    
    # @Author: Michal Zomper 
    # The function create new reschedule event without recurrence
    def createRescheduleEventWithoutRecurrence(self, title, startDate, endDate, startTime, endTime, description, tags, copyDetails, resources='', eventOrganizer='', exitEvent=False): 
        if self.navigateToCreateEventPage() == False:
            writeToLog("INFO","FAILED to enter create event page")
            return False
        
        if self.send_keys(self.SCHEDULE_EVENT_TITLE, title) == False:
            writeToLog("INFO","FAILED to insert event title")
            return False
            
        if eventOrganizer != '':
            self.send_keys(self.SCHEDULE_EVENT_ORGANIZER, Keys.CONTROL + 'a')
            if self.send_keys(self.SCHEDULE_EVENT_ORGANIZER, eventOrganizer) == False:
                writeToLog("INFO","FAILED to change event organizer name")
                return False
        
        if self.clsCommon.editEntryPage.setScheduleStartDate(startDate) == False:
            writeToLog("INFO","FAILED to set event start date")
            return False
        sleep(2) 
        
        if len(startTime) != 0:
            if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDUL_EVENT_START_TIME, startTime) == False:
                writeToLog("INFO","FAILED to set event start time")
                return False
            sleep(2) 
        # else = use the default value
        
        if self.clsCommon.editEntryPage.setScheduleEndDate(endDate) == False:
            writeToLog("INFO","FAILED to set event end date")
            return False
        sleep(2)  
        # else = use the default value
        
        if len(endTime) != 0:
            if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDUL_EVENT_END_TIME, endTime) == False:
                writeToLog("INFO","FAILED to set event end time")
                return False
            sleep(2)
        
        if resources != '':
            if self.click(self.SCHEDULE_EVENT_RESOURCES) == False:
                writeToLog("INFO","FAILED to click and open resource option")
                return False
            
            if type(resources) is list: 
                for resource in resources:
                    tmpResource = (self.SCHEDULE_EVENT_RESOURCE[0], self.SCHEDULE_EVENT_RESOURCE[1].replace('RESOURCE_NAME', resource.value))
                    if self.click(tmpResource) == False:
                        writeToLog("INFO","FAILED to select event resource")
                        return False
            else:
                tmpResource = (self.SCHEDULE_EVENT_RESOURCE[0], self.SCHEDULE_EVENT_RESOURCE[1].replace('RESOURCE_NAME', resource.value))
                if self.click(tmpResource) == False:
                    writeToLog("INFO","FAILED to select event resource")
                    return False
                
            # click on the create event title to close the resource list
            self.click(self.SCHEDULE_CREATE_EVENT_PAGE_TITLE)
            
        # Enter text Description
        if self.click(self.SCHEDULE_EVENT_DESCRIPTION) == False:
            writeToLog("INFO","FAILED to click in description textbox")
            return False
            
        if self.clear_and_send_keys(self.SCHEDULE_EVENT_DESCRIPTION, description) == False:
            writeToLog("INFO","FAILED to type in Description")
            return False
        
        if self.fillFileScheduleTags(tags) == False:
            writeToLog("INFO","FAILED to set event tags")
            return False
        
        if copyDetails == False:
            writeToLog("INFO","FAILED to set event tags")
            return False
            
        if exitEvent==False:
            if self.click(self.SCHEDULE_SAVE_EVENT) == False:
                writeToLog("INFO","FAILED click on save event button")
                return False
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_element(self.SCHEDULE_CREATE_EVENT_SUCCESS_MESSAGE) == False:
                writeToLog("INFO","FAILED find event created success message")
                return False
        else:
            if self.click(self.SCHEDULE_SAVE_AND_EXIT_EVENT) == False:
                writeToLog("INFO","FAILED click on save and exit event button")
                return False
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_element(self.SCHEDULE_PAGE_TITLE, 15) == False:
                writeToLog("INFO","FAILED to verify 'My Schedule page' display after clicking on save and exit event button")
                return False
            
        return True
            
            
    # The method supports BOTH single and multiple upload
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillFileScheduleTags(self, tags):
        try:
            tagsElement = self.get_element(self.SCHEDULE_EVENT_TAGS)
                
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get Tags filed element")
            return False
                
        if self.clickElement(tagsElement) == False:
            writeToLog("INFO","FAILED to click on Tags filed")
            return False            
        sleep(1)

#         if(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
#             # Remove the Mask over all the screen (over tags filed also)
#             maskOverElement = self.get_element(self.clsCommon.channel.CHANNEL_REMOVE_TAG_MASK)
#             self.driver.execute_script("arguments[0].setAttribute('style','display: none;')",(maskOverElement))
#           
#             if self.clickElement(tagsElement) == False:
#                 writeToLog("DEBUG","FAILED to click on Tags filed")
#                 return False    

        if self.send_keys(self.SCHEDULE_EVENT_INPUT_TAGS, tags) == True:
            sleep(2)
            return True
    
            
        writeToLog("INFO","FAILED to type in Tags")
        return False   
        
        
    # @Author: Michal Zomper   
    def navigateToCreateEventPage(self, forceNavigate=False):
        if self.navigateToMySchedule(forceNavigate) == False:
            writeToLog("INFO","FAILED navigate to My Schedule page")
            return False
        
        if self.click(self.SCHEDULE_CREATE_EVENT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on create event button")
            return False
        
        if self.wait_element(self.SCHEDULE_CREATE_EVENT_PAGE_TITLE, timeout=15) == False:
            writeToLog("INFO","FAILED to verify create event page is display")
            return False
            
        return True
        