from base import Base
from admin import Admin
from editEntryPage import EditEntryPage
from entryPage import EntryPage
from general import General
import localSettings
from logger import *
from login import Login
from myMedia import MyMedia
from upload import Upload
from category import Category
from channel import Channel


    #============================================================================================================
    # The class contains functions that relates to common actions
    #============================================================================================================
class Common():
    # Parameters
    driver = None
     
    # Module
    base            = None
    admin           = None
    login           = None
    upload          = None
    general         = None
    myMedia         = None
    entryPage       = None
    editEntryPage   = None
    category        = None
    channel         = None
    
    def __init__(self, driver):
        self.driver             = driver        
        self.base               = Base(driver)
        self.admin              = Admin(self, driver)
        self.login              = Login(self, driver)
        self.upload             = Upload(self, driver)
        self.general            = General(self, driver)
        self.myMedia            = MyMedia(self, driver)
        self.entryPage          = EntryPage(self, driver)
        self.editEntryPage      = EditEntryPage(self, driver)
        self.category           = Category(self, driver)
        self.channel            = Channel(self, driver)
        
    #=============================================================================================================
    # Locators:
    #=============================================================================================================
      
     
    #============================================================================================================
    # Common Methods
    #============================================================================================================
    def loginAsUser(self):
        return self.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)