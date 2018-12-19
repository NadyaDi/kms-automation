from base import *
from general import General
import localSettings
from logger import *
from _ast import Is
from selenium.webdriver.common.keys import Keys
import enums


class Canvas(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                                = ('id', 'pseudonym_session_unique_id')
    LOGIN_PASSWORD_FIELD                                = ('id', 'pseudonym_session_password')
    LOGIN_SUBMIT_BTN                                    = ('xpath', "//button[@class='Button Button--login']")
    USER_NAVIGATION_MENU_BAR                            = ('xpath', "//div[@class='ic-app-header__main-navigation']")
    USER_ACCOUNT_BUTTON_IN_NAV_BAR                      = ('xpath', "//a[@id='global_nav_profile_link']")
    USER_LOGOUT_BTN                                     = ('xpath', "//button[@type='submit']")
    CANVAS_MEDIA_SPACE_IFRAME                           = ('xpath', "//iframe[@id='tool_content']")
    CANVAS_MY_MEDIA_BUTTON_IN_NAV_BAR                   = ('xpath', "//a[contains(@class, 'ontext_external_tool') and @title='My Media']")
    CANVAS_MEDIA_GALLERY_BUTTON_IN_NAV_BAR              = ('xpath', "//a[contains(@class, 'ontext_external_tool') and @title='Media Gallery']")
    #====================================================================================================================================
    #====================================================================================================================================
    #                                                           Methods:
    #
    # The use of any method here, switches to canvas media space Iframe but doesn't return it to default
    # !!! IMPORTENT !!! IMPORTENT !!!  IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!!
    # Before implement any method, please use switchToMoodleIframe method, before addressing to media space elements
    # because you need to switch to canvas media space iframe. And...!!! use 'self.switch_to_default_content' (Basic class) method
    # to return to default iframe in the end of use of canvas media space methods or elements, meaning in the test or other classes.
    #====================================================================================================================================
    def switchToCanvasIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.CANVAS_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_MOODLE
            return True
                     
        if self.wait_visible(self.CANVAS_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_MOODLE
            return True
        else:
            if self.swith_to_iframe(self.CANVAS_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
             
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_MOODLE
        return True
            
                
    def loginToCanvas(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
            #self.clsCommon.login.navigateToLoginPage(url)
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            self.click(self.LOGIN_SUBMIT_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            if self.wait_element(self.USER_NAVIGATION_MENU_BAR, timeout=20) == False:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False

            else:
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                return True
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_CANVAS")
            raise Exception(inst)
             
          
    def logOutOfCanvas(self):
        # Click on account button in main nav bar 
        if self.click(self.USER_ACCOUNT_BUTTON_IN_NAV_BAR) == False:
            writeToLog("INFO","FAILED to click on account button in main nav bar ")
            return False
        
        if self.click(self.USER_LOGOUT_BTN) == False:
            writeToLog("INFO","FAILED to click on logout button")
            return False
         
        # Verify login button is visible
        if self.wait_visible(self.LOGIN_SUBMIT_BTN, 10) == False:
            writeToLog("INFO","FAILED verify user was logout")
            return False
          
        writeToLog("INFO","Success user was logout")   
        return True
     
     
    # Author: Michal Zomper
    def navigateToMyMediaCanvas(self):
        self.switchToCanvasIframe()
        if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_TITLE, 5) != False:
            writeToLog("INFO","Success Already in my Gallery page")
            return True
        
        self.clsCommon.base.switch_to_default_content()
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
            writeToLog("INFO","FAILED navigate to course page")
            return False
        
        if self.click(self.CANVAS_MY_MEDIA_BUTTON_IN_NAV_BAR) == False:
            writeToLog("INFO","FAILED to click on my media button")
            return False
        
        self.switchToCanvasIframe()
        if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_TITLE, timeout=15) == False:
            writeToLog("INFO","FAILED navigate to My Media")
            return False
        
        return True   
         
     
     
    # Author: Michal Zomper
    def navigateToGalleryCanvas(self, forceNavigate=False):
        if forceNavigate == False:
            self.switchToCanvasIframe()
            if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
                writeToLog("INFO","Success Already in my Gallery page")
                return True
        
        self.clsCommon.base.switch_to_default_content()
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
            writeToLog("INFO","FAILED navigate to courses")
            return False
        
        if self.click(self.CANVAS_MEDIA_GALLERY_BUTTON_IN_NAV_BAR) == False:
            writeToLog("INFO","FAILED to click on media gallery button")
            return False 
           
        self.switchToCanvasIframe()
        if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to course Media Gallery")
            return False
         
        return True
     
    
    
