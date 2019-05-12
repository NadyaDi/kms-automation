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
    # Test Name : Recscheduling - Delete Event Series
    # Test description:
    #    1. Create event series
    #    2. enter on of the event >  go to the series page > click on delete series
    #    3. Go to my schedule and verify that all the event series was delete

    #================================================================================================================================
    testNum = "5162"
    
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
    munberOfRecurrenceDays = 8
    resource = enums.RecschedulingResourceOptions.MAIN_STUDENT_LOUNGE
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
            self.eventTitle = clsTestService.addGuidToString("Create recurring event-Daily-Every X days", self.testNum)
            
            self.startTimeInDatetimeFormat = datetime.datetime.now()
            self.startDateForCreateEvent = self.startTimeInDatetimeFormat.strftime("%d/%m/%Y")
            self.endDate = (datetime.datetime.now() + timedelta(days=self.munberOfRecurrenceDays)).strftime("%d/%m/%Y")

            self.startEventTime = time.time() + 0.5*(60*60)
            self.startEventTime = time.strftime("%I:%M %p",time.localtime(self.startEventTime))
             
            self.endTime = time.time() + (60*60)
            self.endTime = time.strftime("%I:%M %p",time.localtime(self.endTime))
            
            self.event = SechdeuleEvent(self.eventTitle, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags,"False")
            self.event.expectedEvent = False
            self.event.resources = self.resource
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
            sleep(3)
            
            self.tmpStartDate = self.event.startDate
            self.tmpStartDateFormat = self.event.verifyDateFormat
            writeToLog("INFO","Step 4: Going to verify event display in my schedule page")
            for day in range(0,self.munberOfRecurrenceDays+1):
                self.event.startDate = (self.startTimeInDatetimeFormat + timedelta(days=day)).strftime("%d/%m/%Y")
                self.event.convertDatetimeToVerifyDate()
                self.event.expectedEvent = not(self.event.expectedEvent)
                
                if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                    if self.event.expectedEvent == True:
                        writeToLog("INFO","Step 4: FAILED to verify event in my schedule page for date: " + self.event.startDate)
                        return
                    elif self.event.expectedEvent == False:
                        writeToLog("INFO","Step 4: FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it shouldn't")
                        return
            
            writeToLog("INFO","Step 5: Going to delete event series")
            if self.common.recscheduling.deteteEvent(self.event, viewEventSeries=True) == False:
                writeToLog("INFO","Step 5: FAILEDto delete event series")
                return
                
            writeToLog("INFO","Step 6: Going to verify that all event series occurrence were deleted")
            self.event.startDate = self.tmpStartDate
            self.event.verifyDateFormat = self.tmpStartDateFormat
            for day in range(0,self.munberOfRecurrenceDays+1):
                self.event.startDate = (self.startTimeInDatetimeFormat + timedelta(days=day)).strftime("%d/%m/%Y")
                self.event.convertDatetimeToVerifyDate()
                self.event.expectedEvent = False
                
                if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                    writeToLog("INFO","Step 6: FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it was deleted")
                    return

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Rescheduling -  Delete Event Series' was done successfully")
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