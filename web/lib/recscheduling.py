from selenium.webdriver.common.action_chains import ActionChains
 
 
from base import *
import clsTestService
import enums
from selenium.webdriver.common.keys import Keys
from general import General


# title - Event Title. this parameter is mandatory! 
# startDate - Event start date. this parameter is mandatory! 
# endDate - Event end date. this parameter is mandatory! 
# startTime - Event start time. this parameter is mandatory! 
# endTime - Event end time. this parameter is mandatory!
# description - Event description. this parameter is mandatory! 
# tags - Event tags. this parameter is mandatory! 
# expectedEvent - this parameter will show if the event need to be display in the calender or not(True/False), we will need this when we have recurrence. this parameter is mandatory!  
# copyDetailsEventToRecording - do we need to copy the metadata to the recording, if no (need new names) we need to initialize the parameters :copeDetailsName, copeDetailsDescriptio, copeDetailsTags
# resources - this parameter need to be send as an enum- RecschedulingResourceOptions
# recurrenceInterval - this parameter need to be send as an enum- scheduleRecurrenceInterval
# isRecurrence - if this parameter is True you need to initialize the needed parameters below
# dailyOption - this parameter need to be send as an enum- scheduleRecurrenceDailyOption
# dailyDays - if in daily 'every X days' option was chosen this parameter will go the number of days
# weeklyWeeks - if weekly was chosen this parameter will go the number of weeks
# weeklyDaysNames - if weekly was chosen this parameter will have the day or days that the event need to recurrence, this parameter need to be send as an enum- scheduleRecurrenceDayOfTheWeek, take the day that have SHORT' in it like SUNDAY_SHORT
# monthlyOption - this parameter need to be send as an enum- scheduleRecurrenceMonthlyOption
# monthlyDayNumber - this parameter is for the number of day in monthly first option
# monthlyMonthNumber - this parameter is for the number of month in monthly first option
# monthlyWeekdaysIndex - this parameter is for the day index ,the first parameter of monthly second option, this parameter need to be send as an enum- scheduleRecurrenceMonthlyIndex
# monthlyDayName - this parameter is for the day name that in the second monthly option ,this parameter need to be send as an enum- scheduleRecurrenceDayOfTheWeek, take the day without  the 'SHORT' in it like SUNDAY
# optionTwoMonthlyMonthNumber - this parameter is for the number of month in monthly second option
# endDateOption - this parameter need to be send as enum: scheduleRecurrenceEndDateOption
# numberOfRecurrence - this parameter is for end date option 'end after X occurrences' in recurrence
# publishTo - this parameter is so we can know where to publish the event to category or channel. if we need to publish both category/channel the parameter need to be a list: ["category", "channel"]
# categoryList - this parameter will have the name of the category to publish to , if we have more then 1 category need to be in a list ([]) format
# channelList = this parameter will have the name of the channel to publish to , if we have more then 1 channel need to be in a list ([]) format
# verifyDateFormat - this parameter is created in the Constructor. it will build a date format to us in my schedule page
# fieldsToUpdate - this parameter will have the fields name that need to be update in edit tests, need to be in a list ([]) format.   
#                  if the event is recurrence and we need to update so of the recurrence fields we don't need to write the fields to update since it will go over all the recurrence fields and rewrite them  
#                  we just need to update the needed fields with the new parameters before calling the edit function.
#                  if the event that we need to update is a single event all the needed parameters need to be in the list
# collaboratorUser - this parameter will have the the user id for collaborator 
# coEditor  - this parameter is to know if collaborator user need to be co editor. this is a boolean parameter so needed to be only True/False 
# coPublisher - this parameter is to know if collaborator user need to be co publisher. this is a boolean parameter so needed to be only True/False 
# coViewer - this parameter is to know if collaborator user need to be co publisher. this is a boolean parameter so needed to be only True/False, Default for this is false
class SechdeuleEvent():
    title = None
    startDate = None
    endDate = None
    startTime = None
    endTime = None
    description = None
    tags = None
    expectedEvent = ''
    copyDetailsEventToRecording = True
    copeDetailsName=''
    copeDetailsDescriptio=''
    copeDetailsTags=''
    resources=''
    organizer=''
    isRecurrence=False
    exitEvent= True
    recurrenceInterval=''
    dailyOption=''
    dailyDays=''
    weeklyDays=''
    weeklyDaysNames=''
    monthlyOption=''
    monthlyDayNumber=''
    monthlyMonthNumber=''
    monthlyWeekdaysIndex=''
    monthlyDayName=''
    optionTwoMonthlyMonthNumber=''
    endDateOption = ''
    numberOfRecurrence=''
    publishTo = ''
    categoryList = ''
    channelList = ''
    verifyDateFormat = ''
    fieldsToUpdate = ''
    eventRecurrencefieldsToUpdate = ''
    collaboratorUser = ''
    coEditor = ''
    coPublisher = ''
    coViewer = False
    
    
    # Constructor
    def __init__(self, title, startDate, endDate, startTime, endTime, description, tags, expectedEvent, organizer=""):
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.startTime = self.removeZeroFromTime(startTime)
        self.endTime = self.removeZeroFromTime(endTime)
        self.description = description
        self.tags = tags
        self.expectedEvent = expectedEvent
        if organizer == "":
            self.organizer = localSettings.LOCAL_SETTINGS_LOGIN_USERNAME
        else:
            self.organizer = organizer
        self.convertDatetimeToVerifyDate()
    
    def convertDatetimeToVerifyDate(self):
        dateTimeObj = datetime.datetime.strptime(self.startDate, "%d/%m/%Y")
        tmpStrDate = ''
        # Get Month nmae
        tmpStrDate = dateTimeObj.strftime("%B")
        #Append day
        day =  dateTimeObj.strftime("%d")
        # Convert to int and back to string, to remove 0 before a digit. For example from '03' to '3'
        day = int(day)
        day = str(day)     
        tmpStrDate = tmpStrDate + " " + day
        tmpStrDate = tmpStrDate + ", " + dateTimeObj.strftime("%Y")
        tmpStrDate = tmpStrDate + " - " + dateTimeObj.strftime("%A")
        self.verifyDateFormat = tmpStrDate
        
    # Convert to int and back to string, to remove 0 before a digit. For example from '03' to '3
    def removeZeroFromTime(self, eventTime):
        tmpTime = eventTime.split(":")
        tmpHour = int(tmpTime[0])
        tmpHour = str(tmpHour)
        return tmpHour + ":" + tmpTime[1]
    
    
