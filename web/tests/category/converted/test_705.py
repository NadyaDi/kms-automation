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
    #  @Author: Inbar Willman
    # Test Name :  Categories - Search in category
    # Test description:
    # Upload entry -> publish entry to category-> Make a search in category that shouldn't return results -> Make a search in category that should return results
    # test cleanup: deleting the uploaded files
    #================================================================================================================================
    testNum = "705"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 =None
    entryName2 =None
    entryName3 = None
    categoryName = 'Apps Automation Category'
    description = "Description" 
    tags = "Tags,"
    searchWithNoResults = 'blablabal'
    searchWithResults = 'searchCategory'
    pageBeforeScrolling = 10
    pageAfterScrolling = 11
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
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
            self.entryName1 = clsTestService.addGuidToString('searchCategory 1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('searchCategory 2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('searchCategory 3', self.testNum)
            self.entryName4 = clsTestService.addGuidToString('searchCategory 4', self.testNum)
            self.entryName5 = clsTestService.addGuidToString('searchCategory 5', self.testNum)
            self.entryName6 = clsTestService.addGuidToString('searchCategory 6', self.testNum)
            self.entryName7 = clsTestService.addGuidToString('searchCategory 7', self.testNum)
            self.entryName8 = clsTestService.addGuidToString('searchCategory 8', self.testNum)
            self.entryName9 = clsTestService.addGuidToString('searchCategory 9', self.testNum)
            self.entryName10 = clsTestService.addGuidToString('searchCategory 10', self.testNum)
            self.entryName11 = clsTestService.addGuidToString('searchCategory 11', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5,
                                self.entryName6, self.entryName7, self.entryName8, self.entryName9, self.entryName10, self.entryName11]
            self.entriesList2 = ['C3B78592-705-searchCategory 1', 'C3B78592-705-searchCategory 2', 'C3B78592-705-searchCategory 3', 'C3B78592-705-searchCategory 4',
                                 'C3B78592-705-searchCategory 5', 'C3B78592-705-searchCategory 6', 'C3B78592-705-searchCategory 7', 'C3B78592-705-searchCategory 8',
                                 'C3B78592-705-searchCategory 9', 'C3B78592-705-searchCategory 10', 'C3B78592-705-searchCategory 11']
            self.entriesToUpload = {
                self.entryName1: self.filePathVideo, 
                self.entryName2: self.filePathVideo,
                self.entryName3: self.filePathVideo,
                self.entryName4: self.filePathVideo,
                self.entryName5: self.filePathVideo,
                self.entryName6: self.filePathVideo,
                self.entryName7: self.filePathVideo,
                self.entryName8: self.filePathVideo,
                self.entryName9: self.filePathVideo,
                self.entryName10: self.filePathVideo,
                self.entryName11: self.filePathVideo}
            ##################### TEST STEPS - MAIN FLOW ##################### 
#             writeToLog("INFO","Step 1: Going to upload 11 entries")            
#             if self.common.upload.uploadEntries(self.entriesToUpload, self.description, self.tags) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to upload entries")
#                 return
            
            writeToLog("INFO","Step 2: Going to show all entries")            
            if self.common.myMedia.showAllEntries() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to show all entries")
                return            
  
            writeToLog("INFO","Step 3: Going to publish entries to category from my media")
            if self.common.myMedia.publishEntriesFromMyMedia(self.entriesList2, [self.categoryName], "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to publish entries to category from my media")
                return 
            
            writeToLog("INFO","Step 4: Going to make a search in category - no results should be displayed")
            if self.common.category.searchInCategoryNoResults(self.searchWithNoResults, self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to make a search and display correct message")
                return   
            
            writeToLog("INFO","Step 5: Going to check that additional entries are displayed after loading")
            if self.common.category.verifyCategoryTableSizeBeforeAndAfterScrollingDownInPage(self.searchWithResults, self.pageBeforeScrolling, self.pageAfterScrolling) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to display additional entries after loading")
                return                     
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'search in category' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")     
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')