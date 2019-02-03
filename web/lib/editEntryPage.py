from selenium.webdriver.common.keys import Keys

from base import *
import clsCommon
import clsTestService
import enums
import utilityTestFunc


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
    EDIT_ENTRY_CO_EDITOR_CHECKBOX                               = ('xpath', "//label[contains(@class,'checkbox') and text()='Co-Editor']")
    EDIT_ENTRY_CO_PUBLISHER_CHECKBOX                            = ('xpath', "//label[contains(@class,'checkbox') and text()='Co-Publisher']")
    EDIT_ENTRY_ADD_COLLABORATOR_SAVE_BUTTON                     = ('xpath', "//a[contains(@class,'btn btn btn-primary')]")
    EDIT_ENTRY_CHOSEN_USER_IN_COLLABORATOR_TABLE                = ('id', "collaborator_USER_NAME")
    EDIT_ENTRY_CHOSEN_USER_PERMISSION_IN_COLLABORATOR_TABLE     = ('xpath', "//td[@class='collaborationPermission' and contains(text(), 'USER_PERMISSION')]") # When using this locator, replace 'USER_PERMISSION' string with your real user_permission
    EDIT_ENTRY_SAVE_BUTTON                                      = ('xpath', "//button[@id='Entry-submit']")
    EDIT_ENTRY_OPTIONS_TAB_SAVE_BUTTON                          = ('id', "EntryOptions-submit")
    EDIT_ENTRY_SAVE_BUTTON_FLAVOR                               = ('id', "EditFlavors-submit")
    EDIT_ENTRY_DETAILS_TAB                                      = ('id', 'details-tab')
    EDIT_ENTRY_OPTION_TAB                                       = ('id', 'options-tab')
    EDIT_ENTRY_THUMBNAIL_TAB                                    = ('id', 'thumbnails-tab-tab')
    EDIT_ENTRY_CAPTION_TAB                                      = ('id', 'captions-tab-tab')
    EDIT_ENTRY_DOWNLOADS_TAB                                    = ('id', 'downloads-tab-tab')
    EDIT_ENTRY_TIMELINE_TAB                                     = ('id', 'chapters-tab')
    EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX                        = ('id', 'EntryOptions-commentsMulti-commentsDisabled')
    EDIT_ENTRY_ENABLE_SCHEDULING_RADIO                          = ('xpath', "//label[@class='schedulerRadioLabel radio' and contains(text(), 'Specific Time Frame')]")
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
    EDIT_ENTRY_THUMBNAIL_PROGRESS_BAR                           = ('xpath', "//div[@id='thumbnailProgress' and @class='bar thumbnails-progressbar bar-success']")
    EDIT_ENTRY_THUMBNAIL_CAPTURED_MES                           = ('xpath', "//button[@class='close' contains(text(), 'Thumbnail has been captured')']")
    EDIT_ENTRY_UPLOAD_THUMBNAIL_BUTTON                          = ('xpath', "//label[@class='thumbnails_upload_button_label']")
    EDIT_ENTRY_THUMBNAIL_AUTO_GENERATE_BUTTON                   = ('xpath', "//button[@id='thumbnail-generate-button' and @class='btn responsiveSize']")
    EDIT_ENTRY_CHOOSE_AUTO_GENERATE_THUMBNAIL                   = ('xpath', "//a[@class='thumbnail' and contains(@href,'/slice/SLOCE_NUMBER/slices/')]") # When using this locator, replace 'SLOCE_NUMBER' string with your real slice number
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
    EDIT_ENTRY_CONFIRM_DELETE_BUTTON                            = ('xpath', "//a[@class='btn btn-danger' and contains(text(), 'Delete') and @href='javascript:;']")
    EDIT_ENTRY_UPLOAD_SLIDES_DECK_TIME_LINE_BUTTON              = ('xpath', "//a[@class='btn btn-large fulldeck btn-combo kmstooltip' and @aria-label='Upload Slides Deck (PPT, PPTX, PDF)']")
    EDIT_ENTRY_DOWNLOADS_FLAVOR                                 = ('xpath', "//label[@class='checkbox' and contains(.,'FLAVOR_NAME')]") #pay attention: this locator is relevant to SOURCE Flavor ONLY
    EDIT_ENTRY_UPLOAD_SLIDES_BUTTON                             = ('id', 'upload-fulldeck')
    EDIT_ENTRY_CHOOSE_FILE_TO_UPLOAD_BUTTON_IN_TIMELINE         = ('xpath', "//label[@class='btn btn-link fileinput-button']")
    EDIT_ENTRY_CUEPOINT_ON_TIMELINE                             = ('xpath', "//div[@class='k-cuepoint slide ui-draggable ui-draggable-handle']")
    EDIT_ENTRY_UPLOAD_DECK_PROCES                               = ('id', 'inProgressMessage')
    EDIT_ENTRY_DELETE_SLIDE_BUTTON_FORM_TIME_LINE               = ('xpath', "//a[@class='btn btn-link remove' and @role ='button']")
    EDIT_ENTRY_SLIDE_IN_TIMELINE                                = ('xpath',"//div[@class='k-cuepoint slide ui-draggable ui-draggable-handle' and @data-time='SLIDE_TIME']")
    EDIT_ENTRY_VIEW_IN_PLAYER_BUTTON                            = ('xpath',"//a[@id='refresh' and @class='btn btn-block']")
    EDIT_ENTRY_ADD_CHAPTER                                      = ('xpath', "//a[@class='btn btn-large chapter kmstooltip' and @aria-label='Create a new Chapter']")
    EDIT_ENTRY_INSERT_CHAPTER_TITLE                             = ('xpath',"//input[@id='k-title' and @placeholder='Enter Chapter Title']")
    EDIT_ENTRY_INSERT_TIME_TO_SLIDE_OR_CHAPTER                  = ('xpath', "//input[@id='k-currentTime' and @name='chapters[time]']")
    EDIT_ENTRY_SAVE_CHAPTER_OR_SLIDE                            = ('xpath', "//a[@id='save' and @class='btn btn-large btn-block btn-primary']")
    EDIT_ENTRY_SAVED_CHAPTER_OR_SLIDE_SUCCESS_MSG               = ('xpath', "//a[@id='saved' and @class='btn btn-large btn-block btn-success']")
    EDIT_ENTRY_CHAPTER_IN_TIME_LINE                             = ('xpath', "//div[@class='k-cuepoint chapter ui-draggable ui-draggable-handle' and @data-time='CHAPTER_TIME']")# When using this locator, replace 'CHAPTER_TIME' string with your real chapter time
    EDIT_ENTRY_DELETE_CHAPTER_BUTTON                            = ('xpath', "//a[@class='btn btn-link remove' and @role='button']")
    EDIT_ENTRY_DISCLAIMER_TEXT_BOX                              = ('xpath', "//div[@id='disclaimet-text']")
    EDIT_ENTRY_BACK_TO_TIMELINE                                 = ('xpath', "//a[contains(text(), 'Back to Timeline')]" )
    EDIT_ENTRY_INSERT_SLIDE_TITLE                               = ('xpath',"//input[@id='k-title' and @placeholder='Enter Slide Title']")
    EDIT_ENTRY_REPLACE_VIDEO_TAB                                = ('xpath', '//a[@id="replacemedia-tab"]')
    EDIT_ENTRY_UPLOAD_NEW_FILE                                  = ('xpath', '//label[@for="replace_media_fileinput"]')
    EDIT_ENTRY_APPROVE_REPLACMENT_BUTTON                        = ('xpath', '//button[@id="approveReplacmentBtn"]')
    EDIT_ENTRY_MEDIA_SUCCESSFULLY_REPLACED_MSG                  = ('xpath', '//div[@class="alert alert-success " and contains(text(),"Your media was successfully replaced")]') 
    EDIT_ENTRY_MEDIA_IS_BEING_PROCCESSED_MSG                    = ('xpath', '//div[@class="alert alert-success " and text()="Your media is being processed"]')
    EDIT_ENTRY_ATTACHMENTS_TAB                                  = ('xpath', '//a[contains(@id,"attachments-tab")]')# USE multipleElements=True
    EDIT_ENTRY_ATTACHMENTS_UPLOAD_FILE                          = ('xpath', '//a[contains(@href, "attachments") and text()="Upload File    "]')
    EDIT_ENTRY_ATTACHMENTS_SELECT_FILE                          = ('xpath', '//label[@for="attachments_fileinput"]')
    EDIT_ENTRY_UPLOAD_ATTACHMENTS_TITLE                         = ('xpath', '//input[@id="title"]')
    EDIT_ENTRY_UPLOAD_ATTACHMENTS_DESCRIPTION                   = ('xpath', '//textarea[contains(@id, "description") and @class="noresize"]')
    EDIT_ENTRY_UPLOAD_ATTACHMENTS_SAVE_BUTTON                   = ('xpath', '//a[@data-handler="1" and text()="Save"]')
    EDIT_ENTRY_UPLOADED_ATTACHMENT_FIELDS                       = ('xpath', '//span[@title="ENTRY_FIELD"]')
    EDIT_ENTRY_UPLOAD_ATTACHMENT_SUCCESS_MSG                    = ('xpath', '//div[@class="alert alert-success " and text()="The information was saved successfully"]')
    EDIT_ENTRY_UPLOAD_ATTACHMENT_COMPLETED_SUCCESS_MSG          = ('xpath', '//div[@id="successmsg" and @class="alert alert-success text-center"]')
    EDIT_ENTRY_EDIT_ATTACHMENT_ICON                             = ('xpath', '//i[@class="icon-pencil icon-large"]')
    EDIT_ENTRY_DOWNLOAD_ATTACHMENT_ICON                         = ('xpath', '//i[@class="icon-download icon-large offset1"]')
    EDIT_ENTRY_REMOVE_ATTACHMENT_ICON                           = ('xpath', '//i[@class="icon-remove-sign icon-large offset1"]')
    EDIT_ENTRY_DELETE_CONFIRMATION_BTN                          = ('xpath', '//a[@class="btn btn-danger" and text()="Delete"]')
    EDIT_ENTRY_DELETE_CONFIRMATION_MSG                          = ('xpath', '//div[@class="alert alert-success " and text()="Attachment was deleted successfully"]')
    EDIT_ENTRY_UPLOAD_SUCCESS_MSG                               = ('xpath', '//div[@class="alert alert-success " and text()="The information was saved successfully"]')
    EDIT_ENTRY_EDIT_ATTACHMENT_MODAL_BODY                       = ('xpath', '//form[@id="changeAttachment"]')
    EDIT_ENTRY_NO_ATTACHMENT_MSG                                = ('xpath', '//div[@id="empty"]')
    EDIT_ENTRY_DELETE_ATTACHMENT_MODAL                          = ('xpath', '//a[@class="close" and text()="Delete Confirmation"]')
