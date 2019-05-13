from base import *
from general import General
import localSettings
from logger import *
from _ast import Is
from selenium.webdriver.common.keys import Keys
import enums


class BlackBoardUltra(Base):
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
    USER_LOGOUT_BTN                                     = ('xpath', "//span[@class='link-text' and contains(text(), 'Sign Out')]")
    COURSES_TAB_MENU                                    = ('xpath', "//span[@class='link-text' and contains(text(), 'Courses')]")
    COURSES_LIST_PAGE                                   = ('xpath', "//h4[@class='ellipsis' and @title='New1']")
    BB_ULTRA_MEDIA_SPACE_IFRAME                         = ('xpath', "//iframe[@id='lti-launch-iframe']")
    BB_ULTRA_USER_NAME                                  = ('xpath', "//bdi[contains(text(), 'USER_NAME')]")
    BB_ULTRA_PRIVECY_TURMS_BUTTON                       = ('xpath', "//button[@id='agree_button']")    
    BB_ULTRA_MY_MEDIA_BUTTON_IN_TOOLS_MENU              = ('xpath', "//span[@class='tool-title' and @title='Automation my media']")
    BB_ULTRA_MEDIA_GALLERY_BUTTON_IN_COURSE             = ('xpath', "//span[text()='New1']/ancestor::a[@class='content-title']")
    BB_ULTRA_ADD_CONTENT_BUTTON                         = ('xpath', "//div[@class='add-element no-select js-add-content-button course-outline-add-button']")
    BB_ULTRA_CONTENT_MARKET_BUTTON                      = ('xpath', "//button[@name='Content Market' and @role='menuitem']")
    BB_ULTRA_BSE_IVQ_BUTTON                             = ('xpath', "//p[@class='tool-title' and @title='Automation IVQ']")
    BB_ULTRA_MORE_OPTION_FOR_EMBED_BUTTON               = ('xpath', "//button[@aria-label='More options for EMBED_NAME' and @class='overflow-menu-button']")
    BB_ULTRA_EDIT_BUTTON_FOR_EMBED                      = ('xpath', "//span[contains(text(),'Edit')]")
    BB_ULTRA_DELETE_BUTTON_FOR_EMBED                    = ('xpath', "//span[contains(text(),'Delete')]")
    BB_ULTRA_DELETE_CONFIRMATION_BUTTON_FOR_EMBED       = ('xpath', "//button[@class='button js-delete-confirm']")
    BB_ULTRA_CONTENT_MARKET_POINTS_POSSIBL              = ('xpath', "//input[@name='grade-possible' and @type='text']")
    BB_ULTRA_CONTENT_MARKET_SAVE_BUTTON                 = ('xpath', "//button[@type='submit' and contains(text(), 'Save')]")
    BB_ULTRA_CONTENT_MARKET_EMBED_LINK                  = ('xpath', "//span[text()='EMBED_NAME']/ancestor::a[@class='content-title']")
    BB_ULTRA_CONTENT_MARKET_LAUNCH_BUTTON               = ('xpath', "//button[@class='button launch-link link' and contains(text(), 'Launch')]")
    BB_ULTRA_EMBED_NAME_ON_GRADES_PAGE_FOR_STUDENT      = ('xpath', '//a[contains(@ng-click,"courseGradesStudent.openItem(grade)") and text()="EMBED_NAME"]/ancestor::div[@class="row tabular-row js-row last-tabular-row-container child-is-invokable"]/descendant::bb-display-grade-pill[@grade="grade"]')
    BB_ULTRA_EMBED_NAME_ON_GRADES_PAGE_FOR_ADMIN        = ('xpath', "//div[@class='score' and contains(@aria-label,'grade is GRADE for EMBED_NAME. Press enter to edit. Posted')]")
    BB_ULTRA_GRADE_NAUMBER                              = ('xpath', "//a[contains(text(),'GRADE')]")
    
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
    def switchToBlackboardUltraIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            self.switch_to_default_content()
            if self.swith_to_iframe(self.BB_ULTRA_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_ULTRA
            return True
                     
        if self.wait_visible(self.BB_ULTRA_MEDIA_SPACE_IFRAME, 3) == False:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_ULTRA
            return True
        else:
            if self.swith_to_iframe(self.BB_ULTRA_MEDIA_SPACE_IFRAME) == False:
                writeToLog("INFO","FAILED to switch to iframe")
                return False
        
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KAF_BLACKBOARD_ULTRA
        return True
    
                
    def loginToBlackBoardUltra(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Navigate to login page
#             if self.click(self.BB_ULTRA_PRIVECY_TURMS_BUTTON) == False:
#                 writeToLog("INFO","FAILED to click on agree terms button")
#                 return False
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            
            sleep(6)
            self.click(self.LOGIN_SIGN_IN_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            sleep(4)
            tmp_user = (self.BB_ULTRA_USER_NAME[0], self.BB_ULTRA_USER_NAME[1].replace('USER_NAME', username))
            if self.wait_element(tmp_user, 30) == False:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
            else:
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                # Get the username after login and set the variable. Will need this it some tests
                #localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN = username
                return True

        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
             
          
    def logOutOfBlackBoardUltra(self, forceNavigate=True):
        if forceNavigate == True:
            if self.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
                writeToLog("INFO","FAILED to get to main page")
                return False  
        
        # Click on the user menu button
        self.clsCommon.base.switch_to_default_content() 
        sleep(3)
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
    def navigateToMyMediaBlackboardUltra(self):
        self.clsCommon.base.switch_to_default_content()
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL) == False:
            writeToLog("INFO","FAILED navigate to my media page")
            return False
        
        self.switchToBlackboardUltraIframe()
        if self.click(self.BB_ULTRA_MY_MEDIA_BUTTON_IN_TOOLS_MENU) == False:
            writeToLog("INFO","FAILED to click on my media button")
            return False
        
        sleep(6)
        self.switchToBlackboardUltraIframe()
        if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_TITLE, timeout=30) == False:
            writeToLog("INFO","FAILED navigate to My Media")
            return False
        
        return True  
     
     
    # Author: Oded Berihon
    def navigateToGalleryBlackBoardUltra(self, galleryName, forceNavigate=False):
        if forceNavigate == False:
            if self.wait_element(self.clsCommon.kafGeneric.KAF_MEDIA_GALLERY_TITLE, 5) != False:
#             self.switchToBlackboardUltraIframe()
#             if self.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","Success Already in my Gallery page")
                return True
        sleep(2)   
        
        if galleryName == "New1":
            if self.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                writeToLog("INFO","Success Already in my Gallery page")
                return False  
            sleep(5)   
                     
            if self.click(self.COURSES_TAB_MENU)== False:
                writeToLog("INFO","Success Already in my Gallery page")
                return False
            sleep(5) 
             
            if self.click(self.COURSES_LIST_PAGE)== False:
                writeToLog("INFO","Success Already in my Gallery page")
                return False
        sleep(5)
         
        self.switchToBlackboardUltraIframe()
        if self.click(self.BB_ULTRA_MEDIA_GALLERY_BUTTON_IN_COURSE) == False:
            writeToLog("INFO","FAILED to click on media gallery button")
            return False
         
        return True
    
    
    # Author: Oded Berihon    
    def createContentMarketBlackboardUltra(self, entryName, kalturaVideoQuizName, ponitesPossible):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_COURSE_CONTENT_PAGE) == False:
            writeToLog("INFO","FAILED navigate to main page")
            return False 
        
        self.switchToBlackboardUltraIframe()
        if self.click(self.COURSES_LIST_PAGE) == False:
            writeToLog("INFO","FAILED to click on course list page")
            return False 
              
        sleep(5)
        if self.click(self.BB_ULTRA_ADD_CONTENT_BUTTON) == False:
            writeToLog("INFO","fail to click on + button")
            return False 
        
        if self.click(self.BB_ULTRA_CONTENT_MARKET_BUTTON) == False:
            writeToLog("INFO","fail to click on content market from menu")
            return False         
        
        if self.click(self.BB_ULTRA_BSE_IVQ_BUTTON) == False:
            writeToLog("INFO","fail to click on automation ivq button")
            return False 
        
        if self.clsCommon.kafGeneric.embedMedia(entryName) == False:    
            writeToLog("INFO","FAILED to choose media in embed page")
            return False
  
        self.switch_to_default_content()
        temp_button = (self.BB_ULTRA_MORE_OPTION_FOR_EMBED_BUTTON[0], self.BB_ULTRA_MORE_OPTION_FOR_EMBED_BUTTON[1].replace('EMBED_NAME', kalturaVideoQuizName))
        if self.click(temp_button) == False:
            writeToLog("INFO","fail to click on menu button")
            return False
        
        if self.click(self.BB_ULTRA_EDIT_BUTTON_FOR_EMBED) == False:
            writeToLog("INFO","fail to click on edit button")
            return False                               
       
        if self.clear_and_send_keys(self.BB_ULTRA_CONTENT_MARKET_POINTS_POSSIBL, ponitesPossible) == False:
            writeToLog("INFO","FAILED to insert possible points")
            return False
        
        if self.click(self.BB_ULTRA_CONTENT_MARKET_SAVE_BUTTON) == False:
            writeToLog("INFO","fail to click on save button")
            return False           
        
        return True    
    
    # Author: Oded Berihon   
    def navigateToContentMarketBlackboardUltra(self, kalturaVideoQuizName):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_COURSE_CONTENT_PAGE) == False:
            writeToLog("INFO","FAILED navigate to main page")
            return False 
        
        self.switchToBlackboardUltraIframe()
        if self.click(self.COURSES_LIST_PAGE) == False:
            writeToLog("INFO","FAILED to click on course list page")
            return False 
        
        self.switch_to_default_content()   
        content_market_name = (self.BB_ULTRA_CONTENT_MARKET_EMBED_LINK[0], self.BB_ULTRA_CONTENT_MARKET_EMBED_LINK[1].replace('EMBED_NAME', kalturaVideoQuizName))
        if self.click(content_market_name) == False:
            writeToLog("INFO","fail to click on menu button")
            return False        
            
        if self.click(self.BB_ULTRA_CONTENT_MARKET_LAUNCH_BUTTON) == False:
            writeToLog("INFO","fail to click on launch button")
            return False        
                        
        return True         

    # Author: Oded Berihon   
    def deleteEmbedBlackboardUltra(self, kalturaVideoQuizName):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_COURSE_CONTENT_PAGE) == False:
            writeToLog("INFO","FAILED navigate to main page")
            return False 
        
        self.switchToBlackboardUltraIframe()
        if self.click(self.COURSES_LIST_PAGE) == False:
            writeToLog("INFO","FAILED to click on course list page")
            return False 

        sleep(10)       
        self.switch_to_default_content()
        temp_button = (self.BB_ULTRA_MORE_OPTION_FOR_EMBED_BUTTON[0], self.BB_ULTRA_MORE_OPTION_FOR_EMBED_BUTTON[1].replace('EMBED_NAME', kalturaVideoQuizName))
        if self.click(temp_button) == False:
            writeToLog("INFO","fail to click on menu button")
            return False
        
        if self.click(self.BB_ULTRA_DELETE_BUTTON_FOR_EMBED) == False:
            writeToLog("INFO","fail to click on delete button")
            return False           

        if self.click(self.BB_ULTRA_DELETE_CONFIRMATION_BUTTON_FOR_EMBED) == False:
            writeToLog("INFO","fail to click on delete confirmation button")
            return False                  
                        
        return True  
    
    # Author: Oded Berihon   
    def verifyGradeAsStudentBlackboardUltra(self, grade, kalturaVideoQuizName):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_COURSE_GRADES_STUDENT_URL) == False:
            writeToLog("INFO","FAILED navigate to main page")
            return False 
        
        tmpGradeParent = (self.BB_ULTRA_EMBED_NAME_ON_GRADES_PAGE_FOR_STUDENT[0], self.BB_ULTRA_EMBED_NAME_ON_GRADES_PAGE_FOR_STUDENT[1].replace('EMBED_NAME', kalturaVideoQuizName))
        tmpAssignmentGradeParentElement = self.wait_element(tmpGradeParent)        
        
        sleep(4)
        if tmpAssignmentGradeParentElement == False:
            writeToLog("INFO","FAILED to find grade element")
            return False 
        
        # Get student grade
        gradeForStudent = tmpAssignmentGradeParentElement.text.split('\n')[-1]
                       
        if grade not in gradeForStudent:
            writeToLog("INFO","FAILED to display grade for " + kalturaVideoQuizName)
            return False 
        writeToLog("INFO","Success: Correct grade is displayed")               
        
        return True        

    # Author: Oded Berihon  
    def verifyGradeAsAdminBlackboardUltra(self, grade, kalturaVideoQuizName):
        if self.clsCommon.base.navigate(localSettings.LOCAL_SETTINGS_COURSE_GRADES_ADMIN_URL) == False:
            writeToLog("INFO","FAILED navigate to main page")
            return False 
        
        tmpQuizGrade = (self.BB_ULTRA_EMBED_NAME_ON_GRADES_PAGE_FOR_ADMIN[0], self.BB_ULTRA_EMBED_NAME_ON_GRADES_PAGE_FOR_ADMIN[1].replace('EMBED_NAME', kalturaVideoQuizName).replace('GRADE', grade))
        quiGradeElement = self.wait_element(tmpQuizGrade)
        if quiGradeElement == False:
            writeToLog("INFO","FAILED to find quiz in full grade center")          
            return False 

        gradeForStudent = quiGradeElement.text.split(" ")[0]
        
        if gradeForStudent != grade:
            writeToLog("INFO","FAILED to display correct quiz grade")          
            return False     
        
        writeToLog("INFO","Success: quiz grade is displayed correctly in full grade center")             
        
        return True     
    
    def getBlackboardUltraLoginUserName(self):
        try:
            userName = self.get_element_text(self.BB_ULTRA_USER_NAME)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get user name element")
            return False
        return userName   
 