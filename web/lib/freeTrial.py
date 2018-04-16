from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from base import *
import clsTestService
import enums
from general import General


class  FreeTrial(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #                                   Free Trial locators:                                                        #
    #=============================================================================================================
    FREE_TRIAL_PARTNER_ID_TEXTBOX                               = ('id', 'partnerId')
    FREE_TRIAL_ADMIN_SECRET_TEXTBOX                             = ('id', 'adminSecret')
    FREE_TRIAL_INSTANCEID_TEXTBOX                               = ('id', 'instanceId')
    FREE_TRIAL_COMPANY_NAME_TEXTBOX                             = ('id', 'company')
    FREE_TRIAL_HOSTNAME_TEXTBOX                                 = ('id', 'hostname')
    FREE_TRIAL_APPLICATION_TEXTBOX                              = ('id', 'applicationProfile')
    FREE_TRIAL_SUBMIT_BUTTON                                    = ('xpath', "//input[@id='saveForm' and @class='button_text']")
    FREE_TRIAL_CONFIRM_INSTANCE_CREATION                        = ('xpath', "//pre[contains(text(),'Creating site...\nSite created with ID')]")
                                                                   
    #============================================================================================================
    
    def createFreeTrialInctance(self, partnerId, adminSecret, instanceId, company, hostname, application):
        if self.send_keys(self.FREE_TRIAL_PARTNER_ID_TEXTBOX, partnerId) == False:
                writeToLog("INFO","FAILED to insert partner Id '" + partnerId + "'")
                return False
            
        if self.send_keys(self.FREE_TRIAL_ADMIN_SECRET_TEXTBOX, adminSecret) == False:
                writeToLog("INFO","FAILED to insert admin secret '" + adminSecret + "'")
                return False

        if self.send_keys(self.FREE_TRIAL_INSTANCEID_TEXTBOX, instanceId) == False:
                writeToLog("INFO","FAILED to insert instance Id '" + instanceId + "'")
                return False
            
        if self.send_keys(self.FREE_TRIAL_COMPANY_NAME_TEXTBOX, company) == False:
                writeToLog("INFO","FAILED to insert company '" + company + "'")
                return False
            
        if self.send_keys(self.FREE_TRIAL_HOSTNAME_TEXTBOX, hostname) == False:
                writeToLog("INFO","FAILED to insert host name '" + hostname + "'")
                return False
            
        if self.select_from_combo_by_text(self.FREE_TRIAL_APPLICATION_TEXTBOX, application) == False:
                writeToLog("INFO","FAILED to choose application '" + hostname + "'")
                return False
        
        if self.click(self.FREE_TRIAL_SUBMIT_BUTTON, 20) == False:
                writeToLog("INFO","FAILED to click on submit button")
                return False
        
        # wait until the creating process is done
        if self.wait_visible(self.FREE_TRIAL_CONFIRM_INSTANCE_CREATION, 120) == False:
                writeToLog("INFO","FAILED to find create instance message confirm")
                return False
            
        writeToLog("INFO","Success, instance " + instanceId + " was created successfully")
        return True
    
    
    def setInstanceNumber(self, instanceNumberFilePath):
        try:
            # read the current instance number
            instanceFile = open(instanceNumberFilePath,'r')
            tempInstance = instanceFile.read()
            instanceFile.close()
              
            #  raise the instance number be 1 and update the file  
            instanceFile = open(instanceNumberFilePath,'w')
            tmp = tempInstance.split('-')
            number = int(tmp[1]) + 1
            instanceNumber = tmp[0] + "-" + str(number)
            instanceFile.write(instanceNumber)
            instanceFile.close()
            return instanceNumber
             
        except NoSuchElementException:
            writeToLog("INFO","FAILED to read / write from the instance file")
            return False
            
            