from base import *
from general import General
import localSettings
from logger import *
from _ast import Is
from selenium.webdriver.common.keys import Keys
import enums


class BlackBoard(Base):
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
    USER_MENU_TOGGLE_BTN                                = ('id', 'global-nav-link')
    USER_LOGOUT_BTN                                     = ('id', 'topframe.logout.label')
    BB_MEDIA_SPACE_IFRAME                               = ('xpath', "//iframe[contains(@src,'/webapps/osv-kaltura-BBLEARN/')]")
    BB_SHARED_REPOSITORY_BUTTON                         = ('xpath', "//a[contains(text(),'Faculty Repository')]")
    BB_MODLUES_PAGE_BUTTON                              = ('xpath', "//a[contains(text(),'Add Module')]")
    BB_ADD_MODULE_BUTTON                                = ('xpath', "//a[contains(@id,'IDaddButton') and contains(text(), 'Add')]")
    BB_REMOVE_MODULE_BUTTON                             = ('xpath', "//a[contains(@id,'IDremoveButton') and contains(text(), 'Remove')]")
    BB_SHARED_REPOSITORY_ADD_REQUIRED_METADATA_BUTTON   = ('xpath', "//label[@class='inline sharedRepositoryMetadata collapsed']")
    BB_COURSE_PAGE                                      = ('xpath', '//span[@title="COURSE_PAGE" and text()="COURSE_PAGE"]')
    BB_SHARED_REPOSITORY_DISCLAIMER_MSG_BEFOR_PUBLISH   = ('xpath', "//div[contains(@class, 'alert') and contains(text(), 'Complete all the required fields and save the entry before you can select to publish it to shared repositories.')]")
    BB_SHARED_REPOSITORY_ADD_REQUIRED_METADATA_BUTTON   = ('xpath', "//label[@class='collapsed inline sharedRepositoryMetadata']")
    BB_SHARED_REPOSITORY_REQUIRED_METADATA_FIELD        = ('xpath', "//span[@class='inline']")
    BB_ADD_COURSE_MODAL                                 = ('xpath', '//a[contains(@href,"/webapps/portal/execute/tabs/tabManageModules") and text()="Add Course Module"]')
    BB_COURSE_ADD_MODULE_SEARCH_FIELD                   = ('xpath', '//input[@id="txtSearch"]')
    BB_COURSE_ADD_MODULE_SEARCH_SUBMIN_BTN              = ('xpath', '//input[@type="submit" and @value="Go"]')
    ADD_COURSE_MODULE_BTN                               = ('xpath', '//a[@id="MODULE_ID:-1addButton"]')
    REMOVE_COURSE_MODULE_BTN                            = ('xpath', '//a[@id="MODULE_ID:-1removeButton"]')     
    COURSE_MODULE_NAME                                  = ('xpath','//span[@class="moduleTitle" and text()="MODULE_NAME"]')   
    BB_MEDIA_GALLERY_ENTRY_NAME                         = ('xpath', '//a[@class="item_link" and text()="ENTRY_NAME"]')  
    FEATURED_MEDIA_ICON                                 = ('xpath', '//a[@id="featured_ENTRY_NAME"]')   
    DETAILED_VIEW                                       = ('xpath', '//i[@class="icon-th-list"]')
    FEATURED_MEDIA_ENTRY                                = ('xpath', '//div[@class="hfm-carousel-item js-hfm-carousel-item slick-slide slick-current slick-active slick-center"]')
    BB_CONTENT_PAGE_MENU                                = ('xpath', '//a[contains(@id, "Menu_actionButton") and contains(text(),"MENU_NAME")]')
    BB_CONTENT_PAGE_MENU_OPTION                         = ('xpath', '//a[contains(@id, "content-handler") and text()="MENU_OPTION"]')
    CONTENT_TYPE_TITLE                                  = ('xpath', '//span[@id="pageTitleText" and contains(text(), "CONTENT_TYPE")]')
    #BB_EMBED_MASHUPS_BTN                                = ('xpath', '//a[@id="htmlData_text_bb_mashupbutton_action"]')
    BB_EMBED_MASHUPS_BTN                                = ('xpath', '//a[@class="mceAction mce_bb_mashupbutton"]')
    BB_EMBED_KALTURA_MEDIA_OPTION                       = ('xpath', '//span[@class="mceText" and @title="Kaltura Media"]')
    KAF_SUBMIT_BUTTON                                   = ('xpath', '//input[@type="submit"]')
    CONTENT_ITEM_NAME_FIELD                             = ('xpath', '//input[@id="user_title" and @name="user_title"]')
    SUCCESS_CREATE_EMBED_MEDIA_MESSAGE                  = ('xpath', '//span[@id="goodMsg1" and text()="Success: ITEM_NAME created."]')
    EMBED_ENTRY_PLAY_ICON                               = ('xpath', '//div[@class="play_image"]')
    EMBED_CONTENT_DROP_DOWN                             = ('xpath', '//a[@href="#contextMenu" and contains(@title,"CONTENT_NAME")]')
    EMBED_CONTENT_MENU_OPTION                           = ('xpath', '//a[@title="OPTION" and text()="OPTION"]')
    SUCCESS_DELETE_EMBED_MEDIA_MESSAGE                  = ('xpath', '//span[@id="goodMsg1" and text()="Success: ITEM_NAME deleted."]')
    CONTENT_KALTURA_MEDIA_NAME_FIELD                    = ('xpath', '//input[@id="title" and @name="title"]') 
    BB_EMBED_KALTURA_MEDIA_IFRAME                       = ('xpath', "//iframe[contains(@src,'../LtiMashup?course_id=_51_1&content_id=_472_1&mode=sa')]")
    BB_CONTENT_TOOLS_MENU_MORE_TOOLS_OPTION             = ('xpath', '//a[@class="donotclose slideoutLink"]')
    BB_CONTENT_ANNOUNCEMENTS_OPTION                     = ('xpath', '//a[@id="tool-announcements" and text()="Announcements"]')
    CONTENT_ANNOUNCEMENTS_NAME_FIELD                    = ('xpath', '//input[@id="specific_link_name"]')
    SUCCESS_DELETE_EMBED_ANNOUNCEMENTS_MESSAGE          = ('xpath', '//span[@id="goodMsg1" and text()="Success: ITEM_NAME Deleted."]')
    BB_ADD_MEDIA_TO_SR_BTN                              = ('xpath', '//a[@id="tab-addcontent"]')
    BB_ADD_NEW_MEDIA_TO_SR_BTN                          = ('xpath', '//a[@id="add-new-tab"]')
    BB_MY_INSTITUTION_BUTTON_IN_NAV_BAR                 = ('xpath', "//span[contains(text(), 'My Institution')]")
    BB_MY_MEDIA_BUTTON_IN_MY_INSTITUTION_PAGE           = ('xpath', "//a[contains(text(), 'My Media')]")
    BB_COURSES_BUTTON_IN_NAV_BAR                        = ('xpath', "//span[contains(text(), 'Courses')]")
    BB_COURSE_NEW1_BUTTON_IN_COURSES_PAGE               = ('xpath', "//a[contains(text(), 'New1: New1')]")
    BB_TOOLS_OPTION_UNDER_TOOLS_MENU_IN_COURSE_PAGE     = ('xpath', "//span[@title= 'Tools' and contains(text(), 'Tools')]")
    BB_MEDIA_GALLEY_OPTION_IN_TOOLS_PAGE                = ('xpath', "//a[contains(text(), 'Media Gallery')]")
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
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER or localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.KAF_BLACKBOARD_EMBED_KALTURA_MEDIA:
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

    
    def switchToBlackboardEmbedKaltruaMedia(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.BB_EMBED_KALTURA_MEDIA_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_EMBED_KALTURA_MEDIA
            return True
                    
        if self.wait_visible(self.BB_EMBED_KALTURA_MEDIA_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_EMBED_KALTURA_MEDIA
            return True
        else:
            if self.swith_to_iframe(self.BB_EMBED_KALTURA_MEDIA_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_EMBED_KALTURA_MEDIA
        return True    
            

                
    def loginToBlackBoard(self, username, password, url=''):
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
    
    
    # Author: Michal Zomper
    def navigateToGalleryBB(self, galleryName, forceNavigate=False):
        if forceNavigate == False:
            if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
                writeToLog("INFO","Success Already in my Gallery page")
                return True
        
        if galleryName == "New1":
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to courses 'New1'")
                return False
        sleep(5)
        
        self.clsCommon.blackBoard.switchToBlackboardIframe()
        if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        
        return True
        

    # @Author: Inbar Willman
    # enable = True - enable module
    # enable = false - disable  media
    # searchTerm = module name
    def enableDisableCourseModule(self, galleryName, searchTerm, moduleId, enable=True, isDisplay=True): 
        if self.navigateToCourseMenuOptionPage(galleryName) == False:
            writeToLog("INFO","FAILED to navigate to course home page")
            return False             
        
        if self.click(self.BB_ADD_COURSE_MODAL) == False:
            writeToLog("INFO","FAILED to click on 'Add course module'")
            return False 
        
        if self.searchInAddModule(searchTerm) == False:
            writeToLog("INFO","FAILED to make a search in 'Add module'")
            return False 
        
        tmp_add_module_element = (self.ADD_COURSE_MODULE_BTN[0], self.ADD_COURSE_MODULE_BTN[1].replace('MODULE_ID', moduleId))
        tmp_remove_module_element = (self.REMOVE_COURSE_MODULE_BTN[0], self.REMOVE_COURSE_MODULE_BTN[1].replace('MODULE_ID', moduleId))
        
        if enable == True:
            #If 'remove' button is visible, click on remove and then add
            if self.wait_visible(tmp_remove_module_element, timeout=3) != False:
                if self.click(tmp_remove_module_element) == False:
                    writeToLog("INFO","FAILED to remove " + searchTerm)
                    return False 
            
            # Click on 'add' button    
            if self.click(tmp_add_module_element) == False:
                    writeToLog("INFO","FAILED to add " + searchTerm)
                    return False                 
    
        else:
            #if 'add' button is is visible, click on add and then remove
            if self.wait_visible(tmp_add_module_element) != False:
                if self.click(tmp_add_module_element) == False:
                    writeToLog("INFO","FAILED to add " + searchTerm)
                    return False 

            if self.click(tmp_remove_module_element) == False:
                writeToLog("INFO","FAILED to remove " + searchTerm)
                return False 
            
        if self.veifyModuleDisplay(searchTerm, isDisplay) == False:
            writeToLog("INFO","FAILED verify " + searchTerm + " displayed")
            return False   
        
        return True                                                                        
             
        
    # @Author: Inbar Willman
    # Make a search in 'Add module'
    def searchInAddModule(self, searchTerm):                        
        if self.click(self.BB_COURSE_ADD_MODULE_SEARCH_FIELD) == False:
            writeToLog("INFO","FAILED to click on search field")
            return False  
        
        if self.send_keys(self.BB_COURSE_ADD_MODULE_SEARCH_FIELD, searchTerm) == False:
            writeToLog("INFO","FAILED to insert search term in search field")
            return False  
        
        if self.click(self.BB_COURSE_ADD_MODULE_SEARCH_SUBMIN_BTN) == False:
            writeToLog("INFO","FAILED to click on submit search button")
            return False  
        
        return True     
    
    
    # @Author: Inbar Willman
    # Verify if featured media is displayed in media gallery home page
    # isDisplay = True - Featured media should be displayed
    # isDisplay = False - Featured media shouldn't be displayed
    def veifyModuleDisplay(self, moduleName, isDisplay=True): 
        tmpHomePageOption = (self.BB_COURSE_PAGE[0], self.BB_COURSE_PAGE[1].replace('COURSE_PAGE', 'Home Page'))  
        if self.click(tmpHomePageOption) == False:
            writeToLog("INFO","FAILED to click on home page")
            return False 
        
        tmp_module_name = (self.COURSE_MODULE_NAME[0], self.COURSE_MODULE_NAME[1].replace('MODULE_NAME', moduleName)) 
        if isDisplay == True:
            if self.is_visible(tmp_module_name) == False:
                writeToLog("INFO","FAILED to display " + moduleName)
                return False  
        else:
            if self.wait_visible(tmp_module_name, 3) != False:
                writeToLog("INFO","FAILED " + moduleName + " is displayed altough it shouldn't be")
                return False  
            
            
    # @Author: Inbar Willman
    # Click on 'featured media' icon for entry
    def clickOnFeaturedMediaIcon(self, entryName):
        #Refresh the page
#         if self.clsCommon.kafGeneric.clickOnMediaGalleryRefreshNowButton() == False:
#             writeToLog("INFO","FAILED to click on 'refresh now' button")
#             return False
        
        self.click(self.clsCommon.kafGeneric.KAF_REFRSH_BUTTON)
        sleep(6)
        
        if self.click(self.DETAILED_VIEW, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on detailed view button")
            return False
        sleep(2)
        
        # Get entry element 
        tmp_entry = (self.BB_MEDIA_GALLERY_ENTRY_NAME[0], self.BB_MEDIA_GALLERY_ENTRY_NAME[1].replace('ENTRY_NAME', entryName))      
        entry_element = self.wait_element(tmp_entry)
        if entry_element == False:
            writeToLog("INFO","FAILED to get BB_MEDIA_GALLERY_ENTRY_NAME element")
            return False
             
        # Get entry id      
        tmp_entry_id = entry_element.get_attribute("href").split("/")
        entry_id = tmp_entry_id[5]
        
        featuredMediaIcon = (self.FEATURED_MEDIA_ICON[0], self.FEATURED_MEDIA_ICON[1].replace('ENTRY_NAME', entry_id))
        if self.hover_on_element(featuredMediaIcon) == False:
            writeToLog("INFO","FAILED to hover on featured media button")
            return False  
                
        if self.click(featuredMediaIcon, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on featured media button")
            return False  
        
        self.clsCommon.general.waitForLoaderToDisappear()
            
        return True                                                   
      
    
    # Author: Michal Zomper
    def navigateToSharedRepositoryInBB(self):
        self.switchToBlackboardIframe()
        tmpGalleryTitle = (self.clsCommon.channel.CHANNEL_PAGE_TITLE[0], self.clsCommon.channel.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', "Shared Repository"))
        if self.wait_element(tmpGalleryTitle, 5) == True:
            writeToLog("INFO","Success Already in Shared Repository page")
            return False
        
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_SHARED_REPOSITORY_URL) == False:
                writeToLog("INFO","FAILED navigate to Shared Repository page")
                return False
        sleep(5)
        
        self.switchToBlackboardIframe()
        if self.wait_element(tmpGalleryTitle, 15) == False:
            writeToLog("INFO","FAILED navigate to Shared Repository page")
            return False
        
        return True
        
    
    # Author: Michal Zomper
    def addRemoveSharedRepositoryModule(self, isEnable):
        self.clsCommon.base.switch_to_default_content()
        tmpGalleryTitle = (self.clsCommon.channel.CHANNEL_PAGE_TITLE[0], self.clsCommon.channel.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', "Shared Repository"))
        if isEnable == True:
            #check if SR button already exist
            if self.wait_visible(self.BB_SHARED_REPOSITORY_BUTTON, 5) != False:
                writeToLog("INFO","Success Shared Repository button exist")
                return True
            
            # SR button doesn't exist - going to add module 
            else:
                if self.click(self.BB_MODLUES_PAGE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on add module button")
                    return False   
                try:
                    sRElement = self.get_element(self.BB_SHARED_REPOSITORY_BUTTON)
                    
                    sRparentElement = sRElement.find_element_by_xpath("../../..")
                    sRID = sRparentElement.get_attribute("id")
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to fined 'shared repository' module in modules page")
                    return False   
                
                if sRID != '':
                    tmpID = sRID.split(":")
    
                tmpAddButton = (self.BB_ADD_MODULE_BUTTON[0], self.BB_ADD_MODULE_BUTTON[1].replace('ID', tmpID[1] + ":" + tmpID[2]))
                if self.click(tmpAddButton) == False:
                    writeToLog("INFO","FAILED to click on 'add' shared repository module button")
                    return False   
                
                if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_KAF_BLACKBOARD_BASE_URL) == False:
                    writeToLog("INFO","FAILED navigate to blackboard main page")
                    return False
                    
                if self.wait_visible(self.BB_SHARED_REPOSITORY_BUTTON, 10) == False:
                    writeToLog("INFO","FAILED, Shared Repository module doesn't exist in blackboard main page although the module was added")
                    return False
                
            if self.click(self.BB_SHARED_REPOSITORY_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Shared Repository button")
                return False
            
            sleep(5)   
            self.clsCommon.blackBoard.switchToBlackboardIframe()
            if self.wait_visible(tmpGalleryTitle, 30) == False:
                writeToLog("INFO","FAILED navigate to Shared Repository page")
                return False
            
            writeToLog("INFO","Success Shared Repository module was added successfully")
            return True
            
        elif isEnable == False:
            #check if SR button dosn't exist
            if self.wait_visible(self.BB_SHARED_REPOSITORY_BUTTON, 5) == False:
                writeToLog("INFO","Success Shared Repository button doesn't exist")
                return True
            
            else: 
                # SR button exist - going to remove module 
                if self.click(self.BB_MODLUES_PAGE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on add module button")
                    return False   
                try:
                    sRElement = self.get_element(self.BB_SHARED_REPOSITORY_BUTTON)
                    
                    sRparentElement = sRElement.find_element_by_xpath("../../..")
                    sRID = sRparentElement.get_attribute("id")
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to fined 'shared repository' module in modules page")
                    return False   
                
                if sRID != '':
                    tmpID = sRID.split(":")
                
                tmpRemoveButton = (self.BB_REMOVE_MODULE_BUTTON[0], self.BB_REMOVE_MODULE_BUTTON[1].replace('ID', tmpID[1] + ":" + tmpID[2]))
                if self.click(tmpRemoveButton) == False:
                    writeToLog("INFO","FAILED to click on 'remove' shared repository module button")
                    return False   
                
                if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_KAF_BLACKBOARD_BASE_URL) == False:
                    writeToLog("INFO","FAILED navigate to blackboard main page")
                    return False
                    
                if self.wait_visible(self.BB_SHARED_REPOSITORY_BUTTON, 10) != False:
                    writeToLog("INFO","FAILED, Shared Repository module exist in blackboard main page although the module was removed")
                    return False
                
                writeToLog("INFO","Success Shared Repository module was removed successfully")
                return True
            
    
    # Author: Michal Zomper
    def addSharedRepositoryMetadata(self, entryName, requiredField, location=enums.Location.EDIT_ENTRY_PAGE):
        if location == enums.Location.EDIT_ENTRY_PAGE:
            if self.clsCommon.editEntryPage.navigateToEditEntryPageFromMyMedia(entryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' edit page")
                return False  
         
        if self.click(self.BB_SHARED_REPOSITORY_ADD_REQUIRED_METADATA_BUTTON) == False:
            writeToLog("INFO","FAILED to click on add required metadata to shared repository button")
            return False
        
        try:
            tmpRequiredMetadata = self.get_elements(self.BB_SHARED_REPOSITORY_REQUIRED_METADATA_FIELD)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to find required metadata field element for shared repository")
            return False
        
        isElementFound = False
        for tmpMetadata in tmpRequiredMetadata:
            if requiredField == tmpMetadata.text:
                if self.clickElement(tmpMetadata) == False:
                    writeToLog("INFO","FAILED to click required metadata field for shared repository")
                    return False
                isElementFound = True
                break
            
        if isElementFound == False:
            writeToLog("INFO","FAILED to find required metadata field for shared repository")
            return False
            
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SAVE_BUTTON, 15) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        
        if location == enums.Location.EDIT_ENTRY_PAGE:
            if self.wait_visible(self.clsCommon.editEntryPage.EDIT_ENTRY_UPLOAD_SUCCESS_MSG) == False:
                writeToLog("INFO","FAILED to find publish success message")
                return False
            
        elif location == enums.Location.SHARED_REPOSITORY:
            if self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_SAVE_MESSAGE_CONFIRM) == False:
                writeToLog("INFO","FAILED to find save success message")
                return False
        
        writeToLog("INFO","Success required metadata was saved successfully")
        return True
            

    # @Author: Inbar Willman
    # Navigate to home page in course
    def navigateToCourseMenuOptionPage(self, galleryName, BBCoursePages=enums.BBCoursePages.HOME_PAGE):
        if self.navigateToGalleryBB(galleryName) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        
        if self.clsCommon.base.switch_to_default_content() == False:
            writeToLog("INFO","FAILED to switch to BB frame")
            return False  
        
        tmpCoursePage = (self.BB_COURSE_PAGE[0], self.BB_COURSE_PAGE[1].replace('COURSE_PAGE', BBCoursePages.value))           
        
        if self.click(tmpCoursePage) == False:
            writeToLog("INFO","FAILED to click on " + BBCoursePages.value + " page")
            return False 
        
        return True
    
    
    # @Author: Inbar Willman
    # Verify that featured entry is displayed under featured media section   
    # shouldBeDisplayed=True - Entry should be displayed in featured media
    # shouldBeDisplayed=False Entry shouldn't be displayed in featured media
    def verifyEntryInFeaturedMedia(self, galleryName, entryName, shouldBeDisplayed=True):
        if self.navigateToCourseMenuOptionPage(galleryName) == False:
            writeToLog("INFO","FAILED to navigate to course: " + galleryName + " home page")   
            return False  
        
        # We don't use 'self.clsCommon.player.switchToPlayerIframe(False)' method because it's different player iframe locator.
        # Because we have only one iframe on the page, we can locate the iframe by 'tag_name'
        if self.swith_to_iframe(('tag_name','iframe')) == False:
            writeToLog("INFO","FAILED to switch to featured media player iframe")   
            return False
        else:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER
        
        # Verify that entry is displayed or not displayed in featured media section
        if shouldBeDisplayed == False:
            carouselItemEl = self.wait_element(self.FEATURED_MEDIA_ENTRY, timeout=3)
            if carouselItemEl != False:
                if entryName in carouselItemEl.text:
                    writeToLog("INFO","FAILED: Entry shouldn't be displayed " + entryName + " in featured media")
                    return False                 
                else:
                    writeToLog("INFO","Success: Entry isn't displayed in featured media")
                    return True 
            else:
                if not entryName in carouselItemEl.text:
                    writeToLog("INFO","Success: Entry isn't displayed in featured media")
                    return True 
                else:
                    writeToLog("INFO","FAILED: Entry shouldn't be displayed " + entryName + " in featured media")   
                    return False                      
            
        # shouldBeDisplayed == True     
        else:        
            carouselItemEl = self.wait_element(self.FEATURED_MEDIA_ENTRY, timeout=3)
            if carouselItemEl == False:
                writeToLog("INFO","FAILED to display " + entryName + " in course featured media")   
                return False
            else:
                if entryName in carouselItemEl.text:
                    writeToLog("INFO","Success: Entry is displayed in featured media")
                    return True 
                else:
                    writeToLog("INFO","FAILED to display " + entryName + " in course featured media")   
                    return False                  
        
            self.clsCommon.sendKeysToBodyElement(Keys.END)
        
            sleep(2)
        
            # Verify that entry is played in featured media section
            if self.clsCommon.player.clickPlayPauseAndVerify('0:09', clickPlayFromBarline=True) == False:
                writeToLog("INFO","FAILED to play and verify entry")
                return False
        
        return True     
    
    
    # @Author: Inbar Willman
    # Navigate to content embed page
    # menu - bulid content, assessments or tools
    # menu option (Enum) - one of the menu options from the menus above
    def navigateToContentEmbedPage(self,galleryName, BBCoursePages=enums.BBCoursePages.CONTENT, menu=enums.BBContentPageMenus.BUILD_CONTENT, menuOption=enums.BBContentPageMenusOptions.ITEM):  
        #Navigate to content page 
        if self.navigateToCourseMenuOptionPage(galleryName, BBCoursePages) == False:
            writeToLog("INFO","FAILED to navigate to " + galleryName + "Content page")
            return False
        
        # Choose menu 
        tmpMenu = (self.BB_CONTENT_PAGE_MENU[0], self.BB_CONTENT_PAGE_MENU[1].replace('MENU_NAME', menu.value))
        if self.click(tmpMenu) == False:
            writeToLog("INFO","FAILED to click on " + menu.value + " menu")
            return False 
        
        # If announcements option is chosen need to click 'more tools' before clicking announcements option
        if menuOption == enums.BBContentPageMenusOptions.ANNOUNCEMENTS:
            if self.click(self.BB_CONTENT_TOOLS_MENU_MORE_TOOLS_OPTION) == False:
                writeToLog("INFO","FAILED to click on " + menuOption.value + " option")
                return False
            
            tmpMenuOption = self.BB_CONTENT_ANNOUNCEMENTS_OPTION
            
        else:
            tmpMenuOption = (self.BB_CONTENT_PAGE_MENU_OPTION[0], self.BB_CONTENT_PAGE_MENU_OPTION[1].replace('MENU_OPTION', menuOption.value))          
          
        if self.click(tmpMenuOption) == False:
            writeToLog("INFO","FAILED to click on " + menuOption.value + " option")
            return False 
        
        # Verify that we are in the right page 
        if menuOption!= enums.BBContentPageMenusOptions.KALTURA_MEDIA: 
            tmpContentTypeTitle = (self.CONTENT_TYPE_TITLE[0], self.CONTENT_TYPE_TITLE[1].replace('CONTENT_TYPE', menuOption.value))
            if self.is_visible(tmpContentTypeTitle) == False:
                writeToLog("INFO","FAILED to displayed " + menuOption.value + " page")
                return False                  
            
        return True
        
    
    # @Author: Inbar Willman
    # Create embed item
    # chooseMediaGalleryinEmbed = False - Media gallery tab in embed page includes just one media gallery
    # chooseMediaGalleryinEmbed = True - Media gallery tab in embed page includes more than one media gallery
    def createEmbedItem(self, galleryName, entryName, itemName, imageThumbnail='', delayTime='', embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False, filePath='', description='', tags=''):
        if self.navigateToContentEmbedPage(galleryName) == False:
            writeToLog("INFO","FAILED to navigate to content item page")
            return False 
         
        #Insert item name
        if self.click(self.CONTENT_ITEM_NAME_FIELD) == False:
            writeToLog("INFO","FAILED to click on item name field")
            return False  
         
        if self.send_keys(self.CONTENT_ITEM_NAME_FIELD, itemName) == False:
            writeToLog("INFO","FAILED to add item name")
            return False                        
 
        # Get window before opening embed window
        window_before = self.clsCommon.base.driver.window_handles[0]
           
        if self.click(self.BB_EMBED_MASHUPS_BTN) == False:
            writeToLog("INFO","FAILED to click on mashups button")
            return False 
         
        if self.click(self.BB_EMBED_KALTURA_MEDIA_OPTION) == False:
            writeToLog("INFO","FAILED to click on kaltura media option")
            return False 
         
        sleep(2)
         
        # Get window after opening embed window and switch to this window
        window_after = self.clsCommon.base.driver.window_handles[1]
        self.clsCommon.base.driver.switch_to_window(window_after)
        
        # Select media in embed page 
        if self.clsCommon.kafGeneric.embedMedia(entryName, galleryName, embedFrom, chooseMediaGalleryinEmbed, filePath, description, tags) == False:
            writeToLog("INFO","FAILED to embed item in item page")
            return False  
         
        self.clsCommon.base.driver.switch_to_window(window_before)           
        
        #Submit item 
        if self.click(self.KAF_SUBMIT_BUTTON)  == False:
            writeToLog("INFO","FAILED to click on 'submit' button")
            return False    
         
        # Verify that Success message is displayed
        successMsg = (self.SUCCESS_CREATE_EMBED_MEDIA_MESSAGE[0], self.SUCCESS_CREATE_EMBED_MEDIA_MESSAGE[1].replace('ITEM_NAME', itemName))
        if self.is_visible(successMsg) == False:
            writeToLog("INFO","FAILED to display correct success message")
            return False             
                    
        return True     
    
    
    # @Author: Inbar Willman
    # Choose option for embed entry
    # menuOption - Delete/Edit/Move etc...
    def selectEmbedItemOption(self, galleryName, menuOption, contentName, BBCoursePages=enums.BBCoursePages.CONTENT):
        if self.navigateToCourseMenuOptionPage(galleryName, BBCoursePages) == False:
            writeToLog("INFO","FAILED to navigate to content item page")
            return False
        
        tmpEmbedContentMenu = (self.EMBED_CONTENT_DROP_DOWN[0], self.EMBED_CONTENT_DROP_DOWN[1].replace('CONTENT_NAME', contentName))
        
        if self.click(tmpEmbedContentMenu) == False:
            writeToLog("INFO","FAILED to click on embed item dropdown in content page")
            return  False  
        
        tmpEmbedOption = (self.EMBED_CONTENT_MENU_OPTION[0], self.EMBED_CONTENT_MENU_OPTION[1].replace('OPTION', menuOption))  
        
        self.clsCommon.base.hover_on_element(tmpEmbedOption)
        if self.click(tmpEmbedOption) == False:
            writeToLog("INFO","FAILED to click on " + menuOption + " option")
            return False                        
        
        return True       
    
    
    # @Author: Inbar Willman
    # Create embed kaltura media
    # chooseMediaGalleryinEmbed = False - Media gallery tab in embed page includes just one media gallery
    # chooseMediaGalleryinEmbed = True - Media gallery tab in embed page includes more than one media gallery
    def createEmbedKalturaMedia(self, galleryName, entryName, itemName, imageThumbnail='', delayTime='', embedFrom=enums.Location.MEDIA_GALLARY, chooseMediaGalleryinEmbed=False, filePath='', description ='', tags=''):
        if self.navigateToContentEmbedPage(galleryName, BBCoursePages=enums.BBCoursePages.CONTENT, menu=enums.BBContentPageMenus.BUILD_CONTENT, menuOption=enums.BBContentPageMenusOptions.KALTURA_MEDIA) == False:
            writeToLog("INFO","FAILED to navigate to content kaltura media page")
            return False 
         
        self.switchToBlackboardEmbedKaltruaMedia()
 
        if self.clsCommon.kafGeneric.embedMedia(entryName, galleryName, embedFrom, chooseMediaGalleryinEmbed, filePath, description, tags) == False:
            writeToLog("INFO","FAILED to embed item in item page")
            return False 
         
        self.switch_to_default_content()
 
        #Insert kaltura media name
        if self.click(self.CONTENT_KALTURA_MEDIA_NAME_FIELD) == False:
            writeToLog("INFO","FAILED to click on item name field")
            return False  
          
        if self.send_keys(self.CONTENT_KALTURA_MEDIA_NAME_FIELD, itemName) == False:
            writeToLog("INFO","FAILED to add item name")
            return False
         
        if self.click(self.KAF_SUBMIT_BUTTON)  == False:
            writeToLog("INFO","FAILED to click on 'submit' button")
            return False              
                    
        return True      
    
    
    # @Author: Inbar Willman
    # Delete embed item
    def deleteEmbedItem(self, galleryName, menuOption, contentName, BBCoursePages=enums.BBCoursePages.CONTENT, embedOption=enums.BBContentPageMenusOptions.ITEM):
        if self.selectEmbedItemOption(galleryName, menuOption, contentName, BBCoursePages) == False:
            writeToLog("INFO","FAILED to select delete option")
            return False 
        
        sleep(2)
       
        if self.clsCommon.base.click_dialog_accept() == False:
            writeToLog("INFO","FAILED click accept dialog")
            return False 
        if embedOption == enums.BBContentPageMenusOptions.ANNOUNCEMENTS:
            tmpDeleteMessage = (self.SUCCESS_DELETE_EMBED_ANNOUNCEMENTS_MESSAGE[0], self.SUCCESS_DELETE_EMBED_ANNOUNCEMENTS_MESSAGE[1].replace('ITEM_NAME', contentName))
        else:
            tmpDeleteMessage = (self.SUCCESS_DELETE_EMBED_MEDIA_MESSAGE[0], self.SUCCESS_DELETE_EMBED_MEDIA_MESSAGE[1].replace('ITEM_NAME', contentName))
             
        if self.is_visible(tmpDeleteMessage) == False:
            writeToLog("INFO","FAILED display delete message")
            
            return False                        
        
        return True     
    
    
    # @Author: Inbar Willman
    def createEmbedAnnouncemnets(self, galleryName, entryName, itemName, imageThumbnail='', delayTime='', embedFrom=enums.Location.SHARED_REPOSITORY, chooseMediaGalleryinEmbed=False, mediaType=enums.MediaType.VIDEO):
        if self.navigateToContentEmbedPage(galleryName, BBCoursePages=enums.BBCoursePages.CONTENT, menu=enums.BBContentPageMenus.TOOLS, menuOption=enums.BBContentPageMenusOptions.ANNOUNCEMENTS) == False:
            writeToLog("INFO","FAILED to navigate to announcements page")
            return False
        
        if self.clear_and_send_keys(self.CONTENT_ANNOUNCEMENTS_NAME_FIELD, itemName) == False:
            writeToLog("INFO","FAILED clear name field and send new name")
            return False  
        
        # Get window before opening embed window
        window_before = self.clsCommon.base.driver.window_handles[0]
        
        if self.click(self.BB_EMBED_MASHUPS_BTN) == False:
            writeToLog("INFO","FAILED to click on mashups button")
            return False 
         
        if self.click(self.BB_EMBED_KALTURA_MEDIA_OPTION) == False:
            writeToLog("INFO","FAILED to click on kaltura media option")
            return False 
         
        sleep(2)
         
        # Get window after opening embed window and switch to this window
        window_after = self.clsCommon.base.driver.window_handles[1]
        self.clsCommon.base.driver.switch_to_window(window_after)
        
        # Select media in embed page 
        if self.clsCommon.kafGeneric.embedMedia(entryName, galleryName, embedFrom, chooseMediaGalleryinEmbed) == False:
            writeToLog("INFO","FAILED to embed item in item page")
            return False  
         
        self.clsCommon.base.driver.switch_to_window(window_before)          
        
        if self.click(self.KAF_SUBMIT_BUTTON)  == False:
            writeToLog("INFO","FAILED to click on 'submit' button")
            return False         
            
        successMsg = (self.SUCCESS_CREATE_EMBED_MEDIA_MESSAGE[0], self.SUCCESS_CREATE_EMBED_MEDIA_MESSAGE[1].replace('ITEM_NAME', "Link " +itemName))
        if self.is_visible(successMsg) == False:
            writeToLog("INFO","FAILED to display correct success message")
            return False 
        
#         if self.clsCommon.kafGeneric.verifyEmbedEntry(imageThumbnail, delayTime, mediaType) == False:
#             writeToLog("INFO","FAILED to played and verify embedded entry")
#             return False             
                    
        return True  
       
         
    # @Author: Inbar Willman
    # Navigate to upload page via SR page
    def navigateToUploadMediaInSR(self):
        if self.navigateToSharedRepositoryInBB() == False:
            writeToLog("INFO","FAILED to navigate to SR page")
            return False 
            
        self.switchToBlackboardIframe()
        
        if self.click(self.BB_ADD_MEDIA_TO_SR_BTN, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on 'add media' button in SR page")
            return False 
        
        self.clsCommon.general.waitForLoaderToDisappear()
        
        if self.click(self.BB_ADD_NEW_MEDIA_TO_SR_BTN) == False:
            writeToLog("INFO","FAILED to click on 'add new media' button in SR page")
            return False 
        
        if self.click(self.clsCommon.upload.DROP_DOWN_MEDIA_UPLOAD_BUTTON)  == False:
            writeToLog("INFO","FAILED to click on 'media upload' option")
            return False      
        
        return True
    
    # @Author: Inbar Willman, Michal Zomper, Oleg Sigalov
    # Verify embed entry (video/image) in page
    def verifyBlackboardEmbedEntry(self, embedTitle, imageThumbnail='', delay=''):
        self.refresh()
        self.clsCommon.base.switch_to_default_content()
        
        tmpEmbedTitle= (self.clsCommon.kafGeneric.KAF_EMBED_TITLE_AFTER_CREATE_EMBED[0], self.clsCommon.kafGeneric.KAF_EMBED_TITLE_AFTER_CREATE_EMBED[1].replace('EMBED_TITLE', embedTitle))
        try:
            embedNameElment = self.get_element(tmpEmbedTitle) 
            embedContainer = embedNameElment.find_element_by_xpath("../../..")
        except NoSuchElementException:
            writeToLog("INFO","FAILED to find embed container")
            return False
        
        try:  
            parentId = embedContainer.get_attribute("id")
        except Exception:
            writeToLog("INFO","FAILED to get_attribute('id')")
            return False     
                          
        if parentId == "":
            writeToLog("INFO","FAILED to get id attribute from embed container")
            return False 
            
        m = re.search('(_\d\d\d_)', parentId)
        if m:
            foundId = m.group(1)
        else:
            writeToLog("INFO","FAILED to get id from string: '" + str(parentId) + "'")
            return False             
                
        iframeElment = self.wait_element(('xpath', "//iframe[contains(@src, 'content_id=" + foundId + "')]"))
        if iframeElment == False:
            writeToLog("INFO","FAILED to get player iframe")
            return False 
          
        try:  
            self.driver.switch_to.frame(iframeElment)
        except Exception:
            writeToLog("INFO","FAILED to switch to '//iframe[contains(@src, 'content_id=' iframe")
            return False  
                        
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        sleep(2)
        # If we are in blackboard need to click on play icon in order to get the player
        if self.click(self.EMBED_ENTRY_PLAY_ICON, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on play icon")
            return False 
         
        sleep(10)
        if delay != '':
            try:   
                self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[starts-with(@src, '/webapps/osv-kaltura-BBLEARN/LtiMashupPlay') and contains(@src, 'content_id=" + parentId[1] + "')]"))
            except Exception:
                writeToLog("INFO","FAILED to switch to '/webapps/osv-kaltura-BBLEARN/LtiMashupPlay' iframe")
                return False                      
            
            try: 
                self.driver.switch_to.frame(self.wait_element(self.clsCommon.player.PLAYER_IFRAME, 60))
                localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER
            except Exception:
                writeToLog("INFO","FAILED to switch to PLAYER_IFRAME iframe")
                return False    
                            
            if self.clsCommon.player.clickPlayPauseAndVerify(delay) == False:
                writeToLog("INFO","FAILED to play and verify video")
                return False                
        
        else:
            if self.clsCommon.player.verifyThumbnailInPlayer(imageThumbnail) == False:
                writeToLog("INFO","FAILED to display correct image thumbnail")
                return False   
    
        writeToLog("INFO","Embed media was successfully verified")    
        return True                                