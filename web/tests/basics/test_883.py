from pymysql.times import Date
from time import strftime

import pytest

from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #================================================================================================================================
    # @Author: Tzachi Guetta
    # Test description:
    # In case disclaimer module is turned on and set to "before upload" 
    # The following test will check that upload is prevented before disclaimer's check-box was checked.
    # The test's Flow: 
    # Login -> Checking that the user is not able to upload before accepting disclaimer -> Accepting disclaimer -> performing upload
    # then, Navigating to Entry page. 
    # test cleanup: deleting the uploaded file, turning off disclaimer module
    #================================================================================================================================
    testNum     = "883"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    channelDescription = "Channel description"
    channelTags = "Channeltags1,Channeltags2,"
    categoryList = ['Galleries - Admin', 'Open Gallery - admin owner']
    entryTodayStartDate = Date.today().strftime("%d/%m/%Y")
    entryFutureStartDate = (Date.today() + timedelta(days=10)).strftime("%d/%m/%Y")

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
            self,captur,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            ########################################################################
            self.entryName = clsTestService.addGuidToString('entryName')
            self.channelName = clsTestService.addGuidToString('Channel name') 

            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to set Future time-frame publishing to entry ")
#             self.common.editEntryPage.setScheduleStartDate(self.entryTodayStartDate)
#             self.common.editEntryPage.setScheduleEndDate(self.entryFutureStartDate)            
            if self.common.editEntryPage.addPublishingSchedule(startTime=self.entryFutureStartTime, entryName=self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to set Future time-frame publishing to entry")
                return
            
            writeToLog("INFO","Step 3: Going to create Channel")
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.PRIVATE, True, True, True, self.categoryList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create Channel")
                return
            
            writeToLog("INFO","Step 4: Going to publish the entry from Step #3")
            if self.common.myMedia.publishSingleEntryInMyMedia(self.entryName, "", [self.channelName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to publish the entry from Step #3")
                return
            
            writeToLog("INFO","Step 5: Verify if the entry is presented inside the channel from step #4 (Expected: should not be presented)")
            if self.common.channel.verifyIfSingleEntryInChannel(self.channelName, self.entryName, isExpected=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED, Entry is presented although it shouldn't")
                return
            
            writeToLog("INFO","Step 6: Going to set Past time-frame publishing to entry ")
            if self.common.editEntryPage.addPublishingSchedule(startTime=self.entryPastStartTime, entryName=self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to set past time-frame publishing to entry")
                return
            
            writeToLog("INFO","Step 7: Verify if the entry is presented inside the channel from step #4 (Expected: should be presented)")
            if self.common.channel.verifyIfSingleEntryInChannel(self.channelName, self.entryName, isExpected=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED, Entry is not presented although it should")
                return

            #########################################################################
            print("DONE")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.channel.deleteChannel(self.channelName)
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')