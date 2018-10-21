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
    # Test Name : My Media - Publish to category - single 
    # Test description:
    # Upload entry -> Search medie in My Media -> Check entry's checkbox -> Click on 'Action' -> Choose 'publish' -> Choose category -> Click 'Save'
    #================================================================================================================================
    testNum = "662"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    categoryName = None
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'

    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('publishEntryToCategory', self.testNum)
            self.categoryName = clsTestService.addGuidToString('My Media-Publish to category-single', self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################  
            
            writeToLog("INFO","Step 1: Going to create open category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.entryDescription) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create open category")
                return
             
            writeToLog("INFO","Step 2: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 4: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED failed to upload entry")
                return
               
            writeToLog("INFO","Step 5: Going to publish entry to category")
            if self.common.myMedia.publishSingleEntry(self.entryName, [self.categoryName], "", publishFrom = enums.Location.MY_MEDIA, disclaimer=False) == False: 
                self.status = "Fail"        
                writeToLog("INFO","Step 5: FAILED to publish entry to category")
                return    
            
            writeToLog("INFO","Step 6: Going to search entry in category page")
            if self.common.category.searchEntriesInCategory([self.entryName], self.categoryName) == False:
                self.status = "Fail"        
                writeToLog("INFO","Step 6: FAILED to find entry in category")
                return                         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'My Media - Publish to category - single ' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.apiClientSession.deleteCategory(self.categoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')