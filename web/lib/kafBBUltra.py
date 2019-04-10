from base import *
from general import General
import localSettings
from logger import *
from _ast import Is
from selenium.webdriver.common.keys import Keys
import enums


class BlackBoardUltra(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                                = ('id', 'user_id')
    LOGIN_PASSWORD_FIELD                                = ('id', 'password')
    LOGIN_SIGN_IN_BTN                                   = ('id', 'entry-login')
    USER_LOGOUT_BTN                                     = ('xpath', "//span[@class='link-text' and contains(text(), 'Sign Out')]")
    COURSES_TAB_MENU                                    = ('xpath', "//span[@class='link-text' and contains(text(), 'Courses')]")
    COURSES_LIST_PAGE                                   = ('xpath', "//h4[@class='ellipsis' and @title='New1']")
    BB_ULTRA_MEDIA_SPACE_IFRAME                         = ('xpath', "//iframe[@id='lti-launch-iframe']")
    BB_ULTRA_USER_NAME                                  = ('xpath', "//bdi[contains(text(), 'USER_NAME')]")
    BB_ULTRA_PRIVECY_TURMS_BUTTON                       = ('xpath', "//button[@id='agree_button']")    
    BB_ULTRA_MY_MEDIA_BUTTON_IN_TOOLS_MENU              = ('xpath', "//span[@class='tool-title' and @title='Automation my media']")
    BB_ULTRA_MEDIA_GALLERY_BUTTON_IN_COURSE             = ('xpath', "//span[text()='New1']/ancestor::a[@class='content-title']")
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
    def switchToBlackboardUltraIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.BB_ULTRA_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_ULTRA
            return True
                     
        if self.wait_visible(self.BB_ULTRA_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_ULTRA
            return True
        else:
            if self.swith_to_iframe(self.BB_ULTRA_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
             
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_ULTRA
        return True
    
                
    def loginToBlackBoardUltra(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
            if self.click(self.BB_ULTRA_PRIVECY_TURMS_BUTTON) == False:
                writeToLog("INFO","FAILED to click on agree terms button")
                return False                
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            self.click(self.LOGIN_SIGN_IN_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            sleep(4)
            tmp_user = (self.BB_ULTRA_USER_NAME[0], self.BB_ULTRA_USER_NAME[1].replace('USER_NAME', username))
            if self.wait_element(tmp_user, 30) == False:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
            else:
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                # Get the username after login and set the variable. Will need this it some tests
                #localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN = username
                return True

        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
             
          
    def logOutOfBlackBoardUltra(self):
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
     
     
    # Author: Michal Zomper
    def navigateToMyMediaBlackboardUltra(self):
        self.clsCommon.base.switch_to_default_content()
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
            writeToLog("INFO","FAILED navigate to my media page")
            return False
        
        if self.click(self.BB_ULTRA_MY_MEDIA_BUTTON_IN_TOOLS_MENU) == False:
            writeToLog("INFO","FAILED to click on my media button")
            return False
        sleep(4)
        self.switchToBlackboardUltraIframe()
        if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_TITLE, timeout=30) == False:
            writeToLog("INFO","FAILED navigate to My Media")
            return False
        
        return True  
     
     
    # Author: Oded Berihon
    def navigateToGalleryBlackBoardUltra(self, galleryName, forceNavigate=False):
        if forceNavigate == False:
            if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
#             self.switchToBlackboardUltraIframe()
#             if self.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","Success Already in my Gallery page")
                return True
        sleep(2)   
        
        if galleryName == "New1":
            if self.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","Success Already in my Gallery page")
                return False  
            sleep(5)   
                     
            if self.click(self.COURSES_TAB_MENU)== False:
                writeToLog("INFO","Success Already in my Gallery page")
                return False
            sleep(5) 
             
            if self.click(self.COURSES_LIST_PAGE)== False:
                writeToLog("INFO","Success Already in my Gallery page")
                return False
        sleep(5)
         
        self.switchToBlackboardUltraIframe()
        if self.click(self.BB_ULTRA_MEDIA_GALLERY_BUTTON_IN_COURSE) == False:
            writeToLog("INFO","FAILED to click on media gallery button")
            return False
         
        return True
        
    
#     def getBlackboardUltraLoginUserName(self):
#         try:
#             userName = self.get_element_text(self.BB_USER_NAME)
#         except NoSuchElementException:
#             writeToLog("INFO","FAILED to get user name element")
#             return False
#         return userName   
    
    