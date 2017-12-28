import localSettings
from logger import *

from base import Base
from login import Login
from upload import Upload
from general import General
from myMedia import MyMedia
from entryPage import EntryPage


    #============================================================================================================
    # The class contains functions that relates to common actions
    #============================================================================================================
    
class Common():
    # Parameters
    driver = None
     
    # Module
    base    = None
    login   = None
    upload  = None
    general = None
    myMedia = None
    
    def __init__(self, driver):
        self.base           = Base(driver)
        self.driver         = driver
        self.login          = Login(self, driver)
        self.upload         = Upload(self, driver)
        self.general        = General(self, driver)
        self.myMedia        = MyMedia(self, driver)
        self.entryPage      = EntryPage(self, driver)
    #=============================================================================================================
    # Locators:
    #=============================================================================================================
      
     
    #============================================================================================================
    # Common Methods
    #============================================================================================================
    def loginAsUser(self):
        return self.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)