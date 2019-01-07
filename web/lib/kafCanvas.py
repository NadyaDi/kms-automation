from base import *
from general import General
import localSettings
from logger import *
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
    CANVAS_DASHBOARD_BUTTON_IN_NAV_BAR                  = ('xpath', "//a[@id='global_nav_dashboard_link']")
    CANVAS_GALLERY_NEW1_IN_DASHBOARD_MENU               = ('xpath', "//div[@class='ic-DashboardCard' and @aria-label='New1']")
    CANVAS_USER_NAME                                    = ('xpath', "//h2[@class='_16dxlnN _2nPix9- _3ofYXie _1vP3JKU']")
    CANVAS_ANNOUNCEMENTS_TAB                            = ('xpath', '//a[@title="Announcements"]')
    CANVAS_CREATE_ANNOUNCEMENT_BTN                      = ('xpath', '//a[@id="add_announcement"]')
    CANVAS_ANNOUNCEMENTS_TITLE                          = ('xpath', '//input[@id="discussion-title"]')
    CANVAS_WYSIWYG                                      = ('xpath', '//button[@id="mceu_21-button"]')
    CANVAS_SAVE_ANNOUNCEMENT_BTN                        = ('xpath', '//button[@type="submit" and text()="Save"]')
    CANVAS_EMBED_ANNOUNCEMENTS_TITLE                    = ('xpath', '//h3[@data-ui-testable="Heading" and text()="EMBED_ANNOUNCEMENT_NAME"]')
    CANVAS_EMBED_IFRAME                                 = ('xpath', '//iframe=[@id="external_tool_button_frame"]')
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
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_CANVAS
            return True
                     
        if self.wait_visible(self.CANVAS_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_CANVAS
            return True
        else:
            if self.swith_to_iframe(self.CANVAS_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
             
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_CANVAS
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
        
        if self.click(self.USER_LOGOUT_BTN, multipleElements=True) == False:
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
        self.clsCommon.base.switch_to_default_content()
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
            writeToLog("INFO","FAILED navigate to my media page")
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
                writeToLog("INFO","Success Already in gallery page")
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
     
    def getCanvasLoginUserName(self):
        self.clsCommon.base.switch_to_default_content()
        if self.click(self.USER_ACCOUNT_BUTTON_IN_NAV_BAR) == False:
            writeToLog("INFO","FAILED to click on account button")
            return False 
        try:
            userName = self.get_element_text(self.CANVAS_USER_NAME)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get user name element")
            return False
        return userName.lower()   
    

    # @Author: Inbar Willman
    def createEmbedAnnouncements(self, announcementTitle, entryName, mediaGalleryName=None, embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False, filePath=None, description=None, tags=None):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_ANNOUNCEMENTS_URL) == False:
            writeToLog("INFO","FAILED navigate to announcements page")
            return False 
        
        if self.click(self.CANVAS_CREATE_ANNOUNCEMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on create announcement button")
            return False             
        
        if self.send_keys(self.CANVAS_ANNOUNCEMENTS_TITLE, announcementTitle)   == False:
            writeToLog("INFO","FAILED to insert announcement title")
            return False 
        
        if self.click(self.CANVAS_WYSIWYG) == False:
                writeToLog("INFO","FAILED to click on wysiwyg")
                return False  
            
        self.clsCommon.base.swith_to_iframe(self.CANVAS_EMBED_IFRAME)
        
        # In embed page, choose page to embed from and media
        if self.clsCommon.kafGeneric.embedMedia(entryName, mediaGalleryName, embedFrom, chooseMediaGalleryinEmbed, filePath, description, tags, application=enums.Application.CANVAS) == False:    
            writeToLog("INFO","FAILED to choose media in embed page")
            return False  
   
        # wait until the player display in the page
        self.clsCommon.player.switchToPlayerIframe()
        self.wait_element(self.clsCommon.player.PLAYER_CONTROLER_BAR, timeout=30)
        
        self.clsCommon.base.switch_to_default_content()  
        
        if self.click(self.CANVAS_SAVE_ANNOUNCEMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False 
        
        writeToLog("INFO","Success: Embed announcement was created successfully")
        return True    
    
    
    # @Author: Inbar Willman
    def verifyCanvasEmbedEntry(self, embedTitle, imageThumbnail, delay, forceNavigate=False):
        # Navigate to announcements page  
        if forceNavigate == True: 
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_ANNOUNCEMENTS_URL) == False:
                writeToLog("INFO","FAILED navigate to announcements page")
                return False     
                
        embed_anouncement = (self.CANVAS_EMBED_ANNOUNCEMENTS_TITLE[0], self.CANVAS_EMBED_ANNOUNCEMENTS_TITLE[1].replace('EMBED_ANNOUNCEMENT_NAME', embedTitle))
        if self.click(embed_anouncement) == False:
            writeToLog("INFO","FAILED to click on embed announcement name")
            return False                                        
        
        self.clsCommon.player.switchToPlayerIframe()
        self.wait_element(self.clsCommon.player.PLAYER_CONTROLER_BAR, timeout=30)
        self.clsCommon.base.switch_to_default_content()
        self.swith_to_iframe(self.MOODLE_EMBED_ENTRY_IFRAME) 
        sleep(5)
        
        # If entry type is video
        if delay != '':   
#            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER 
            if self.clsCommon.player.clickPlayPauseAndVerify(delay) == False:
                writeToLog("INFO","FAILED to play and verify video")
                return False                
        
        # If entry type is image     
        else:
            if self.clsCommon.player.verifyThumbnailInPlayer(imageThumbnail) == False:
                writeToLog("INFO","FAILED to display correct image thumbnail")
                return False
        
        writeToLog("INFO","Success embed was verified")
        return True                                  