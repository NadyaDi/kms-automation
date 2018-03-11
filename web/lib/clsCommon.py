from admin import Admin
from autoit import Autoit
from base import Base
from category import Category
from channel import Channel
from editEntryPage import EditEntryPage
from entryPage import EntryPage
from general import General
import localSettings
from logger import *
from login import Login
from myMedia import MyMedia
from myPlaylists import MyPlaylists
from player import Player
from upload import Upload
from clsQrCodeReader import QrCodeReader
from myHistory import MyHistory
from kea import Kea
import clsTestService


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

        
    #=============================================================================================================
    # Locators:
    #=============================================================================================================
      
     
    #============================================================================================================
    # Common Methods
    #============================================================================================================
    def instertPathInFileUploadWindows(self, path):
        if (localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_IE):
            # TODO IE not implemented yet
            self.autoit.autoitDriver.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFile.exe', path)
        elif(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_FIREFOX):
            self.autoit.autoitDriver.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFileFirefox.exe', path)
        elif(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
            self.autoit.autoitDriver.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFileChrome.exe', path)
        else:
            writeToLog("INFO","FAILED to type into 'Choose File' window, unknown browser: '" + localSettings.LOCAL_RUNNING_BROWSER + "'")
        
        
        
    def loginAsUser(self):
        return self.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)