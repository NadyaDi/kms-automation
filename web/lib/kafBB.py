from base import *
from general import General
import localSettings
from logger import *


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
    BB_SHARED_REPOSITORY_DISCLAIMER_MSG_BEFOR_PUBLISH   = ('xpath', "//div[@class='alert ' and contains(text(), 'Complete all the required fields and save the entry before you can select to publish it to shared repositories.')]")
    BB_SHARED_REPOSITORY_ADD_REQUIRED_METADATA_BUTTON   = ('xpath', "//label[@class='inline sharedRepositoryMetadata collapsed']")
    BB_SHARED_REPOSITORY_REQUIRED_METADATA_FIELD        = ('xpath', "//span[@class='inline' and contains(text(), 'FIELD_NAME')]")
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
    def navigateToGalleryBB(self, galleryName, forceNavigate=False):
        if forceNavigate == False:
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
        
    
    # Author: Michal Zomper
    def navigateToSharedRepositoryInBB(self):
        tmpGalleryTitle = (self.clsCommon.channel.CHANNEL_PAGE_TITLE[0], self.clsCommon.channel.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', "Shared Repository"))
        if self.wait_visible(tmpGalleryTitle, 5) == True:
            writeToLog("INFO","Success Already in Shared Repository page")
            return False
        
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_SHARED_REPOSITORY_URL) == False:
                writeToLog("INFO","FAILED navigate to Shared Repository page")
                return False
        
        if self.wait_visible(tmpGalleryTitle, 15) == True:
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
    def addSharedRepositoryMetadata(self, entryName, RequiredField):
        if self.clsCommon.myMedia.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED navigate to entry '" + entryName + "' edit page")
            return False  
        
        if self.click(self.BB_SHARED_REPOSITORY_ADD_REQUIRED_METADATA_BUTTON) == False:
            writeToLog("INFO","FAILED to click on add required metadata to shared repository button")
            return False
        
        tmRequiredField = (self.BB_SHARED_REPOSITORY_REQUIRED_METADATA_FIELD[0], self.BB_SHARED_REPOSITORY_REQUIRED_METADATA_FIELD[1].replace('FIELD_NAME', RequiredField))
        if self.check_element(tmRequiredField, True) == False:
            writeToLog("INFO","FAILED to checked required metadata field for shared repository")
            return False
        
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SAVE_BUTTON, 15) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False
        
        if self.wait_visible(self.clsCommon.editEntryPage.EDIT_ENTRY_UPLOAD_SUCCESS_MSG) == False:
            writeToLog("INFO","FAILED to find save success message")
            return False
        
        writeToLog("INFO","Success required metadata was saved successfully")
        return True
            
            
    
