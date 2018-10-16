from base import *
import clsTestService
from general import General
from logger import writeToLog
from editEntryPage import EditEntryPage
import enums
from selenium.webdriver.common.keys import Keys


class Home(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Home page locators:
    #=============================================================================================================
    HOME_LINK                                           = ('id', 'menu-Home-btn')
    HOME_PLAYLIST                                       = ('xpath', "//a[@class='clickable-header' and contains(text(),'PLAYLIST')]")
    HOME_PLAYLIST_ENTRY                                 = ('xpath', '//img[contains(@alt,"ENTRY_NAME")]/ancestor::div[@class="photo-group featured_wrapper"]')
    HOME_CAROUSEL_ENTRY                                 = ('xpath', "//h1[@class='home__carousel-entry-title entryTitle tight' and contains(text(),'ENTRY_NAME')]")
    HOME_CAROUSEL_ENTRY_OLD_UI                          = ('xpath', "//img[@alt='ENTRY_NAME']")
    
    #=============================================================================================================  
    # @Author: Inbar Willman / Michal Zomper
    # This method navigate to home page
    def navigateToHomePage(self, forceNavigate=False):
        if forceNavigate == False:
            # Check if we are already in home page
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_TEST_BASE_URL , False, 3) == True:
                return True
         
        # navigate to home page
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_TEST_BASE_URL) == False:
            writeToLog("INFO","FAILED navigate to home page")
            return False
            
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_TEST_BASE_URL , False, 5) == False:
            writeToLog("INFO","FAILED verify that home page display")
            return False
        return True
    
    # @Author: Inbar Willman
    def checkEntryInHomePlaylist(self, playlist, entryName):
        if self.navigateToHomePage() == False:
            writeToLog("INFO","FAILED to navigate to home page")
            return False 
                   
        playlist_list = (self.HOME_PLAYLIST[0], self.HOME_PLAYLIST[1].replace('PLAYLIST', playlist))
        if self.is_visible(playlist_list):
            tmp_entry = (self.HOME_PLAYLIST_ENTRY[0], self.HOME_PLAYLIST_ENTRY[1].replace('ENTRY_NAME', entryName))
            if self.is_visible(tmp_entry) == False:
                writeToLog("INFO","FAILED to find entry in " + playlist + " List")
                return False  
            
            return True         
        
        writeToLog("INFO","FAILED to find " + playlist + " List")
        return False 
        
            
    # @Author: Michal Zomper
    def verifyEntyNameAndThumbnailInHomePagePlaylist(self, entryName, expectedQrResult, cropLeft, croTop, cropRight, cropBottom):  
        tmp_entry = (self.HOME_PLAYLIST_ENTRY[0], self.HOME_PLAYLIST_ENTRY[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmp_entry) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' in playlist")
            return False
        
        qrResult = self.clsCommon.qrcode.getScreenshotAndResolveCustomImageQrCode(cropLeft, croTop, cropRight, cropBottom, tmp_entry)
        
        if qrResult != str(expectedQrResult):
            writeToLog("INFO","FAILED entry thumbnail is '" + str(qrResult) + "' but need to be '" + str(expectedQrResult) + "'")
            return False  
        
        writeToLog("INFO","Success, entry'" + entryName + "' was verified")
        return True  
        

    def verifyEntryInHomePageCarousel(self, entryName, expectedQrResult, cropLeft, croTop, cropRight, cropBottom):  
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            tmpEntryName = (self.HOME_CAROUSEL_ENTRY_OLD_UI[0], self.HOME_CAROUSEL_ENTRY_OLD_UI[1].replace('ENTRY_NAME', entryName) + "/ancestor::div[@class='carmain']")
        else:
            tmpEntryName = (self.HOME_CAROUSEL_ENTRY[0], self.HOME_CAROUSEL_ENTRY[1].replace('ENTRY_NAME', entryName) + "/ancestor::div[@class='thumbnail-info__container']")
         
        if self.is_visible(tmpEntryName) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' in home page carousel playlist")
            return False 
        
        qrResult = self.clsCommon.qrcode.getScreenshotAndResolveCustomImageQrCode(cropLeft, croTop, cropRight, cropBottom, tmpEntryName)
        
        if qrResult != str(expectedQrResult):
            writeToLog("INFO","FAILED entry thumbnail is '" + str(qrResult) + "' but need to be '" + str(expectedQrResult) + "'")
            return False  
        
        writeToLog("INFO","Success, entry'" + entryName + "' in  home page carousel  was verified")
        return True