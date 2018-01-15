from base import *
import clsTestService
from general import General
from logger import writeToLog


class MyMedia(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #My Media locators:
    #=============================================================================================================
    MY_MEDIA_SEARCH_BAR                         = ('id', 'searchBar')
    MY_MEDIA_NO_RESULTS_ALERT                   = ('xpath',"//div[@class='alert alert-info no-results']")
    MY_MEDIA_ENRTY_DELETE_BUTTON                = ('xpath', '//*[@title = "Delete ENTRY_NAME"]')# When using this locator, replace 'ENTRY_NAME' string with your real entry name
    MY_MEDIA_ENRTY_EDIT_BUTTON                  = ('xpath', '//*[@title = "Edit ENTRY_NAME"]')# When using this locator, replace 'ENTRY_NAME' string with your real entry name
    MY_MEDIA_CONFIRM_ENTRY_DELETE               = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    #=============================================================================================================
    def getSearchBarElement(self):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            return self.get_elements(self.MY_MEDIA_SEARCH_BAR)[0]
        else:
            return self.get_elements(self.MY_MEDIA_SEARCH_BAR)[1]
    
    # This method, clicks on the menu and My Media
    def navigateToMyMedia(self):
        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False
        
        # Click on My Media
        if self.click(self.clsCommon.general.USER_MENU_MY_MEDIA_BUTTON) == False:
            writeToLog("INFO","FAILED to on My Media from the menu")
            return False
        
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False) == False:
            writeToLog("INFO","FAILED to navigate to My Media")
            return False
        
        return True
        
#     def navigateToEditEntryPage(self):
#         
    def deleteSingleEntryFromMyMedia(self, entryName):
        # Search for entry in my media
        if self.searchEntryMyMedia(entryName) == False:
            return False
        # Click on delete button
        tmp_entry_name = (self.MY_MEDIA_ENRTY_DELETE_BUTTON[0], self.MY_MEDIA_ENRTY_DELETE_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            writeToLog("INFO","FAILED to click on delete entry button")
            return False
        sleep(2)
        # Click on confirm delete
        if self.click(self.MY_MEDIA_CONFIRM_ENTRY_DELETE) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
#         
#     def deleteMultipleEntries(self):
#     
    def showAllEntriesInMyMedia(self, timeout):
        # Navigate to My Media
        self.navigateToMyMedia()
        # Press END key till "There are no more media items." is visible
        # Press Home

        
    def searchEntryMyMedia(self, entryName):
        # Navigate to My Media
        if self.navigateToMyMedia() == False:
            return False
        # Search Entry     
        self.getSearchBarElement().click()
        self.getSearchBarElement().send_keys(entryName)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
        
        
    def clickEntryAfterSearchInMyMedia(self, entryName):    
        # Click on the Entry name
        if self.click(('xpath', "//span[@class='entry-name' and text()='" + entryName + "']"), 10) == False:
            # If entry not found, search for 'No Entries Found' alert
            if self.wait_for_text(self.MY_MEDIA_NO_RESULTS_ALERT, 'No Entries Found', 5) == True:
                writeToLog("INFO","No Entry: '" + entryName + "' was found")
            else:
                writeToLog("INFO","FAILED search for Entry: '" + entryName + "' something went wrong")
    

    def clickEditEntryAfterSearchInMyMedia(self, entryName):    
        # Click on the Edit Entry button
        tmp_entry_name = (self.MY_MEDIA_ENRTY_EDIT_BUTTON[0], self.MY_MEDIA_ENRTY_EDIT_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            # If entry not found, search for 'No Entries Found' alert
            if self.wait_for_text(self.MY_MEDIA_NO_RESULTS_ALERT, 'No Entries Found', 5) == True:
                writeToLog("INFO","No Entry: '" + entryName + "' was found")
            else:
                writeToLog("INFO","FAILED search for Entry: '" + entryName + "' something went wrong")
            
