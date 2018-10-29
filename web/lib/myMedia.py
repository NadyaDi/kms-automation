from base import *
import clsTestService
from general import General
from logger import writeToLog
from editEntryPage import EditEntryPage
import enums
from selenium.webdriver.common.keys import Keys
import re



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
    MY_MEDIA_SEARCH_BAR_OLD_UI                                  = ('id', 'searchBar')
    MY_MEDIA_ELASTIC_SEARCH_BAR                                 = ('xpath', "//input[@class='searchForm__text']")
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
    #MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI                         = ('xpath', "//a[@id ='accordion-ENTRY_ID']")
    MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI                         = ('xpath', "//div[@id ='accordion_ENTRY_ID']")
    MY_MEDIA_ENTRY_PUBLISHED_BTN                                = ('xpath', "//a[@id ='accordion-ENTRY_ID']/i[@class='icon-plus-sign kmstooltip']")
    MY_MEDIA_ENTRY_CHILD_POPUP                                  = ('xpath', "//strong[@class='valign-top']")
    MY_MEDIA_SORT_BY_DROPDOWNLIST_OLD_UI                        = ('xpath', "//a[@id='sort-btn']")
    MY_MEDIA_SORT_BY_DROPDOWNLIST_NEW_UI                        = ('xpath', "//a[@id='sortBy-menu-toggle']")
    MY_MEDIA_FILTER_BY_STATUS_DROPDOWNLIST                      = ('xpath', "//a[@id='status-btn']")
    MY_MEDIA_FILTER_BY_TYPE_DROPDOWNLIST                        = ('xpath', "//a[@id='type-btn']")
    MY_MEDIA_FILTER_BY_COLLABORATION_DROPDOWNLIST               = ('xpath', "//a[@id='mediaCollaboration-btn']")
    MY_MEDIA_FILTER_BY_SCHEDULING_DROPDOWNLIST                  = ('xpath', "//a[@id='sched-btn']")
    MY_MEDIA_DROPDOWNLIST_ITEM_OLD_UI                           = ('xpath', "//a[@role='menuitem' and contains(text(), 'DROPDOWNLIST_ITEM')]")
    MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI                           = ('xpath', "//span[@class='filter-checkbox__label' and contains(text(), 'DROPDOWNLIST_ITEM')]")
    MY_MEDIA_ENTRY_TOP                                          = ('xpath', "//span[@class='entry-name' and text()='ENTRY_NAME']")
    MY_MEDIA_END_OF_PAGE                                        = ('xpath', "//div[@class='alert alert-info endlessScrollAlert']")
    MY_MEDIA_TABLE_SIZE                                         = ('xpath', "//table[@class='table table-condensed table-hover bulkCheckbox mymediaTable mediaTable full']/tbody/tr")
    MY_MEDIA_CONFIRM_CHANGING_STATUS                            = ('xpath', "//a[@class='btn btn-primary' and text()='OK']")
    MY_MEDIA_ENTRY_THUMBNAIL                                    = ('xpath', "//img[@class='thumb_img' and @alt='Thumbnail for entry ENTRY_NAME']")
    MY_MEDIA_ENTRY_THUMBNAIL_ELASTIC_SEARCH                     = ("xpath", "//img[@class='entryThumbnail__img']")
    MY_MEDIA_REMOVE_SEARCH_ICON_OLD_UI                          = ('xpath', "//i[@class='icon-remove']")
    MY_MEDIA_REMOVE_SEARCH_ICON_NEW_UI                          = ('xpath', "//a[@class='clear searchForm_icon']")
    MY_MEDIA_NO_ENTRIES_FOUND                                   = ('xpath',"//div[@class='alert alert-info no-results' and contains(text(), 'No Entries Found')]")
    MY_MEDIA_TABLE                                              = ('xpath', "//table[@class='table table-condensed table-hover bulkCheckbox mymediaTable mediaTable full']")
    MY_MEDIA_IMAGE_ICON                                         = ('xpath', "//i[@class='icon-picture icon-white']")
    MY_MEDIA_AUDIO_ICON                                         = ('xpath', "//i[@class='icon-music icon-white']")
    MY_MEDIA_QUIZ_ICON                                          = ('xpath', "//i[@class='icomoon-quiz icon-white']")
    MY_MEDIA_VIDEO_ICON_OLD_UI                                  = ('xpath', "//i[@class='icon-film icon-white']")
    MY_MEDIA_EXPEND_MEDIA_DETAILS                               = ('xpath', "//div[@class='accordion-body in collapse contentLoaded' and @id='collapse_ENTRY_ID']")
    MY_MEDIA_COLLAPSED_VIEW_BUTTON                              = ('xpath', "//button[@id='MyMediaList' and @data-original-title='Collapsed view']")
    MY_MEDIA_DETAILED_VIEW_BUTTON                               = ('xpath', "//button[@id='MyMediaThumbs' and @data-original-title='Detailed view']")
    SEARCH_RESULTS_ENTRY_NAME                                   = ('xpath', "//span[@class='results-entry__name']")
    MY_MEDIA_FILTERS_BUTTON_NEW_UI                              = ('xpath', "//button[contains(@class,'toggleButton btn shrink-container__button hidden-phone') and text()='Filters']")
    SEARCH_RESULTS_ENTRY_NAME_OLD_UI                            = ('xpath', '//span[@class="searchTerm" and text()="ENTRY_NAME"]')
    EDIT_BUTTON_REQUIRED_FIELD_MASSAGE                          = ('xpath', '//a[@class="hidden-phone" and text()="Edit"]')
    CUSTOM_FIELD                                                = ('xpath', '//input[@id="customdata-DepartmentName"]')
    CUSTOM_FIELD_DROP_DOWN                                      = ('xpath', '//select[@id="customdata-DepartmentDivision"]')
    SET_DATE_FROM_CALENDAR                                      = ('xpath', "//input[@id='customdata-DateEstablished']")
    EDIT_ENTRY_CUSTOM_DATA_CALENDAR_DAY                         = ('xpath', "//td[@class='today day']")
    CLICK_ON_CALENDAR                                           = ('xpath', "//i[@class='icon-th']")
    CLICK_ON_CALENDAR_DATE_ESTABLISHED                          = ('xpath', "//div[@class='input-append date datepicker']") 
    #=============================================================================================================
    def getSearchBarElement(self):
        try:
            # Check which search bar do we have: old or new (elastic)
            if self.clsCommon.isElasticSearchOnPage():
                if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
                    return self.get_element(self.MY_MEDIA_ELASTIC_SEARCH_BAR)
                else:
                    return self.get_elements(self.MY_MEDIA_ELASTIC_SEARCH_BAR)[1]
            else:
                return self.wait_visible(self.MY_MEDIA_SEARCH_BAR, 30, True)
        except:
            writeToLog("INFO","FAILED get Search Bar element")
            return False        

    
    # This method, clicks on the menu and My Media
    def navigateToMyMedia(self, forceNavigate = False):
        application = localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST
        if application == enums.Application.BLACK_BOARD:
            if self.clsCommon.blackBoard.navigateToMyMediaBlackBoard() == False:
                writeToLog("INFO","FAILED navigate to my media in blackboard")
                return False
        
        else:    
            # Check if we are already in my media page
            if forceNavigate == False:
                if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 5) == True:
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
        sleep(5)
        
        # Click on confirm delete
        if self.click(self.MY_MEDIA_CONFIRM_ENTRY_DELETE, multipleElements=True) == False:
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
    def deleteEntriesFromMyMedia(self, entriesNames, showAllEntries=False):
        if self.navigateToMyMedia(forceNavigate = True) == False:
            writeToLog("INFO","FAILED Navigate to my media page")
            return False
        
        success = True
        # Checking if entriesNames list type
        if type(entriesNames) is list:
            if showAllEntries == True:
                if self.showAllEntries() == False:
                    return False                
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
     
        
    def searchEntryMyMedia(self, entryName, forceNavigate=True, exactSearch=False):
        # Check if my media page is already open
        # Navigate to My Media
        if self.navigateToMyMedia(forceNavigate) == False:
            return False
        
        sleep(5)
        # Search Entry     
        searchBarElement = self.getSearchBarElement()
        if searchBarElement == False:
            writeToLog("INFO","FAILED to get search bar element")
            return False
        searchBarElement.click()
        if exactSearch == True:
            searchLine = '"' + entryName + '"'
        else:
            if self.clsCommon.isElasticSearchOnPage():
                searchLine = '"' + entryName + '"'
            else:
                searchLine = entryName
            
        self.getSearchBarElement().send_keys(searchLine + Keys.ENTER)
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
        
           
    def clickEntryAfterSearchInMyMedia(self, entryName):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if self.click(('xpath', "//span[@class='entry-name' and text()='" + entryName + "']"), 10) == False:            
                writeToLog("INFO","FAILED to click on Entry: '" + entryName + "'")
                return False
        else:    
            result = self.getResultAfterSearch(entryName)
            if result == False:
                return False

            if self.clickElement(result) == False:
                writeToLog("INFO","FAILED to click on Entry: '" + entryName + "'")
                return False
        return True
    
    
    # This method for Elastic Search (new UI), returns the result element.         
    def getResultAfterSearch(self, searchString):
        #If we are in new UI with Elastic search
        if self.clsCommon.isElasticSearchOnPage() == True:
            results = self.wait_elements(self.SEARCH_RESULTS_ENTRY_NAME, 30)
        
        #If we are in old UI
        else:
            tmp_results = (self.SEARCH_RESULTS_ENTRY_NAME_OLD_UI[0], self.SEARCH_RESULTS_ENTRY_NAME_OLD_UI[1].replace('ENTRY_NAME', searchString))
            results = self.wait_elements(tmp_results, 30) 
            
        if results == False:
                writeToLog("INFO","No entries found")
                return False        
        
        for result in results:
            if result.text == searchString:
                return result        
    
        writeToLog("INFO","No entries found after search entry: '" + searchString + "'") 
        return False        
        
        
    # This method for Elastic Search (new UI), clicks on the returned result element.         
    def clickResultEntryAfterSearch(self, entryName):
        result = self.getResultAfterSearch(entryName)
        if result == False:
            writeToLog("INFO","FAILED to click on Entry: '" + entryName + "'")
            return False
        else:
            if self.clickElement(result) == False:
                writeToLog("INFO","FAILED to click on Entry: '" + entryName + "'")
                return False
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
        sleep(5)
        
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
        
        if self.click(self.MY_MEDIA_PUBLISH_UNLISTED, 30) == False:
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
        
        writeToLog("INFO","Success, Entry '" + entryName + "' was set to unlisted successfully")
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
            
            if self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 45) == False:
                writeToLog("DEBUG","FAILED to click on publish button")
                return False      

        elif publishFrom == enums.Location.UPLOAD_PAGE: 
            writeToLog("INFO","Publishing from Upload page, Entry name: '" + entryName + "'")       
            sleep(2)
            # When the radio is disabled, it still clickable, self.click() wont return false
            # The solution is to check button attribute "disabled" == "disabled"
            if self.wait_visible(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 45).get_attribute("disabled") == 'true':
                writeToLog("DEBUG","FAILED to click on publish button - button is disabled")
                return False
            
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
   
                if self.click(tmpChannelName, 20, multipleElements=True) == False:
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
        writeToLog("INFO","Success, publish entry '" + entryName + "' was successful")
        return True
    
    
    # Author: Tzachi Guetta 
    def verifyEntryPrivacyInMyMedia(self, entryName, expectedEntryPrivacy, forceNavigate=True):
        try:    
            if forceNavigate == True:           
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
                else:
                    tmpBtn = (self.MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI[0], self.MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI[1].replace('ENTRY_ID', entryId) + "/descendant::strong[@class='valign-top']")
                if str(expectedEntryPrivacy) in self.get_element_text(tmpBtn):
                    writeToLog("INFO","As Expected: The privacy of: '" + entryName + "' in My-media page is: '" + str(expectedEntryPrivacy) + "'")
                    return True                    
                    
        except NoSuchElementException:
            writeToLog("INFO","FAILED to verify that entry '" + entryName + "' label is " + expectedEntryPrivacy.value) 
            return False
    
        
    # Author: Michal Zomper  
    def verifyEntriesPrivacyInMyMedia(self, entriesList):
        for entry in entriesList:
            if self.verifyEntryPrivacyInMyMedia(entry, entriesList[entry], forceNavigate=False) == False:
                writeToLog("INFO","FAILED to verify entry '" + entry + "' label")
                return False
                
        writeToLog("INFO","Success, All entries label were verified")
        return True 


    # Author: Tzachi Guetta 
    def SortAndFilter(self, dropDownListName='' ,dropDownListItem=''):
        if self.clsCommon.isElasticSearchOnPage() == True:
            if dropDownListName == enums.SortAndFilter.SORT_BY:
                tmpSortlocator = self.MY_MEDIA_SORT_BY_DROPDOWNLIST_NEW_UI
                if self.click(tmpSortlocator, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on :" + dropDownListItem.value + " filter in my media")
                    return False
                
                # only sort filter use the locater of the dropdownlist_item_old_ui
                tmpSortBy = (self.MY_MEDIA_DROPDOWNLIST_ITEM_OLD_UI[0], self.MY_MEDIA_DROPDOWNLIST_ITEM_OLD_UI[1].replace('DROPDOWNLIST_ITEM', dropDownListItem.value))
                if self.click(tmpSortBy, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on sort by  :" + dropDownListItem.value + " filter in my media")
                    return False
            else:
                if self.click(self.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on filters button in my media")
                    return False
                sleep(2)
                
                tmpEntry = (self.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[0], self.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[1].replace('DROPDOWNLIST_ITEM', dropDownListItem.value)) 
                if self.click(tmpEntry, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on the drop-down list item: " + dropDownListItem.value)
                    return False
                
            self.clsCommon.general.waitForLoaderToDisappear()   
            writeToLog("INFO","Success, Sort was set successfully")
            return True
        else:
            if dropDownListName == enums.SortAndFilter.SORT_BY:
                tmplocator = self.MY_MEDIA_SORT_BY_DROPDOWNLIST_OLD_UI
            
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
            
            tmpEntry = self.replaceInLocator(self.MY_MEDIA_DROPDOWNLIST_ITEM_OLD_UI, "DROPDOWNLIST_ITEM", str(dropDownListItem)) 
            if self.click(tmpEntry, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on the drop-down list item: " + str(dropDownListItem))
                return False

        self.clsCommon.general.waitForLoaderToDisappear()    
        writeToLog("INFO","Success, sort by " + dropDownListName.value + " - " + str(dropDownListItem) + " was set successfully")
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
    
    # @Author: Michal Zomper   
    def navigateToEntryPageFromMyMediaViaThubnail(self, entryName):    
        tmp_entry_name = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True                 
        
        if self.clsCommon.myMedia.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILD to search entry name: '" + entryName + "' in my media")
            return False 
        
        if self.clsCommon.isElasticSearchOnPage() == False:
            tmp_entryThumbnail = (self.MY_MEDIA_ENTRY_THUMBNAIL[0], self.MY_MEDIA_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName))
            if self.click(tmp_entryThumbnail, 20) == False:
                writeToLog("INFO","FAILED to click on entry thumbnail: " + entryName)
                return False
        else:
            if self.click(self.MY_MEDIA_ENTRY_THUMBNAIL_ELASTIC_SEARCH, 20) == False:
                writeToLog("INFO","FAILED to click on entry thumbnail: " + entryName)
                return False
                            
        if self.wait_visible(tmp_entry_name, 30) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
        
        sleep(2)
        writeToLog("INFO","Success, entry was open successfully")
        return True
       
   
    # @Author: Michal Zomper
    def verifyEntriesExistInMyMedia(self, searchKey, entriesList, entriesCount):
        if self.searchEntryMyMedia(searchKey) == False:
            writeToLog("INFO","FAILED to search entry: '" + searchKey + "' in my media")
            return False 
        
        try: 
            searchedEntries = self.get_elements(self.MY_MEDIA_TABLE_SIZE)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list")
            return False
        
        # Check that number of entries that display is correct 
        if len(searchedEntries) != entriesCount:
            writeToLog("INFO","FAILED, number of entries after search is '" + str(len(self.get_elements(self.MY_MEDIA_TABLE_SIZE))) + "' but need to be '" + str(entriesCount) + "'")
            return False 
            
        if self.clsCommon.isElasticSearchOnPage() == False:
            if type(entriesList) is list:
                i=1 
                for entry in entriesList: 
                    if (entry in searchedEntries[len(searchedEntries)-i].text) == False:
                        writeToLog("INFO","FAILED to find entry: '" + entry + "'  after search in my media") 
                        return False
                    i = i+1
            # only one entry 
            else:
                if (entriesList in searchedEntries[0].text) == False:
                    writeToLog("INFO","FAILED to find entry: '" + entriesList + "' after search in my media")
                    return False
        else:
            if type(entriesList) is list:
                for entry in entriesList: 
                    if (self.getResultAfterSearch(entry)) == False:
                        writeToLog("INFO","FAILED to find entry: '" + entry + "'  after search in my media") 
                        return False
            # only one entry 
            else:
                if (self.getResultAfterSearch(entriesList)) == False:
                    writeToLog("INFO","FAILED to find entry: '" + entriesList + "' after search in my media")
                    return False
                
        if self.clearSearch() == False:
            writeToLog("INFO","FAILED to clear search textbox")
            return False
            
        sleep(1)
        writeToLog("INFO","Success, All searched entries were found after search")
        return True  
        
        
    # Author: Michal Zomper 
    def clearSearch(self):
        if self.clsCommon.isElasticSearchOnPage() == True:
            try:
                clear_button = self.get_elements(self.MY_MEDIA_REMOVE_SEARCH_ICON_NEW_UI)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find clear search icon")
                return False
            
            if self.clickElement(clear_button[1]) == False:
                writeToLog("INFO","FAILED click on the remove search icon")
                return False
        else:
            if self.click(self.MY_MEDIA_REMOVE_SEARCH_ICON_OLD_UI, 15, multipleElements=True) == False:
                writeToLog("INFO","FAILED click on the remove search icon")
                return False
        self.clsCommon.general.waitForLoaderToDisappear()
             
        writeToLog("INFO","Success, search was clear from search textbox")
        return True
    
    
    #  @Author: Michal Zomper      
    # The following method can handle list of entries and a single entry:
    #    in order to publish list of entries pass a List[] of entries name, for single entry - just pass the entry name
    #    also: the method will navigate to My media
    #    in categoryList / channelList will have all the names of the categories / channels to publish to
    # Known limitation: entries MUST be presented on the first page of my media
    def publishEntriesFromMyMedia(self, entriesName, categoryList, channelList='', disclaimer=False, showAllEntries=False):
        if self.navigateToMyMedia(forceNavigate = True) == False:
            writeToLog("INFO","FAILED Navigate to my media page")
            return False
        
        if showAllEntries == True:
            if self.showAllEntries() == False:
                return False     
        
        # Checking if entriesNames list type
        if type(entriesName) is list:
            if disclaimer == True:
                for entryName in entriesName: 
                    sleep(2)
                    if self.handleDisclaimerBeforePublish(entryName) == False:
                        writeToLog("INFO","FAILED, Handle disclaimer before Publish failed for entry:" + entryName)
                        return False
                    
            for entryName in entriesName: 
                if self.checkSingleEntryInMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to CHECK the entry in my-media page")
                    return False
        else:
            if disclaimer == True:
                if self.handleDisclaimerBeforePublish(entriesName) == False:
                    writeToLog("INFO","FAILED, Handle disclaimer before Publish failed")
                    return False 
                
            if self.checkSingleEntryInMyMedia(entriesName) == False:
                writeToLog("INFO","FAILED to CHECK the entry in my-media page")
                return False
                
        if self.clickActionsAndPublishFromMyMedia() == False:
            writeToLog("INFO","FAILED to click on action button")
            return False
        
        sleep(10)
        
        if self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 40, True) == False:
            writeToLog("INFO","FAILED to click on publish button")
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
   
                if self.click(tmpChannelName, 20, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to select published channel '" + channel + "'")
                    return False
        
        sleep(1) 
        if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False                
                
        if self.wait_visible(self.MY_MEDIA_SAVE_MESSAGE_CONFIRM, 45) == False:
            writeToLog("INFO","FAILED to find confirm save message")
            return False
        
        sleep(3)       
        if type(entriesName) is list: 
            entries = ", ".join(entriesName)
            writeToLog("INFO","Success, The entries '" + entries + "' were published successfully")
        else:
            writeToLog("INFO","Success, The entry '" + entriesName + "' was publish  successfully")
        return True
                
                     
    #  @Author: Oded berihon                 
    def addCustomDataAndPublish(self, entryName, customfield, customFieldDropdwon=enums.DepartmentDivision.FINANCE):  
        if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False
        
        if self.clickActionsAndPublishFromMyMedia() == False:
            writeToLog("INFO","FAILED to click on Action button, Entry: '" + entryName + "' something went wrong")
            return False
        
        if self.wait_visible(self.MY_MEDIA_DISCLAIMER_MSG) == False:
            writeToLog("INFO","FAILED, Disclaimer alert (before publish) wasn't presented although Disclaimer module is turned on")
            return False  
        
        if self.click(self.EDIT_BUTTON_REQUIRED_FIELD_MASSAGE) == False:
            writeToLog("INFO","FAILED to click on edit button")
            return False  

        if self.send_keys(self.CUSTOM_FIELD, customfield) == False:
            writeToLog("INFO","FAILED to fill a customfield:'" + customfield + "'")
            return False
                      
        if customFieldDropdwon == enums.DepartmentDivision.FINANCE:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'FInance') == False:
                writeToLog("INFO","Failed select finance devision")
                return False 
        
        elif customFieldDropdwon == enums.DepartmentDivision.MARKETING:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Marketing') == False:
                writeToLog("INFO","Failed select finance devision")
                return False 
            
        elif customFieldDropdwon == enums.DepartmentDivision.PRODUCT:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Product') == False:
                writeToLog("INFO","Failed select finance devision")
                return False    
            
        elif customFieldDropdwon == enums.DepartmentDivision.ENGINEERING:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Engineering') == False:
                writeToLog("INFO","Failed select finance devision")
                return False    
            
        elif customFieldDropdwon == enums.DepartmentDivision.SALES:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Sales') == False:
                writeToLog("INFO","Failed select finance devision")
                return False  
            
        elif customFieldDropdwon == enums.DepartmentDivision.HR:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'HR') == False:
                writeToLog("INFO","Failed select finance devision")
                return False 
            
        elif customFieldDropdwon == enums.DepartmentDivision.MANAGMENT:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Management') == False:
                writeToLog("INFO","Failed select finance devision")
                return False        
        
        parentElement = self.wait_visible(self.CLICK_ON_CALENDAR_DATE_ESTABLISHED)        
        self.get_child_element(parentElement, self.CLICK_ON_CALENDAR).click()             
        
        if self.click(self.EDIT_ENTRY_CUSTOM_DATA_CALENDAR_DAY) == False:                  
            writeToLog("INFO","Failed select finance devision")
            return False         
        
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SAVE_BUTTON, 15) == False:
            writeToLog("INFO","FAILED to click on Edit button")
            return False    
        
        return True 
        
   
    #  @Author: Michal Zomper    
    # The function check and verify that the entries sort in my media are in the correct order 
    def verifySortInMyMedia(self, sortBy, entriesList):
        if self.clsCommon.isElasticSearchOnPage() == True:
            sortBy = sortBy.value
            
        if self.SortAndFilter(enums.SortAndFilter.SORT_BY,sortBy) == False:
            writeToLog("INFO","FAILED to sort entries")
            return False
                
        if self.showAllEntries() == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False
        sleep(10)
        
        try:
            entriesInMyMedia = self.wait_visible(self.MY_MEDIA_TABLE).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in galley")
            return False
        entriesInMyMedia = entriesInMyMedia.split("\n")
        
        if self.verifySortOrder(entriesList, entriesInMyMedia) == False:
            writeToLog("INFO","FAILED ,sort by '" + sortBy + "' isn't correct")
            return False
        
        if self.clsCommon.isElasticSearchOnPage() == True:
            writeToLog("INFO","Success, My media sort by '" + sortBy + "' was successful")
            return True
        else:
            writeToLog("INFO","Success, My media sort by '" + sortBy.value + "' was successful")
            return True

    
    # @Author: Michal Zomper
    # The function is checking that the sort order is correct
    # entriesOrderAfterSor is the parameter of all the text in the sort page
    def verifySortOrder(self, entriesList, entriesOrderAfterSort):
        prevEntryIndex = -1
         
        if self.clsCommon.isElasticSearchOnPage() == True:
            for entry in entriesList:
                try:
                    currentEntryIndex = entriesOrderAfterSort.index(entry.lower())
                except:
                    writeToLog("INFO","FAILED , entry '" + entry + "' was not found" )
                    return False  
          
                #if prevEntryIndex > currentEntryIndex:       
                if (prevEntryIndex < currentEntryIndex) == False:
                    #writeToLog("INFO","FAILED ,sort by '" + sortBy + "' isn't correct. entry '" + entry + "' isn't in the right place" )
                    writeToLog("INFO","FAILED , entry '" + entry + "' isn't in the right place")
                    return False
                prevEntryIndex = currentEntryIndex
            #writeToLog("INFO","Success, My media sort by '" + sortBy + "' was successful")         
            writeToLog("INFO","Success, entries sort was successful")
            return True   
        else:
            for entry in entriesList:
                currentEntryIndex = entriesOrderAfterSort.index(entry.lower())
                #if prevEntryIndex > currentEntryIndex:
                if (prevEntryIndex < currentEntryIndex) == False:
                    #writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct. entry '" + entry + "' isn't in the right place" )
                    writeToLog("INFO","FAILED , entry '" + entry + "' isn't in the right place")
                    return False
                prevEntryIndex = currentEntryIndex
                
            #writeToLog("INFO","Success, My media sort by '" + sortBy.value + "' was successful")
            writeToLog("INFO","Success, entries sort  was successful")
            return True
        
    
    def showAllEntries(self, searchIn = enums.Location.MY_MEDIA, timeOut=60, afterSearch=False):
        # Check if we are in My Media page  
        if searchIn == enums.Location.MY_MEDIA:
            tmp_table_size = self.MY_MEDIA_TABLE_SIZE
            no_entries_page_msg = self.MY_MEDIA_NO_RESULTS_ALERT
        
        # Check if we are in category page    
        elif searchIn == enums.Location.CATEGORY_PAGE:
            if self.clsCommon.isElasticSearchOnPage() == True:
                if afterSearch == False:
                    tmp_table_size = self.clsCommon.category.CATEGORY_TABLE_SIZE_NEW_UI
                    no_entries_page_msg = self.clsCommon.category.CATEGORY_NO_MORE_MEDIA_ITEMS_MSG                    
                else:
                    tmp_table_size = self.clsCommon.category.CATEGORY_TABLE_SIZE_AFTER_SEARCH
                    no_entries_page_msg = self.clsCommon.category.CATEGORY_NO_MORE_MEDIA_FOUND_NEW_UI_MSG 
            else:#TODO OLD UI
                if afterSearch == False:
                    tmp_table_size = self.clsCommon.category.CATEGORY_TABLE_SIZE
                    no_entries_page_msg = self.clsCommon.category.CATEGORY_NO_MORE_MEDIA_FOUND_MSG                    
                else:
                    tmp_table_size = self.clsCommon.category.CATEGORY_TABLE_SIZE
                    no_entries_page_msg = self.clsCommon.category.CATEGORY_NO_MORE_MEDIA_FOUND_MSG                 
                
        elif searchIn == enums.Location.MY_HISTORY: 
            tmp_table_size = self.clsCommon.myHistory.MY_HISTORY_TABLE_SIZE
            no_entries_page_msg = self.clsCommon.myHistory.MY_HISTORY_NO_MORE_RESULTS_ALERT   
            
        elif searchIn == enums.Location.ADD_TO_CHANNEL_MY_MEDIA:    
            tmp_table_size = self.clsCommon.channel.ADD_TO_CHANNEL_MY_MEDIA_TABLE_SIZE
            no_entries_page_msg = self.clsCommon.channel.ADD_TO_CHANNEL_MY_MEDIA_NO_MORE_MEDIA_FOUND_MSG
            
        elif searchIn == enums.Location.ADD_TO_CHANNEL_SR:
            tmp_table_size = self.clsCommon.channel.ADD_TO_CHANNEL_MY_MEDIA_TABLE_SIZE
            no_entries_page_msg = self.clsCommon.channel.ADD_TO_CHANNEL_SR_NO_MORE_MEDIA_FOUND_MSG
            
        elif searchIn == enums.Location.EDITOR_PAGE:
            tmp_table_size = self.clsCommon.kea.EDITOR_TABLE_SIZE
            no_entries_page_msg = self.clsCommon.kea.EDITOR_NO_MORE_MEDIA_FOUND_MSG                          
                
        else:
            writeToLog("INFO","Failed to get valid location page")
            return False
         
        if len(self.get_elements(tmp_table_size)) < 5:
                writeToLog("INFO","Success, All media is display")
                return True 
              
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)  
        while wait_until > datetime.datetime.now():                       
            if self.is_present(no_entries_page_msg, 2) == True:
                writeToLog("INFO","Success, All media is display")
                sleep(1)
                # go back to the top of the page
                self.clsCommon.sendKeysToBodyElement(Keys.HOME)
                return True 
             
            self.clsCommon.sendKeysToBodyElement(Keys.END)
             
        writeToLog("INFO","FAILED to show all media")
        return False  
     
    
    #  @Author: Michal Zomper    
    # The function check the the entries in my media are filter correctly
    def verifyFiltersInMyMedia(self, entriesDict):
        if self.showAllEntries() == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False
             
        try:
            entriesInMyMedia = self.get_element(self.MY_MEDIA_TABLE).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in galley")
            return False
         
        for entry in entriesDict:
            #if entry[1] == True:
            if entriesDict[entry] == True:
                #if entry[0].lower() in entriesInMyMedia == False:
                if (entry.lower() in entriesInMyMedia) == False:
                    writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in my media although he need to be found")
                    return False
                 
            #elif entry[1] == False:
            if entriesDict[entry] == False:
                # if entry[0].lower() in entriesInMyMedia == True:
                if (entry.lower() in entriesInMyMedia) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in my media although he doesn't need to be found")
                    return False
                 
        writeToLog("INFO","Success, Only the correct media display in my media")
        return True
    
    
    #@Author: Michal Zomper 
    # The function going over the entries list and check that the entries icon that display on the thumbnail are  match the 'entryType' parameter
    def verifyEntryTypeIcon(self, entriesList, entryType):
        for entry in entriesList:
            tmpEntry = (self.MY_MEDIA_ENTRY_THUMBNAIL[0], self.MY_MEDIA_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entry))
            try:
                entryThumbnail = self.get_element(tmpEntry)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find entry '" + entry + "' element")
                return False

            if entryType == enums.MediaType.IMAGE:
                try: 
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_IMAGE_ICON)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Image icon")
                    return False
                 
            if entryType == enums.MediaType.AUDIO:
                try:
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_AUDIO_ICON)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Audio icon")
                    return False
                
            if entryType == enums.MediaType.QUIZ:
                try:
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_QUIZ_ICON)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Quiz icon")
                    return False                
            
            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
                if entryType == enums.MediaType.VIDEO:
                    try:
                        self.get_child_element(entryThumbnail, self.MY_MEDIA_VIDEO_ICON_OLD_UI)
                    except NoSuchElementException:
                        writeToLog("INFO","FAILED to find entry '" + entry + "' Video icon")
                        return False
            
        if self.verifyFilterUniqueIconType(entryType) == False:
            writeToLog("INFO","FAILED entries from different types display although the filter set to " + entryType.value)
            return False
                
        writeToLog("INFO","Success, All entry '" + entry + "' " + entryType.value + "  icon was verify")
        return True       
    
    
    #@Author: Michal Zomper 
    # The function check that only the entries type with that match the 'iconType' parameter display in the list in my media
    def verifyFilterUniqueIconType(self, iconType):
        if self.showAllEntries() == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False
                  
        if iconType != enums.MediaType.IMAGE:
            if self.wait_elements(self.MY_MEDIA_IMAGE_ICON) != False:
                writeToLog("INFO","FAILED, Image icon display in the list although only " + iconType.value + "need to be display")
                return False
                
        if iconType != enums.MediaType.AUDIO:
            if self.wait_elements(self.MY_MEDIA_AUDIO_ICON) != False:
                writeToLog("INFO","FAILED, Audio icon display in the list although only " + iconType.value + "need to be display")
                return False
            
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:     
            if iconType != enums.MediaType.VIDEO:
                if self.wait_elements(self.MY_MEDIA_VIDEO_ICON_OLD_UI) != False:
                    writeToLog("INFO","FAILED, Video icon display in the list although only " + iconType.value + "need to be display")
                    return False
            
        writeToLog("INFO","Success, only " + iconType.value + " type entries display")
        return True   
    
    
    #@Author: Michal Zomper 
    def expendAndVerifyPublishedEntriesDetails(self, entryName, categoris, channels):
        if self.verifyEntryPrivacyInMyMedia(entryName, enums.EntryPrivacyType.PUBLISHED, forceNavigate=False) == False:
                writeToLog("INFO","FAILED to verify entry '" + entryName + "' privacy")
                return False
        
        if self.verifyPublishedInExpendEntryDeatails(entryName, categoris, len(categoris), channels, len(channels)) == False:
            writeToLog("INFO","FAILED to verify entry '" + entryName + "' published categories/channels")
            return False
                
        writeToLog("INFO","Success, Entry published details were verified successfully")
        return True  
                
                
    #@Author: Michal Zomper 
    # pre condition to this function : need to open the publish option (the '+' button) in order to see all the publish details
    # the function verifyEntryPrivacyInMyMedia have the option to open the details     
    def verifyPublishedInExpendEntryDeatails(self, entryName, categories="", categoryCount="",  channels="", channelCount=""):
        tmpEntry = self.replaceInLocator(self.MY_MEDIA_ENTRY_PARNET, "ENTRY_NAME", entryName) 
        entryId = self.clsCommon.upload.extractEntryID(tmpEntry)       
        detailsBody = (self.MY_MEDIA_EXPEND_MEDIA_DETAILS[0], self.MY_MEDIA_EXPEND_MEDIA_DETAILS[1].replace('ENTRY_ID', entryId))
        
        tmpDetails = self.get_element(detailsBody).text
        tmpDetails = tmpDetails.split("\n")
        
        if len(categories) > 0:
            # verify number of published categories
            if len(categories) == 1:
                if (str(categoryCount) + " Category:") in tmpDetails == False:
                    writeToLog("INFO","FAILED to verify entry '" + entryName + "' have " + str(categoryCount) + " categories")
                    return False
            else:
                if (str(categoryCount) + " Categories:") in tmpDetails == False:
                    writeToLog("INFO","FAILED to verify entry '" + entryName + "' have " + str(categoryCount) + " categories")
                    return False
                    
            # Verify categories names
            listOfCategories =""  
            for category in categories:
                listOfCategories = listOfCategories + category + " "
            listOfCategories = (listOfCategories.strip())
                
            if listOfCategories in tmpDetails == False:
                writeToLog("INFO","FAILED to find category '" + category + "' under the entry '" + entryName + "' published in option")
                return False
         
        if len(channels) > 0:
            # verify number of published categories
            if len(channels) == 1:
                if (str(channelCount) + " Channel:") in tmpDetails == False:
                    writeToLog("INFO","FAILED to verify entry '" + entryName + "' have " + str(channelCount) + " channels")
                    return False
            else:
                if (str(channelCount) + " Channels:") in tmpDetails == False:
                    writeToLog("INFO","FAILED to verify entry '" + entryName + "' have " + str(channelCount) + " channels")
                    return False
            
            # Verify channels names
            listOfChannels =""   
            for channel in channels:
                listOfChannels = listOfChannels + channel + " "
            listOfChannels = (listOfChannels.strip())
                
            if listOfChannels in tmpDetails == False:
                writeToLog("INFO","FAILED to find channel '" + channel + "' under the entry '" + entryName + "' published in option")
                return False
                 
        writeToLog("INFO","Success, All entry '" + entryName + "' categories/channels display under published in option")
        return True      
       
            
    #@Author: Michal Zomper 
    def verifyMyMediaView(self, entryName, view=enums.MyMediaView.DETAILED):
        tmpEntryCheckBox = (self.MY_MEDIA_ENTRY_CHECKBOX[0], self.MY_MEDIA_ENTRY_CHECKBOX[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmpEntryCheckBox) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' checkbox")
            return False
            
        tmpEntryName = (self.MY_MEDIA_ENTRY_TOP[0], self.MY_MEDIA_ENTRY_TOP[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmpEntryName) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' title")
            return False   
        
        tmpEntryEditButton = (self.MY_MEDIA_ENRTY_EDIT_BUTTON[0], self.MY_MEDIA_ENRTY_EDIT_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmpEntryEditButton) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' edit Button")
            return False  
        
        tmpEntryDeleteButton = (self.MY_MEDIA_ENRTY_DELETE_BUTTON[0], self.MY_MEDIA_ENRTY_DELETE_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmpEntryDeleteButton) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' delete button")
            return False  
        
        if view == enums.MyMediaView.DETAILED:
            tmpEntryThmbnail = (self.MY_MEDIA_ENTRY_THUMBNAIL[0], self.MY_MEDIA_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName))
            if self.is_visible(tmpEntryThmbnail) == False:
                writeToLog("INFO","FAILED to find entry '" + entryName + "' thumbnail")
                return False 
            
        writeToLog("INFO","Success, my media '" + view.value + " view' was verify for entry '" + entryName + "'")
        return True   
    
    
    #@Author: Michal Zomper 
    def verifyMyMediaViewForEntris(self, entrisList, viewType):
        # Checking if entriesNames list type
        if type(entrisList) is list:
            for entry in entrisList:
                if self.verifyMyMediaView(entry, viewType) == False:
                    writeToLog("INFO","FAILED to verify my media view '" + viewType.value + "' for entry" + entry + "'")
                    return False 
                    
        else:
            if self.verifyMyMediaView(entrisList) == False:
                writeToLog("INFO","FAILED to verify my media view '" + viewType.value + "' for entry" + entrisList + "'")
                return False 
            
        writeToLog("INFO","Success, my media '" + viewType.value + " view' was verified")
        return True     
            