class  Recscheduling(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #================================
    #=============================================================================================================
    #General locators: 
    #=============================================================================================================
    SCHEDULE_PAGE_TITLE                                                     = ('xpath', "//h1[@class='inline' and text()='My Schedule']")
    USER_MENU_MY_SCHEDULE_BUTTON                                            = ('xpath', "//a[@role='menuitem' and text()='My Schedule']")
    SCHEDULE_CREATE_EVENT_BUTTON                                            = ('xpath', "//a[@id='create-event-btn']")
    SCHEDULE_CREATE_EVENT_PAGE_TITLE                                        = ('xpath', "//h1[@class='inline' and contains(text(),'Create Event')]")
    SCHEDULE_EVENT_TITLE                                                    = ('xpath', "//input[@id='CreateEvent-eventTitle' or @value='EVENT_TITLE']") 
    SCHEDULE_EVENT_ORGANIZER                                                = ('xpath', "//input[@id='CreateEvent-eventOrganizer']")
    SCHEDULE_EVENT_START_TIME                                               = ('xpath', "//input[@id='rsStartTime-rsStartTime_time']")
    SCHEDULE_EVENT_END_TIME                                                 = ('xpath', "//input[@id='rsEndTime-rsEndTime_time']")
    SCHEDULE_EVENT_DESCRIPTION                                              = ('xpath', "//textarea[@id='CreateEvent-eventDescription']")
    SCHEDULE_EVENT_INPUT_TAGS                                               = ('xpath', "//input[contains(@id,'s2id_autogen') and contains(@class, '-input')]")
    SCHEDULE_EVENT_TAGS                                                     = ('xpath', "//div[@id='s2id_CreateEvent-tags']")
    SCHEDULE_SAVE_EVENT                                                     = ('xpath', "//button[@id='CreateEvent-btnSave' and contains(text(),'Save')]")
    SCHEDULE_SAVE_AND_EXIT_EVENT                                            = ('xpath', "//button[@id='CreateEvent-btnCreateEvent' and contains(text(),'Save and Exit')]")
    SCHEDULE_CREATE_EVENT_SUCCESS_MESSAGE                                   = ('xpath', "//p[contains(text(),'Event created successfully.')]")
    SCHEDULE_EVENT_RESOURCES                                                = ('xpath', "//input[@placeholder='Click here to search resource']")
    SCHEDULE_EVENT_RESOURCE                                                 = ('xpath', "//div[@class='sol-label-text' and contains(text(),'RESOURCE_NAME')]")
    SCHEDULE_COPE_DETAILS_BUTTON                                            = ('xpath', "//input[@id='CreateEvent-eventCopyDetails']")
    SCHEDULE_COPE_DETAILS_NAME                                              = ('xpath', "//input[@id='Entry-name']")
    SCHEDULE_COPE_DETAILS_DESCRIPTION                                       = ('xpath', "//textarea[@id='description']")
    SCHEDULE_ADD_RECURRENCE_BUTTON                                          = ('xpath', "//button[@id='CreateEvent-recurrenceMain']")
    SCHEDULE_RECURRENCE_INTERVAL                                            = ('xpath', "//label[@class='radio' and @for='EventRecurrence-recurrence-RECURRENCE_INTERVAL']")
    SCHEDULE_RECURRENCE_START_TIME                                          = ('xpath', "//input[@id='EventRecurrence-startTime']")
    SCHEDULE_RECURRENCE_END_TIME                                            = ('xpath', "//input[@id='EventRecurrence-endTime']")
    SCHEDULE_RECURRENCE_START_DATE_CALENDAR                                 = ('xpath', "//input[@id='EventRecurrence-start']")
    SCHEDULE_RECURRENCE_END_DATE_CALENDAR                                   = ('xpath', "//input[@id='EventRecurrence-endby_date']")
    SCHEDULE_RECURRENCE_END_DATE_REDIO_BUTTON                               = ('xpath', "//label[@class='radio' and @for='EventRecurrence-end_main-END_DTAR_OPTION']")
    SCHEDULE_RECURRENCE_END_DATE_AFTER_X_OCCURRENCES                        = ('xpath', "//input[@id='EventRecurrence-endafter_occurrences']")
    SCHEDULE_RECURRENCE_DAILY_EVERY_X_DAYS_RADIO_BUTTON                     = ('xpath', "//input[@id='EventRecurrence-daily_main-byDay']") # this locator is to choose the 'every X days' in daily option
    SCHEDULE_RECURRENCE_DAILY_EVERY_X_DAYS                                  = ('xpath', "//input[@id='EventRecurrence-daily_days']") # this locator is to enter the number of how many days in daily option
    SCHEDULE_RECURRENCE_DAILY_WEEKDAY_RADIO_BUTTON                          = ('xpath', "//input[@id='EventRecurrence-daily_main-byWeekday']")
    SCHEDULE_RECURRENCE_WEEKLY_EVERY_X_WEEKS                                = ('xpath', "//input[@id='EventRecurrence-weekly_index']") # this locator is to enter the number of how many weeks in weekly option
    SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK                              = ('xpath', "//input[@id='EventRecurrence-weekly_days-DAY_OF_THE_WEEK']") # this locator is for weekly option to choose the day of the week
    SCHEDULE_RECURRENCE_MONTHLY_DAY_X_OF_EVERY_Y_MONTHS_RADIO_BUTTON        = ('xpath', "//input[@id='EventRecurrence-monthly_main-byDay']") # this locator is for monthly option, this is the option 'Day X of every Y months'
    SCHEDULE_RECURRENCE_MONTHLY_BY_DAY_OPTION_DAY_NUMBER                    = ('xpath', "//input[@id='EventRecurrence-monthly_days_day']") # this locator is for monthly option, this is for the option 'Day X of every Y months'-the number of the day 
    SCHEDULE_RECURRENCE_MONTHLY_BY_DAY_OPTION_MONTH_NUMBER                  = ('xpath', "//input[@id='EventRecurrence-monthly_days_months']") # this locator is for monthly option, this is for the option 'Day X of every Y months'-the number of the month
    SCHEDULE_RECURRENCE_MONTHLY_BY_WEEKDAY_RADIO_BUTTON                     = ('xpath', "//input[@id='EventRecurrence-monthly_main-byWeekday']") # this locator is for monthly option, this is the second option in monthly were we choose also the day in the week 
    SCHEDULE_RECURRENCE_MONTHLY_WEEK_IN_THE_MONTH                           = ('xpath', "//select[@id='EventRecurrence-monthly_weekdays_index']") # this locator is for monthly option,this is the second option in monthly-the week in the month
    SCHEDULE_RECURRENCE_MONTHLY_DAY_IN_THE_MONTH                            = ('xpath', "//select[@id='EventRecurrence-monthly_weekdays_days']") # this locator is for monthly option,this is the second option in monthly-the day in the month
    SCHEDULE_RECURRENCE_MONTHLY_BY_WEEKDAY_OPTION_MONTH_NUMBER              = ('xpath', "//input[@id='EventRecurrence-monthly_weekdays_months']") # this locator is for monthly option,this is the second option in monthly-how many month
    SCHEDULE_RECURRENCE_SAVE_BUTTON                                         = ('xpath', "//a[@class='btn btn-primary' and contains(text(),'Save')]")
    SCHEDULE_EVENT_TITLE_IN_MY_SCHDULE_PAGE                                 = ('xpath', "//a[contains(text(), 'EVENT_TITLE')]")
    SCHEDULE_JUMP_TO_BUTTON                                                 = ('xpath', "//a[@id='jumpto']")
    SCHEDULE_EVENT_DATE_IN_THE_TOP_OF_THE_PAGE                              = ('xpath', "//th[contains(text(),'DATE')]") # the DATE need to be in format ("%B %d, %Y - %A") -us the parameter verifyDateFormat in event class, for exm: April 08, 2019 - Monday, 
    SCHEDULE_DELETE_EVENT_BUTTON                                            = ('xpath', "//i[@class='icon-trash icon-white']")
    SCHEDULE_EDIT_EVENT_PAGE_TITLE                                          = ('css', "div#titleBar")
    SCHEDULE_EDIT_EVENT_PAGE_START_DATE                                     = ('css', "input#rsStartTime-rsStartTime_date")
    SCHEDULE_EDIT_EVENT_PAGE_END_DATE                                       = ('css', "input#rsEndTime-rsEndTime_date")
    SCHEDULE_EDIT_EVENT_PAGE_SELECTED_RESOURCES                             = ('css', "div.sol-current-selection")
    SCHEDULE_EDIT_EVENT_PAGE_DELETE_RESOURCES                               = ('css', "span.sol-quick-delete")
    SCHEDULE_EDIT_EVENT_PAGE_CURRENT_TAGS                                   = ('css', "li.select2-search-choice")
    SCHEDULE_EDIT_EVENT_PAGE_DELETE_TAGS                                    = ('css', "a.select2-search-choice-close")
    SCHEDULE_EVENT_PAGE_GO_TO_SERIES_BUTTON                                 = ('css', "a#gotoSeries")
    SCHEDULE_VIEW_EVENT_SERIES_MESSAGE                                      = ('xpath', "//p[contains(text(),'You are viewing an event series')]")
    SCHEDULE_EDIT_EVENT_PAGE_RECURRENCE_BUTTON                              = ('css', "button#CreateEvent-recurrenceMain")
    SCHEDULE_CONTINUE_TO_SERIES_PAGE_WITHOUT_SAVE_MESSAGE                   = ('xpath', "//a[@class='btn btn-danger' and contains(text(),'Continue')]")
    SCHEDULE_VIEW_EVENT_PUBLISH_IN_SECTION_AFTER_PUBLISH                    = ('css', "div.pblBadge")
    SCHEDULE_CONFLICT_POP_UP_MESSAGE                                        = ('css', "div.bootbox.modal.fade.in")
    SCHEDULE_CONFLICT_POP_UP_MESSAGE_OK_BUTTON                              = ('xpath', "//a[@class='btn btn-primary' and contains(text(),'OK')]")
    SCHEDULE_POP_UP_MESSAGE_SAVE_SINGLE_EVENT_THAT_BELONG_TO_SERIES         = ('xpath', "//div[contains(text(),'Changes were made to a single occurrence from a series.')]")
    #=============================================================================================================
    
    # @Author: Michal Zomper 
    def navigateToMySchedule(self, forceNavigate=False):
        # Check if we are already in my media page
        if forceNavigate == False:
            if self.wait_element(self.SCHEDULE_PAGE_TITLE, 5) != False:
                writeToLog("INFO","Already in My Schedule")
                return True

        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False

        # Click on My Media
        if self.click(self.USER_MENU_MY_SCHEDULE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on My Schedule from the user menu")
            return False

        if self.wait_element(self.SCHEDULE_PAGE_TITLE, 15) == False:
            writeToLog("INFO","FAILED navigate to My Schedule page")
            return False

        return True
    
    
    # @Author: Michal Zomper 
    # The function create new reschedule event 
    def createRescheduleEvent(self, eventInstance):
        if self.createRescheduleEventWithoutRecurrence(eventInstance) == False:
            writeToLog("INFO","FAILED to create schedule event")
            return False
        sleep(2)
        
        if eventInstance.isRecurrence == True:
            if self.click(self.SCHEDULE_ADD_RECURRENCE_BUTTON) == False:
                writeToLog("INFO","FAILED to click on add recurrence button")
                return False
            sleep(1)
            
            if self.setEventRecurrence(eventInstance) == False:
                writeToLog("INFO","FAILED to set event recurrence")
                return False
        
        sleep(3)
        if eventInstance.exitEvent==False:
            if self.click(self.SCHEDULE_SAVE_EVENT) == False:
                writeToLog("INFO","FAILED click on save event button")
                return False
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_element(self.SCHEDULE_CREATE_EVENT_SUCCESS_MESSAGE) == False:
                writeToLog("INFO","FAILED find event created success message")
                return False
            
            sleep(5)
        else:
            if self.click(self.SCHEDULE_SAVE_AND_EXIT_EVENT) == False:
                writeToLog("INFO","FAILED click on save and exit event button")
                return False
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_element(self.SCHEDULE_PAGE_TITLE, 15) == False:
                writeToLog("INFO","FAILED to verify 'My Schedule page' display after clicking on save and exit event button")
                return False
        
        writeToLog("INFO","Success, Event was created successfully") 
        return True 
    
    
    # @Author: Michal Zomper 
    # The function create new reschedule event without recurrence
    def createRescheduleEventWithoutRecurrence(self, eventInstance): 
        if self.navigateToCreateEventPage() == False:
            writeToLog("INFO","FAILED to enter create event page")
            return False
        sleep(2)
        
        if self.updateEventTitle(eventInstance.title) == False:
            writeToLog("INFO","FAILED to add event title")
            return False
            
        if eventInstance.organizer != '':
            if self.updateorganizer(eventInstance.organizer) == False:
                writeToLog("INFO","FAILED to update event organizer name")
                return False
        
        if self.clsCommon.editEntryPage.setScheduleStartDate(eventInstance.startDate) == False:
            writeToLog("INFO","FAILED to set event start date")
            return False
        sleep(2) 
        
        if len(eventInstance.startTime) != 0:
            if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_EVENT_START_TIME, eventInstance.startTime) == False:
                writeToLog("INFO","FAILED to set event start time")
                return False
            sleep(2) 
        # else = use the default value
        
        if self.clsCommon.editEntryPage.setScheduleEndDate(eventInstance.endDate) == False:
            writeToLog("INFO","FAILED to set event end date")
            return False
        sleep(2)  
        # else = use the default value
        
        if len(eventInstance.endTime) != 0:
            if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_EVENT_END_TIME, eventInstance.endTime) == False:
                writeToLog("INFO","FAILED to set event end time")
                return False
            sleep(2)
        
        if eventInstance.resources != '':
            if self.updateEventResources(eventInstance.resources) == False:
                writeToLog("INFO","FAILED to add resources")
                return False 
            
        if self.updateDescription(eventInstance.description) == False:
            writeToLog("INFO","FAILED to add Description")
            return False
        
        if self.fillFileScheduleTags(eventInstance.tags) == False:
            writeToLog("INFO","FAILED to set event tags")
            return False
        
        # copyDetailsEventToRecording == False mean that we need to insert new metadata 
        if eventInstance.copyDetailsEventToRecording == False:
            if self.changeEventDetailsInEventCopyDetails(eventInstance) == False:
                writeToLog("INFO","FAILED to set new metadata in 'Copy details from event to recording' section")
                return False
            
        return True
            
       
    # @Author: Michal Zomper      
    # The method supports BOTH single and multiple upload
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillFileScheduleTags(self, tags):
        # remove any tags if their are any
        if (self.wait_elements(self.SCHEDULE_EDIT_EVENT_PAGE_CURRENT_TAGS, timeout=5)) != False:
            # we are reducing 1 from the len since it's always add an empty tag
            if (len(self.wait_elements(self.SCHEDULE_EDIT_EVENT_PAGE_CURRENT_TAGS)) -1) > 0:
                tmpTags = self.get_elements(self.SCHEDULE_EDIT_EVENT_PAGE_DELETE_TAGS)
                tagsCount = len(tmpTags)
                for tag in tmpTags:
                    if tagsCount > 1:
                        try:
                            if tag.size['width'] != 0.0:
                                if self.clickElement(tag) == False:
                                    writeToLog("INFO","FAILED to remove tag")
                                    return False
                        except:
                            # element: tag.size['width'] == 0.0- doesn't really exist 
                            pass
                    tagsCount = tagsCount-1
                
        try:
            tagsElement = self.get_element(self.SCHEDULE_EVENT_TAGS)
                 
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get Tags filed element")
            return False
                 
        if self.clickElement(tagsElement) == False:
            writeToLog("INFO","FAILED to click on Tags filed")
            return False            
        sleep(1)
        if self.send_keys(self.SCHEDULE_EVENT_INPUT_TAGS, tags) == True:
            sleep(2)
            return True
    
        writeToLog("INFO","FAILED to type in Tags")
        return False   
        
        
    # @Author: Michal Zomper   
    def navigateToCreateEventPage(self, forceNavigate=False):
        if self.navigateToMySchedule(forceNavigate) == False:
            writeToLog("INFO","FAILED navigate to My Schedule page")
            return False
        sleep(2)
        
        if self.click(self.SCHEDULE_CREATE_EVENT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on create event button")
            return False
        
        if self.wait_element(self.SCHEDULE_CREATE_EVENT_PAGE_TITLE, timeout=15) == False:
            writeToLog("INFO","FAILED to verify create event page is display")
            return False
            
        return True
    
    
    # @Author: Michal Zomper 
    # The function insert new metadata in to the section 'Copy details from event to recording' 
    def changeEventDetailsInEventCopyDetails(self, eventInstance):
        if self.click(self.SCHEDULE_COPE_DETAILS_BUTTON) == False:
            writeToLog("INFO","FAILED to uncheck 'Copy details from event to recording' button")
            return False
        
        if eventInstance.copeDetailsName != '':
            if self.clear_and_send_keys(self.SCHEDULE_COPE_DETAILS_NAME, eventInstance.copeDetailsName) == False:
                writeToLog("INFO","FAILED to insert new name in 'Copy details from event to recording'")
                return False   
        
        if eventInstance.copeDetailsDescriptio != '':
            # Click in Description text box
            if self.click(self.SCHEDULE_COPE_DETAILS_DESCRIPTION) == False:
                writeToLog("INFO","FAILED to click in description textbox")
                return False
             
            # Enter text Description
            if self.clear_and_send_keys(self.SCHEDULE_COPE_DETAILS_DESCRIPTION, eventInstance.copeDetailsDescriptio) == False:
                writeToLog("INFO","FAILED to insert new description in 'Copy details from event to recording'")
                return False

        if  eventInstance.copeDetailsTags != '':
            if self.clsCommon.upload.fillFileUploadEntryTags(eventInstance.copeDetailsTags) == False:
                writeToLog("INFO","FAILED to insert new tags in 'Copy details from event to recording'")
                return False
            
        return True
    
    
    # @Author: Michal Zomper 
    # recurrenceInterval - this parameter need to be send as an enum- scheduleRecurrenceInterval
    # dailyOption - this parameter need to be send as an enum- scheduleRecurrenceDailyOption
    # dailyDays - if in daily 'every X days' option was chosen this parameter will go the number of days
    # weeklyWeeks - if weekly was chosen this parameter will go the number of weeks
    # weeklyDaysNames - if weekly was chosen this parameter will have the day or days that the event need to recurrence, this parameter need to be send as an enum- scheduleRecurrenceDayOfTheWeek, take the day that have SHORT' in it like SUNDAY_SHORT
    # monthlyOption - this parameter need to be send as an enum- scheduleRecurrenceMonthlyOption
    # monthlyDayNumber - this parameter is for the number of day in monthly first option
    # monthlyMonthNumber - this parameter is for the number of month in monthly first option
    # monthlyWeekdaysIndex - this parameter is for the day index ,the first parameter of monthly second option, this parameter need to be send as an enum- scheduleRecurrenceMonthlyIndex
    # monthlyDayName - this parameter is for the day name that in the second monthly option ,this parameter need to be send as an enum- scheduleRecurrenceDayOfTheWeek, take the day without  the 'SHORT' in it like SUNDAY
    # optionTwoMonthlyMonthNumber - this parameter is for the number of month in monthly second option
    def setEventRecurrence(self,eventInstance):
        # Choose the needed interval
        tmpRecurrenceInterval = (self.SCHEDULE_RECURRENCE_INTERVAL[0], self.SCHEDULE_RECURRENCE_INTERVAL[1].replace('RECURRENCE_INTERVAL', eventInstance.recurrenceInterval.value))
        sleep(1)
        if self.click(tmpRecurrenceInterval) == False:
            writeToLog("INFO","FAILED to select recurrence interval: " + eventInstance.recurrenceInterval.value)
            return False
        sleep(1)
        
        if eventInstance.recurrenceInterval == enums.scheduleRecurrenceInterval.DAYS:
            if eventInstance.dailyOption == enums.scheduleRecurrenceDailyOption.EVERY_X_DAYS:
                if self.click(self.SCHEDULE_RECURRENCE_DAILY_EVERY_X_DAYS_RADIO_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on 'every X days' radio button")
                    return False
                sleep(1)
                
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_DAILY_EVERY_X_DAYS, eventInstance.dailyDays) == False:
                    writeToLog("INFO","FAILED to add number of days to the 'every X days' option")
                    return False
            
            elif eventInstance.dailyOption == enums.scheduleRecurrenceDailyOption.EVERY_WEEKDAY:
                if self.click(self.SCHEDULE_RECURRENCE_DAILY_WEEKDAY_RADIO_BUTTON) == False:
                    writeToLog("INFO","FAILED to add number of weeks to the weekly option")
                    return False
                
        elif eventInstance.recurrenceInterval == enums.scheduleRecurrenceInterval.WEEKS: 
            if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_WEEKLY_EVERY_X_WEEKS, eventInstance.weeklyWeeks) == False:
                writeToLog("INFO","FAILED to add number of days to the 'every X days' option")
                return False
            sleep(1)
            
            if type(eventInstance.weeklyDaysNames) is list: 
                for dayInTheWeek in eventInstance.weeklyDaysNames:
                    tmpDay = (self.SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK[0], self.SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK[1].replace('DAY_OF_THE_WEEK', dayInTheWeek.value))
                    if self.click(tmpDay) == False:
                        writeToLog("INFO","FAILED to select day '" + dayInTheWeek.value + "' in weekly option")
                        return False
                        
            else:   
                tmpDay = (self.SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK[0], self.SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK[1].replace('DAY_OF_THE_WEEK',eventInstance.weeklyDaysNames.value))
                if self.click(tmpDay) == False:
                    writeToLog("INFO","FAILED to select day '" + eventInstance.weeklyDaysNames.value + "' in weekly option")
                    return False  
                
        elif eventInstance.recurrenceInterval == enums.scheduleRecurrenceInterval.MONTHS:  
            if eventInstance.monthlyOption == enums.scheduleRecurrenceMonthlyOption.DAY_X_OF_EVERY_Y_MONTHS:
                if self.click(self.SCHEDULE_RECURRENCE_MONTHLY_DAY_X_OF_EVERY_Y_MONTHS_RADIO_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on 'day X of every Y months' radio button")
                    return False
                sleep(1)
                
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_MONTHLY_BY_DAY_OPTION_DAY_NUMBER, eventInstance.monthlyDayNumber) == False:
                    writeToLog("INFO","FAILED to add number of days to the 'day X of every Y months' option")
                    return False
                sleep(1)
                    
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_MONTHLY_BY_DAY_OPTION_MONTH_NUMBER, eventInstance.monthlyMonthNumber) == False:
                    writeToLog("INFO","FAILED to add number of month to the 'day X of every Y months' option")
                    return False
            
            elif eventInstance.monthlyOption == enums.scheduleRecurrenceMonthlyOption.BY_WEEKDAY:
                if self.click(self.SCHEDULE_RECURRENCE_MONTHLY_BY_WEEKDAY_RADIO_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on 'by weekday' radio button")
                    return False
                sleep(1)
                
                if self.select_from_combo_by_text(self.SCHEDULE_RECURRENCE_MONTHLY_WEEK_IN_THE_MONTH , eventInstance.monthlyWeekdaysIndex.value) == False:
                    writeToLog("INFO","FAILED to choose index or the day index for monthly second option")
                    return False
                sleep(1)
                   
                if self.select_from_combo_by_text(self.SCHEDULE_RECURRENCE_MONTHLY_DAY_IN_THE_MONTH, eventInstance.monthlyDayName.value) == False:
                    writeToLog("INFO","FAILED to select day for monthly second option")
                    return False
                sleep(1)
                
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_MONTHLY_BY_WEEKDAY_OPTION_MONTH_NUMBER, eventInstance.optionTwoMonthlyMonthNumber) == False:
                    writeToLog("INFO","FAILED to add number of month for monthly second option")
                    return False
        
       
        if self.setRecurrenceRange(eventInstance) == False:
            writeToLog("INFO","FAILED to set event recurrence range")
            return False

        if self.click(self.SCHEDULE_RECURRENCE_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on save recurrence button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()   
        writeToLog("INFO","Success, Event recurrence was set")   
        return True
    
    
    # @Author: Michal Zomper 
    # endDateOption - this parameter need to be send as enum: scheduleRecurrenceEndDateOption
    # numberOfRecurrence - this parameter is for end date option 'end after X occurrences' 
    def setRecurrenceRange(self, eventInstance): #endDateOption, reccurenceStartTime,reccurenceStartDate, reccurenceEndTime, reccurenceEndDate, numberOfRecurrence =''):
        if (self.changeDateOrder(self.wait_element(self.SCHEDULE_RECURRENCE_START_DATE_CALENDAR).get_attribute("value")) == eventInstance.startDate) == False:
            if self.setRecurrenceStartDate(eventInstance.startDate) == False:
                writeToLog("INFO","FAILED to set event start date")
                return False
            sleep(2) 
        
        if eventInstance.endDateOption == enums.scheduleRecurrenceEndDateOption.END_AFTER_X_OCCURRENCES:
            if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_END_DATE_AFTER_X_OCCURRENCES  , eventInstance.numberOfRecurrence) == False:
                writeToLog("INFO","FAILED insert number of occurrences to end date")
                return False
            
        elif eventInstance.endDateOption == enums.scheduleRecurrenceEndDateOption.END_BY:
            tmpEndDate = (self.SCHEDULE_RECURRENCE_END_DATE_REDIO_BUTTON[0], self.SCHEDULE_RECURRENCE_END_DATE_REDIO_BUTTON[1].replace('END_DTAR_OPTION', eventInstance.endDateOption.value))
            if self.click(tmpEndDate) == False:
                writeToLog("INFO","FAILED to choose end date option")
                return False
            
            if (self.changeDateOrder(self.wait_element(self.SCHEDULE_RECURRENCE_END_DATE_CALENDAR).get_attribute("value")) == eventInstance.endDate) == False:
                if self.setRecurrenceEndDate(eventInstance.endDate) == False:
                    writeToLog("INFO","FAILED to set event end date")
                    return False
            sleep(2)  
        
        if len(eventInstance.startTime) != 0:
            if (self.wait_element(self.SCHEDULE_RECURRENCE_START_TIME).get_attribute("value") == eventInstance.startTime) == False:
                if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_RECURRENCE_START_TIME, eventInstance.startTime) == False:
                    writeToLog("INFO","FAILED to set event start time")
                    return False
                sleep(2) 
        
        if len(eventInstance.endTime) != 0:
            if (self.wait_element(self.SCHEDULE_RECURRENCE_END_TIME).get_attribute("value") == eventInstance.endTime) == False:
                if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_RECURRENCE_END_TIME, eventInstance.endTime) == False:
                    writeToLog("INFO","FAILED to set event end time")
                    return False
                sleep(2)
        
        return True


    # @Author: Michal Zomper 
    # Format desteStr - '24/01/2018'
    # startOrEnd - String 'start' or 'end'
    def setRecurrenceStartDate(self, dateStr):
        return self.setRecurrenceScheduleDate(dateStr, 'start')
    
    
    # @Author: Michal Zomper 
    def setRecurrenceEndDate(self, dateStr):
        return self.setRecurrenceScheduleDate(dateStr, 'end')
        
    
    # @Author: Michal Zomper    
    def setRecurrenceScheduleDate(self, dateStr, startOrEnd):
        if startOrEnd.lower() == 'start':
            locator = (self.SCHEDULE_RECURRENCE_START_DATE_CALENDAR[0], self.SCHEDULE_RECURRENCE_START_DATE_CALENDAR[1] + "/following-sibling::span")
        elif startOrEnd.lower() == 'end':
            locator = (self.SCHEDULE_RECURRENCE_END_DATE_CALENDAR[0], self.SCHEDULE_RECURRENCE_END_DATE_CALENDAR[1] + "/following-sibling::span")
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
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_TOP) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the year")
            return False
        
        # Click again to show all years
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_TOP, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the year")
            return False
        
        # Select a year
        if self.click((self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_YEAR[0], self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_YEAR[1].replace('YEAR', year))) == False:
            writeToLog("INFO","FAILED to select the year")
            return False        
        
        # Set Month
        if self.click((self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH[0], self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH[1].replace('MONTH', month))) == False:
            writeToLog("INFO","FAILED to select the month")
            return False
        
        # Set Day
        # We have class of 'old day', 'day' and 'today active day'. The issue is when we have the same day on specific month.
        # The solution is to get_elemets of contains(@class,'day') and NOT click on 'old day'
        if self.clsCommon.editEntryPage.clickOnDayFromDatePicker(day) == False:
            writeToLog("INFO","FAILED to select the day")
            return False        
        
        return True
    
    
    # @Author: Michal Zomper
    # verifyDateFormat = this parameter format need to be : "%B %d, %Y - %A". example- April 07, 2019 - Sunday
    def verifyScheduleEventInMySchedulePage(self, eventInstance):
        if self.setScheduleInMySchedulePage(eventInstance.verifyDateFormat) == False:
            writeToLog("INFO","FAILED to move to start time '" + eventInstance.startDate + "' in my schedule page")
            return False  
        sleep(1)
        tmpEventTiltle = (self.SCHEDULE_EVENT_TITLE_IN_MY_SCHDULE_PAGE[0], self.SCHEDULE_EVENT_TITLE_IN_MY_SCHDULE_PAGE[1].replace('EVENT_TITLE', eventInstance.title))
        event = self.wait_element(tmpEventTiltle, multipleElements=True)
        if event == False:
            if eventInstance.expectedEvent == True:
                writeToLog("INFO","FAILED to find event title")
                return False
            
            elif eventInstance.expectedEvent == False: 
                writeToLog("INFO","Success, As expected event isn't display in my schedule page")
                return True
        else:
            if eventInstance.expectedEvent == False:
                writeToLog("INFO","FAILED, event display although it shouldn't need to be displayed in this date: " + eventInstance.startDate)
                return False           
             
        eventParentEl = event.find_element_by_xpath("../..")
        eventMetadata = eventParentEl.text
        if eventMetadata == None:
            writeToLog("INFO","FAILED to find event element text")
            return False
        
        if eventInstance.startTime.replace(" ", "").lower() + "-" + eventInstance.endTime.replace(" ", "").lower() in eventMetadata == False:
            writeToLog("INFO","FAILED to find event time")
            return False
        
        if eventInstance.resources != '':
            if type(eventInstance.resources) is list:
                for resource in eventInstance.resources:
                    if resource.value in eventMetadata == False:
                        writeToLog("INFO","FAILED to find event resource: " + resource)
                        return False
            else:
                if eventInstance.resources.value in eventMetadata == False:
                        writeToLog("INFO","FAILED to find event resource: " + eventInstance.resources)
                        return False
        
        writeToLog("INFO","Success, Event name/date/time/resource display correctly in my schedule page")
        return True
    
    
    # @Author: Michal Zomper
    # the function choose the needed date form calendar in my schedule page
    # the dateStr need to be in format ("%B %d, %Y - %A")- us the parameter verifyDateFormat in event class, for exm: April 08, 2019 - Monday,
    def setScheduleInMySchedulePage(self, dateStr, forceNavigate=False):
        if self.navigateToMySchedule() == False:
            writeToLog("INFO","FAILED navigate to my schedule page")
            return False
            
        # verify that the need date isn't already display
        tmpNeededDate = (self.SCHEDULE_EVENT_DATE_IN_THE_TOP_OF_THE_PAGE[0], self.SCHEDULE_EVENT_DATE_IN_THE_TOP_OF_THE_PAGE[1].replace('DATE', dateStr))
        if self.wait_element(tmpNeededDate, timeout=5, multipleElements=True) != False:
            writeToLog("INFO","Success, date '" + dateStr + "' display")
            return True
        
        if self.click(self.SCHEDULE_JUMP_TO_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'jump to' button")
            return False
        
        tmpDate = dateStr.split('-')[0]
        tmpDate = tmpDate.split(',')
        year = tmpDate[1][1:-1]
        tmpDate = tmpDate[0].split(' ')
        month =  tmpDate[0][:3]
        # Convert to int and back to string, to remove 0 before a digit. For example from '03' to '3'
        day = int(tmpDate[1])
        day = str(day)     
            
        # Set a year
        # Click on the year - at the top of the calendar
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_TOP) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the year")
            return False
        
        # Click again to show all years
        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_TOP, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on the top of the calendar, to select the year")
            return False
        
        # Select a year
        if self.click((self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_YEAR[0], self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_YEAR[1].replace('YEAR', year))) == False:
            writeToLog("INFO","FAILED to select the year")
            return False        
        
        # Set Month
        if self.click((self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH[0], self.clsCommon.editEntryPage.EDIT_ENTRY_SCHEDULING_CALENDAR_MONTH[1].replace('MONTH', month))) == False:
            writeToLog("INFO","FAILED to select the month")
            return False
        
        # Set Day
        # We have class of 'old day', 'day' and 'today active day'. The issue is when we have the same day on specific month.
        # The solution is to get_elemets of contains(@class,'day') and NOT click on 'old day'
        if self.clsCommon.editEntryPage.clickOnDayFromDatePicker(day) == False:
            writeToLog("INFO","FAILED to select the day")
            return False        
        
        # Verify correct day display in my schedule
        if self.wait_element(tmpNeededDate, timeout=5, multipleElements=True) == False:
            writeToLog("INFO","FAILED, the date '" + dateStr + "' is not display in the page")
            return False      
        
        sleep(1)
        writeToLog("INFO","Success, date '" + dateStr + "' display") 
        return True
    
    
    # @Author: Michal Zomper
    # The function delete a singel event or an event series
    # viewEventSeries - if we wont to edit/delete or change a parameter in event that will affect the entire series this parameter need to be True in order to go viewing an event series.
    def deteteEvent(self, eventInstance, viewEventSeries=False):
        if self.navigateToEventPage(eventInstance, viewEventSeries) == False:
            writeToLog("INFO","FAILED navigate to edit event page")
            return False  
        sleep(1)
        
        if self.click(self.SCHEDULE_DELETE_EVENT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on delete event button")
            return False
        sleep(1)
        
        # Click on confirm delete
        if self.click(self.clsCommon.myMedia.MY_MEDIA_CONFIRM_ENTRY_DELETE, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear() 
        sleep(2)
        
        if self.wait_element(self.SCHEDULE_PAGE_TITLE, timeout=5, multipleElements=True) == True:
            writeToLog("INFO","FAILED to verify my schedule page display")
            return False 
        
        # verify event deleted
        if self.setScheduleInMySchedulePage(eventInstance.verifyDateFormat) == False:
            writeToLog("INFO","FAILED to move to start time '" + eventInstance.verifyDateFormat + "' in my schedule page")
            return False 
         
        tmpEventTiltle = (self.SCHEDULE_EVENT_TITLE_IN_MY_SCHDULE_PAGE[0], self.SCHEDULE_EVENT_TITLE_IN_MY_SCHDULE_PAGE[1].replace('EVENT_TITLE', eventInstance.title))
        if self.wait_element(tmpEventTiltle, timeout=5, multipleElements=True) == True:
            writeToLog("INFO","FAILED event '" + eventInstance.verifyDateFormat.title + "' was find although it was deleted")
            return False 
        
        writeToLog("INFO","Success, Event was deleted successfully")
        return True
        

    # @Author: Michal Zomper 
    # The function navigate to event page
    # viewEventSeries - if we wont to edit/delete or change a parameter in event that will affect the entire series this parameter need to be True in order to go viewing an event series. 
    def navigateToEventPage(self, eventInstance, viewEventSeries=False):
        tmpTiltle = (self.SCHEDULE_EVENT_TITLE[0], self.SCHEDULE_EVENT_TITLE[1].replace('EVENT_TITLE', eventInstance.title))
        if self.wait_element(tmpTiltle, timeout=5) != False:
            if viewEventSeries == True:
                if self.wait_element(self.SCHEDULE_VIEW_EVENT_SERIES_MESSAGE) != False:
                    writeToLog("INFO","Already in series page")
                    return True
            else: 
                writeToLog("INFO","Already in event page")
                return True 
        
        sleep(2)
        if self.setScheduleInMySchedulePage(eventInstance.verifyDateFormat) == False:
            writeToLog("INFO","FAILED to move to start time '" + eventInstance.verifyDateFormat + "' in my schedule page")
            return False  
        sleep(5)
        
        tmpEventTiltle = (self.SCHEDULE_EVENT_TITLE_IN_MY_SCHDULE_PAGE[0], self.SCHEDULE_EVENT_TITLE_IN_MY_SCHDULE_PAGE[1].replace('EVENT_TITLE', eventInstance.title))
        if self.click(tmpEventTiltle, multipleElements=True) == False:
            writeToLog("INFO","FAILED to find and click on event '" + eventInstance.title + "' in my schedule page")
            return False 
        
        if viewEventSeries == True:
            if self.click(self.SCHEDULE_EVENT_PAGE_GO_TO_SERIES_BUTTON) == False:
                writeToLog("INFO","FAILED to click on 'go to series button' in event page")
                return False 
            
            # if a change were made in event page without save a popup message will display and ask if we wont to continue without save
            if self.wait_element(self.SCHEDULE_CONTINUE_TO_SERIES_PAGE_WITHOUT_SAVE_MESSAGE, timeout=6) == True:
                if self.click(self.SCHEDULE_CONTINUE_TO_SERIES_PAGE_WITHOUT_SAVE_MESSAGE) == False:
                    writeToLog("INFO","FAILED click on continue button in order to go to serires page")
                    return False
            self.clsCommon.general.waitForLoaderToDisappear()
            sleep(1)
            
            if self.wait_element(self.SCHEDULE_VIEW_EVENT_SERIES_MESSAGE) == False:
                writeToLog("INFO","FAILED to verify that event series view display")
                return False
            
        if self.wait_element(tmpTiltle, timeout=30) == False:
            writeToLog("INFO","FAILED to verify that edit event '" + eventInstance.title + "' page display")
            return False 
    
        return True
    
    
    # @Author: Michal Zomper  
    def VerifyEventDeatailsInEventPage(self, eventInstance):
        if self.navigateToEventPage(eventInstance) == False:
            writeToLog("INFO","FAILED navigate to edit event page")
            return False  
        sleep(1)
        if (self.wait_element(self.SCHEDULE_EVENT_TITLE).get_attribute("value") == eventInstance.title) == False:
            writeToLog("INFO","FAILED to verify event title")
            return False
         
        if (self.wait_element(self.SCHEDULE_EVENT_ORGANIZER).get_attribute("value") == eventInstance.organizer) == False:
            writeToLog("INFO","FAILED to verify event organizer")
            return False
            
        if (self.changeDateOrder(self.wait_element(self.SCHEDULE_EDIT_EVENT_PAGE_START_DATE).get_attribute("value")) == eventInstance.startDate) == False:
            writeToLog("INFO","FAILED to verify event start date")
            return False
        
        if (self.changeDateOrder(self.wait_element(self.SCHEDULE_EDIT_EVENT_PAGE_END_DATE).get_attribute("value")) == eventInstance.endDate) == False:
            writeToLog("INFO","FAILED to verify event end date")
            return False
        
        if (self.wait_element(self.SCHEDULE_EVENT_START_TIME).get_attribute("value") == eventInstance.startTime) == False:
            writeToLog("INFO","FAILED to verify event start time")
            return False
        
        if (self.wait_element(self.SCHEDULE_EVENT_END_TIME).get_attribute("value") == eventInstance.endTime) == False:
            writeToLog("INFO","FAILED to verify event end time")
            return False
            
        if eventInstance.resources != "":
            if type(eventInstance.resources) is list:
                tmpResources = self.wait_element(self.SCHEDULE_EDIT_EVENT_PAGE_SELECTED_RESOURCES).text
                for resource in eventInstance.resources:
                    if (resource.value in tmpResources) == False:
                        writeToLog("INFO","FAILED to verify event resource '" + resource.value + "'")
                        return False
            else:
                if (eventInstance.resources.value in self.wait_element(self.SCHEDULE_EDIT_EVENT_PAGE_SELECTED_RESOURCES).text) == False:
                    writeToLog("INFO","FAILED to verify event resource '" + eventInstance.resources.value + "'")
                    return False
            
        if (self.wait_element(self.SCHEDULE_EVENT_DESCRIPTION).text == eventInstance.description) == False:
            writeToLog("INFO","FAILED to verify event description")
            return False
        
        if eventInstance.tags != "":                 
            tagsList = eventInstance.tags.split(",")
            tmpTags = self.wait_element(self.SCHEDULE_EVENT_TAGS).text.replace("\n", " ")
            for tag in tagsList:
                if (tag in tmpTags) == False:
                    writeToLog("INFO","FAILED to verify event tag '" + tag + "'")
                    return False
        
        if eventInstance.collaboratorUser != '':
            # Check that the user was added to collaboration permissions table
            tmpUserName = (self.clsCommon.editEntryPage.EDIT_ENTRY_CHOSEN_USER_IN_COLLABORATOR_TABLE[0], self.clsCommon.editEntryPage.EDIT_ENTRY_CHOSEN_USER_IN_COLLABORATOR_TABLE[1].replace('USER_NAME', eventInstance.collaboratorUser))
            parentEl = self.get_element(tmpUserName)
            if parentEl == None:
                writeToLog("INFO","FAILED to find added user in collaboration permissions table")
                return False      
            
            tmp_permissions = self.clsCommon.editEntryPage.setCollaboratorPermissionsLocator(eventInstance.coEditor, eventInstance.coPublisher, eventInstance.coViewer)
            if tmp_permissions == False:
                writeToLog("INFO", "FAILED to set  permissions locator")
                return False
            
            # Check that the user permissions correctly were added to collaboration permissions table
            try:
                self.get_child_element(parentEl, tmp_permissions)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find added user permissions in collaboration permissions table")
                return False
        
        # verify publish section if exist
        if eventInstance.publishTo !='':
            # Check if 'Copy details from event' check box is checked and if it's check unchecked it 
            # default is that 'Copy details from event' is checked and to open its need to be unchecked
            if self.is_element_checked(self.SCHEDULE_COPE_DETAILS_BUTTON) == True:
                if self.check_element(self.SCHEDULE_COPE_DETAILS_BUTTON, 'True') == False:
                    writeToLog("INFO","FAILED to unchecked 'Copy details from event' button")
                    return False
            sleep(1)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
            sleep(1)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
            sleep(1)
            self.wait_element(self.SCHEDULE_VIEW_EVENT_PUBLISH_IN_SECTION_AFTER_PUBLISH, timeout=30)
            try:
                tmpPublish = self.get_element(self.SCHEDULE_VIEW_EVENT_PUBLISH_IN_SECTION_AFTER_PUBLISH).text
            except:
                writeToLog("INFO","FAILED to find publish section in event page")
                return False
            
            if ("Published in" in tmpPublish) == False:
                writeToLog("INFO","FAILED to find 'publish in' title in event page")
                return False
            
            # verify all category/channel name that the event published to display
            if eventInstance.categoryList != '':
                if type(eventInstance.categoryList) is list:
                    for category in eventInstance.categoryList:
                        if (category in tmpPublish) == False:
                            writeToLog("INFO","FAILED to find category '" + category + "' name in event page")
                            return False
                else:
                    if (eventInstance.categoryList in tmpPublish) == False:
                        writeToLog("INFO","FAILED to find category '" + eventInstance.categoryList + "' name in event page")
                        return False
            
            if eventInstance.channelList != '':
                if type(eventInstance.channelList) is list:
                    for channel in eventInstance.channelList:
                        if (channel in tmpPublish) == False:
                            writeToLog("INFO","FAILED to find channel '" + channel + "' name in event page")
                            return False
                else:
                    if (eventInstance.channelList in tmpPublish) == False:
                        writeToLog("INFO","FAILED to find channel '" + eventInstance.channelList + "' name in event page")
                        return False
            
        
        writeToLog("INFO","Success, Event metadata in event page were verify successfully")
        return True
        
    
    # @Author: Michal Zomper 
    def editRescheduleEvent(self, eventInstance):
        if self.editRescheduleEventWithoutRecurrence(eventInstance) == False:
            writeToLog("INFO","FAILED to update event metadata")
            return False
            
        if eventInstance.isRecurrence == True:
            if self.click(self.SCHEDULE_EDIT_EVENT_PAGE_RECURRENCE_BUTTON) == False:
                writeToLog("INFO","FAILED to click on recurrence button")
                return False
            sleep(2)
            
            if self.setEventRecurrence(eventInstance) == False:
                writeToLog("INFO","FAILED to update recurrence metadata")
                return False
                
        sleep(3)
        if eventInstance.exitEvent==False:
            if self.click(self.SCHEDULE_SAVE_EVENT) == False:
                writeToLog("INFO","FAILED click on save event button")
                return False
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_element(self.SCHEDULE_CREATE_EVENT_SUCCESS_MESSAGE) == False:
                writeToLog("INFO","FAILED find event created success message")
                return False
            
            sleep(5)
        else:
            if self.click(self.SCHEDULE_SAVE_AND_EXIT_EVENT) == False:
                writeToLog("INFO","FAILED click on save and exit event button")
                return False
            sleep(2)
            
            # if we are changing a single event that was created as part of event series a pop up will display and ask if we wont to save the changes
            if self.wait_element(self.SCHEDULE_POP_UP_MESSAGE_SAVE_SINGLE_EVENT_THAT_BELONG_TO_SERIES) != False:
                sleep(1)
                if self.click(self.SCHEDULE_RECURRENCE_SAVE_BUTTON, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on save button in order to save event occurrence changes")
                    return False
            self.clsCommon.general.waitForLoaderToDisappear()  
             
            if self.wait_element(self.SCHEDULE_PAGE_TITLE, 15) == False:
                writeToLog("INFO","FAILED to verify 'My Schedule page' display after clicking on save and exit event button")
                return False
        
        writeToLog("INFO","Success, Edit event was created successfully") 
        return True 
        
    # @Author: Michal Zomper 
    # The function edit reschedule event without recurrence
    def editRescheduleEventWithoutRecurrence(self, eventInstance): 
        for update in eventInstance.fieldsToUpdate:
            sleep(1)
            if update.lower() == "title":
                if self.updateEventTitle(eventInstance.title) == False:
                    writeToLog("INFO","FAILED to update event title")
                    return False
                
            elif update.lower() == "organizer":
                if self.updateorganizer(eventInstance.organizer) == False:
                    writeToLog("INFO","FAILED to update event organizer name")
                    return False
            
            elif update.lower() == "startdate":
                if self.clsCommon.editEntryPage.setScheduleStartDate(eventInstance.startDate) == False:
                    writeToLog("INFO","FAILED to set event start date")
                    return False
                sleep(2) 
            
            elif update.lower() == "starttime":
                if len(eventInstance.startTime) != 0:
                    if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_EVENT_START_TIME, eventInstance.startTime) == False:
                        writeToLog("INFO","FAILED to set event start time")
                        return False
                    sleep(2) 
            
            elif update.lower() == "enddate":
                if self.clsCommon.editEntryPage.setScheduleEndDate(eventInstance.endDate) == False:
                    writeToLog("INFO","FAILED to set event end date")
                    return False
                sleep(2)  
            
            elif update.lower() == "endtime":
                if len(eventInstance.endTime) != 0:
                    if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_EVENT_END_TIME, eventInstance.endTime) == False:
                        writeToLog("INFO","FAILED to set event end time")
                        return False
                    sleep(2)
            
            elif update.lower() == "resources":
                if self.updateEventResources(eventInstance.resources) == False:
                    writeToLog("INFO","FAILED to update resources")
                    return False
                
            elif update.lower() == "description":    
                if self.updateDescription(eventInstance.description) == False:
                    writeToLog("INFO","FAILED to update Description")
                    return False
            
            elif update.lower() == "tags":  
                if self.fillFileScheduleTags(eventInstance.tags) == False:
                    writeToLog("INFO","FAILED to update tags")
                    return False
            
            elif update.lower() == "copydetailseventtorecording":
                if self.changeEventDetailsInEventCopyDetails(eventInstance) == False:
                    writeToLog("INFO","FAILED to update new metadata in 'Copy details from event to recording' section")
                    return False
            
        return True
    
    
#     def editRecurrecntEvent(self,eventInstance):
#         if self.click(self.SCHEDULE_EDIT_EVENT_PAGE_RECURRENCE_BUTTON) == False:
#             writeToLog("INFO","FAILED to click on recurrence button")
#             return False
#         sleep(2)
#         
#         for update in eventInstance.eventRecurrencefieldsToUpdate:
#             if update.lower() == "startdate":
#                 if self.setRecurrenceStartDate(eventInstance.startDate) == False:
#                     writeToLog("INFO","FAILED to set event start date")
#                     return False
#                 sleep(2) 
#          
#             elif update.lower() == "starttime":
#                 if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_RECURRENCE_START_TIME, eventInstance.startTime) == False:
#                     writeToLog("INFO","FAILED to set event start time")
#                     return False
#                 sleep(2) 
#             
#             elif update.lower() == "enddate":
#                 if self.setRecurrenceEndDate(eventInstance.endDate) == False:
#                     writeToLog("INFO","FAILED to set event end date")
#                     return False
#                 sleep(2)  
#             
#             elif update.lower() == "endtime":
#                 if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_RECURRENCE_END_TIME, eventInstance.endTime) == False:
#                     writeToLog("INFO","FAILED to set event end time")
#                     return False
#                     sleep(2)
#             
#         if self.click(self.SCHEDULE_RECURRENCE_SAVE_BUTTON) == False:
#             writeToLog("INFO","FAILED to click on recurrence save button")
#             return False
#         self.clsCommon.general.waitForLoaderToDisappear()
#         
#         return True
    
    # @Author: Michal Zomper 
    def updateEventTitle(self, title):
        if self.clear_and_send_keys(self.SCHEDULE_EVENT_TITLE, title) == False:
            writeToLog("INFO","FAILED to insert event title")
            return False
        return True
    
    
    # @Author: Michal Zomper
    def updateorganizer(self, organizer):
        self.send_keys(self.SCHEDULE_EVENT_ORGANIZER, Keys.CONTROL + 'a')
        if self.send_keys(self.SCHEDULE_EVENT_ORGANIZER, organizer) == False:
            writeToLog("INFO","FAILED to change event organizer name")
            return False
        return True
    
    
    # @Author: Michal Zomper
    def updateEventResources(self, resources):
        # remove any resources if their are any
        if self.wait_element(self.SCHEDULE_EDIT_EVENT_PAGE_SELECTED_RESOURCES).text != '':
            tmpResoures = self.get_elements(self.SCHEDULE_EDIT_EVENT_PAGE_DELETE_RESOURCES)
            for resource in tmpResoures:
                if self.clickElement(resource) == False:
                    writeToLog("INFO","FAILED to remove resource")
                    return False
                    
        if self.click(self.SCHEDULE_EVENT_RESOURCES) == False:
            writeToLog("INFO","FAILED to click and open resource option")
            return False
        sleep(1)
        if type(resources) is list: 
            for resource in resources:
                tmpResource = (self.SCHEDULE_EVENT_RESOURCE[0], self.SCHEDULE_EVENT_RESOURCE[1].replace('RESOURCE_NAME', resource.value))
                if self.click(tmpResource) == False:
                    writeToLog("INFO","FAILED to select event resource")
                    return False
        else:
            tmpResource = (self.SCHEDULE_EVENT_RESOURCE[0], self.SCHEDULE_EVENT_RESOURCE[1].replace('RESOURCE_NAME', resources.value))
            if self.click(tmpResource) == False:
                writeToLog("INFO","FAILED to select event resource")
                return False
        
        sleep(2)   
        # click on event title to close the resource list
        self.click(self.SCHEDULE_EDIT_EVENT_PAGE_TITLE)
        return True
    
    
    # @Author: Michal Zomper
    def updateDescription(self, description):
        # Click in Description text box
        if self.click(self.SCHEDULE_EVENT_DESCRIPTION) == False:
            writeToLog("INFO","FAILED to click in description textbox")
            return False
        
        # Enter text Description
        if self.clear_and_send_keys(self.SCHEDULE_EVENT_DESCRIPTION, description) == False:
            writeToLog("INFO","FAILED to type in Description")
            return False
        
        #click to exit description textbox
        self.click(self.SCHEDULE_EDIT_EVENT_PAGE_TITLE, timeout=5)
        return True
    
    
    # @Author: Michal Zomper
    # This function change to date order from ("%d/%m/%Y") to ("%m/%d/%Y")
    def changeDateOrder(self, date):
        tmpDate = date.split("/")
        newDate = tmpDate[1] + "/" + tmpDate[0] + "/" + tmpDate[2]
        return newDate
   
   
    # @Author: Michal Zomper
    # The function publish event to channel / category
    # publishTo - in this parameter will have to were publish to: channel / category
    # categories / channels - in those parameters will have the names of channels/categories name
    # viewEventSeries - if we wont to edit a parameter in event series this parameter need to be True in order to go  viewing an event series. 
    def publishEvent(self, eventInstance, viewEventSeries=False):
        if self.navigateToEventPage(eventInstance, viewEventSeries) == False:
                writeToLog("INFO","FAILED navigate to event page")
                return False
        sleep(1)   
        # Check if 'Copy details from event' check box is checked and if it's check unchecked it 
        # default is that 'Copy details from event' is checked and to open its need to be unchecked
        if self.is_element_checked(self.SCHEDULE_COPE_DETAILS_BUTTON) == True:
            if self.check_element(self.SCHEDULE_COPE_DETAILS_BUTTON, 'True') == False:
                writeToLog("INFO","FAILED to unchecked 'Copy details from event' button")
                return False
        sleep(1)
        self.get_body_element().send_keys(Keys.PAGE_DOWN)
        sleep(3)
        
        if self.click(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 45) == False:
            writeToLog("INFO","FAILED to click on publish button")
            return False
        
        if type(eventInstance.publishTo) is list:
            for category in eventInstance.publishTo:
                if category.lower() == 'category':
                    # Click on Publish in Category
                    if self.click(self.clsCommon.myMedia.MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION, 30) == False:
                        writeToLog("INFO","FAILED to click on Publish in Category")
                        return False
                
                    if self.chooseCategoryToPublishTo(eventInstance.categoryList) == False:
                        writeToLog("INFO","FAILED to choose categories")
                        return False
                    
                elif category.lower() == 'channel':
                    # Click on Publish in Channel
                    if self.click(self.clsCommon.myMedia.MY_MEIDA_PUBLISH_TO_CHANNEL_OPTION, 30) == False:
                        writeToLog("INFO","FAILED to click on Publish in channel")
                        return False
                    
                    if self.chooseCategoryToPublishTo(eventInstance.channelList) == False:
                        writeToLog("INFO","FAILED to choose channels")
                        return False
        else:     
            if eventInstance.publishTo.lower() == 'category':  
                # Click on Publish in Category
                if self.click(self.clsCommon.myMedia.MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION, 30) == False:
                    writeToLog("INFO","FAILED to click on Publish in Category")
                    return False
            
                if self.chooseCategoryToPublishTo(eventInstance.categoryList) == False:
                    writeToLog("INFO","FAILED to choose categories")
                    return False
                
            elif eventInstance.publishTo.lower() == 'channel':
                # Click on Publish in Channel
                if self.click(self.clsCommon.myMedia.MY_MEIDA_PUBLISH_TO_CHANNEL_OPTION, 30) == False:
                    writeToLog("INFO","FAILED to click on Publish in channel")
                    return False
                
                if self.chooseCategoryToPublishTo(eventInstance.channelList) == False:
                    writeToLog("INFO","FAILED to choose channels")
                    return False
        sleep(1)

        if self.click(self.SCHEDULE_SAVE_EVENT, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()

        sleep(3)
        writeToLog("INFO","Success, publish event was successful")
        return True
        
    
    # @Author: Michal Zomper
    # This function only choose the channel/ category that need to publish to    
    def chooseCategoryToPublishTo(self, categories):
        if type(categories) is list:
            # choose all the  channels to publish to
            for category in categories:
                tmpCategoryName = (self.clsCommon.myMedia.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.clsCommon.myMedia.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', category))

                if self.click(tmpCategoryName, 20, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to select published channel '" + category + "'")
                    return False
                
        elif categories != '':
            tmpChannelName = (self.clsCommon.myMedia.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.clsCommon.myMedia.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', categories))

            if self.click(tmpChannelName, 20, multipleElements=True) == False:
                writeToLog("INFO","FAILED to select published channel '" + tmpCategoryName + "'")
                return False
        return True
    
    
    # @Author: Michal Zomper
    # The function adding collaborator to event
    # viewEventSeries - if we wont to edit a parameter in event series this parameter need to be True in order to go  viewing an event series. 
    def addCollaboratorToScheduleEvent(self, eventInstance, location=enums.Location.SCHEDULE_EVENT_PAGE, viewEventSeries=False):
        if self.navigateToEventPage(eventInstance, viewEventSeries) == False:
                writeToLog("INFO","FAILED navigate to event page")
                return False
            
        # Check if 'Copy details from event' check box is checked and if it's check unchecked it 
        # default is that 'Copy details from event' is checked and to open its need to be unchecked
        if self.is_element_checked(self.SCHEDULE_COPE_DETAILS_BUTTON) == True:
            if self.check_element(self.SCHEDULE_COPE_DETAILS_BUTTON, 'True') == False:
                writeToLog("INFO","FAILED to unchecked 'Copy details from event' button")
                return False
            
        if self.clsCommon.editEntryPage.addCollaborator("", eventInstance.collaboratorUser , eventInstance.coEditor, eventInstance.coPublisher, eventInstance.coViewer, location) == False:
            writeToLog("INFO","FAILED adding collaborator to event")
            return False
        
        if self.click(self.SCHEDULE_SAVE_EVENT, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()

        writeToLog("INFO","Success, collaborator was added successfully to event")
        return True