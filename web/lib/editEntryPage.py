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
    EDIT_ENTRY_SAVE_MASSAGE                                     = ('xpath', "//div[@class='alert alert-success ']")
    EDIT_ENTRY_OPTION_TAB                                       = ('id', 'options-tab')
    EDIT_ENTRY_THUMBNAIL_TAB                                    = ('id', 'thumbnails-tab-tab')
    EDIT_ENTRY_CAPTION_TAB                                      = ('id', 'captions-tab-tab')
    EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX                        = ('id', 'EntryOptions-commentsMulti-commentsDisabled')
    EDIT_ENTRY_ENABLE_SCHEDULING_RADIO                          = ('xpath', "//label[@class='schedulerRadioLabel radio' and contains(text(), 'Specific Time Frame')]")
    EDIT_ENTRY_SAVE_MASSAGE                                     = ('xpath' , "//div[@class='alert alert-success ']")
    EDIT_ENTRY_SCHEDULING_START_TIME_CALENDAR                   = ('xpath' , "//input[@aria-label='Start Time Time']")
    EDIT_ENTRY_SCHEDULING_START_DATE_CALENDAR                   = ('xpath' , "//input[@aria-label='Start Time Date']")
    EDIT_ENTRY_SCHEDULING_END_DATE_CALENDAR                   = ('xpath' , "//input[@aria-label='End Time Date']")
    EDIT_ENTRY_SCHEDULING_CALENDAR_TOP                          = ('xpath' , "//th[@class='datepicker-switch' and @colspan='5']")
    EDIT_ENTRY_SCHEDULING_CALENDAR_YEAR                         = ('xpath' , "//span[contains(@class,'year') and text()='YEAR']")# When using this locator, replace 'YEAR' string with your real year
    EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH                        = ('xpath' , "//span[contains(@class,'month') and text()='MONTH']")# When using this locator, replace 'MONTH' string with your real month
    EDIT_ENTRY_SCHEDULING_CALENDAR_DAY                          = ('xpath' , "//td[contains(@class,'day') and text()='DAY']")# When using this locator, replace 'DAY' string with your real day
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
    

#     TODO: add calendar support 
#     TODO: add support for end time field
    def addPublishingSchedule(self, startDate='', startTime='', endDate='', endTime='', timeZone='', entryName=''):
        try:
            if len(entryName) != 0:
                if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False   
                
            if self.click(self.EDIT_ENTRY_ENABLE_SCHEDULING_RADIO) == False:
                writeToLog("INFO","FAILED to click on 'Specific Time Frame' radiobox")
                return False
              
            if len(startTime) != 0:
                self.clear_and_send_keys(self.EDIT_ENTRY_SCHEDULING_START_TIME_CALENDAR, startTime) 
            # else = use the default value
              
            if self.click(self.EDIT_ENTRY_SAVE_BUTTON, 30) == False:
                writeToLog("INFO","FAILED to click on save button ")
                return False
        
            self.clsCommon.general.waitForLoaderToDisappear()
                    
            if self.wait_visible(self.EDIT_ENTRY_SAVE_MASSAGE, 30) == False:
                writeToLog("INFO","FAILED to find save massage")
                return False   
          
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
        # TODO ELSE!  Unknown tabName   
        return True
    
# TODO
#     def changeEntryOptions(self, isDisable):
#         if self.clickOnEditTab(enums.EditEntryPageTabName.OPTIONS) == False:
#             writeToLog("INFO","FAILED to click on options tab")
#             return False
#         
#         # check Disable comments option
#         if self.click(self.EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX, 30) == False:
#             writeToLog("INFO","FAILED to check 'Disable comments' option")
#             return False
#                     
#         if self.wait_visible(self.EDIT_ENTRY_SAVE_MASSAGE, 30) == False:
#             writeToLog("INFO","FAILED to find save massage")
#             return False
#         sleep(3)
#         
#         
#         
#         el = self.driver.find_element_by_id(self.EDIT_ENTRY_DISABLE_COMMENTS_CHECKBOX[1])
#         if  el.get_attribute("checked") != True:
#             writeToLog("INFO","FAILED to")
#             return False
#         
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
        