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
    # Test Name : Recscheduling - Edit an occurrence 
    # Test description:
    #    1. Enter to my schedule > create event
    #    3. Fill in all fields :start/end date, start,end, time, description ,tags, rcurrence(new recurring event - Daily - Every X day) and select a resource
    #    4. Click save and exit
    #    5. Go to my schedule page and verify that all events display with the correct date and time
    #    6. From my schedule page enter one event and edit his metadata: start/end date, start,end, time, description ,tags, rcurrence
    #    7. Go to my schedule page and verify that only the event that was change is realy changed
    #
    #    1-7. The event is created successfully and appears on the agenda view
    #================================================================================================================================
    testNum = "4972"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    eventTitle = None
    description = "Description"
    tags = "Tags,"
    editDescription = "Edit Description"
    editTags = "Edit Tags,"
    startDate = None
    endDate = None
    startEventTime = None
    endTime = None
    seriesResource = enums.RecschedulingResourceOptions.AUTOMATION_ROOM
#     occurrenceEventEditResource = enums.RecschedulingResourceOptions.SUMMER_CONFERENCE_ROOM
    numberOfRecurrenceDays = 6
    recurrenceEveryXDays = 2 
    
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
            self.occurrenceEventTitle = clsTestService.addGuidToString("Edit event occurrence", self.testNum)
            
            
            self.startDateInDatetimeFormat = (datetime.datetime.now())
            self.startDateForCreateEvent = self.startDateInDatetimeFormat.strftime("%d/%m/%Y")
            
            self.endDate = (datetime.datetime.now() + timedelta(days=self.numberOfRecurrenceDays)).strftime("%d/%m/%Y")
            
            self.occurrenceEventEditStartDate = (datetime.datetime.now() + timedelta(days=self.numberOfRecurrenceDays+2)).strftime("%d/%m/%Y")
            self.occurrenceEventEditEndDate = (datetime.datetime.now() + timedelta(days=self.numberOfRecurrenceDays+2)).strftime("%d/%m/%Y")
            
            self.startEventTime = time.time() + 1.5*(60*60)
            self.startEventTime = time.strftime("%I:%M %p",time.localtime(self.startEventTime))
            
            self.endTime = time.time() + 2*(60*60)
            self.endTime = time.strftime("%I:%M %p",time.localtime(self.endTime))
            
            self.occurrenceEventEditStartTime = time.time() + (60*60)
            self.occurrenceEventEditStartTime = time.strftime("%I:%M %p",time.localtime(self.occurrenceEventEditStartTime))
            
            self.occurrenceEventEditEndTime = time.time() + 1.5*(60*60)
            self.occurrenceEventEditEndTime = time.strftime("%I:%M %p",time.localtime(self.occurrenceEventEditEndTime))
            
            self.event = SechdeuleEvent(self.eventTitle, self.startDateForCreateEvent, self.endDate, self.startEventTime, self.endTime, self.description, self.tags, "True")
            self.event.resources = self.seriesResource
            self.event.expectedEvent = False
            self.event.isRecurrence = True
            self.event.recurrenceInterval = enums.scheduleRecurrenceInterval.DAYS
            self.event.dailyOption =  enums.scheduleRecurrenceDailyOption.EVERY_X_DAYS
            self.event.dailyDays = self.recurrenceEveryXDays
            self.event.endDateOption = enums.scheduleRecurrenceEndDateOption.END_BY
            
            self.occurrenceEvent = SechdeuleEvent(self.occurrenceEventTitle, self.occurrenceEventEditStartDate, self.occurrenceEventEditEndDate, self.occurrenceEventEditStartTime, self.occurrenceEventEditEndTime, self.editDescription, self.editTags, "True")
#             self.occurrenceEvent.resources= self.occurrenceEventEditResource
            #self.occurrenceEvent.fieldsToUpdate = ["title", "tags", "description", "resources", "startDate", "endDate", "startTime", "endTime"]
            self.occurrenceEvent.fieldsToUpdate = ["title", "tags", "description", "startDate", "endDate", "startTime", "endTime"]
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to set rescheduling in admin")
            if self.common.admin.enableRecscheduling(True) == False:
                writeToLog("INFO","Step 1: FAILED set rescheduling in admin")
                return
                 
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
             
            writeToLog("INFO","Step 3: Going to create event series")
            if self.common.recscheduling.createRescheduleEvent(self.event) == False:
                writeToLog("INFO","Step 3: FAILED to create new single event")
                return
            
            self.tmpStartDate = self.event.startDate
            self.tmpEndDate = self.event.endDate
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
            sleep(2)
            
            # the evenet that we will edit is the event in the end date        
            self.event.startDate = self.event.endDate  
            self.event.convertDatetimeToVerifyDate()   
            writeToLog("INFO","Step 5: Going navigate to event page")
            if self.common.recscheduling.navigateToEventPage(self.event) == False:
                writeToLog("INFO","Step 5: FAILED navigate to event")
                return 
            sleep(2)

            writeToLog("INFO","Step 6: Going to edit occurrence event metadata - this will be the event at the end time")
            if self.common.recscheduling.editRescheduleEvent(self.occurrenceEvent) == False:
                writeToLog("INFO","Step 6: FAILED to edit occurrence event metadata")
                return 
            sleep(3)
            
            writeToLog("INFO","Step 7: Going to verify that the metadata of the event occurrence saved")
            if self.common.recscheduling.VerifyEventDeatailsInEventPage(self.occurrenceEvent) == False:
                writeToLog("INFO","Step 7: FAILED to verify that the metadata of the event occurrence saved")
                return 
            
            writeToLog("INFO","Step 8: Going to verify that only the event occurrence in the end data of series were changed and donesn't appear anymore in the original end date")
            self.event.expectedEvent = True
            self.numberOfDaysSinceFirstEvent = 1
            for day in range(0,self.numberOfRecurrenceDays+1):
                self.event.startDate = (self.startDateInDatetimeFormat + timedelta(days=day)).strftime("%d/%m/%Y")
                self.event.convertDatetimeToVerifyDate()
                self.event.endDate = self.event.startDate
                
                if self.common.recscheduling.verifyScheduleEventInMySchedulePage(self.event) == False:
                    if self.event.expectedEvent == True:
                        writeToLog("INFO","Step 8: FAILED to verify event in my schedule page for date: " + self.event.startDate)
                        return
                    elif self.event.expectedEvent == False:
                        writeToLog("INFO","Step 8: FAILED, event display in my schedule page for date: " + self.event.startDate + "  although it shouldn't")
                        return
                
                if self.event.expectedEvent == True:
                    if self.common.recscheduling.VerifyEventDeatailsInEventPage(self.event) == False:
                        writeToLog("INFO","Step 8: FAILED to verify event metadata in event page")
                        return
                
                # the last event in the series was changed and isn't part of the series anymore so we need to know when you arrived to the end date and then to make sure that the event isn't display there
                if self.numberOfDaysSinceFirstEvent < self.numberOfRecurrenceDays:
                    self.numberOfDaysSinceFirstEvent = self.numberOfDaysSinceFirstEvent + 1
                    self.event.expectedEvent = not(self.event.expectedEvent)
                else:
                    self.numberOfDaysSinceFirstEvent = self.numberOfDaysSinceFirstEvent + 1
                    self.event.expectedEvent = False
                    
                
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Rescheduling - Edit an occurrence' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.event.startDate = self.tmpStartDate 
            self.event.verifyDateFormat= self.tmpStartDateFormat
            self.common.recscheduling.deteteEvent(self.event, viewEventSeries=True)
            self.common.recscheduling.deteteEvent(self.occurrenceEvent)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')