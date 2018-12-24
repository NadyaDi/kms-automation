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
    #  @Author: Cus Horia
    # Test Name : Setup test for eSearch
    # Test description:
    # Upload a Image entry, publish it and insert custom data: a new text line, two unlimited, a list and a custom date
    #================================================================================================================================
    testNum = "28"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Description"
    entryTags = "Tags,"
    navigateFrom = enums.Location.MY_MEDIA

    userName1 = "inbar.willman@kaltura.com" # main user
    userPass1 = "Kaltura1!"
    entryName1 = "Filter by custom-data - Image"
    entryPath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\automation.jpg'
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)

            # Category tests in gallery/add to gallery tabs
            self.categoryForEsearch = 'eSearch category'
            self.categoryForModerator = 'category for eSearch moderator'

            # Channel for tests in channel/ add to channel tabs
            self.channelForEsearch  = "Channel for eSearch"
            self.channelForModerator = 'channel moderator for eSearch'
            self.SrChannelForEsearch = "SR-Channel for eSearch"

            self.channelForEsearchDescription = "channel for eSearch tests"
            self.channelForEsearchTags = 'channel tag,'
            self.channelForEsearchPrivacy = 'open'


            # Custom data fields
            self.singleTextCustomdataField1 = "SIngleText"
            self.singleTextCustomdataFieldInput1 = "Filter by custom-data - Image Single Text"
            self.unlimitedTextCustomdataField1 = "UnlimitedText0"
            self.unlimitedTextCustomdataFieldInput1 = ["Filter by custom-data - Image unlimited one", "Filter by custom-data - Image unlimited two"]
            self.unlimitedTextCustomdataAddField = "UnlimitedText"
            self.ListCustomdataField1 = "SingleTextSelectedList"
            self.ListCustomdataFieldOption1 = "Search in - Two"
            self.dateCustomDataField = "SIngleDate"
            self.dateCustomDataFieldYear = '2018'
            self.dateCustomDataFieldMonth = 'May'
            self.dateCustomDataFieldDate = '2'
            ##################### TEST STEPS - MAIN FLOW #############################################################
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return
 
            writeToLog("INFO","Step 2: Going to upload " + self.entryName1 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload " + self.entryName1 + " entry")
                return
 
            writeToLog("INFO","Step 3: Going to publish the " + self.entryName1 +"  entry")
            if self.common.myMedia.publishSingleEntry(self.entryName1, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 3: FAILED to publish the " + self.entryName1 +"  entry")
                return

            writeToLog("INFO","Step 4: Going to enter in edit entry page for the " + self.entryName1 + " entry")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName1) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to enter in edit entry page for the " + self.entryName1 + " entry")
                return

            writeToLog("INFO","Step 5: Going to add new text single custom data fields for: " + self.entryName1)
            if self.common.editEntryPage.setCustomDataField(self.singleTextCustomdataField1, self.singleTextCustomdataFieldInput1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add new text single custom data fields for: " + self.entryName1)
                return
 
            writeToLog("INFO","Step 6: Going to add new text unlimited custom data fields for: " + self.entryName1)
            if self.common.editEntryPage.setCustomDataField(self.unlimitedTextCustomdataField1, self.unlimitedTextCustomdataFieldInput1, self.unlimitedTextCustomdataAddField, enums.CustomdataType.TEXT_UNLIMITED) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to add new text unlimited custom data fields for: " + self.entryName1)
                return
            
            writeToLog("INFO","Step 7: Going to add new list custom data fields for: " + self.entryName1)
            if self.common.editEntryPage.setCustomDataField(self.ListCustomdataField1, self.ListCustomdataFieldOption1, fieldType=enums.CustomdataType.LIST) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to add new list custom data fields for: " + self.entryName1)
                return
 
            writeToLog("INFO","Step 8: Going to add date custom data fields for: " + self.entryName1)
            if self.common.editEntryPage.setCustomDataField(self.dateCustomDataField, fieldType=enums.CustomdataType.DATE, year=self.dateCustomDataFieldYear, month=self.dateCustomDataFieldMonth, day=self.dateCustomDataFieldDate)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to add date custom data fields for: " + self.entryName1)
                return

            writeToLog("INFO","TEST PASSED: The Image entry for Filter by custom data has been successfully created with all the custom data")
            #################################################################################

        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)

    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')
