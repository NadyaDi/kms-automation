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
    #=============================================================================================================
    def getSearchBarElement(self):
        return self.get_element(self.MY_HISTORY_SEARCH_BAR)    
    
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
        # Search Entry     
        self.getSearchBarElement().click()
        self.getSearchBarElement().send_keys(entryName)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
     
    
    #  @Author: Inbar Willman    
    #This method search if entry exists or not in My history page    
    def isEntryExistsInMyHistory(self, entryName, timeout=30):    
        self.searchEntryMyHistory(entryName)
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