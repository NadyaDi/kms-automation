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
    MOODLE_SITE_BLOG_TITLE                              = ('xpath', '//h2[contains(text(), "Site blog")]')
    MOODLE_SITE_BLOG_ADD_NEW_ENTRY                      = ('xpath', '//a[contains(@href, "moodle/blog") and text()="Add a new entry"]')
    MOODLE_SITE_BLOG_ENTRY_TITLE                        = ('xpath', '//input[@id="id_subject"]')
    MOODLE_SITE_BLOG_WYSIWYG                            = ('xpath', '//button[@class="atto_kalturamedia_button"]')
    MOODLE_SITE_BLOG_SUBMIT_BTN                         = ('xpath', '//input[@id="id_submitbutton"]')
    MOODLE_EMBED_IFRAME                                 = ('xpath', '//iframe[@id="kafIframe"]')
    MOODLE_EMBED_BTN                                    = ('xpath', '//button[@id="KalturaMediaSubmit"]')
    MOODLE_EMBED_SITE_BLOG_TITLE                        = ('xpath', '//a[contains(@href,"/moodle/blog/") and text()="SITE_BLOG_TITLE"]')
    MOODLE_EMBED_ENTRY_IFRAME                           = ('xpath', '//iframe[@class="kaltura-player-iframe"]')
    MOODLE_DELETE_EMBED_SITE_BLOG                       = ('xpath', '//a[contains(@href, "/moodle/blog") and text()="Delete"]')
    MOODLE_CONFIRM_DELETE_BUTTON                        = ('xpath', '//input[@type="submit" and @value="Continue"]')
    MOODLE_EMBED_SITE_BLOG_SECTION                      = ('xpath', '//div[@class="forumpost blog_entry blog clearfix site"]')
    MOODLE_TURN_EDITING_ON_BTN                          = ('xoath', '//input[@type="submit" and @value="Turn editing on"]')
    MOODLE_ADD_ACTIVITY_BUTTON                          = ('xpath', '//span[@class="section-modchooser-text" and text()="Add an activity or resource"]')
    MOODLE_KALTURA_VIDEO_RESOURCE_OPTION                = ('xpath', '//input[@id="item_kalvidres"]')
    MOODLE_ADD_CHOSEN_ACTIVITY_BTN                      = ('xpath', '//input[@class="submitbutton" and @value="Add"]')
    MOODLE_KALTURA_VIDEO_SOURCE_PAGE                    = ('xpath', '//img[@class="icon iconlarge" and text()="Adding a new Kaltura Video Resource"]')
    MOODLE_FILL_ACTIVITY_NAME                           = ('xpath', '//input[@id="id_name"]')
    MOODLE_KALTURA_VIDEO_SOURCE_ADD_MEDIA_BTN           = ('xpath', 'input[@id="id_add_video"]')
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
            
        self.clsCommon.moodle.switchToMoodleIframe()
        self.wait_element(self.clsCommon.kafGeneric.KAF_GRID_VIEW, timeout=20)
        self.clsCommon.base.switch_to_default_content()
        if self.wait_element(self.MOODLE__MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        
        self.clsCommon.moodle.switchToMoodleIframe()
        return True
    
    
    # @Author: Inbar Willmam
    def navigateToSiteBlog(self, forceNavigate=False):      
        self.clsCommon.base.switch_to_default_content()
        if forceNavigate == False:
            if self.wait_visible(self.MOODLE_SITE_BLOG_TITLE, 5) != False:
                writeToLog("INFO","Success Already in site blog page")
                self.clsCommon.moodle.switchToMoodleIframe()
                return True
            
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_SITE_BLOG_URL) == False:
                writeToLog("INFO","FAILED navigate to site blog page")
                return False            
        
        if self.wait_visible(self.MOODLE_SITE_BLOG_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to site blog page")
            return False
        
        self.clsCommon.moodle.switchToMoodleIframe()
        return True
    
    
    # @Author: Inbar Willman
    def createEmbedSiteBlog(self, entryName, siteBlogTitle, embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False):
        if self.navigateToSiteBlog() == False:
            writeToLog("INFO","FAILED navigate to to site blog page")
            return False
        
        if self.click(self.MOODLE_SITE_BLOG_ADD_NEW_ENTRY) == False:
            writeToLog("INFO","FAILED to click on 'Add a new entry'")
            return False     
        
        if self.send_keys(self.MOODLE_SITE_BLOG_ENTRY_TITLE, siteBlogTitle) == False:
            writeToLog("INFO","FAILED to insert site blog entry title")
            return False   
        
        # Get window before opening embed window
        window_before = self.clsCommon.base.driver.window_handles[0]  
        
        if self.click(self.MOODLE_SITE_BLOG_WYSIWYG) == False:
            writeToLog("INFO","FAILED to click on wysiwyg")
            return False  
        
        sleep(2)
        
        # Get window after opening embed window and switch to this window
        window_after = self.clsCommon.base.driver.window_handles[1]
        self.clsCommon.base.driver.switch_to_window(window_after)
        
        if self.clsCommon.kafGeneric.embedMedia(entryName, '', embedFrom=embedFrom, chooseMediaGalleryinEmbed=chooseMediaGalleryinEmbed, application=enums.Application.MOODLE) == False:    
            writeToLog("INFO","FAILED to choose media in embed page")
            return False  
                
        self.clsCommon.base.driver.switch_to_window(window_before) 
        
        if self.click(self.MOODLE_SITE_BLOG_SUBMIT_BTN) == False:
            writeToLog("INFO","FAILED to click on submit button")
            return False  
                    
        return True       
    
    
    # @Author: Inbar Willman
    def verifyMoodleEmbedEntry(self, embedTitle, imageThumbnail='', delay='', forceNavigate=False): 
        # Navigate to site blog   
        if forceNavigate == True:   
            if self.navigateToSiteBlog() == False:
                writeToLog("INFO","FAILED to navigate to site blog")
                return False  
        
            # Click on embed site blog
            embedSiteBlogTitle = (self.MOODLE_EMBED_SITE_BLOG_TITLE[0], self.MOODLE_EMBED_SITE_BLOG_TITLE[1].replace('SITE_BLOG_TITLE', embedTitle))
            if self.click(embedSiteBlogTitle) == False:
                writeToLog("INFO","FAILED to click on site blog title")
                return False   
         
        # If entry type is video
        if delay != '':  
            self.swith_to_iframe(self.MOODLE_EMBED_ENTRY_IFRAME) 
#            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER 
            if self.clsCommon.player.clickPlayPauseAndVerify(delay) == False:
                writeToLog("INFO","FAILED to play and verify video")
                False                
        
        # If entry type is image     
        else:
            if self.clsCommon.player.verifyThumbnailInPlayer(imageThumbnail) == False:
                writeToLog("INFO","FAILED to display correct image thumbnail")
                
        return True 
    
    
    # @Author: Inbar Willman
    # Delete embed item
    def deleteEmbedSiteBlog(self, embedName, forceNavigate=False):
        self.switch_to_default_content()
        
        if forceNavigate == True:
            # Navigate to site blog      
            if self.navigateToSiteBlog() == False:
                writeToLog("INFO","FAILED to navigate to site blog")
                return False  
        
            # Click on embed site blog
            embedSiteBlogTitle = (self.MOODLE_EMBED_SITE_BLOG_TITLE[0], self.MOODLE_EMBED_SITE_BLOG_TITLE[1].replace('SITE_BLOG_TITLE', embedName))
            if self.click(embedSiteBlogTitle) == False:
                writeToLog("INFO","FAILED to click on site blog title")
                return False 
        
        # Click on delete button    
        if self.click(self.MOODLE_DELETE_EMBED_SITE_BLOG) == False:
            writeToLog("INFO","FAILED click on 'delete' button")
            return False 
        
        # Confirm delete
        if self.click(self.MOODLE_CONFIRM_DELETE_BUTTON) == False:
            writeToLog("INFO","FAILED click on 'conform' button")
            return False                       
    
        #Verify that site blog section isn't display anymore 
        if self.wait_element(self.MOODLE_EMBED_SITE_BLOG_SECTION) != False:
            writeToLog("INFO","FAILED, embed site blog section is still displayed")
            return False             
        
        return True   
    
    
    # @Author: Inbar Willman
    def chooseMoodleActivity(self, galleryName='New1', activity=enums.MoodleActivities.KALTURA_VIDEO_RESOURCE):
        if self.navigateToGalleryMoodle(galleryName) == False:
            writeToLog("INFO","FAILED navigate to to course page")
            return False
        
        # Check if turn editing on id enabled
        if self.wait_element(self.MOODLE_TURN_EDITING_ON_BTN) == False:
            # Enable turn editing on
            if self.click(self.MOODLE_TURN_EDITING_ON_BTN) == False:
                writeToLog("INFO","FAILED to click on 'turn editing on' button")
                return False  
            
        if self.click(self.MOODLE_ADD_ACTIVITY_BUTTON) == False:
                writeToLog("INFO","FAILED to click on 'add an activity or resource' button")
                return False 
            
        if activity == enums.MoodleActivities.KALTURA_VIDEO_RESOURCE:
            if self.click(self.MOODLE_KALTURA_VIDEO_RESOURCE_OPTION) == False:
                writeToLog("INFO","FAILED to click on 'kaltura video resource' option")
                return False  
            
        if self.click(self.MOODLE_ADD_CHOSEN_ACTIVITY_BTN) == False:
                writeToLog("INFO","FAILED to click on 'Add' button")
                return False
            
        if activity == enums.MoodleActivities.KALTURA_VIDEO_RESOURCE:
            if self.wait_element(self.MOODLE_KALTURA_VIDEO_SOURCE_PAGE) == False:
                writeToLog("INFO","FAILED to display kaltura video spurce page")
                return False 
            
        return True
            
    
    # @Author: Inbar Willman        
    def createEmbedActivity(self, entryName, activityName, galleryName='New1', activity=enums.MoodleActivities.KALTURA_VIDEO_RESOURCE, embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False):
        if self.chooseMoodleActivity(galleryName, activity) == False:
                writeToLog("INFO","FAILED to choose moodle activity")
                return False  
            
        if self.send_keys(self.MOODLE_FILL_ACTIVITY_NAME, activityName) == False:
            writeToLog("INFO","FAILED to insert site blog entry title")
            return False   
        
        # Get window before opening embed window
        window_before = self.clsCommon.base.driver.window_handles[0]  
        
        if activity == enums.MoodleActivities.KALTURA_VIDEO_RESOURCE:
            if self.click(self.MOODLE_KALTURA_VIDEO_SOURCE_ADD_MEDIA_BTN) == False:
                writeToLog("INFO","FAILED to click on 'Add medoa' button")
                return False                
             
        else:
            if self.click(self.MOODLE_SITE_BLOG_WYSIWYG) == False:
                writeToLog("INFO","FAILED to click on wysiwyg")
                return False  
        
        sleep(2)
        
        # Get window after opening embed window and switch to this window
        window_after = self.clsCommon.base.driver.window_handles[1]
        self.clsCommon.base.driver.switch_to_window(window_after)
        
        if self.clsCommon.kafGeneric.embedMedia(entryName, '', embedFrom=embedFrom, chooseMediaGalleryinEmbed=chooseMediaGalleryinEmbed, application=enums.Application.MOODLE) == False:    
            writeToLog("INFO","FAILED to choose media in embed page")
            return False  
                
        self.clsCommon.base.driver.switch_to_window(window_before) 
        
        if self.click(self.MOODLE_SITE_BLOG_SUBMIT_BTN) == False:
            writeToLog("INFO","FAILED to click on submit button")
            return False  
                    
        return True         