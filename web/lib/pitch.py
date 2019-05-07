from base import *


class Pitch(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                        = ('css','input#email')
    LOGIN_PASSWORD_FIELD                        = ('css','input#password')
    LOGIN_SIGN_IN_BTN                           = ('css','button[type="submit"]')
    USER_MENU_TOGGLE_BTN                        = ('css','span.username.text-smaller.red-dot')
    USER_LOGOUT_BTN                             = ('css','a[href="/logout"]')
    #====================================================================================================================================
    #                                                           Methods:
    #====================================================================================================================================
    # @Author: Oleg Sigalov
    # Perform login with given username and password and verify an element on the landing page (to make sure login was successful)
    def loginToPitch(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
            if self.clsCommon.myMedia.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL)==False:
                self.clsCommon.login.navigateToLoginPage(url)
                
            # Enter username
            if self.send_keys(self.LOGIN_USERNAME_FIELD, username) == False:
                writeToLog("INFO","FAILED to set username: '" + username + "'")
                return False
            
            # Enter password
            if self.send_keys(self.LOGIN_PASSWORD_FIELD, password) == False:
                writeToLog("INFO","FAILED to set password: '" + password + "'")
                return False
            
            # Click Sign In
            if self.click(self.LOGIN_SIGN_IN_BTN) == False:
                writeToLog("INFO","FAILED to click on Sing In")
                return False
            
            # Wait page load
            if self.wait_for_page_readyState() == False:
                writeToLog("INFO","FAILED to login after clicking on 'Sing In' button")
                return False
            
            # Verify logged in - Verify the menu button on the top right corner is visible
            if self.wait_element(self.USER_MENU_TOGGLE_BTN) == False:
                writeToLog("INFO","FAILED to login after clicking on 'Sing In' button")
                return False
            
            return True
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_PITCH")
            return False
            
            
    # @Author: Oleg Sigalov
    # Perform logout by click on logout button from use menu and verify 'Sign In' button after logout (to make sure logout was successful)     
    def logOutPitch(self):
        if self.click(self.USER_MENU_TOGGLE_BTN) == False:
            writeToLog("INFO","FAILED to click on user menu button")
            return False    
                
        # Click on the user menu button
        if self.click(self.USER_LOGOUT_BTN) == False:
            writeToLog("INFO","FAILED to click on logout button")
            return False
        
        # Verify Sign In button is visible
        if self.wait_element(self.LOGIN_SIGN_IN_BTN, 20) == False:
            writeToLog("INFO","FAILED to verify user was logout")
            return False
         
        writeToLog("INFO","Logged out successfully")   
        return True
