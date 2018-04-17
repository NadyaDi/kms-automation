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
    HOME_PLAYLIST                                       = ('xpath', '//a[@class="clickable-header" and text()="PLAYLIST"]')
    HOME_PLAYLIST_ENTRY                                 = ('xpath', '//img[@alt="ENTRY_NAME"]/ancestor::li[@class="span4"]')
    
    #=============================================================================================================  
    # @Author: Inbar Willman
    # This method navigate to home page
    def navigateToHomePage(self, forceNavigate = False):
        # Check if we are already in home page
#         if forceNavigate == False:
#             if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_HOME_URL , False, 1) == True:
#                 return True
        
        # Click on name in header in order to navigate to home page
        if self.click(self.HOME_LINK) == False:
            writeToLog("INFO","FAILED to click on name in header")
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
    def verifyEntyNameAndThumbnailInHomePagePlaylist(self, entryName, expectedQrResult, cropLeft, croTop, cropRight, cropButtom):  
        tmp_entry = (self.HOME_PLAYLIST_ENTRY[0], self.HOME_PLAYLIST_ENTRY[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmp_entry) == False:
            writeToLog("INFO","FAILED to find entry in " + entryName + " in playlist")
            return False  
        
        qrResult = self.clsCommon.qrcode.takeCustomQrCodeScreenshot(cropLeft, croTop, cropRight, cropButtom)
        
        if qrResult != expectedQrResult:
            writeToLog("INFO","FAILED entry thumbnail is '" + qrResult + "' but need to be '" + expectedQrResult + "'")
            return False  
        
        writeToLog("INFO","Success, entry'" + entryName + "' was verified")
        return True  
            
        

        
              
   