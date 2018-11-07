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
    # Test Name : Setup test for eSearch
    # Test description:
    # Update galleries for sort by in galleries
    #================================================================================================================================
    testNum = "8"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    filePathForSortBy = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    channelDescription = "Description"
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
            # Galleries for sort by in galleris
            self.galleryName1 = "1 - First gallery"
            self.galleryName2 = "2 - second gallery"
            self.galleryName3 = "3 - third gallery"
            self.galleryName4 = "4 - forth gallery"
            
            # Entries to publish to channels for sort by in Channels/My channels 
            self.entryName1 = "Sort Galleries 1"
            self.entryName2 = "Sort Galleries 2"
            self.entryName3 = "Sort Galleries 3"
            ##################### TEST STEPS - MAIN FLOW #############################################################  
            # Create channels for sort by in channels/My channels
            writeToLog("INFO","Creating channels for sort by in channels/My channels")
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return      
                          
            for i in range(1,4):
                writeToLog("INFO","Step " + str(i+1) + ": Going to upload new entry '" + eval('self.entryName'+str(i)))            
                if self.common.upload.uploadEntry(self.filePath, eval('self.entryName'+str(i)), self.entryDescription, self.entryTags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i+1) + ": FAILED to upload new entry: " + eval('self.entryName'+str(i)))
                    return
                        
            writeToLog("INFO","Step 5: Going to publish entry: " + self.entryName1)            
            if self.common.myMedia.publishSingleEntry(self.entryName1, (self.galleryName1, self.galleryName2, self.galleryName4), "") == False: 
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to publish entry: " + self.entryName1)
                return
                      
            writeToLog("INFO","Step 6: Going to publish entry: " + self.entryName2)            
            if self.common.myMedia.publishSingleEntry(self.entryName2, (self.galleryName2, self.galleryName4), "") == False: 
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to publish entry: " + self.entryName2)
                return
                      
            writeToLog("INFO","Step 7: Going to publish entry: " + self.entryName3)            
            if self.common.myMedia.publishSingleEntry(self.entryName3, [(self.galleryName2)], "") == False: 
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to publish entry: " + self.entryName2)
                return
                        
            writeToLog("INFO","Step 8: Going to add user " + self.userName2+  " as members in gallery " + self.galleryName2)
            if self.common.category.addMemberToCategory(self.galleryName2, self.userName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to add user " + self.userName2 +  " as members in gallery " + self.galleryName2)
                return
            
            writeToLog("INFO","Step 9: Going to add user " + self.userName3+  " as members in gallery " + self.galleryName2)
            if self.common.category.addMemberToCategory(self.galleryName2, self.userName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to add user " + self.userName3 +  " as members in gallery " + self.galleryName2)
                return 
            
            writeToLog("INFO","Step 10: Going to add user " + self.userName4+  " as members in gallery " + self.galleryName2)
            if self.common.category.addMemberToCategory(self.galleryName2, self.userName4) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to add user " + self.userName4 +  " as members in gallery " + self.galleryName2)
                return    
            
            writeToLog("INFO","Step 11: Going to add user " + self.userName2 +  " as members in gallery " + self.galleryName1)
            if self.common.category.addMemberToCategory(self.galleryName1, self.userName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to add user " + self.userName2 +  " as members in gallery " + self.galleryName1)
                return
            
            writeToLog("INFO","Step 12: Going to add user " + self.userName3 +  " as members in gallery " + self.galleryName1)
            if self.common.category.addMemberToCategory(self.galleryName1, self.userName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to add user " + self.userName3 +  " as members in gallery " + self.galleryName1)
                return            
                     
            writeToLog("INFO","Step 10: Going to add user " + self.userName3 + " as member to gallery " + self.galleryName3)
            if self.common.category.addMemberToCategory(self.galleryName3, self.userName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to add user " + self.userName3 + " as members to gallery " + self.galleryName3)
                return      
                     
            writeToLog("INFO","Galleries for sort by were updated successfully")
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