import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from enum import *
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *
import ctypes


class Test:
    #================================================================================================================================
    # @Author: Michal Zomper
    # Test Name : BlackBoard: Remove Media From Media Gallery
    # Test description:
    # Upload an entry and publish it to media gallery
    # Go to Media gallery -> find the entry and click on the '+' button -> click on remove button 
    # verify that entry was removed from media gallery
    #================================================================================================================================
    testNum     = "4425"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3'
    galleryName = "New1"
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self, driverFix, self.application)
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Remove Media From Media Gallery", self.testNum)

            ##################### TEST STEPS - MAIN FLOW ##################### 
                        
            writeToLog("INFO","Step 1: Going to upload entry")            
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == None:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return

            writeToLog("INFO","Step 2: Going to publish entry to gallery")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", "", [self.galleryName], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 2: FAILED -to publish entry to gallery")
                return

            writeToLog("INFO","Step 3: Going navigate to gallery page")                                     
            if self.common.kafGeneric.navigateToGallery(self.galleryName) == False:    
                writeToLog("INFO","Step 3: FAILED navigate to gallery page")
                return 
            
            writeToLog("INFO","Step 4: Going to remove entry from gallery")                                     
            if self.common.channel.removeEntry(self.entryName) == False:    
                writeToLog("INFO","Step 4: FAILED to remove entry '" + self.entryName + "' from gallery: " + self.galleryName)
                return 
            
            writeToLog("INFO","Step 5: Going to verify that entry doesn't display in gallery any more")                                     
            if self.common.channel.searchEntryInChannel(self.entryName) == True:    
                writeToLog("INFO","Step 5: FAILED entry '" + self.entryName + "' still display in gallery although he was removed")
                return 
            writeToLog("INFO","Step 5: Preview step failed as expected - entry was removed from gallery and should not be found")
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'BlackBoard: Remove Media From Media Gallery' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')