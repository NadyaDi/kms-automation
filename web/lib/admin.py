from base import *
import clsTestService
from logger import writeToLog


class Admin(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #My Media locators:
    #=============================================================================================================
    #=============================================================================================================
    def navigateToAdminPage(self):
        adminUrl = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/admin'
        if self.navigate(adminUrl) == False:
            writeToLog("INFO","FAILED to load Admin page: '" + adminUrl + "'")
            return False
                    
        if self.clsCommon.myMedia.verifyUrl(adminUrl, False) == False:
            return False
        else:
            return True
              
              
    def loginToAdminPage(self):
        if self.navigateToAdminPage() == False:
            return False
        
        # Enter test partner username
        if self.send_keys(self.clsCommon.login.LOGIN_USERNAME_FIELD, localSettings.LOCAL_SETTINGS_ADMIN_USERNAME) == False:
            writeToLog("INFO","FAILED to enter username")
            return False 
                   
        # Enter test partner password
        if self.send_keys(self.clsCommon.login.LOGIN_PASSWORD_FIELD, localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD) == False:
            writeToLog("INFO","FAILED to enter password")
            return False
        
        # Click Sign In
        if self.click(self.clsCommon.login.LOGIN_SIGN_IN_BTN) == False:
            writeToLog("INFO","FAILED to click on Sign In button")
            return False
        
        # Wait page load
        self.wait_for_page_readyState()
        return True
        
                      
#     def adminEnableCollaboration(self):
# https://2307831.qakmstest.dev.kaltura.com/admin/config/tab/mediaCollaboration#mediaCollaborationEnabled