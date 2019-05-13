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
    REACH_ORDER_CAPTIONS_FIELD_DROPDOWN                      = ('xpath', '//span[@class="order-form__drop-down--label" and text()="FIELD_NAME:"]/descendant::div[@class="css-2ib6dj control"]')
    REACH_ORDER_CAPTIONS_DROPDOWN_OPTION                     = ('xpath', '//div[@class="css-va7pk8" and text()="DROPDOWN_OPTION"]')
    REACH_ORDER_CAPTIONS_BUTTON                              = ('css', 'button.order-btn btn btn-primary pull-right ')
    #=============================================================================================================
    
    # @Author: Inbar Willman
    # Verify that correct captions request data is displayed
    # Verify that correct message is displayed if there are no captions requests
    # isCaptionsRequestsEmpty=boolean. False if there are no captions requests
    # captionsRequestData = List. Contains captions request data: Request date, Service type(string), Language(string) and status(string)
    def verifyCaptionsRequestsSection(self,isCaptionsRequestsEmpty=False, captionsRequestData=[], entryName='', forceNavigate=False):
        if forceNavigate == True:
            if self.clsCommon.entryPage.chooseCaptionsRequestsOption(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to choose 'Captions Requests' option")
                return False         
        
        if isCaptionsRequestsEmpty == True:
            if self.wait_element(self.REACH_NO_REQUESTS_FOUND_MESSAGE) == False:
                writeToLog("INFO","FAILED to displayed 'No requests were found' message")
                return False  
        
        else:
            tmpRequestDate = captionsRequestData[0]
            tmpRequestService = captionsRequestData[1]
            tmpRequestLanguage = captionsRequestData[2]
            tmpRequestStatus = captionsRequestData[3]
            
            captionsRequestRow = tmpRequestDate + '\n' + tmpRequestService + '\n' + tmpRequestLanguage + '\n' + tmpRequestStatus
             
            reachCaptionsTable = self.wait_element(self.REACH_CAPTIONS_REQUESTS_TABLE)
            if reachCaptionsTable == False:
                writeToLog("INFO","FAILED to display captions requests table")
                return False  
            
            if captionsRequestRow not in reachCaptionsTable.text:
                writeToLog("INFO","FAILED to display captions request row in table")
                return False                                                  
        
        writeToLog("INFO","'Captions Requests' section was verified successfully")
        return True


    # @Author: Inbar Willman
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