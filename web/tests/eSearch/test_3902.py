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
    # Test Name: Sort by - Galleries page
    # The test's Flow: 
    # Login to KMS-> Go to galleries page and make a search -> SOrt galleries by all options
    #================================================================================================================================
    testNum     = "3902"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
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
            self.sortByMostReccentList = ["4 - forth gallery", "3 - third gallery", "2 - second gallery", "1 - First gallery"]
            self.sortByAlphabeticalAToZList = ["1 - First gallery", "2 - second gallery", "3 - third gallery", "4 - forth gallery"]
            self.sortByAlphabeticalZToAList = ["4 - forth gallery", "3 - third gallery", "2 - second gallery", "1 - First gallery"]
            self.sortByMembersAndSubscribers = ["3 - third gallery","4 - forth gallery", "2 - second gallery", "1 - First gallery"]
            self.sortByMediaCount = ["4 - forth gallery", "1 - First gallery", "3 - third gallery", "2 - second gallery"]
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to navigate to galleries page")
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_KMS_GALLERIES_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED navigate to galleries page")
                return
            
            writeToLog("INFO","Step 2: Going to check that default sort is relevance")
            if self.common.channel.verifyChannelsDefaultSort(enums.ChannelsSortBy.RELEVANCE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to displayed correct default sort")
                return 

            writeToLog("INFO","Step 3: Going to sort galleries by most recent")
            if self.common.category.verifySortInGalleries(enums.ChannelsSortBy.MOST_RECENT, self.sortByMostReccentList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to sort galleries by most recent")
                return   
            
            writeToLog("INFO","Step 4: Going to sort galleries by alphabetical A-Z")
            if self.common.category.verifySortInGalleries(enums.ChannelsSortBy.ALPHABETICAL_NEWUI, self.sortByAlphabeticalAToZList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to sort galleries by alphabetical A-Z")
                return                                  
        
            writeToLog("INFO","Step 5: Going to sort galleries by alphabetical Z-A")
            if self.common.category.verifySortInGalleries(enums.ChannelsSortBy.ALPHABETICAL_Z_A_NEWUI, self.sortByAlphabeticalZToAList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to sort galleries by alphabetical Z-A")
                return 
            
            writeToLog("INFO","Step 6: Going to sort galleries by members & subscribers")
            if self.common.category.verifySortInGalleries(enums.ChannelsSortBy.MEMBERS_AND_SUBSCRIBERS, self.sortByMembersAndSubscribers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to sort galleries by members & subscribers")
                return 
            
            writeToLog("INFO","Step 7: Going to sort galleries by media count")
            if self.common.category.verifySortInGalleries(enums.ChannelsSortBy.MEDIA_COUNT_NEWUI, self.sortByMediaCount) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to sort galleries by media count")
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
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesToDelete)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')