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
    #USER_LOGOUT_BTN                                     = ('xpath', "//button[@type='submit']")
    USER_LOGOUT_BTN                                     = ('xpath', "//span[@class='Button__dUxGkD-content' and contains(text(), 'Logout')]")
    CANVAS_MEDIA_SPACE_IFRAME                           = ('xpath', "//iframe[@id='tool_content']")
    CANVAS_MY_MEDIA_BUTTON_IN_NAV_BAR                   = ('xpath', "//a[contains(@class, 'ontext_external_tool') and @title='My Media']")
    CANVAS_MEDIA_GALLERY_BUTTON_IN_NAV_BAR              = ('xpath', "//a[contains(@class, 'ontext_external_tool') and @title='Media Gallery']")
    CANVAS_DASHBOARD_BUTTON_IN_NAV_BAR                  = ('xpath', "//a[@id='global_nav_dashboard_link']")
    CANVAS_GALLERY_NEW1_IN_DASHBOARD_MENU               = ('xpath', "//div[@class='ic-DashboardCard' and @aria-label='New1']")
    CANVAS_USER_NAME                                    = ('xpath', "//h2[@class='View__ehkxkl-root Heading__fsRVvb-root Heading__fsRVvb-h3 Heading__fsRVvb-color-inherit']")
    CANVAS_ANNOUNCEMENTS_TAB                            = ('xpath', '//a[@title="Announcements"]')
    CANVAS_CREATE_ANNOUNCEMENT_BTN                      = ('xpath', '//a[@id="add_announcement"]')
    CANVAS_ANNOUNCEMENTS_TITLE                          = ('xpath', '//input[@id="discussion-title"]')
    CANVAS_WYSIWYG                                      = ('xpath', '//button[@id="mceu_21-button"]')
    CANVAS_SAVE_ANNOUNCEMENT_BTN                        = ('xpath', '//button[@type="submit" and text()="Save"]')
    CANVAS_EMBED_ANNOUNCEMENTS_TITLE                    = ('xpath', '//h3[@data-ui-testable="Heading" and text()="EMBED_ANNOUNCEMENT_NAME"]')
    CANVAS_EMBED_IFRAME                                 = ('xpath', '//iframe[@id="external_tool_button_frame"]')
    CANVAS_ANNOUNCEMNET_ACTION_DROPDOWN                 = ('xpath', '//a[@class="al-trigger btn announcement_cog"]')
    CANVAS_DELETE_ANNOUNCEMENT_BTN                      = ('xpath' , '//a[contains(@class,"delete_discussion ui-corner-all")]')
    CANVAS_DELETE_ANNOUNCEMENT_SUCCESS_MSG              = ('xpath', '//li[@class="ic-flash-success"]') 
    CANVAS_EMBED_ENTRY_IFRAME                           = ('xpath', '//iframe[contains(@src, "/courses/471/external_tools")]')
    CANVAS_SHARED_REPOSITORY_ADD_REQUIRED_METADATA_BTN  = ('xpath', '//label[@class="collapsed inline sharedRepositoryMetadata"]')
    CANVAS_ENTRY_COURSE_FIELD_DROPDOWN                  = ('xpath', '//select[@id="sharedRepositories-Course"]')
    CANVAS_ENTRY_COURSE_FIELD_DROPDOWN_OPTION           = ('xpath', '//option[@value="VALUE"]')
    CANVAS_EMBED_UPLOAD_IFRAME                          = ('xpath', '//iframe[@id="external_tool_button_frame"]')
    CANVAS_ANNOUNCEMENT_DESCRIPTION_IFRAME              = ('xpath', '//iframe[contains(@id,"discussion-topic")]') 
    CANVAS_ADD_ASSIGNMENT_BTN                           = ('xpath', '//a[@title="Add Assignment"]')
    CANVAS_ASSIGNMENT_TITLE                             = ('xpath', '//input[@id="assignment_name"]')
    CANVAS_ASSIGNEMNT_SUBMISSION_TYPE_DROPDOWN          = ('xpath', '//select[@id="assignment_submission_type"]')
    CANVAS_ASSIGNEMNT_EXTERNAL_SUBMISSION_TYPE_OPTION   = ('xpath', '//option[@value="external_tool"]')
    CANVAS_FIND_EXTERNAL_TOOL_BTN                       = ('xpath', '//button[@id="assignment_external_tool_tag_attributes_url_find"]')
    CANVAS_KALTURA_VIDEO_QUIZ_EXTERNAL_TOOL_CONFIGURE   = ('xpath', '//a[@class="name" and text()="Gradebook"]')
    CANVAS_CONFIGURE_EXTERNAL_TOOL_TITLE                = ('xpath', '//span[@class="ui-dialog-title" and text()="Configure External Tool"]') 
    CANVAS_EXTERNAL_TOOL_IFRAME                         = ('xpath', '//iframe[@id="resource_selection_iframe"]')          
    CANVAS_CONFIGURE_EXTERNAL_TOOL_SELECT_BTN           = ('xpath', '//button[@class="add_item_button btn btn-primary ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only"]')  
    CANVAS_SAVE_AND_PUBLISH_ASSIGNMENT_BTN              = ('xpath', '//button[@class="btn btn-default save_and_publish"]')     
    CANVAS_ASSIGNMENT_POINTS_POSSIBLE                   = ('xpath', '//input[@id="assignment_points_possible"]')   
    CANVAS_ASSIGNMENT_NAME_IN_ASSIGNMENTS_PAGE          = ('xpath', '//a[@class="ig-title" and contains(text(), "ASSIGNMENT_NAME")]')
    CANVAS_ASSIGNMENT_GRADE_TITLE_FOR_ADMIN             = ('xpath', '//div[@title="ASSIGNMENT_NAME"]')
    CANVAS_ASSIGNMENT_GRADE_FOR_ADMIN                   = ('xpath', '//a[@class="gradebook-cell-comment" and @data-assignment-id="ID_NAME"]/..')
    CANVAS_ASSIGNMENT_GRADE_FOR_STUDENT                 = ('xpath', '//a[contains(@href,"/courses/471/assignments/") and text()="ASSIGNMENT_NAME"]/ancestor::tr[@class="student_assignment assignment_graded editable"]/descendant::span[@class="grade"]')
    CANVAS_ASSIGNMENT_DROP_DOWN                         = ('xpath', '//span[@class="screenreader-only" and contains(text(), "ASSIGNMENT_NAME")]/..')
    CANVAS_DELETE_ASSIGNMENT_OPTION                     = ('xpath', '//a[@aria-label="Delete Assignment ASSIGNMENT_NAME"]')
    CANVAS_ASSIGNMENT_PAGE_TITLE                        = ('xpath', '//h1[@class="title" and contains(text(), "ASSIGNMENT_NAME")]')    
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
        self.clsCommon.base.switch_to_default_content()
        # Click on account button in main nav bar 
        if self.click(self.USER_ACCOUNT_BUTTON_IN_NAV_BAR, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on account button in main nav bar ")
            return False
        
        sleep(10)
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
    def createEmbedAnnouncements(self, announcementTitle, entryName, mediaGalleryName=None, embedFrom=enums.Location.MY_MEDIA, chooseMediaGalleryinEmbed=False, filePath=None, description=None, tags=None, isTagsNeeded=True):
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
        if self.clsCommon.kafGeneric.embedMedia(entryName, mediaGalleryName, embedFrom, chooseMediaGalleryinEmbed, filePath, description, tags, application=enums.Application.CANVAS, isTagsNeeded=isTagsNeeded) == False:    
            writeToLog("INFO","FAILED to choose media in embed page")
            return False  
   
        # wait until the player display in the page
        self.switch_to_default_content()
        
        self.swith_to_iframe(self.CANVAS_ANNOUNCEMENT_DESCRIPTION_IFRAME)
        self.swith_to_iframe(self.CANVAS_EMBED_ENTRY_IFRAME) 
        
        self.clsCommon.player.switchToPlayerIframe()
        self.wait_element(self.clsCommon.player.PLAYER_CONTROLER_BAR, timeout=30)
        
        self.clsCommon.base.switch_to_default_content()  
        
        if self.click(self.CANVAS_SAVE_ANNOUNCEMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False 
        
        writeToLog("INFO","Success: Embed announcement was created successfully")
        return True    
    
    
    # @Author: Inbar Willman
    def verifyCanvasEmbedEntry(self, embedTitle, imageThumbnail, delay, forceNavigate=False,isQuiz=False):
        # Navigate to announcements page  
        if forceNavigate == True: 
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_ANNOUNCEMENTS_URL) == False:
                writeToLog("INFO","FAILED navigate to announcements page")
                return False     
                
            embed_anouncement = (self.CANVAS_EMBED_ANNOUNCEMENTS_TITLE[0], self.CANVAS_EMBED_ANNOUNCEMENTS_TITLE[1].replace('EMBED_ANNOUNCEMENT_NAME', embedTitle))
            if self.click(embed_anouncement) == False:
                writeToLog("INFO","FAILED to click on embed announcement name")
                return False   
                                                 
        self.swith_to_iframe(self.CANVAS_EMBED_ENTRY_IFRAME) 
        self.clsCommon.player.switchToPlayerIframe()
        self.wait_element(self.clsCommon.player.PLAYER_CONTROLER_BAR, timeout=30)
        self.clsCommon.base.switch_to_default_content()
        self.swith_to_iframe(self.CANVAS_EMBED_ENTRY_IFRAME) 
        sleep(5)
        
        # If entry type is video
        if delay != '':   
#            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER 
            if self.clsCommon.player.clickPlayPauseAndVerify(delay) == False:
                writeToLog("INFO","FAILED to play and verify video")
                return False                
        
        # If entry type is image     
        elif imageThumbnail !='':
            sleep(5)
            if self.clsCommon.player.verifyThumbnailInPlayer(imageThumbnail) == False:
                writeToLog("INFO","FAILED to display correct image thumbnail")
                return False
            
        elif isQuiz == True:
            writeToLog("INFO","Success: embed quiz was found in course page")
            return True             
        
        self.clsCommon.base.switch_to_default_content()
        writeToLog("INFO","Success embed was verified")
        return True    
    
    
    # @Author: Inbar Willman
    def deleteAnnouncemnt(self, announcementName, forceNavigate=False):   
        if forceNavigate == True:
            if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_ANNOUNCEMENTS_URL) == False:
                writeToLog("INFO","FAILED navigate to announcements page")
                return False     
                
            embed_anouncement = (self.CANVAS_EMBED_ANNOUNCEMENTS_TITLE[0], self.CANVAS_EMBED_ANNOUNCEMENTS_TITLE[1].replace('EMBED_ANNOUNCEMENT_NAME', announcementName))
            if self.click(embed_anouncement) == False:
                writeToLog("INFO","FAILED to click on embed announcement name")
                return False  
            
        if self.click(self.CANVAS_ANNOUNCEMNET_ACTION_DROPDOWN) == False:
            writeToLog("INFO","FAILED to click on announcement action dropdown menu")
            return False  
        
