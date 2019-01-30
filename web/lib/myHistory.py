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
    MY_HISTORY_ENTRY_DESCRIPTION                                  = ('xpath', "//a[@class='searchme']")
    MY_HISTORY_ENTRY_LAST_WATCHED                                 = ('xpath', "//a[@class='watch-time']")
    MY_HISTORY_ENTRY_VIEWD_IN                                     = ('xpath', "//a[contains(@href, 'channel/')")
    MY_HISTORY_ENTRY_PARNET                                       = ('xpath', "//span[@class='entry-name' and text() ='ENTRY_NAME']/ancestor::td[@class='dataTd entryDetails']") 
    MY_HISTORY_PROGRESS_BAR_STARTED                               = ('xpath', "//div[@class='progress history-progress started']")
    MY_HISTORY_PROGRESS_BAR_COMPLETE                              = ('xpath', "//div[@class='progress history-progress complete']")
    MY_HISTORY_PROGRESS_BAR_PRECENT                               = ('xpath', "//div[@class='bar' and contains(@style, 'width:')]")
    MY_HISTORY_NO_RESULTS_ALERT                                   = ('xpath', '//div[@class="alert alert-info no-results" and contains(text(), "No Entries Found")]')
    MY_HISTORY_DROP_DOWN_LIST_NAME                                = ('xpath', '//a[@class="dropdown-toggle responsiveSize" and @aria-controls="DROPDOWN_LIST_NAME"]')
    MY_HISTORY_DROP_DOWN_ITEM                                     = ('xpath' , '//a[@role="menuitem" and text()="MENU_ITEM"]')
    MY_HISTORY_TABLE                                              = ('xpath', '//table[@class="table table-condensed table-hover mediaTable myHistoryTable full"]')
    MY_HISTORY_NO_MORE_RESULTS_ALERT                              = ('xpath', "//div[@id='myHistory_scroller_alert' and contains(text(),'There are no more media items.')]")
    MY_HISTORY_TABLE_SIZE                                         = ('xpath', "//table[@class='table table-condensed table-hover mediaTable myHistoryTable full']/tbody/tr") 
    MY_HISTORY_REFRESH_BTN                                        = ('xpath', '//i[@class="icon-refresh"]')
    #=============================================================================================================
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
     
    
    # @Author: Inbar Willman    
    # This method search for entry in My history page   
    def searchEntryMyHistory(self, entryName):
        # Navigate to My Media
        if self.navigateToMyHistory(True) == False:
            return False
        
        # Check if search field is displayed 
        if self.isSearchFieldIsDisplayed() == False:
            return False
        
        #If search field is displayed make a search
        self.clsCommon.myMedia.getSearchBarElement().click()
        self.clsCommon.myMedia.getSearchBarElement().send_keys(entryName)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
     
    
    # @Author: Inbar Willman    
    # This method search if entry exists or not in My history page    
    def isEntryExistsInMyHistory(self, entryName, description='', timeout=30):  
        if description == '':
            if self.searchEntryMyHistory(entryName) == False:
                return False
        else:
            if self.searchEntryMyHistory(description) == False:
                return False
            
        tmpEntryName = (self.MY_HISTORY_RESULTS_ENTRY [0], self.MY_HISTORY_RESULTS_ENTRY [1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmpEntryName, timeout) == False: 
            return False
  
        return True
    
    
    # @Author: Inbar Willman
    def waitTillLocatorExistsInMyHistory(self, entryName, description='', timeout=30):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)   
        while wait_until > datetime.datetime.now(): 
            if self.isEntryExistsInMyHistory(entryName,description, 5):
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
        
        # Verify that correct message is displayed
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
        
    # @Author: Inbar Willman   
    # Check that all entry data is correct in My History
    def checkEntryDetailsInMyHistory(self, entryName, descripiton, tags, channelName):
        tmp_entry_parent = (self.MY_HISTORY_ENTRY_PARNET[0], self.MY_HISTORY_ENTRY_PARNET[1].replace('ENTRY_NAME', entryName))
        entry_text = self.get_element_text(tmp_entry_parent)
        entryMetadata = re.search(entryName + "\n" + descripiton + "\n" + tags, entry_text)
        # Check if entry details name, description and tags are displayed correctly
        if entryMetadata == False:
            writeToLog("INFO","FAILED to display correct entry details - Name, Description and tags")
            return False 
        
        # Check if entry was watched a moment ago
        entryWatchedTimeMomentList = re.findall("(Watched A moment ago on " + channelName +")", entry_text)
        if len(entryWatchedTimeMomentList) == 0:
        # If entry wasn't watched moment ago, check if it was watched less than 10 minutes ago
            entryWatchedTimeMinutesList = re.findall("Watched (\d*) Minutes ago on " + channelName, entry_text)
            if len(entryWatchedTimeMinutesList) == 0:
                writeToLog("INFO","FAILED to display correct text for watched entry")
                return False 
            
            else:
                if int(entryWatchedTimeMinutesList[0]) < 0 or int(entryWatchedTimeMinutesList[0]) > 10:
                    writeToLog("INFO","FAILED to display correct time when entry was watched")
                    return False 
                       
        return True    
     
    
    # @Author: Inbar Willman
    # Search entry in My History and check that the percent in progress bar is displayed in correct range
    # The assumption is that there is just one entry in search results
    def checkPercentInProgressBar(self, entryName, percent, timeout=60): 
        # Make a search in My History
        if self.isEntryExistsInMyHistory(entryName) == False:
            writeToLog("INFO","FAILED to find entry in My History")
            return False  
        
        # Check for percent display in progress bar   
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)   
        while wait_until > datetime.datetime.now(): 
            element = self.get_element(self.MY_HISTORY_PROGRESS_BAR_PRECENT)
            element_attribute_values = element.get_attribute("style").split()
            element_percent = int(element_attribute_values[1][:-2])
            if element_percent == percent:
                return True
            else:
                if element_percent > (percent - 4) and element_percent < (percent + 4):
                    return True
            self.isEntryExistsInMyHistory(entryName)  
            
        writeToLog("INFO","FAILED to display correct percent in progress bar")
        return False  
              
              
    # @Author: Inbar Willman
    def checkProgressBarStatus(self, entryName, description='', status=enums.ProgressBarStatus.STARTED, timeout=60):
        # Make a search in My History
        if self.isEntryExistsInMyHistory(entryName, description='') == False:
            writeToLog("INFO","FAILED to find entry in My History")
            return False  
             
        # Check for progress bar status
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)   
        while wait_until > datetime.datetime.now(): 
            if status == enums.ProgressBarStatus.COMPLETE:
                if self.is_visible(self.MY_HISTORY_PROGRESS_BAR_COMPLETE):
                    return True
            elif status == enums.ProgressBarStatus.STARTED:
                if self.is_visible(self.MY_HISTORY_PROGRESS_BAR_STARTED):
                    return True
            else:
                writeToLog("INFO","FAILED to get valid progress bar status")
                return False         
            self.isEntryExistsInMyHistory(entryName)     
            
        writeToLog("INFO","FAILED to display correct progress bar status")
        return False    
    
    
    # @Author: Inbar Willman 
    def clickEntryAfterSearchInMyHistory(self, entryName):    
        # Click on the Entry name
        if self.click(('xpath', "//span[@class='entry-name' and text()='" + entryName + "']"), 10) == False:
            # If entry not found, search for 'No Entries Found' alert
            if self.wait_for_text(self.MY_HISTORY_NO_RESULTS_ALERT, 'No Entries Found', 5) == True:
                writeToLog("INFO","No Entry: '" + entryName + "' was found")
            else:
                writeToLog("INFO","FAILED search for Entry: '" + entryName + "' something went wrong")
                
        return True
    
    
    # @Author: Inbar Willman
    # Filter entries in My History Page: By media type, watch status and time
    def filterInMyHistory(self, dropDownListName='' ,dropDownListItem=''):
        # Click on relevant filter
        tmpDropDown = (self.MY_HISTORY_DROP_DOWN_LIST_NAME[0], self.MY_HISTORY_DROP_DOWN_LIST_NAME[1].replace('DROPDOWN_LIST_NAME', dropDownListName.value)) 
        if self.click(tmpDropDown) == False:
            writeToLog("INFO","FAILED to click on filter " + dropDownListName.value)
            return False  
        
        sleep(2)   
        
        # Click on relevant filter item
        tmpFilterItem = (self.MY_HISTORY_DROP_DOWN_ITEM[0], self.MY_HISTORY_DROP_DOWN_ITEM[1].replace('MENU_ITEM', dropDownListItem.value))      
        if self.click(tmpFilterItem) == False:
            writeToLog("INFO","FAILED to click on item " + dropDownListItem.value)
            return False 
           
        self.clsCommon.general.waitForLoaderToDisappear()    
        writeToLog("INFO","Success, filter " + dropDownListName.value + " - " + dropDownListItem.value + " was set successfully")
        
        return True
    
    
    # @Author: Inbar Willman
    # Verify entries in my history page after filtering
    def verifyFiltersInMyHistory(self, entriesDict):
        if self.click(self.MY_HISTORY_REFRESH_BTN) == False:
            writeToLog("INFO","FAILED to click on refresh button")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
                    
        if self.clsCommon.myMedia.showAllEntries(searchIn = enums.Location.MY_HISTORY) == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False
            
        try:
            entriesInMyHistory = self.get_element(self.MY_HISTORY_TABLE).text.lower()
        except NoSuchElementException:
                writeToLog("INFO","FAILED to get entries list in galley")
                return False
        
        for entry in entriesDict:
            if entriesDict[entry] == True:
                if (entry.lower() in entriesInMyHistory) == False:
                        writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in my media although he need to be found")
                        return False
                
            if entriesDict[entry] == False:
                if (entry.lower() in entriesInMyHistory) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in my media although he doesn't need to be found")
                    return False
                
        writeToLog("INFO","Success, Only the correct media display in my media")
        return True
    
    
    # @Author: Inbar Willman 
    # The function check that only the entries with watch status that matches the 'watchStatus' parameter display in the list in my history
    def verifyFilterWatchStatus(self, watchStatus):
        if self.clsCommon.myMedia.showAllEntries(searchIn = enums.Location.MY_HISTORY) == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False
                  
        if watchStatus != enums.MyHistoryWatcheStatusItems.STARTED_WATCHING:
            if self.wait_elements(self.MY_HISTORY_PROGRESS_BAR_STARTED) != False:
                writeToLog("INFO","FAILED, entries with completed watching status are displayed in the list although only " + watchStatus.value + " need to be display")
                return False
                
        if watchStatus != enums.MyHistoryWatcheStatusItems.COMPLETED_WATCHING:
            if self.wait_elements(self.MY_HISTORY_PROGRESS_BAR_COMPLETE) != False:
                writeToLog("INFO","FAILED, entries with start watching status are displayed in the list although only " + watchStatus.value + " need to be display")
                return False
    
        writeToLog("INFO","Success, only " + watchStatus.value + " type entries display")
        return True   