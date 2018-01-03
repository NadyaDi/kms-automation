# import inspect
from base import *
# from logger import *
# import localSettings



class Login(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #=============================================================================================================
    #Login XPATH locators:
    #=============================================================================================================
    LOGIN_USERNAME_FIELD                = ('id', 'Login-username')
    LOGIN_PASSWORD_FIELD                = ('id', 'Login-password')
    LOGIN_SIGN_IN_BTN                   = ('id', 'Login-login')
    USER_MENU_TOGGLE_BTN                = ('id', 'userMenuToggleBtn')
    #============================================================================================================
    
    def loginToKMS(self, username, password):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
            self.navigateToLoginPage()
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            self.click(self.LOGIN_SIGN_IN_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            el = self.get_element_text(self.USER_MENU_TOGGLE_BTN)
            if el != 'Guest':
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                # Get the username after login and set the variable. Will need this it some tests
                localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN = el
                return True
            else:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
        
    def navigateToLoginPage(self):
        self.navigate(localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL)
        self.clsCommon.myMedia.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL, False)        