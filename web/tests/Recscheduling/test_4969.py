import time, pytest, datetime
from datetime import datetime
import sys,os
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
    # Test Name : Recscheduling - Delete an occurrence 
    # Test description:
    #    1. Login with Rescheduling admin user
    #    2. Click on my schedule > create event
    #    3. Fill in all fields :start/end date, start,end, time, description ,tags, rcurrence(new recurring event - Daily - Every X day) and select a resource
    #    4. Click save and exit
    #    5. Go to my schedule page and verify that all events display with the correct date and time
    #    6. From my schedule page enter one event and delete only this event  
    #    7. Go to my schedule page and verify that only the event that was chosen deleted and the rest of events are still display
    #
    #    1-7. The event is created successfully and appears on the agenda view
    #================================================================================================================================
    testNum = "4969"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    eventTitle = None
    description = "Description"
    tags = "Tags, schedule,"
    startDate = None
    endDate = None
    startEventTime = None
    endTime = None
    resource = enums.RecschedulingResourceOptions.AUTOMATION_ROOM
    numberOfRecurrenceDays = 6
    resourceEveryXDays = 2 
    
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
            self.eventTitle = clsTestService.addGuidToString("Create event series", self.testNum)
            self.editEventTitle = clsTestService.addGuidToString("Edit event series", self.testNum)
            
            
            self.startDateInDatetimeFormat = (datetime.datetime.now())
            self.startDateForCreateEvent = self.startDateInDatetimeFormat.strftime("%d/%m/%Y")
            
            self.endDate = (datetime.datetime.now() + timedelta(days=self.numberOfRecurrenceDays)).strftime("%d/%m/%Y")

            self.startEventTime = time.time() + 1.5*(60*60)
            self.startEventTime = time.strftime("%I:%M %p",time.localtime(self.startEventTime))
            
            self.endTime = time.time() + 2*(60*60)
            self.endTime = time.strftime("%I:%M %p",time.localtime(self.endTime))
            
            self.event = SechdeuleEvent(self.eventTitle, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags, "True")
            
            self.event.resources = self.resource
            self.event.expectedEvent = False
            self.event.isRecurrence = True
            self.event.recurrenceInterval = enums.scheduleRecurrenceInterval.DAYS
            self.event.dailyOption =  enums.scheduleRecurrenceDailyOption.EVERY_X_DAYS
            self.event.dailyDays = self.resourceEveryXDays
            self.event.endDateOption = enums.scheduleRecurrenceEndDateOption.END_BY
            
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
            
            self.tmpStartDate = self.event.startDate
            self.tmpStartDateFormat = self.event.verifyDateFormat
            writeToLog("INFO","Step 4: Going to verify event display in my schedule page")
            for day in range(0,self.numberOfRecurrenceDays+1):
                self.event.startDate = (self.startDateInDatetimeFormat + timedelta(days=day)).strftime("%d/%m/%Y")
                self.event.convertDatetimeToVerifyDate()
                self.event.expectedEvent = not(self.event.expectedEvent)
                
                if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                    if self.event.expectedEvent == True:
                        writeToLog("INFO","Step 4: FAILED to verify event in my schedule page for date: " + self.event.startDate)
                        return
                    elif self.event.expectedEvent == False:
                        writeToLog("INFO","Step 4: FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it shouldn't")
                        return
            
            self.event.startDate = self.tmpStartDate
            self.event.convertDatetimeToVerifyDate()
            writeToLog("INFO","Step 5: Going to delete an event occurrence, delete the first event in the series")
            if self.common.recscheduling.deteteEvent(self.event) == False:
                writeToLog("INFO","Step 5: FAILED to delete an event occurrence, delete the first event in the series")
                return 
            sleep(3)
            
            writeToLog("INFO","Step 6: Going to verify that only the first occurrence of the event series was deleted")
            self.event.expectedEvent = False
            self.numberOfDaysSinceEventDispaly = 1
            for day in range(0,self.numberOfRecurrenceDays+1):
                self.event.startDate = (self.startDateInDatetimeFormat + timedelta(days=day)).strftime("%d/%m/%Y")
                self.event.convertDatetimeToVerifyDate()
                
                if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                    if self.event.expectedEvent == True:
                        writeToLog("INFO","Step 6: FAILED to verify event in my schedule page for date: " + self.event.startDate)
                        return
                    elif self.event.expectedEvent == False:
                        writeToLog("INFO","Step 6: FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it shouldn't")
                        return
                
                # the first event in the series was deleted and after it the event series stay the same so we need to make sure that the first occurrence will be in the 3 day after the series started 
                if self.numberOfDaysSinceEventDispaly < 2:
                    self.numberOfDaysSinceEventDispaly = self.numberOfDaysSinceEventDispaly + 1
                    self.event.expectedEvent = False
                else:
                    self.numberOfDaysSinceEventDispaly = self.numberOfDaysSinceEventDispaly + 1
                    self.event.expectedEvent = not(self.event.expectedEvent)
                    
                
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Rescheduling -  Delete an occurrence ' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.event.startDate = self.endDate
            self.event.convertDatetimeToVerifyDate() 
            self.common.recscheduling.deteteEvent(self.event, viewEventSeries=True)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')