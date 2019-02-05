from openpyxl.compat.strings import unicode
from selenium.webdriver.common.action_chains import ActionChains
 
 
from base import *
import clsTestService
import enums
from selenium.webdriver.common.keys import Keys
from general import General



class  GlobalSearch(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #                                  Global Search locators:                                                   #
    #=============================================================================================================
    GLOBAL_SEARCH_BUTTON_NEWUI                          = ('xpath', "//span[@class='hidden-tablet' and contains(text(),'Search')]")
    GLOBAL_SEARCH_TEXTBOX                               = ('xpath', "//input[@placeholder='Search all media' and @type='text']")
    ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_NEWUI           = ('xpath', "//a[@class='entryThumbnail  ' and @href='/media/ENTRY_ID']")
    ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_OLDUI           = ('xpath', "//img[@class='thumb_img' and @alt='Thumbnail for entry ENTRY_NAME']")
    ENTRY_PARENT_DESCRIPTION_AFTER_GLOBAL_SEARCH_NEWUI  = ('xpath', "//a[@class='cursor-pointer' and @href='/media/ENTRY_ID']")
    ENTRY_DESCRIPTION_AFTER_GLOBAL_SEARCH_NEWUI         = ('xpath', "//div[@class='results-entry__description hidden-phone']")
    ENTRY_DESCRIPTION_AFTER_GLOBAL_SEARCH_OLDUI         = ('xpath', "//p[@class='normalWordBreak searchme hidden-phone']")
    ENTRY_DESCRIPTION_AFTER_GLOBAL_SEARCH_OLDUI         = ('xpath', "//p[@class='normalWordBreak searchme hidden-phone']")
    GLOBAL_SEARCH_GO_TO_GALLERY_RESULTS_NEWUI           = ('xpath', "//a[@class='CategorySearchResults__resultsLink' and contains(text(), 'Go to Gallery Results')]")
    GLOBAL_SEARCH_GO_TO_CHANNEL_RESULTS_NEWUI           = ('xpath', "//a[@class='CategorySearchResults__resultsLink' and contains(text(), 'Go to Channel Results')]")
    GLOBAL_SEARCH_CATEGORIES_TAB_OLDUI                  = ('xpath', "//a[@id='galleries-tab']")
    GLOBAL_SEARCH_RESULT_CATEGORY_NAME                  = ('xpath', "//span[@aria-label='CTEGORY_NAME']")
    GLOBAL_SEARCH_RESULT_CATEGORY_TABLE_OLDUI           = ('xpath', "//table[@id='galleryResultsTable']")
    GLOBAL_SEARCH_CHANNEL_TAB_OLDUI                     = ('xpath', "//a[@id='channels-tab']")
    GLOBAL_SEARCH_RESULT_CHANNELY_TABLE_OLDUI           = ('xpath', "//table[@id='channelResultsTable']")
    GLOBAL_SEARCH_IN_CAPTION_TAB_OLDUI                  = ('xpath', "//a[@id='captions-tab']")
    GLOBAL_SEARCH_CAPTION_TIME_RESULT_OLDUI             = ('xpath', "//a[@class='captions_search_result' and  contains(text(),'CAPTION_TIME')]")
    #GLOBAL_SEARCH_CAPTION_SEARCH_WORD_RESULT_NEWUI      = ('xpath', "//span[@class='resultLine searchme' and  contains(text(),'CAPTION_WORD')]")
    GLOBAL_SEARCH__PARENT_CAPTION_SEARCH_WORD_RESULT_NEWUI = ('xpath', "//span[@class='resultLine searchme']")
    GLOBAL_SEARCH__CHILD_CAPTION_SEARCH_WORD_RESULT_NEWUI = ('xpath', "//span[@class='searchTerm' and contains(text(),'CAPTION_WORD')]")
    GLOBAL_SEARCH_CAPTION_SEARCH_WORD_RESULT_NEWUI      = ('xpath', "//span[@class='resultLine searchme' and  contains(text(),'CAPTION_WORD')]")
    GLOBAL_SEARCH_CAPTION_ICON_NEWUI                    = ('xpath', ".//span[@class='results-summary-item__text']")
    GLOBAL_SEARCH_CAPTION_RESULT_NEWUI                  = ('xpath', "//div[@class='results__result-item']")
    GLOBAL_SEARCH_ENTRY_RESUTLT_ROW                     = ('xpath', "//div[@class='results-entry__container']")
    GLOBAL_SEARCH_NO_RESULTS_ALERT                      = ('xpath', '//div[@class="no-results alert alert-info" and text()="No more media found."]')
    GLOBAL_SEARCH_ENTRY_RESUTLT_NAME                    = ('xpath', '//span[@class="results-entry__name"]')
    GLOBAL_SEARCH_NO_RESULTS_ALERT_QUIZ                 = ('xpath', "//div[@id='quizMyMedia_scroller_alert']")
    GLOBAL_SEARCH_NO_RESULTS_ALERT_FLTER                = ('xpath', "//div[@class='no-results_body']")
    #============================================================================================================#
    
    # Author: Michal Zomper
    # the function only insert and search word in global search , NO VERIFICATION in this function for the result
    def searchInGlobalsearch(self, searchWord):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if self.click(self.GLOBAL_SEARCH_BUTTON_NEWUI, timeout=15) == False:
                writeToLog("INFO","FAILED to click on global search button")
                return False
            
        sleep(1)        
        if self.clear_and_send_keys(self.GLOBAL_SEARCH_TEXTBOX, searchWord + Keys.ENTER, multipleElements=True) == False:
            writeToLog("INFO","FAILED to insert search word to global search textbox")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(5)
        
        return True
        
        
    # Author: Michal Zomper
    # The function search and verify the entry that was searched in global search
    def serchAndVerifyEntryInGlobalSearch(self, searchWord):
        if self.searchInGlobalsearch(searchWord) == False:
            writeToLog("INFO","FAILED to search in global search ")
            return False
        
        # Remove '"' (if exists) from the begining and end of the search word
        searchWord = searchWord.replace('"', '')
        
        result =  self.clsCommon.myMedia.getResultAfterSearch(searchWord)
        if result == False:
            writeToLog("INFO","FAILED to find search word in global search")
            return False
        
        if result.text != searchWord:
            writeToLog("INFO","FAILED, the search word that was found is not the correct one. search word is: " + searchWord + " and what was found is: " + result.text)
            return False
            
        writeToLog("INFO","Success, search word was found and verify")    
        return True
    
    
    # Author: Michal Zomper
    # the function verify the matedata for the searched entry in the global search 
    def VerifyEntryMetadataAfterGlobalSearch(self, entryName, thumbQRCodeResult, description):
        sleep(2)
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            # Verify thumbnail qr code
            result =  self.clsCommon.myMedia.getResultAfterSearch(entryName)
            if result == False:
                writeToLog("INFO","FAILED to find search word in global search")
                return False
            
            sleep(1)
            parent = result.find_element_by_xpath("..")
            entryHref = parent.get_attribute("href")
            entryId = entryHref.split("/")[len(entryHref.split("/"))-1]
            
            tmp_entryThum = (self.ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_NEWUI[0], self.ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_NEWUI[1].replace('ENTRY_ID', entryId))
            thumbElement = self.wait_element(tmp_entryThum, multipleElements=True)
            if thumbElement == False:
                writeToLog("INFO","FAILED to find entry thumbnail element after global search")
                return False                
            
            sleep(2)
            thumQrCode =  self.clsCommon.qrcode.takeAndResolveElementQrCodeScreenshot(thumbElement) 
            if thumQrCode != thumbQRCodeResult:
                writeToLog("INFO","FAILED verify entry thumbnail QR code after global search")
                return False
            
            # Verify entry description
            tmp_entrydesc = (self.ENTRY_PARENT_DESCRIPTION_AFTER_GLOBAL_SEARCH_NEWUI[0], self.ENTRY_PARENT_DESCRIPTION_AFTER_GLOBAL_SEARCH_NEWUI[1].replace('ENTRY_ID', entryId))
            try:
                descriptionPerantElement = self.get_element(tmp_entrydesc)
                descriptionElement = self.get_child_element(descriptionPerantElement, self.ENTRY_DESCRIPTION_AFTER_GLOBAL_SEARCH_NEWUI)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find entry description element after global search")
                return False
            
            if descriptionElement.text != description:
                writeToLog("INFO","FAILED to verify entry description after global search")
                return False
        else:
            # Verify thumbnail qr code
            tmp_entryThum = (self.ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_OLDUI[0], self.ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_OLDUI[1].replace('ENTRY_NAME', entryName))
            try:
                thumbElement = self.get_element(tmp_entryThum)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find entry thumbnail element after global search")
                return False
            
            thumQrCode =  self.clsCommon.qrcode.takeAndResolveElementQrCodeScreenshot(thumbElement) 
            if thumQrCode != thumbQRCodeResult:
                writeToLog("INFO","FAILED verify entry thumbnail QR code after global search")
                return False
            
            
            try:
                entryParentel = thumbElement.find_element_by_xpath("../../../..")
                descriptionElement = self.get_child_element(entryParentel, self.ENTRY_DESCRIPTION_AFTER_GLOBAL_SEARCH_OLDUI)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find entry description element after global search")
                return False
            
            if descriptionElement.text != description:
                writeToLog("INFO","FAILED to verify entry description after global search")
                return False
            
        writeToLog("INFO","Success, entry matedata was verify after global search")    
        return True
    
    # Author: Michal Zomper
    # The function search and verify the CATEGORY that was searched in global search
    def serchAndVerifyCategoryInGlobalSearch(self, searchWord):
        if self.searchInGlobalsearch(searchWord) == False:
            writeToLog("INFO","FAILED to search in global search ")
            return False
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if self.click(self.GLOBAL_SEARCH_GO_TO_GALLERY_RESULTS_NEWUI, timeout=15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on go to gallery results button")
                return False
        else:
            if self.click(self.GLOBAL_SEARCH_CATEGORIES_TAB_OLDUI, timeout=15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on categories tab")
                return False
        sleep(3)
        if self.getAndVerifyCategoryResultAfterGlobalSearch(searchWord) == False:
            writeToLog("INFO","FAILED, the search category was NOT found")
            return False
            
        writeToLog("INFO","Success, searched category was found and verify")    
        return True
   
   
    # This method for Elastic Search (new UI), returns the result element.         
    def getAndVerifyCategoryResultAfterGlobalSearch(self, searchString):
        #If we are in new UI with Elastic search
        if self.clsCommon.isElasticSearchOnPage() == True:
            tmpCategory = (self.GLOBAL_SEARCH_RESULT_CATEGORY_NAME[0], self.GLOBAL_SEARCH_RESULT_CATEGORY_NAME[1].replace('CTEGORY_NAME', searchString))
            results = self.wait_elements(tmpCategory, 30)
        
            if results == False:
                writeToLog("INFO","No categories found")
                return False 
            for result in results:
                
                if result.text == searchString:
                    return True
        #If we are in old UI
        else:
            results = self.wait_elements(self.GLOBAL_SEARCH_RESULT_CATEGORY_TABLE_OLDUI, 30) 
            if results == False:
                    writeToLog("INFO","No categories found")
                    return False        
            
            for result in results:
                if searchString in result.text:
                    return True 
        
        writeToLog("INFO","No categories found after search entry: '" + searchString + "'") 
        return False 
       
    
    # Author: Michal Zomper
    # The function search and verify the channel that was searched in global search
    def serchAndVerifyChannelInGlobalSearch(self, searchChannel):
        if self.searchInGlobalsearch(searchChannel) == False:
            writeToLog("INFO","FAILED to search in global search ")
            return False
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if self.click(self.GLOBAL_SEARCH_GO_TO_CHANNEL_RESULTS_NEWUI, timeout=15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on go to channel results button")
                return False
            sleep(3)
            
            tmpChannelName = (self.clsCommon.channel.MY_CHANNELS_HOVER[0], self.clsCommon.channel.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', searchChannel))
            if self.wait_visible(tmpChannelName, timeout=15, multipleElements=False) == False:
                writeToLog("INFO","FAILED, searched channel was NOT found")
                return False
            
            writeToLog("INFO","Success, searched channel was found and verify")    
            return True
            
        else:
            if self.click(self.GLOBAL_SEARCH_CHANNEL_TAB_OLDUI, timeout=15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on channels tab")
                return False
            sleep(3)
            
            results = self.wait_elements(self.GLOBAL_SEARCH_RESULT_CHANNELY_TABLE_OLDUI, 30) 
            if results == False:
                writeToLog("INFO","No channel found")
                return False        
            
            for result in results:
                if searchChannel in result.text:
                    writeToLog("INFO","Success, searched channel was found and verify")
                    return True 

            writeToLog("INFO","FAILED, searched channel was NOT found")    
            return False
        
        
    # Author: Michal Zomper
    # The function search and verify the caption that was searched in global search
    def serchAndVerifyCaptionInGlobalSearch(self, searchedCaption, captionTime, entryName):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if self.searchInGlobalsearch('"' + searchedCaption+ '"') == False:
                writeToLog("INFO","FAILED to search in global search ")
                return False
        
            tmpEntry =  self.clsCommon.myMedia.getResultAfterSearch(entryName)
            if tmpEntry == False:
                writeToLog("INFO","FAILED to find the entry of with the searched caption after global search")
                return False
            
            try:
                entryParent = tmpEntry.find_element_by_xpath("../../../..")
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find entry parent")
                return False
            
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
            if self.click_child(entryParent, self.GLOBAL_SEARCH_CAPTION_ICON_NEWUI, timeout=15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on entry caption icon")
                return False
#             entryParent.find_element_by_xpath(".//span[@class='results-summary-item__text']").click()
            
            try:
                tmpCaption = self.get_child_element(entryParent, self.GLOBAL_SEARCH_CAPTION_RESULT_NEWUI)
            except NoSuchElementException:
                    writeToLog("INFO","FAILED to find caption results")
                    return False
            
            if  (captionTime in tmpCaption.text) == False:
                writeToLog("INFO","FAILED to find caption correct time")
                return False
            
            if (searchedCaption in tmpCaption.text) == False:
                writeToLog("INFO","FAILED to find searched caption under the entry")
                return False
                
        else:
            if self.searchInGlobalsearch(searchedCaption) == False:
                writeToLog("INFO","FAILED to search in global search ")
                return False
            
            if self.click(self.GLOBAL_SEARCH_IN_CAPTION_TAB_OLDUI, timeout=15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on search in video tab")
                return False
            sleep(3)
            
            tmpEntryThumbnail = (self.clsCommon.myMedia.MY_MEDIA_ENTRY_THUMBNAIL[0], self.clsCommon.myMedia.MY_MEDIA_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName))
            entryThumbnail = self.wait_element(tmpEntryThumbnail, 30) 
            if entryThumbnail == False:
                writeToLog("INFO","FAILED No entry found")
                return False 
            try:
                entryParent= entryThumbnail.find_element_by_xpath("../../../..")
            except NoSuchElementException:
                writeToLog("INFO","FAILED to fins entry parent")
                return False
            
            tmeCaptionTime = (self.GLOBAL_SEARCH_CAPTION_TIME_RESULT_OLDUI[0], self.GLOBAL_SEARCH_CAPTION_TIME_RESULT_OLDUI[1].replace('CAPTION_TIME', captionTime))
            if  self.wait_visible_child(entryParent, tmeCaptionTime, timeout=20) == False:
                writeToLog("INFO","FAILED to find caption time after global search")
                return False   
            
            try:
                parentCaptionSearch= self.wait_element(self.GLOBAL_SEARCH__PARENT_CAPTION_SEARCH_WORD_RESULT_NEWUI)
                if parentCaptionSearch == False:
                    writeToLog("INFO","FAILED to find caption parent element after global search")
                    return False   
            except NoSuchElementException:
                return False     
            
            tmeCaptionSearch = (self.GLOBAL_SEARCH__CHILD_CAPTION_SEARCH_WORD_RESULT_NEWUI[0], self.GLOBAL_SEARCH__CHILD_CAPTION_SEARCH_WORD_RESULT_NEWUI[1].replace('CAPTION_WORD', searchedCaption))
            if self.wait_visible_child(parentCaptionSearch, tmeCaptionSearch, timeout=20) == False:
                writeToLog("INFO","FAILED to find caption search word after global search")
                return False
            
        writeToLog("INFO","Success, searched caption was found and verify")
        return True 
    
    
    # @Author: Inbar Willman
    # Make an exact search in global search
    # isHeader search - if true make an header global search, else make global search in global search body page
    def makeAGloablSearchForEsearch(self,searchTerm,isHeaderSearch=True, exactSearch=True):
        if isHeaderSearch == True:
            if self.click(self.GLOBAL_SEARCH_BUTTON_NEWUI, timeout=15) == False:
                writeToLog("INFO","FAILED to click on global search button")
                return False
            
        if self.click(self.GLOBAL_SEARCH_TEXTBOX, timeout=10, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on global search textbox")
            return False
        
        if exactSearch == True:
            searchLine = '"' + searchTerm + '"'
        else:
            searchLine = searchTerm
                
        if self.clear_and_send_keys(self.GLOBAL_SEARCH_TEXTBOX, searchLine + Keys.ENTER, multipleElements=True) == False:
            writeToLog("INFO","FAILED to insert search word to global search textbox")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(5)
        
        return True
    
    
    # @Author: Inbar Willman
    # Sort entries in global page and verify that they are sorted by the correct order
    def verifySortInGlobalPage(self, sortBy, entriesList):
        if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.SORT_BY,sortBy) == False:
            writeToLog("INFO","FAILED to sort entries")
            return False
                
        if self.showAllEntriesInGloablPage() == False:
            writeToLog("INFO","FAILED to show all entries in global page")
            return False
        sleep(10)
        
        try:
            # Get list of all entries element in results
            entriesInGlobalPage = self.get_elements(self.GLOBAL_SEARCH_ENTRY_RESUTLT_NAME)
            listOfEntriesInResults = []
            
            # Get text of each entry element and add to a new list
            for entry in entriesInGlobalPage:
                entry.text.lower()
                listOfEntriesInResults.append(entry.text.lower())
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list")
            return False
        
        prevEntryIndex = -1
        
        if self.clsCommon.isElasticSearchOnPage() == True:
            for entry in entriesList:
                try:
                    currentEntryIndex = listOfEntriesInResults.index(entry.lower())
                except:
                    writeToLog("INFO","FAILED , entry '" + entry + "' was not found in global page" )
                    return False             
                       
                if prevEntryIndex > currentEntryIndex:
                    writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct. entry '" + entry + "' isn't in the right place" )
                    return False
                prevEntryIndex = currentEntryIndex
                    
            writeToLog("INFO","Success, Global page sort by '" + sortBy.value + "' was successful")
            return True   
        else:
            for entry in entriesList:
                currentEntryIndex = listOfEntriesInResults.index(entry.lower())
                if prevEntryIndex > currentEntryIndex:
                    writeToLog("INFO","FAILED ,sort by '"  + sortBy.value + "' isn't correct. entry '" + entry + "' isn't in the right place" )
                    return False
                prevEntryIndex = currentEntryIndex
                    
            writeToLog("INFO","Success, Global page sort by '" + sortBy.value + "' was successful")
            return True
        
        
    # @Author: Inbar Willman
    # Show all entries in global page    
    def showAllEntriesInGloablPage(self, timeOut=75):
        # Get all entries in results
        try:
            tmpResultsList = self.get_elements(self.GLOBAL_SEARCH_ENTRY_RESUTLT_ROW)
            
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries in results")
            return False
        
        if len(tmpResultsList) < 4:
            writeToLog("INFO","Success, All media in global page are displayed")
            return True 
        
        else:      
            self.clsCommon.sendKeysToBodyElement(Keys.END)
            wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)  
            while wait_until > datetime.datetime.now():                       
                if self.is_present(self.GLOBAL_SEARCH_NO_RESULTS_ALERT, 2) == True:
                    writeToLog("INFO","Success, All media in global page are displayed")
                    sleep(1)
                    # go back to the top of the page
                    self.clsCommon.sendKeysToBodyElement(Keys.HOME)
                    return True 
             
                self.clsCommon.sendKeysToBodyElement(Keys.END)
             
        writeToLog("INFO","FAILED to show all media")
        return False    
    
    
    # @Author: Inbar Willman
    # The function check the the entries in my media are filter correctly
    def verifyFiltersInGlobalPage(self, entriesDict, noEntriesExpected=False):
        if noEntriesExpected == True:
            if self.wait_element(self.GLOBAL_SEARCH_NO_RESULTS_ALERT_FLTER, 1, multipleElements=True) != False:
                writeToLog("INFO", "PASSED, no entries are displayed")
                return True
            else:
                writeToLog("INFO", "Some entries are present, we will verify the dictionaries")
        
        if self.showAllEntriesInGloablPage() == False:
                writeToLog("INFO","FAILED to show all entries in global page")
                return False
             
        try:
            # Get list of all entries element in results
            entriesInGlobalPage = self.get_elements(self.GLOBAL_SEARCH_ENTRY_RESUTLT_NAME)
            listOfEntriesInResults = []
            
            # Get text of each entry element and add to a new list
            for entry in entriesInGlobalPage:
                entry.text.lower()
                listOfEntriesInResults.append(entry.text.lower())
                
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list")
            return False
         
        for entry in entriesDict:
            #if entry[1] == True:
            if entriesDict[entry] == True:
                #if entry[0].lower() in entriesInMyMedia == False:
                if (entry.lower() in listOfEntriesInResults) == False:
                    writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in global page results although he need to be found")
                    return False
                 
            #elif entry[1] == False:
            if entriesDict[entry] == False:
                # if entry[0].lower() in entriesInMyMedia == True:
                if (entry.lower() in listOfEntriesInResults) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in global page results although he doesn't need to be found")
                    return False
                 
        writeToLog("INFO","Success, Only the correct media display in global page")
        return True
