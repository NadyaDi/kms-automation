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
    # Test Name: Categories - Enable\Disable comments in category
    # Test description:
    # Login to KMS-> Upload entry and publish to category -> Go to category -> Click on 'Actions'-'Edit'-> Enable comments in category -> Go to entry page from category > Add comments -> go to category->
    # Click on 'Actions'-'Edit'-> Uncheck the option: 'Enable comments in channel' -> Go to entry page from category -> Check that there is no option to add comment
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "714"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    commnetText = 'test123'
    categoryName = 'Apps Automation Category'
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
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
            ########################################################################
            self.entryName = clsTestService.addGuidToString('disableComments', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return 
            
            writeToLog("INFO","Step 2: Going to publish entry to category")
            if self.common.myMedia.publishSingleEntry(self.entryName, [self.categoryName], [], publishFrom = enums.Location.UPLOAD_PAGE) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to publish entry to category")
                return                   
               
            writeToLog("INFO","Step 3: Going to navigate to edit category page")
            if self.common.category.navigateToEditCategoryPage(self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to edit category page")
                return           
               
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return
                        
            writeToLog("INFO","Step 4: Going to add new comment to entry")
            if self.common.entryPage.addComment(self.commnetText) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add new comment")
                return            
              
            writeToLog("INFO","Step 5: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to edit entry page")
                return    
            
            writeToLog("INFO","Step 6: Going to click on option tab and enable - disabled comment")
            if self.common.editEntryPage.changeEntryOptions(True, False, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to click on option tab and enable disabled comments option")
                return    
            
            writeToLog("INFO","Step 7: Going to navigate to entry page")
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to entry page")
                return   
            
            writeToLog("INFO","Step 8: Going to verify that comments section isn't displayed in entry page")
            if self.common.entryPage.checkEntryCommentsSection(self.commnetText, True, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED - Comments section still displayed in entry page")
                return                                                                                       
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')