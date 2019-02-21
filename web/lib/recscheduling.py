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
    SCHEDULE_EVENT_DESCRIPTION                          = ('xpath', "//input[@id='CreateEvent-eventDescription']")
    SCHEDULE_EVENT_TAGS                                 = ('xpath', "//input[@id='CreateEvent-tags']")
    
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