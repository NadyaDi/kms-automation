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
    MY_MEDIA_SEARCH_BAR                                         = ('id', 'searchBar')
    MY_MEDIA_NO_RESULTS_ALERT                                   = ('xpath',"//div[@class='alert alert-info no-results']")
    MY_MEDIA_ENRTY_DELETE_BUTTON                                = ('xpath', '//*[@title = "Delete ENTRY_NAME"]')
    MY_MEDIA_ENRTY_EDIT_BUTTON                                  = ('xpath', '//*[@title = "Edit ENTRY_NAME"]')
    MY_MEDIA_CONFIRM_ENTRY_DELETE                               = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    MY_MEDIA_ENTRY_CHECKBOX                                     = ('xpath', '//*[@title = "ENTRY_NAME"]')
    MY_MEDIA_ACTIONS_BUTTON                                     = ('id', 'actionsDropDown')
    MY_MEDIA_ACTIONS_BUTTON_PUBLISH_BUTTON                      = ('id', 'Publish')
    MY_MEDIA_PUBLISH_UNLISTED                                   = ('id', 'unlisted')
    MY_MEDIA_PUBLISH_SAVE_BUTTON                                = ('xpath', "//button[@class='btn btn-primary pblSave' and text()='Save']")
    MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG                          = ('xpath', "//div[contains(.,'Media successfully set to Unlisted')]")
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
                
        return True
    

    def clickEditEntryAfterSearchInMyMedia(self, entryName):    
        # Click on the Edit Entry button
        tmp_entry_name = (self.MY_MEDIA_ENRTY_EDIT_BUTTON[0], self.MY_MEDIA_ENRTY_EDIT_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            # If entry not found, search for 'No Entries Found' alert
            if self.wait_for_text(self.MY_MEDIA_NO_RESULTS_ALERT, 'No Entries Found', 5) == True:
                writeToLog("INFO","No Entry: '" + entryName + "' was found")
            else:
                writeToLog("INFO","FAILED search for Entry: '" + entryName + "' something went wrong")
                
        return True       
                
    def checkSingleEntryInMyMedia(self, entryName):  
        if self.clsCommon.myMedia.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to find: '" + entryName + "'")
            return False
        
        # Click on the Entry's check-box in MyMedia page
        tmp_entry_name = (self.MY_MEDIA_ENTRY_CHECKBOX[0], self.MY_MEDIA_ENTRY_CHECKBOX[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            # If entry not found, search for 'No Entries Found' alert
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False
        
        return True
    
    
    def clickActionsAndPublish(self):
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Action button")
            return False 
        
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON_PUBLISH_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Publish button")
            return False
        
        return True
    
    
    def publishSingleEntryPrivacyToUnlisted(self, entryName):  
        if self.clsCommon.myMedia.checkSingleEntryInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False
        
        if self.clickActionsAndPublish() == False:
            writeToLog("INFO","FAILED to click on Action button, Entry: '" + entryName + "' something went wrong")
            return False
        
        if self.click(self.MY_MEDIA_PUBLISH_UNLISTED) == False:
            writeToLog("INFO","FAILED to click on Unlisted button")
            return False 
        
        if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Unlisted button")
            return False
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()
        
        if self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG, 20) == False:
            writeToLog("INFO","FAILED to Publish Entry: '" + entryName + "' something went wrong")
            return False
        
        return True 
        