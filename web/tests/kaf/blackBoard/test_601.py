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
    # Test Name : BlackBoard - Publish From Entry Page
    # Test description:
    # Upload entry
    # Go to the entry page that was uploaded and publish it to course
    # Go to the course that the entry was published to and verify that the entry display their
    #================================================================================================================================
    testNum     = "601"
    application = enums.Application.BLACK_BOARD
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
            self.entryName = clsTestService.addGuidToString("Publish From Entry Page", self.testNum)
        
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return      
              
            writeToLog("INFO","Step 2: Going navigate to entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED  navigate to entry page: " + self.entryName)
                return           
              
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return
                  
            writeToLog("INFO","Step 5: Going to publish entry to gallery from entry page")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", "", [self.galleryName], publishFrom = enums.Location.ENTRY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to publish entry '" + self.entryName + "' to gallery '" + self.galleryName + "' from entry page")
                return                 
            
            writeToLog("INFO","Step 6: Going navigate to gallery page")
            if self.common.blackBoard.navigateToGalleryBB(self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED navigate to gallery: " + self.galleryName)
                return             
                          
            writeToLog("INFO","Step 7: Going to search entry in gallery")
            if self.common.channel.searchEntryInChannel(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to find entry entry '" + self.entryName + "' in gallery '" + self.galleryName)
                return               
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'BlackBoard - Publish From Entry Page' was done successfully")
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