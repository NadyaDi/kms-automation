from base import *
import clsTestService
import clsCommon
import enums


class EditEntryPage(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Entry Page locators:
    #=============================================================================================================
    EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE                            = ('xpath', "//span[@id='entryName' and contains(text(), 'ENTRY_NAME')]") # When using this locator, replace 'ENTRY_NAME' string with your real entry name
    EDIT_ENTRY_COLLABORATION_TAB                                = ('id', "collaboration-tab")
    EDIT_ENTRY_ADD_COLLABORATOR_BUTTON                          = ('xpath', "//i[@class='icon-plus icon-white']")  
    EDIT_ENTRY_ADD_USER_TEXTBOX                                 = ('id', "EditEntryCollaborator-userId")
    EDIT_ENTRY_CO_EDITOR_CHECKBOX                               = ('id', "EditEntryCollaborator-permissions-2")
    EDIT_ENTRY_CO_PUBLISHER_CHECKBOX                            = ('id', "EditEntryCollaborator-permissions-1")
    EDIT_ENTRY_ADD_COLLABORATOR_SAVE_BUTTON                     = ('xpath', "//a[@class='btn btn btn-primary' and contains(text(), 'Add')]")
    EDIT_ENTRY_CHOSEN_USER_IN_COLLABORATOR_TABLE                = ('id', "collaborator_USER_NAME")
    EDIT_ENTRY_CHOSEN_USER_PERMISSION_IN_COLLABORATOR_TABLE     = ('xpath', "//td[@class='collaborationPermission' and contains(text(), 'USER_PERMISSION')]") # When using this locator, replace 'USER_PERMISSION' string with your real user_permission
    EDIT_ENTRY_SAVE_BUTTON                                      = ('xpath', "//button[@id='Entry-submit']")
    EDIT_ENTRY_OPTIONS_TAB_SAVE_BUTTON                          = ('id', "EntryOptions-submit")
    EDIT_ENTRY_SAVE_MASSAGE                                     = ('xpath', "//div[@class='alert alert-success ']")
    EDIT_ENTRY_OPTION_TAB                                       = ('id', 'options-tab')
    EDIT_ENTRY_THUMBNAIL_TAB                                    = ('id', 'thumbnails-tab-tab')
    EDIT_ENTRY_CAPTION_TAB                                      = ('id', 'captions-tab-tab')
    EDIT_ENTRY_TIMELINE_TAB                                     = ('id', 'chapters-tab')
    EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX                        = ('id', 'EntryOptions-commentsMulti-commentsDisabled')
    EDIT_ENTRY_ENABLE_SCHEDULING_RADIO                          = ('xpath', "//label[@class='schedulerRadioLabel radio' and contains(text(), 'Specific Time Frame')]")
    EDIT_ENTRY_SAVE_MASSAGE                                     = ('xpath' , "//div[@class='alert alert-success ']")
    EDIT_ENTRY_SCHEDULING_START_TIME_CALENDAR                   = ('xpath' , "//input[@aria-label='Start Time Time']")
    EDIT_ENTRY_SCHEDULING_START_DATE_CALENDAR                   = ('xpath' , "//input[@aria-label='Start Time Date']")
    EDIT_ENTRY_SCHEDULING_END_DATE_CALENDAR                     = ('xpath' , "//input[@aria-label='End Time Date']")
    EDIT_ENTRY_SCHEDULING_CALENDAR_TOP                          = ('xpath' , "//th[@class='datepicker-switch' and @colspan='5']")
    EDIT_ENTRY_SCHEDULING_CALENDAR_YEAR                         = ('xpath' , "//span[contains(@class,'year') and text()='YEAR']")# When using this locator, replace 'YEAR' string with your real year
    EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH                        = ('xpath' , "//span[contains(@class,'month') and text()='MONTH']")# When using this locator, replace 'MONTH' string with your real month
    EDIT_ENTRY_SCHEDULING_CALENDAR_DAY                          = ('xpath' , "//td[contains(@class,'day') and text()='DAY']")# When using this locator, replace 'DAY' string with your real day
    EDIT_ENTRY_SAVE_MASSAGE                                     = ('xpath' ,"//div[@class='alert alert-success ']")
    EDIT_ENTRY_CLOSED_COMMENTS_CHECKBOX                         = ('id', 'EntryOptions-commentsMulti-discussionClosed')
    EDIT_ENTRY_CLIP_PERMISSION_EVERYONE_CHECKBOX                = ('id', 'EntryOptions-ClipPermission-everyone')
    EDIT_ENTRY_GO_TO_MEDIA_BUTTON                               = ('xpath', "//a[@class='btn btn-link' and contains(text(), 'Go To Media')]")
    EDIT_ENTRY_SCHEDULING_START_TIME                            = ('xpath' ,"//input[@aria-label='Start Time Time']")
    EDIT_ENTRY_CAPTURE_THUMBNAIL_BUTTON                         = ('xpath', "//button[@id='thumbnail-capture-button']")
    EDIT_ENTRY_VERIFY_IMAGE_ADDED_TO_THUMBNAIL_AREA             = ('xpath', "//img[@alt='Thumbnail for media']")
    EDIT_ENTRY_THUMBNAIL_ENTRY_IN_CATEGORY                      = ('xpath', "//div[@class='photo-group thumb_wrapper' and @title='ENTRY_NAME']") # When using this locator, replace 'ENTRY_NAME' string with your real entry name
    EDIT_ENTRY_UPLOAD_CAPTION_BUTTON                            = ('id', 'upload')   
    EDIT_ENTRY_CAPTION_BROWSE_BUTTON                            = ('xpath', "//label[@class='captions-browse-button btn responsiveSize fileinput-button' and contains(text(), 'Browse...')]")
    EDIT_ENTRY_UPLOAD_CAPTION_SUCCESS_MESSAGE                   = ('xpath', "//div[@class='captions-upload-complete-message alert alert-success text-center']")
    EDIT_ENTRY_CAPTION_LABEL                                    = ('xpath', "//input[@id='Upload-label' and @name='Upload[label]']")
    EDIT_ENTRY_CAPTION_LANGUAGE                                 = ('id', 'Upload-language')
    EDIT_ENTRY_CAPTION_SAVE_BUTTON                              = ('xpath', "//a[@class='btn btn-primary captions-upload-modal-save-btn' and contains(text(), 'Save')]")
    EDIT_ENTRY_VARIFY_CAPTION_ADDED_TO_CAPRION_TABLE            = ('xpath', "//span[@data-type='label' and contains(text(), 'LABEL_NAME')]")# When using this locator, replace 'LABEL_NAME' string with your real label name
    EDIT_ENTRY_REMOVE_CAPTION_BUTTON                            = ('xpath', "//i[@class='icon-remove']")
    EDIT_ENTRY_CONFIRM_DELETE_BUTTON                            = ('xpath', "//a[@class='btn btn-danger' and contains(text(), 'Delete')]")
    EDIT_ENTRY_UPLOAD_SLIDES_DECK_TIME_LINE_BUTTON              = ('xpath', "//a[@class='btn btn-large fulldeck btn-combo kmstooltip' and @aria-label='Upload Slides Deck (PPT, PPTX, PDF)']")
    EDIT_ENTRY_UPLOAD_SLIDES_BUTTON                             = ('id', 'upload-fulldeck')
    EDIT_ENTRY_CHOOSE_FILE_TO_UPLOAD_BUTTON_IN_TIMELINE         = ('xpath', "//label[@class='btn btn-link fileinput-button']")
    EDIT_ENTRY_CUEPOINT_ON_TIMELINE                             = ('xpath', "//div[@class='k-cuepoint slide ui-draggable ui-draggable-handle']")
    #=============================================================================================================
    
    
    #  @Author: Tzachi Guetta
    def navigateToEditEntryPageFromMyMedia(self, entryName):
        tmp_entry_name = (self.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[0], self.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True        
        
        if self.clsCommon.myMedia.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to find: '" + entryName + "'")
            return False
                    
        if self.clsCommon.myMedia.clickEditEntryAfterSearchInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to on entry Edit button, Entry name: '" + entryName + "'")
            return False
        
        #Wait page load - wait for entry title
        if self.wait_visible(tmp_entry_name, 5) == False:
            writeToLog("INFO","FAILED to open edit entry page, Entry name: '" + entryName + "'")
            return False
        
        return True
    
    
    #  @Author: Tzachi Guetta
    def navigateToEditEntryPageFromEntryPage(self, entryName):
        tmp_entry_name = (self.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[0], self.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True  
        
        #Open "Actions" drop-down list 
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
            writeToLog("INFO","FAILED to click on Actions button")
            return False
         
        #Click on Edit button
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Edit button")
            return False    
        
        #Wait page load - wait for entry title
        if self.wait_visible(tmp_entry_name, 5) == False:
            writeToLog("INFO","FAILED to open edit entry page")
            return False
        
        return True

        
    # Author: Michal Zomper   
    def addCollaborator(self, entryName, userId, isCoEditor, isCoPublisher):
        #Click on collaboration tab
        if self.clickOnEditTab(enums.EditEntryPageTabName.COLLABORATION) == False:
            writeToLog("INFO","FAILED to click on collaboration tab")
            return False    
        
        sleep(1)
        #click on add collaborator
        if self.click(self.EDIT_ENTRY_ADD_COLLABORATOR_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on add collaborator button")
            return False       
        
        sleep(2)
        # Enter user name 
        if self.send_keys(self.EDIT_ENTRY_ADD_USER_TEXTBOX, userId) == False:
            writeToLog("DEBUG","FAILED to type user name in collaborator textbox")
            return False  
        
        # Check if need to add co editor
        if isCoEditor == True:
            # Click to add co editor
            if self.click(self.EDIT_ENTRY_CO_EDITOR_CHECKBOX, 30) == False:
                writeToLog("INFO","FAILED to click on co editor checkbox")
                return False  
            
        # Check if need to add co publisher
        if isCoPublisher == True:
            # Click to add co editor
            if self.click(self.EDIT_ENTRY_CO_PUBLISHER_CHECKBOX, 30) == False:
                writeToLog("INFO","FAILED to click on co publisher checkbox")
                return False    
               
        # Click on save              
        if self.click(self.EDIT_ENTRY_ADD_COLLABORATOR_SAVE_BUTTON , 30) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False 
        
        # Check that the user was added to collaboration permissions table
        tmp_user_name = (self.EDIT_ENTRY_CHOSEN_USER_IN_COLLABORATOR_TABLE[0], self.EDIT_ENTRY_CHOSEN_USER_IN_COLLABORATOR_TABLE[1].replace('USER_NAME', userId))
        parentEl = self.get_element(tmp_user_name)
        if parentEl == None:
            writeToLog("INFO","FAILED to find added user in collaboration permissions table")
            return False      
        
        # set the permissions locator 
        if isCoEditor == True and isCoPublisher == True:
            tmp_permissions = (self.EDIT_ENTRY_CHOSEN_USER_PERMISSION_IN_COLLABORATOR_TABLE[0], self.EDIT_ENTRY_CHOSEN_USER_PERMISSION_IN_COLLABORATOR_TABLE[1].replace('USER_PERMISSION', "Co-Editor, Co-Publisher"))
        elif isCoEditor == True and isCoPublisher == False:
            tmp_permissions = (self.EDIT_ENTRY_CHOSEN_USER_PERMISSION_IN_COLLABORATOR_TABLE[0], self.EDIT_ENTRY_CHOSEN_USER_PERMISSION_IN_COLLABORATOR_TABLE[1].replace('USER_PERMISSION', "Co-Editor"))
        elif isCoEditor == False and isCoPublisher == True:
            tmp_permissions = (self.EDIT_ENTRY_CHOSEN_USER_PERMISSION_IN_COLLABORATOR_TABLE[0], self.EDIT_ENTRY_CHOSEN_USER_PERMISSION_IN_COLLABORATOR_TABLE[1].replace('USER_PERMISSION', "Co-Publisher"))   
        
        # Check that the user permissions correctly were added to collaboration permissions table
        try:
            self.get_child_element(parentEl, tmp_permissions)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to find added user permissions in collaboration permissions table")
            return False
        
        writeToLog("INFO","Success user was added successfully as collaborator to entry:'" + entryName + "'")
        return True 
            
        
    # Author: Michal Zomper                
    def changeEntryMetadata (self, entryName, newEntryName, newDescription, NewTags): 
        if self.navigateToEditEntryPageFromEntryPage(entryName) == False:
            writeToLog("INFO","FAILED navigate to edit entry page from entry page with collaborator user")
            return False
        sleep(2)
        if self.clsCommon.upload.fillFileUploadEntryDetails(newEntryName, newDescription, NewTags)  == False:
            writeToLog("INFO","FAILED to insert new metadata to entry '" +  entryName + "' with collaborator user")
            return False
        
        if self.click(self.EDIT_ENTRY_SAVE_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on save button ")
            return False
        
        if self.wait_visible(self.EDIT_ENTRY_SAVE_MASSAGE, 30) == False:
            writeToLog("INFO","FAILED to find save massage")
            return False
        sleep(3)
        
        writeToLog("INFO","Success metadata were change successfully")
        return True
    
    
#    How-to: if entryName was delivered - the function will first navigate to the entry's edit page
#    TODO: add full description this the function
    def addPublishingSchedule(self, startDate='', startTime='', endDate='', endTime='', timeZone='', entryName=''):
        try:
            if len(entryName) != 0:
                if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False   
        
            if self.click(self.EDIT_ENTRY_ENABLE_SCHEDULING_RADIO) == False:
                writeToLog("INFO","FAILED to click on 'Specific Time Frame' radiobox")
                return False
            
            if len(startDate) != 0:
                if self.setScheduleStartDate(startDate) == False:
                    return False
                sleep(2) 
            # else = use the default value
            
            if len(startTime) != 0:
                self.clear_and_send_keys(self.EDIT_ENTRY_SCHEDULING_START_TIME_CALENDAR, startTime)
                sleep(2) 
            # else = use the default value
            
            if len(endDate) != 0:
                if self.setScheduleEndDate(endDate) == False:
                    return False
                sleep(2)  
            # else = use the default value
            
            if len(endTime) != 0:
                self.clear_and_send_keys(self.EDIT_ENTRY_SCHEDULING_START_TIME_CALENDAR, endTime)
                sleep(2)
            # else = use the default value
            
            # The below if checking if you are in Edit entry page OR in upload page
            if len(entryName) != 0: 
                if self.click(self.EDIT_ENTRY_SAVE_BUTTON, 30) == False:
                    writeToLog("INFO","FAILED to click on save button ")
                    return False
            
                self.clsCommon.general.waitForLoaderToDisappear()

                if self.wait_visible(self.EDIT_ENTRY_SAVE_MASSAGE, 30) == False:
                    writeToLog("INFO","FAILED to find save massage")
                    return False
            else:
                # You are at Upload page, then: Click Save
                if self.click(self.clsCommon.upload.UPLOAD_ENTRY_SAVE_BUTTON) == False:
                    writeToLog("DEBUG","FAILED to click on 'Save' button")
                    return None
                sleep(2)
    
                # Wait for loader to disappear
                self.clsCommon.general.waitForLoaderToDisappear()
          
        except NoSuchElementException:
            return False
          
        return True

      
    # Author: Michal Zomper    
    # tabName - enums.EditEntryPageTabName    
    def clickOnEditTab(self, tabName):
        if tabName == enums.EditEntryPageTabName.OPTIONS: 
            if self.click(self.EDIT_ENTRY_OPTION_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on option tab")
                return False
    
        elif tabName == enums.EditEntryPageTabName.COLLABORATION:
            if self.click(self.EDIT_ENTRY_COLLABORATION_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on Collaboration tab")
                return False

        elif tabName == enums.EditEntryPageTabName.THUMBNAILS:
            if self.click(self.EDIT_ENTRY_THUMBNAIL_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on Thumbnails tab")
                return False
            
        elif tabName == enums.EditEntryPageTabName.CAPTIONS:
            if self.click(self.EDIT_ENTRY_CAPTION_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on Captions tab")
                return False
            
        elif tabName == enums.EditEntryPageTabName.TIMELINE:
            if self.click(self.EDIT_ENTRY_TIMELINE_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on time-line tab")
                return False
        else:
            writeToLog("INFO","FAILED, Unknown tabName")
            return False
        
        return True   


      
    # Author: Michal Zomper 
    def changeEntryOptions(self, isEnableComments, isEnableCloseDiscussion, isEnableEveryoneToCreateClip):
        if self.clickOnEditTab(enums.EditEntryPageTabName.OPTIONS) == False:
            writeToLog("INFO","FAILED to click on options tab")
            return False
         
        # Disable comments 
        if self.check_element(self.EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX, isEnableComments) == False:
            writeToLog("INFO","FAILED to check/uncheck 'Disable comments' option")
            return False
                   
        # Close Discussion 
        if self.check_element(self.EDIT_ENTRY_CLOSED_COMMENTS_CHECKBOX, isEnableCloseDiscussion) == False:
            writeToLog("INFO","FAILED to check/uncheck 'Disable comments' option")
            return False
                   
        # Enable Everyone To Create Clip
        if self.check_element(self.EDIT_ENTRY_CLIP_PERMISSION_EVERYONE_CHECKBOX, isEnableEveryoneToCreateClip) == False:
            writeToLog("INFO","FAILED to check/uncheck 'Disable comments' option")
            return False
                                    
        if self.click(self.EDIT_ENTRY_OPTIONS_TAB_SAVE_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(3)
       
        if self.get_elements(self.EDIT_ENTRY_GO_TO_MEDIA_BUTTON)[1].click() == False:
        #if self.click(self.EDIT_ENTRY_GO_TO_MEDIA_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on 'go to media' button")
            return False            
        sleep(3)
        
        #Open "Actions" drop-down list 
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
            writeToLog("INFO","FAILED to click on Actions button")
            return False
         
        #Click on Edit button
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Edit button")
            return False 
        sleep(2)
        
        if self.clickOnEditTab(enums.EditEntryPageTabName.OPTIONS) == False:
            writeToLog("INFO","FAILED to click on option tab")
            return False 
        
        # Verify Disable comments 
        if self.is_element_checked(self.EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX) == False:
            writeToLog("INFO","FAILED to verify check/uncheck 'Disable comments' option")
            return False
                   
        # Verify Close Discussion 
        if self.is_element_checked(self.EDIT_ENTRY_CLOSED_COMMENTS_CHECKBOX) == False:
            writeToLog("INFO","FAILED to verify check/uncheck 'Disable comments' option")
            return False
                   
        # Verify Enable Everyone To Create Clip
        if self.is_element_checked(self.EDIT_ENTRY_CLIP_PERMISSION_EVERYONE_CHECKBOX) == False:
            writeToLog("INFO","FAILED to verify check/uncheck 'Disable comments' option")
            return False
        
        return True
     

    # Format desteStr - '24/01/2018'
    # startOrEnd - String 'start' or 'end'
    def setScheduleStartDate(self, dateStr):
        return self.setScheduleDate(dateStr, 'start')
    
    
    def setScheduleEndDate(self, dateStr):
        return self.setScheduleDate(dateStr, 'end')
        
       
    def setScheduleDate(self, dateStr, startOrEnd):
        if startOrEnd.lower() == 'start':
            locator = self.EDIT_ENTRY_SCHEDULING_START_DATE_CALENDAR
        elif startOrEnd.lower() == 'end':
            locator = self.EDIT_ENTRY_SCHEDULING_END_DATE_CALENDAR
        else:
            writeToLog("INFO","FAILED, unknown Schedule start/stop type: '" + startOrEnd + "'")
            return False            
        # Extract from dateStr the day, month, year
        day = dateStr.split('/')[0]
        # Convert to int and back to string, to remove 0 before a digit. For example from '03' to '3'
        intDay = int(day)
        day = str(intDay)
        formated_month = datetime.datetime.strptime(dateStr, "%d/%m/%Y")
        month = formated_month.strftime("%b")
        year = dateStr.split('/')[2]
        
        # Click on Start Date calendar
        if self.click(locator) == False:
                writeToLog("INFO","FAILED to click start date calendar")
                return False
            
        # Set a year
        # Click on the year - at the top of the calendar
        if self.click(self.EDIT_ENTRY_SCHEDULING_CALENDAR_TOP) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the year")
            return False
        
        # Click again to show all years
        if self.click(self.EDIT_ENTRY_SCHEDULING_CALENDAR_TOP, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the year")
            return False
        
        # Select a year
        if self.click((self.EDIT_ENTRY_SCHEDULING_CALENDAR_YEAR[0], self.EDIT_ENTRY_SCHEDULING_CALENDAR_YEAR[1].replace('YEAR', year))) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the year")
            return False        
        
        # Set Month
        if self.click((self.EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH[0], self.EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH[1].replace('MONTH', month))) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the month")
            return False
        
        # Set Day
        if self.click((self.EDIT_ENTRY_SCHEDULING_CALENDAR_DAY[0], self.EDIT_ENTRY_SCHEDULING_CALENDAR_DAY[1].replace('DAY', day))) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the day")
            return False
         
    # Author: Michal Zomper 
    # TODO : add stop player in the given time and verify that the image that was capture is correct   
    def captureThumbnail(self, timeToStop="", qrCodeRedult=""): 
        if self.clickOnEditTab(enums.EditEntryPageTabName.THUMBNAILS) == False:
            writeToLog("INFO","FAILED to click on the thumbnail tab")
            return False
        
        if timeToStop == "" or qrCodeRedult == "":
            if self.click(self.EDIT_ENTRY_CAPTURE_THUMBNAIL_BUTTON, 30) == False:
                writeToLog("INFO","FAILED to click on capture thumbnail button")
                return False
            
            # verify image was add
            if self.wait_visible(self.EDIT_ENTRY_VERIFY_IMAGE_ADDED_TO_THUMBNAIL_AREA, 20) == False:
                writeToLog("INFO","FAILED to verify capture was added to thumbnail area")
                return False
        
        return True       

    
    # Author: Michal Zomper
    def addCaptions(self, captionFilePath, captionLanguage, captionLabel):
        if self.clickOnEditTab(enums.EditEntryPageTabName.CAPTIONS) == False:
            writeToLog("INFO","FAILED to click on the caption tab")
            return False
            
        if self.click(self.EDIT_ENTRY_UPLOAD_CAPTION_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click on upload caption file button")
            return False
        sleep(2)
        
        # Click on browse
        if self.click(self.EDIT_ENTRY_CAPTION_BROWSE_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click on browse caption button")
            return False
        sleep(2)
        # Type in a file path
        self.clsCommon.upload.typeIntoFileUploadDialog(captionFilePath)
        
        # Verify caption file was uploaded
        if self.wait_visible(self.EDIT_ENTRY_UPLOAD_CAPTION_SUCCESS_MESSAGE, 20) == False:
            writeToLog("INFO","FAILED to find caption uploaded success message")
            return False
        sleep(1)            
        
        # choose caption language
        if self.select_from_combo_by_text(self.EDIT_ENTRY_CAPTION_LANGUAGE, captionLanguage) == False:
            writeToLog("INFO","FAILED select caption language")
            return False 
        sleep(1)
        
        # Enter caption label
        if self.click(self.EDIT_ENTRY_CAPTION_LABEL, 20) == False:
            writeToLog("INFO","FAILED to on label name text box")
            return False  
            
        if self.send_keys(self.EDIT_ENTRY_CAPTION_LABEL, captionLabel) == False:
            writeToLog("INFO","FAILED to insert label name")
            return False  
            
        # Click save
        if self.click(self.EDIT_ENTRY_CAPTION_SAVE_BUTTON, 20) == False:
            writeToLog("INFO","FAILED click on save caption button")
            return False              
        sleep(3)
        
        # Verify caption was added to caption table
        tmpLabel = (self.EDIT_ENTRY_VARIFY_CAPTION_ADDED_TO_CAPRION_TABLE[0], self.EDIT_ENTRY_VARIFY_CAPTION_ADDED_TO_CAPRION_TABLE[1].replace('LABEL_NAME', captionLabel))
        if self.is_visible(tmpLabel) == False:
            writeToLog("INFO","FAILED verify uploaded caption added to caption table")
            return False    
        sleep(2)    
        
        writeToLog("INFO","Success caption was added successfully") 
        return True
    
    
    # Author: Michal Zomper       
    def removeCaption(self, captionLabel):
        if self.clickOnEditTab(enums.EditEntryPageTabName.CAPTIONS) == False:
            writeToLog("INFO","FAILED to click on the caption tab")
            return False
        
        tmpLabel = self.EDIT_ENTRY_VARIFY_CAPTION_ADDED_TO_CAPRION_TABLE[1].replace('LABEL_NAME', captionLabel)
        sleep(1)
        
        # find caption label click on the remove button in the label row
        elParent = self.driver.find_element_by_xpath(tmpLabel+"/ancestor::div[@class='row-fluid captionRow']")
        if elParent == None:
            writeToLog("INFO","FAILED find caption row in captions table")
        sleep(2)
        
        elements = elParent.find_elements_by_xpath(self.EDIT_ENTRY_REMOVE_CAPTION_BUTTON[1])
        if self.clickElement(elements, True) == False:
            writeToLog("INFO","FAILED to click on remove caption button")
        sleep(3)
        
        # Click on confirm delete
        if self.click(self.EDIT_ENTRY_CONFIRM_DELETE_BUTTON, 20, True) == False:
            writeToLog("INFO","FAILED to click on remove caption button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(3)
        
        # Verify caption was deleted to caption table
        tmpLabel = (self.EDIT_ENTRY_VARIFY_CAPTION_ADDED_TO_CAPRION_TABLE[0], self.EDIT_ENTRY_VARIFY_CAPTION_ADDED_TO_CAPRION_TABLE[1].replace('LABEL_NAME', captionLabel))
        if self.is_visible(tmpLabel) == True:
            writeToLog("INFO","FAILED to delete caption from caption table")
            return False 
        sleep(2)     
        
        writeToLog("INFO","Success caption was deleted successfully") 
        return True
    
    
    # Author: Michal Zomper
    # NOT finish
    def uploadSlidesDeck(self, filePath):
        if self.clickOnEditTab(enums.EditEntryPageTabName.TIMELINE) == False:
            writeToLog("INFO","FAILED to click on the time-line tab")
            return False
         
        # Click on the upload slides button in the time line bar 
        if self.click(self.EDIT_ENTRY_UPLOAD_SLIDES_DECK_TIME_LINE_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click on upload slides deck button in the time line bar")
            return False           
         
        # click on the upload button 
        if self.click(self.EDIT_ENTRY_UPLOAD_SLIDES_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click on upload slides button")
            return False              
         
        if self.click(self.EDIT_ENTRY_CHOOSE_FILE_TO_UPLOAD_BUTTON_IN_TIMELINE, 20) == False:
            writeToLog("INFO","FAILED to click on choose a file to upload button")
            return False            
         
        self.clsCommon.upload.typeIntoFileUploadDialog(filePath)
         
        # Wait until the ptt will upload 
        sleep(20)
         
        # Verify cuepoint  were added to time line
        # Their should be 9 cuepoint
        if len(self.get_elements(self.EDIT_ENTRY_CUEPOINT_ON_TIMELINE)) != 9:
            writeToLog("INFO","FAILED, Not all cuepoints were added to timeline")
            return False 
        
        writeToLog("INFO","Success presentation was upload and added to time line successfully")
        return True
            