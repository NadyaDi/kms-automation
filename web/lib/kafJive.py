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
    JIVE_USER_NAME                                      = ('xpath', "//span[@class='j-user-name j-navLabel']")
    JIVE_START_DISCUSSION_BTN                           = ('xpath', '//li[@id="jive-link-createThread"]')
    JIVE_WRITE_DOCUMENT_BTN                             = ('xpath', '//li[@id="jive-link-createDocument"]')
    JIVE_DISCUSSION_TITLE                               = ('xpath', '//input[@id="subject"]')
    JIVE_WYSIWYG_BTN                                    = ('xpath', '//a[@id="wysiwygtext_extra"]')
    JIVE_BSE_MAIN_IFRAME                                = ('xpath', '//iframe[@src="/kaltura-browse-and-embed.jspa"]')
    JIVE_BSE_INNER_IFRAME                               = ('xpath', '//iframe[@id="browse_and_embed_frame"]')
    JIVE_SAVE_DISCUSSION_BTN                            = ('xpath', '//button[@id="submitButton"]')
    JIVE_DISPLAY_EMBED_FOR_EVERYONE_OPTION              = ('xpath', '//input[@id="js-all"]')
    JIVE_EMBED_TITLE_IN_COMMUNITY                       = ('xpath', '//a[@class="title" and text()="EMBED_NAME"]')
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
        
           
    def getJiveLoginUserName(self):
        try:
            userName = self.get_element_text(self.JIVE_USER_NAME)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get user name element")
            return False
        return userName.lower() 


    # @Author: Inbar Willman
    # isDiscussion=True: Create embed from discussion page
    # isDocument=True: Create embed from document page
    def createEmbedMedia(self,embedTitle, entryName, mediaGalleryName=None, embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False, filePath=None, description=None, tags=None, isTagsNeeded=True, isDiscussion=True, isDocument=False):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
            writeToLog("INFO","FAILED navigate to courses 'New1'")
            return False
        
        if isDiscussion == True:
            if self.click(self.JIVE_START_DISCUSSION_BTN) == False:
                writeToLog("INFO","FAILED to click on 'discussion' button")
                return False 
            
        elif isDocument == True:
            if self.click(self.JIVE_WRITE_DOCUMENT_BTN) == False:
                writeToLog("INFO","FAILED to click on 'dociment' button")
                return False 
        else:
            writeToLog("INFO","FAILED: Page to embed from wasn't given")
            return False
        
        if self.send_keys(self.JIVE_DISCUSSION_TITLE, embedTitle) == False:
            writeToLog("INFO","FAILED to insert title in embed page")
            return False 
        
        if self.click(self.JIVE_WYSIWYG_BTN) == False:
            writeToLog("INFO","FAILED to click on 'wysisyg' button")
            return False   
        
        if self.swith_to_iframe(self.JIVE_BSE_MAIN_IFRAME) == False:
            writeToLog("INFO","FAILED to switch to jive main BSE iframe")
            return False 
        
        if self.swith_to_iframe(self.JIVE_BSE_INNER_IFRAME) == False:
            writeToLog("INFO","FAILED to switch to jive inner BSE iframe")
            return False                    
        
        if self.clsCommon.kafGeneric.embedMedia(entryName, mediaGalleryName, embedFrom, chooseMediaGalleryinEmbed, filePath, description, tags, application=enums.Application.JIVE, isTagsNeeded=isTagsNeeded) == False:    
            writeToLog("INFO","FAILED to choose media in embed page")
            return False  
        
        sleep(4)
   
        self.clsCommon.base.switch_to_default_content()
        
#         if self.click(self.JIVE_DISPLAY_EMBED_FOR_EVERYONE_OPTION) == False:
#             writeToLog("INFO","FAILED to click on 'The jive Community' option")
#             return False              
        
        if self.click(self.JIVE_SAVE_DISCUSSION_BTN) == False:
            writeToLog("INFO","FAILED to Save embed page")
            return False 
        
        writeToLog("INFO","Success: Embed discussion/document was created successfully")
        return True           
    
    # TODO
    # @Author: Inbar Willman 
    def verifyEmbedMedia(self, embedName, imageThumbnail, delay, forceNavigate=False):      
        if forceNavigate == True:
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to courses 'New1'")
                return False 
            
        tmp_embed_name = (self.JIVE_EMBED_TITLE_IN_COMMUNITY[0], self.JIVE_EMBED_TITLE_IN_COMMUNITY[1].replace('EMBED_NAME', embedName))
        if self.click(tmp_embed_name) == False:
                writeToLog("INFO","FAILED navigate to " + embedName + " embed page")
                return False    
            
        return True                                 