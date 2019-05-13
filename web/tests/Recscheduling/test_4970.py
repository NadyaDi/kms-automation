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
    # Test Name : Recscheduling - Edit Single event
    # Test description:
    #    1. Login with Rescheduling admin user
    #    2. Click on my schedule > create event
    #    3. Fill in all fields (start/end date, start/end time, description ,tags ) and select a resource
    #    4. Click save and exit
    #    5. Go to my schedule page and verify that the event display in the correct date and time
    #    6. From my schedule page enter the event and edit the following fields: 
    #       title, description, tags ,resource, Event organizer, add Collaborators, time , date, and publish the event
    #    7. go to the original start date and verify that the event doesn't display
    #    8. Go to my schedule page and verify that the event details was changed.
    #
    #    1-8. The event is created successfully and appears on the agenda view
    #================================================================================================================================
    testNum = "4970"
    
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
    publishTo = 'category'
    category = "Apps Automation Category"
    
    editDescription = "Edit Description"
    editTags = "Edit Tags, schedule,"
    editResources = [enums.RecschedulingResourceOptions.QA_APP_ROOM, enums.RecschedulingResourceOptions.MAIN_STUDENT_LOUNGE]
    editOrganizer = 'Automation_User_1' 
    userId = 'AutomationUser8'
    
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
            self.eventTitle = clsTestService.addGuidToString("Create single event", self.testNum)
            self.editEventTitle = clsTestService.addGuidToString("Edit single event", self.testNum)
            
            self.startDateForCreateEvent = datetime.datetime.now().strftime("%d/%m/%Y")
            self.editStartDate = (datetime.datetime.now() + timedelta(days=2)).strftime("%d/%m/%Y")
            self.endDate = datetime.datetime.now().strftime("%d/%m/%Y")
            self.editEndDate = (datetime.datetime.now() + timedelta(days=2)).strftime("%d/%m/%Y")

            self.startEventTime = time.time() + (60*60)
            self.startEventTime = time.strftime("%I:%M %p",time.localtime(self.startEventTime))

            
            self.editStartEventTime = time.time() + 3*(60*60)
            self.editStartEventTime = time.strftime("%I:%M %p",time.localtime(self.editStartEventTime))
            tmpTime = self.editStartEventTime.split(":")
            tmpHour = int(tmpTime[0])
            tmpHour = str(tmpHour)
            self.editStartEventTime = tmpHour + ":" + tmpTime[1]
            
            self.endTime = time.time() + 2*(60*60)
            self.endTime = time.strftime("%I:%M %p",time.localtime(self.endTime))

            
            self.editEndTime = time.time() + 4*(60*60)
            self.editEndTime = time.strftime("%I:%M %p",time.localtime(self.editEndTime))
            tmpTime = self.editEndTime.split(":")
            tmpHour = int(tmpTime[0])
            tmpHour = str(tmpHour)
            self.editEndTime = tmpHour + ":" + tmpTime[1]
            
            self.event = SechdeuleEvent(self.eventTitle, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags, "True")
            self.event.resources = self.resource
            self.event.fieldsToUpdate = ["title", "Organizer","startDate", "endDate", "startTime", "endTime", "description", "tags", "resources"]

            
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
            
            writeToLog("INFO","Step 4: Going to verify event metadata")
            if self.common.recscheduling.VerifyEventDeatailsInEventPage(self.event) == False:
                writeToLog("INFO","Step 4: FAILED to verify event metadata in event page")
                return
            
            writeToLog("INFO","Step 5: Going navigate to event page")
            if self.common.recscheduling.navigateToEventPage(self.event) == False:
                writeToLog("INFO","Step 5: FAILED navigate to event")
                return 
            sleep(2)
            
            self.event.title = self.editEventTitle
            self.event.startDate = self.editStartDate
            self.event.convertDatetimeToVerifyDate()
            self.event.endDate = self.editEndDate
            self.event.startTime = self.editStartEventTime
            self.event.endTime = self.editEndTime
            self.event.description = self.editDescription
            self.event.tags = self.editTags
            self.event.organizer = self.editOrganizer
            self.event.resources = self.editResources
            self.event.collaboratorUser = self.userId
            self.event.coEditor = True
            self.event.coPublisher = False
            self.event.publishTo = self.publishTo
            self.event.categoryList = self.category
            
            sleep(3)     
            writeToLog("INFO","Step 6: Going to verify event display in my schedule page")
            if self.common.recscheduling.editRescheduleEvent(self.event) == False:
                writeToLog("INFO","Step 6: FAILED to edit event metadata")
                return
            
            sleep(3)
            writeToLog("INFO","Step 7: Going to publish event")
            if self.common.recscheduling.publishEvent(self.event) == False:
                writeToLog("INFO","Step 7: FAILED to publish event")
                return
            
            writeToLog("INFO","Step 8: Going to add collaborator to event")
            if self.common.recscheduling.addCollaboratorToScheduleEvent(self.event, location=enums.Location.SCHEDULE_EVENT_PAGE) == False:
                writeToLog("INFO","Step 8: FAILED adding collaborator to event")
                return
            sleep(3)
            
            self.event.startDate = self.startDateForCreateEvent
            self.event.convertDatetimeToVerifyDate()
            self.event.expectedEvent = False
            writeToLog("INFO","Step 9: Going to verify that event does not display in the original start date")
            if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                writeToLog("INFO","Step 9:FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it shouldn't")
                return
            
            self.event.startDate = self.editStartDate
            self.event.convertDatetimeToVerifyDate()
            writeToLog("INFO","Step 10: Going to verify event metadata")
            if self.common.recscheduling.VerifyEventDeatailsInEventPage(self.event) == False:
                writeToLog("INFO","Step 10: FAILED to verify event metadata in event page")
                return
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Rescheduling - Edit Single event' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            if self.common.recscheduling.deteteEvent(self.event) == False:
                self.event.startDate =self.startDateForCreateEvent
                self.event.convertDatetimeToVerifyDate()
                self.event.title = self.eventTitle
                self.common.recscheduling.deteteEvent(self.event)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')