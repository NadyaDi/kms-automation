import pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','lib')))
from utilityTestFunc import *
from clsPractiTest import clsPractiTest
import clsTestService

class Test:
    
    #=============================================================================================================
    #This is the test that gets all test sets from PractiTest that need to be executed 
    #=============================================================================================================
    localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.PITCH
    practiTest = clsPractiTest()
    testNum     = "pitch_practitest"
    status      = "Fail"   
    
    # Update the PractiTest variables by the Project name
    
    def test_01(self,env):
        
        os.environ["RUNNING_TEST_ID"] = self.testNum 
        
        try:
            self.startTime = time.time() 
            writeToLog("INFO","************************************************************************************************************************")
            writeToLog("INFO","Start setup test pitch_practitest")            
            
            prSessionInfo = self.practiTest.getPractiTestAutomationSession()
            if (prSessionInfo["sessionSystemID"] != -1):
                testIDsDct = self.practiTest.getPractiTestSessionInstances(prSessionInfo)
                if (len (testIDsDct) > 0):
                    self.practiTest.createAutomationTestSetFile(prSessionInfo["hostname"], prSessionInfo["environment"], prSessionInfo["setPlatform"], testIDsDct)
                else:
                    writeToLog("INFO","Unable to get test list")
                                    
                if (self.practiTest.setTestSetAutomationStatusAsProcessed(prSessionInfo["sessionSystemID"]) != True):
                    self.status = "Fail"
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
         
