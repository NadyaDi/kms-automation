import time, pytest, datetime
from datetime import datetime
import sys,os
from calendar import week
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
from recscheduling import SechdeuleEvent

class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : Recscheduling - Create new recurring event - Weekly - Every X weeks
    # Test description:
    #    1. Click on my schedule > create series of  event
    #    2. Fill in all fields :start/end date, start/end time, description ,tags, rcurrence(new recurring event - Daily -Every weekday) and select a resource
    #    3. Click save and exit
    #        * this is what we are testing : Every weekday for 9 days (event do NOT need to display on the weekend: saturday or sunday)
    #    4. Click save and exit
    #    5. Go to my schedule page and verify that the event display only on the weekday (and not on  weekend: saturday or sunday) with  the correct date and time
    #    6. Go to the first weekday after the event ended and verify that the event doesn't  display
    #
    #    1-6. All the event recurrence are created successfully and appears on the agenda view

    #================================================================================================================================
    testNum = "4964"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    eventTitle = None
    description = "Description"
    tags = "Tags,"
    startDate = None
    endDate = None
    startEventTime = None
    endTime = None
    resource = enums.RecschedulingResourceOptions.SUMMER_CONFERENCE_ROOM
    numberOfRecurrenceWeeks = 2
    
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.eventTitle = clsTestService.addGuidToString("recurring event-Weekly-Every X weeks", self.testNum)
            
            self.startDateInDatetimeFormat = datetime.datetime.now()
            self.startDateForCreateEvent = self.startDateInDatetimeFormat.strftime("%d/%m/%Y")
            
            self.endDate = (datetime.datetime.now() + timedelta(week=self.numberOfRecurrenceWeeks)).strftime("%d/%m/%Y")
            
            self.startEventTime = time.time() + 2*(60*60)
            self.startEventTime = time.strftime("%I:%M %p",time.localtime(self.startEventTime))
             
            self.endTime = time.time() + 3.5*(60*60)
            self.endTime = time.strftime("%I:%M %p",time.localtime(self.endTime))
            
            self.event = SechdeuleEvent(self.eventTitle, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags,"False")
            
            self.event.resources = self.resource
            self.event.isRecurrence = True
            self.event.recurrenceInterval = enums.scheduleRecurrenceInterval.WEEKS
            self.event.weeklyWeeks = self.numberOfRecurrenceWeeks
            self.event.endDateOption = enums.scheduleRecurrenceEndDateOption.END_AFTER_X_OCCURRENCES
            self.event.numberOfRecurrence = self.numberOfRecurrence
            
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to set rescheduling in admin")
            if self.common.admin.enableRecscheduling(True) == False:
                writeToLog("INFO","Step 1: FAILED set rescheduling in admin")
                return
                
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
              
            writeToLog("INFO","Step 3: Going to create new single event")
            if self.common.recscheduling.createRescheduleEvent(self.event) == False:
                writeToLog("INFO","Step 3: FAILED to create new single event")
                return
            sleep(3)
            
            self.tmpStartDate = self.event.startDate
            self.tmpStartDateFormat = self.event.verifyDateFormat
            self.NumberOfDisplayEventsFromStartDay = 0
            writeToLog("INFO","Step 4: Going to verify event display in my schedule page")
            for day in range(0,self.numberOfDaysForEvent):
                dayInTheWeek = (self.startDateInDatetimeFormat + timedelta(days=day)).strftime("%A").lower()
                if dayInTheWeek.lower() != (enums.scheduleRecurrenceDayOfTheWeek.SATURDAY.value).lower() and \
                   dayInTheWeek.lower() != (enums.scheduleRecurrenceDayOfTheWeek.SUNDAY.value).lower():
                    self.event.expectedEvent = True
                    self.NumberOfDisplayEventsFromStartDay = self.NumberOfDisplayEventsFromStartDay + 1
                else:  #day is saturday or sunday
                    self.event.expectedEvent = False
                
                self.event.startDate = (self.startDateInDatetimeFormat + timedelta(days=day)).strftime("%d/%m/%Y")
                self.event.convertDatetimeToVerifyDate()
                
                if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                    if self.event.expectedEvent == True:
                        writeToLog("INFO","Step 4: FAILED to verify event in my schedule page for date: " + self.event.startDate)
                        return
                    elif self.event.expectedEvent == False:
                        writeToLog("INFO","Step 4: FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it shouldn't")
                        return
        
            if self.NumberOfDisplayEventsFromStartDay != self.event.numberOfRecurrence:
                writeToLog("INFO","Step 4: FAILED, the event display '"+ self.displayEventFromStartDay + "' times although it should appear '" + self.event.numberOfRecurrence + "' times")
                return
                
            writeToLog("INFO","Step 5: Going to verify that event isn't display in after all events recurrence are over")
            # need to check that the day after the event end isn't saturday or sunday and if it is we need to look for the next monday to check that the event isn't display any more
            for day in range(0,3):
                dayInTheWeek = (self.startDateInDatetimeFormat + timedelta(days=(self.numberOfDaysForEvent+day))).strftime("%A").lower()
                if dayInTheWeek.lower() != (enums.scheduleRecurrenceDayOfTheWeek.SATURDAY.value).lower() and \
                   dayInTheWeek.lower() != (enums.scheduleRecurrenceDayOfTheWeek.SUNDAY.value).lower():
                    self.event.startDate = (self.startDateInDatetimeFormat + timedelta(days=self.numberOfDaysForEvent+day)).strftime("%d/%m/%Y")
                    self.event.convertDatetimeToVerifyDate()
                    self.event.expectedEvent = False
                    if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                        writeToLog("INFO","Step 4: FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it shouldn't")
                        return
                    break
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Rescheduling - Create new recurring event - Daily - Every X days' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            self.event.startDate = self.tmpStartDate
            self.event.verifyDateFormat = self.tmpStartDateFormat
            self.common.recscheduling.deteteEvent(self.event, viewEventSeries=True)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')