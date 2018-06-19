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
    # Test Name : Categories - Browse channels
    # Test description:
    # create new category
    # create new channel and assigned it to the category that was created - add to the channel entries / members / subscribers.
    # Go to your category click on 'Browse Channels' link - The channels that are assigned to the category should be displayed and all channel info should be correct
    #================================================================================================================================
    testNum = "722"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    userName1 = "Automation_User_1"
    userPass1 = "Kaltura1!"
    categoryName = "Category - Browse channels"
    channelName = "Browse channels"

    
    
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
            self.entryName = clsTestService.addGuidToString("Categories - Browse channels", self.testNum)
            self.channelName = clsTestService.addGuidToString(self.channelName, self.testNum)
            self.categoryName = clsTestService.addGuidToString(self.categoryName, self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create new category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, 'description', 'tags')
           
            writeToLog("INFO","Step 2: Going to clear cache in admin page") 
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to clear cache in admin page")
                return

            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return
                        
            writeToLog("INFO","Step 4: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, False, True, True, linkToCategoriesList=self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED create new channel: " + self.channelName)
                return
            
            writeToLog("INFO","Step 5: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED failed to upload entry")
                return
                  
            writeToLog("INFO","Step 6: Going to publish entry to channel")
            if self.common.myMedia.publishSingleEntry(self.entryName, "", [self.channelName], publishFrom = enums.Location.MY_MEDIA, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED publish entry '" + self.entryName + "' to channel: " + self.channelName)
                return
            
            writeToLog("INFO","Step 7: Going to add user '" + self.userName1 +"' as member to channel '" + self.channelName + "'")
            if self.common.channel.addMembersToChannel(self.channelName1, self.userName1, permission=enums.ChannelMemberPermission.MEMBER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to add user '" + self.userName1 + "' as member to channel '" + self.channelName + "'")
                return               
                           
            sleep(2)
            writeToLog("INFO","Step 8: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to logout from main user")
                return  
                            
            writeToLog("INFO","Step 9: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to login with " + self.userName1)
                return                 
                           
            writeToLog("INFO","Step 10: Going to add user '" + self.userName1 +"' as channel subscriber in '" + self.channelName + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to add user '" + self.userName1 + "' as channel subscriber in '" + self.channelName + "'")
                return             
            
            sleep(2)
            writeToLog("INFO","Step 11: Going to logout from user: " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to logout from user: " + self.userName1)
                return  
                            
            writeToLog("INFO","Step 12: Going to login with main user")
            if self.common.loginAsUser()  == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to login with main user")
                return 
                           
            writeToLog("INFO","Step 13: Going navigate to category")  
            if self.common.category.navigateToCategory(self.categoryName) == False:
                writeToLog("INFO","Step 13: FAILED navigate to category: " + self.categoryName[0])
                return

            writeToLog("INFO","Step 12: FAILED navigate to category: " + self.categoryName[0])
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Categories - Browse channels' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.channel.deleteChannel(self.channelName)
            self.common.apiClientSession.deleteCategory(self.categoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')