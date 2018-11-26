from base import *
from general import General
import localSettings
from logger import *
from _ast import Is


class BlackBoard(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #====================================================================================================================================
    #Login locators:
    #====================================================================================================================================
    LOGIN_USERNAME_FIELD                    = ('id', 'user_id')
    LOGIN_PASSWORD_FIELD                    = ('id', 'password')
    LOGIN_SIGN_IN_BTN                       = ('id', 'entry-login')
    USER_MENU_TOGGLE_BTN                    = ('id', 'global-nav-link')
    USER_LOGOUT_BTN                         = ('id', 'topframe.logout.label')
    BB_MEDIA_SPACE_IFRAME                   = ('xpath', "//iframe[contains(@src,'/webapps/osv-kaltura-BBLEARN/')]")
    BB_COURSE_HOME_PAGE                     = ('xpath', '//span[@title="Home Page" and text()="Home Page"]')
    BB_ADD_COURSE_MODAL                     = ('xpath', '//a[contains(@href,"/webapps/portal/execute/tabs/tabManageModules") and text()="Add Course Module"]')
    BB_COURSE_ADD_MODULE_SEARCH_FIELD       = ('xpath','//input[@id="txtSearch"]')
    BB_COURSE_ADD_MODULE_SEARCH_SUBMIN_BTN  = ('xpath', '//input[@type="submit" and @value="Go"]')
    ADD_COURSE_MODULE_BTN                   = ('xpath', '//a[@id="MODULE_ID:-1addButton"]')
    REMOVE_COURSE_MODULE_BTN                = ('xpath', '//a[@id="MODULE_ID:-1removeButton"]')     
    COURSE_MODULE_NAME                      = ('xpath','//span[@class="moduleTitle" and text()="MODULE_NAME"]')   
    BB_MEDIA_GALLERY_ENTRY_NAME             = ('xpath', '//a[@class="item_link" and text()="ENTRY_NAME"]')  
    FEATURED_MEDIA_ICON                     = ('xpath', '//a[@id="featured_ENTRY_NAME"]')   
    DETAILED_VIEW                           = ('xpath', '//i[@class="icon-th-list"]') 
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
    
    
    # Author: Michal Zomper
    def navigateToGalleryBB(self, galleryName):
        if self.wait_visible(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
            writeToLog("INFO","Success Already in my Gallery page")
            return True
        
        if galleryName == "New1":
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","FAILED navigate to courses 'New1'")
                return False
        sleep(5)
        
        self.clsCommon.blackBoard.switchToBlackboardIframe()
        if self.wait_visible(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        
        return True
        

    # @Author: Inbar Willman
    # enable = True - enable module
    # enable = false - disable  media
    # searchTerm = module name
    def enableDisableCourseModule(self, galleryName, searchTerm, moduleId, enable=True, isDisplay=True):
        if self.navigateToGalleryBB(galleryName) == False:
            writeToLog("INFO","FAILED navigate to to courses 'New1'")
            return False
        
        if self.clsCommon.base.switch_to_default_content() == False:
            writeToLog("INFO","FAILED to switch to BB frame")
            return False               
        
        if self.click(self.BB_COURSE_HOME_PAGE) == False:
            writeToLog("INFO","FAILED to click on home page")
            return False 
        
        if self.click(self.BB_ADD_COURSE_MODAL) == False:
            writeToLog("INFO","FAILED to click on 'Add course module'")
            return False 
        
        if self.searchInAddModule(searchTerm) == False:
            writeToLog("INFO","FAILED to make a search in 'Add module'")
            return False 
        
        if enable == True:
            tmp_add_module_element = (self.ADD_COURSE_MODULE_BTN[0], self.ADD_COURSE_MODULE_BTN[1].replace('MODULE_ID', moduleId)) 
            if self.click(tmp_add_module_element) == False:
                writeToLog("INFO","FAILED to add " + searchTerm)
                return False 
        else:
            tmp_remove_module_element = (self.REMOVE_COURSE_MODULE_BTN[0], self.REMOVE_COURSE_MODULE_BTN[1].replace('MODULE_ID', moduleId)) 
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
        if self.click(self.BB_COURSE_HOME_PAGE) == False:
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
        if self.click(self.DETAILED_VIEW) == False:
            writeToLog("INFO","FAILED to click on detailed view button")
            return False  
        
        # Get entry element 
        tmp_entry = (self.BB_MEDIA_GALLERY_ENTRY_NAME[0], self.BB_MEDIA_GALLERY_ENTRY_NAME[1].replace('ENTRY_NAME', entryName))      
        entry_element = self.wait_visible(tmp_entry)
        
        # Get entry id      
        tmp_entry_id = entry_element.get_attribute("href").split("/")
        entry_id= tmp_entry_id[5]
        
        featuredMediaIcon =  (self.FEATURED_MEDIA_ICON[0], self.FEATURED_MEDIA_ICON[1].replace('ENTRY_NAME', entry_id))
        if self.click(featuredMediaIcon) == False:
            writeToLog("INFO","FAILED to click on featured media button")
            return False  
            
        return True                                                   