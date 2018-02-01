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
from upload import Upload
from myPlaylists import MyPlaylists



    #============================================================================================================
    # The class contains functions that relates to common actions
    #============================================================================================================
class Common():
    # Parameters
    driver = None
     
    # Module
    base            = None
    autoit          = None
    admin           = None
    login           = None
    upload          = None
    general         = None
    myMedia         = None
    entryPage       = None
    editEntryPage   = None
    category        = None
    channel         = None
    MyPlaylists     = None
    
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
        
    #=============================================================================================================
    # Locators:
    #=============================================================================================================
      
     
    #============================================================================================================
    # Common Methods
    #============================================================================================================
    def instertPathInFileUploadWindows(self, path):
        self.autoit.autoitDriver.execute_script(localSettings.LOCAL_SETTINGS_REMOTE_KMS_WEB_DIR + r'autoit\openFile.exe', path)
        
        
    def loginAsUser(self):
        return self.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)