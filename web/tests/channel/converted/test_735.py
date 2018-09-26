import time, pytest
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
    # Test Name : Channel page - Search in channel 
    # Test description:
    # Upload several entries and publish them to channel
    # In channel page:
    #    1. In the search textbox - insert word which does not exists in the channel -  'No Search Results...' message should be received.
    #    2. In the search textbox - insert existing word (in the entry's name / tags / description) - The compatible results should be displayed in the page
    #================================================================================================================================
    testNum = "735"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    channelName = None
    searchWithNoResults = "blablabal"
    searchWithResults = "Search in channel"
    pageBeforeScrolling = 10
    pageAfterScrolling = 11

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
            self.channelName = clsTestService.addGuidToString("Channel page - Search in channel", self.testNum)
            self.channelName= [(self.channelName)]
            self.entryName1 = clsTestService.addGuidToString('Search in channel 1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('Search in channel 2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('Search in channel 3', self.testNum)
            self.entryName4 = clsTestService.addGuidToString('Search in channel 4', self.testNum)
            self.entryName5 = clsTestService.addGuidToString('Search in channel 5', self.testNum)
            self.entryName6 = clsTestService.addGuidToString('Search in channel 6', self.testNum)
            self.entryName7 = clsTestService.addGuidToString('Search in channel 7', self.testNum)
            self.entryName8 = clsTestService.addGuidToString('Search in channel 8', self.testNum)
            self.entryName9 = clsTestService.addGuidToString('Search in channel 9', self.testNum)
            self.entryName10 = clsTestService.addGuidToString('Search in channel 10', self.testNum)
            self.entryName11 = clsTestService.addGuidToString('Search in channel 11', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5,
                                self.entryName6, self.entryName7, self.entryName8, self.entryName9, self.entryName10, self.entryName11]
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
                
            for i in range(1,12):
                writeToLog("INFO","Step " + str(i) + ": Going to upload new entry: '" + eval('self.entryName'+str(i)))            
                if self.common.upload.uploadEntry(self.filePath, eval('self.entryName'+str(i)), self.description, self.tags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to upload new entry: " + eval('self.entryName'+str(i)))
                    return
             
            writeToLog("INFO","Step 12: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED create new channel")
                return
             
            writeToLog("INFO","Step 13: Going to publish entries to channel")            
            if self.common.myMedia.publishEntriesFromMyMedia(self.entriesList, "", self.channelName, disclaimer=False, showAllEntries=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to publish entries to channel: " + self.channelName)
                return
             
            writeToLog("INFO","Step 14: Going to make a search in channel - no results should be displayed")
            if self.common.channel.searchInChannelNoResults(self.searchWithNoResults, self.channelName[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to make a search and display correct message")
                return   
            
            writeToLog("INFO","Step 15: Going to check that additional entries are displayed after loading")
            if self.common.channel.verifyChannelTableSizeBeforeAndAfterScrollingDownInPage(self.searchWithResults, self.pageBeforeScrolling, self.pageAfterScrolling, noQuotationMarks=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to verify all entries display in channel")
                return      
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Channel page - Search in channel ' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                   
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            self.common.channel.deleteChannel(self.channelName[0])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')