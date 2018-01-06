from base import *
import clsTestService
from general import General


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
    MY_MEDIA_ENRTY_DELETE_BUTTON                = ('xpath', '//*[@title = "Delete ENTRY_NAME"]')
    MY_MEDIA_CONFIRM_ENTRY_DELETE               = ('id', 'delete_button_1_g9uqjz6t')
    #=============================================================================================================
    def getSearchBarElement(self):
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
        self.searchEntryMyMedia(entryName)
        # Click on delete button
        tmp_entry_name = self.MY_MEDIA_ENRTY_DELETE_BUTTON[1].replace('ENTRY_NAME', entryName)
#         tep_entry_name = tep_entry_name[1].replace('ENTRY_NAME', entryName)
        self.click(tmp_entry_name)
        # Click on confirm delete
         
         
         
         
         
         
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
        self.navigateToMyMedia()
        # Search Entry     
        self.getSearchBarElement().click()
        self.send_keys(self.MY_MEDIA_SEARCH_BAR, entryName)
        self.clsCommon.general.waitForLoaderToDisappear()
        
        
    def clickEntryAfterSearchInMyMedia(self, entryName):    
        # Click on the Entry name
        if self.click(('xpath', "//span[@class='entry-name' and text()='" + entryName + "']"), 10) == False:
            # If entry not found, search for 'No Entries Found' alert
            if self.wait_for_text(self.MY_MEDIA_NO_RESULTS_ALERT, 'No Entries Found', 5) == True:
                writeToLog("INFO","No Entry: '" + entryName + "' was found")
            else:
                writeToLog("INFO","FAILED search for Entry: '" + entryName + "' something went wrong")
            
