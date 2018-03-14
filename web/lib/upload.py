import subprocess
try:
    import win32com.client
except:
    pass
import enums
from base import *
import clsTestService
from general import General


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
    UPLOAD_MENU_DROP_DOWN_ELEMENT               = ('id', "uploadMenuDropDown")
    UPLOAD_ENTRY_DETAILS_ENTRY_NAME             = ('id', "Entry-name")
    UPLOAD_ENTRY_DESCRIPTION_IFRAME             = ('class_name', "wysihtml5-sandbox")
    UPLOAD_ENTRY_DETAILS_ENTRY_DESCRIPTION      = ('tag_name', 'body') #before using need to switch frame and click on the description box
    UPLOAD_ENTRY_DETAILS_ENTRY_TAGS             = ('id', 's2id_Entry-tags')
    UPLOAD_ENTRY_DETAILS_ENTRY_TAGS2            = ('id', 'tags-list')
    UPLOAD_ENTRY_SAVE_BUTTON                    = ('id', 'Entry-submit')
    UPLOAD_ENTRY_PROGRESS_BAR                   = ('id', 'progressBar')
    UPLOAD_ENTRY_SUCCESS_MESSAGE                = ('xpath', "//span[contains(.,'Your changes have been saved.')]")
    UPLOAD_ENTRY_DISCLAIMER_CHECKBOX            = ('id', 'disclaimer-Accepted')
    UPLOAD_GO_TO_MEDIA_BUTTON                   = ('xpath', "//a[@class='btn btn-link' and text() = 'Go To Media']")
    UPLOAD_ENABLE_SCHEDULING_RADIO              = ('id', 'schedulingRadioButtons_5a65e5d39199d-scheduled')
    DROP_DOWN_VIDEO_QUIZ_BUTTON                 = ('xpath', ".//span[text()='Video Quiz']")
    VIDEO_QUIZ_PAGE_TITLE                       = ('xpath', "//h1[@class='editorBreadcrumbs inline']")
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
            return False
        
        return entryID
    
    
    # @Authors: Oleg Sigalov &  Tzachi Guetta
    def uploadEntry(self, filePath, name, description, tags, timeout=60, disclaimer=False, retries=3, uploadFrom=enums.Location.UPLOAD_PAGE):
        for i in range(retries):
            try:
                if i > 0:
                    writeToLog("INFO","FAILED to upload after " + str(i) + " retries of " + str(retries) + ". Going to upload again...")
                # Convert path for Windows
                filePath = filePath.replace("/", "\\")     
                
                if uploadFrom == enums.Location.UPLOAD_PAGE:
                    # Click Add New
                    if self.click(General.ADD_NEW_DROP_DOWN_BUTTON) == False:
                        writeToLog("DEBUG","FAILED to click on 'Add New' button")
                        continue
                    # Click Media Upload
                    if self.clickMediaUpload() == False:
                        writeToLog("DEBUG","FAILED to click on 'Media Upload' button")
                        continue

                #checking if disclaimer is turned on for "Before upload"
                if disclaimer == True:
                    if self.clsCommon.upload.handleDisclaimerBeforeUplod() == False:
                        writeToLog("INFO","FAILED, Handle disclaimer before upload failed")
                        continue
                    
                # Wait page load
                self.wait_for_page_readyState()
                # Click Choose a file to upload
                if self.click(self.CHOOSE_A_FILE_TO_UPLOAD_BUTTON) == False:
                    writeToLog("DEBUG","FAILED to click on 'Choose a file to upload' button")
                    continue
                
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
                if self.fillFileUploadEntryDetails(name, description, tags) == False:
                    continue
                
                # Click Save
                if self.click(self.UPLOAD_ENTRY_SAVE_BUTTON) == False:
                    writeToLog("DEBUG","FAILED to click on 'Save' button")
                    continue
                sleep(3)
                
                # Wait for loader to disappear
                self.clsCommon.general.waitForLoaderToDisappear()
                
                # Wait for 'Your changes have been saved.' message
                if self.wait_visible(self.UPLOAD_ENTRY_SUCCESS_MESSAGE, 45) != False:                
                    entryID = self.extractEntryID(self.UPLOAD_GO_TO_MEDIA_BUTTON)
                    if entryID != None:
                        writeToLog("INFO","Successfully uploaded entry: '" + name + "'"", entry ID: '" + entryID + "'")
                        return entryID
                else:
                    writeToLog("INFO","FAILED to upload entry, no success message was appeared'")
                    continue
    
            except Exception:
                writeToLog("INFO","FAILED to upload entry, retry number " + int(i))
                pass
        
        
    def waitUploadCompleted(self, startTime, timeout=60):
        if self.wait_for_text(self.UPLOAD_COMPLETED_LABEL, "Upload Completed!", timeout) == False:
            writeToLog("INFO","Upload didn't finish after timeout: " + str(timeout) + " seconds")
            return False
        else:
            now = datetime.datetime.now().replace(microsecond=0)
            uploadDuration = now - startTime
            writeToLog("INFO","Upload finished after: " + str(uploadDuration))
            return True
        
        
    def typeIntoFileUploadDialog_old(self, filePath):
        try:
            shell = win32com.client.Dispatch("WScript.Shell")  
            shell.Sendkeys(filePath)
            sleep(1)
            shell.Sendkeys("~")
            return True       
        except Exception:
            writeToLog("INFO","FAILED to type into 'Choose File' window")
            return False
        
    def typeIntoFileUploadDialog(self, filePath):
        try:
            # If running on remote node
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
    def fillFileUploadEntryDetails(self, name="", description="", tags=""): 
        if self.wait_visible(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME) == False:
            return False
        self.get_element(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME).clear()
        if self.send_keys(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME, name) == False:
            writeToLog("INFO","FAILED to fill a entry name:'" + name + "'")
            return False
        
        if self.fillFileUploadEntryDescription(description) == False:
            writeToLog("INFO","FAILED to fill a entry Description:'" + description + "'")
            return False
        
        if self.fillFileUploadEntryTags(tags) == False:
            writeToLog("INFO","FAILED to fill a entry Tags:'" + tags + "'")
            return False
        
        
    def fillFileUploadEntryDescription(self, text):
        # Switch to Description iFrame
        descpriptionIframe = self.get_element(self.UPLOAD_ENTRY_DESCRIPTION_IFRAME)
        self.driver.switch_to.frame(descpriptionIframe)
        
        # Click on Description text box
        el = self.driver.find_element_by_xpath("//div[@class='content']")
        #el = self.driver.find_element_by_xpath("//div[@class='content' and contains(text(), 'Enter Description')]")
        #el = self.driver.find_element_by_xpath("//body[contains(@class,'description span11 wysiwyg-Active wysihtml5-editor')]")
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
    
    
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillFileUploadEntryTags(self, tags):
        try:
            self.switch_to_default_content()
            tagsElement = self.get_element(self.UPLOAD_ENTRY_DETAILS_ENTRY_TAGS)
            
        except NoSuchElementException:
            writeToLog("DEBUG","FAILED to get Tags filed element")
            return False
                
        if tagsElement.click() == False:
            writeToLog("DEBUG","FAILED to click on Tags filed")
            return False            
        sleep(1)

        if self.send_keys(self.UPLOAD_ENTRY_DETAILS_ENTRY_TAGS, tags) == True:
            return True
        else:
            writeToLog("DEBUG","FAILED to type in Tags")
            return False

    # Return true if error message ('Oops! Entry could not be created.') appeared after upload    
    def isErrorUploadMessage(self):
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
            if type(entriesDict) is dict: 
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