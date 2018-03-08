from time import strftime

import pytest

from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *



class Test:
    
    #================================================================================================================================
    # @Author: Tzachi Guetta
    # Test description:
    # 
    #================================================================================================================================
    testNum     = "894"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    
    entryPastStartDate = (datetime.datetime.now() + timedelta(days=-1)).strftime("%d/%m/%Y")
    entryTodayStartDate = datetime.datetime.now().strftime("%d/%m/%Y")
    entryFutureStartDate = (datetime.datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")

    entryFutureStartTime = time.time() + (60*60)
    entryFutureStartTime= time.strftime("%I:%M %p",time.localtime(entryFutureStartTime))
     
    entryPastStartTime = time.time() - (60*60)
    entryPastStartTime= time.strftime("%I:%M %p",time.localtime(entryPastStartTime))
    
    
#     expectedEntriesList_Comments = ["C - Automation Entry - Comments", "B - Automation Entry - Views", "A - Automation Entry - Alphabetical",  "D - Automation Entry - Most Recent"]
#     expectedEntriesList_Likes = ["E - Automation Entry - Likes", "A - Automation Entry - Alphabetical", "B - Automation Entry - Views",  "D - Automation Entry - Most Recent"]
#     expectedEntriesList_Views = ["B - Automation Entry - Views", "A - Automation Entry - Alphabetical", "C - Automation Entry - Comments",  "D - Automation Entry - Most Recent"]
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg' 
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,captur,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('Scheduling_Always', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('Scheduling_1_hour_from_now', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('Scheduling_1_Day__AND_1_hour_from_now', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry #1 - Scheduling = Always")
            if self.common.upload.uploadEntry(self.filePath, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return    
             
            writeToLog("INFO","Step 2: Going to upload entry #2, Scheduling = 1 hour from now")
            if self.common.upload.uploadEntry(self.filePath, self.entryName2, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return           
             
            writeToLog("INFO","Step 3: Going to set Future time-frame publishing to entry ")   
            if self.common.editEntryPage.addPublishingSchedule(startTime=self.entryFutureStartTime) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to set Future time-frame publishing to entry")
                return
             
            writeToLog("INFO","Step 4: Going to upload entry #3, Scheduling = 1 day + 1 hour from now")
            if self.common.upload.uploadEntry(self.filePath, self.entryName3, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED failed to upload entry")
                return           
             
            writeToLog("INFO","Step 5: Going to set Future time-frame publishing to entry ")   
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryFutureStartDate, startTime=self.entryFutureStartTime) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to set Future time-frame publishing to entry")
                return
             
            expectedEntriesList_SCHEDULING_ASC = [self.entryName1, self.entryName2, self.entryName3]
            expectedEntriesList_SCHEDULING_DEC = [self.entryName3, self.entryName2, self.entryName1]
            expectedEntriesList_SCHEDULING_AND_PRIVATE = [self.entryName1, self.entryName2]
             
            writeToLog("INFO","Step 6: Going to sort entries by Scheduling ASC")
            if self.common.myMedia.sortAndFilterInMyMedia(enums.SortBy.SCHEDULING_ASC) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to sort entries by Scheduling ASC")
                return
              
            writeToLog("INFO","Step 7: Going to verify entries order - by Scheduling DEC")
            if self.common.myMedia.verifyEntriesOrder(expectedEntriesList_SCHEDULING_ASC) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify entries order - by Scheduling DEC")
                return
 
            writeToLog("INFO","Step 8: Going to sort entries by Scheduling DEC")
            if self.common.myMedia.sortAndFilterInMyMedia(enums.SortBy.SCHEDULING_DESC) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to sort entries by Scheduling DEC")
                return
              
            writeToLog("INFO","Step 9: Going to verify entries order - by Scheduling DEC")
            if self.common.myMedia.verifyEntriesOrder(expectedEntriesList_SCHEDULING_DEC) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify entries order - by Scheduling DEC")
                return
             
            writeToLog("INFO","Step 10: Going to set entry #3 to unlisted")
            if self.common.myMedia.publishSingleEntryPrivacyToUnlistedInMyMedia(self.entryName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to set entry #3 to unlisted")
                return
             
            writeToLog("INFO","Step 11: Going to sort&filter entries - by Scheduling ASC & only Privacy=Private")
            if self.common.myMedia.sortAndFilterInMyMedia(enums.SortBy.SCHEDULING_ASC, enums.EntryPrivacyType.PRIVATE, resetFields=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to sort&filter entries - by Scheduling ASC & only Privacy=Private")
                return
            
            writeToLog("INFO","Step 12: Going to verify that entry #3 is not presented")
            if self.common.myMedia.isEntryPresented(self.entryName3, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to verify that entry #3 is not presented")
                return
                   
            writeToLog("INFO","Step 13: Going to verify entries order - by Scheduling ASC & only Privacy=Private")
            if self.common.myMedia.verifyEntriesOrder(expectedEntriesList_SCHEDULING_AND_PRIVATE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to verify entries order - by Scheduling ASC & only Privacy=Private")
                return
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')