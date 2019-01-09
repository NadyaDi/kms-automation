from base import *
from general import General
import localSettings
from logger import *
from _ast import Is
from selenium.webdriver.common.keys import Keys
import enums


class Jive(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                                = ('xpath', "//input[contains(@id,'username')]")
    LOGIN_PASSWORD_FIELD                                = ('xpath', "//input[contains(@id,'password')]")
    LOGIN_SIGN_IN_BTN                                   = ('xpath', "//input[@id='login-submit']")
    USER_MENU_TOGGLE_BTN                                = ('xpath', "//span[@class='j-user-name j-navLabel']")
    USER_LOGOUT_BTN                                     = ('xpath', "//a[@id='jive-nav-link-logout' and contains(text(), 'Log out')]")
    JIVE_MEDIA_SPACE_IFRAME                             = ('xpath', "//iframe[contains(@src,'kaltura.com/hosted/index/')]")
    JIVE_MY_MEIDA_BUTTON_IN_MENU                        = ('xpath', "//a[@id='kaltura-nav-link-my-media' and contains(text(), 'My Media')]")
    JIVE_PLACES_BUTTON_IN_NAVIGATION_BAR                = ('xpath', "//a[@href='/places' and contains(@class, 'j-globalNavLink')]")
    JIVE_MEDIA_GALLEY_NEW1_IN_PLACES                    = ('xpath', "//span[@class='js-header-text' and contains(text(), 'New1')]")
    
    JIVE_USER_NAME                                       = ('xpath', "//span[@class='d2l-navigation-s-personal-menu-text']")
    #====================================================================================================================================
    #====================================================================================================================================
    #                                                           Methods:
    #
    # The use of any method here, switches to blackboard media space Iframe but doesn't return it to default
    # !!! IMPORTENT !!! IMPORTENT !!!  IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!!
    # Before implement any method, please use switchToBlackboardIframe method, before addressing to media space elements
    # because you need to switch to blackboard media space iframe. And...!!! use 'self.switch_to_default_content' (Basic class) method
    # to return to default iframe in the end of use of blackboard media space methods or elements, meaning in the test or other classes.
    #====================================================================================================================================
    def switchToJiveIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.JIVE_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_JIVE
            return True
                   
        if self.wait_visible(self.JIVE_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_JIVE
            return True
        else:
            if self.swith_to_iframe(self.JIVE_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
           
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_JIVE
        return True

  
    def loginToJive(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
#             self.clsCommon.login.navigateToLoginPage(url)
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            self.click(self.LOGIN_SIGN_IN_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            # Verify logged in
            if self.wait_element(self.USER_MENU_TOGGLE_BTN, timeout=30) == False:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
            else:
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                return True
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
            
         
    def logOutOfJive(self):
        # Click on the user menu button
        if self.click(self.USER_MENU_TOGGLE_BTN) == False:
            writeToLog("INFO","FAILED to click on user menu button")
            return False
        
        # Click on logout button
        if self.click(self.USER_LOGOUT_BTN) == False:
            writeToLog("INFO","FAILED to click on user menu button")
            return False
        
        # Verify login button is visible
        if self.wait_visible(self.LOGIN_SIGN_IN_BTN, 10) == False:
            writeToLog("INFO","FAILED verify user was logout")
            return False
         
        writeToLog("INFO","Success user was logout")   
        return True
    
    
    # Author: Michal Zomper
    def navigateToGalleryJive(self, galleryName, forceNavigate=False):
        if forceNavigate == False:
            if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
                writeToLog("INFO","Success Already in gallery page")
                return True
        
        if galleryName == "New1":
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to courses 'New1'")
                return False
        sleep(5)
        self.switchToJiveIframe()
        if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        
        return True
        
           
#     def getJiveLoginUserName(self):
#         try:
#             userName = self.get_element_text(self.D2L_USER_NAME)
#         except NoSuchElementException:
#             writeToLog("INFO","FAILED to get user name element")
#             return False
#         return userName.lower() 
#         