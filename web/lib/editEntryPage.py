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
    EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX                        = ('id', 'EntryOptions-commentsMulti-commentsDisabled')
    EDIT_ENTRY_ENABLE_SCHEDULING_RADIO                          = ('xpath', "//label[@class='schedulerRadioLabel radio' and contains(text(), 'Specific Time Frame')]")
    EDIT_ENTRY_SAVE_MASSAGE                                     = ('xpath' ,"//div[@class='alert alert-success ']")
    EDIT_ENTRY_CLOSED_COMMENTS_CHECKBOX                         = ('id', 'EntryOptions-commentsMulti-discussionClosed')
    EDIT_ENTRY_CLIP_PERMISSION_EVERYONE_CHECKBOX                = ('id', 'EntryOptions-ClipPermission-everyone')
    EDIT_ENTRY_GO_TO_MEDIA_BUTTON                               = ('xpath', "//a[@class='btn btn-link' and contains(text(), 'Go To Media')]")
    EDIT_ENTRY_3_DOTS_ON_ENTRY_THUMBNAIL                        = ('xpath', "//a[@title='...']")
    EDIT_ENTRY_THUMBNAIL_EDIT_ENTRY_BUTTON                      = ('xpath', "//i[@class='icon-pencil']")

    
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
        if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to navigate to edit entry page")
            return False    
        
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
        # TODO ELSE!  Unknown tabName   
        return True
    
# TODO
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
        
#     def addPublishingSchedule(self, starDate, startTime, endDate='', endTime='', timeZone=''):
#         try:
#             if self.click(self.EDIT_ENTRY_ENABLE_SCHEDULING_RADIO) == False:
#                 writeToLog("INFO","FAILED to click on 'Specific Time Frame' radiobox")
#                 return False
#              
#             if len(startTimeDate) != 0:
#              
#          
#         except NoSuchElementException:
#             return False
#          
#         return True



    # TODO  
#     def navigateToEditEntryPageFromCategoryPage(self, categoryName, entryName): 
#         if self.clsCommon.Category.navigateToCategory(categoryName) == False:
#             writeToLog("INFO","FAILED to navigate to category: " + categoryName)
#             return False            
#         
        