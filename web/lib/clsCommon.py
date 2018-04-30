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
        ### KAF ###
        self.blackBoard         = BlackBoard(self, driver)
        self.sharePoint         = SharePoint(self, driver)
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
        file1 = open(path,"w")
        file1.write(text)
        file1.close()
        
        
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
        