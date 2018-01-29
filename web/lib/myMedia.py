from base import *
import clsTestService
from general import General
from logger import writeToLog
from editEntryPage import EditEntryPage
import enums



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
    MY_MEDIA_ENRTY_DELETE_BUTTON                                = ('xpath', '//*[@title = "Delete ENTRY_NAME"]')# When using this locator, replace 'ENTRY_NAME' string with your real entry name
    MY_MEDIA_ENRTY_EDIT_BUTTON                                  = ('xpath', '//*[@title = "Edit ENTRY_NAME"]')# When using this locator, replace 'ENTRY_NAME' string with your real entry name
    MY_MEDIA_CONFIRM_ENTRY_DELETE                               = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    MY_MEDIA_ENTRY_CHECKBOX                                     = ('xpath', '//*[@title = "ENTRY_NAME"]')
    MY_MEDIA_ACTIONS_BUTTON                                     = ('id', 'actionsDropDown')
    MY_MEDIA_ACTIONS_BUTTON_PUBLISH_BUTTON                      = ('id', 'Publish')
    MY_MEDIA_PUBLISH_UNLISTED                                   = ('id', 'unlisted')
    MY_MEDIA_PUBLISH_SAVE_BUTTON                                = ('xpath', "//button[@class='btn btn-primary pblSave' and text()='Save']")
    MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG                          = ('xpath', "//div[contains(.,'Media successfully set to Unlisted')]")
    MY_MEDIA_PAGE_TITLE                                         = ('xpath', "//h1[@class='inline' and contains(text(), 'My Media')]")
    MY_MEDIA_PUBLISHED_RADIO_BUTTON                             = ('id', 'published') #This refers to the publish radio button after clicking action > publish
    MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION                         = ('class_name', 'pblTabCategory')
    MY_MEIDA_PUBLISH_TO_CHANNEL_OPTION                          = ('class_name', 'pblTabChannel')
    MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH                         = ('xpath', "//span[contains(.,'PUBLISHED_CATEGORY')]")# When using this locator, replace 'PUBLISHED_CATEGORY' string with your real category/channel name
    MY_MEDIA_SAVE_MESSAGE_CONFIRM                               = ('xpath', "//div[@class='alert alert-success ' and contains(text(), 'Media successfully published')]")
    MY_MEDIA_DISCLAIMER_MSG                                     = ('xpath', "//div[@class='alert ' and contains(text(), 'Complete all the required fields and save the entry before you can select to publish it to categories or channels.')]")
    #=============================================================================================================
    def getSearchBarElement(self):
