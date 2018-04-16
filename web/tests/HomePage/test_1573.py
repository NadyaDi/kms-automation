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
    testNum = "1573"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4'
    filePath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4'
    filePath3 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4'
    categoryList = [("Apps Automation Category")]
    channelList = ""
    categoryName = None
    whereToPublishFrom = "Entry Page"
    
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
            self.entryName1 = clsTestService.addGuidToString("Home Page Playlist 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Home Page Playlist 2", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("Home Page Playlist 3", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
                
            #leftimage =img.crop((pageElement['right'] /9.6, pageElement['bottom'] / 1.81 , pageElement['right'] / 2.7 , pageElement['bottom'])).save(filePath)
           # middle =  img.crop((pageElement['right'] /2.7, pageElement['bottom'] / 1.81 , pageElement['right'] / 1.57 , pageElement['bottom'])).save(filePath)
           # rigth = img.crop((pageElement['right'] /1.58, pageElement['bottom'] / 1.81 , pageElement['right'] , pageElement['bottom'])).save(filePath)
                
            self.common.qrcode.takeCustomQrCodeScreenshot("", "", "", "")
            
            writeToLog("INFO","Step 1: Going to upload entry number 1")
            if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry number 1")
                return
            
            writeToLog("INFO","Step 2: Going to upload entry number 2")
            if self.common.upload.uploadEntry(self.filePath2, self.entryName2, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry number 2")
                return
            
            writeToLog("INFO","Step 3: Going to upload entry number 3")
            if self.common.upload.uploadEntry(self.filePath3, self.entryName3, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to upload entry number 3")
                return
                 
                 
                 
                 
                 
                 
                 
                    
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                self.status = "Fail"
                return
                          
            writeToLog("INFO","Step 3: Going to add Collaborator in edit Entry Page")
            if self.common.editEntryPage.addCollaborator(self.entryName, self.newUserId, True, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to add user as a collaborator")
                return
                 
            sleep(2)     
            writeToLog("INFO","Step 4: Going to publish the entry so the add user as a collaborator can see it")            
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryList, "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to publish entry '" + self.entryName + "'")
                return
                 


            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Home Page Playlist' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)
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