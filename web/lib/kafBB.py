from base import *
from general import General
import localSettings
from logger import *
from upload import Upload


class BlackBoard(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                = ('id', 'user_id')
    LOGIN_PASSWORD_FIELD                = ('id', 'password')
    LOGIN_SIGN_IN_BTN                   = ('id', 'entry-login')
    USER_MENU_TOGGLE_BTN                = ('id', 'global-nav-link')
    USER_LOGOUT_BTN                     = ('id', 'topframe.logout.label')
    BB_MEDIA_SPACE_IFRAME               = ('xpath', "//iframe[contains(@src,'/webapps/osv-kaltura-BBLEARN/')]")
    KAF_MEDIA_GALLERY_TITLE             = ('xpath', "//h1[@id='channel_title' and text()='Media Gallery']")
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
    def switchToBlackboardIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.BB_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD
            return True
                    
        if self.wait_visible(self.BB_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD
            return True
        else:
            if self.swith_to_iframe(self.BB_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD
        return True
            
                
    def loginToBlackBoard(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
            self.clsCommon.login.navigateToLoginPage(url)
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
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
            
         
    def logOutOfBlackBoard(self):
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
    
    
    def navigateToUploadPageBlackBoard(self):
        if self.navigateToMyMediaBlackBoard() == False:
            return False
        if self.switchToBlackboardIframe() == False:
            return False
        return True
    
    def navigateToMyMediaBlackBoard(self):
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
            writeToLog("INFO","FAILED navigate to My Media")
            return False
        
        sleep(2)
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 30) == False:
            writeToLog("INFO","FAILED navigate to My Media")
            return False
        
        if self.switchToBlackboardIframe() == False:
            return False
        
        return True
    
    
    def navigateToGalleryBB(self, galleryName):
        if self.wait_visible(self.KAF_MEDIA_GALLERY_TITLE, 5) != False:
            writeToLog("INFO","Success Already in my Gallery page")
            return True
        
        if galleryName == "New1":
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to courses 'New1'")
                return False
        sleep(5)
        
        self.clsCommon.blackBoard.switchToBlackboardIframe()
        if self.wait_visible(self.KAF_MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        
        return True
        
        
    def navigateToEntryPageFromBBGalleryPage(self, entryName, galleryName):
        tmpEntryName = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmpEntryName, 5) != False:
            writeToLog("INFO","Already in entry page: '" + entryName + "'")
            return True
        
        if self.navigateToGalleryBB(galleryName) == False:
            writeToLog("INFO","FAILED navigate to gallery:" + galleryName)
            return False             
        sleep(2)
           
        if self.clsCommon.channel.searchEntryInChannel(entryName) == False:
            writeToLog("INFO","FAILED to search entry'" + entryName + "' in gallery" + galleryName)
            return False  
            
        # click on the entry
        if self.clsCommon.myMedia.clickResultEntryAfterSearch(entryName) == False:
            writeToLog("INFO","FAILED to click on entry " + entryName)
            return False 
        
        if self.wait_visible(tmpEntryName, 15) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
           
        return True