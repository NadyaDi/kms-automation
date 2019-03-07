from selenium.webdriver.common.action_chains import ActionChains
 
 
from base import *
import clsTestService
import enums
from selenium.webdriver.common.keys import Keys
from general import General



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
    SCHEDULE_EVENT_TITLE                                                    = ('xpath', "//input[@id='CreateEvent-eventTitle']")
    SCHEDULE_EVENT_ORGANIZER                                                = ('xpath', "//input[@id='CreateEvent-eventOrganizer']")
    SCHEDUL_EVENT_START_TIME                                                = ('xpath', "//input[@id='rsStartTime-rsStartTime_time']")
    SCHEDUL_EVENT_END_TIME                                                  = ('xpath', "//input[@id='rsEndTime-rsEndTime_time']")
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
    SCHEDULE_RECURRENCE_INTERVAL                                            = ('xpath', "//label[@class='radio' and @for='EventRecurrence-recurrence-'RECURRENCE_INTERVAL']")
    SCHEDULE_RECURRENCE_START_TIME                                          = ('xpath', "//input[@id='EventRecurrence-startTime']")
    SCHEDULE_RECURRENCE_END_TIME                                            = ('xpath', "//input[@id='EventRecurrence-endTime']")
    SCHEDULE_RECURRENCE_START_DATE_CALENDAR                                 = ('xpath', "//input[@id='EventRecurrence-start']")
    SCHEDULE_RECURRENCE_END_DATE_CALENDAR                                   = ('xpath', "//input[@id='EventRecurrence-endby_date']")
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
    
    #=============================================================================================================
    
    # @Author: Michal Zomper 
    def navigateToMySchedule(self, forceNavigate=False):
        # Check if we are already in my media page
        if forceNavigate == False:
            if self.wait_element(self.SCHEDULE_PAGE_TITLE, 5) == True:
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
    def createRescheduleEvent(self, title, startDate, endDate, startTime, endTime, description, tags, CopyDetailsEventToRecording, copeDetailsName='', copeDetailsDescriptio='', copeDetailsTags='', resources='', eventOrganizer='', isRecurrence=False, exitEvent=False):
        if self.createRescheduleEventWithoutRecurrence(title, startDate, endDate, startTime, endTime, description, tags, CopyDetailsEventToRecording, copeDetailsName, copeDetailsDescriptio, copeDetailsTags, resources, copeDetailsName, copeDetailsDescriptio, copeDetailsTags, eventOrganizer, exitEvent) == False:
            writeToLog("INFO","FAILED to create schdule event")
            return False
            
        if isRecurrence == True:
            if self.click(self.SCHEDULE_ADD_RECURRENCE_BUTTON) == False:
                writeToLog("INFO","FAILED to click on add recurrence button")
                return False
            
            
            
            
            
    
    
    # @Author: Michal Zomper 
    # The function create new reschedule event without recurrence
    def createRescheduleEventWithoutRecurrence(self, title, startDate, endDate, startTime, endTime, description, tags, copyDetails, copeDetailsName, copeDetailsDescriptio, copeDetailsTags, resources='', eventOrganizer='', exitEvent=False): 
        if self.navigateToCreateEventPage() == False:
            writeToLog("INFO","FAILED to enter create event page")
            return False
        sleep(2)
        
        if self.send_keys(self.SCHEDULE_EVENT_TITLE, title) == False:
            writeToLog("INFO","FAILED to insert event title")
            return False
            
        if eventOrganizer != '':
            self.send_keys(self.SCHEDULE_EVENT_ORGANIZER, Keys.CONTROL + 'a')
            if self.send_keys(self.SCHEDULE_EVENT_ORGANIZER, eventOrganizer) == False:
                writeToLog("INFO","FAILED to change event organizer name")
                return False
        
        if self.clsCommon.editEntryPage.setScheduleStartDate(startDate) == False:
            writeToLog("INFO","FAILED to set event start date")
            return False
        sleep(2) 
        
        if len(startTime) != 0:
            if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDUL_EVENT_START_TIME, startTime) == False:
                writeToLog("INFO","FAILED to set event start time")
                return False
            sleep(2) 
        # else = use the default value
        
        if self.clsCommon.editEntryPage.setScheduleEndDate(endDate) == False:
            writeToLog("INFO","FAILED to set event end date")
            return False
        sleep(2)  
        # else = use the default value
        
        if len(endTime) != 0:
            if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDUL_EVENT_END_TIME, endTime) == False:
                writeToLog("INFO","FAILED to set event end time")
                return False
            sleep(2)
        
        if resources != '':
            if self.click(self.SCHEDULE_EVENT_RESOURCES) == False:
                writeToLog("INFO","FAILED to click and open resource option")
                return False
            
            if type(resources) is list: 
                for resource in resources:
                    tmpResource = (self.SCHEDULE_EVENT_RESOURCE[0], self.SCHEDULE_EVENT_RESOURCE[1].replace('RESOURCE_NAME', resource.value))
                    if self.click(tmpResource) == False:
                        writeToLog("INFO","FAILED to select event resource")
                        return False
            else:
                tmpResource = (self.SCHEDULE_EVENT_RESOURCE[0], self.SCHEDULE_EVENT_RESOURCE[1].replace('RESOURCE_NAME', resource.value))
                if self.click(tmpResource) == False:
                    writeToLog("INFO","FAILED to select event resource")
                    return False
                
            # click on the create event title to close the resource list
            self.click(self.SCHEDULE_CREATE_EVENT_PAGE_TITLE)
            
        # Click in Description text box
        if self.click(self.SCHEDULE_EVENT_DESCRIPTION) == False:
            writeToLog("INFO","FAILED to click in description textbox")
            return False
        
        # Enter text Description
        if self.clear_and_send_keys(self.SCHEDULE_EVENT_DESCRIPTION, description) == False:
            writeToLog("INFO","FAILED to type in Description")
            return False
        
        if self.fillFileScheduleTags(tags) == False:
            writeToLog("INFO","FAILED to set event tags")
            return False
        
        # copyDetails == False mean that we need to insert new metadata 
        if copyDetails == False:
            if self.click(self.SCHEDULE_COPE_DETAILS_BUTTON) == False:
                writeToLog("INFO","FAILED to uncheck 'Copy details from event to recording' button")
                return False
            
            if self.changeEventDetailsinRecording(copeDetailsName, copeDetailsDescriptio, copeDetailsTags) == False:
                writeToLog("INFO","FAILED to set new metadata in 'Copy details from event to recording' section")
                return False
            
        if exitEvent==False:
            if self.click(self.SCHEDULE_SAVE_EVENT) == False:
                writeToLog("INFO","FAILED click on save event button")
                return False
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_element(self.SCHEDULE_CREATE_EVENT_SUCCESS_MESSAGE) == False:
                writeToLog("INFO","FAILED find event created success message")
                return False
        else:
            if self.click(self.SCHEDULE_SAVE_AND_EXIT_EVENT) == False:
                writeToLog("INFO","FAILED click on save and exit event button")
                return False
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_element(self.SCHEDULE_PAGE_TITLE, 15) == False:
                writeToLog("INFO","FAILED to verify 'My Schedule page' display after clicking on save and exit event button")
                return False
            
        return True
            
            
    # The method supports BOTH single and multiple upload
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillFileScheduleTags(self, tags):
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
    def changeEventDetailsinRecording(self, copeDetailsName='', copeDetailsDescriptio='', copeDetailsTags=''):
        if copeDetailsName != '':
            if self.clear_and_send_keys(self.SCHEDULE_COPE_DETAILS_NAME, copeDetailsName) == False:
                writeToLog("INFO","FAILED to insert new name in 'Copy details from event to recording'")
                return False   
        
        if copeDetailsDescriptio != '':
            # Click in Description text box
            if self.click(self.SCHEDULE_COPE_DETAILS_DESCRIPTION) == False:
                writeToLog("INFO","FAILED to click in description textbox")
                return False
             
            # Enter text Description
            if self.clear_and_send_keys(self.SCHEDULE_COPE_DETAILS_DESCRIPTION, copeDetailsDescriptio) == False:
                writeToLog("INFO","FAILED to insert new description in 'Copy details from event to recording'")
                return False

        if  copeDetailsTags != '':
            if self.clsCommon.upload.fillFileUploadEntryTags(copeDetailsTags) == False:
                writeToLog("INFO","FAILED to insert new tags in 'Copy details from event to recording'")
                return False
            
        return True
    
    
    # recurrenceInterval - this parameter need to be send as an enum- scheduleRecurrenceInterval
    # dailyOption - this parameter need to be send as an enum- scheduleRecurrenceDailyOption
    # dailyDays - if in daily 'every X days' option was chosen this parameter will go the number of days
    # weeklyDays - if weekly was chosen this parameter will go the number of weeks
    # weeklyDaysNames - if weekly was chosen this parameter will have the day or days that the event need to recurrence, this parameter need to be send as an enum- scheduleRecurrenceWeeklyDayOfTheWeek
    # monthlyOption - this parameter need to be send as an enum- scheduleRecurrenceMonthlyOption
    # monthlyDayNumber - this parameter is for the number of day in monthly first option
    # monthlyMonthNumber - this parameter is for the number of month in monthly first and second option
    # monthlyDayName - this parameter is for the day name that in the second monthly option ,this parameter need to be send as an enum- scheduleRecurrenceMonthlyDayOfTheWeek
    def setEventRecurrence(self, recurrenceInterval, dailyOption='', dailyDays='', weeklyDays='', weeklyDaysNames='', monthlyOption, monthlyDayNumber='',  monthlyMonthNumber='', monthlyDayName='' ):
        
        # Choose the needed interval
        tmpRecurrenceInterval = (self.SCHEDULE_RECURRENCE_INTERVAL[0], self.SCHEDULE_RECURRENCE_INTERVAL[1].replace('RECURRENCE_INTERVAL', recurrenceInterval.value))
        if self.click(tmpRecurrenceInterval) == False:
            writeToLog("INFO","FAILED to select recurrence interval: " + recurrenceInterval.value)
            return False
            
        if recurrenceInterval == enums.scheduleRecurrenceInterval.NONE:
            writeToLog("INFO","FAILED to select recurrence interval: " + recurrenceInterval.value)
        
        
        
        elif recurrenceInterval == enums.scheduleRecurrenceInterval.DAYS:
            if dailyOption == enums.scheduleRecurrenceDailyOption.EVERY_X_DAYS:
                if self.click(self.SCHEDULE_RECURRENCE_DAILY_EVERY_X_DAYS_RADIO_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on 'every X days' radio button")
                    return False
                
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_DAILY_EVERY_X_DAYS, dailyDays) == False:
                    writeToLog("INFO","FAILED to add number of days to the 'every X days' option")
                    return False
            
            elif dailyOption == enums.scheduleRecurrenceDailyOption.EVERY_WEEKDAY:
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_WEEKLY_RECUR_EVERY_X_WEEKS, weeklyDays) == False:
                    writeToLog("INFO","FAILED to add number of weeks to the weekly option")
                    return False
                
                  
                        
        elif recurrenceInterval == enums.scheduleRecurrenceInterval.WEEKS: 
            if type(weeklyDaysNames) is list: 
                for dayInTheWeek in weeklyDaysNames:
                    tmpDay = (self.SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK[0], self.SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK[1].replace('DAY_OF_THE_WEEK', dayInTheWeek))
                    if self.click(tmpDay) == False:
                        writeToLog("INFO","FAILED to select day '" + dayInTheWeek.value + "' in weekly option")
                        return False
                        
            else:   
                tmpDay = (self.SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK[0], self.SCHEDULE_RECURRENCE_WEEKLY_DAY_OF_THE_WEEK[1].replace('DAY_OF_THE_WEEK', weeklyDaysNames))
                if self.click(tmpDay) == False:
                    writeToLog("INFO","FAILED to select day '" + weeklyDaysNames.value + "' in weekly option")
                    return False  
                
                
            
        elif recurrenceInterval == enums.scheduleRecurrenceInterval.MONTHS:  
            if monthlyOption == enums.scheduleRecurrenceMonthlyOption.DAY_X_OF_EVERY_Y_MONTHS:
                if self.click(self.SCHEDULE_RECURRENCE_MONTHLY_DAY_X_OF_EVERY_Y_MONTHS_RADIO_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on 'day X of every Y months' radio button")
                    return False
                
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_MONTHLY_BY_DAY_OPTION_DAY_NUMBER, monthlyDayNumber) == False:
                    writeToLog("INFO","FAILED to add number of days to the 'day X of every Y months' option")
                    return False
                    
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_MONTHLY_BY_DAY_OPTION_MONTH_NUMBER, monthlyMonthNumber) == False:
                    writeToLog("INFO","FAILED to add number of month to the 'day X of every Y months' option")
                    return False
            
            
            elif monthlyOption == enums.scheduleRecurrenceMonthlyOption.BY_WEEKDAY:
                if self.click(self.SCHEDULE_RECURRENCE_MONTHLY_BY_WEEKDAY_RADIO_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on 'by weekday' radio button")
                    return False
                
                if self.select_from_combo_by_text(self.SCHEDULE_RECURRENCE_MONTHLY_WEEK_IN_THE_MONTH , 'first') == False:
                    writeToLog("INFO","FAILED to click on 'by weekday' radio button")
                    return False
                    
                if self.select_from_combo_by_text( self.SCHEDULE_RECURRENCE_MONTHLY_DAY_IN_THE_MONTH, monthlyDayName.value) == False:
                    writeToLog("INFO","FAILED to click on 'by weekday' radio button")
                    return False
    
                if self.clear_and_send_keys(self.SCHEDULE_RECURRENCE_MONTHLY_BY_WEEKDAY_OPTION_MONTH_NUMBER  , monthlyMonthNumber) == False:
                    writeToLog("INFO","FAILED to add number of month to the 'day X of every Y months' option")
                    return False
                
        return True
    
    
    
    def setRecurrenceRange(self, reccurenceStartDate, reccurenceEndDate, reccurenceStartTime, reccurenceEndTime): 
        if self.setRecurrenceStartDate(reccurenceStartDate) == False:
            writeToLog("INFO","FAILED to set event start date")
            return False
        sleep(2) 
        
        if self.setRecurrenceEndDate(reccurenceEndDate) == False:
            writeToLog("INFO","FAILED to set event end date")
            return False
        sleep(2)  
        
        if len(reccurenceStartTime) != 0:
            if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_RECURRENCE_START_TIME, reccurenceStartTime) == False:
                writeToLog("INFO","FAILED to set event start time")
                return False
            sleep(2) 
        
        if len(reccurenceEndTime) != 0:
            if self.clsCommon.editEntryPage.setScheduleTime(self.SCHEDULE_RECURRENCE_END_TIME, reccurenceEndTime) == False:
                writeToLog("INFO","FAILED to set event end time")
                return False
            sleep(2)
        
        return True
        
    
    # Format desteStr - '24/01/2018'
    # startOrEnd - String 'start' or 'end'
    def setRecurrenceStartDate(self, dateStr):
        return self.setRecurrenceScheduleDate(dateStr, 'start')
    
    
    def setRecurrenceEndDate(self, dateStr):
        return self.setRecurrenceScheduleDate(dateStr, 'end')
        
       
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