#    EDIT_ENTRY_DELETE_ENTRY_BUTTON                              = ('xpath', "//a[@id='deleteMediaBtn']")
    EDIT_ENTRY_DELETE_ENTRY_BUTTON                              = ('xpath', "//a[contains(@id,'deleteMediaBtn')]")
    EDIT_ENTRY_CUSTOM_DATA_TEXT_FIELD                           = ('xpath', '//input[@id="customdata-FIELD_NAME"]')  
    EDIT_ENTRY_CUSTOM_LIST_FIELD                                = ('xpath', '//select[@id="customdata-FIELD_NAME"]')   
    EDIT_ENTRY_ADD_UNLIMITED_TEXT_CUSTOMDATA_FIELD              = ('xpath', '//button[@id="customdata-FIELD_NAME-addBtn"]')
    EDIT_ENTRY_CUSTOM_DATE                                      = ('xpath', '//input[@id="customdata-FIELD_NAME"]')
    EDIT_ENTRY_CUSTOM_DATEPICKER_SWITCH                         = ('xpath', '//th[@class="datepicker-switch"]')
    EDIT_ENTRY_CUSTOM_DATE_INTERVAL_YEAR_OR_DATE                = ('xpath', '//span[contains(text(),"YEAR_or_DATE")]')    
    EDIT_ENTRY_CUSTOM_DATE_DAY                                  = ('xpath', "//td[@class='day'][contains(text(),'DAY')]")  
    EDIT_ENTRY_CHANGE_MEDIA_OWNER                               = ('xpath', "//a[@id='change_owner']")
    EDIT_ENTRY_CHANGE_MEDIA_OWNER_POP_UP_TITLE                  = ('xpath', "//h3[contains(text(),'Change Media Owner')]") 
    EDIT_ENTRY_CHANGE_MEDIA_OWNER_SAVE_BUTTON                   = ('xpath', "//a[contains(text(),'Save')]")                                                    
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
        if self.wait_visible(tmp_entry_name, 30) == False:
            writeToLog("INFO","FAILED to open edit entry page, Entry name: '" + entryName + "'")
            return False
        
        return True
    
    
    #  @Author: Tzachi Guetta
    def navigateToEditEntryPageFromEntryPage(self, entryName):
        tmp_entry_name = (self.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[0], self.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_element(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True  
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            self.click(self.clsCommon.entryPage.ENTRY_PAGE_DETAILS_BUTTON, timeout=5 ,multipleElements=True)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
        
        sleep(2)
        #Open "Actions" drop-down list 
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on Actions button")
            return False
        
        #Click on Edit button
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Edit button")
            return False
        
        #Wait page load - wait for entry title 
        if self.wait_element(tmp_entry_name, 20) == False:
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
        # Insert username to field
        if self.send_keys(self.clsCommon.channel.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, userId) == False:
            writeToLog("INFO","FAILED to insert username")
            return False
        
        sleep(3)
        if self.send_keys(self.clsCommon.channel.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, Keys.RETURN) == False:
            writeToLog("INFO","FAILED to press Enter after username was typed")
            return False   
                
        sleep(3)
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
               
        sleep(1)  
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
    # Author: Tzachi Guetta
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
                self.setScheduleTime(self.EDIT_ENTRY_SCHEDULING_START_TIME_CALENDAR, startTime)
                sleep(2) 
            # else = use the default value
            
            if len(endDate) != 0:
                if self.setScheduleEndDate(endDate) == False:
                    return False
                sleep(2)  
            # else = use the default value
            
            if len(endTime) != 0:
                self.setScheduleTime(self.EDIT_ENTRY_SCHEDULING_START_TIME_CALENDAR, endTime)
                sleep(2)
            # else = use the default value
            
            # The below if checking if you are in Edit entry page OR in upload page
            if len(entryName) != 0: 
                sleep(2)
                if self.click(self.EDIT_ENTRY_SAVE_BUTTON, 30) == False:
                    writeToLog("INFO","FAILED to click on save button ")
                    return False
                
                self.clsCommon.general.waitForLoaderToDisappear()
                sleep(2) 
                
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


    # This is work around method for set Schedule Time, instead of using "self.clear_and_send_keys(self.EDIT_ENTRY_SCHEDULING_START_TIME_CALENDAR, startTime)"
    # self.clear_and_send_keys() stopped to work with the schedule filed, it wont clear the filed
    def setScheduleTime(self, locator, text, multipleElements=False):
        try:
            element = self.wait_visible(locator, 15, multipleElements)
            if element == False:
                writeToLog("INFO", "FAILED to get schedule time filed")
                return False
            
            ActionChains(self.driver).click(element).perform()
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            element.send_keys(Keys.BACK_SPACE)
            sleep(2)
            element.send_keys(text)
            return True
        except:
            writeToLog("INFO", "FAILED to type text: " + str(text))
            return False    

      
    # Author: Michal Zomper    
    # tabName - enums.EditEntryPageTabName    
    def clickOnEditTab(self, tabName):
        if tabName == enums.EditEntryPageTabName.DETAILS:
            if self.click(self.EDIT_ENTRY_DETAILS_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on details tab")
                return False
            
        elif tabName == enums.EditEntryPageTabName.OPTIONS: 
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
            
        elif tabName == enums.EditEntryPageTabName.DOWNLOADS:
            if self.click(self.EDIT_ENTRY_DOWNLOADS_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on downloads tab")
                return False  
            
        elif tabName == enums.EditEntryPageTabName.REPLACE_VIDEO:
            if self.click(self.EDIT_ENTRY_REPLACE_VIDEO_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on replace video tab")
                return False 
            
        elif tabName == enums.EditEntryPageTabName.ATTACHMENTS:
            if self.click(self.EDIT_ENTRY_ATTACHMENTS_TAB, 30, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on attachment tab")
                return False             
                                  
        else:
            writeToLog("INFO","FAILED, Unknown tabName")
            return False
        
        return True   

      
    # Author: Michal Zomper 
    def changeEntryOptions(self, isEnableComments, isEnableCloseDiscussion, isEnableEveryoneToCreateClip, entryType=enums.MediaType.VIDEO):
        if self.clickOnEditTab(enums.EditEntryPageTabName.OPTIONS) == False:
            writeToLog("INFO","FAILED to click on options tab")
            return False
         
        # Disable comments 
        if self.check_element(self.EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX, isEnableComments) == False:
            writeToLog("INFO","FAILED to check/uncheck 'Disable comments' option")
            return False
                   
        # Close Discussion 
        if self.check_element(self.EDIT_ENTRY_CLOSED_COMMENTS_CHECKBOX, isEnableCloseDiscussion) == False:
            writeToLog("INFO","FAILED to check/uncheck 'Close Discussion' option")
            return False
        
        if entryType == enums.MediaType.VIDEO:       
            # Enable Everyone To Create Clip
            if self.check_element(self.EDIT_ENTRY_CLIP_PERMISSION_EVERYONE_CHECKBOX, isEnableEveryoneToCreateClip) == False:
                writeToLog("INFO","FAILED to check/uncheck 'Enable everyone to create clips from this video' option")
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
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
            self.click(self.clsCommon.entryPage.ENTRY_PAGE_DETAILS_BUTTON)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
        
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
        if self.is_element_checked(self.EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX) != isEnableComments:
            writeToLog("INFO","FAILED to verify check/uncheck 'Disable comments' option")
            return False
                   
        # Verify Close Discussion 
        if self.is_element_checked(self.EDIT_ENTRY_CLOSED_COMMENTS_CHECKBOX) != isEnableCloseDiscussion:
            writeToLog("INFO","FAILED to verify check/uncheck 'Disable comments' option")
            return False
        
        if entryType == enums.MediaType.VIDEO:            
            # Verify Enable Everyone To Create Clip
            if self.is_element_checked(self.EDIT_ENTRY_CLIP_PERMISSION_EVERYONE_CHECKBOX) != isEnableEveryoneToCreateClip:
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
            locator = (self.EDIT_ENTRY_SCHEDULING_START_DATE_CALENDAR[0], self.EDIT_ENTRY_SCHEDULING_START_DATE_CALENDAR[1] + "/following-sibling::span")
        elif startOrEnd.lower() == 'end':
            locator = (self.EDIT_ENTRY_SCHEDULING_END_DATE_CALENDAR[0], self.EDIT_ENTRY_SCHEDULING_END_DATE_CALENDAR[1] + "/following-sibling::span")
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
            writeToLog("INFO","FAILED to select the year")
            return False        
        
        # Set Month
        if self.click((self.EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH[0], self.EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH[1].replace('MONTH', month))) == False:
            writeToLog("INFO","FAILED to select the month")
            return False
        
        # Set Day
        # We have class of 'old day', 'day' and 'today active day'. The issue is when we have the same day on specific month.
        # The solution is to get_elemets of contains(@class,'day') and NOT click on 'old day'
        if self.clickOnDayFromDatePicker(day) == False:
            writeToLog("INFO","FAILED to select the day")
            return False        
        
        return True
    
    
    # Author: Oleg Sigalov
    # We have class of 'old day', 'day' and 'today active day'. The issue is when we have the same day on specific month.
    # The solution is to get_elemets of contains(@class,'day') and NOT click on 'old day'    
    # Help method for setScheduleDate or setScheduleEndDate
    def clickOnDayFromDatePicker(self, day):
        tmpDayLocator = (self.EDIT_ENTRY_SCHEDULING_CALENDAR_DAY[0], self.EDIT_ENTRY_SCHEDULING_CALENDAR_DAY[1].replace('DAY', day))
        elements = self.wait_elements(tmpDayLocator)
        for el in elements:
            if el.get_attribute("class") != 'old day':
                el.click()
                return True
        return False
    
        
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
        sleep(4)
        
        # Type in a file path
        self.clsCommon.upload.typeIntoFileUploadDialog(captionFilePath)
        
        # Verify caption file was uploaded
        if self.wait_visible(self.EDIT_ENTRY_UPLOAD_CAPTION_SUCCESS_MESSAGE, 30) == False:
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
    def uploadSlidesDeck(self, filePath, mySlidesList, waitToFinish=True):
        sleep(2)
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
        
        sleep(2)  
        if self.click(self.EDIT_ENTRY_CHOOSE_FILE_TO_UPLOAD_BUTTON_IN_TIMELINE, 20) == False:
            writeToLog("INFO","FAILED to click on choose a file to upload button")
            return False            
        
        sleep(2)  
        self.clsCommon.upload.typeIntoFileUploadDialog(filePath)
          
        # verify ptt start processing
        if self.wait_visible(self.EDIT_ENTRY_UPLOAD_DECK_PROCES, 20) == False:
            writeToLog("INFO","FAILED, Can NOT find upload deck processing message")
            return False
        
        if waitToFinish == True: 
            # Wait until the ptt will upload   
            if self.wait_while_not_visible(self.EDIT_ENTRY_UPLOAD_DECK_PROCES, 420) == False:
                writeToLog("INFO","FAILED, upload deck processing isn't done after 7 minutes")
                return False
            sleep(2)
            
            # verify that slide display in timeline
            if self.verifySlidesInTimeLine(mySlidesList) == False:
                writeToLog("INFO","FAILED, Not all slides display in time line")
                return False
            sleep(1)
            # Verify cuepoint were added on the player
            if self.clsCommon.player.verifySlidesInPlayerSideBar(mySlidesList) == False:
            #if len(self.get_elements(self.EDIT_ENTRY_CUEPOINT_ON_TIMELINE)) != totalSlideNum:
                writeToLog("INFO","FAILED, Not all cuepoints were verify")
                return False
             
            writeToLog("INFO","Success presentation was upload and added to time line successfully")
        else:
            sleep(5)
            if self.click(self.EDIT_ENTRY_BACK_TO_TIMELINE, 30) == False:
                writeToLog("INFO","FAILED to click on 'back to timeline' button")
                return False   
             
        return True
      
    # Author: Tzachi Guetta
    def addFlavorsToEntry(self, entryName, flavorsList):
        try:
            if len(entryName) != 0:
                if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                  
                if self.clickOnEditTab(enums.EditEntryPageTabName.DOWNLOADS) == False:
                    writeToLog("INFO","FAILED to navigate to DOWNLOADS tab")
                    return False
                
                if len(flavorsList) != 0:
                    for flavor in flavorsList: 
                        tmoFlavorName = (self.EDIT_ENTRY_DOWNLOADS_FLAVOR[0], self.EDIT_ENTRY_DOWNLOADS_FLAVOR[1].replace('FLAVOR_NAME', flavor))
                        if self.click(tmoFlavorName, 30) == False:
                            writeToLog("INFO","FAILED to click on flavor:" + flavor)
                            return False
                        writeToLog("INFO","Flavor: " + flavor + " added successfully")
                else:   
                    writeToLog("INFO","flavorsList not supplied")
                    return False
                
                sleep(1)
                if self.click(self.EDIT_ENTRY_SAVE_BUTTON_FLAVOR, 30) == False:
                    writeToLog("INFO","FAILED to click on save button ")
                    return False
            
                if self.wait_visible(self.EDIT_ENTRY_SAVE_MASSAGE, 30) == False:
                    writeToLog("INFO","FAILED to find save massage")
                    return False
                sleep(3)
            else:
                writeToLog("INFO","Entry name not supplied")
                return False
            
        except NoSuchElementException:
            return False
          
        return True
    
    
    # Author: Michal Zomper
    def navigateToEntryPageFromEditEntryPage(self, entryName, leavePage=False):
        if self.clickOnEditTab(enums.EditEntryPageTabName.DETAILS) == False:
            writeToLog("INFO","FAILED to click on the details tab")
            return False
        
        if self.click(self.EDIT_ENTRY_SAVE_BUTTON, 15) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        sleep(2)
        if self.click(self.EDIT_ENTRY_GO_TO_MEDIA_BUTTON, 20, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on go to media button")
            return False
        sleep(3)
        
        # Click Leave Page if expected    
        if leavePage == True:
            if self.click_leave_page() == False:
                return False
        
        sleep(3)       
        tmp_entry_name = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        # Wait page load - wait for entry title
        if self.wait_visible(tmp_entry_name, 25) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
        sleep(3)
        writeToLog("INFO","Success, entry page open")
        return True
     
     
    # Author: Michal Zomper   
    def deleteSingelSlideFromTimeLine(self, slideTime):
        slideTimeInSec = utilityTestFunc.convertTimeToSecondsMSS(slideTime)
        sleep(2)
        locatorSlideTime = (self.EDIT_ENTRY_SLIDE_IN_TIMELINE[0], self.EDIT_ENTRY_SLIDE_IN_TIMELINE[1].replace('SLIDE_TIME', str(slideTimeInSec * 1000)))
        if self.click(locatorSlideTime, 20) == False:
            writeToLog("INFO","FAILED to find and click on slide at time : '" + str(slideTime) + "' in time line")
            return False
        sleep(2)
        self.hover_on_element(self.EDIT_ENTRY_DELETE_SLIDE_BUTTON_FORM_TIME_LINE)
        sleep(2)
        if self.click(self.EDIT_ENTRY_DELETE_SLIDE_BUTTON_FORM_TIME_LINE, 20) == False:
            writeToLog("INFO","FAILED to click on delete slide button")
            return False
            
        sleep(3)
        deleteEl = self.driver.find_elements_by_xpath(self.EDIT_ENTRY_CONFIRM_DELETE_BUTTON[1])
        if self.clickElement(deleteEl, True) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False   
        
        sleep(2)
        if self.is_visible(locatorSlideTime) == True:
            writeToLog("INFO","FAILED, slide in time '" + str(slideTime) + "' was found although this slide was deleted")
            return False   
        
        writeToLog("INFO","Success, slide at " + str(slideTime) + " second was delete from time line")
        return True      
    
    
    # Author: Michal Zomper   
    def deleteSlidesFromTimeLine(self, entryName, deleteSlidesList):
        if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED navigate to edit entry page")
            return False
        
        if self.clickOnEditTab(enums.EditEntryPageTabName.TIMELINE) == False:
            writeToLog("INFO","FAILED to click on the time-line tab")
            return False
        
        for slide in deleteSlidesList:
            if self.deleteSingelSlideFromTimeLine(deleteSlidesList[str(slide)][1:]) == False:
                writeToLog("INFO","FAILED to delete slide")
                return False
            
        writeToLog("INFO","Success, all slides were deleted successfully")
        return True
    
    def navigateToEditEntry(self, entryName="", navigateFrom = enums.Location.MY_MEDIA):
            if navigateFrom == enums.Location.MY_MEDIA:
                if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED navigate to edit entry '" + entryName + "' from " + enums.Location.MY_MEDIA.value)
                    return False  
                
            elif navigateFrom == enums.Location.ENTRY_PAGE:
                if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED navigate to edit entry '" + entryName + "' from " + enums.Location.ENTRY_PAGE.value)
                    return False            
            sleep(2)
            return True    
    
    # Author: Michal Zomper 
    def addChapter(self, chapterName, chapterTime):
        if self.click(self.EDIT_ENTRY_ADD_CHAPTER, 20) == False:
            writeToLog("INFO","FAILED to click on add chapter button")
            return False
        
        if self.send_keys(self.EDIT_ENTRY_INSERT_CHAPTER_TITLE, chapterName) == False:
            writeToLog("INFO","FAILED insert chapter name")
            return False
        
        if self.clear_and_send_keys(self.EDIT_ENTRY_INSERT_TIME_TO_SLIDE_OR_CHAPTER, chapterTime) == False:
            writeToLog("INFO","FAILED insert chapter time")
            return False           
            
        if self.click(self.EDIT_ENTRY_SAVE_CHAPTER_OR_SLIDE, 20) == False:
            writeToLog("INFO","FAILED click on save chapter button")
            return False               
        
        sleep(5)
        # Verify chapter saved 
        if self.is_visible(self.EDIT_ENTRY_SAVED_CHAPTER_OR_SLIDE_SUCCESS_MSG) == False:
            writeToLog("INFO","FAILED to fined saved chapter success label")
            return False  
           
        writeToLog("INFO","Success, chapter was created successfully")
        return True  
    
    # Author: Michal Zomper 
    def addChapters(self, entryName, chaptersList):
        if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED navigate to edit entry page")
            return False
        
        if self.clickOnEditTab(enums.EditEntryPageTabName.TIMELINE) == False:
            writeToLog("INFO","FAILED to click on the time-line tab")
            return False
        
        for chapter in chaptersList:
            if self.addChapter(chapter, chaptersList[chapter]) == False:
                writeToLog("INFO","FAILED add chapter name: " + chapter)
                return False
            
        if self.click(self.EDIT_ENTRY_VIEW_IN_PLAYER_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click on 'view in player' button")
            return False
            
        sleep(2)
        writeToLog("INFO","Success, All chapters were created successfully")
        return True  
        
    
    # Author: Michal Zomper 
    def deleteChapter (self, chapterTime):
        chapterTimeInSec = utilityTestFunc.convertTimeToSecondsMSS(chapterTime)
        ChapterTime = (self.EDIT_ENTRY_CHAPTER_IN_TIME_LINE[0], self.EDIT_ENTRY_CHAPTER_IN_TIME_LINE[1].replace('CHAPTER_TIME', str(chapterTimeInSec * 1000)))
        sleep(3)
        if self.click(ChapterTime) == False:
            writeToLog("INFO","FAILED to click on chapter icon in time line")
            return False          
        sleep(2)
        
        if self.click(self.EDIT_ENTRY_DELETE_CHAPTER_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click on delete chapter button")
            return False
        sleep(3)
        
        # Click on confirm delete
        if self.click(self.EDIT_ENTRY_CONFIRM_DELETE_BUTTON, 20, True) == False:
            writeToLog("INFO","FAILED to click on remove caption button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        
        # Verify that the chapter was delete
        if self.is_visible(ChapterTime) == True:
            writeToLog("INFO","FAILED, chapter was found although the chapter was deleted")
            return False
            
        writeToLog("INFO","Success, Chapter was deleted successfully")
        return True  
    
    # Author: Michal Zomper 
    def deletechpaters(self, entryName, chaptersList):
        if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED navigate to edit entry page")
            return False
        
        if self.clickOnEditTab(enums.EditEntryPageTabName.TIMELINE) == False:
            writeToLog("INFO","FAILED to click on the time-line tab")
            return False
        
        for chapter in chaptersList:
            if self.deleteChapter(chaptersList[chapter]) == False:
                writeToLog("INFO","FAILED to delete chapter name: " + chapter)
                return False
            
        if self.click(self.EDIT_ENTRY_VIEW_IN_PLAYER_BUTTON, 20, True) == False:
            writeToLog("INFO","FAILED to click on 'view in player' button")
            return False
            
        sleep(2)
        writeToLog("INFO","Success, All chapters were deleted successfully")
        return True  
        
    # Author: Michal Zomper
    # The function change a single slide time in the time line
    def changeSlideTimeInTimeLine(self, oldSlideTime, newSlideTime):
        slideTimeInSec = utilityTestFunc.convertTimeToSecondsMSS(oldSlideTime)
        locatorSlideTime = (self.EDIT_ENTRY_SLIDE_IN_TIMELINE[0], self.EDIT_ENTRY_SLIDE_IN_TIMELINE[1].replace('SLIDE_TIME', str(slideTimeInSec * 1000)))
        sleep(3)
        if self.click(locatorSlideTime, 20) == False:
            writeToLog("INFO","FAILED to find and click on slide at time : '" + str(oldSlideTime) + "' in time line")
            return False   
        
        sleep(1) 
        if self.clear_and_send_keys(self.EDIT_ENTRY_INSERT_TIME_TO_SLIDE_OR_CHAPTER, newSlideTime, multipleElements= True) == False:
            writeToLog("INFO","FAILED insert new slide time: " + str(newSlideTime))
            return False             
        
        sleep(1)
        if self.click(self.EDIT_ENTRY_SAVE_CHAPTER_OR_SLIDE, 30) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False               
        
        sleep(3)
        # Verify new time saved 
        if self.wait_visible(self.EDIT_ENTRY_SAVED_CHAPTER_OR_SLIDE_SUCCESS_MSG, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to fined saved success label")
            return False  
        
        sleep(1)
        writeToLog("INFO","Success, slide time '" + str(oldSlideTime) + "' was changed to '" + str(newSlideTime) + "' successfully")
        return True  
    
    
    # Author: Michal Zomper
    # The function go over all the the slide list and change the slides time
    def changeSlidesTimeInTimeLine(self, entryName, changeTimeOfSlidesList):
        if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED navigate to edit entry page")
            return False
         
        if self.clickOnEditTab(enums.EditEntryPageTabName.TIMELINE) == False:
            writeToLog("INFO","FAILED to click on the time-line tab")
            return False      
        
        for slide in changeTimeOfSlidesList:
            if self.changeSlideTimeInTimeLine(slide, changeTimeOfSlidesList[slide]) == False:
                writeToLog("INFO","FAILED change slide in time: " + str(slide) + " to time: " + str(changeTimeOfSlidesList[slide]))
                return False
             
        writeToLog("INFO","Success, All slides time was changed successfully")
        return True


    # Author: Tzachi Guetta
    def verifyDisclaimerText(self, entryName, expectedText):
        try:
            if self.navigateToEditEntry(entryName) == False:
                writeToLog("INFO","FAILED to navigate to edit entry page, Entry name: " + entryName)
                return False
            
            if not self.get_element(self.EDIT_ENTRY_DISCLAIMER_TEXT_BOX).text in expectedText:
                writeToLog("INFO","FAILED, the expected text wasn't presented")
                return False
                            
            writeToLog("INFO","Passed, the expected text was presented")
            return True
            
        except:
            writeToLog("INFO","FAILED Disclaimer text wasn't found, Entry name: " + entryName)
            return False
       
    # Author: Michal Zomper
    # The function go over all the the slide in time line and verify that the time is correct   
    def verifySlidesInTimeLine(self, slidesList):
        self.click(self.EDIT_ENTRY_TIMELINE_TAB, 15)
        sleep(2)
        for slide in slidesList:
            slideTimeInSec = utilityTestFunc.convertTimeToSecondsMSS(slidesList[slide])
            locatorSlideTime = (self.EDIT_ENTRY_SLIDE_IN_TIMELINE[0], self.EDIT_ENTRY_SLIDE_IN_TIMELINE[1].replace('SLIDE_TIME', str(slideTimeInSec * 1000)))
            if self.is_visible(locatorSlideTime) == False:
                writeToLog("INFO","FAILED to find slide at time : '" + str(slidesList[slide]) + "' in time line")
                return False
            
            writeToLog("INFO","Success, all slides display in time line")
            return True
            
    
    # Author: Michal Zomper        
    def addNameToslides(self,slidsWithNameList):
        self.click(self.EDIT_ENTRY_TIMELINE_TAB, 15)
        sleep(2)
        for slide in slidsWithNameList:
            slideTimeInSec = utilityTestFunc.convertTimeToSecondsMSS(slidsWithNameList[slide])
            locatorSlideTime = (self.EDIT_ENTRY_SLIDE_IN_TIMELINE[0], self.EDIT_ENTRY_SLIDE_IN_TIMELINE[1].replace('SLIDE_TIME', str(slideTimeInSec * 1000)))
            if self.click(locatorSlideTime, 20) == False:
                writeToLog("INFO","FAILED to find and click on slide at time : '" + str(slidsWithNameList[slide]) + "' in time line")
                return False
            
            sleep(1)
            self.hover_on_element(self.EDIT_ENTRY_INSERT_SLIDE_TITLE)
            if self.send_keys(self.EDIT_ENTRY_INSERT_SLIDE_TITLE, slide) == False:
                writeToLog("INFO","FAILED insert slide name")
                return False
            
            if self.click(self.EDIT_ENTRY_SAVE_CHAPTER_OR_SLIDE, 20) == False:
                writeToLog("INFO","FAILED click on save slide button")
                return False 
            
            sleep(5)
            # Verify chapter saved 
            if self.is_visible(self.EDIT_ENTRY_SAVED_CHAPTER_OR_SLIDE_SUCCESS_MSG, multipleElements=True) == False:
                writeToLog("INFO","FAILED to find saved slide success label")
                return False
              
        writeToLog("INFO","Success, name was added to all needed slides")
        return True
    
    # Author: Michal Zomper     
    def uploadThumbnail(self, filePath, ExpectedQRresult):  
        if self.clickOnEditTab(enums.EditEntryPageTabName.THUMBNAILS) == False:
            writeToLog("INFO","FAILED to click on the thumbnail tab")
            return False
        sleep(2)
        
        if self.click(self.EDIT_ENTRY_UPLOAD_THUMBNAIL_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click on upload thumbnail button")
            return False
        self.clsCommon.upload.typeIntoFileUploadDialog(filePath)
        
        # verify that the upload progress bar disappear
        if self.wait_while_not_visible(self.EDIT_ENTRY_THUMBNAIL_PROGRESS_BAR) == False:
            writeToLog("INFO","FAILED to verify that thumbnail progress bar disappear")
            return False
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
            self.click(self.EDIT_ENTRY_THUMBNAIL_TAB)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
            
        # verify image was add
        if self.wait_visible(self.EDIT_ENTRY_VERIFY_IMAGE_ADDED_TO_THUMBNAIL_AREA, 20) == False:
            writeToLog("INFO","FAILED to verify capture was added to thumbnail area")
            return False
        
        sleep(3)    
        thumbnailResult = self.clsCommon.qrcode.getScreenshotAndResolveImageInThumbnailTabQrCode()
        
        if thumbnailResult != str(ExpectedQRresult):
            writeToLog("INFO","FAILED to verify that the upload thumbnail is correct, expected qr code is '" + str(ExpectedQRresult)+ "' and the upload thumbnail qr code is '" + str(thumbnailResult) + "'")
            return False
        
        writeToLog("INFO","Success, upload thumbnail was successfully")
        return True
    
    
    # Author: Michal Zomper 
    def captureThumbnail(self, timeToStop, qrCodeRedult, playFromBarline=True): 
        if self.clickOnEditTab(enums.EditEntryPageTabName.THUMBNAILS) == False:
            writeToLog("INFO","FAILED to click on the thumbnail tab")
            return False
        sleep(2)
        
        if self.clsCommon.player.clickPlayAndPause(timeToStop, timeout=45, clickPlayFromBarline=playFromBarline) == False:
            writeToLog("INFO","FAILED to stop player at time: " + str(timeToStop))
            return False
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
            if self.clsCommon.blackBoard.switchToBlackboardIframe() == False:
                writeToLog("INFO","FAILED to load blackboard iframe")
                return False
        else:
            self.clsCommon.switch_to_default_iframe_generic()
            
        if self.click(self.EDIT_ENTRY_CAPTURE_THUMBNAIL_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on capture thumbnail button")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        # verify that the capture message display
        self.is_visible(self.EDIT_ENTRY_THUMBNAIL_CAPTURED_MES)
        sleep(5)
        # verify image was add
        if self.wait_visible(self.EDIT_ENTRY_VERIFY_IMAGE_ADDED_TO_THUMBNAIL_AREA, 30) == False:
            writeToLog("INFO","FAILED to verify capture was added to thumbnail area")
            return False
            
        thumbnailResult = self.clsCommon.qrcode.getScreenshotAndResolveImageInThumbnailTabQrCode()
        
        #TODO add tolerance 
        if (int(qrCodeRedult)-1 <= int(thumbnailResult)) and (int(thumbnailResult) < int(qrCodeRedult)+1) == False:
            writeToLog("INFO","FAILED to verify that the capture thumbnail is correct, expected qr code is '" + str(qrCodeRedult)+ "' and the capture thumbnail qr code is '" + str(thumbnailResult) + "'")
            return False
        
        writeToLog("INFO","Success, capture thumbnail was successfully")
        return True       


    # Author: Michal Zomper 
    def chooseAutoGthumbnail(self, chosenThumbnailNumber, ExpectedQRresult):  
        if self.clickOnEditTab(enums.EditEntryPageTabName.THUMBNAILS) == False:
            writeToLog("INFO","FAILED to click on the thumbnail tab")
            return False
        sleep(3)
        
        if self.click(self.EDIT_ENTRY_THUMBNAIL_AUTO_GENERATE_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click on thumbnail auto generate button")
            return False
        
        sleep(10)
        chosenThumbnail = (self.EDIT_ENTRY_CHOOSE_AUTO_GENERATE_THUMBNAIL[0], self.EDIT_ENTRY_CHOOSE_AUTO_GENERATE_THUMBNAIL[1].replace('SLOCE_NUMBER', str(chosenThumbnailNumber)))
        if self.click(chosenThumbnail, timeout=20) == False:
            writeToLog("INFO","FAILED to choose thumbnail number '" + str(chosenThumbnailNumber) + "' from auto generate")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        # verify that the capture message display
        self.is_visible(self.EDIT_ENTRY_THUMBNAIL_CAPTURED_MES)

        # verify image was add
        if self.wait_visible(self.EDIT_ENTRY_VERIFY_IMAGE_ADDED_TO_THUMBNAIL_AREA, 20) == False:
            writeToLog("INFO","FAILED to verify auto generate thumbnail was added to thumbnail area")
            return False
         
        sleep(1)   
        thumbnailResult = self.clsCommon.qrcode.getScreenshotAndResolveImageInThumbnailTabQrCode()
        
        if thumbnailResult != str(ExpectedQRresult):
            writeToLog("INFO","FAILED to verify that the thumbnail that was choden from auto generate is correct, expected qr code is '" + str(ExpectedQRresult)+ "' and the auto generate thumbnail qr code is '" + str(thumbnailResult) + "'")
            return False
        
        writeToLog("INFO","Success, capture thumbnail was successfully")
        return True               
        
        
    # @ Author: Inbar Willmna
    # Replace entry's video
    def replaceVideo(self, filePath,timeout=15):
        #Choose replace video option
        if self.clickOnEditTab(enums.EditEntryPageTabName.REPLACE_VIDEO) == False:
            writeToLog("INFO","FAILED to click on replace video tab")
            return True               
        
        #Click on Choose a file to upload
        if self.click(self.EDIT_ENTRY_UPLOAD_NEW_FILE) == False:
            writeToLog("INFO","FAILED to click on 'Choose a file to upload' button")
            return False 

        sleep(3)
        # Type in a file path
        if self.clsCommon.upload.typeIntoFileUploadDialog(filePath) == False:
            writeToLog("INFO","FAILED to choose file")
            return False        
        
        # Wait for success message "Upload Completed"
        startTime = datetime.datetime.now().replace(microsecond=0)
        if self.clsCommon.upload.waitUploadCompleted(startTime, timeout) == False:
            writeToLog("INFO","FAILED to displayed 'Upload complete' message")
            return False                
        
        #Click on approve replacement button
        if self.click(self.EDIT_ENTRY_APPROVE_REPLACMENT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'approve replacement' button")
            return False
        
        # wait until 'Your media was successfully replaced.' message is displayed
        if self.wait_visible(self.EDIT_ENTRY_MEDIA_SUCCESSFULLY_REPLACED_MSG, timeout= 110) == False:
            writeToLog("INFO","FAILED to display 'Your media was successfully replaced.' message")
            return False
        
        return True    
    
    
    # @Author: Inbar Willman
    def addAttachments(self, filePath, attachmentName, attachmentsTitle, attachmentsDescription):    
        # Choose attachments tab
        if self.clickOnEditTab(enums.EditEntryPageTabName.ATTACHMENTS) == False:
            writeToLog("INFO","FAILED to click on attachments tab")
            return False   
        
        # wait for loading to disappeared
        self.clsCommon.general.waitForLoaderToDisappear()       
        
        # Upload attachment file
        if self.uploadAttachment(filePath) == False:
            writeToLog("INFO","FAILED to upload attachment file")
            return False              
       
        #Insert attachment fields and save information
        if self.insertAttachmentFields(attachmentsTitle, attachmentsDescription) == False:
            writeToLog("INFO","FAILED to insert attachment fields - title and description")
            return False      
        
        # wait for loading to disappeared
        self.clsCommon.general.waitForLoaderToDisappear()              
        
        #Verify that attachment fields are displayed
        if self.verifyAttachmentFields(attachmentName, attachmentsTitle, attachmentsDescription) == False:
            writeToLog("INFO","FAILED to displayed correct attachment field")
            return False              
    
        return True
    
    
    # @Author: Inbar Willman
    #Upload file in attachment tab
    def uploadAttachment(self, filePath):
        # Click on Upload file
        if self.click(self.EDIT_ENTRY_ATTACHMENTS_UPLOAD_FILE) == False:
            writeToLog("INFO","FAILED to click on upload file button")
            return False 
        
        sleep(3)
        
        # Click on select file
        if self.click(self.EDIT_ENTRY_ATTACHMENTS_SELECT_FILE) == False:
            writeToLog("INFO","FAILED to click select file button")
            return False                  
        
        # Type in a file path
        if self.clsCommon.upload.typeIntoFileUploadDialog(filePath) == False:
            writeToLog("INFO","FAILED to choose file")
            return False  
        
        # Wait for file to upload
        if self.wait_visible(self.EDIT_ENTRY_UPLOAD_ATTACHMENT_COMPLETED_SUCCESS_MSG,timeout=30) == False:
            writeToLog("INFO","FAILED to complete upload")
            return False  
        
        return True
        
    
    # @Author: Inbar Willman
    # Insert attachment title and description
    def insertAttachmentFields(self, attachmentsTitle, attachmentsDescription, isNewAttachment=True):
        #If uploading new attachment file
        if isNewAttachment == True:
            # Click on title field
            if self.click(self.EDIT_ENTRY_UPLOAD_ATTACHMENTS_TITLE) == False:
                writeToLog("INFO","FAILED to click on title field")
                return False  
        
        else:    
            # Wait to modal to be displayed
            if self.wait_visible(self.EDIT_ENTRY_EDIT_ATTACHMENT_MODAL_BODY) == False:
                writeToLog("INFO","FAILED to displayed edit attachments modal")
                return False 
        
        sleep(2)                     
            
        # Click on title field
        if self.click(self.EDIT_ENTRY_UPLOAD_ATTACHMENTS_TITLE) == False:
            writeToLog("INFO","FAILED to click on description field")
            return False              

        # Insert content to field
        if self.clear_and_send_keys(self.EDIT_ENTRY_UPLOAD_ATTACHMENTS_TITLE, attachmentsTitle) == False:
            writeToLog("INFO","FAILED to insert title")
            return False 
             
        # Click on description field
        if self.click(self.EDIT_ENTRY_UPLOAD_ATTACHMENTS_DESCRIPTION) == False:
            writeToLog("INFO","FAILED to click on description field")
            return False        
        
        # Insert content to field
        if self.clear_and_send_keys(self.EDIT_ENTRY_UPLOAD_ATTACHMENTS_DESCRIPTION, attachmentsDescription) == False:
            writeToLog("INFO","FAILED to insert description")
            return False              
        
        # Save fields
        if self.click(self.EDIT_ENTRY_UPLOAD_ATTACHMENTS_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click save button")
            return False
        
        # Check that success message is displayed
        if self.wait_visible(self.EDIT_ENTRY_UPLOAD_ATTACHMENT_SUCCESS_MSG) == False:
            writeToLog("INFO","FAILED to displayed success message")
            return False
        
        return True
    
    
    # @Author: Inbar WIllman
    # Check that correct attachment fields are displayed
    def verifyAttachmentFields(self, attachmentName, attachmentsTitle, attachmentsDescription):
        # Check that correct fields are displayed - Name, Title and description
        tmp_name = (self.EDIT_ENTRY_UPLOADED_ATTACHMENT_FIELDS[0], self.EDIT_ENTRY_UPLOADED_ATTACHMENT_FIELDS[1].replace('ENTRY_FIELD', attachmentName))
        tmp_title = (self.EDIT_ENTRY_UPLOADED_ATTACHMENT_FIELDS[0], self.EDIT_ENTRY_UPLOADED_ATTACHMENT_FIELDS[1].replace('ENTRY_FIELD', attachmentsTitle))
        tmp_descrition = (self.EDIT_ENTRY_UPLOADED_ATTACHMENT_FIELDS[0], self.EDIT_ENTRY_UPLOADED_ATTACHMENT_FIELDS[1].replace('ENTRY_FIELD', attachmentsDescription))
        
        # Check that success message is displayed
        if self.wait_visible(self.EDIT_ENTRY_UPLOAD_SUCCESS_MSG) == False:
            writeToLog("INFO","FAILED to success message")
            return False             
        
        # Check that correct file name is displayed
        if self.is_visible(tmp_name) == False:
            writeToLog("INFO","FAILED to displayed correct name: " + attachmentName)
            return False 
        
        # Check that correct file title is displayed
        if self.is_visible(tmp_title) == False:
            writeToLog("INFO","FAILED to displayed correct title: " + attachmentsTitle)
            return False 
        
        # Check that correct file description is displayed
        if self.is_visible(tmp_descrition) == False:
            writeToLog("INFO","FAILED to displayed correct description: " + attachmentsDescription)
            return False       
        
        return True   
    
    
    # @Author: Inbar Willman
    # Edit attachment title and description
    def editAttachmentFields(self, attachmentName, newAttachmentsTitle, newAttachmentsDescription, isNewAttachment=False): 
        # Scroll down in page
        self.clsCommon.sendKeysToBodyElement(Keys.END) 
        
        sleep(2)   
        
        # Hover over edit icon
        if self.hover_on_element(self.EDIT_ENTRY_EDIT_ATTACHMENT_ICON) == False:
            writeToLog("INFO","FAILED to hover over attachment icon")
            return False  
        
        #Click on edit icon   
        if self.click(self.EDIT_ENTRY_EDIT_ATTACHMENT_ICON) == False:
            writeToLog("INFO","FAILED to click on edit attachment icon")
            return False       
       
        #Insert attachment fields and save inforamtion
        if self.insertAttachmentFields(newAttachmentsTitle, newAttachmentsDescription,isNewAttachment) == False:
            writeToLog("INFO","FAILED to insert attachment fields - title and description")
            return False   
        
        # wait for loading to disappeared
        self.clsCommon.general.waitForLoaderToDisappear()                          
        
        #Verify that attachment fields are displayed
        if self.verifyAttachmentFields(attachmentName, newAttachmentsTitle, newAttachmentsDescription) == False:
            writeToLog("INFO","FAILED to displayed correct attachment field")
            return False              
    
        return True      
    
    
    # @Author: Inbar Willman 
    # Download attachment file
    def downloadAttachmentFileFromEditPage(self, originalPath, downloadPath):     
        # Scroll down in page
        self.clsCommon.sendKeysToBodyElement(Keys.END)  
        
        sleep(2) 
        
        # Hover over download icon
        if self.hover_on_element(self.EDIT_ENTRY_DOWNLOAD_ATTACHMENT_ICON) == False:
            writeToLog("INFO","FAILED to hover over download attachment icon")
            return False             
        
        #Click on download icon   
        if self.click(self.EDIT_ENTRY_DOWNLOAD_ATTACHMENT_ICON) == False:
            writeToLog("INFO","FAILED to click on download attachment icon")
            return False   
        
        # Compare between uploaded file and download file
        writeToLog("INFO","Going to compare between uploaded file and download file")  
        if self.clsCommon.compareBetweenTwoFilesBinary(originalPath, downloadPath) == False:
            writeToLog("INFO","FAILED to click on to download file correctly")
            return False              
          
        return True
    
    
    # @Author: Inbar Willman 
    # remove attachment file
    def removeAttachmentFile(self):        
        # Choose attachments tab
        if self.clickOnEditTab(enums.EditEntryPageTabName.ATTACHMENTS) == False:
            writeToLog("INFO","FAILED to click on attachments tab")
            return False 
        
        # wait for loading to disappeared
        self.clsCommon.general.waitForLoaderToDisappear()  
        
        # Scroll down in page
        self.clsCommon.sendKeysToBodyElement(Keys.END) 
        
        sleep(2)
                   
        # Hover over remove icon
        if self.hover_on_element(self.EDIT_ENTRY_REMOVE_ATTACHMENT_ICON) == False:
            writeToLog("INFO","FAILED to hover over download attachment icon")
            return False             
        
        # Click on remove icon   
        if self.click(self.EDIT_ENTRY_REMOVE_ATTACHMENT_ICON) == False:
            writeToLog("INFO","FAILED to click on download attachment icon")
            return False 
        
        sleep(2)
          
        # Click on delete in delete confirmation modal
        if self.click(self.EDIT_ENTRY_DELETE_CONFIRMATION_BTN) == False:
            writeToLog("INFO","FAILED to click on delete confirmation button")
            return False 
        
        # Wait until confirmation delete message is displayed
        if self.wait_visible(self.EDIT_ENTRY_DELETE_CONFIRMATION_MSG) == False:
            writeToLog("INFO","FAILED to displayed delete success message")
            return False   
        
        # Check that 'No attachments' message is displayed
        if self.is_visible(self.EDIT_ENTRY_NO_ATTACHMENT_MSG) == False:
            writeToLog("INFO","FAILED to displayed 'No attachments' message")
            return False                         
        
        return True
    
    
    # @Author: Michal Zomper
    def deleteEnteyFromEditEntryPage(self):
        if self.click(self.EDIT_ENTRY_DELETE_ENTRY_BUTTON, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on delete button")
            return False
        sleep(2)
        
        # Click on confirm delete
        if self.click(self.clsCommon.myMedia.MY_MEDIA_CONFIRM_ENTRY_DELETE, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        
        writeToLog("INFO","Entry Was Deleted")
        return True
                
                
    # @Author: Inbar Willman
    # Set custom data fields
    # Field input can be single value or list in case filling unlimited text field
    def setCustomDataField(self, fieldName, fieldInput="", fieldBtn ="", fieldType = enums.CustomdataType.TEXT_SINGLE, year=None, month=None, day=None):
        # Set element
        tmp_field = (self.EDIT_ENTRY_CUSTOM_DATA_TEXT_FIELD[0], self.EDIT_ENTRY_CUSTOM_DATA_TEXT_FIELD[1].replace('FIELD_NAME', fieldName))
        
        # If field is single text field
        if fieldType == enums.CustomdataType.TEXT_SINGLE:
            if self.send_keys(tmp_field, fieldInput) == False:
                writeToLog("INFO","FAILED to fill single text customdata field")
                return False                
        
        # If field is unlimited text field
        elif fieldType == enums.CustomdataType.TEXT_UNLIMITED:
            for idx, text in enumerate(fieldInput):
                # Get field elements list - After clicking add button there are more than one elements (the new field)
                tmp_list = self.get_elements(tmp_field)
                
                # Send input
                tmp_list[idx].send_keys(text)

                # Click on add button
                tmp_add_btn = (self.EDIT_ENTRY_ADD_UNLIMITED_TEXT_CUSTOMDATA_FIELD[0], self.EDIT_ENTRY_ADD_UNLIMITED_TEXT_CUSTOMDATA_FIELD[1].replace('FIELD_NAME', fieldBtn))
                if self.click(tmp_add_btn) == False:
                    writeToLog("INFO","FAILED to add new field box to text unlimited field")
                    return False                     
      
        elif fieldType == enums.CustomdataType.LIST:
            tmp_field = (self.EDIT_ENTRY_CUSTOM_LIST_FIELD[0], self.EDIT_ENTRY_CUSTOM_LIST_FIELD[1].replace('FIELD_NAME', fieldName))
            self.select_from_combo_by_value(tmp_field, fieldInput)
        
        elif fieldType == enums.CustomdataType.DATE:
            if self.setCustomDate(fieldName, year, month, day) == False:
                writeToLog("INFO", "Failed to select a custom date")
                return False

        # Save changes
        if self.click(self.EDIT_ENTRY_SAVE_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on save button ")
            return False
        
        if self.wait_visible(self.EDIT_ENTRY_SAVE_MASSAGE, 30) == False:
            writeToLog("INFO","FAILED to find save massage")
            return False
        
        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "Failed to save the changes")
            return False
        sleep(1)
        
        writeToLog("INFO","Success customdata were change successfully")
        return True
    
    
    # @Author: Horia Cus
    # This function opens the custom date calendar and selects a specific year,month and day
    def setCustomDate(self, fieldName, year, month, day):
        tmp_field = (self.EDIT_ENTRY_CUSTOM_DATE[0], self.EDIT_ENTRY_CUSTOM_DATE[1].replace('FIELD_NAME', fieldName))
        if self.click(tmp_field) == False:
            writeToLog("INFO", "FAILED to select the custom date field")
            return False
        
        if self.click(self.EDIT_ENTRY_CUSTOM_DATEPICKER_SWITCH, multipleElements=True) == False:
            writeToLog("INFO", "Failed to enter in the months calendar")
            return False
        
        if self.click(self.EDIT_ENTRY_CUSTOM_DATEPICKER_SWITCH, multipleElements=True) == False:
            writeToLog("INFO", "Failed to enter in the years calendar")
            return False
        
        tmp_field = (self.EDIT_ENTRY_CUSTOM_DATE_INTERVAL_YEAR_OR_DATE[0], self.EDIT_ENTRY_CUSTOM_DATE_INTERVAL_YEAR_OR_DATE[1].replace('YEAR_or_DATE', year))       
        if self.click(tmp_field) == False:
            writeToLog("INFO", "Failed to select a year from the calendar")
            return False
        
        tmp_field = (self.EDIT_ENTRY_CUSTOM_DATE_INTERVAL_YEAR_OR_DATE[0], self.EDIT_ENTRY_CUSTOM_DATE_INTERVAL_YEAR_OR_DATE[1].replace('YEAR_or_DATE', month))      
        if self.click(tmp_field) == False:
            writeToLog("INFO", "Failed to select a month from the calendar")
            return False 
               
        if self.clickOnDayFromDatePicker(day) == False:
            writeToLog("INFO", "Failed to select a day from the calendar")
            return False      
        
        return True
    

    # Author: Horia Cus
    # This function enters in collaboration tab and changes the media owner to a new one 
    def changeMediaOwner(self, newMediaOwner):
        if self.clickOnEditTab(enums.EditEntryPageTabName.COLLABORATION) == False:
            writeToLog("INFO","FAILED to click on collaboration tab")
            return False    
        
        sleep(1)
        if self.click(self.EDIT_ENTRY_CHANGE_MEDIA_OWNER, 30) == False:
            writeToLog("INFO","FAILED to click on add collaborator button")
            return False    
           
        sleep(2)
        if self.wait_element(self.EDIT_ENTRY_CHANGE_MEDIA_OWNER_POP_UP_TITLE, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to trigger the change media owner pop up")
            return False
        
        if self.send_keys(self.clsCommon.channel.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, newMediaOwner) == False:
            writeToLog("INFO","FAILED to insert the " + newMediaOwner + " user within the field box")
            return False
        
        sleep(3)
        if self.send_keys(self.clsCommon.channel.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, Keys.RETURN) == False:
            writeToLog("INFO","FAILED to press Enter after " + newMediaOwner + " was typed")
            return False  
 
        sleep(1)                
        if self.click(self.EDIT_ENTRY_CHANGE_MEDIA_OWNER_SAVE_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False

        if self.wait_while_not_visible(self.EDIT_ENTRY_CHANGE_MEDIA_OWNER_POP_UP_TITLE, 30) == False:
            writeToLog("INFO","FAILED to save the changes")
            return False 
        
        return True
        