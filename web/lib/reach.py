from base import *
import clsTestService
import enums
from logger import writeToLog
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

class Reach(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Reach locators:
    #=============================================================================================================
    REACH_NO_REQUESTS_FOUND_MESSAGE                          = ('xpath', '//div[@class="message__text" and text()="No requests were found"]')
    REACH_CAPTIONS_REQUESTS_REQUEST_DATE_FIELD               = ('xpath', '//div[@class="createdAt requests-table-cell" and text()="DATE"]')
    REACH_CAPTIONS_REQUESTS_SERVICE_FIELD                    = ('xpath', '//span[@class="enum-renderer__text" and text()="SERVICE"]')
    REACH_CAPTIONS_REQUESTS_LANGUAGE_FIELD                   = ('xpath', '//div[@class="requests-table-cell" and text()="LANGUAGE"]')
    REACH_CAPTIONS_REQUESTS_STATUS_FIELD                     = ('xpath', '//span[@class="enum-renderer__text" and text()="STATUS"]')
    REACH_CAPTIONS_REQUESTS_TABLE                            = ('css', 'div.rt-tbody')
    #=============================================================================================================
    
    # @Author: Inbar Willman
    # Verify that correct captions request data is displayed
    # Verify that correct message is displayed if there are no captions requests
    # isCaptionsRequestsEmpty=boolean. False if there are no captions requests
    # captionsRequestData = List. Contains captions request data: Request date, Service type(string), Language(string), status(string) and row number(int)
    def verifyCaptionsRequestsSection(self,isCaptionsRequestsEmpty=False, captionsRequestData=[], entryName='', forceNavigate=False):
        if forceNavigate == True:
            if self.clsCommon.entryPage.chooseCaptionsRequestsOption(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to choose 'Captions Requests' option")
                return False         
        
        if isCaptionsRequestsEmpty == True:
            if self.wait_element(self.REACH_NO_REQUESTS_FOUND_MESSAGE) != False:
                writeToLog("INFO","FAILED to displayed 'No requests were found' message")
                return False  
        
        else:
#             tmpRequestDate = captionsRequestData[0]
#             tmpRequestService = captionsRequestData[1]
#             tmpRequestLanguage = captionsRequestData[2]
#             tmpRequestStatus = captionsRequestData[3]
#             tmpRowNumber = captionsRequestData[4]
#             
            reachCaptionsTable = self.wait_element(self.REACH_CAPTIONS_REQUESTS_TABLE)
            if reachCaptionsTable == False:
                writeToLog("INFO","FAILED to display captions requests table")
                return False  
            
            reachCaptionsTable.text            
            
            # Verify that request date is displayed
#             captionsRequestsRequestDate = (self.REACH_CAPTIONS_REQUESTS_REQUEST_DATE_FIELD[0], self.REACH_CAPTIONS_REQUESTS_REQUEST_DATE_FIELD[1].replace('DATE', tmpRequestDate)) 
#             if self.wait_element(captionsRequestsRequestDate)[tmpRowNumber] == False:
#                 writeToLog("INFO","FAILED to display correct request date")
#                 return False   
            
            # Verify that service type is displayed
#             captionsRequestsService = (self.REACH_CAPTIONS_REQUESTS_SERVICE_FIELD[0], self.REACH_CAPTIONS_REQUESTS_SERVICE_FIELD[1].replace('SERVICE', tmpRequestService)) 
#             if self.wait_element(captionsRequestsService)[tmpRowNumber] == False:
#                 writeToLog("INFO","FAILED to display correct request date")
#                 return False                            
            
            
        
        writeToLog("INFO","'Captions Requests' section was verified successfully")
        return True
