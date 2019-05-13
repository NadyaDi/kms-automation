import pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from utilityTestFunc import *
from clsPractiTest import clsPractiTest
import clsTestService
from collections import OrderedDict

class Test:
    
    #===================================================================================================================================
    # This script if for test automation night run, which is triggered from Jenkins at night.
    # Sets all testsets under specified filter ('Night Run' under current version), to Pending and disable 'Automation Run Only FAILED'.
    # Sets all tests in each testset to No Run
    #===================================================================================================================================
    localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST = enums.Application.PITCH
    practiTest          = clsPractiTest()
    testNum             = "run_all"
    status              = "Pass"   
    filter              = localSettings.LOCAL_SETTINGS_PRACTITEST_NIGHT_RUN_FILTER_ID
    onlyExecuteAtNight  = localSettings.LOCAL_SETTINGS_PRACTITEST_ONLY_EXECUTE_AT_NIGHT
    
    def test_01(self,env):
        try:
            # Get all Testset under specified Filter ID
            writeToLog("INFO","Going to get all testsets instance ids under filter " + self.filter)
            testSetList = self.practiTest.getPractiTestTestSetByFilterId(self.filter, onlyExecuteAtNight=self.onlyExecuteAtNight)
            if testSetList == False:
                writeToLog("INFO","FAILED to get all testsets instance ids under filter " + self.filter)
                self.status = "Fail"                    
              
            writeToLog("INFO","Going to set No Run status to all testsets under filter " + self.filter)            
            if self.practiTest.setStatusToEntireTestset(testSetList, self.practiTest.TEST_STATUS.NO_RUN) == False:
                writeToLog("INFO","FAILED to set No Run status to all testset under filter " + self.filter)
                self.status = "Fail"
                  
            writeToLog("INFO","Going to set 'Automation Status' as 'Pending' to all testsets under filter " + self.filter)
            writeToLog("INFO","Going to set 'Automation Run Only FAILED ' as 'False' to all testsets under filter " + self.filter)
            customFiledsDict =  OrderedDict({'---f-30327':'Pending', '---f-38033':'no'})          
            if self.practiTest.updateTestsetsCustomFields(testSetList, customFiledsDict) == False:
                writeToLog("INFO","FAILED to set 'Automation Status' as 'Pending' to all testsets under filter " + self.filter)           
                self.status = "Fail"                

         
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst)
                
    def teardown_method(self,method):
        assert (self.status == "Pass")   
        
    pytest.main('test_' + testNum  + '.py --tb=line')
         
