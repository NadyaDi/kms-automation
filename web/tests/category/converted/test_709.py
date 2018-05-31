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
    # As the categoy's owner:
    # Choose one of your entries in the category and check that all the entry details (views, likes, comments) are correct 
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
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    categoryName = [("Apps Automation Category")]
    comments = ["Comment 1", "Comment 2"]

    
    
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
            
            writeToLog("INFO","Step 1: Going to enable like module")            
            if self.common.admin.enablelike(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to enable like module")
                return
            
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 3: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to upload entry")
                return
                
            writeToLog("INFO","Step 4: Going navigate to entry page")            
            if self.common.entryPage.navigateToEntry(self.entryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to entry: " + self.entryName)
                return 
                 
            writeToLog("INFO","Step 5: Going to like the entry page")            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to like entry: " + self.entryName)
                return   
                
            writeToLog("INFO","Step 6: Going to add comments to entry")  
            for i in range(2):
                if self.common.entryPage.addComment(self.comments[i]) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 6: FAILED to add comment '" + self.comments[i] + "' to entry: " + self.entryName)
                    return
                  
            writeToLog("INFO","Step 7: Going to publish entry to category")
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryName, "", publishFrom = enums.Location.ENTRY_PAGE, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED publish entry '" + self.entryName + "' to category: " + self.categoryName)
                return
               
            writeToLog("INFO","Step 8: Going navigate to category")  
            if self.common.category.navigateToCategory(self.categoryName[0]) == False:
                writeToLog("INFO","Step 8: FAILED navigate to category: " + self.categoryName[0])
                return
             
            writeToLog("INFO","Step 9: Going to verify entry details in category")
            if self.common.category.verifyEntryDetails(self.entryName, "1", "0", str(len(self.comments))) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify entry details in category page")
                return
             
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Category Entry Details' was done successfully")
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