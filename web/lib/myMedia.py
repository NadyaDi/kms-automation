from base import *
import clsTestService
from general import General
from logger import writeToLog
from editEntryPage import EditEntryPage
import enums
from selenium.webdriver.common.keys import Keys



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
    MY_MEDIA_NO_RESULTS_ALERT                                   = ('xpath', "//div[@id='myMedia_scroller_alert' and contains(text(),'There are no more media items.')]")
    MY_MEDIA_ENRTY_DELETE_BUTTON                                = ('xpath', '//*[@title = "Delete ENTRY_NAME"]')# When using this locator, replace 'ENTRY_NAME' string with your real entry name
    MY_MEDIA_ENRTY_EDIT_BUTTON                                  = ('xpath', '//*[@title = "Edit ENTRY_NAME"]')# When using this locator, replace 'ENTRY_NAME' string with your real entry name
    MY_MEDIA_CONFIRM_ENTRY_DELETE                               = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    MY_MEDIA_ENTRY_CHECKBOX                                     = ('xpath', '//*[@title = "ENTRY_NAME"]')
    MY_MEDIA_ACTIONS_BUTTON                                     = ('id', 'actionsDropDown')
    MY_MEDIA_ACTIONS_BUTTON_PUBLISH_BUTTON                      = ('id', 'Publish')
    MY_MEDIA_ACTIONS_BUTTON_DELETE_BUTTON                       = ('id', 'tab-Delete')
    MY_MEDIA_ACTIONS_BUTTON_ADDTOPLAYLIST_BUTTON                = ('id', 'Addtoplaylists')
    MY_MEDIA_PUBLISH_UNLISTED                                   = ('id', 'unlisted')
    MY_MEDIA_PUBLISH_PRIVATE                                    = ('id', 'private')
    MY_MEDIA_PUBLISH_SAVE_BUTTON                                = ('xpath', "//button[@class='btn btn-primary pblSave' and text()='Save']")
    MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG                          = ('xpath', "//div[contains(.,'Media successfully set to Unlisted')]")
    MY_MEDIA_PUBLISHED_AS_PRIVATE_MSG                           = ('xpath', "//div[contains(.,'Media successfully set to Private')]")
    MY_MEDIA_PAGE_TITLE                                         = ('xpath', "//h1[@class='inline' and contains(text(), 'My Media')]")
    MY_MEDIA_PUBLISHED_RADIO_BUTTON                             = ('id', 'published') #This refers to the publish radio button after clicking action > publish
    MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION                         = ('class_name', 'pblTabCategory')
    MY_MEIDA_PUBLISH_TO_CHANNEL_OPTION                          = ('class_name', 'pblTabChannel')
    MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH                         = ('xpath', "//span[contains(.,'PUBLISHED_CATEGORY')]")# When using this locator, replace 'PUBLISHED_CATEGORY' string with your real category/channel name
    MY_MEDIA_SAVE_MESSAGE_CONFIRM                               = ('xpath', "//div[@class='alert alert-success ' and contains(text(), 'Media successfully published')]")
    MY_MEDIA_DISCLAIMER_MSG                                     = ('xpath', "//div[@class='alert ' and contains(text(), 'Complete all the required fields and save the entry before you can select to publish it to categories or channels.')]")
    #MY_MEDIA_ENTRY_PARNET                                       = ('xpath', "//div[@class='photo-group thumb_wrapper' and @title='ENTRY_NAME']")
    MY_MEDIA_ENTRY_CHILD                                        = ('xpath', "//p[@class='status_content' and contains(text(), 'ENTRY_PRIVACY')]")
    MY_MEDIA_ENTRY_PARNET                                       = ('xpath', "//span[@class='entry-name' and text() ='ENTRY_NAME']/ancestor::a[@class='entryTitle tight']")                                   
    MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI                         = ('xpath', "//a[@id = 'accordion-ENTRY_ID']")
    MY_MEDIA_ENTRY_PUBLISHED_BTN                                = ('xpath', "//a[@id = 'accordion-ENTRY_ID']/i[@class='icon-plus-sign kmstooltip']")
    MY_MEDIA_ENTRY_CHILD_POPUP                                  = ('xpath', "//strong[@class='valign-top']")
    MY_MEDIA_SORT_BY_DROPDOWNLIST                               = ('xpath', "//a[@id='sort-btn']")
    MY_MEDIA_FILTER_BY_STATUS_DROPDOWNLIST                      = ('xpath', "//a[@id='status-btn']")
    MY_MEDIA_FILTER_BY_TYPE_DROPDOWNLIST                        = ('xpath', "//a[@id='type-btn']")
    MY_MEDIA_FILTER_BY_COLLABORATION_DROPDOWNLIST               = ('xpath', "//a[@id='mediaCollaboration-btn']")
    MY_MEDIA_FILTER_BY_SCHEDULING_DROPDOWNLIST                  = ('xpath', "//a[@id='sched-btn']")
    MY_MEDIA_DROPDOWNLIST_ITEM                                  = ('xpath', "//a[@role='menuitem' and contains(text(), 'DROPDOWNLIST_ITEM')]")
    MY_MEDIA_ENTRY_TOP                                          = ('xpath',"//span[@class='entry-name' and text()='ENTRY_NAME']")
    MY_MEDIA_END_OF_PAGE                                        = ('xpath',"//div[@class='alert alert-info endlessScrollAlert']")
    MY_MEDIA_TABLE_SIZE                                         = ('xpath',"//table[@class='table table-condensed table-hover bulkCheckbox mymediaTable mediaTable full']/tbody/tr")
    MY_MEDIA_CONFIRM_CHANGING_STATUS                            = ('xpath',"//a[@class='btn btn-primary' and text()='OK']")
    #=============================================================================================================
    def getSearchBarElement(self):
        # We got multiple elements, search for element which is not size = 0
        elements = self.get_elements(self.MY_MEDIA_SEARCH_BAR)
        for el in elements:
            if el.size['width']!=0 and el.size['height']!=0:
                return el
        return False        
    
    
    # This method, clicks on the menu and My Media
    def navigateToMyMedia(self, forceNavigate = False):
        # Check if we are already in my media page
        if forceNavigate == False:
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 1) == True:
                return True
        
        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False
        
        # Click on My Media
        if self.click(self.clsCommon.general.USER_MENU_MY_MEDIA_BUTTON) == False:
            writeToLog("INFO","FAILED to click on My Media from the user menu")
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
    
    #  @Author: Tzachi Guetta      
    # The following method can handle list of entries and a single entry:
    #    in order to delete list of entries pass a List[] of entries name, for single entry - just pass the entry name
    #    also: the method will navigate to My media
    # Known limitation: entries MUST be presented on the first page of my media
    def deleteEntriesFromMyMedia(self, entriesNames):
        if self.navigateToMyMedia(forceNavigate = True) == False:
            writeToLog("INFO","FAILED Navigate to my media page")
            return False
        
        success = True
        # Checking if entriesNames list type
        if type(entriesNames) is list: 
            for entryName in entriesNames: 
                if self.checkSingleEntryInMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to CHECK the entry in my-media page")
                    success = False
            
                writeToLog("INFO","Going to delete Entry: " + entryName)
        else:
            if self.checkSingleEntryInMyMedia(entriesNames) == False:
                    writeToLog("INFO","FAILED to CHECK the entry in my-media page")
                    success = False
                
            writeToLog("INFO","Going to delete Entry: " + entriesNames)
        
        if self.clickActionsAndDeleteFromMyMedia() == False:
            writeToLog("INFO","FAILED to click Action -> Delete")
            return False
        
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear() 
        
        if self.click(self.MY_MEDIA_CONFIRM_ENTRY_DELETE) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False
        
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear() 
                     
        # Printing the deleted entries
        if success == True:    
            if type(entriesNames) is list: 
                entries = ", ".join(entriesNames)
                writeToLog("INFO","The following entries were deleted: " + entries + "")
            else:
                writeToLog("INFO","The following entry was deleted: " + entriesNames + "")
        else:  
            writeToLog("INFO","Failed, Not all entries were deleted")
            
        return success
     
        
    def searchEntryMyMedia(self, entryName, forceNavigate=True):
        # Check if my media page is already open
        # Navigate to My Media
        if self.navigateToMyMedia(forceNavigate) == False:
            return False
        
        sleep(2)
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
    def serachAndCheckSingleEntryInMyMedia(self, entryName):  
        if self.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to find: '" + entryName + "'")
            return False
        
        # Click on the Entry's check-box in MyMedia page
        if self.checkSingleEntryInMyMedia(entryName) == False:
            return False
    
        return True
    
    #  @Author: Tzachi Guetta     
    def checkSingleEntryInMyMedia(self, entryName):
        # Click on the Entry's check-box in MyMedia page
        tmp_entry_name = (self.MY_MEDIA_ENTRY_CHECKBOX[0], self.MY_MEDIA_ENTRY_CHECKBOX[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            # If entry not found, search for 'No Entries Found' alert
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False
        
        return True
    
    #  @Author: Tzachi Guetta     
    def checkEntriesInMyMedia(self, entriesNames):
        if type(entriesNames) is list: 
            for entryName in entriesNames: 
                if self.checkSingleEntryInMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to CHECK the entry: " + entryName + ", in my media page")
                    return False
                
        else:
            writeToLog("INFO","FAILED, Entries list was not provided")
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
    def clickActionsAndDeleteFromMyMedia(self):
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Action button")
            return False 
        
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON_DELETE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Publish button")
            return False
        
        sleep(1)
        return True
    
    
    #  @Author: Tzachi Guetta
    def clickActionsAndAddToPlaylistFromMyMedia(self):
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Action button")
            return False 
        
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON_ADDTOPLAYLIST_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Publish button")
            return False
        
        sleep(1)
        return True
    
    
    #  @Author: Tzachi Guetta       
    def publishSingleEntryPrivacyToUnlistedInMyMedia(self, entryName):  
        if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
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
        if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
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
    # publishFrom - enums.Location
    # in categoryList / channelList will have all the names of the categories / channels to publish to
    def publishSingleEntry(self, entryName, categoryList, channelList, publishFrom = enums.Location.MY_MEDIA, disclaimer=False):  
        #checking if disclaimer is turned on for "Before publish"
        if disclaimer == True:
            if self.handleDisclaimerBeforePublish(entryName) == False:
                writeToLog("INFO","FAILED, Handle disclaimer before Publish failed")
                return False
            
        if publishFrom == enums.Location.MY_MEDIA: 
            if self.navigateToMyMedia() == False:
                writeToLog("INFO","FAILED to navigate to my media")
                return False
            
            sleep(1)
            if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
                writeToLog("INFO","FAILED to check entry '" + entryName + "' check box")
                return False
         
            if self.clickActionsAndPublishFromMyMedia() == False:
                writeToLog("INFO","FAILED to click on action button")
                return False
                sleep(7)   

            if self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 30) == False:
                writeToLog("DEBUG","FAILED to click on publish button")
                return False     

        elif publishFrom == enums.Location.ENTRY_PAGE:
            sleep(1)
            # Click on action tab
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST, 30) == False:
                writeToLog("INFO","FAILED to click on action button in entry page '" + entryName + "'")
                return False  
            
            sleep(5)
            # Click on publish button
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_PUBLISH_BUTTON, 30) == False:
                writeToLog("INFO","FAILED to click on publish button in entry page '" + entryName + "'")
                return False

        elif publishFrom == enums.Location.UPLOAD_PAGE: 
            writeToLog("INFO","Publishing from Upload page, Entry name: '" + entryName + "'")       
            sleep(2)            
            if self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 45) == False:
                writeToLog("DEBUG","FAILED to click on publish button")
                return False        
          

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
        if publishFrom == enums.Location.MY_MEDIA or publishFrom == enums.Location.ENTRY_PAGE:  
            if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON, 30) == False:
                writeToLog("INFO","FAILED to click on save button")
                return False                
                    
            if self.wait_visible(self.MY_MEDIA_SAVE_MESSAGE_CONFIRM, 45) == False:
                writeToLog("INFO","FAILED to find confirm save message")
                return False
        else:
            if self.click(self.clsCommon.upload.UPLOAD_ENTRY_SAVE_BUTTON) == False:
                writeToLog("DEBUG","FAILED to click on 'Save' button")
                return None
            sleep(2)

            # Wait for loader to disappear
            self.clsCommon.general.waitForLoaderToDisappear()            
        
        sleep(3)       
        writeToLog("INFO","Success to publish entry '" + entryName + "'")
        return True
    
    
    # Author: Tzachi Guetta 
    def verifyEntryPrivacyInMyMedia(self, entryName, expectedEntryPrivacy):
        try:                
            if self.navigateToMyMedia() == False:
                writeToLog("INFO","FAILED to navigate to  my media")
                return False
            
            if expectedEntryPrivacy == enums.EntryPrivacyType.UNLISTED:
            
                parent = self.wait_visible(self.replaceInLocator(self.MY_MEDIA_ENTRY_PARNET, "ENTRY_NAME", entryName))
                child = self.replaceInLocator(self.MY_MEDIA_ENTRY_CHILD, "ENTRY_PRIVACY", 'Unlisted')
                if self.clsCommon.base.get_child_element(parent, child) != None:
                    writeToLog("INFO","As Expected: The privacy of: '" + entryName + "' in My-media page is: '" + str(enums.EntryPrivacyType.UNLISTED) + "'")
                    return True 
            
            elif expectedEntryPrivacy == enums.EntryPrivacyType.PRIVATE:
            
                parent = self.wait_visible(self.replaceInLocator(self.MY_MEDIA_ENTRY_PARNET, "ENTRY_NAME", entryName))
                child = self.replaceInLocator(self.MY_MEDIA_ENTRY_CHILD, "ENTRY_PRIVACY", 'Private')
                if self.clsCommon.base.get_child_element(parent, child) != None:
                    writeToLog("INFO","As Expected: The privacy of: '" + entryName + "' in My-media page is: '" + str(enums.EntryPrivacyType.PRIVATE) + "'")
                    return True 
                
            elif expectedEntryPrivacy == enums.EntryPrivacyType.REJECTED or expectedEntryPrivacy == enums.EntryPrivacyType.PENDING or expectedEntryPrivacy == enums.EntryPrivacyType.PUBLISHED:
                
                tmpEntry = self.replaceInLocator(self.MY_MEDIA_ENTRY_PARNET, "ENTRY_NAME", entryName) 
                entryId = self.clsCommon.upload.extractEntryID(tmpEntry)
                tmpBtn = (self.MY_MEDIA_ENTRY_PUBLISHED_BTN[0], self.MY_MEDIA_ENTRY_PUBLISHED_BTN[1].replace('ENTRY_ID', entryId))
                if self.click(tmpBtn) == False:
                    writeToLog("INFO","FAILED to click on the 'published' pop-up of: " + entryName)
                    return False
                sleep(3)
                
                if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
                    tmpBtn = (self.MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI[0], self.MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI[1].replace('ENTRY_ID', entryId))
                tmpBtn = (tmpBtn[0], tmpBtn[1] + "/descendant::strong[@class='valign-top']")
                if str(expectedEntryPrivacy) in self.get_element_text(tmpBtn):
                    writeToLog("INFO","As Expected: The privacy of: '" + entryName + "' in My-media page is: '" + str(expectedEntryPrivacy) + "'")
                    return True                    
                    
        except NoSuchElementException:
            return False
    
        
    # Author: Tzachi Guetta 
    def SortAndFilter(self, dropDownListName='' ,dropDownListItem=''):
        try:                
            if dropDownListName == enums.SortAndFilter.SORT_BY:
                tmplocator = self.MY_MEDIA_SORT_BY_DROPDOWNLIST
            
            elif dropDownListName == enums.SortAndFilter.PRIVACY:
                tmplocator = self.MY_MEDIA_FILTER_BY_STATUS_DROPDOWNLIST
                
            elif dropDownListName == enums.SortAndFilter.MEDIA_TYPE:
                tmplocator = self.MY_MEDIA_FILTER_BY_TYPE_DROPDOWNLIST
            
            elif dropDownListName == enums.SortAndFilter.COLLABORATION:
                tmplocator = self.MY_MEDIA_FILTER_BY_COLLABORATION_DROPDOWNLIST
                
            elif dropDownListName == enums.SortAndFilter.SCHEDULING:
                tmplocator = self.MY_MEDIA_FILTER_BY_SCHEDULING_DROPDOWNLIST
                
            else:
                writeToLog("INFO","FAILED, drop-down-list name was not provided")
                return False
                
            if self.click(tmplocator, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on: " + str(dropDownListName) + " in my media")
                return False
            
            tmpEntry = self.replaceInLocator(self.MY_MEDIA_DROPDOWNLIST_ITEM, "DROPDOWNLIST_ITEM", str(dropDownListItem)) 
            if self.click(tmpEntry, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on the drop-down list item: " + str(dropDownListItem))
                return False

            self.clsCommon.general.waitForLoaderToDisappear()    
        
        except NoSuchElementException:
            return False
    
        return True
    
    
        # Author: Tzachi Guetta 
    def sortAndFilterInMyMedia(self, sortBy='', filterPrivacy='', filterMediaType='', filterCollaboration='', filterScheduling='', resetFields=False):
        try:         
            if self.navigateToMyMedia(forceNavigate = resetFields) == False:
                writeToLog("INFO","FAILED to navigate to  my media")
                return False                
            
            if sortBy != '':
                if self.SortAndFilter(enums.SortAndFilter.SORT_BY, sortBy) == False:
                    writeToLog("INFO","FAILED to set sortBy: " + str(sortBy) + " in my media")
                    return False
                
            if filterPrivacy != '':
                if self.SortAndFilter(enums.SortAndFilter.PRIVACY, filterPrivacy) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterPrivacy) + " in my media")
                    return False
                
            if filterMediaType != '':
                if self.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, filterMediaType) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterMediaType) + " in my media")
                    return False
                
            if filterCollaboration != '':
                if self.SortAndFilter(enums.SortAndFilter.COLLABORATION, filterCollaboration) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterCollaboration) + " in my media")
                    return False
                
            if filterScheduling != '':
                if self.SortAndFilter(enums.SortAndFilter.SCHEDULING, filterScheduling) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterScheduling) + " in my media")
                    return False                                                     
        
        except NoSuchElementException:
            return False
    
        return True

    
    # Author: Tzachi Guetta 
    # MUST: enableLoadButton must be turned off in KMS admin 
    def scrollToBottom(self, retries=5):
        try:           
            if len(self.get_elements(self.MY_MEDIA_TABLE_SIZE)) < 4:
                return True
            else:
                count = 0
                while count < retries:
                    self.driver.find_element_by_xpath('//body').send_keys(Keys.END)
                    writeToLog("INFO","Scrolling to bottom, retry #: " + str(count+1))
                    sleep(2)
                    if self.wait_visible(self.MY_MEDIA_END_OF_PAGE, 1) != False:
                        writeToLog("INFO","*** Reached the End of page ***")
                        return True
                    count += 1
                    
                writeToLog("INFO","FAILED, scrolled " + str(retries) + " times and didn't reached the bottom of the page, maybe you need add more retries")

        except NoSuchElementException:
            return False
    
        return False

        # Author: Tzachi Guetta 
    def getTop(self, entryName, location):
        try: 
            if location == enums.Location.MY_MEDIA:
                tmpEntry = self.replaceInLocator(self.clsCommon.myMedia.MY_MEDIA_ENTRY_TOP, "ENTRY_NAME", entryName)
                
            elif location == enums.Location.MY_PLAYLISTS or location == enums.Location.PENDING_TAB:
                tmpEntry = self.replaceInLocator(self.clsCommon.myPlaylists.PLAYLIST_ENTRY_NAME_IN_PLAYLIST, "ENTRY_NAME", entryName)
                
            entrytop = self.get_element_attributes(tmpEntry, multipleElements=True)['top']
            writeToLog("INFO","The top of: '" + entryName + "' is: " + str(entrytop))
            return entrytop
        
        except NoSuchElementException:          
            writeToLog("INFO","The top of: '" + entryName + "' could not be located")
            return False
    
    
    # Author: Tzachi Guetta 
    def verifyEntriesOrder(self, expectedEntriesOrder, location = enums.Location.MY_MEDIA):
        try:         
            if location == enums.Location.MY_MEDIA:
                if self.clsCommon.myMedia.navigateToMyMedia() == False:
                    return False
            
                if self.scrollToBottom() == False:
                    writeToLog("INFO","FAILED to scroll to bottom in my-media")
                    return False
                
            elif location == enums.Location.MY_PLAYLISTS: 
                if self.clsCommon.myPlaylists.navigateToMyPlaylists(True) == False:
                    return False
                
            tmpTop = -9999
            for entry in expectedEntriesOrder:
                currentEntryTop = self.getTop(entry, location)
                if currentEntryTop != False and currentEntryTop!= 0:
                    if currentEntryTop <= tmpTop:
                        writeToLog("INFO","FAILED, the location of: '" + entry + "' is not as expected. (the top is '" + str(currentEntryTop) + "' and it should be higher than: '" + str(tmpTop) + "')")
                        return False
                else:
                    return False
                tmpTop = currentEntryTop
                
        except NoSuchElementException:
            return False
    
        return True
    
    
    # Author: Tzachi Guetta 
    def isEntryPresented(self, entryName, isExpected):
        try:         
            tmpEntry = self.replaceInLocator(self.MY_MEDIA_ENTRY_TOP, "ENTRY_NAME", entryName)
            isPresented = self.is_present(tmpEntry, 5)
            
            strPresented = "Not Presented" 
            if isPresented == True:
                strPresented = "Presented"

            if isPresented == isExpected:
                writeToLog("INFO","Passed, As expected, Entry: '" + entryName + "' is " + strPresented)
                return True
            else:
                writeToLog("INFO","FAILED, Not expected, Entry: '" + entryName + "' is " + strPresented)
                return False          
                
        except NoSuchElementException:
            return False
    
        return True
    
    # Author: Tzachi Guetta 
    def areEntriesPresented(self, entriesDict):
        try:
            for entry in entriesDict:
                if self.isEntryPresented(entry, entriesDict.get(entry)) == False:
                    writeToLog("INFO","FAILED to verify if entry presented for entry: " + str(entry))  
                    return False
                
        except NoSuchElementException:
            return False
    
        return True
    
    # @Author: Inbar Willman
    def publishSingleEntryToUnlistedOrPrivate(self, entryName, privacy, alreadyPublished=False, publishFrom=enums.Location.MY_MEDIA): 
        if publishFrom == enums.Location.MY_MEDIA:
            if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
                writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
                return False
        
            if self.clickActionsAndPublishFromMyMedia() == False:
                writeToLog("INFO","FAILED to click on Action button, Entry: '" + entryName + "' something went wrong")
                return False
            sleep(3)
            
            if privacy == enums.ChannelPrivacyType.UNLISTED:
                    if self.click(self.MY_MEDIA_PUBLISH_UNLISTED) == False:
                        writeToLog("INFO","FAILED to click on Unlisted button")
                        return False 
                    
                    if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON) == False:
                        writeToLog("INFO","FAILED to click on Unlisted button")
                        return False                        
                    
                    if alreadyPublished == True:
                        #Click on confirm modal
                        if self.click(self.MY_MEDIA_CONFIRM_CHANGING_STATUS) == False:
                            writeToLog("INFO","FAILED to click on confirm button")
                            return False 
                    
                    sleep(1)
                    self.clsCommon.general.waitForLoaderToDisappear()
        
                    if self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG, 20) == False:
                        writeToLog("INFO","FAILED to Publish Entry: '" + entryName + "' something went wrong")
                        return False    

            elif privacy == enums.ChannelPrivacyType.PRIVATE:
                    if self.click(self.MY_MEDIA_PUBLISH_PRIVATE) == False:
                        writeToLog("INFO","FAILED to click on Unlisted button")
                        return False 
                    
                    if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON) == False:
                        writeToLog("INFO","FAILED to click on Unlisted button")
                        return False                        
                    
                    if alreadyPublished == True:                   
                        #Click on confirm modal
                        if self.click(self.MY_MEDIA_CONFIRM_CHANGING_STATUS) == False:
                            writeToLog("INFO","FAILED to click on confirm button")
                            return False 
                    
                    sleep(1)
                    self.clsCommon.general.waitForLoaderToDisappear()
        
                    if self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_AS_PRIVATE_MSG, 20) == False:
                        writeToLog("INFO","FAILED to Publish Entry: '" + entryName + "' something went wrong")
                        return False                                       
        
            else:
                writeToLog("INFO","FAILED to get valid privacy:" + str(privacy))
                return False
        
        elif publishFrom == enums.Location.UPLOAD_PAGE: 
            writeToLog("INFO","Publishing from Upload page, Entry name: '" + entryName + "'")       
            sleep(2)            
            if self.click(self.MY_MEDIA_PUBLISH_UNLISTED) == False:
                writeToLog("INFO","FAILED to click on Unlisted button")
                return False    
            
            if self.click(self.clsCommon.upload.UPLOAD_ENTRY_SAVE_BUTTON) == False:
                writeToLog("DEBUG","FAILED to click on 'Save' button")
                return None
            
            sleep(2)
            # Wait for loader to disappear
            self.clsCommon.general.waitForLoaderToDisappear()            
        
            if self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG, 20) == False:
                writeToLog("INFO","FAILED to Publish Entry: '" + entryName + "' something went wrong")
                return False                                       
            
        return True