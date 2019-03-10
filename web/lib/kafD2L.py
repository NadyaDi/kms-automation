from base import *
from general import General
from localSettings import *
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
    D2L_SELECT_COURSES_BUTTON                           = ('xpath', "//div[@class='d2l-navigation-s-course-menu']")
    D2L_SELECT_COURSE_NEW1_BUTTON                       = ('xpath', "//a[@class='d2l-link d2l-datalist-item-actioncontrol' and contains(text(), 'New1 - New1')]")
    D2L_HEANDL_ENTRY_WIDGET_IN_ENTRY_PAGE               = ('xpath', "//h2[@class='d2l-heading vui-heading-4']") # in entry page if need to do page down/up us this locator to grab the page
    D2L_USER_NAME                                       = ('xpath', "//span[@class='d2l-navigation-s-personal-menu-text']")
    D2L_CREATE_NEW_DISCUSSIONS_BTN                      = ('xpath', '//a[@id="NewDiscussionsButtonMenu"]')
    D2L_NEW_FORUM_OPTION                                = ('xpath', "//span[contains(text(), 'New Forum')]")
    D2L_FORUM_TITLE                                     = ('xpath', '//input[@id="EDT_forumTitle"]')
    D2L_DISCUSSION_EDITOR_ICON                          = ('xpath', '//a[@class="d2l-htmleditor-button"]')
    D2L_INSERT_STUFF_IFRAME                             = ('xpath', '//iframe[@class="d2l-dialog-frame"]')
    D2L_QA_APP_BSE_OPTION                               = ('xpath' , '//span[@class="d2l-textblock" and text()="QAapp BSE "]')
    D2L_EMBED_INSERT_BTN                                = ('xpath', '//button[@class="d2l-button" and text()="Insert"]')
    D2L_SAVE_AND_CLOSE_DISCUSSION                       = ('xpath', '//button[contains(@class,"2l-button") and text()="Save and Close"]')
    D2L_DISCUSSIONS_LINK_BTN                            = ('xpath', '//a[@href="/d2l/le/6750/discussions/List"]')
    D2L_NEW_FORUM_TITLE                                 = ('xpath', '//span[@class="vui-heading-1" and text()="New Forum"]')   
    D2L_INSERT_STUFF_TITLE                              = ('xpath', '//span[@class="vui-heading-3" and text()="Insert Stuff"]')    
    D2L_EMBED_IFRAME                                    = ('xpath', '//iframe[@id="remoteIframe"]')  
    D2L_FORUM_DESCRIPTION_IFRAME                        = ('xpath', '//iframe[contains(@id, "forumDescription")]')  
    D2L_FORUM_DESCRIPTION_ENTRY_IFRAME                  = ('xpath', '//iframe[contains(@title, "ENTRY_NAME")]')   
    D2L_EMBED_DISCUSSION_MENU                           = ('xpath', '//a[@title="Actions for DISCUSSION_NAME"]')    
    #D2L_EMBED_DISCUSSION_DELETE_OPTION                  = ('xpath', '//d2l-menu-item[contains(@id,"DeleteForum") and @class="d2l-contextmenu-item d2l-menu-item-last"]')
    D2L_EMBED_DISCUSSION_DELETE_OPTION                  = ('xpath', "//span[contains(text(), 'Delete')]")
    D2L_DELETE_DISCUSSION_CONFIRMATION_BTN              = ('xpath', '//button[@class="d2l-button" and text()="Yes"]')
    D2L_DELETE_CONFIRMATION_MSG                         = ('xpath', '//div[contains(@data-message-text,"has been deleted")]')
    D2L_QA_PROD_BSE_OPTION                              = ('xpath', '//span[@class="d2l-textblock" and text()="QA PROD BSE"]')
    D2L_EMBED_DISCUSSION_FRAME_TITLE                    = ('xpath', "//a[contains(@id, 'ForumContextMenu') and contains(@title,'GUID')]")
    D2L_COURSE_CONTENT_TAB                              = ('xpath', '//a[@class="d2l-navigation-s-link" and text()="Content"]')
    D2L_ADD_EXISTING_ACTIVITIES_DROPDOWN                = ('xpath', '//a[@title="Add activities to activity"]')
    D2L_ADD_EXISTING_ACTIVITIES_OPTION                  = ('xpath', '//a[@class=" vui-dropdown-menu-item-link" and contains(text(),"BSE_EVIORMENT")]')
    D2L_GRADEBOOK_EMBED_IFRAME                          = ('xpath', '//iframe[@id="QuickLinkSelectorFrame"]')
    D2L_GRADEBOOK_TITLE                                 = ('xpath', '//a[@title=""ENTRY_NAME" - External Learning Tool"]')
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
        
    
    # @Author: Inbar Willman
    def createEmbedDiscussion(self, discussionTitle, entryName, mediaGalleryName=None, embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False, filePath=None, description=None, tags=None, isTagsNeeded=True):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
            writeToLog("INFO","FAILED navigate to New1 media gallery page")
            return False 
        
        if self.click(self.D2L_DISCUSSIONS_LINK_BTN) == False:
            writeToLog("INFO","FAILED to click on 'Discussions' button")
            return False  
        
        if self.wait_element(self.D2L_CREATE_NEW_DISCUSSIONS_BTN) == False:
            writeToLog("INFO","FAILED to display 'New' button")
            return False  
        
        sleep(4)         
        
        if self.click(self.D2L_CREATE_NEW_DISCUSSIONS_BTN) == False:
            writeToLog("INFO","FAILED to click on new button")
            return False 
         
        if self.click(self.D2L_NEW_FORUM_OPTION, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on new forum button")
            return False                  
        
        if self.wait_element(self.D2L_FORUM_TITLE, timeout=15) == False:
            writeToLog("INFO","FAILED to display forum title field")
            return False    
        
        sleep(3)         
        
        if self.send_keys(self.D2L_FORUM_TITLE, discussionTitle)   == False:
            writeToLog("INFO","FAILED to insert forum title field")
            return False 
        
        sleep(3)
        
        if self.click(self.D2L_DISCUSSION_EDITOR_ICON) == False:
                writeToLog("INFO","FAILED to click on editor icon")
                return False 
            
        self.clsCommon.base.swith_to_iframe(self.D2L_INSERT_STUFF_IFRAME)
        
        if self.wait_element(self.D2L_INSERT_STUFF_TITLE) == False:
                writeToLog("INFO","FAILED to display 'Insert Stuff' title")
                return False                
        
        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
        
        if localSettings.LOCAL_SETTINGS_ENV_NAME != 'ProdNewUI':
            if self.click(self.D2L_QA_APP_BSE_OPTION) == False:
                writeToLog("INFO","FAILED to click on 'QAapp BSE' option")
                return False  
        else:
            if self.click(self.D2L_QA_PROD_BSE_OPTION) == False:
                writeToLog("INFO","FAILED to click on 'QA PROD BSE' option")
                return False              
        
        self.clsCommon.base.swith_to_iframe(self.D2L_EMBED_IFRAME)
        
        # In embed page, choose page to embed from and media
        if localSettings.LOCAL_SETTINGS_ENV_NAME == 'ProdNewUI':
            if self.clsCommon.kafGeneric.embedMedia(entryName, mediaGalleryName, embedFrom, True, filePath, description, tags, application=enums.Application.D2L, isTagsNeeded=isTagsNeeded) == False:    
                writeToLog("INFO","FAILED to choose media in embed page")
                return False            
        else:
            if self.clsCommon.kafGeneric.embedMedia(entryName, mediaGalleryName, embedFrom, chooseMediaGalleryinEmbed, filePath, description, tags, application=enums.Application.D2L, isTagsNeeded=isTagsNeeded) == False:    
                writeToLog("INFO","FAILED to choose media in embed page")
                return False  
        
        sleep(4)
   
        # wait until the player display in the page
        self.clsCommon.base.switch_to_default_content()
        
        # Switch to forum description iframe
        self.swith_to_iframe(self.D2L_FORUM_DESCRIPTION_IFRAME)
        
        # Switch to entry iframe - in forum description
        tmp_entry_iframe = (self.D2L_FORUM_DESCRIPTION_ENTRY_IFRAME[0], self.D2L_FORUM_DESCRIPTION_ENTRY_IFRAME[1].replace('ENTRY_NAME', entryName))
        self.swith_to_iframe(tmp_entry_iframe)
        
        self.clsCommon.player.switchToPlayerIframe()
        self.wait_element(self.clsCommon.player.PLAYER_CONTROLER_BAR, timeout=30)
        
        self.clsCommon.base.switch_to_default_content()
        
        if self.click(self.D2L_SAVE_AND_CLOSE_DISCUSSION) == False:
            writeToLog("INFO","FAILED to click on 'Save and Close' button")
            return False 
        
        writeToLog("INFO","Success: Embed discussion was created successfully")
        return True  
    
    
    # @ Author: Inbar Willman
    def verifyD2lEmbedEntry(self, entryName, imageThumbnail, delay, forceNavigate=False, isQuiz=False):
        # Navigate to discussions page  
        if forceNavigate == True: 
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to New1 media gallery page")
                return False 
        
            if self.click(self.D2L_DISCUSSIONS_LINK_BTN) == False:
                writeToLog("INFO","FAILED to click on 'Discussions' button")
                return False  
            
        # Focus on the frame title
        frameMenuBtnEl = self.wait_element((self.D2L_EMBED_DISCUSSION_FRAME_TITLE[0], self.D2L_EMBED_DISCUSSION_FRAME_TITLE[1].replace('GUID', localSettings.LOCAL_SETTINGS_GUID)))
        if frameMenuBtnEl == False:
            writeToLog("INFO","FAILED to get frame menu button")
            return False
        frameMenuBtnEl.send_keys('')           
        self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN,6)            
               
        # Switch to embed iframe                                         
        tmp_entry_iframe = (self.D2L_FORUM_DESCRIPTION_ENTRY_IFRAME[0], self.D2L_FORUM_DESCRIPTION_ENTRY_IFRAME[1].replace('ENTRY_NAME', entryName))
        self.swith_to_iframe(tmp_entry_iframe) 
        
        # Switch to player iframe
        self.clsCommon.player.switchToPlayerIframe()
        self.wait_element(self.clsCommon.player.PLAYER_CONTROLER_BAR, timeout=30)
        
        sleep(6)
        
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
    
    
    # @Author: Inbar WIllman
    def deleteDiscussion(self, discussionName, forceNavigate=False):  
        # Navigate to discussions page  
        if forceNavigate == True: 
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to New1 media gallery page")
                return False 
        
            if self.click(self.D2L_DISCUSSIONS_LINK_BTN) == False:
                writeToLog("INFO","FAILED to click on 'Discussions' button")
                return False 

        tmp_discussion_menu = (self.D2L_EMBED_DISCUSSION_MENU[0], self.D2L_EMBED_DISCUSSION_MENU[1].replace('DISCUSSION_NAME', discussionName))
        discussion_menu_element = self.wait_element(tmp_discussion_menu)
         
        if discussion_menu_element != False:
            if ActionChains(self.driver).move_to_element(discussion_menu_element).click().perform() == False:
                writeToLog("INFO","FAILED to click on embed discussion menu")
                return False    
        else:
            writeToLog("INFO","FAILED to find embed discussion menu")
            return False  
        
        sleep(2)    

        if self.click(self.D2L_EMBED_DISCUSSION_DELETE_OPTION, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on delete option")
            return False
        
        if self.click(self.D2L_DELETE_DISCUSSION_CONFIRMATION_BTN) == False:
            writeToLog("INFO","FAILED to click 'Yes' on delete confirmation popup")
            return False  
        
#        tmp_delete_message = (self.D2L_DELETE_CONFIRMATION_MSG[0], self.D2L_DELETE_CONFIRMATION_MSG[1].replace('DISCUSSION_NAME', discussionName))   
        if self.wait_element(self.D2L_DELETE_CONFIRMATION_MSG) == False:
            writeToLog("INFO","FAILED to displayed delete confirmation message")
            return False   
        
        writeToLog("INFO","Success: Embed discussion was deleted")    
        return True    
    
    
    # @Author: Inbar Willman 
    def createGradebook(self, entryName):  
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
            writeToLog("INFO","FAILED navigate to New1 media gallery page")
            return False  
        
        if self.click(self.D2L_COURSE_CONTENT_TAB) == False:
            writeToLog("INFO","FAILED to click on 'Content' tab")
            return False      
        
        if self.click(self.D2L_ADD_EXISTING_ACTIVITIES_DROPDOWN) == False:
            writeToLog("INFO","FAILED to click on 'Add Existing Activities' dropdown")
            return False 
        
        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN) 
       
        if localSettings.LOCAL_SETTINGS_ENV_NAME == 'ProdNewUI':
            tmpBseEnviorment = (self.D2L_ADD_EXISTING_ACTIVITIES_OPTION[0], self.D2L_ADD_EXISTING_ACTIVITIES_OPTION[1].replace('BSE_EVIORMENT', 'QA PROD BSE')) 
            
        elif localSettings.LOCAL_SETTINGS_ENV_NAME == 'TestingNewUI':
            tmpBseEnviorment = (self.D2L_ADD_EXISTING_ACTIVITIES_OPTION[0], self.D2L_ADD_EXISTING_ACTIVITIES_OPTION[1].replace('BSE_EVIORMENT', 'QAapp BSE ')) 
            
        if self.click(tmpBseEnviorment) == False:
            writeToLog("INFO","FAILED to click on BSE option")
            return False 
        
        self.swith_to_iframe(self.D2L_GRADEBOOK_EMBED_IFRAME)
        
        if self.clsCommon.kafGeneric.embedMedia(entryName) == False:
            writeToLog("INFO","FAILED to choose media in BSE page")
            return False  
        
        self.switch_to_default_content()  
        
        tmpGradebookTitle = (self.D2L_GRADEBOOK_TITLE[0], self.D2L_GRADEBOOK_TITLE[1].replace('ENTRY_NAME', entryName)) 
        if self.wait_element(tmpGradebookTitle) == False:
            writeToLog("INFO","FAILED to display gradebook title")
            return False  
                  
        writeToLog("INFO","Success: Gradebook was created")
        return True         
                                                                   