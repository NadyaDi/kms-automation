from base import *
import clsTestService
from general import General
from logger import writeToLog
from editEntryPage import EditEntryPage
import enums
import clsCommon


class MyHistory(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #My History locators:
    #=============================================================================================================
    MY_HISTORY_SEARCH_BAR                                         = ('id', 'searchBar')
    MY_HISTORY_RESULTS_ENTRY                                      = ('xpath', '//span[@class="entry-name" and text() = "ENTRY_NAME"]')
    MY_HISTORY_REMOVE_ENTRY_BUTTON                                = ('xpath', "//a[@href = '/history/delete/entry-id/ENTRY_ID']")
    MY_HISTORY_ENTRY                                              = ('xpath', "//a[contains(@href, '/media/') and contains(text(), 'ENTRY_NAME')]")  
    MY_HISTORY_ENTRY_DELETED_MESSAGE                              = ('xpath', '//div[@class = "lead"]')  
    MY_HISTORY_CLEAR_HISORY_BUTTON                                = ('xpath', '//button[@href = "/history/clear"]')  
    MY_HISTORY_CONFIRM_HISTORY_DELETE                             = ('xpath', "//a[@class='btn btn-danger' and @data-handler = '1']")
    MY_HISTORY_CLEAR_HISTORY_SUCCESS_MESSAGE                      = ('class_name', 'empty-header')
    #=============================================================================================================
    def getSearchBarElement(self):
        # We got multiple elements, search for element which is not size = 0
        elements = self.get_elements(self.MY_HISTORY_SEARCH_BAR)
        for el in elements:
            if el.size['width']!=0 and el.size['height']!=0:
                return el
        return False      
    
    #  @Author: Inbar Willman
    # This method, clicks on the menu and My History
    def navigateToMyHistory(self, forceNavigate = False):
        # Check if we are already in my history page
        if forceNavigate == False:
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_HISTORY_URL, False, 1) == True:
                writeToLog("INFO","Success Already in My History page")
                return True
        
        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False
        
        # Click on My history
        if self.click(self.clsCommon.general.USER_MENU_MY_HISTORY_BUTTON ) == False:
            writeToLog("INFO","FAILED to click on My History from the menu")
            return False
        
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_HISTORY_URL, False) == False:
            writeToLog("INFO","FAILED to navigate to My History")
            return False
        
        return True
     
    
    #  @Author: Inbar Willman    
    #This method search for entry in My history page   
    def searchEntryMyHistory(self, entryName):
        # Navigate to My Media
        if self.navigateToMyHistory(True) == False:
            return False
        
        # Check if search field is displayed 
        if self.isSearchFieldIsDisplayed() == False:
            return False
        
        #If search field is displayed make a search
        self.getSearchBarElement().click()
        self.getSearchBarElement().send_keys(entryName)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
     
    
    #  @Author: Inbar Willman    
    #This method search if entry exists or not in My history page    
    def isEntryExistsInMyHistory(self, entryName, timeout=30):    
        if self.searchEntryMyHistory(entryName) == False:
            return False
        tmpEntryName = (self.MY_HISTORY_RESULTS_ENTRY [0], self.MY_HISTORY_RESULTS_ENTRY [1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmpEntryName, timeout) == False: 
            return False
  
        return True
    
    
    #  @Author: Inbar Willman
    def waitTillLocatorExistsInMyHistory(self, entryName, timeout=30):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)   
        while wait_until > datetime.datetime.now(): 
            if self.isEntryExistsInMyHistory(entryName, 5):
                #Entry exist
                return True
        writeToLog("INFO","FAILED to find entry in My History")
        return False
    
    
    #  @Author: Inbar Willman
    def removeEntryFromWatchListMyHistory(self, entryName):
        tmpEntry = (self.MY_HISTORY_ENTRY[0], self.MY_HISTORY_ENTRY[1].replace('ENTRY_NAME', entryName))
        entryId = self.clsCommon.upload.extractEntryID(tmpEntry)
        tmpDeleteBtn = (self.MY_HISTORY_REMOVE_ENTRY_BUTTON[0], self.MY_HISTORY_REMOVE_ENTRY_BUTTON[1].replace('ENTRY_ID', entryId))
        if self.click(tmpDeleteBtn) == False:
            writeToLog("INFO","FAILED to delete entry: " + entryName)
            return False 
        
        #Verify that correct message is displayed
        tmpMessage = self.get_element_text(self.MY_HISTORY_ENTRY_DELETED_MESSAGE)
        if "This item has been removed from your history." != tmpMessage:
            writeToLog("INFO","FAILED to display correct message")
            return False 
        
        return True

    
    #  @Author: Inbar Willman      
    def clearHistory(self):
        if self.click(self.MY_HISTORY_CLEAR_HISORY_BUTTON) ==  False:
            writeToLog("INFO","FAILED to click clear history")
            return False 
        
        sleep(2)
        
        if self.click(self.MY_HISTORY_CONFIRM_HISTORY_DELETE) == False:
            writeToLog("INFO","FAILED to click confirm deletion")
            return False
        
        #Verify that correct message is displayed
        tmpMessage = self.get_element_text(self.MY_HISTORY_CLEAR_HISTORY_SUCCESS_MESSAGE)
        if 'Your feed is empty' != tmpMessage:
            writeToLog("INFO","FAILED to display correct answer")
            return False 
        
        return True
    
    
    # @Author: Inbar Willman   
    # Check if search field is displayed in page (in case My History is empty search field isn't displayed).
    def isSearchFieldIsDisplayed(self):
        if self.wait_visible(self.MY_HISTORY_CLEAR_HISTORY_SUCCESS_MESSAGE) == False:
            if self.wait_visible(self.MY_HISTORY_SEARCH_BAR) == False:
                return False 
            return True
      
        return False
        