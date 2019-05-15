import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
import collections


class Test:

    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Entry Design - Show Elements Enabled
    # Test description:
    # Create a new video entry, in order to change its Entry Design
    # Enable all of the Show Elements from the Entry Page, Display Tab
    # Verify that all of the Show Elements were enabled in the Entry Page
    #================================================================================================================================
    testNum = "5205"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    typeTest            = "Entry that has in the Entry Page all of the elements enabled"
    description         = "Description"
    entryName           = None
    entryDescription    = "description"
    entryTags           = "tag1,"
    instanceURL         = None
    entryURL            = None

    # Variables used in order to specify the path of the video entry
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    cssFilePath   = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\css\simple.css'
    logoFilePath  = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\kaltura_logo.png'
        
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
            # Variables used in order to proper create the Entry
            self.entryName             = clsTestService.addGuidToString("Entry Design - Show Elements Enabled", self.testNum)

            # All elements disabled
            self.showElementsDictEnabled      = {enums.EditEntryDisplayElements.HEADER:True, 
                                                 enums.EditEntryDisplayElements.HEADER_LOGO:True, 
                                                 enums.EditEntryDisplayElements.SIDEBAR:True,
                                                 enums.EditEntryDisplayElements.ENTRY_PROPERTIES:True,
                                                 enums.EditEntryDisplayElements.ENTRY_TABS:True,
                                                 enums.EditEntryDisplayElements.COMMENTS:True,
                                                 enums.EditEntryDisplayElements.FOOTER:True}  
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload the " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload the " + self.entryName + " entry")
                return
              
            writeToLog("INFO","Step 2: Going to navigate to the entry page of " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the entry page of " + self.entryName)
                return           
                 
            writeToLog("INFO","Step 3: Going to wait until the entry has been processed")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 3: FAILED to wait until the entry has been processed")
                return
 
            self.entryURL = self.common.base.driver.current_url
 
            writeToLog("INFO","Step 4: Going to navigate to the edit entry page of " + self.entryName)
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 4: FAILED to navigate to the edit entry page of " + self.entryName)
                return
              
            writeToLog("INFO","Step 5: Going to change the Entry Design by enabling all of the available Show Elements")
            if self.common.editEntryPage.changeEntryDisplay(self.showElementsDictEnabled, '', '', '') == False:
                writeToLog("INFO","Step 5: FAILED to change the Entry Design by enabling all of the available Show Elements")
                return
             
            # Navigate to the entry page
            self.common.base.navigate(self.entryURL)
             
            writeToLog("INFO","Step 6: Going to verify the Entry Design changes while being in the Entry Page of the entry: " + self.entryName)
            if self.common.entryPage.verifyEntryDisplay(self.showElementsDictEnabled, '', '', '') == False:
                writeToLog("INFO","Step 6: FAILED to verify the Entry Design changes while being in the Entry Page of the entry: " + self.entryName)
                return 
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Entry Design Test case has been successfully verified for an " + self.typeTest)
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')