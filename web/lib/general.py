from base import *
from selenium.webdriver.common.keys import Keys


class General(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #General locators:
    #=============================================================================================================
    KMS_LOADER                                          = ('id', 'loader')#loaderWrap
    ADD_NEW_DROP_DOWN_BUTTON                            = ('id', 'addNewDropDown')
    USER_MENU_TOGGLE_BUTTON                             = ('id', 'userMenuToggleBtn')
    USER_MENU_MY_MEDIA_BUTTON                           = ('xpath', "//a[@href='/my-media' and @role='menuitem']")
    USER_MENU_MY_CHANNELS_BUTTON                        = ('xpath', "//a[@href='/my-channels' and @role='menuitem']")
    USER_MENU_MY_PLAYLISTS_BUTTON                       = ('xpath', "//a[@href='/my-playlists' and @role='menuitem']")
    USER_MENU_MY_HISTORY_BUTTON                         = ('xpath', "//a[@href='/history' and @role='menuitem']")
    GLOBAL_SEARCH_BUTTON_NEWUI                          = ('xpath', "//span[@class='hidden-tablet' and contains(text(),'search')]")
    GLOBAL_SEARCH_TEXTBOX                               = ('xpath', "//input[@placeholder='Search all media' and @type='text']")
    ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_NEWUI           = ('xpath', "//a[@class='entryThumbnail  ' and @href='/media/ENTRY_ID']")
    ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_OLDUI           = ('xpath', "//img[@class='thumb_img' and @alt='Thumbnail for entry ENTRY_NAME']")
    ENTRY_PARENT_DESCRIPTION_AFTER_GLOBAL_SEARCH_NEWUI  = ('xpath', "//a[@class='cursor-pointer' and @href='/media/ENTRY_ID']")
    ENTRY_DESCRIPTION_AFTER_GLOBAL_SEARCH_NEWUI         = ('xpath', "//div[@class='results-entry__description hidden-phone']")
    ENTRY_DESCRIPTION_AFTER_GLOBAL_SEARCH_OLDUI         = ('xpath', "//p[@class='normalWordBreak searchme hidden-phone']")
    
    #=============================================================================================================

    def waitForLoaderToDisappear(self, timeout=60):
        sleep(1)
        self.wait_while_not_visible(self.KMS_LOADER, timeout)
        sleep(1)
        self.wait_while_not_visible(self.KMS_LOADER, timeout)
        
        
    def serchAndVerifyInGlobalSearch(self, searchWord):
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
        result =  self.clsCommon.myMedia.getResultAfterSearch(searchWord)
        if result == False:
            writeToLog("INFO","FAILED to find search word in global search")
            return False
        
        if result.text != searchWord:
            writeToLog("INFO","FAILED, the search word that was found is not the correct one. search word is: " + searchWord + " and what was found is: " + result.text)
            return False
            
        writeToLog("INFO","Success, search word was found and verify")    
        return True
    
 
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