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
    
    status = "Fail"
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
    numberOfEntriesInChannelPage = 10

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
            
            self.entriesToUpload = {
                self.entryName1: self.filePath, 
                self.entryName2: self.filePath,
                self.entryName3: self.filePath, 
                self.entryName4: self.filePath,
                self.entryName5: self.filePath,
                self.entryName6: self.filePath, 
                self.entryName7: self.filePath,
                self.entryName8: self.filePath, 
                self.entryName9: self.filePath,
                self.entryName10: self.filePath,
                self.entryName11: self.filePath }            
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
                
            writeToLog("INFO","Step 1: Going to change number of entries to display in channel page")            
            if self.common.admin.changNumberEentriesPageSizeForChannel(self.numberOfEntriesInChannelPage) == False:
                writeToLog("INFO","Step 1: FAILED to change number of entries to display in channel page")
                return
             
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
             
            writeToLog("INFO","Step 3: Going to upload 11 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.description, self.tags) == False:
                writeToLog("INFO","Step 3: FAILED to upload 11 entries")
                return

            writeToLog("INFO","Step 4: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                writeToLog("INFO","Step 4: FAILED create new channel")
                return
            
            sleep(2)
            writeToLog("INFO","Step 5: Going to publish entries to channel")            
            if self.common.myMedia.publishEntriesFromMyMedia(self.entriesList, "", self.channelName, disclaimer=False, showAllEntries=True) == False:
                writeToLog("INFO","Step 5: FAILED to publish entries to channel: " + self.channelName[0])
                return
             
            writeToLog("INFO","Step 6: Going to make a search in channel - no results should be displayed")
            if self.common.channel.searchInChannelNoResults(self.searchWithNoResults, self.channelName[0]) == False:
                writeToLog("INFO","Step 6: FAILED to make a search and display correct message")
                return   
            
            writeToLog("INFO","Step 7: Going to check that additional entries are displayed after loading")
            if self.common.channel.verifyChannelTableSizeBeforeAndAfterScrollingDownInPage(self.searchWithResults, self.pageBeforeScrolling, self.pageAfterScrolling, noQuotationMarks=True) == False:
                writeToLog("INFO","Step 7: FAILED to verify all entries display in channel")
                return      
            
            ##################################################################
            self.status = "Pass"
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