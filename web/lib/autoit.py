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
                else:
                    writeToLog("INFO","FAIELD to connect to Autoit service on remote host: " + localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL)
        except Exception as exp:
            writeToLog("INFO","FAIELD to connect to Autoit service on remote host: " + localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL)
            writeToLog("INFO",str(exp))
