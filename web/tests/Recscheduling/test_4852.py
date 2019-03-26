import time, pytest, datetime
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
    startTime = None
    endTime = None
    
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
            self.startDate = datetime.datetime.now().strftime("%d/%m/%Y")
            self.endDate = (datetime.datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        
            startTime = time.time() + (60*60)
            startTime = time.strftime("%I:%M %p",time.localtime(startTime))
             
            endTime = time.time() + 2*(60*60)
            endTime = time.strftime("%I:%M %p",time.localtime(endTime))
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
                
#            self.common.base.click(self.common.recscheduling.SCHEDULE_ADD_RECURRENCE_BUTTON) 

            
#           self.common.recscheduling.setEventRecurrence(recurrenceInterval, dailyOption, dailyDays, weeklyWeeks, weeklyDaysNames, monthlyOption, monthlyDayNumber,  monthlyMonthNumber, monthlyWeekdaysIndex , monthlyDayName, optionTwoMonthlyMonthNumber, reccurenceStartDate, reccurenceEndDate, reccurenceStartTime, reccurenceEndTime)
#            self.common.recscheduling.setEventRecurrence(recurrenceInterval=enums.scheduleRecurrenceInterval.MONTHS, monthlyOption=enums.scheduleRecurrenceMonthlyOption.BY_WEEKDAY, monthlyWeekdaysIndex=enums.scheduleRecurrenceMonthlyIndex.third, monthlyDayName=enums.scheduleRecurrenceDayOfTheWeek.SATURDAY, optionTwoMonthlyMonthNumber="5", endDateOption=enums.scheduleRecurrenceEndDateOption.END_BY, reccurenceStartTime=startTime, reccurenceEndTime=endTime ,reccurenceStartDate=self.startDate, reccurenceEndDate=self.endDate)
            
#             
#             self.common.recscheduling.createRescheduleEventWithoutRecurrence(self.eventTitle, self.startDate, self.endDate, startTime,endTime, self.description, self.tags, False, 'copeDetailsName', 'copeDetailsDescriptio', 'copeDetailsTags,', [enums.RecschedulingResourceOptions.MAIN_AUDITORIUM,enums.RecschedulingResourceOptions.AUTOMATION_ROOM] ,eventOrganizer='python_automation') 
#             
#           self.common.recscheduling.createRescheduleEvent(self.eventTitle, self.startDate, self.endDate, startTime,endTime, self.description, self.tags, True, resources=enums.RecschedulingResourceOptions.AUTOMATION_ROOM, isRecurrence=True, exitEvent=False, recurrenceInterval=enums.scheduleRecurrenceInterval.MONTHS, monthlyOption=enums.scheduleRecurrenceMonthlyOption.BY_WEEKDAY, monthlyWeekdaysIndex=enums.scheduleRecurrenceMonthlyIndex.third, monthlyDayName=enums.scheduleRecurrenceDayOfTheWeek.SATURDAY, optionTwoMonthlyMonthNumber="5", endDateOption=enums.scheduleRecurrenceEndDateOption.END_BY, reccurenceStartTime=startTime, reccurenceEndTime=endTime ,reccurenceStartDate=self.startDate, reccurenceEndDate=self.endDate)
            self.common.recscheduling.verifyScheduleEventInMySchedulePage("automation", "startDate", "endDate", "03:32 PM-04:32 PM", resource=enums.RecschedulingResourceOptions.AUTOMATION_ROOM)
            
            writeToLog("INFO","Step 1: Going to set rescheduling in admin")
            if self.common.admin.enableRecscheduling(True) == False:
                writeToLog("INFO","Step 1: FAILED set rescheduling in admin")
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

            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')