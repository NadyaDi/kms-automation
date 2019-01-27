from base import *
from general import General
import localSettings
from logger import *
from _ast import Is
from selenium.webdriver.common.keys import Keys
import enums


class Sakai(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                                = ('xpath', "//input[contains(@id,'eid')]")
    LOGIN_PASSWORD_FIELD                                = ('xpath', "//input[contains(@id,'pw')]")
    LOGIN_SIGN_IN_BTN                                   = ('xpath', "//input[@id='submit']")
    USER_MENU_TOGGLE_BTN                                = ('xpath', "//span[@class='j-user-name j-navLabel']")
    USER_LOGOUT_BTN                                     = ('xpath', "//a[contains(@id,'loginLink') and contains(text(), 'Logout')]")
    SAKAI_MEDIA_SPACE_IFRAME                            = ('xpath', "//iframe[@class='portletMainIframe']")
    SAKAI_NEW1_GALLERY_IN_NAV_BAR                       = ('xpath', "//a[@title='New1' and @role='menuitem']")
    SAKAI_MY_MEIDA_BUTTON_IN_MENU                       = ('xpath', "//span[@class='menuTitle' and contains(text(), 'My Media')]")
    SAKAI_MEDIA_GALLERY_BUTTON_IN_MENU                  = ('xpath', "//span[@class='menuTitle' and contains(text(), 'Media Gallery')]")
#     JIVE_MEDIA_GALLEY_NEW1_IN_PLACES                    = ('xpath', "//span[@class='js-header-text' and contains(text(), 'New1')]")
#     JIVE_USER_NAME                                      = ('xpath', "//span[@class='j-user-name j-navLabel']")
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
    def switchToSakaiIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.SAKAI_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_SAKAI
            return True
                   
        if self.wait_visible(self.SAKAI_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_SAKAI
            return True
        else:
            if self.swith_to_iframe(self.SAKAI_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
           
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_SAKAI
        return True

  
    def loginToSakai(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            self.click(self.LOGIN_SIGN_IN_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            if self.wait_element(self.USER_LOGOUT_BTN, timeout=30) == False:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
            else:
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                return True
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
            
         
    def logOutOfSakai(self):
        self.clsCommon.base.switch_to_default_content()
        # Click on logout button
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
    def navigateToMyMediaSakai(self, forceNavigate=False):
        if forceNavigate == False:
            if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_PAGE_TITLE, 5) != False:
                writeToLog("INFO","Success Already in gallery page")
                return True
        
        self.refresh()
        self.clsCommon.base.switch_to_default_content()
        if self.click(self.SAKAI_NEW1_GALLERY_IN_NAV_BAR, 15) == False:
            writeToLog("INFO","FAILED to click on courses 'New1' in nav bar")
            return False
        
        if self.click(self.SAKAI_MY_MEIDA_BUTTON_IN_MENU, 15) == False:
            writeToLog("INFO","FAILED to click on 'My Media' button in menu")
            return False
        sleep(5)
        
        self.switchToSakaiIframe()
        if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_PAGE_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate my media")
            return False
        
        return True
    
    # Author: Michal Zomper
    def navigateToGallerySakai(self, galleryName, forceNavigate=False):
        if forceNavigate == False:
            if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
                writeToLog("INFO","Success Already in gallery page")
                return True
        
        self.refresh()
        self.clsCommon.base.switch_to_default_content()
        if galleryName == "New1":
            if self.click(self.SAKAI_NEW1_GALLERY_IN_NAV_BAR, 15) == False:
                writeToLog("INFO","FAILED to click on courses 'New1' in nav bar")
                return False
        
            if self.click(self.SAKAI_MEDIA_GALLERY_BUTTON_IN_MENU, 15) == False:
                writeToLog("INFO","FAILED to click on 'Media Galley' button in menu")
                return False
        
        sleep(5)
        self.switchToSakaiIframe()
        if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 30) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
         
        return True
#         
#            
#     def getSakaiLoginUserName(self):
#         try:
#             userName = self.get_element_text(self.JIVE_USER_NAME)
#         except NoSuchElementException:
#             writeToLog("INFO","FAILED to get user name element")
#             return False
#         return userName.lower() 
