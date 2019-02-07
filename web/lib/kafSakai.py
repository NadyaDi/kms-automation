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
    SAKAI_USER_NAVGATION_MENU                           = ('xpath', "//span[@class='topnav']")
    SAKAI_USER_NAME                                     = ('xpath', "//a[@id='loginUser']")
    SAKAI_ANNOUNCEMENT_BTN                              = ('xpath', '//span[@class="menuTitle" and text()="Announcements"]')  
    SAKAI_ANNOUNCEMENT_PAGE_TITLE                       = ('xpath', '//span[@class="siteTitle" and text()="New1:"]')
    SAKAI_ADD_ANNOUNCEMENT_BTN                          = ('xpath', '//a[@title="Add"]')
    SAKAI_INSERT_ANNOUNCEMENT_TITLE                     = ('xpath', '//input[@id="subject"]')
    SAKAI_ANNOUNCEMENT_WYSIWYG                          = ('xpath', '//span[@class="cke_button_icon cke_button__kaltura_icon"]')
    SAKAI_BSE_IFRAME                                    = ('xpath', '//iframe[contains(@src, "/media-gallery-tool/")]')
    SAKAI_EMBED_ENTRY_IFRAME                            = ('xpath', '//iframe[@class="cke_wysiwyg_frame cke_reset"]')
    SAKAI_POST_ANNOUNCEMENT_BTN                         = ('xpath', '//input[@id="saveChanges"]')
    SAKAI_EMBED_ANNOUNCEMENT_TITLE                      = ('xpath', '//a[contains(@title, "ANNOUNCEMENT_NAME")]')
    SAKAI_REMOVE_ANNOUNCEMENT_BTN                       = ('xpath', '//a[@title="Remove"]')
    SAKAI_CONFIRM_REMOVE_ANNOUNCEMENT_BTN               = ('xpath', '//input[@name="eventSubmit_doDelete"]')
    SAKAI_POST_ANNOUNCEMENT_HEADER                      = ('xpath', '//h3[contains(text(),"Post Announcement")]')
    SAKAI_EMBED_ENTRY_THUMBNAIL                         = ('xpath', '//img[contains(@data-cke-saved-src, "thumbnail/entry_id")]')
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
         
            
    def getSakaiLoginUserName(self):
        self.clsCommon.base.switch_to_default_content()
        if self.click(self.SAKAI_USER_NAVGATION_MENU) == False:
            writeToLog("INFO","FAILED to click on user menu")
            return False
            
        try:
            userName = self.get_element_text(self.SAKAI_USER_NAME)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get user name element")
            return False
        return userName 

    
    # @Author: Inbar Willman
    def createEmbedAnnouncement(self, announcementTitle, entryName, mediaGalleryName=None, embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False, filePath=None, description=None, tags=None, isTagsNeeded=True):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_SITE_NEW1_URL) == False:
            writeToLog("INFO","FAILED to navigate to 'New1' page")
            return False    
                    
        if self.click(self.SAKAI_ANNOUNCEMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on 'announcement' button")
            return False   
        
        if self.wait_element(self.SAKAI_ANNOUNCEMENT_PAGE_TITLE) == False:
            writeToLog("INFO","FAILED to displayed 'announcement' page title")
            return False  
        
        self.switchToSakaiIframe()
        
        if self.click(self.SAKAI_ADD_ANNOUNCEMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on 'add' button")
            return False  
        
        if self.send_keys(self.SAKAI_INSERT_ANNOUNCEMENT_TITLE, announcementTitle) == False:
            writeToLog("INFO","FAILED to insert announcement title")
            return False 
        
        sleep(3)
        
        if self.click(self.SAKAI_ANNOUNCEMENT_WYSIWYG) == False:
            writeToLog("INFO","FAILED to click on 'wysiwyg' button")
            return False 
        
        if self.swith_to_iframe(self.SAKAI_BSE_IFRAME) == False:
            writeToLog("INFO","FAILED to switch to BSE iframe")
            return False 
        
        if self.clsCommon.kafGeneric.embedMedia(entryName, mediaGalleryName, embedFrom, chooseMediaGalleryinEmbed, filePath, description, tags, application=enums.Application.D2L, isTagsNeeded=isTagsNeeded) == False:    
            writeToLog("INFO","FAILED to choose media in embed page")
            return False 
        
        sleep(5)
        
        # Switch to embed entry iframe
        self.clsCommon.base.switch_to_default_content()
        self.switchToSakaiIframe() 
        self.swith_to_iframe(self.SAKAI_EMBED_ENTRY_IFRAME)
        
        if self.wait_element(self.SAKAI_EMBED_ENTRY_THUMBNAIL) == False:
            writeToLog("INFO","FAILED to displayed emebed entry thumbnail")
            return False 
        
        # Switch to sakai iframe
        self.clsCommon.base.switch_to_default_content()
        self.switchToSakaiIframe()         
        
        self.click(self.SAKAI_POST_ANNOUNCEMENT_HEADER)
        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
        
        sleep(3)
        
        if self.click(self.SAKAI_POST_ANNOUNCEMENT_BTN) == False:
            writeToLog("INFO","FAILED to save announcement")
            return False 
        
        self.clsCommon.base.switch_to_default_content()
        writeToLog("INFO","Success: embed was created")
        return True
    
    
    # @Author: Inbar Willman
    def verifyEmbedAnnouncement(self, announcementName, imageThumbnail, delay, forceNavigate=False):
        if forceNavigate == True:
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_SITE_NEW1_URL) == False:
                writeToLog("INFO","FAILED to navigate to 'New1' page")
                return False    
                    
            if self.click(self.SAKAI_ANNOUNCEMENT_BTN) == False:
                writeToLog("INFO","FAILED to click on 'announcement' button")
                return False 
        
        self.switch_to_default_content()
        self.switchToSakaiIframe() 

        tmp_announcement_name = (self.SAKAI_EMBED_ANNOUNCEMENT_TITLE[0], self.SAKAI_EMBED_ANNOUNCEMENT_TITLE[1].replace('ANNOUNCEMENT_NAME', announcementName))
        if self.click(tmp_announcement_name) == False:
            writeToLog("INFO","FAILED to click on embed announcement title")
            return False
         
        self.swith_to_iframe(self.SAKAI_BSE_IFRAME) 
        self.clsCommon.player.switchToPlayerIframe()
        self.wait_element(self.clsCommon.player.PLAYER_CONTROLER_BAR, timeout=30)
        
        sleep(3)
        
        # If entry type is video
        if delay != '':   
            if self.clsCommon.player.clickPlayPauseAndVerify(delay) == False:
                writeToLog("INFO","FAILED to play and verify video")
                return False                
        
        # If entry type is image     
        else:
            if self.clsCommon.player.verifyThumbnailInPlayer(imageThumbnail) == False:
                writeToLog("INFO","FAILED to display correct image thumbnail")
                return False
        
        self.clsCommon.base.switch_to_default_content()
        writeToLog("INFO","Success embed was verified")
        return True 
    
    
    # @Author: Inbar Willman
    def deleteAnnouncement (self, announcementName, forceNavigate=False): 
        # Get announcement title locator 
        tmp_announcement_name = (self.SAKAI_EMBED_ANNOUNCEMENT_TITLE[0], self.SAKAI_EMBED_ANNOUNCEMENT_TITLE[1].replace('ANNOUNCEMENT_NAME', announcementName))
         
        if forceNavigate == True:
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_SITE_NEW1_URL) == False:
                writeToLog("INFO","FAILED to navigate to 'New1' page")
                return False    
                    
            if self.click(self.SAKAI_ANNOUNCEMENT_BTN) == False:
                writeToLog("INFO","FAILED to click on 'announcement' button")
                return False 
        
            self.switch_to_default_content()
            self.switchToSakaiIframe() 

            if self.click(tmp_announcement_name) == False:
                writeToLog("INFO","FAILED to click on embed announcement title")
                return False    
        
        self.switchToSakaiIframe() 
        
        if self.click(self.SAKAI_REMOVE_ANNOUNCEMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on 'remove' button")
            return False
        
        if self.click(self.SAKAI_CONFIRM_REMOVE_ANNOUNCEMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on confirm remove button")
            return False              
        
        if self.wait_element(tmp_announcement_name) != False:
            writeToLog("INFO","FAILED to delete " + announcementName + " , announcement is still displayed in page")
            return False    
        
        writeToLog("INFO","Success: " + announcementName + " was deleted") 
        return True        