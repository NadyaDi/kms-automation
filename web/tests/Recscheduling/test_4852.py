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


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : Rescheduling - Create new single event
    # Test description:
    #    1. Login with Rescheduling admin user
    #    2. Click on my schedule > create event
    #    3. Fill in all fields (description ,tags ) and select a resource
    #    4. Select start and end time
    #    5. Click save and exit
    #    6. Enter the event > click delete
    #    7. Click yes on pop up message
    #
    #    1-5. The event is created successfully and appears on the agenda view
    #    6-8. Event will be deleted

    #================================================================================================================================
    testNum = "4852"
    
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
    resource = enums.RecschedulingResourceOptions.AUTOMATION_ROOM
    
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
            self.eventTitle = clsTestService.addGuidToString("Create new single event", self.testNum)
            
            # we have 2 startDate that hold the same day for the event. one in format to create the event and the second one is in format so we can compare it to the date in the calendar
            self.startDateForCreateEvent = datetime.datetime.now().strftime("%d/%m/%Y")
            self.startDateToVerifyEventIncalender = datetime.datetime.now().strftime("%B %d, %Y - %A")
            self.endDate = datetime.datetime.now().strftime("%d/%m/%Y")

            self.startEventTime = time.time() + (60*60)
            self.startEventTime = time.strftime("%I:%M%p",time.localtime(self.startEventTime))
             
            self.endTime = time.time() + 2*(60*60)
            self.endTime = time.strftime("%I:%M%p",time.localtime(self.endTime))

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
            if self.common.recscheduling.createRescheduleEvent(self.eventTitle, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags, True, resources=self.resource, exitEvent=True) == False:
                writeToLog("INFO","Step 3: FAILED to create new single event")
                return
                 
            writeToLog("INFO","Step 4: Going to verify event display in my schedule page")
            if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.eventTitle, self.startDateToVerifyEventIncalender, self.endDate, self.startEventTime, self.endTime, self.resource) == False:
                writeToLog("INFO","Step 4: FAILED to create new single verify event display in my schedule page")
                return
            
            writeToLog("INFO","Step 5: Going to delete event")
            if self.common.recscheduling.deteteSingleEvent(self.eventTitle, self.startDateToVerifyEventIncalender) == False:
                writeToLog("INFO","Step54: FAILED to delete event from my schedule page")
                return
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Rescheduling - Create new single event' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            self.common.recscheduling.deteteSingleEvent(self.eventTitle, self.startDateToVerifyEventIncalender)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')