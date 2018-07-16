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
    # Test Name : My Media - Sort media
    # Test description:
    # upload sevaral entries and add them likes / comments.
    # Sort My Media by:
    #    1. Most Recent - The entries' order should be from the last uploaded video to the first one.
    #    2. Alphabetical - The entries' order should be alphabetical
    #    3. Likes (enable via the Admin page) - The entries' order should be descending by likes' number
    #    4. Comments - The entries' order should be descending by comments' number
    #================================================================================================================================
    testNum = "668"
    
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
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    userName1 = "Automation_User_1"
    userPass1 = "Kaltura1!"
    userName2 = "Automation_User_2"
    userPass2 = "Kaltura1!"
    comments = ["Comment 1", "Comment 2", "Comment 3"]
    categoryName = [("Apps Automation Category")]
    
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
            self.entryName1 = clsTestService.addGuidToString("My Media - Sort A", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("My Media - Sort B", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("My Media - Sort C", self.testNum)
            self.entryName4 = clsTestService.addGuidToString("My Media - Sort D", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to enable like module")            
            if self.common.admin.enablelike(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to enable like module")
                return
                  
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
                 
            for i in range(3,7):
                writeToLog("INFO","Step " + str(i) + ": Going to upload new entry '" + eval('self.entryName'+str(i-2)))            
                if self.common.upload.uploadEntry(self.filePath, eval('self.entryName'+str(i-2)), self.description, self.tags) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to upload new entry " + eval('self.entryName'+str(i-2)))
                    return
                   
            writeToLog("INFO","Step 7: Going to publish entries")    
            if self.common.myMedia.publishEntriesFromMyMedia([self.entryName2, self.entryName4], self.categoryName, "", disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to publish entries to category: " + self.categoryName[0])
                return 
                   
            writeToLog("INFO","Step 8: Going navigate to entry '" + self.entryName1 + "'")    
            if self.common.entryPage.navigateToEntry(self.entryName1, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to entry: " + self.entryName1)
                return 
                       
            writeToLog("INFO","Step 9: Going to like entry: " + self.entryName1)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to like entry: " + self.entryName1)
                return   
                     
            sleep(2) 
            writeToLog("INFO","Step 10: Going to add comments to entry: " + self.entryName1)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to add comments to entry: " + self.entryName1)
                return    
                    
            writeToLog("INFO","Step 11: Going navigate to entry: "+ self.entryName2)    
            if self.common.entryPage.navigateToEntry(self.entryName2, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED navigate to entry: " + self.entryName2)
                return 
                    
            writeToLog("INFO","Step 12: Going to like entry: " + self.entryName2)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to like entry: " + self.entryName2)
                return   
                    
            writeToLog("INFO","Step 13: Going navigate to entry: "+ self.entryName3)    
            if self.common.entryPage.navigateToEntry(self.entryName3, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED navigate to entry: " + self.entryName3)
                return 
                    
            sleep(2) 
            writeToLog("INFO","Step 14: Going to add comments to entry: " + self.entryName3)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to add comments to entry: " + self.entryName3)
                return    
                    
            writeToLog("INFO","Step 15: Going navigate to entry: "+ self.entryName4)    
            if self.common.entryPage.navigateToEntry(self.entryName4, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED navigate to entry: " + self.entryName4)
                return 
                    
            writeToLog("INFO","Step 16: Going to like entry: " + self.entryName4)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to like entry: " + self.entryName4)
                return 
                    
            sleep(2) 
            writeToLog("INFO","Step 17: Going to add comment to entry: " + self.entryName4)  
            if self.common.entryPage.addComment("Comment 1") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to add comment to entry: " + self.entryName4)
                return    
                    
            sleep(3)
            writeToLog("INFO","Step 18: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to logout from main user")
                return  
                                           
            writeToLog("INFO","Step 19: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to login with " + self.userName1)
                return
                       
            writeToLog("INFO","Step 20: Going navigate to entry: "+ self.entryName2)    
            if self.common.entryPage.navigateToEntry(self.entryName2, enums.Location.CATEGORY_PAGE, self.categoryName[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED navigate to entry: " + self.entryName2)
                return 
                       
            writeToLog("INFO","Step 21: Going to like entry: " + self.entryName2)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to like entry: " + self.entryName2)
                return    
                       
            writeToLog("INFO","Step 22: Going navigate to entry: "+ self.entryName4)    
            if self.common.entryPage.navigateToEntry(self.entryName4, enums.Location.CATEGORY_PAGE, self.categoryName[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED navigate to entry: " + self.entryName4)
                return 
                       
            writeToLog("INFO","Step 23: Going to like entry: " + self.entryName4)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to like entry: " + self.entryName4)
                return  
                       
            sleep(3)
            writeToLog("INFO","Step 24: Going to logout from : " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to logout from: " + self.userName1)
                return  
                                           
            writeToLog("INFO","Step 25: Going to login with user " + self.userName2)
            if self.common.login.loginToKMS(self.userName2, self.userPass2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25: FAILED to login with " + self.userName2)
                return
                       
            writeToLog("INFO","Step 26: Going navigate to entry: "+ self.entryName2)    
            if self.common.entryPage.navigateToEntry(self.entryName2, enums.Location.CATEGORY_PAGE, self.categoryName[0]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26: FAILED navigate to entry: " + self.entryName2)
                return 
                       
            writeToLog("INFO","Step 27: Going to like entry: " + self.entryName2)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27: FAILED to like entry: " + self.entryName2)
                return    
                       
            sleep(3)
            writeToLog("INFO","Step 28: Going to logout from : " + self.userName2)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28: FAILED to logout from: " + self.userName2)
                return                   
                     
            writeToLog("INFO","Step 29: Going to login with main user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 29: FAILED to login with main user")
                return
              
            writeToLog("INFO","Step 30: Going navigate to my media")    
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 30: FAILED navigate to my media")
                return 
            
            
            writeToLog("INFO","Step 31: Going to sort my media by: Alphabetical")  
            if self.common.myMedia.verifySortInMyMedia(enums.SortBy.ALPHABETICAL, (self.entryName1, self.entryName2, self.entryName3, self.entryName4)) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 31: FAILED to sort my media by Alphabetical")
                return 
              
            sleep(1)
              
            if self.common.isElasticSearchOnPage() == True:  
                writeToLog("INFO","Step 32: Going to sort my media by: Most recent")
                if self.common.myMedia.verifySortInMyMedia(enums.SortBy.CREATION_DATE_DESC, (self.entryName4, self.entryName3, self.entryName2, self.entryName1)) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 32: FAILED to sort my media by Most recent")
                    return
            else:
                writeToLog("INFO","Step 32: Going to sort my media by: Most recent")   
                if self.common.myMedia.verifySortInMyMedia(enums.SortBy.MOST_RECENT , (self.entryName4, self.entryName3, self.entryName2, self.entryName1)) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 32: FAILED to sort my media by Most recent")
                    return
         
            sleep(1)
            writeToLog("INFO","Step 33: Going to sort my media by: comments")    
            if self.common.myMedia.verifySortInMyMedia(enums.SortBy.COMMENTS, (self.entryName3, self.entryName1, self.entryName4, self.entryName2)) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 33: FAILED to sort my media by comments")
                return
            
            sleep(1)
            writeToLog("INFO","Step 34: Going to sort my media by: Likes")    
            if self.common.myMedia.verifySortInMyMedia(enums.SortBy.LIKES, (self.entryName2, self.entryName4, self.entryName1, self.entryName3)) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 34: FAILED to sort my media by Likes")
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'My Media - Sort' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            if localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN != "QA APPLICATION":
                self.common.login.logOutOfKMS()
                self.common.loginAsUser()
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')