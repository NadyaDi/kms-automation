import random
import subprocess
from base import *
import clsTestService
import enums
from general import General
from selenium.webdriver.common.keys import Keys
try:
    import win32com.client
except:
    pass
import collections


# This class is for multiple upload
class UploadEntry():
    filePath = ''
    name = ''
    description = ''
    tags = ''
    timeout = 0
    retries = 0
    
    # Constructor
    def __init__(self, filePath, name, description, tags, timeout=60, retries=3):
        self.filePath = filePath
        self.name = name
        self.description = description
        self.tags = tags
        self.timeout = timeout
        self.retries = retries
        
        
class Upload(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Upload locators:
    #=============================================================================================================
    UPLOAD_MENU_DROP_DOWN_ELEMENT               = ('id', 'uploadMenuDropDown')
    DROP_DOWN_MEDIA_UPLOAD_BUTTON               = ('xpath', ".//span[text()='Media Upload']")
    CHOOSE_A_FILE_TO_UPLOAD_BUTTON              = ('xpath', "//label[contains(.,'Choose a file to upload')]")
    UPLOAD_COMPLETED_LABEL                      = ('xpath', "//strong[contains(.,'Upload Completed!')]")
    UPLOAD_ENTRY_DETAILS_ENTRY_NAME             = ('id', "Entry-name")
    UPLOAD_ENTRY_DESCRIPTION_IFRAME             = ('class_name', "wysihtml5-sandbox")
    UPLOAD_ENTRY_DESCRIPTION_TEXT_BOX           = ('xpath', "//div[@class='content']")
    UPLOAD_ENTRY_DETAILS_ENTRY_DESCRIPTION      = ('tag_name', 'body') #before using need to switch frame and click on the description box
    UPLOAD_ENTRY_DETAILS_ENTRY_TAGS             = ('id', 's2id_Entry-tags')
    UPLOAD_ENTRY_DETAILS_ENTRY_TAGS_INPUT       = ('xpath', "//input[contains(@id,'s2id_autogen') and contains(@class, 'focused')]")
    UPLOAD_ENTRY_SAVE_BUTTON                    = ('xpath', "//button[@id='Entry-submit']")
    UPLOAD_ENTRY_PROGRESS_BAR                   = ('id', 'progressBar')
    UPLOAD_ENTRY_SUCCESS_MESSAGE                = ('xpath', "//span[contains(.,'Your changes have been saved.')]")
    UPLOAD_ENTRY_DISCLAIMER_CHECKBOX            = ('id', 'disclaimer-Accepted')
    UPLOAD_GO_TO_MEDIA_BUTTON                   = ('xpath', "//a[@class='btn btn-link' and text() = 'Go To Media']")
    UPLOAD_ENABLE_SCHEDULING_RADIO              = ('id', 'schedulingRadioButtons_5a65e5d39199d-scheduled')
    DROP_DOWN_VIDEO_QUIZ_BUTTON                 = ('xpath', ".//span[text()='Video Quiz']")
    DROP_DOWN_YOUTUBE_BUTTON                    = ('xpath', ".//span[text()='YouTube']")
    VIDEO_QUIZ_PAGE_TITLE                       = ('xpath', "//h1[@class='editorBreadcrumbs inline']")
    YOUTUBE_PAGE_TITLE                          = ('xpath', "//h1[@class='uploadBoxHeading']")
    YOUTUBE_PAGE_LINK_FIELD                     = ('id', 'externalContentId')
    # Elements for multiple upload
    UPLOAD_UPLOADBOX                            = ('xpath', "//div[@id='uploadbox[ID]']") #Replace [ID] with uploadbox ID
    UPLOAD_MULTIPLE_CHOOSE_A_FILE_BUTTON        = ('xpath', "//label[@for='fileinput[ID]']") #Replace [ID] with uploadbox ID
    UPLOAD_GO_TO_MEDIA_BUTTON                   = ('xpath', "//a[@id='back' and contains(text(), 'Go To Media')]")
    WEBCAST_PAGE_TITLE                          = ('xpath', "//h1[text()='Schedule a Webcast Event']")
    UPLOAD_MODERATION_UPLOAD_MESSAGE            = ('xpath', "//div[contains(text(), 'Some media may not be published until approved by the media moderator.')]")
    UPLOAD_PAGE_TITLE                           = ('xpath', "//h1[text()='Upload Media']")
    DROP_DOWN_WEBCAST_BUTTON                    = ('xpath', ".//span[text()='Webcast Event']")
    UPLOAD_DESCRIPTION_FIELD_TITLE              = ('xpath', '//label[@id="description-label"]')   
    DROP_DOWN_WEBCAM_RECORDING_BUTTON           = ('xpath', ".//span[text()='Webcam Recording']")
    RECORDER_PAGE_TITLE                         = ('xpath', "//h1[text()='Record Media']")
    RECORDER_START_BTN                          = ('xpath', '//button[@id="startRecord"]')
    RECORDER_STOP_BTN                           = ('xpath', '//button[contains(@class,"timer-button timer-button")]')
    RECORDER_USE_THIS_BTN                       = ('xpath', '//button[contains(@class,"btn btn-primary btn__save bottom__btn__") and text()="Use This"]')
    RECORDER_RECORD_AGAIN_BTN                   = ('xpath', '//button[contains(@class,"btn btn__reset bottom__btn__") and text()="Record Again"]')
    RECORDER_SCREEN                             = ('xpath', '//video[@id="recorder"]')
    RECORDER_PLAY_BTN                           = ('xpath', '//a[@class="playkit-pre-playback-play-button"]')
    RECORDER_COUNTDOWN                          = ('xpath', '//div[contains(@class, "countdown countdown")]')
    UPLOAD_CHOOSE_A_FILE_BUTTON                 = ('xpath', "//input[contains(@id,'fileinput')]") 
    #============================================================================================================
    
    def clickMediaUpload(self):
        try:
            parentElement = self.get_element(self.UPLOAD_MENU_DROP_DOWN_ELEMENT)
            self.get_child_element(parentElement, self.DROP_DOWN_MEDIA_UPLOAD_BUTTON).click()
            return True
        except NoSuchElementException:
            writeToLog("INFO","FAILED to click on Media Upload from drop down menu")
            return False
        
        
    #  @Author: Inbar Willman  
    def clickVideoQuiz(self):
        try:
            parentElement = self.get_element(self.UPLOAD_MENU_DROP_DOWN_ELEMENT)
            self.get_child_element(parentElement, self.DROP_DOWN_VIDEO_QUIZ_BUTTON).click()
            return True
        except NoSuchElementException:
            writeToLog("INFO","FAILED to click on Video Quiz from drop down menu")
            return False   
        
    #  @Author: Inbar Willman  
    def clickYoutube(self):
        try:
            parentElement = self.get_element(self.UPLOAD_MENU_DROP_DOWN_ELEMENT)
            self.get_child_element(parentElement, self.DROP_DOWN_YOUTUBE_BUTTON).click()
            return True
        except NoSuchElementException:
            writeToLog("INFO","FAILED to click on youtube from drop down menu")
            return False   
    
        
    #  @Author: Tzachi Guetta
    # In case disclaimer module is turned on and set to "before upload" 
    # The following function will check that upload is prevented before disclaimer's check-box was checked.
    def handleDisclaimerBeforeUplod(self):
        try:
            if self.wait_visible(self.clsCommon.upload.CHOOSE_A_FILE_TO_UPLOAD_BUTTON, 5) == False:
                if self.click(self.UPLOAD_ENTRY_DISCLAIMER_CHECKBOX) == False:
                    writeToLog("INFO","FAILED to click on disclaimer check-box")
                    return False
            else:
                writeToLog("INFO","FAILED, upload button is presented before User agree to terms of Use (disclaimer)")
                return False
        except NoSuchElementException:
            return False
        
        return True
    
    
    #  @Author: Tzachi Guetta    
    def extractEntryID (self, locator):
        try:
            div = self.get_element(locator)
            href = div.get_attribute('href')
            entryID = href.split("/")[len(href.split("/"))-1]
             
        except NoSuchElementException:
            writeToLog("INFO","FAILED to extract entry ID from entry, locator: '" + locator[1] + "'")
            return False
         
        return entryID
    
                
    # @Authors: Oleg Sigalov &  Tzachi Guetta
    # IMPORTENT!! This method return None (not False) if failed and an entry ID if passed
    def uploadEntry(self, filePath, name, description, tags, timeout=60, disclaimer=False, retries=3, uploadFrom=enums.Location.UPLOAD_PAGE, verifyModerationWarning=False, isTagsNeeded=True):
        for i in range(retries):
            try:
                if i > 0:
                    writeToLog("INFO","FAILED to upload after " + str(i) + " retries of " + str(retries) + ". Going to upload again...")
                # Convert path for Windows
                filePath = filePath.replace("/", "\\")
                filePath = filePath.replace("\\\\", "\\")
                 
                # Navigate to upload page
                if uploadFrom == enums.Location.UPLOAD_PAGE or uploadFrom == enums.Location.UPLOAD_PAGE_EMBED:
                    if self.navigateToUploadPage(uploadFrom) == False:
                        continue
 
                #checking if disclaimer is turned on for "Before upload"
                if disclaimer == True:
                    if self.clsCommon.upload.handleDisclaimerBeforeUplod() == False:
                        writeToLog("INFO","FAILED, Handle disclaimer before upload failed")
                        continue
                     
                # Wait page load
                self.wait_for_page_readyState()
                # If running on remote node
                if localSettings.LOCAL_SETTINGS_RUN_MDOE == localSettings.REMOTE_RUN_MODE:
                    # Because of miltiple run at same time, we apply random wait
                    timeDelay = random.uniform(1.1, 2.9)
                    sleep(timeDelay)      
                             
#                 # Set file path to upload - instead of clicking on UPLOAD_CHOOSE_A_FILE_BUTTON         
#                 if self.send_keys(self.UPLOAD_CHOOSE_A_FILE_BUTTON, filePath, multipleElements=True) == False:
#                     writeToLog("DEBUG","FAILED to set file path to upload")
#                     continue            
                
                # TODO (Oleg Sigalov): Remove next part if previous code works (03/02/19)                
                # Click Choose a file to upload
                if self.click(self.CHOOSE_A_FILE_TO_UPLOAD_BUTTON) == False:
                    writeToLog("DEBUG","FAILED to click on 'Choose a file to upload' button")
                    continue
                  
                sleep(3)
                # Type in a file path
                if self.typeIntoFileUploadDialog(filePath) == False:
                    continue
                 
                # Wait for success message "Upload Completed"
                startTime = datetime.datetime.now().replace(microsecond=0)
                if self.waitUploadCompleted(startTime, timeout) == False:
                    continue
                 
                if self.isErrorUploadMessage() == True:# TODO verify it doesn't take time when there is no error
                    writeToLog("INFO","FAILED to upload entry, error message appeared on the screen: 'Oops! Entry could not be created.'")
                    continue
                    
                # Fill entry details: name, description, tags
                if self.fillFileUploadEntryDetails(name, description, tags, isTagsNeeded=isTagsNeeded) == False:
                    continue
                 
                if self.getAppUnderTest() == enums.Application.BLACK_BOARD:
                    self.get_body_element().send_keys(Keys.TAB) 
                    self.get_body_element().send_keys(Keys.PAGE_DOWN)
                 
                if verifyModerationWarning == True:
                    self.click(self.UPLOAD_PAGE_TITLE)
                    self.get_body_element().send_keys(Keys.PAGE_DOWN)   
                    if self.wait_visible(self.UPLOAD_MODERATION_UPLOAD_MESSAGE) == False:
                        writeToLog("INFO","FAILED to find moderation upload message")
                        return False
                    
                # Click Save
                if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD or uploadFrom == enums.Location.UPLOAD_PAGE_EMBED:
                    if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
                        self.switch_to_default_content()
                        if self.swith_to_iframe(self.clsCommon.canvas.CANVAS_EMBED_UPLOAD_IFRAME)  == False:
                            writeToLog("DEBUG","FAILED to switch to canvas upload embed iFrame")
                            continue
                        
                    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
                        self.switch_to_default_content()
                        self.clsCommon.base.swith_to_iframe(self.clsCommon.d2l.D2L_INSERT_STUFF_IFRAME)
                        self.clsCommon.base.swith_to_iframe(self.clsCommon.d2l.D2L_EMBED_IFRAME)
                        
                    elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
                        self.switch_to_default_content()
                        self.swith_to_iframe(self.clsCommon.jive.JIVE_BSE_MAIN_IFRAME)
                        self.swith_to_iframe(self.clsCommon.jive.JIVE_BSE_INNER_IFRAME)
                                               
                    self.click(self.UPLOAD_PAGE_TITLE)
                    self.get_body_element().send_keys(Keys.PAGE_DOWN)  
                    sleep(3)
                    
                if self.click(self.UPLOAD_ENTRY_SAVE_BUTTON, multipleElements=True) == False:
                    writeToLog("DEBUG","FAILED to click on 'Save' button")
                    continue
                sleep(3)
                 
                # Wait for loader to disappear
                self.clsCommon.general.waitForLoaderToDisappear()
                sleep(3)
                 
                # Wait for 'Your changes have been saved.' message
                if self.wait_visible(self.UPLOAD_ENTRY_SUCCESS_MESSAGE, 45) != False: 
                    if uploadFrom != enums.Location.UPLOAD_PAGE_EMBED:              
                        entryID = self.extractEntryID(self.UPLOAD_GO_TO_MEDIA_BUTTON)
                        if entryID != None:
                            writeToLog("INFO","Successfully uploaded entry: '" + name + "'"", entry ID: '" + entryID + "'")
                            return entryID
                    else:   
                        writeToLog("INFO","Successfully uploaded entry: '" + name)
                        return True
                else:
                    writeToLog("INFO","FAILED to upload entry, no success message was appeared'")
                    continue
     
            except Exception:
                writeToLog("INFO","FAILED to upload entry, retry number " + str(i))
                pass
            
        if i >= retries - 1:
            return None
    
    
    def uploadMulitple(self, uploadEntrieList, disclaimer=False, uploadFrom=enums.Location.UPLOAD_PAGE):
        uploadboxCount = 1
        if uploadFrom == enums.Location.UPLOAD_PAGE:
            # Click Add New
            if self.click(General.ADD_NEW_DROP_DOWN_BUTTON, multipleElements=True) == False:
                writeToLog("DEBUG","FAILED to click on 'Add New' button")
                return False
            # Click Media Upload
            if self.clickMediaUpload() == False:
                writeToLog("DEBUG","FAILED to click on 'Media Upload' button")
                return False

        # Checking if disclaimer is turned on for "Before upload"
        if disclaimer == True:
            if self.clsCommon.upload.handleDisclaimerBeforeUplod() == False:
                writeToLog("INFO","FAILED, Handle disclaimer before upload failed")
                return False
            
        # Wait page load
        self.wait_for_page_readyState()        
        for entry in uploadEntrieList:
            if self.fillFileUploadEntryDetailsMultiple(entry.filePath, entry.name, entry.description, entry.tags, entry.timeout, uploadboxCount) == False:
                return False 
            
#           # Click Save
            if self.click(('xpath', self.UPLOAD_UPLOADBOX[1].replace('[ID]', str(uploadboxCount)) + self.UPLOAD_ENTRY_SAVE_BUTTON[1])) == False:
                writeToLog("DEBUG","FAILED to click on 'Save' button")
                return False
            
            # Click Save another time, it's a workaround
            if self.click(('xpath', self.UPLOAD_UPLOADBOX[1].replace('[ID]', str(uploadboxCount)) + self.UPLOAD_ENTRY_SAVE_BUTTON[1])) == False:
                writeToLog("DEBUG","FAILED to click on 'Save' button")
                return False            
            sleep(3)
            
            # Wait for loader to disappear
            self.clsCommon.general.waitForLoaderToDisappear()
            
            # Wait for 'Your changes have been saved.' message
            if self.wait_visible(('xpath', self.UPLOAD_UPLOADBOX[1].replace('[ID]', str(uploadboxCount)) + self.UPLOAD_ENTRY_SUCCESS_MESSAGE[1]), 45) != False:
            # TODO return entry ID
                entryID = self.extractEntryID(('xpath', self.UPLOAD_UPLOADBOX[1].replace('[ID]', str(uploadboxCount)) + self.UPLOAD_GO_TO_MEDIA_BUTTON[1]))
#                 if entryID != None:
#                     writeToLog("INFO","Successfully uploaded entry: '" + entry.name + "'"", entry ID: '" + entryID + "'")
#                     return entryID
                writeToLog("INFO","Successfully uploaded entry: '" + entry.name + "'"", entry ID: '" + entryID + "'")
                uploadboxCount += 1
                sleep(1)
                continue
            else:
                writeToLog("INFO","FAILED to upload entry, no success message was appeared'")
                return False
            
        return True
            


    # Fill basic entry details after upload is completed, only: name, description, tags     
    def fillFileUploadEntryDetailsMultiple(self, filePath, name="", description="", tags="", timeout=60, uploadboxId=""):
        # Get the uploadbox element
        uploadBoxElement = self.get_element(self.replaceInLocator(self.UPLOAD_UPLOADBOX, '[ID]', str(uploadboxId)))
        
        # Click Choose a file to upload
        if self.click_child(uploadBoxElement, self.replaceInLocator(self.UPLOAD_MULTIPLE_CHOOSE_A_FILE_BUTTON, '[ID]', str(uploadboxId))) == False:
            writeToLog("DEBUG","FAILED to click on 'Choose a file to upload' button")
            return False
        
        # Type in a file path
        if self.typeIntoFileUploadDialog(filePath) == False:
            return False
        
        # Wait for success message "Upload Completed"
        startTime = datetime.datetime.now().replace(microsecond=0)
        if self.waitUploadCompleted(startTime, timeout, uploadboxId) == False:
            return False
        
        if self.isErrorUploadMessage(uploadboxId) == True:# TODO verify it doesn't take time when there is no error
            writeToLog("INFO","FAILED to upload entry, error message appeared on the screen: 'Oops! Entry could not be created.'")
            return False        
        
        entryNameElement = self.wait_visible_child(uploadBoxElement, self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME, 30)
        if entryNameElement == False:
            writeToLog("INFO","FAILED to find an entry name field:'" + name + "'")
            return False   
             
        entryNameElement.clear()
        if self.send_keys_to_child(uploadBoxElement, self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME, name) == False:
            writeToLog("INFO","FAILED to fill an entry name:'" + name + "'")
            return False
                
        if self.fillFileUploadEntryDescription(description, uploadboxId) == False:
            writeToLog("INFO","FAILED to fill an entry Description:'" + description + "'")
            return False
        
#         if self.fillFileUploadEntryTagsMultiple(tags, uploadboxId) == False:
#             writeToLog("INFO","FAILED to fill an entry Tags:'" + tags + "'")
#             return False
        if self.fillFileUploadEntryTags(tags, uploadboxId) == False:
            writeToLog("INFO","FAILED to fill an entry Tags:'" + tags + "'")
            return False
    
        return True


    # The method supports BOTH single and multiple upload    
    def waitUploadCompleted(self, startTime, timeout=60, uploadboxId=-1):
        if uploadboxId != -1:
            # Get the uploadbox element
            uploadBoxElement = self.get_element(self.replaceInLocator(self.UPLOAD_UPLOADBOX, '[ID]', str(uploadboxId)))
            isUploadCompleted = self.wait_for_child_text(uploadBoxElement, self.UPLOAD_COMPLETED_LABEL, "Upload Completed!", timeout)
        else:    
            isUploadCompleted = self.wait_for_text(self.UPLOAD_COMPLETED_LABEL, "Upload Completed!", timeout)
                     
        if isUploadCompleted == False:
            writeToLog("INFO","Upload didn't finish after timeout: " + str(timeout) + " seconds")
            return False
        else:
            now = datetime.datetime.now().replace(microsecond=0)
            uploadDuration = now - startTime
            writeToLog("INFO","Upload finished after: " + str(uploadDuration))
            return True
        
        
    def typeIntoFileUploadDialog(self, filePath):
        try:
            if localSettings.LOCAL_SETTINGS_RUN_MDOE == localSettings.REMOTE_RUN_MODE:
                self.clsCommon.instertPathInFileUploadWindows(filePath)
            else:
                if (localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_IE):
                    # TODO IE not implemented yet
                    subprocess.call([localSettings.LOCAL_SETTINGS_AUTOIT_SCRIPTS + r'\openFile.exe' ,filePath])
                elif(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_FIREFOX):
                    subprocess.call([localSettings.LOCAL_SETTINGS_AUTOIT_SCRIPTS + r'\openFileFirefox.exe' ,filePath])
                elif(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
                    subprocess.call([localSettings.LOCAL_SETTINGS_AUTOIT_SCRIPTS + r'\openFileChrome.exe' ,filePath])
                else:
                    writeToLog("INFO","FAILED to type into 'Choose File' window, unknown browser: '" + localSettings.LOCAL_RUNNING_BROWSER + "'")
                    return False 
            return True       
        except Exception:
            writeToLog("INFO","FAILED to type into 'Choose File' window")
            return False        
        
        
    # Fill basic entry details after upload is completed, only: name, description, tags     
    def fillFileUploadEntryDetails(self, name="", description="", tags="", isTagsNeeded=True):
        if self.wait_visible(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME) == False:
            return False
        
        self.get_element(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME).clear()
        
        if self.send_keys(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME, name) == False:
            writeToLog("INFO","FAILED to fill a entry name:'" + name + "'")
            return False
        sleep(2)
        if self.fillFileUploadEntryDescription(description) == False:
            writeToLog("INFO","FAILED to fill a entry Description:'" + description + "'")
            return False
        sleep(2)
        if isTagsNeeded == True:
            if self.fillFileUploadEntryTags(tags) == False:
                writeToLog("INFO","FAILED to fill a entry Tags:'" + tags + "'")
                return False        
        
    
    # The method supports BOTH single and multiple upload    
    def fillFileUploadEntryDescription(self, text, uploadboxId=-1):
        if uploadboxId != -1:
            # Get the uploadbox element
            uploadBoxElement = self.get_element(self.replaceInLocator(self.UPLOAD_UPLOADBOX, '[ID]', str(uploadboxId)))
            
            # Switch to Description iFrame
            descpriptionIframe = self.get_child_element(uploadBoxElement, self.UPLOAD_ENTRY_DESCRIPTION_IFRAME)
        else:
            # Switch to Description iFrame
            descpriptionIframe = self.get_element(self.UPLOAD_ENTRY_DESCRIPTION_IFRAME)
        
        # Switch to iframe which is contains the description text box    
        self.driver.switch_to.frame(descpriptionIframe)
        
        # Click on Description text box
        el = self.get_element(self.UPLOAD_ENTRY_DESCRIPTION_TEXT_BOX)
        if el.click() == False:
            writeToLog("DEBUG","FAILED to click on Description filed")
            return False               
        sleep(2)
        
        # Enter text Description
        if self.clear_and_send_keys(self.UPLOAD_ENTRY_DETAILS_ENTRY_DESCRIPTION, text) == True:
            return True
        else:
            writeToLog("DEBUG","FAILED to type in Description")
            return False
        self.switch_to_default_content()
    
    
    # The method supports BOTH single and multiple upload
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillFileUploadEntryTags(self, tags, uploadboxId=-1):
        try:
            self.switch_to_default_content()
            if self.getAppUnderTest() == enums.Application.BLACK_BOARD:
                self.clsCommon.blackBoard.switchToBlackboardIframe()
            elif self.getAppUnderTest() == enums.Application.SHARE_POINT:
                self.clsCommon.sharePoint.switchToSharepointIframe()
                self.get_body_element().send_keys(Keys.PAGE_DOWN)
                sleep(1)
            elif self.getAppUnderTest() == enums.Application.MOODLE:
                self.clsCommon.moodle.switchToMoodleIframe()
            elif self.getAppUnderTest() == enums.Application.CANVAS:
                self.clsCommon.canvas.switchToCanvasIframe()
            elif self.getAppUnderTest() == enums.Application.D2L:
                self.clsCommon.d2l.switchToD2LIframe()
            elif self.getAppUnderTest() == enums.Application.JIVE:
                self.clsCommon.jive.switchToJiveIframe()
            elif self.getAppUnderTest() == enums.Application.SAKAI:
                self.clsCommon.sakai.switchToSakaiIframe()
            # If upload single (method: uploadEntry)
            if uploadboxId == -1:
                tagsElement = self.get_element(self.UPLOAD_ENTRY_DETAILS_ENTRY_TAGS)
            else:
                # Get the uploadbox element
                uploadBoxElement = self.get_element(self.replaceInLocator(self.UPLOAD_UPLOADBOX, '[ID]', str(uploadboxId)))            
                tagsElement = self.get_child_element(uploadBoxElement, self.UPLOAD_ENTRY_DETAILS_ENTRY_TAGS)
                
        except NoSuchElementException:
            writeToLog("DEBUG","FAILED to get Tags filed element")
            return False
                
        if self.clickElement(tagsElement) == False:
            writeToLog("DEBUG","FAILED to click on Tags filed")
            return False            
        sleep(1)

        if(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
            # Remove the Mask over all the screen (over tags filed also)
            maskOverElement = self.get_element(self.clsCommon.channel.CHANNEL_REMOVE_TAG_MASK)
            self.driver.execute_script("arguments[0].setAttribute('style','display: none;')",(maskOverElement))
         
            if self.clickElement(tagsElement) == False:
                writeToLog("DEBUG","FAILED to click on Tags filed")
                return False    
                            
        if uploadboxId == -1: # -1 stands for single
            if self.send_keys(self.UPLOAD_ENTRY_DETAILS_ENTRY_TAGS_INPUT, tags) == True:
                return True
        else:
            if self.send_keys_to_child(uploadBoxElement, self.UPLOAD_ENTRY_DETAILS_ENTRY_TAGS_INPUT, tags) == True:
                return True
            
        writeToLog("DEBUG","FAILED to type in Tags")
        return False                
        
    
    # The method supports BOTH single and multiple upload
    # Return true if error message ('Oops! Entry could not be created.') appeared after upload    
    def isErrorUploadMessage(self, uploadboxId=-1):
        if uploadboxId != -1:
            # Get the uploadbox element
            uploadBoxElement = self.get_element(self.replaceInLocator(self.UPLOAD_UPLOADBOX, '[ID]', str(uploadboxId)))
            progressBarText = self.get_element_child_text(uploadBoxElement, self.UPLOAD_ENTRY_PROGRESS_BAR)
        else:        
            progressBarText = self.get_element_text(self.UPLOAD_ENTRY_PROGRESS_BAR)
        if progressBarText == None:
            return False
        if progressBarText == 'Oops! Entry could not be created.':
            return True
        else:
            return False
        
    # Use after upload is done, from upload page    
    def clickGoToMyMedia(self):
        return self.click(self.UPLOAD_GO_TO_MEDIA_BUTTON)
    
    
    # @Author: Inbar Willman
    def addNewVideoQuiz(self):
        # Click Add New
        if self.click(General.ADD_NEW_DROP_DOWN_BUTTON) == False:
            writeToLog("DEBUG","FAILED to click on 'Add New' button")
            return False
            
        # Click video quiz
        if self.clickVideoQuiz() == False:
            writeToLog("DEBUG","FAILED to click on 'Video Quiz' button")
            return False

        if self.wait_visible(self.VIDEO_QUIZ_PAGE_TITLE, 30) == False:
            writeToLog("DEBUG","FAILED to navigate to add new video quiz page")
            return False
        
        return True
        
        
    # @Author: Tzachi Guetta
    # Note: all entries were shared the same description & tags
    def uploadEntries(self, entriesDict, entryDescription, entryTags):
        try:
            # Checking if entriesNames list type
            if (type(entriesDict) is dict) or (type(entriesDict) is collections.OrderedDict): 
                for entryName in entriesDict: 
                    if self.uploadEntry(entriesDict.get(entryName), entryName, entryDescription, entryTags) == None:
                        writeToLog("INFO","FAILED to upload entry: " + entryName)
                        return False
            else:
                writeToLog("INFO","FAILED, Entries list was not provided ")
                return False
            
        except Exception:
            return False
        
        return True   
    
    
    # @Author: Inbar Willman
    def clickAddYoutube(self):
        # Click Add New
        if self.click(General.ADD_NEW_DROP_DOWN_BUTTON) == False:
            writeToLog("DEBUG","FAILED to click on 'Add New' button")
            return False
            
        # Click youtube
        if self.clickYoutube() == False:
            writeToLog("DEBUG","FAILED to click on 'Yotube' button")
            return False

        if self.wait_visible(self.YOUTUBE_PAGE_TITLE, 30) == False:
            writeToLog("DEBUG","FAILED to navigate to add new youtube page")
            return False
        
        return True


    # @Author: Inbar Willman
    def addYoutubeEntry(self, youtubeLink, entryName):
        youtubeField = self.get_element(self.YOUTUBE_PAGE_LINK_FIELD)    
        
        #Insert youtube link in field
        if youtubeField.send_keys(youtubeLink) == False:
            writeToLog("DEBUG","FAILED to insert youtube link")
            return False       
        
        #Click enter in field in order to see entry's fields
        if youtubeField.send_keys(Keys.ENTER) == False:
            writeToLog("DEBUG","FAILED to click on youtube link field")
            return False 
        
        # Wait for loader to disappear
        self.clsCommon.general.waitForLoaderToDisappear()
        
        #Wait until tag element is displayed
        self.wait_visible(self.UPLOAD_ENTRY_DETAILS_ENTRY_TAGS, timeout=60)    
        
        #Insert new name for entry
        self.get_element(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME).clear()
        if self.send_keys(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME, entryName) == False:
            writeToLog("INFO","FAILED to fill a entry name:'" + entryName + "'")
            return False
        
        # Click Save
        if self.click(self.UPLOAD_ENTRY_SAVE_BUTTON) == False:
            writeToLog("DEBUG","FAILED to click on Save button")
            return False 
        
        sleep(3)
                 
        # Wait for loader to disappear
        self.clsCommon.general.waitForLoaderToDisappear()
                 
        # Wait for 'Your changes have been saved.' message
        if self.wait_visible(self.UPLOAD_ENTRY_SUCCESS_MESSAGE, 45) != False:                
            entryID = self.extractEntryID(self.UPLOAD_GO_TO_MEDIA_BUTTON)
            if entryID != None:
                writeToLog("INFO","Successfully uploaded youtube entry")
                return entryID
            else:
                writeToLog("INFO","FAILED to upload entry, no success message was appeared'")
                return False      
            
            
    def navigateToUploadPage(self, uploadFrom=enums.Location.UPLOAD_PAGE):
        # KAF
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
            if uploadFrom!=enums.Location.UPLOAD_PAGE_EMBED:
                if self.clsCommon.kafGeneric.navigateToUploadPageKAF() == False:
                    writeToLog("INFO","FAILED navigate to upload page in " + localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST.value)
                    return False
                  
        # Click Add New
        if self.click(General.ADD_NEW_DROP_DOWN_BUTTON, multipleElements=True) == False:
            writeToLog("DEBUG","FAILED to click on 'Add New' button")
            return False
        # Click Media Upload
        if self.clickMediaUpload() == False:
            writeToLog("DEBUG","FAILED to click on 'Media Upload' button")
            return False            
        return True     
    
    
    # @Author: Inbar Willman
    # Upload multiple entries with same filePath
    def uploadMultipleEntries(self, filePath, entriesList, description, tags, timeout=60, disclaimer=False, retries=3, uploadFrom=enums.Location.UPLOAD_PAGE):
        for entry in entriesList:
            if self.uploadEntry(filePath, entry, description, tags, timeout, disclaimer, retries, uploadFrom) == False:
                writeToLog("DEBUG","FAILED to upload entry as part of multiple upload")
                return False
            
        return True
           
           
    def navigateToEntryPageFromUploadPage(self, entryName):     
        if self.click(self.UPLOAD_GO_TO_MEDIA_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'go to media' button")
            return False  
        
        tmpEntry = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmpEntry, 15) == False:
            writeToLog("INFO","FAILED, entry page for entry '" + entryName + "' did NOT open")
            return False      
        
        sleep(2)
        writeToLog("INFO","Success, entry page was open successfully")
        return True
    
    
    # @Auther: Ori Flchtman
    # Upload a new webcast entry
    def addWebcastEntry(self, entryName, description, tags, disclaimer=False):
        if self.click(General.ADD_NEW_DROP_DOWN_BUTTON, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on 'Add New' button")
            return False

        if self.click(self.DROP_DOWN_WEBCAST_BUTTON, multipleElements=True) == False:
            writeToLog("INFO","FAILED to select the Webcast option from the drop down menu")
            return False
      
        if self.wait_visible(self.WEBCAST_PAGE_TITLE, 30) == False:
            writeToLog("INFO","FAILED to navigate to add new Webcast page")
            return False
        
        if self.fillFileUploadEntryDetails(entryName, description, tags) == False:
            writeToLog("INFO","FAILED to complete the field forms")
            return False
        
        if disclaimer == True:
            if self.clsCommon.upload.handleDisclaimerBeforeUplod() == False:
                writeToLog("INFO","FAILED, Handle disclaimer before upload failed")
                return False        
        
        if self.click(self.UPLOAD_ENTRY_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False
        
        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "FAILED to save webcast entry changes")
            return False

        if self.wait_visible(self.UPLOAD_ENTRY_SUCCESS_MESSAGE, 45) == False:
            writeToLog("INFO", "FAILED to save webcast entry changes")
            return False                
            
        return True
    

    #  @Author: Horia Cus
    # Extracts the entry id from the entry checkbox while being used in Pending tab   
    def extractEntryIDFromCheckBox (self, locator):
        try:
            div = self.get_element(locator)
            id = div.get_attribute('id')
            entryID = id.split("/")[len(id.split("/"))-1]
             
        except NoSuchElementException:
            writeToLog("INFO","FAILED to extract entry ID from entry, locator: '" + locator + "'")
            return False
         
        return entryID
    
    
    # @Author: Inbar Willman
    def clickAddWebcamRecording(self):
        # Click Add New
        if self.click(General.ADD_NEW_DROP_DOWN_BUTTON) == False:
            writeToLog("DEBUG","FAILED to click on 'Add New' button")
            return False
            
        # Click webcam recording option
        try:
            parentElement = self.get_element(self.UPLOAD_MENU_DROP_DOWN_ELEMENT)
            self.get_child_element(parentElement, self.DROP_DOWN_WEBCAM_RECORDING_BUTTON).click()
            
        except NoSuchElementException:
            writeToLog("INFO","FAILED to click webcam recording option from drop down menu")
            return False 

        if self.wait_visible(self.RECORDER_PAGE_TITLE, 30) == False:
            writeToLog("DEBUG","FAILED to navigate to recorder page")
            return False
        
        writeToLog("INFO","Success: webcam recording option was chosen")
        return True

    # NOT FINISHED
    # @Author: Inbar Willman
    # timeToStopRecording - When to stop recording (int)
    # recordAgain - If to record again (delete the current recording) 
    # numOfRecordinAgain - How many times to click record again before saving the recording
    def addNewWebcamRecording(self, entryName=None, description=None, tags=None, timeToStopRecording=None, recordAgain=False, numOfRecordinAgain=None, publishStatus=enums.EntryPrivacyType.PRIVATE, channelsList=[], categoriesList=[]):
        if self.clickAddWebcamRecording() == False:
            writeToLog("INFO","FAILED to click on webcam recording option in 'Add new'")
            return False  
        
        if self.wait_element(self.RECORDER_START_BTN) == False:
            writeToLog("INFO","FAILED to display recorder start button")
            return False 
        
        sleep(5)   
                          
        if self.clickPlayAndPauseInRecorder(timeToStopRecording) == False:
            writeToLog("INFO","FAILED to play and stop recording")
            return False 
        
        if recordAgain == True:
            for i in range(numOfRecordinAgain):
                if self.clickPlayAndPauseInRecorder(timeToStopRecording, True) == False:
                    writeToLog("INFO","FAILED to play and stop recording after clicking 'record again'")
                    return False 
                
                i=i+1
        
        if self.click(self.RECORDER_USE_THIS_BTN) == False:
            writeToLog("INFO","FAILED to click on 'Use This' button")
            return False             
        
        if self.wait_visible(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME) == False:
            writeToLog("INFO","FAILED to displayed entry details section")
            return False                         
        
        if self.fillFileUploadEntryDetails(entryName, description, tags) == False:
            writeToLog("INFO","FAILED to fill entry details")
            return False               
         
        # Click Save           
        if self.click(self.UPLOAD_ENTRY_SAVE_BUTTON, multipleElements=True) == False:
            writeToLog("DEBUG","FAILED to click on 'Save' button")
            return False 
                 
        # Wait for loader to disappear
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(3)
        
        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
                 
        # Wait for 'Your changes have been saved.' message
        if self.wait_visible(self.UPLOAD_ENTRY_SUCCESS_MESSAGE, 45) == False: 
            writeToLog("INFO","FAILED to upload entry, no success message was appeared'")
            return False
        
        if publishStatus == enums.EntryPrivacyType.UNLISTED:
            return True
        
        return True      
    
    
    # @Author: Inbar Willman
    def clickPlayAndPauseInRecorder(self, timeToStopRecording, isRecordAgain=False):  
        if isRecordAgain == False:  
            if self.click(self.RECORDER_START_BTN) == False:
                writeToLog("INFO","FAILED to click on start button")
                return False 
        else:
            if self.click(self.RECORDER_RECORD_AGAIN_BTN) == False:
                writeToLog("INFO","FAILED to click on 'Record Again' button")
                return False 
        
        if self.wait_while_not_visible(self.RECORDER_COUNTDOWN) == False:
            writeToLog("INFO","FAILED: countdown is still displayed")
            return False             
        
        if self.wait_for_text(self.RECORDER_STOP_BTN, timeToStopRecording, 100) == False:
            writeToLog("INFO","FAILED to display correct time")
            return False   
        
        if self.click(self.RECORDER_STOP_BTN) == False:
            writeToLog("INFO","FAILED to click on stop button")
            return False                       
        
        return True