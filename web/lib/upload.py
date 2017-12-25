from base import *
from general import *
import win32com.client  
from symbol import except_clause


class Upload(Base):
    #=============================================================================================================
    #Upload XPATH locators:
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
    UPLOAD_ENTRY_DETAILS_ENTRY_TAGS2             = ('id', 'tags-list')
    UPLOAD_ENTRY_SAVE_BUTTON                    = ('id', 'Entry-submit')
    #============================================================================================================
#     general = General(Base.driver) #TODO
    
    def clickMediaUpload(self):
        try:
            parentElement = self.get_element(self.UPLOAD_MENU_DROP_DOWN_ELEMENT)
            self.get_child_element(parentElement, self.DROP_DOWN_MEDIA_UPLOAD_BUTTON).click()
            return True
        except NoSuchElementException:
            return False        

    
    def upload(self, filePath, name, descrition, tags, timeout=60):
#         filePath = "C:\\TestComplete\\automation-tests\\KalturaCore\\TestData\\Videos\\QR_05_minutes.mp4"
        filePath = "C:\\TestComplete\\automation-tests\\KalturaCore\\TestData\\Videos\\Images\\automation.jpg"
        try:
            # Click Add New
            if self.click(General.ADD_NEW_DROP_DOWN_BUTTON) == False:
                writeToLog("DEBUG","FAILED to click on 'Add New' button")
                return False
             
            # Click Media Upload
            if self.clickMediaUpload() == False:
                writeToLog("DEBUG","FAILED to click on 'Media Upload' button")
                return False 
                        
            # Wait page load
            self.wait_for_page_readyState()
            # Click Choose a file to upload
            if self.click(self.CHOOSE_A_FILE_TO_UPLOAD_BUTTON) == False:
                writeToLog("DEBUG","FAILED to click on 'Choose a file to upload' button")
                return False
            
            # Type in a file path
            self.typeIntoFileUploadDialog(filePath)
            
            # Wait for success message "Upload Completed"
            startTime = datetime.datetime.now().replace(microsecond=0)
            self.waitUploadCompleted(startTime, timeout)
            
            # Fill entry details: name, descrition, tags
            self.fillFileUploadEntryDetails(name, descrition, tags)
            
            # Click Save
            if self.click(self.UPLOAD_ENTRY_SAVE_BUTTON) == False:
                writeToLog("DEBUG","FAILED to click on 'Save' button")
                return False
            sleep(4)
            
            # Wait for loader to disappear
#             self.general.waitForLoaderToDisappear(timeout) #TODO
            self.wait_while_not_visible(General.KMS_LOADER, 60)
            sleep(2)
            # Wait for 'Your changes have been saved.' message
                   
#             writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
        except Exception as inst:
#             writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_UPLOAD")
            raise Exception(inst)
        
        
    def waitUploadCompleted(self, startTime, timeout=60):
        if self.wait_for_text(self.UPLOAD_COMPLETED_LABEL, "Upload Completed!", timeout) != True:
            writeToLog("INFO","Upload didn't finish after timeout:" + timeout + "' seconds")
            return False
        else:
            now = datetime.datetime.now().replace(microsecond=0)
            uploadDuration = now - startTime
            writeToLog("INFO","Upload finished after:" + str(uploadDuration) + "'")
            return True
        
        
    def typeIntoFileUploadDialog(self, filePath):
        try:
            shell = win32com.client.Dispatch("WScript.Shell")  
            shell.Sendkeys(filePath)
            sleep(1)
            shell.Sendkeys("~")
            return True       
        except Exception:
            writeToLog("INFO","FAILED to type into 'Choose File' window")
            return False
        
        
    # Fill basic entry details after upload is completed, only: name, descrition, tags     
    def fillFileUploadEntryDetails(self, name="", descrition="", tags=""): 
        self.get_element(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME).clear()
        if self.send_keys(self.UPLOAD_ENTRY_DETAILS_ENTRY_NAME, name) == False:
            writeToLog("INFO","FAILED to fill a entry name:'" + name + "'")
            return False
        
        if self.fillFileUploadEntryDescription(descrition) == False:
            writeToLog("INFO","FAILED to fill a entry Description:'" + descrition + "'")
            return False
        
        if self.fillFileUploadEntryTags(tags) == False:
            writeToLog("INFO","FAILED to fill a entry Tags:'" + tags + "'")
            return False
        
        
    def fillFileUploadEntryDescription(self, text):
        # Switch to Description iFrame
        descpriptionIframe = self.get_element(self.UPLOAD_ENTRY_DESCRIPTION_IFRAME)
        self.driver.switch_to.frame(descpriptionIframe)
        
        # Click on Description text box
        el = self.driver.find_element_by_xpath("//div[@class='content' and contains(text(), 'Enter Description')]")
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