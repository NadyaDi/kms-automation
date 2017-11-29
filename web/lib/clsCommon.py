from base import Base
import localSettings
from logger import *
from login import Login


class Common(Base):
    # Parameters
    driver = None
     
    # Module
    login = None
     
    def __init__(self, driver):
        self.driver         = driver
        self.login          = Login(self.driver)  
    #=============================================================================================================
    # Locators:
    #=============================================================================================================
      
    #============================================================================================================
    # The class contains functions that relates to common actions
    #============================================================================================================
     
    #============================================================================================================
    def loginAsUser(self):
        return self.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)