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
    #  @Author: Horia Cus
    # Test Name : Setup test for eSearch
    # Test description:
    # Going to upload four entries and assign them a co-editor, co-publisher, co-publisher and co-editor and change the owner
    #================================================================================================================================
    testNum = "34"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryNameOwner         = "Filter by Ownership - pending owner"
    entryNameEditor        = "Filter by Ownership - pending co-editor"
    entryNamePublisher     = "Filter by Ownership - pending co-publisher"
    entryNameBoth          = "Filter by Ownership - pending both"

    entryDescription = "filter by ownership"
    entryTags = "tag1,"

    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'

    userName1 = "inbar.willman@kaltura.com"
    userPass1 = "Kaltura1!"

    userOwner        = "adminForEsearch"    
    userEditor       = "admin"
    userPublisher    = "privateForEsearch"
    userBoth         = "unmodForEsearch"

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
            self.categoryForModerator = 'category for eSearch moderator'

            # Channel for tests in channel/ add to channel tabs
            self.channelForModerator = 'channel moderator for eSearch'

            self.entryPermissionList = {self.entryNameEditor:[self.userEditor, True, False], self.entryNamePublisher:[self.userPublisher, False, True], self.entryNameBoth:[self.userBoth, True, True]}
            self.entriesList         = [self.entryNameOwner, self.entryNameEditor, self.entryNamePublisher, self.entryNameBoth]
            self.entriesToUpload     = {self.entryNameOwner: self.filePath, self.entryNameEditor: self.filePath, self.entryNamePublisher: self.filePath, self.entryNameBoth: self.filePath}
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return

            i = 2
            writeToLog("INFO","Step " + str(i) + ": Going to upload multiple entries for " + self.userName1 + " user")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": Failed to upload multiple entries for " + self.userName1 + " user")
                return
            else:
                i = i + 1
            i = i
    
            for entry in self.entriesList:
                i = i
                writeToLog("INFO","Step " + str(i) + ": Going to publish the " + entry +"  entry")
                if self.common.myMedia.publishSingleEntry(entry, self.categoryForModerator, self.channelForModerator, publishFrom=enums.Location.MY_MEDIA) == False:
                    writeToLog("INFO","Step " + str(i) + ": FAILED to publish the " + entry +"  entry")
                    return
                else:
                    i = i + 1
                i = i
 
            for entry in self.entryPermissionList:
                i = i
 
                writeToLog("INFO", "Step " + str(i) + ": Going to navigate to " + entry + " entry")
                if self.common.editEntryPage.navigateToEditEntry(entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to navigate to " + entry + " entry")
                    return
                else:
                    i = i + 1
 
                writeToLog("INFO", "Step " + str(i) + ": Going to add permissions for " + self.entryPermissionList[entry][0] + " in " + entry + " entry")
                if self.common.editEntryPage.addCollaborator(entry, userId=self.entryPermissionList[entry][0], isCoEditor=self.entryPermissionList[entry][1], isCoPublisher=self.entryPermissionList[entry][2]) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to add permissions for " + self.entryPermissionList[entry][0] + " in " + entry + " entry")
                    return
                else:
                    i = i + 1
            sleep(10)
            
            for entry in self.entriesList:
                i = i

                writeToLog("INFO", "Step " + str(i) + ": Going to navigate to " + entry + " entry")
                if self.common.editEntryPage.navigateToEditEntry(entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to navigate to " + entry + " entry")
                    return
                else:
                    i = i + 1

                writeToLog("INFO", "Step " + str(i) + ": Going to change the owner from " + entry + " to " + self.userOwner)
                if self.common.editEntryPage.changeMediaOwner(self.userOwner) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to change the owner from " + entry + " to " + self.userOwner)
                    return
                else:
                    i = i + 1
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