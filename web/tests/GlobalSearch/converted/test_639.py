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
    # Test Name : Global Search for Captions in Video
    # Test description:
    # Upload video entry, add caption to the video
    # In the header global search enter the a word that display in the video caption to the text box and click on search: 
    #     Search results page should be opened successfully.
    #     The title should be "Search for: "
    #     the searched word- 
    #     move to search in Video tab 
    #     the entry that have the search caption need to be display
    #     the thime of the caption need to be display

    #================================================================================================================================
    testNum = "639"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    entryName = None
    categoryName = [("Apps Automation Category")]
    captionLanguage = 'English'
    captionLabel = 'Caption'
    captionText = 'This is a 2nd caption'
    captionTime = '00:29'
    filePathCaption = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\app-caption-entry-page.xml'
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_60sec.mp4'

    
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
            self.entryName = clsTestService.addGuidToString("Global Search for Captions in Video", self.testNum)

            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload new entry")            
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload new entry: " + self.entryName)
                return
             
            writeToLog("INFO","Step 2: Going to publish entry to category")
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryName, "", publishFrom = enums.Location.MY_MEDIA, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED publish entry '" + self.entryName + "' to category: " + self.categoryName)
                return
             
            writeToLog("INFO","Step 3: Going navigate to entry page")
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to entry '"+ self.entryName +"' page")
                return           
               
            writeToLog("INFO","Step 4: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED - New entry is still processing")
                return
               
            writeToLog("INFO","Step 5: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to edit entry page")
                return    
             
            writeToLog("INFO","Step 6: Going to click on caption tab")
            if self.common.editEntryPage.clickOnEditTab(enums.EditEntryPageTabName.CAPTIONS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to click on caption tab")
                return            
             
            writeToLog("INFO","Step 7: Going to add caption")
            if self.common.editEntryPage.addCaptions(self.filePathCaption, self.captionLanguage, self.captionLabel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to upload caption")
                return     
            sleep(10)
            
            writeToLog("INFO","Step 8: Going to search and verify caption in global search")
            if self.common.globalSearch.serchAndVerifyCaptionInGlobalSearch(self.captionText, self.captionTime, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to search for caption '" + self.captionText + "' in entry '" + self.entryName +"' after global search")
                return 
             
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Global search - Search for Captions in Video' was done successfully")
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