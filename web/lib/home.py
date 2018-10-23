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
    HOME_NAV_BAR_BUTTON                                 = ('xpath', "//a[@id='Kbtn-navbar']")
    HOME_NAV_BAR                                        = ('xpath', "//ul[@id='menu' and contains(@class, 'nav dd-menu']")
    HOME_LINK_IN_NAV_BAR                                = ('xpath', "//a[@class='navbar-link' and contains(text(),'LINK_NAME')]")
    HOME_HORIZONTAL_MENU_NAV_BAR                        = ('xpath', "//div[@id='horizontalMenu']")
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
        
        
    # @Author: Michal Zomper
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
    
    
    # @Author: Michal Zomper
    def openVerticalNavigationBar(self):
        if self.click(self.HOME_NAV_BAR_BUTTON) == False:
            writeToLog("INFO","FAILED to click on main menu button")
            return False 
        
        if self.is_visible(self.HOME_NAV_BAR) == False:
            writeToLog("INFO","FAILED to find main menu")
            return False
        
        if self.is_visible(self.HOME_HORIZONTAL_MENU_NAV_BAR) == False:
            writeToLog("INFO","FAILED to verify  vertical navigation bar is dispaly")
            return False
        
        writeToLog("INFO","Success,main menu is open")
        return True
            
            
    # @Author: Michal Zomper       
    def checklinkFormNavBarOnInNewWindow(self, linkName, expectedUrl, isExactUrl):
        # Save current window driver
        window_before = self.driver.window_handles[0]
        
        #open new window
        linkNameTmp = (self.HOME_LINK_IN_NAV_BAR[0], self.HOME_LINK_IN_NAV_BAR[1].replace('LINK_NAME', linkName)) 
        if self.click(linkNameTmp) == False:
            writeToLog("INFO","FAILED to click on link in nav bar")
            return False
        sleep(2)   
            
        # Verify new window landing page URL
        window_after = self.driver.window_handles[1]
        self.driver.switch_to_window(window_after)
        if isExactUrl == False:
            if expectedUrl not in self.driver.current_url:
                writeToLog("INFO","FAILED to verify new window landing page URL, expected: " + expectedUrl + "; Actual: " + self.driver.current_url)
                return False
        else:
            if expectedUrl != self.driver.current_url:
                writeToLog("INFO","FAILED to verify new window landing page URL, expected: " + expectedUrl + "; Actual: " + self.driver.current_url)
                return False           
       
        # Close landing page
        self.driver.close()
        # Restore to original window driver
        self.driver.switch_to_window(window_before)
        
        return True