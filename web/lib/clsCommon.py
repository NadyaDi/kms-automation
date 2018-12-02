import os
import shutil
from admin import Admin
from autoit import Autoit
from base import Base
from category import Category
from channel import Channel
from clsQrCodeReader import QrCodeReader
import clsTestService
from editEntryPage import EditEntryPage
from entryPage import EntryPage
from general import General
from kea import Kea
import localSettings
from logger import *
from login import Login
from myHistory import MyHistory
from myMedia import MyMedia
from myPlaylists import MyPlaylists
from player import Player
from upload import Upload
from home import Home
from freeTrial import FreeTrial
from kafBB import BlackBoard
from kafSharepoint import SharePoint
from selenium.webdriver.common.keys import Keys
from api import ApiClientSession
from globalSearch import GlobalSearch
import filecmp
from kafGeneric import KafGeneric
from kafMoodle import Moodle


    #============================================================================================================
    # The class contains functions that relates to common actions
    #============================================================================================================
class Common():
    # Parameters
    driver = None
   
    def __init__(self, driver):
        self.driver             = driver
        self.base               = Base(driver)
        self.autoit             = Autoit(self) 
        self.admin              = Admin(self, driver)
        self.login              = Login(self, driver)
        self.upload             = Upload(self, driver)
        self.general            = General(self, driver)
        self.myMedia            = MyMedia(self, driver)
        self.entryPage          = EntryPage(self, driver)
        self.editEntryPage      = EditEntryPage(self, driver)
        self.category           = Category(self, driver)
        self.channel            = Channel(self, driver)
        self.myPlaylists        = MyPlaylists(self, driver)
        self.player             = Player(self, driver)
        self.myHistory          = MyHistory(self, driver)
        self.qrcode             = QrCodeReader(self, driver)
        self.kea                = Kea(self, driver)
        self.home               = Home(self, driver)
        self.freeTrail          = FreeTrial(self, driver)
        self.apiClientSession   = ApiClientSession(self, driver)
        self.globalSearch       = GlobalSearch(self, driver)
        ### KAF ###
        self.kafGeneric         = KafGeneric(self, driver)
        self.blackBoard         = BlackBoard(self, driver)
        self.sharePoint         = SharePoint(self, driver)
        self.moodle             = Moodle(self, driver)
        
    #=============================================================================================================
    # Locators:
    #=============================================================================================================
      
     
    #============================================================================================================
    # Common Methods
    #============================================================================================================
    def instertPathInFileUploadWindows(self, path):
        if localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd":
            autoitDr = self.autoit.autoitDriver
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd2":
            autoitDr = self.autoit.autoitDriver2
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd3":
            autoitDr = self.autoit.autoitDriver3
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd4":
            autoitDr = self.autoit.autoitDriver4
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd5":
            autoitDr = self.autoit.autoitDriver5
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd6":
            autoitDr = self.autoit.autoitDriver6
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd7":
            autoitDr = self.autoit.autoitDriver7    
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd8":
            autoitDr = self.autoit.autoitDriver8    
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd9":
            autoitDr = self.autoit.autoitDriver9    
        elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd10":
            autoitDr = self.autoit.autoitDriver10                                        
            
        if (localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_IE):
            # TODO IE not implemented yet
            autoitDr.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFile.exe', path)
        elif(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_FIREFOX):
            autoitDr.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFileFirefox.exe', path)
        elif(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
            # If running on chrome, use autoitDriver2 because it on another node
            autoitDr.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFileChrome.exe', path)
        else:
            writeToLog("INFO","FAILED to type into 'Choose File' window, unknown browser: '" + localSettings.LOCAL_RUNNING_BROWSER + "'")
        
        
    def loginAsUser(self):
        if self.base.getAppUnderTest() == enums.Application.MEDIA_SPACE:
            return self.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
        elif self.base.getAppUnderTest() == enums.Application.BLACK_BOARD:
            return self.blackBoard.loginToBlackBoard(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
        elif self.base.getAppUnderTest() == enums.Application.SHARE_POINT:
            return self.sharePoint.loginToSharepoint(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)      
        elif self.base.getAppUnderTest() == enums.Application.MOODLE:
            return self.moodle.loginToMoodle(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)   
    
    
    # Author: Tzachi Guetta     
    def navigateTo(self, navigateTo, navigateFrom='', nameValue='', forceNavigate=False):
        if navigateTo == enums.Location.ENTRY_PAGE:
            if self.entryPage.navigateToEntry(nameValue, navigateFrom) == False:
                raise Exception("INFO","FAILED navigate to entry: '" + nameValue)
                
        elif navigateTo == enums.Location.EDIT_ENTRY_PAGE:
            if self.editEntryPage.navigateToEditEntry(nameValue, navigateFrom) == False:
                raise Exception("INFO","FAILED navigate to edit entry: '" + nameValue)

        elif navigateTo == enums.Location.MY_MEDIA:
            if self.myMedia.navigateToMyMedia(forceNavigate) == False:
                raise Exception("INFO","FAILED navigate to my media")
        
        elif navigateTo == enums.Location.CHANNELS_PAGE:
            if self.channel.navigateToChannels() == False:
                raise Exception("INFO","FAILED navigate to Channels page")
            
        elif navigateTo == enums.Location.MY_CHANNELS_PAGE:
            if self.channel.navigateToMyChannels() == False:
                raise Exception("INFO","FAILED navigate to my Channels")
            
        elif navigateTo == enums.Location.CHANNEL_PAGE:
            if self.channel.navigateToChannel(nameValue, navigateFrom) == False:
                raise Exception("INFO","FAILED navigate to Channel: " + nameValue)
            
        elif navigateTo == enums.Location.MY_PLAYLISTS:
            if self.myPlaylists.navigateToMyPlaylists(forceNavigate) == False:
                raise Exception("INFO","FAILED navigate to my Playlists")

        elif navigateTo == enums.Location.CATEGORY_PAGE:
            if self.category.navigateToCategory(nameValue) == False:
                raise Exception("INFO","FAILED navigate to Category: " + str(nameValue))

        elif navigateTo == enums.Location.MY_HISTORY:
            if self.myHistory.navigateToMyHistory(forceNavigate) == False:
                raise Exception("INFO","FAILED navigate to my history")
            
        elif navigateTo == enums.Location.HOME:
            if self.myHistory.navigateToHomePage(forceNavigate) == False:
                raise Exception("INFO","FAILED navigate to home page")        
                                                            
        return True 
    
    
    # @Author: Inbar Willman
    def writeToFile(self, path, text):
        try:
            file1 = open(path,"w")
            file1.write(text)
            file1.close()
        except:
            writeToLog("INFO","FAILED to write file: " + path + "; Text: " + text)
            return False
        return True
    
    
    # @Author: Oleg Sigalov
    def deleteFile(self, path):
        try:
            os.remove(path)
        except:
            writeToLog("INFO","FAILED to delete file: " + path)
            return False
        return True        
        
        
    # @Author: Oleg Sigalov
    # Use ONLY for linux    
    def createFolder(self, path):
        try:     
            os.makedirs(path)
            writeToLog("INFO","Created folder: " + path)
        except:
            writeToLog("INFO","FAILED to create folder: " + path)
            return False
        return True
    
    
    # @Author: Oleg Sigalov
    # Use ONLY for linux    
    def deleteFolder(self, path):
        try:     
            shutil.rmtree(path)
            writeToLog("INFO","Deleted folder: " + path)
        except:
            writeToLog("INFO","FAILED to delete folder: " + path)
            return False
        return True            
    
    
    # @Author: Oleg Sigalov
    # leavePageExpected=True if the test may fail somewhere, and Leave Page may appear.
    # we need to click leave page, because it will not continue to tearDown and other tests...
    def handleTestFail(self, status, leavePageExpected=False):
        self.switch_to_default_iframe_generic()
        if status == "Fail":
            self.base.takeScreeshotGeneric('LAST_SCRENNSHOT')
            if leavePageExpected==True:
                # Try to navigate to any place to show leave page if it was not visible
                self.base.navigate(localSettings.LOCAL_SETTINGS_TEST_BASE_URL)
                # Try to click leave page if already present
                self.base.click_leave_page()
        return True
    
                    
    # @Author: Oleg Sigalov
    # Switch to default Media Space Iframe, if testing Media Space it will switch to default_content
    # If testing KAF, it will switch to KAF Media Space Iframe
    def switch_to_default_iframe_generic(self):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MEDIA_SPACE:
            return self.base.switch_to_default_content() 
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            return self.blackBoard.switchToBlackboardIframe()
        else:
            self.base.switch_to_default_content()
            
            
    def sendKeysToBodyElement(self, keys):
        self.base.send_keys_to_element(self.base.get_body_element(), keys)
        return True
    
    
    # Check which search bar do we have: old or new (elastic)
    def isElasticSearchOnPage(self):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
                return True
            if len(self.base.get_elements(self.myMedia.MY_MEDIA_ELASTIC_SEARCH_BAR)) > 1:
                return True
            else:
                return False
        else:
            return False
        
        
    # @Author: Inbar Willman
    # Compare between two files binary
    def compareBetweenTwoFilesBinary(self, path1, path2): 
        # Compare between two files
        if filecmp.cmp(path1, path2) == False:
            writeToLog("INFO","FAILED to find match between two files")
            return False      
        else:
            writeToLog("INFO","Two files are identical (binary)")
        return True      
