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
    # Test description:

    #================================================================================================================================
    testNum = "709"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    categoryList = [("Apps Automation Category")]
    comments = ["Comment1", "Comment2"]

    
    
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
            self.entryName = clsTestService.addGuidToString("Category Entry Details", self.testNum)
            
            
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            self.common.entryPage.LikeUnlikeEntry(False)
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
             
            writeToLog("INFO","Step 2: Going to publish entry to category")
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryList, "", publishFrom = enums.Location.MY_MEDIA, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED publish entry '" + self.entryName + "' to category: " + self.categoryList[0])
                return
              
            writeToLog("INFO","Step 3: Going to like the entry page")            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to like entry: " + self.entryName)
                return   
             
            writeToLog("INFO","Step 4: Going to add comments to entry")  
            for i in range(2):
                if self.common.entryPage.addComment(self.comments[i]) == False:
                    writeToLog("INFO","Step 4: FAILED to add comment '" + self.comments[i] + "' to entry: " + self.entryName)
                    return
             
            writeToLog("INFO","Step 7: Going to set carousel interval in admin")  
            if self.common.admin.setCarouselInterval(self.carouselInterval) == False:
                writeToLog("INFO","Step 7: FAILED set carousel interval in admin")
                return
            writeToLog("INFO","Step 8: Going to navigate to home page")
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_TEST_BASE_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to home page")
                return
             
                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Category Entry Details' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")   
            sleep(4)                         
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')