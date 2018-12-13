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
    # Upload and publish multiple youtube entries in order to verify that the Filter by Duration works properly for entries between 0 to over 180 minutes
    #================================================================================================================================
    testNum = "14"
    
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
    
    entryName1 = "Filter by Duration - Under ten minutes"
    entryName2 = "Filter by Duration - Under thirty minutes"
    entryName3 = "Filter by Duration - Under sixty minutes"
    entryName4 = "Filter by Duration - Under onehundredandeighty minutes"
    entryName5 = "Filter by Duration - Over onehundredandeighty minutes"
    youtubeLink1 = "https://www.youtube.com/watch?v=vBOtWCGnc4g"
    youtubeLink2 = "https://www.youtube.com/watch?v=eStXV_TYFFw"
    youtubeLink3 = "https://www.youtube.com/watch?v=mKRZYUds32M"
    youtubeLink4 = "https://www.youtube.com/watch?v=sn3Fobs6RYI"
    youtubeLink5 = "https://www.youtube.com/watch?v=TRKqyTfw56c"
    youtubeMap = {youtubeLink1:entryName1, youtubeLink2:entryName2, youtubeLink3:entryName3, youtubeLink4:entryName4, youtubeLink5:entryName5}

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
            ##################### TEST STEPS - MAIN FLOW #############################################################
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return
            
            i = 1
            for entry in self.youtubeMap:
                i = i + 1        
                writeToLog("INFO","Step " + str(i) + ": Going to navigate to youtube upload page")
                if self.common.upload.clickAddYoutube() == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to youtube upload page")
                    return
                       
                writeToLog("INFO","Step " + str(i + 1) + ": Going to upload " + self.youtubeMap[entry] +" entry")
                if self.common.upload.addYoutubeEntry(entry, self.youtubeMap[entry]) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 1) + ": FAILED to upload a " + self.youtubeMap[entry] +"  entry")
                    return  
                     
                writeToLog("INFO","Step " + str(i + 2) + ": Going to publish the " + self.youtubeMap[entry] +"  entry")
                if self.common.myMedia.publishSingleEntry(self.youtubeMap[entry], [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                    writeToLog("INFO","Step " + str(i +2) + ": FAILED to publish the " + self.youtubeMap[entry] +"  entry")
                    return
                
                i = i + 2
                       
            writeToLog("INFO","TEST PASSED: All the youtube entries were created and published successfully") 
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