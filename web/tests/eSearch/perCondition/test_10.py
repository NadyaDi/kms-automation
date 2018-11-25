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
    #  @Author: Ori Flchtman
    # Test Name : Setup test for eSearch
    # Test description:
    # Going to upload entries for filter as admin - entries owner
    #================================================================================================================================
    testNum = "10"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    entriesList = []
    entryDescription = "filter by owner"
    entryTags = "tag1,"
    playlistName1  = None
    playlistName2  = None
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\automation2.jpg'
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4' 
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3' 
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'   
    channelTags = "Tags,"
    userName1 = "inbar.willman@kaltura.com" # main user
    userPass1 = "Kaltura1!"
    userName2 = "private"
    userPass2 = "123456"
    userName3 = "admin"
    userPass3 = "123456"
    userName4 = "unmod"
    userPass4 = "123456"
    userName5 = "adminForEsearch"
    userPass5 = "123456" 
    userName6 = "privateForEsearch"
    userPass6 = "123456"    
    userName7 = "unmodForEsearch"
    userPass7 = "123456"  
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
            ########################################################################
            self.entryName2 = clsTestService.addGuidToString('EntryVideo', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('EntryAudio', self.testNum)
            self.entryName4 = clsTestService.addGuidToString('EntryImage', self.testNum)             
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3, self.entryName4]
            self.playlistName1 = clsTestService.addGuidToString('emptyPlaylistTest#1', self.testNum)
            self.playlistName2 = clsTestService.addGuidToString('PlaylistTest#2', self.testNum)
            self.listOfPlaylists = [self.playlistName1, self.playlistName2]
            self.youtuebLink = "https://www.youtube.com/watch?v=usNsCeOV4GM"
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entriesToUpload = {
                self.entryName2: self.filePathVideo,
                self.entryName3: self.filePathAudio,
                self.entryName4: self.filePathImage}     
            
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return    
            
            writeToLog("INFO","Step 2: Going to upload 3 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 3 entries")
                return  
            
            writeToLog("INFO","Step 3: Going to create webcast event")
            if self.common.upload.clickAddNewWebcast(self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create webcast event")
                return  
            
            #Create Video Quiz:
            writeToLog("INFO","Step 4: Going to navigate to add new video quiz")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to click video quiz")
                return  
              
            writeToLog("INFO","Step 5: Going to search the uploaded entry and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryName, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to find entry and open KEA")
                return  
              
            writeToLog("INFO","Step 6: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to start quiz and add questions")
                return   
              
            writeToLog("INFO","Step 7: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to save quiz and navigate to media page")
                return         
            
            #Upload Youtube:
            writeToLog("INFO","Step 8: Going to upload youtube entry")
            if self.common.upload.clickAddYoutube() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to upload youtube entry")
                return
            
            writeToLog("INFO","Step 9: Going to insert youtube link")
            if self.common.upload.addYoutubeEntry(self.youtuebLink, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to insert youtube link")
                return                                            
                          
#             
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