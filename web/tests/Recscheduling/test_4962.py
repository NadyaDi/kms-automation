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
    # Test Name : Recscheduling - Create new recurring event - Daily - Every X days
    # Test description:
    #    1. Login with Rescheduling admin user
    #    2. Click on my schedule > create event
    #    3. Fill in all fields (description ,tags ) and select a resource
    #    4. Select start and end time
    #    5. Click on the recurrence button
    #        4.1. Select daily > Every X days 
    #        * this is what we are testing : Every 2 days for 10 days
    #    6. Click save and exit
    #    7. Go to my schedule page and verify that the event display in the correct date and time
    #        7.1 Check that all the event recurrence display in the correct date
    #    8. Enter on of the event recurrence > click delete all recurrence
    #
    #    1-6. All the event recurrence are created successfully and appears on the agenda view
    #    7-8. All event recurrence were deleteded

    #================================================================================================================================
    testNum = "4962"
    
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
    munberOfRecurrenceDays = 10
    resource = enums.RecschedulingResourceOptions.MAIN_STUDENT_LOUNGE
    
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

            self.startEventTime = time.time() + (60*60)
            self.startEventTime = time.strftime("%I:%M %p",time.localtime(self.startEventTime))
             
            self.endTime = time.time() + 3.5*(60*60)
            self.endTime = time.strftime("%I:%M %p",time.localtime(self.endTime))
            self.event = SechdeuleEvent(self.eventTitle, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags,"False")
            self.event.expectedEvent = False
            self.event.resources = self.resource
            self.event.isRecurrence = True
            self.event.recurrenceInterval = enums.scheduleRecurrenceInterval.DAYS
            self.event.dailyOption =  enums.scheduleRecurrenceDailyOption.EVERY_X_DAYS
            self.event.dailyDays = self.munberOfRecurrenceDays
            self.event.endDateOption = enums.scheduleRecurrenceEndDateOption.END_AFTER_X_OCCURRENCES
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
#             writeToLog("INFO","Step 1: Going to set rescheduling in admin")
#             if self.common.admin.enableRecscheduling(True) == False:
#                 writeToLog("INFO","Step 1: FAILED set rescheduling in admin")
#                 return
#              
#             writeToLog("INFO","Step 2: Going navigate to home page")            
#             if self.common.home.navigateToHomePage(forceNavigate=True) == False:
#                 writeToLog("INFO","Step 2: FAILED navigate to home page")
#                 return
             
            writeToLog("INFO","Step 3: Going to create new single event")
            if self.common.recscheduling.createRescheduleEvent(self.event) == False:
                writeToLog("INFO","Step 3: FAILED to create new single event")
                return
            sleep(3)
            
            for day in range(0,self.munberOfRecurrenceDays):
                self.event.startDate = (self.startTimeInDatetimeFormat + timedelta(days=day)).strftime("%d/%m/%Y")
                self.event.convertDatetimeToVerifyDate()
                self.event.expectedEvent = not(self.event.expectedEvent)
                  
                writeToLog("INFO","Step "+ str(day+1) + ": Going to verify event display in my schedule page")
                if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                    if self.event.expectedEvent == True:
                        writeToLog("INFO","Step "+ str(day+1) + ": FAILED to verify event in my schedule page for date: " + self.event.startDate)
                        return
                    elif self.event.expectedEvent == False:
                        writeToLog("INFO","Step "+ str(day+1) + ": FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it shouldn't")
                        return
            
            
            sleep(3)
            writeToLog("INFO","Step "+ str(day+1) + ": Going to delete event")
            if self.common.recscheduling.deteteSingleEvent(self.event) == False:
                writeToLog("INFO","Step "+ str(day+1) + ":: FAILED to delete event from my schedule page")
                return
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
            self.common.recscheduling.deteteSingleEvent(self.event)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')