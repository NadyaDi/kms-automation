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
    REACH_CAPTIONS_REQUESTS_TABLE                            = ('css', 'div.rt-tbody')
    REACH_ORDER_CAPTIONS_BTN                                 = ('css', 'button.order-btn btn btn-primary pull-right ')
    REACH_SUBMIT_ORDER_CAPTIONS_BTN                          = ('ccs', 'button.btn btn-primary order-form__submit-button  ')
    REACH_INSTRUCTIONS_AND_NOTES_FIELD                       = ('css', 'textarea.span12 order-form__instructions-textarea')
    REACH_CAPTIONS_REQUESTS_ROW_ARROW_OPEN                   = ('xpath', '//i[@class="kmsr-arrow-right"]')
    REACH_CAPTIONS_REQUESTS_DETAILS                          = ('css', 'div.task-details')
    REACH_CANCEL_CAPTIONS_REQUEST_BUTTON                     = ('xpath', '//button[@data-action="deleteTask"]')
    REACH_APPROVE_CANCELATION_OF_CAPTIONS_REQUEST            = ('xpath', '//a[@class="btn btn-danger" and text()="Yes"]')
    REACH_EDIT_CAPTIONS_BTN                                  = ('xpath', '//button[@data-action="editCaption"]')
    REACH_CAPTIONS_EDITOR_PAGE_HEADER                        = ('xpath', '//h1[@text()="Closed Captions Editor"]')
    #=============================================================================================================
    
    # @Author: Inbar Willman
    # Verify that correct captions request data is displayed
    # Verify that correct message is displayed if there are no captions requests
    # isCaptionsRequestsEmpty=boolean. False if there are no captions requests
    # captionsRequestRowData = List. Contains captions request data: Request date, Service type(string), Language(string) status(string)
    # captionsRequestDetails = List. Contains Requester(string),Feature(enums.OrderCaptionsFeatureOptions), TurnAroundTime(enums.OrderCaptionsTurnaroundTimeOptions)
    def verifyCaptionsRequestsSection(self,isCaptionsRequestsEmpty=False, captionsRequestRowData=[], captionsRequestDetails=[], entryName='', forceNavigate=False):
        if forceNavigate == True:
            if self.clsCommon.entryPage.chooseCaptionsRequestsOption(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to choose 'Captions Requests' option")
                return False         

        if isCaptionsRequestsEmpty == True:
            if self.wait_element(self.REACH_NO_REQUESTS_FOUND_MESSAGE) == False:
                writeToLog("INFO","FAILED to displayed 'No requests were found' message")
                return False 
            
        else:
            if self.verifyCaptionsRequestsTableRow(captionsRequestRowData) == False:
                writeToLog("INFO","FAILED to displayed correct data in caption requests table")
                return False   
            
            if self.verifyCaptionsRequestsDeatails(captionsRequestDetails) == False:
                writeToLog("INFO","FAILED to displayed correct caption requests details")
                return False                               
            
        writeToLog("INFO","'Captions Requests' section was verified successfully")
        return True
    
    
    # @Author: Inbar Willman
    # Verify that correct data is displayed in Captions Requests table rows
    # captionsRequestRowData = List. Contains captions request data: Request date, Service type(string), Language(string) status(string)
    def verifyCaptionsRequestsTableRow(self, captionsRequestRowData=[]):
        tmpRequestDate = captionsRequestRowData[0]
        tmpRequestService = captionsRequestRowData[1]
        tmpRequestLanguage = captionsRequestRowData[2]
        tmpRequestStatus = captionsRequestRowData[3]
            
        # Verify captions requests data in row (request date, service, language, status)
        captionsRequestRow = tmpRequestDate + '\n' + tmpRequestService + '\n' + tmpRequestLanguage + '\n' + tmpRequestStatus
             
        captionsRequestTable = self.wait_element(self.REACH_CAPTIONS_REQUESTS_TABLE)
        if captionsRequestTable == False:
            writeToLog("INFO","FAILED to display captions requests table")
            return False  
           
        if captionsRequestRow not in captionsRequestTable.text:
            writeToLog("INFO","FAILED to display captions request row in table")
            return False 
            
        writeToLog("INFO","'Captions Requests' row was verified successfully")
        return True    
    
    
    # @Author: Inbar Willman
    # Verify that correct details is displayed for specific captions request 
    # captionsRequestDetails = List. Contains Requester(string),Feature(enums.OrderCaptionsFeatureOptions), 
    # TurnAroundTime(enums.OrderCaptionsTurnaroundTimeOptions), captionsRequestRow(int)
    def verifyCaptionsRequestsDeatails(self, captionsRequestDetails=[]):
        tmpRequestRequester = captionsRequestDetails[0]
        tmpRequestFeature = captionsRequestDetails[1]
        tmpRequestTurnaroundTime = captionsRequestDetails[2]
        tmpRequestRow = int(captionsRequestDetails[3])

        tmpArrowButton = self.wait_elements(self.REACH_CAPTIONS_REQUESTS_ROW_ARROW_OPEN)[tmpRequestRow]  
        if tmpArrowButton == False:
            writeToLog("INFO","FAILED to display arrow button for captions request")
            return False
        
        try:
            self.driver.execute_script("arguments[0].click();", tmpArrowButton)
        except Exception:
            writeToLog("INFO", "FAILED to scroll to the BSE Environment element")
            return False                      

        # Verify Captions Requests details after clicking on row right arrow                                                  
        captionsRequestGivenDetails = "Requester: " + tmpRequestRequester + '\n' + "Feature: " + tmpRequestFeature  + '\n' + "Turnaround Time: " + tmpRequestTurnaroundTime
             
        captionsRequestDetails = self.wait_element(self.REACH_CAPTIONS_REQUESTS_DETAILS)
        if captionsRequestDetails == False:
            writeToLog("INFO","FAILED to display captions requests table")
            return False  
           
        if captionsRequestGivenDetails not in captionsRequestDetails.text:
            writeToLog("INFO","FAILED to display captions request details")
            return False 
            
        writeToLog("INFO","'Captions Requests' details section was verified successfully")
        return True    


    # @Author: Inbar Willman - TO DO
    # Order captions via KMS
    # orderCaptionsField = enums.OrderCaptionsFields
    # service = enums.OrderCaptionsServiceOptions 
    # sourceMediaLanguage = enums.OrderCaptionsSourceMediaLanguageOptions
    # feature = enums.OrderCaptionsFeatureOptions
    # turnaroundTime = enums.OrderCaptionsTurnaroundTimeOptions
    def orderCaptionViaKMS(self, service='', sourceMediaLanguage='', feature='', turnaroundTime=''):
#         # Click on 'order' button
#         if self.click(self.REACH_ORDER_CAPTIONS_BUTTON) == False:
#             writeToLog("INFO","FAILED to click on 'Order' button")
#             return False  

        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
        
        # Click on 'Service' dropdown
        tmpServiceDropdown = (self.REACH_ORDER_CAPTIONS_FIELD_DROPDOWN[0], self.REACH_ORDER_CAPTIONS_FIELD_DROPDOWN[1].replace('FIELD_NAME', enums.OrderCaptionsFields.SERVICE.value))  
        if self.click(tmpServiceDropdown) == False:
            writeToLog("INFO","FAILED to click on 'Service' dropdown")
            return False 
        
        tmpServiceOption = (self.REACH_ORDER_CAPTIONS_DROPDOWN_OPTION[0], self.REACH_ORDER_CAPTIONS_DROPDOWN_OPTION[1].replace('DROPDOWN_OPTION', service)) 
        if self.click(tmpServiceOption) == False:
            writeToLog("INFO","FAILED to click on " + service + " option")
            return False             
        
        return True    
    
    
    # @Author: Inbar Willman
    # rowNumber = int. Represent the row number of the captions request in the requests table
    def cancelCaptionsRequest(self, rowNumber,captionsRequestData=[], entryName='', forceNavigate=False):   
        if forceNavigate == True:
            if self.clsCommon.entryPage.chooseCaptionsRequestsOption(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to choose 'Captions Requests' option")
                return False   
        
        tmpCancelButton = self.wait_elements(self.REACH_CANCEL_CAPTIONS_REQUEST_BUTTON)[rowNumber]  
        if tmpCancelButton == False:
            writeToLog("INFO","FAILED to find cancel button")
            return False
        
        try:
            self.driver.execute_script("arguments[0].click();", tmpCancelButton)
        except Exception:
            writeToLog("INFO", "FAILED to click on cancel button")
            return False          
            
        if self.click(self.REACH_APPROVE_CANCELATION_OF_CAPTIONS_REQUEST) == False:
            writeToLog("INFO", "FAILED to click on confirmation cancel button")
            return False  
        
        if self.verifyCaptionsRequestsTableRow(captionsRequestData) == True:
            writeToLog("INFO", "FAILED to cancel captions request, request data is still displayed")
            return False              
        
        writeToLog("INFO","Captions request was successfully deleted")
        return True      
    
    
    # @Author:Inbar Willman
    # rowNumber = int. Represent the row number of the captions request in the requests table
    def navigateToCaptionsEditor(self, entryName='', forceNavigate=False):  
        if forceNavigate == True:
            if self.clsCommon.entryPage.chooseCaptionsRequestsOption(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to choose 'Captions Requests' option")
                return False 
             
        tmpEditButton = self.wait_element(self.REACH_EDIT_CAPTIONS_BTN)
        if tmpEditButton == False:
            writeToLog("INFO","FAILED to find cancel button")
            return False
        
        try:
            self.driver.execute_script("arguments[0].click();", tmpEditButton)
        except Exception:
            writeToLog("INFO", "FAILED to click on cancel button")
            return False              
      
        if self.wait_element(self.REACH_CAPTIONS_EDITOR_PAGE_HEADER) == False:
            writeToLog("INFO", "FAILED to displayed captions editor page")
            return False 
                
        writeToLog("INFO","Navigate to captions editor page successfully")
        return True                             