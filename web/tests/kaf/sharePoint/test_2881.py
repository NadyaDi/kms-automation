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
    # @Author: Oded Berihon
    # Test Name : Share_Point - View Collapsed Expanded Modes
    # Test description:
    # upload several entries
    # in my media -  In the page's top right side - Change between the view options : 
    #    Collapsed view 
    #    Expanded view
    # All the entries / buttons / menus should be displayed in both view options and the page should look properly 
    #================================================================================================================================
    testNum     = "2881"
    application = enums.Application.SHARE_POINT
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    
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
            self.entryName1 = clsTestService.addGuidToString("My Media - View: Collapsed Expanded 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("My Media - View: Collapsed Expanded 2", self.testNum)
            
            self.entriesToUpload = {
            self.entryName1: self.filePath,
            self.entryName2: self.filePath}
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload 2 entries")   
            if self.common.upload.uploadEntries(self.entriesToUpload, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 2 entries")
                return          

            writeToLog("INFO","Step 2: Going navigate to my media")  
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to my media")
                return  
 
            writeToLog("INFO","Step 3: Going to change my media view to 'collapsed'")  
            if self.common.base.click(self.common.myMedia.MY_MEDIA_COLLAPSED_VIEW_BUTTON, timeout=15) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to change my media view to 'collapsed view'")
                return 
               
            writeToLog("INFO","Step 4: Going to verify my media view")
            if self.common.myMedia.verifyMyMediaViewForEntris([self.entryName1, self.entryName2], viewType=enums.MyMediaView.COLLAPSED) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify my media view")
                return
            
            writeToLog("INFO","Step 5: Going to change my media view to 'detailed'")  
            if self.common.base.click(self.common.myMedia.MY_MEDIA_DETAILED_VIEW_BUTTON, timeout=15) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to change my media view to 'detailed view'")
                return 
               
            writeToLog("INFO","Step 6: Going to verify my media view")
            if self.common.myMedia.verifyMyMediaViewForEntris([self.entryName1, self.entryName2], viewType=enums.MyMediaView.DETAILED) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify my media view")
                return
           
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Share_Point - View Collapsed Expanded Modes' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')