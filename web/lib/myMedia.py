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
    #Upload XPATH locators:
    #=============================================================================================================
    MY_MEDIA_SEARCH_BAR                         = ('id', 'searchBar')
    MY_MEDIA_NO_RESULTS_ALERT                   = ('xpath',"//div[@class='alert alert-info no-results']")
    #=============================================================================================================
    
    # This method, clicks on the menu and My Media
    def navigateToMyMedia(self):
        # Click on User Menu Toggle Button
        self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON)
        
        # Click on Me Media
        self.click(self.clsCommon.general.USER_MENU_MY_MEDIA_BUTTON)
        self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False)
        
#     def navigateToEditEntryPage(self):
#         
#     def deleteSingleEntryFromMyMedia(self):
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
        self.click(self.MY_MEDIA_SEARCH_BAR)
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
            
