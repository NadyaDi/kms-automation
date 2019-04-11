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
    LOGIN_USERNAME_FIELD                            = ('xpath', "//input[@name='loginfmt']")
    LOGIN_NEXT_BUTTON                               = ('xpath', "//input[@type='submit']")
    LOGIN_PASSWORD_FIELD                            = ('xpath', "//input[@name='passwd']")
    LOGIN_NO_BUTTON                                 = ('xpath', "//input[@id='idBtn_Back']")
    LOGIN_USE_ANOTHER_ACCOUNT_BUTTON                = ('xpath', "//div[@id='otherTileText']")
    USER_MENU_TOGGLE_BTN                            = ('id', 'DeltaPlaceHolderPageTitleInTitleArea')
    USER_LOGOUT_BTN                                 = ('xpath', "//a[contains(@id,'SignoutLink') and contains(text(), 'Sign out')]")
    SP_MEDIA_SPACE_IFRAME                           = ('xpath', "//iframe[contains(@src,'kalturasp2013.sharepoint.com')]")
    SP_PAGE_TITLE_IN_SP_IFRAME                      = ('xpath', "//div[contains(@class,'pageTitle_')]")
    SP_MY_MEDIA_BUTTON_IN_NAV_MENU                  = ('xpath', "//a[contains(@href, '/My Media.aspx') and @title='My Media']")
    SP_NEW1_MEDIA_GALLERY_BUTTON_IN_NAV_MENU        = ('xpath', "//a[contains(@href, '/Media Gallery.aspx') and @title='New1']")
    SP_USER_ACCOUNT_BUTTON                          = ('xpath', "//button[@id='O365_MainLink_Me']")
    SP_USER_NAME                                    = ('xpath', "//span[@class='otFsDF8X99BQFKkxYU2A7 o365sx-neutral-dark-font']")
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
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.SP_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_SHAREPOINT
            return True
                    
        if self.wait_visible(self.SP_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_SHAREPOINT
            return True
        else:
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
            sleep(1)
            # look to see login user name display on we need to click on 'use another account'
            if self.wait_visible(self.LOGIN_USERNAME_FIELD, timeout=5) == False:
                # click on 'use another account'
                if self.click(self.LOGIN_USE_ANOTHER_ACCOUNT_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on use another account button")
                    return False
                self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            else:
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
            if self.wait_element(self.SP_USER_ACCOUNT_BUTTON, timeout=20) == False:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
            else:
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                return True
            
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
            
         
    def logOutOfSharepoint(self):
        # Click on the user menu button
        if self.click(self.SP_USER_ACCOUNT_BUTTON, timeout=15) == False:
            writeToLog("INFO","FAILED to click on user menu button")
            return False

        if self.click(self.USER_LOGOUT_BTN) == False:
            writeToLog("INFO","FAILED to click on logout button")
            return False
         
        writeToLog("INFO","Success user was logout")   
        return True
    
    
        # Author: Michal Zomper
    def navigateToGallerySharePoint(self, galleryName, forceNavigate=False):
        if forceNavigate == False:
            self.switchToSharepointIframe()
            if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
                writeToLog("INFO","Success Already in gallery page")
                return True
        
        self.clsCommon.base.switch_to_default_content()
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
            writeToLog("INFO","FAILED navigate to courses")
            return False
        sleep(5)
           
        self.switchToSharepointIframe()
        if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to course Media Gallery")
            return False
         
        return True
    
    
    def getSharePointLoginUserName(self):
        if self.click(self.SP_USER_ACCOUNT_BUTTON, timeout=15) == False:
            writeToLog("INFO","FAILED to click on user menu button")
            return False
        
        try:
            userName = self.get_element_text(self.SP_USER_NAME)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get user name element")
            return False
        self.click(self.SP_USER_ACCOUNT_BUTTON, timeout=15)
        return userName