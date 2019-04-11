from selenium import webdriver
from base import *
import clsTestService
import localSettings

class Autoit():
    autoitDriver      = None
    clsCommon   = None
         
    def __init__(self, clsCommon):
        try:
            if localSettings.LOCAL_SETTINGS_RUN_MDOE == localSettings.REMOTE_RUN_MODE:
                self.clsCommon = clsCommon
                if localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd":
                    self.autoitDriver = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})      
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd2":
                    self.autoitDriver2 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST2 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd3":
                    self.autoitDriver3 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST3 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd4":
                    self.autoitDriver4 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST4 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd5":
                    self.autoitDriver5 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST5 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd6":
                    self.autoitDriver6 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST6 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd7":
                    self.autoitDriver7 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST7 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'}) 
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd8":
                    self.autoitDriver8 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST8 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'}) 
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd9":
                    self.autoitDriver9 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST9 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'}) 
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd10":
                    self.autoitDriver10 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST10 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})                                                                                                     
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd11":
                    self.autoitDriver11 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST11 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})                
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd12":
                    self.autoitDriver12 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST12 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd13":
                    self.autoitDriver13 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST13 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd14":
                    self.autoitDriver14 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST14 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd15":
                    self.autoitDriver15 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST15 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})            
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd16":
                    self.autoitDriver16 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST16 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd17":
                    self.autoitDriver17 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST17 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd18":
                    self.autoitDriver18 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST18 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd19":
                    self.autoitDriver19 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST19 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd20":
                    self.autoitDriver20 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST20 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd21":
                    self.autoitDriver21 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST21 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd22":
                    self.autoitDriver22 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST22 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
                elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd23":
                    self.autoitDriver23 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST23 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})                                                                                                                        
                else:
                    writeToLog("INFO","FAIELD to connect to Autoit service on remote host: " + localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL)
        except Exception as exp:
            writeToLog("INFO","FAIELD to connect to Autoit service on remote host: " + localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL)
            writeToLog("INFO",str(exp))
