from base import *
import clsTestService
from general import General
from logger import writeToLog
from selenium.webdriver.common.keys import Keys
import subprocess
import getpass
import configparser
import os

class Webcast(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Webcast locators:
    #=============================================================================================================
    KMC_LOGIN_USERNAME_FIELD                      = ('xpath', "//div[@class='ng-untouched ng-pristine ng-invalid ui-inputtext ui-corner-all ui-state-default ui-widget']")
    EDIT_WC_EVENT_BUTTON_FROM_CREATE_WC_PAGE      = ('xpath', "//a[@class='btn btn-link' and text()='Edit webcast']")                                            
    LAUNCH_WC_APPLICATION                         = ('xpath', "//a[@class='btn launchWebcastBtn' and text()='Launch Application']")
    #=============================================================================================================
    #Webcast Sikulix script setup:
    #=============================================================================================================  
    CONNECTED_USER                                = getpass.getuser()
    CONFIG_FILE_PATH                              = r'C:\\Users\\'+ CONNECTED_USER + '\\Desktop\\WebcastAutomationSettings.ini'
    CONFIG                                        = configparser.ConfigParser()
    RUN_SIKULIX_FILE_PATH                         = "C:\\Users\\" + CONNECTED_USER + "\\Downloads\\runsikulix.cmd -r";
    WEBCAST_SCRIPT_PATH                           = "C:\\Users\\" + CONNECTED_USER + "\\Desktop\\WebcastAutomation.skl";
    
    
    def editWebCastEvent(self):
        if self.click(self.EDIT_WC_EVENT_BUTTON_FROM_CREATE_WC_PAGE) == False:
            writeToLog("INFO","FAILED to click on Edit webcast button from create webcast event page")
            return False 
            
        if self.wait_element(self.LAUNCH_WC_APPLICATION) == False:
            writeToLog("INFO","FAILED to navigate to webcast  edit page from create webcast event page")
            return False
       
        return True
        
        
    def loginToKMC(self):
        try:
            self.driver.execute_script("window.open();")
            self.driver.switch_to_window(self.driver.window_handles[1]); 
            self.driver.get("https://kmc.kaltura.com/index.php/kmcng/login");
            self.driver.close();
            
            return True
        except NoSuchElementException:
            writeToLog("INFO","FAILED to click on Media Upload from drop down menu")
            return False
        
        
    def setWebcastSetting(self, settingsList,timeOut=120,numOfSlide=50):
        
        try:
            self.CONFIG.read(self.CONFIG_FILE_PATH)
            
            self.CONFIG.set('Settings','finishedsuccessfull','0')
            
            if  'launchapplication' in settingsList:
                self.CONFIG.set('Settings','launchapplication', '1')
                
            else:
                self.CONFIG.set('Settings','launchapplication','0')
                
            if 'startliveevent' in settingsList:
                self.CONFIG.set('Settings','startliveevent','1')
                
            else:
                self.CONFIG.set('Settings','startliveevent','0')
                
            if 'staging' in settingsList:
                self.CONFIG.set('Settings','staging','1')
                
            else:
                self.CONFIG.set('Settings','staging','0')
                 
            if 'monitoring' in settingsList:
                self.CONFIG.set('Settings','monitoring','1')
                
            else:
                self.CONFIG.set('Settings','monitoring','0')
                 
            if 'polls' in settingsList:
                self.CONFIG.set('Settings','polls','1')
                
            else:
                self.CONFIG.set('Settings','polls','0')
                
            if 'answeronair' in settingsList:
                self.CONFIG.set('Settings','answeronair','1')
                
            else:
                self.CONFIG.set('Settings','answeronair','0')
                
            if 'multiplepresenters' in settingsList:
                self.CONFIG.set('Settings','multiplepresenters','1')
                
            else:
                self.CONFIG.set('Settings','multiplepresenters','0')
    
            if 'explicitlive' in settingsList:
                self.CONFIG.set('Settings','explicitlive','1')
                
            else:
                self.CONFIG.set('Settings','explicitlive','0')
                
            if 'selfserved' in settingsList:
                self.CONFIG.set('Settings','selfserved','1')
                
                if 'camera' in settingsList:
                    self.CONFIG.set('Settings','camera','1')
                    
                else:
                    self.CONFIG.set('Settings','camera','0')
                    
                if 'screen' in settingsList:
                    self.CONFIG.set('Settings','screen','1')
                    
                else:
                    self.CONFIG.set('Settings','screen','0')
                    
            else:
                self.CONFIG.set('Settings','selfserved','0')
                      
            
            if 'liveclipping' in settingsList:
                self.CONFIG.set('Settings','liveclipping','1')
                
            else:
                self.CONFIG.set('Settings','liveclipping','0')
                
            if 'dvr' in settingsList:
                self.CONFIG.set('Settings','dvr','1')
                
            else:
                self.CONFIG.set('Settings','dvr','0')
                
            if 'vod' in settingsList:
                self.CONFIG.set('Settings','vod','1')
                
            else:
                self.CONFIG.set('Settings','vod','0')
                
            if 'archive' in settingsList:
                self.CONFIG.set('Settings','archive','1')
               
            else:
                self.CONFIG.set('Settings','archive','0')
                
            if 'selfservedstreamverification' in settingsList:
                self.CONFIG.set('Settings','selfservedstreamverification','1')
                self.CONFIG.set('Settings','timeout',timeOut)
                
            else:
                self.CONFIG.set('Settings','selfservedstreamverification','0')
                 
            if 'slidestress' in settingsList:
                self.CONFIG.set('Settings','slidestress','1')
                self.CONFIG.set('Settings','numofslides',numOfSlide)
                
            else:
                self.CONFIG.set('Settings','slidestress','0')
               
            if 'export' in settingsList:
                self.CONFIG.set('Settings','export','1')
                
            else:
                self.CONFIG.set('Settings','export','0')
                                      
            with open(self.CONFIG_FILE_PATH,'w') as wcSettings:
                self.CONFIG.write(wcSettings)
            
            return True
        
        except Exception:
            writeToLog("INFO","FAILED write to webcast in file")
            return False
        
        
    def startSikulixScript(self):
        try:
            os.system('taskkill /F /IM iexplore.exe')
            os.system('taskkill /F /IM KWP.exe')
            os.system(self.RUN_SIKULIX_FILE_PATH+" "+self.WEBCAST_SCRIPT_PATH)
            self.CONFIG.read(self.CONFIG_FILE_PATH)
            if self.CONFIG.get('Settings','finishedsuccessfull') == '0':
                writeToLog("INFO","FAILED to run sikulix webcast automation script, please check logs for more info")
                return False
            else:
                return True
            
        except Exception:
            writeToLog("INFO","FAILED to run sikulix webcast automation script")
            return False