from base import *
from general import General
import localSettings
from logger import *
from _ast import Is
from selenium.webdriver.common.keys import Keys
import enums


class D2L(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                                = ('id', 'userName')
    LOGIN_PASSWORD_FIELD                                = ('id', 'password')
    LOGIN_SIGN_IN_BTN                                   = ('xpath', "//button[@class='d2l-button' and contains(text(), 'Log In')]")
    USER_MENU_TOGGLE_BTN                                = ('xpath', "//span[@class='d2l-navigation-s-personal-menu-text']")
    USER_LOGOUT_BTN                                     = ('xpath', "//a[contains(@class,'d2l-link d2l') and contains(text(), 'Log Out')]")
    D2L_MEDIA_SPACE_IFRAME                              = ('xpath', "//iframe[contains(@src,'/d2l/lms/remoteplugins/lti/launchLti.d2l')]")
    D2L_SELECT_COURSES_BUTTON                           = ('xpath', "//button[@class='d2l-navigation-s-button-highlight d2l-dropdown-opener']")
    D2L_SELECT_COURSE_NEW1_BUTTON                       = ('xpath', "//a[@class='d2l-link d2l-datalist-item-actioncontrol' and contains(text(), 'New1 - New1')]")
    D2L_HEANDL_ENTRY_WIDGET_IN_ENTRY_PAGE               = ('xpath', "//h2[@class='d2l-heading vui-heading-4']") # in entry page if need to do page down/up us this locator to grab the page
    D2L_USER_NAME                                       = ('xpath', "//span[@class='d2l-navigation-s-personal-menu-text']")
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
    def switchToD2LIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.D2L_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_D2L
            return True
                   
        if self.wait_visible(self.D2L_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_D2L
            return True
        else:
            if self.swith_to_iframe(self.D2L_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
           
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_D2L
        return True

  
    def loginToD2L(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
#             self.clsCommon.login.navigateToLoginPage(url)
            sleep(2)
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            sleep(1)
            # Click Sign In
            self.click(self.LOGIN_SIGN_IN_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            if self.wait_visible(self.USER_MENU_TOGGLE_BTN, timeout=20) == False:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
            else:
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                self.clsCommon.d2l.switchToD2LIframe()
                self.wait_element(self.clsCommon.myMedia.MY_MEDIA_TITLE, timeout=25)
                return True
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
            
         
    def logOutOfD2L(self):
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
    def navigateToGalleryD2L(self, galleryName, forceNavigate=False):
        if forceNavigate == False:
            if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
                writeToLog("INFO","Success Already in Gallery page")
                return True
        
        if galleryName == "New1":
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to courses 'New1'")
                return False
        sleep(5)
        
        self.removeD2LPopupIngallery()
        self.switchToD2LIframe()
        if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        
        return True
        
        
    # Author: Michal Zomper
    def removeD2LPopupIngallery(self):
        self.clsCommon.base.switch_to_default_content()
        self.driver.execute_script("try{var element = document.querySelectorAll('div[data-id=tourorg-1]')[0];element.parentNode.removeChild(element);}catch (e){}")
        self.switchToD2LIframe()
        
    
    def getD2LLoginUserName(self):
        try:
            userName = self.get_element_text(self.D2L_USER_NAME)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get user name element")
            return False
        return userName.lower() 
        