from base import *
from general import General
import localSettings
from logger import *
from _ast import Is
from selenium.webdriver.common.keys import Keys
import enums


class Moodle(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                                = ('id', 'username')
    LOGIN_PASSWORD_FIELD                                = ('id', 'password')
    LOGIN_SUBMIT_BTN                                    = ('id', 'loginbtn')
    LOGIN_SIGN_IN_BTN                                   = ('xpath', "//a[contains(text(), 'Log in')]")
    USER_MENU_TOGGLE_BTN                                = ('xpath', "//span[@class='userbutton']")
    USER_LOGOUT_BTN                                     = ('xpath', "//span[contains(@id,'actionmenuaction') and  contains(text(), 'Log out')]")
    MOODLE_MEDIA_SPACE_IFRAME                           = ('xpath', "//iframe[@id='contentframe']")
    MOODLE_SITE_HOME_BUTTON                             = ('xpath', "//li[@class='type_setting depth_2 contains_branch']")
    MOODLE_MY_MEDIA_BUTTON_IN_NAVIGATION_MENU           = ('xpath', "//span[@class='item-content-wrap' and  contains(text(), 'My Media')]")
    MOODLE_MEDIA_GALLERY_BUTTON_IN_NAVIGATION_MENU      = ('xpath', "//span[@class='item-content-wrap' and  contains(text(), 'Kaltura Media Gallery')]")
    MOODLE_MY_COURSES_BUTTON                            = ('xpath', "//li[@class='type_system depth_2 contains_branch']")
    MOODLE_COURSE_BUTTON_IN_MENU_BAR                    = ('xpath', "//a[@title='New1']")
    MOODLE__MEDIA_GALLERY_TITLE                         = ('xpath', "//h1[contains(text(), 'Kaltura Media Gallery')]")
    #====================================================================================================================================
    #====================================================================================================================================
    #                                                           Methods:
    #
    # The use of any method here, switches to moodle media space Iframe but doesn't return it to default
    # !!! IMPORTENT !!! IMPORTENT !!!  IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!!
    # Before implement any method, please use switchToMoodleIframe method, before addressing to media space elements
    # because you need to switch to moodle media space iframe. And...!!! use 'self.switch_to_default_content' (Basic class) method
    # to return to default iframe in the end of use of moodle media space methods or elements, meaning in the test or other classes.
    #====================================================================================================================================
    def switchToMoodleIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.MOODLE_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_MOODLE
            return True
                    
        if self.wait_visible(self.MOODLE_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_MOODLE
            return True
        else:
            if self.swith_to_iframe(self.MOODLE_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_MOODLE
        return True
            
                
    def loginToMoodle(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
            self.clsCommon.login.navigateToLoginPage(url)
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            self.click(self.LOGIN_SUBMIT_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            el = self.get_element_text(self.USER_MENU_TOGGLE_BTN)
            if username in el:
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                # Get the username after login and set the variable. Will need this it some tests
                #localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN = username
                return True
            else:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_MOODLE")
            raise Exception(inst)
             
          
    def logOutOfMoodle(self):
        # Click on the user menu button
        if self.click(self.USER_MENU_TOGGLE_BTN) == False:
            writeToLog("INFO","FAILED to click on menu button")
            return False
        
        if self.click(self.USER_LOGOUT_BTN) == False:
            writeToLog("INFO","FAILED to click on logout button")
            return False
         
        # Verify login button is visible
        if self.wait_visible(self.LOGIN_SIGN_IN_BTN, 10) == False:
            writeToLog("INFO","FAILED verify user was logout")
            return False
          
        writeToLog("INFO","Success user was logout")   
        return True
     
     
 # Author: Michal Zomper
    def navigateToGalleryMoodle(self, galleryName, forceNavigate=False):
        self.clsCommon.base.switch_to_default_content()
        if forceNavigate == False:
            if self.wait_element(self.MOODLE__MEDIA_GALLERY_TITLE, 5) != False:
                writeToLog("INFO","Success Already in my Gallery page")
                self.clsCommon.moodle.switchToMoodleIframe()
                return True
        
        if galleryName == "New1":
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to courses 'New1'")
                return False
        self.wait_element(self.clsCommon.channel.CHANNEL_ACTION_BUTTON, timeout=20)
        
        if self.wait_element(self.MOODLE__MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        self.clsCommon.moodle.switchToMoodleIframe()
        return True
            