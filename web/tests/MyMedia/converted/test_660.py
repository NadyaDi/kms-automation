import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # Test Name: My Media - Delete - single
    # test description: Delete single entry from my media
    # The test's Flow: 
    # Go to My Media -> Select one entry -> Click 'Action' - Delete
    # Verify that the entry was deleted from my media
    # Find the second entry and click the delete button for that entry
    # Verify that the entry was deleted from my media
    #================================================================================================================================
    testNum     = "660"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryDescription = "description"
    entryTags = "tag1,"
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'  
    filePath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param  
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)        
            self.entryName1 = clsTestService.addGuidToString('delete Single one', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('delete Single two', self.testNum)
            
            self.entriesToUpload = {
            self.entryName1: self.filePath1, 
            self.entryName2: self.filePath2}
            
            ########################## TEST STEPS - MAIN FLOW ####################### 
            
            writeToLog("INFO","Step 1: Going to upload 2 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 1: FAILED to upload 2 entries")
                return
               
            writeToLog("INFO","Step 2: Going to delete entry via the entry delete button")
            if self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1) == False:
                writeToLog("INFO","Step 2: FAILED to delete entry via the entry delete button")
                return
            
            writeToLog("INFO","Step 3: Going to verify that entry '" + self.entryName1 + "' doesn't display in my media")
            if self.common.myMedia.verifyNoResultAfterSearchInMyMedia(self.entryName1) == False:
                writeToLog("INFO","Step 3: FAILED entry '" + self.entryName1 + "' still display in my media although it was deleted")
                return
                
            writeToLog("INFO","Step 4: Going to delete entry via 'action > delete")
            if self.common.myMedia.deleteEntriesFromMyMedia(self.entryName2) == False:
                writeToLog("INFO","Step 4: FAILED to delete entry '" + self.entryName2  +" entry via 'action > delete")
                return
            
            writeToLog("INFO","Step 5: Going to verify that entry '" + self.entryName2 + "'  doesn't display in my media")
            if self.common.myMedia.verifyNoResultAfterSearchInMyMedia(self.entryName2) == False:
                writeToLog("INFO","Step 5: FAILED entry '" + self.entryName2 + "' still display in my media although it was deleted")
                return
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Delete single entry' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')