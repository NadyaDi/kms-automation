import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
from KalturaClient.Plugins.Core import KalturaPrivacyType, KalturaContributionPolicyType, KalturaAppearInListType
import enums
from upload import UploadEntry


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : Categories - Sort media on category page
    # Test description:
    # Create category 
    # upload several entries and add comment and likes
    # GO to category and sort Media by :
    #    1. Most Recent -  The entries' order should be from the last uploaded video to the first one.
    #    2. Alphabetical - The entries' order should be alphabetical
    #    3. Comment -      The entries' order should be descending by comments number
    #    4. Like  -        The entries' order should be descending by Likes' number
    #================================================================================================================================
    testNum = "1025"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description"
    tags = "Tags,"
    categoryName = None
    entryName = None
    filePath= localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\audio.mp3'
    userName1 = "Automation_User_1"
    userPass1 = "Kaltura1!"
    userName2 = "Automation_User_2"
    userPass2 = "Kaltura1!"
    comments = ["Comment 1", "Comment 2", "Comment 3"]

    
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
            self.categoryName = clsTestService.addGuidToString("Sort media on category page", self.testNum)
            self.entryName1 = clsTestService.addGuidToString("Sort Media In Category - Sort A", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Sort Media In Category - Sort B", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("Sort Media In Category - Sort C", self.testNum)
            self.entryName4 = clsTestService.addGuidToString("Sort Media In Category - Sort D", self.testNum)    
            
            self.sortAlphabetical = [self.entryName1, self.entryName2, self.entryName3, self.entryName4]
            self.sortMostRecent = [self.entryName4, self.entryName3, self.entryName2, self.entryName1]
            self.sortComments = [self.entryName3, self.entryName1, self.entryName4, self.entryName2]
            self.sortLikes = [self.entryName2, self.entryName4, self.entryName1, self.entryName3]   
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.description, None) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create category")
                return
            
            writeToLog("INFO","Step 2: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return     
            
            for i in range(4,8):
                writeToLog("INFO","Step " + str(i) + ": Going to upload new entry '" + eval('self.entryName'+str(i-3)))            
                if self.common.upload.uploadEntry(self.filePath, eval('self.entryName'+str(i-3)), self.description, self.tags) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to upload new entry " + eval('self.entryName'+str(i-3)))
                    return
                   
            writeToLog("INFO","Step 8: Going to publish entries")    
            if self.common.myMedia.publishEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4], [self.categoryName], "", disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to publish entries to category: " + self.categoryName[0])
                return 
            
            writeToLog("INFO","Step 9: Going navigate to entry '" + self.entryName1 + "'")    
            if self.common.entryPage.navigateToEntry(self.entryName1, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED navigate to entry: " + self.entryName1)
                return 
                       
            writeToLog("INFO","Step 10: Going to like entry: " + self.entryName1)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to like entry: " + self.entryName1)
                return   
                     
            sleep(2) 
            writeToLog("INFO","Step 11: Going to add comments to entry: " + self.entryName1)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to add comments to entry: " + self.entryName1)
                return    
                    
            writeToLog("INFO","Step 12: Going navigate to entry: "+ self.entryName2)    
            if self.common.entryPage.navigateToEntry(self.entryName2, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED navigate to entry: " + self.entryName2)
                return 
                    
            writeToLog("INFO","Step 13: Going to like entry: " + self.entryName2)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to like entry: " + self.entryName2)
                return   
                    
            writeToLog("INFO","Step 14: Going navigate to entry: "+ self.entryName3)    
            if self.common.entryPage.navigateToEntry(self.entryName3, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED navigate to entry: " + self.entryName3)
                return 
                    
            sleep(2) 
            writeToLog("INFO","Step 15: Going to add comments to entry: " + self.entryName3)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to add comments to entry: " + self.entryName3)
                return    
                    
            writeToLog("INFO","Step 16: Going navigate to entry: "+ self.entryName4)    
            if self.common.entryPage.navigateToEntry(self.entryName4, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED navigate to entry: " + self.entryName4)
                return 
                    
            writeToLog("INFO","Step 17: Going to like entry: " + self.entryName4)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to like entry: " + self.entryName4)
                return 
                    
            sleep(2) 
            writeToLog("INFO","Step 20: Going to add comment to entry: " + self.entryName4)  
            if self.common.entryPage.addComment("Comment 1") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to add comment to entry: " + self.entryName4)
                return    
                    
            sleep(3)
            writeToLog("INFO","Step 21: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to logout from main user")
                return  
                                           
            writeToLog("INFO","Step 22: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to login with " + self.userName1)
                return
                       
            writeToLog("INFO","Step 23: Going navigate to entry: "+ self.entryName2)    
            if self.common.entryPage.navigateToEntry(self.entryName2, enums.Location.CATEGORY_PAGE, self.categoryName[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED navigate to entry: " + self.entryName2)
                return 
                       
            writeToLog("INFO","Step 24: Going to like entry: " + self.entryName2)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to like entry: " + self.entryName2)
                return    
                       
            writeToLog("INFO","Step 25: Going navigate to entry: "+ self.entryName4)    
            if self.common.entryPage.navigateToEntry(self.entryName4, enums.Location.CATEGORY_PAGE, self.categoryName[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25: FAILED navigate to entry: " + self.entryName4)
                return 
                       
            writeToLog("INFO","Step 26: Going to like entry: " + self.entryName4)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26: FAILED to like entry: " + self.entryName4)
                return  
            
            sleep(3)
            writeToLog("INFO","Step 27: Going to logout from : " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27: FAILED to logout from: " + self.userName1)
                return  
                                           
            writeToLog("INFO","Step 28: Going to login with user " + self.userName2)
            if self.common.login.loginToKMS(self.userName2, self.userPass2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28: FAILED to login with " + self.userName2)
                return
                       
            writeToLog("INFO","Step 29: Going navigate to entry: "+ self.entryName2)    
            if self.common.entryPage.navigateToEntry(self.entryName2, enums.Location.CATEGORY_PAGE, self.categoryName[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 29: FAILED navigate to entry: " + self.entryName2)
                return 
                       
            writeToLog("INFO","Step 30: Going to like entry: " + self.entryName2)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 30: FAILED to like entry: " + self.entryName2)
                return    
            
            sleep(3)
            writeToLog("INFO","Step 31: Going to logout from : " + self.userName2)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 31: FAILED to logout from: " + self.userName2)
                return                   
                     
            writeToLog("INFO","Step 32: Going to login with main user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 32: FAILED to login with main user")
                return
            
            writeToLog("INFO","Step 33: Going navigate to category page")    
            if self.common.category.navigateToCategory(self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 33: FAILED navigate to category page")
                return 
            
            writeToLog("INFO","Step 34: Going to sort in category by: Alphabetical")  
            if self.common.myMedia.verifySortInMyMedia(enums.SortBy.ALPHABETICAL, self.sortAlphabetical) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 34: FAILED to sort in category by Alphabetical")
                return 
            sleep(1)
              
            if self.common.isElasticSearchOnPage() == True:  
                writeToLog("INFO","Step 35: Going to sort in category by: Most recent")
                if self.common.myMedia.verifySortInMyMedia(enums.SortBy.CREATION_DATE_DESC, self.sortMostRecent) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 35: FAILED to sort in category by Most recent")
                    return
            else:
                writeToLog("INFO","Step 36: Going to sort in category by: Most recent")   
                if self.common.myMedia.verifySortInMyMedia(enums.SortBy.MOST_RECENT , self.sortMostRecent) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 36: FAILED to sort in category by Most recent")
                    return
            sleep(1)
            
            writeToLog("INFO","Step 37: Going to sort in category by: comments")    
            if self.common.myMedia.verifySortInMyMedia(enums.SortBy.COMMENTS, self.sortComments) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 37: FAILED to sort in category by comments")
                return
            sleep(1)
            
            writeToLog("INFO","Step 38: Going to sort in category by: Likes")    
            if self.common.myMedia.verifySortInMyMedia(enums.SortBy.LIKES, self.sortLikes) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 38: FAILED to sort in category by Likes")
                return
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Categories - Sort media on category page' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")        
            self.common.myMedia.deleteEntriesFromMyMedia((self.entryName1, self.entryName2, self.entryName3, self.entryName4), showAllEntries=True)       
            self.common.apiClientSession.deleteCategory(self.catagoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')