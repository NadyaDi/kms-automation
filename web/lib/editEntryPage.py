from base import *
import clsTestService
import clsCommon


class EditEntryPage(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Entry Page locators:
    #=============================================================================================================
    EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE            = ('id', "entryName")      
    #=============================================================================================================
    
    def navigateToEditEntryPageFromMyMedia(self, entryName):
        if self.clsCommon.myMedia.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to find: '" + entryName + "'")
            return False
                    
        if self.clsCommon.myMedia.clickEditEntryAfterSearchInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to on entry Edit button, Entry name: '" + entryName + "'")
            return False
        
        #Wait page load - wait for entry title
        if self.wait_visible(self.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE, 15) == False:
            writeToLog("INFO","FAILED to open edit entry page, Entry name: '" + entryName + "'")
            return False

    def navigateToEditEntryPageFromEntryPage(self):
        #Open "Actions" drop-down list 
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
            writeToLog("INFO","FAILED to click on Actions button")
            return False
        
        #Wait up to 5s
        self.wait_visible(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON, 5)  
         
        #Click on Edit button
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Edit button")
            return False    
        
        #Wait page load - wait for entry title
        if self.wait_visible(self.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE, 15) == False:
            writeToLog("INFO","FAILED to open edit entry page")
            return False
        