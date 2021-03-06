import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
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
    # Scheduling media - add media to channel via upload page 
    #================================================================================================================================
    testNum     = "876"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    channelDescription = "Channel description"
    channelTags = "Channeltags1,Channeltags2,"
    categoryList = ['Galleries - Admin', 'Open Gallery - admin owner']
    
    entryPastStartDate = (datetime.datetime.now() + timedelta(days=-1)).strftime("%d/%m/%Y")
    entryTodayStartDate = datetime.datetime.now().strftime("%d/%m/%Y")
    entryFutureStartDate = (datetime.datetime.now() + timedelta(days=10)).strftime("%d/%m/%Y")

    entryFutureStartTime = time.time() + (60*60)
    entryFutureStartTime= time.strftime("%I:%M %p",time.localtime(entryFutureStartTime))
     
    entryPastStartTime = time.time() - (60*60)
    entryPastStartTime= time.strftime("%I:%M %p",time.localtime(entryPastStartTime))
    
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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            ########################################################################
            self.entryName = clsTestService.addGuidToString('SchedulingEntry', self.testNum)
            self.channelName = clsTestService.addGuidToString('Scheduling_Channel', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to create Channel")
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.PRIVATE, True, True, True) == False:
                writeToLog("INFO","Step 1: FAILED to create Channel")
                return            
            
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 3: Going to set Future time-frame publishing to entry ")   
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryFutureStartDate, startTime=self.entryFutureStartTime) == False:
                writeToLog("INFO","Step 3: FAILED to set Future time-frame publishing to entry")
                return
            
            writeToLog("INFO","Step 4: Going to publish the entry from Step #2")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", [self.channelName], publishFrom = enums.Location.UPLOAD_PAGE) == False:
                writeToLog("INFO","Step 4: FAILED to publish the entry from Step #")
                return
            
            writeToLog("INFO","Step 5: Verify if the entry is presented inside the channel from step #2 (Expected: should not be presented)")
            if self.common.channel.verifyIfSingleEntryInChannel(self.channelName, self.entryName, isExpected=False) == False:
                writeToLog("INFO","Step 5: FAILED, Entry is presented although it shouldn't")
                return
            
            writeToLog("INFO","Step 6: Going to set Past time-frame publishing to entry ")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, entryName=self.entryName) == False:
                writeToLog("INFO","Step 6: FAILED to set past time-frame publishing to entry")
                return
            
            writeToLog("INFO","Step 7: Verify if the entry is presented inside the channel from step #2 (Expected: should be presented)")
            if self.common.channel.verifyIfSingleEntryInChannel(self.channelName, self.entryName, isExpected=True) == False:
                writeToLog("INFO","Step 7: FAILED, Entry is not presented although it should")
                return            

            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.channel.deleteChannel(self.channelName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')