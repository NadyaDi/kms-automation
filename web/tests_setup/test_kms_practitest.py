import pytest
import sys,os
from utilityTestFunc import *
from clsPractiTest import clsPractiTest
import clsTestService

class Test:
    
    #=============================================================================================================
    #This is the test that does setup
    #=============================================================================================================
    localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.MEDIA_SPACE
    practiTest = clsPractiTest()
    testNum     = "kms_practitest"
    status      = "Fail"   
    
    
    def test_01(self,env):
        
        os.environ["RUNNING_TEST_ID"] = self.testNum 
        
        try:
            self.startTime = time.time() 
            writeToLog("INFO","************************************************************************************************************************")
            writeToLog("INFO","Start setup test test_kms_practitest")            
            
            prSessionInfo = self.practiTest.getPractiTestAutomationSession()
            if (prSessionInfo["sessionSystemID"] != -1):
                testIDsDct = self.practiTest.getPractiTestSessionInstances(prSessionInfo)
                if (len (testIDsDct) > 0):
                    self.practiTest.createAutomationTestSetFile(prSessionInfo["hostname"], prSessionInfo["environment"], prSessionInfo["setPlatform"], testIDsDct)
                else:
                    writeToLog("INFO","Unable to get test list")
                    return
                                    
                if (self.practiTest.setTestSetAutomationStatusAsProcessed(prSessionInfo["sessionSystemID"]) != True):
                    writeToLog("INFO","Unable to set test set as processed") 
                    return
                
                self.status = 'Pass'
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
                
    def teardown_method(self,method):
        
        duration = str(round(time.time() - self.startTime))
        writeToLog("INFO","test_" + self.testNum + ": " + self.status + " (" + duration + " sec)")
        assert (self.status == "Pass")   
        
    pytest.main('test_' + testNum  + '.py --tb=line')
         
