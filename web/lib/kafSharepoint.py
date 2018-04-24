from base import *
from general import General
import localSettings
from logger import *
from upload import Upload


class SharePoint(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                = ('xpath', "//input[@name='loginfmt']")
    LOGIN_NEXT_BUTTON                   = ('xpath', "//input[@type='submit']")
    LOGIN_PASSWORD_FIELD                = ('xpath', "//input[@name='passwd']")
    LOGIN_NO_BUTTON                     = ('xpath', "//input[@id='idBtn_Back']")
    USER_MENU_TOGGLE_BTN                = ('id', 'DeltaPlaceHolderPageTitleInTitleArea')
    USER_LOGOUT_BTN                     = ('id', 'topframe.logout.label')
    SP_MEDIA_SPACE_IFRAME               = ('xpath', "//iframe[contains(@src,'kalturasp2013.sharepoint.com')]")
    #====================================================================================================================================
    #====================================================================================================================================
    #                                                           Methods:
    #
    # The use of any method here, switches to Sharepoint media space Iframe but doesn't return it to default
    # !!! IMPORTENT !!! IMPORTENT !!!  IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!!
    # Before implement any method, please use switchToSharepointIframe method, before addressing to media space elements
    # because you need to switch to Sharepoint media space iframe. And...!!! use 'self.switch_to_default_content' (Basic class) method
    # to return to default iframe in the end of use of Sharepoint media space methods or elements, meaning in the test or other classes.
    #====================================================================================================================================
    def switchToSharepointIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.KAF_SHAREPOINT:
            return True
        else:
            if self.wait_visible(self.SP_MEDIA_SPACE_IFRAME, 60) == False:
                writeToLog("INFO","FAILED to get iframe element")
                return False
            if self.swith_to_iframe(self.SP_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_SHAREPOINT
        return True
            
                
    def loginToSharepoint(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
            self.clsCommon.login.navigateToLoginPage(url, False)
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            sleep(1)
            # Click Next
            self.click(self.LOGIN_NEXT_BUTTON)
            sleep(1)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            sleep(1)
            # Click Sign In
            self.click(self.LOGIN_NEXT_BUTTON)
            sleep(1)
            # Wait page load
            self.wait_for_page_readyState()
            # Check if 'Stay signed in?' appeared, and click No, if appeared
            self.click(self.LOGIN_NO_BUTTON, 10)
            # Verify logged in
            el = self.get_element_text(self.USER_MENU_TOGGLE_BTN).strip()
            if el in username:
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
            
         
    def logOutOfSharepoint(self):
        # Click on the user menu button
        if self.click(self.USER_LOGOUT_BTN) == False:
            writeToLog("INFO","FAILED to click on logout button")
            return False
        
        # Verify login button is visible
        if self.wait_visible(self.LOGIN_SIGN_IN_BTN, 10) == False:
            writeToLog("INFO","FAILED verify user was logout")
            return False
         
        writeToLog("INFO","Success user was logout")   
        return True
    
    
    def navigateToUploadPageSharePoint(self):
        if self.navigateToMyMediaSharepoint() == False:
            return False
        if self.switchToSharepointIframe() == False:
            return False
        return True
    
    def navigateToMyMediaSharepoint(self):
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
            writeToLog("INFO","FAILED navigate to My Media")
            return False

        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 30) == False:
            writeToLog("INFO","FAILED navigate to My Media")
            return False
        
        return True