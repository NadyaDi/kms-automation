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
    # Test Name : Editor - Create comments and sub comments with time stamp and then Trimming the Entry
    # Test description:
    # Create a comment that has a time cue point at second 15
    # Verify that when the entry is normal, the user is able to use the comment cue point time
    # Verify that the comment cue point time can be used after the entry has been trimmed
    #================================================================================================================================
    testNum = "5122"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    typeTest            = "Entry that has a comment with cue point and used when the user was normal and then trimmed"
    description         = "Description"
    tags                = "Tags,"
    entryName           = "Editor - Comments Trimmed"
    entryDescription    = "description"
    entryTags           = "tag1,"
    
    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    entryComment          = 'comment with time'
    entryCommentReply     = 'comment reply'
    
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
            self,self.driver             = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common                  = Common(self.driver)
            self.entryName               = clsTestService.addGuidToString("Editor - Comments Trimmed", self.testNum)
            expectedEntryDuration        = "0:20"
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return        
                 
            writeToLog("INFO","Step 2: Going to navigate to the entry page of " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to the entry page of " + self.entryName)
                return           
                 
            writeToLog("INFO","Step 3: Going to wait until the entry is processed")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 3: FAILED to wait until the entry is processed")
                return
                                                      
            writeToLog("INFO","Step 4: Going to add " + self.entryComment + " at second 15 of the entry")
            if self.common.entryPage.addCommentWithTimeStamp(self.entryComment, '0:15') == False:
                writeToLog("INFO","Step 4: FAILED  to add " + self.entryComment + " at second 15 of the entry")
                return
             
            writeToLog("INFO","Step 5: Going to replay with " + self.entryCommentReply + " to the " + self.entryComment + " comment")
            if self.common.entryPage.replyComment(self.entryCommentReply) == False:
                writeToLog("INFO","Step 5: FAILED to replay with " + self.entryCommentReply + " to the " + self.entryComment + " comment")
                return
            
            writeToLog("INFO","Step 6: Going to start the playing process of the entry from second 15 while using " + self.entryComment + " comment Cue Point, before trim")
            if self.common.player.clickAndVerifyCommentTimeStamp(15) == False:
                writeToLog("INFO","Step 6: FAILED to start the playing process of the entry from second 15 while using " + self.entryComment + " comment Cue Point, before trim")
                return  
            
            writeToLog("INFO","Step 7: Going to trim the entry from time interval 00:10 - 00:20")  
            if self.common.kea.trimEntry(self.entryName, "00:10", "00:20", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 7: FAILED to trim the entry from time interval 00:10 - 00:20")  
                return

            writeToLog("INFO","Step 8: Going to navigate to the entry page of " + self.entryName)
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 8: FAILED to navigate to the entry page of " + self.entryName)
                return 
            sleep(10)
            writeToLog("INFO","Step 9: Going to start the playing process of the entry from second 15 while using " + self.entryComment + " comment Cue Point, after trim")
            if self.common.player.clickAndVerifyCommentTimeStamp(15) == False:
                writeToLog("INFO","Step 9: FAILED to start the playing process of the entry from second 15 while using " + self.entryComment + " comment Cue Point, after trim")
                return   
            #################################################################################################
            self.status = "Pass"   
            writeToLog("INFO","TEST PASSED")
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