#         if self.hover_on_element(self.CANVAS_DELETE_ANNOUNCEMENT_BTN) == False:
#             writeToLog("INFO","FAILED to hover over 'delete' option")
#             return False   
           
        if self.click(self.CANVAS_DELETE_ANNOUNCEMENT_BTN, timeout=30) == False:
            writeToLog("INFO","FAILED to click on delete option")
            return False 
        
        if self.clsCommon.base.click_dialog_accept() == False:
            writeToLog("INFO","FAILED click accept dialog")
            return False 
        
        if self.wait_visible(self.CANVAS_DELETE_ANNOUNCEMENT_SUCCESS_MSG) == False:
            writeToLog("INFO","FAILED to displayed delete success message")
            return False 
        
        embed_anouncement = (self.CANVAS_EMBED_ANNOUNCEMENTS_TITLE[0], self.CANVAS_EMBED_ANNOUNCEMENTS_TITLE[1].replace('EMBED_ANNOUNCEMENT_NAME', announcementName))
        if self.click(embed_anouncement) == True:
            writeToLog("INFO","FAILED: announcement is still display in announcements page")
            return False 
        
        writeToLog("INFO","Success: announcement was deleted")
        return True             
    
    
    # @Author: Inbar Willman
    def addSharedRepositoryMetadataCanvas(self, entryName, sharedRepositoryMetadataValue, location=enums.Location.EDIT_ENTRY_PAGE):
        if location == enums.Location.EDIT_ENTRY_PAGE:
            if self.clsCommon.editEntryPage.navigateToEditEntryPageFromMyMedia(entryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' edit page")
                return False  
        
        self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_DETAILS_TAB) 
        self.get_body_element().send_keys(Keys.PAGE_DOWN)
        sleep(1)
        
        if self.click(self.CANVAS_SHARED_REPOSITORY_ADD_REQUIRED_METADATA_BTN) == False:
            writeToLog("INFO","FAILED to click on add required metadata to shared repository button")
            return False
        
        if self.click(self.CANVAS_ENTRY_COURSE_FIELD_DROPDOWN) == False:
            writeToLog("INFO","FAILED to click on course field dropdown")
            return False  
        
        metadataOption = (self.CANVAS_ENTRY_COURSE_FIELD_DROPDOWN_OPTION[0], self.CANVAS_ENTRY_COURSE_FIELD_DROPDOWN_OPTION[1].replace('VALUE', sharedRepositoryMetadataValue))
        if self.click(metadataOption) == False:
            writeToLog("INFO","FAILED to choose '" + sharedRepositoryMetadataValue + "' option in dropdown")
            return False                                    
             
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SAVE_BUTTON, 15) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False
         
        self.clsCommon.general.waitForLoaderToDisappear()

        return True      
    
    
    # @Author: Inbar Willman
    def createEmbedAssignment(self, assignmentTitle, entryName, ponitesPossible):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_ASSIGNMENTSS_URL) == False:
            writeToLog("INFO","FAILED navigate to assignment page")
            return False 
        
        if self.click(self.CANVAS_ADD_ASSIGNMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on create assignment button")
            return False             
        
        if self.send_keys(self.CANVAS_ASSIGNMENT_TITLE, assignmentTitle)   == False:
            writeToLog("INFO","FAILED to insert announcement title")
            return False 
        
        if self.clear_and_send_keys(self.CANVAS_ASSIGNMENT_POINTS_POSSIBLE, ponitesPossible) == False:
            writeToLog("INFO","FAILED to insert possible points")
            return False 
                     
        if self.click(self.CANVAS_ASSIGNEMNT_SUBMISSION_TYPE_DROPDOWN) == False:
            writeToLog("INFO","FAILED to click on submission type dropdown")
            return False 
                    
        if self.click(self.CANVAS_ASSIGNEMNT_EXTERNAL_SUBMISSION_TYPE_OPTION) == False:
            writeToLog("INFO","FAILED to click on 'external tool' option")
            return False  
        
        if self.click(self.CANVAS_FIND_EXTERNAL_TOOL_BTN) == False:
            writeToLog("INFO","FAILED to click on find external tool button")
            return False  
        
        if self.wait_element(self.CANVAS_CONFIGURE_EXTERNAL_TOOL_TITLE) == False:
            writeToLog("INFO","FAILED to display 'configure external tool' modal")
            return False                                  

        if self.click(self.CANVAS_KALTURA_VIDEO_QUIZ_EXTERNAL_TOOL_CONFIGURE) == False:
            writeToLog("INFO","FAILED to click on 'kaltura video quiz' option")
            return False            
            
        self.clsCommon.base.swith_to_iframe(self.CANVAS_EXTERNAL_TOOL_IFRAME)
        
        # In embed page, choose page to embed from and media
        if self.clsCommon.kafGeneric.embedMedia(entryName) == False:    
            writeToLog("INFO","FAILED to choose media in embed page")
            return False 
        
        self.switch_to_default_content()
        sleep(4)
        if self.click(self.CANVAS_CONFIGURE_EXTERNAL_TOOL_SELECT_BTN) == False:
            writeToLog("INFO","FAILED to click on configure external tool select button")
            return False
        
        sleep(4)
        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
        
        if self.click(self.CANVAS_SAVE_AND_PUBLISH_ASSIGNMENT_BTN) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False 
        
        tmpAssignmentPageTitle = (self.CANVAS_ASSIGNMENT_PAGE_TITLE[0], self.CANVAS_ASSIGNMENT_PAGE_TITLE[1].replace('ASSIGNMENT_NAME', assignmentTitle))
        if self.wait_element(tmpAssignmentPageTitle) == False:
            writeToLog("INFO","FAILED to displayed assignment title in assignment page")
            return False             

        writeToLog("INFO","Success: Embed assignment was created successfully")
        return True    
    
    
    # @Author: Inbar Willman
    def navigateToAssignmentPage(self, assignmentName):      
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_ASSIGNMENTSS_URL) == False:
            writeToLog("INFO","FAILED navigate to assignment page")
            return False   
        
        tmpAssignmentName = (self.CANVAS_ASSIGNMENT_NAME_IN_ASSIGNMENTS_PAGE[0], self.CANVAS_ASSIGNMENT_NAME_IN_ASSIGNMENTS_PAGE[1].replace('ASSIGNMENT_NAME', assignmentName))
        if self.click(tmpAssignmentName) == False:
            writeToLog("INFO","FAILED click on assignment " + assignmentName)
            return False   
        
        writeToLog("INFO","Success: Navigate to assignment page")
        return True               
        
    
    # @Author: Inbar Willman
    def verifyGradeAsAdminCanvas(self, grade, assignmentName):  
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_GRADEBOOK_URL) == False:
            writeToLog("INFO","FAILED navigate to gradebook page")
            return False
        
        # Get assignment name in grades cell
        tmpAssignmentName = (self.CANVAS_ASSIGNMENT_GRADE_TITLE_FOR_ADMIN[0], self.CANVAS_ASSIGNMENT_GRADE_TITLE_FOR_ADMIN[1].replace('ASSIGNMENT_NAME', assignmentName))      
        tmpAssignmentNameElement = self.wait_element(tmpAssignmentName) 
        if tmpAssignmentNameElement == False:
            writeToLog("INFO","FAILED to find assignment " + assignmentName + " name in grades page")
            return False  
        
        # Get assignment name id number
        tmpAssignmentNameIdAttribute = tmpAssignmentNameElement.get_attribute("id")  
        tmpAssignmentNameId = tmpAssignmentNameIdAttribute.split("_")[-1]   
        
        # Get grade parent according to the assignment name ID
        tmpGradeParent = (self.CANVAS_ASSIGNMENT_GRADE_FOR_ADMIN[0], self.CANVAS_ASSIGNMENT_GRADE_FOR_ADMIN[1].replace('ID_NAME', tmpAssignmentNameId)) 
        tmpGradeParentElement = self.wait_element(tmpGradeParent)
        
        if tmpGradeParentElement.text not in grade:
            writeToLog("INFO","FAILED to find assignment " + assignmentName + " grade")
            return False 
        
        writeToLog("INFO","Success: " + assignmentName + " grade is display")              
        return True  
    
    
    # @Author: Inbar Willman   
    def verifyGradeAsStudentCanvas(self, grade, assignmentName):   
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_GRADES_STUDENT_URL) == False:
            writeToLog("INFO","FAILED navigate to grades page")
            return False           
        
        tmpAssignmentGradeParent = (self.CANVAS_ASSIGNMENT_GRADE_FOR_STUDENT[0], self.CANVAS_ASSIGNMENT_GRADE_FOR_STUDENT[1].replace('ASSIGNMENT_NAME', assignmentName))  
        tmpAssignmentGradeParentElement = self.wait_element(tmpAssignmentGradeParent)
        
        if tmpAssignmentGradeParentElement == False:
            writeToLog("INFO","FAILED to find grade element")
            return False 
        
        # Get student grade
        gradeForStudent = tmpAssignmentGradeParentElement.text.split('\n')[-1]
                       
        if grade not in gradeForStudent:
            writeToLog("INFO","FAILED to display grade for " + assignmentName)
            return False  
        
        writeToLog("INFO","Success: " + assignmentName + " grade is display")              
        return True   
    
    
    # @Author: Inbar Willman
    def deleteAssignment(self, assignmentName):     
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_ASSIGNMENTSS_URL) == False:
            writeToLog("INFO","FAILED navigate to assignment page")
            return False  
        
        tmpAssignmentDropDown = (self.CANVAS_ASSIGNMENT_DROP_DOWN[0], self.CANVAS_ASSIGNMENT_DROP_DOWN[1].replace('ASSIGNMENT_NAME', assignmentName))  
        if self.click(tmpAssignmentDropDown) == False:
            writeToLog("INFO","FAILED to click on assignment drop down icon")
            return False 
        
        tmpDeleteAssignmentBtn = (self.CANVAS_DELETE_ASSIGNMENT_OPTION[0], self.CANVAS_DELETE_ASSIGNMENT_OPTION[1].replace('ASSIGNMENT_NAME', assignmentName))  
        if self.click(tmpDeleteAssignmentBtn) == False:
            writeToLog("INFO","FAILED to click on delete assignment option")
            return False  
        
        if self.clsCommon.base.click_dialog_accept() == False:
            writeToLog("INFO","FAILED click accept dialog")
            return False    
        
        # Verify that assignment isn't displayed in page anymore
        tmpAssignmentName = (self.CANVAS_ASSIGNMENT_NAME_IN_ASSIGNMENTS_PAGE[0], self.CANVAS_ASSIGNMENT_NAME_IN_ASSIGNMENTS_PAGE[1].replace('ASSIGNMENT_NAME', assignmentName)) 
        if self.wait_element(tmpAssignmentName, 3) != False:
            writeToLog("INFO","FAILED: " + assignmentName + " is still displayed in page")
            return False 
        
        # Navigate to grades page and verify that assignment isn't displayed in grades page 
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_GRADEBOOK_URL) == False:
            writeToLog("INFO","FAILED navigate to gradebook page")
            return False
        
        tmpAssignmentGradeParent = (self.CANVAS_ASSIGNMENT_GRADE_FOR_STUDENT[0], self.CANVAS_ASSIGNMENT_GRADE_FOR_STUDENT[1].replace('ASSIGNMENT_NAME', assignmentName))  
        if self.wait_element(tmpAssignmentGradeParent, 3) != False:
            writeToLog("INFO","FAILED : " + assignmentName + " is still displayed in grades page")
            return False  
        
        writeToLog("INFO","Success: " + assignmentName + " was deleted")              
        return True                  