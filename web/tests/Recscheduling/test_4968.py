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
    # Test Name : Recscheduling - Create event with resource conflict
    # Test description:
    #    1. Enter to my schedule > create event
    #    2. Fill in all fields: title , start/end date, start/and time ,description ,tags and select a resource
    #    3. Click save and exit
    #    4. Go to my schedule page and verify that the event display in the correct date and time
    #    5. Enter to my schedule > create another event
    #    6. Fill in all fields: title,description ,tags.
    #    7. Fill the parameters :start/end date, start/and time and select a resource with the same details as in the preview event (step 2) 
    #    8. A conflict message display that say the the resource for the second event is unavailable since is already use at this current time with the first event   
    
    #    1-8. Conflict message appears 
    #================================================================================================================================
    testNum = "4968"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    eventTitle1 = None
    eventTitle2 = None
    description = "Description"
    tags = "Tags,"
    startDate = None
    endDate = None
    startEventTime = None
    endTime = None
    resource = enums.RecschedulingResourceOptions.FALL_CONFERENCE_ROOM
    
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
            self.eventTitle1 = clsTestService.addGuidToString("new single event", self.testNum)
            self.eventTitle2 = clsTestService.addGuidToString("new event with resource conflict", self.testNum)
            
            self.startDateForCreateEvent = datetime.datetime.now().strftime("%d/%m/%Y")
            self.endDate = datetime.datetime.now().strftime("%d/%m/%Y")

            self.startEventTime = time.time() + (60*60)
            self.startEventTime = time.strftime("%I:%M%p",time.localtime(self.startEventTime))
             
            self.endTime = time.time() + 2*(60*60)
            self.endTime = time.strftime("%I:%M%p",time.localtime(self.endTime))
            self.event1 = SechdeuleEvent(self.eventTitle1, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags, "True")
            self.eventWithConflict = SechdeuleEvent(self.eventTitle2, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags, "True")
            self.event1.resources = self.resource
            self.eventWithConflict.resources = self.resource
            
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
            if self.common.recscheduling.createRescheduleEvent(self.event1) == False:
                writeToLog("INFO","Step 3: FAILED to create new single event")
                return
            
            sleep(3)     
            writeToLog("INFO","Step 4: Going to verify event display in my schedule page")
            if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event1) == False:
                writeToLog("INFO","Step 4: FAILED to verify event in my schedule page")
                return
            
            sleep(3)
            writeToLog("INFO","Step 5: Going to create new single event")
            if self.common.recscheduling.createRescheduleEvent(self.eventWithConflict) == True:
                writeToLog("INFO","Step 5: FAILED, event was create although their is a conflict with resource")
                return
            writeToLog("INFO","Step 5: As expected event '" + self.event1.title + "' wasn't created")
            
            writeToLog("INFO","Step 6: Going to check if a conflict pop up display after fail to create event")
            conflictMessageElement =  self.common.base.wait_element(self.common.recscheduling.SCHEDULE_CONFLICT_POP_UP_MESSAGE)
            if conflictMessageElement != False:
                if ("Error: Resource Conflict" in conflictMessageElement.text) == False:
                    writeToLog("INFO","Step 6: FAILED, conflict error title message isn't display")
                    return
                conflictMessageText = self.event1.title + ", " + \
                                        self.common.recscheduling.changeDateOrder(self.event1.startDate) + " " + \
                                        self.event1.startTime.lower() + "-" + \
                                        self.event1.endTime.lower() + "\n" + \
                                        self.event1.resources.value
                                        
                if (conflictMessageText in conflictMessageElement.text) == False:
                    writeToLog("INFO","Step 6: FAILED, conflict error message doesn't show the correct conflict that need to be with event: " + self.event1.title)
                    return
            else:
                writeToLog("INFO","Step 6: FAILED, conflict message was not found")
                return
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Rescheduling - Create event with resource conflict' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            # click on the ok conflict button in order to continue with the delete
            sleep(1)
            self.common.base.click(self.common.recscheduling.SCHEDULE_CONFLICT_POP_UP_MESSAGE_OK_BUTTON)
            sleep(1)
            self.common.recscheduling.navigateToMySchedule(forceNavigate=True)
            self.common.recscheduling.deteteEvent(self.event1)
            self.common.recscheduling.deteteEvent(self.eventWithConflict)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')