#         if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
#             return self.get_elements(self.MY_MEDIA_SEARCH_BAR)[0]
#         else:
#             return self.get_elements(self.MY_MEDIA_SEARCH_BAR)[1]
        return self.get_element(self.MY_MEDIA_SEARCH_BAR)
    
    
    # This method, clicks on the menu and My Media
    def navigateToMyMedia(self, forceNavigate = False):
        # Check if we are already in my media page
        if forceNavigate == False:
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 1) == True:
                writeToLog("INFO","Success Already in my media page")
                return True
        
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
        
    # Author: Michal Zomper   
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
        
        writeToLog("INFO","Entry: '" + entryName + "' Was Deleted")
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
        if self.navigateToMyMedia(True) == False:
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
    
    # Author: Michal Zomper    
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
          
                
    #  @Author: Tzachi Guetta                   
    def checkSingleEntryInMyMedia(self, entryName):  
        if self.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to find: '" + entryName + "'")
            return False
        
        # Click on the Entry's check-box in MyMedia page
        tmp_entry_name = (self.MY_MEDIA_ENTRY_CHECKBOX[0], self.MY_MEDIA_ENTRY_CHECKBOX[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            # If entry not found, search for 'No Entries Found' alert
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False
        
        return True
    
    
    #  @Author: Tzachi Guetta       
    def clickActionsAndPublishFromMyMedia(self):
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Action button")
            return False 
        
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON_PUBLISH_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Publish button")
            return False
        
        sleep(1)
        return True
    
    
    #  @Author: Tzachi Guetta       
    def publishSingleEntryPrivacyToUnlistedInMyMedia(self, entryName):  
        if self.checkSingleEntryInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False
        
        if self.clickActionsAndPublishFromMyMedia() == False:
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
    
    
    #  @Author: Tzachi Guetta       
    def handleDisclaimerBeforePublish(self, entryName):  
        if self.checkSingleEntryInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False
        
        if self.clickActionsAndPublishFromMyMedia() == False:
            writeToLog("INFO","FAILED to click on Action button, Entry: '" + entryName + "' something went wrong")
            return False
        
        if self.wait_visible(self.MY_MEDIA_DISCLAIMER_MSG) == False:
            writeToLog("INFO","FAILED, Disclaimer alert (before publish) wasn't presented although Disclaimer module is turned on")
            return False
        
        if self.clsCommon.editEntryPage.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to navigate to Edit entry page, Entry: '" + entryName + "' something went wrong")
            return False
        
        if self.click(self.clsCommon.upload.UPLOAD_ENTRY_DISCLAIMER_CHECKBOX) == False:
            writeToLog("INFO","FAILED to click on disclaimer check-box")
            return False
        
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on save button at edit entry page")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        
        if self.navigateToMyMedia() == False:
            writeToLog("INFO","FAILED to navigate to my media")
            return False         
        
        return True      
    
    
    # Author: Michal Zomper       
    # publishFrom - enums.PublishFrom
    # in categoryList / channelList will have all the names of the categories / channels to publish to
    def publishSingleEntry(self, entryName, categoryList, channelList, publishFrom = enums.PublishFrom.MY_MEDIA, disclaimer=False): 
        if publishFrom == enums.PublishFrom.MY_MEDIA: 
            if self.navigateToMyMedia() == False:
                writeToLog("INFO","FAILED to navigate to my media")
                return False
            
            if self.checkSingleEntryInMyMedia(entryName) == False:
                writeToLog("INFO","FAILED to check entry '" + entryName + "' check box")
                return False
         
            if self.clickActionsAndPublishFromMyMedia() == False:
                writeToLog("INFO","FAILED to click on action button")
                return False
                sleep(7)  
                  
        elif publishFrom == enums.PublishFrom.ENTRY_PAGE: 
            sleep(1)
            # Click on action tab
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST, 30) == False:
                writeToLog("INFO","FAILED to click on action button in entry page '" + entryName + "'")
                return False  
            
            sleep(1)
            # Click on publish button
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_PUBLISH_BUTTON, 30) == False:
                writeToLog("INFO","FAILED to click on publish button in entry page '" + entryName + "'")
                return False

        elif publishFrom == enums.PublishFrom.UPLOAD_PAGE: 
            writeToLog("INFO","Publishing from Upload page, Entry name: '" + entryName + "'")            
         
        #checking if disclaimer is turned on for "Before publish"
        if disclaimer == True:
            if self.handleDisclaimerBeforePublish(entryName) == False:
                writeToLog("INFO","FAILED, Handle disclaimer before Publish failed")
                return False
         
        sleep(2)            
        self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 30)
     
        sleep(2)    
        # Click if category list is empty
        if len(categoryList) != 0:
            # Click on Publish in Category
            if self.click(self.MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION, 30) == False:
                writeToLog("INFO","FAILED to click on Publish in Category")
                return False
            
            # choose all the  categories to publish to
            for category in categoryList: 
                tmoCategoryName = (self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', category))
 
                if self.click(tmoCategoryName, 30) == False:
                    writeToLog("INFO","FAILED to select published category '" + category + "'")
                    return False
                
        sleep(2)
        # Click if channel list is empty
        if len(channelList) != 0:
            # Click on Publish in Channel
            if self.click(self.MY_MEIDA_PUBLISH_TO_CHANNEL_OPTION, 30) == False:
                writeToLog("INFO","FAILED to click on Publish in channel")
                return False 
            sleep(2)
            
            # choose all the  channels to publish to
            for channel in channelList:
                tmpChannelName = (self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', channel))
   
                if self.click(tmpChannelName, 30) == False:
                    writeToLog("INFO","FAILED to select published channel '" + channel + "'")
                    return False
                
        sleep(1)   
        if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False                
                
        if self.wait_visible(self.MY_MEDIA_SAVE_MESSAGE_CONFIRM, 30) == None:
            writeToLog("INFO","FAILED to find confirm save message")
            return False
        
        sleep(3)       
        writeToLog("INFO","Success to publish entry '" + entryName + "'")
        return True
    
    #TODO
    #def verifyPublish(self, entryName, categoryList, channelList):
                
