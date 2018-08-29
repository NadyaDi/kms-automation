from openpyxl.compat.strings import unicode
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from base import *
import clsTestService
import enums
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
    GLOBAL_SEARCH_RESULT_CATEGORY_TABLE_OLDUI            = ('xpath', "//table[@id='galleryResultsTable']")
    #============================================================================================================#
    
    # Author: Michal Zomper
    # the function only insert and search word in global search , NO VERIFICATION in this function for the result
    def searchInGlobalsearch(self, searchWord):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if self.click(self.GLOBAL_SEARCH_BUTTON_NEWUI, timeout=15) == False:
                writeToLog("INFO","FAILED to click on global search button")
                return False
            
            if self.click(self.GLOBAL_SEARCH_TEXTBOX, timeout=10, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on global search textbox")
                return False
                
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
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            # Verify thumbnail qr code
            result =  self.clsCommon.myMedia.getResultAfterSearch(entryName)
            if result == False:
                writeToLog("INFO","FAILED to find search word in global search")
                return False
            
            parent = result.find_element_by_xpath("..")
            entryHref = parent.get_attribute("href")
            entryId = entryHref.split("/")[len(entryHref.split("/"))-1]
            
            tmp_entryThum = (self.ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_NEWUI[0], self.ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_NEWUI[1].replace('ENTRY_ID', entryId))
            try:
                thumbElement = self.get_element(tmp_entryThum)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find entry thumbnail element after global search")
                return False
            
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
    def serchAndVerifyChannelInGlobalSearch(self, searchWord):
        if self.searchInGlobalsearch(searchWord) == False:
            writeToLog("INFO","FAILED to search in global search ")
            return False
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if self.click(self.GLOBAL_SEARCH_GO_TO_CHANNEL_RESULTS_NEWUI, timeout=15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on go to channel results button")
                return False
        else:
            if self.click(self.GLOBAL_SEARCH_CATEGORIES_TAB_OLDUI, timeout=15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on categories tab")
                return False
        sleep(3)
        tmpChannelName = (self.clsCommon.channel.MY_CHANNELS_HOVER[0], self.clsCommon.channel.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', searchWord))
        if self.wait_visible(tmpChannelName, timeout=15, multipleElements=False) == False:
            writeToLog("INFO","FAILED, searched channel was NOT found")
            return False
            
        writeToLog("INFO","Success, searched channel was found and verify")    
        return True