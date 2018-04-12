from selenium import webdriver
from base import *
import clsTestService
import localSettings

class Autoit():
    autoitDriver      = None
    clsCommon   = None
         
    def __init__(self, clsCommon):
        if localSettings.LOCAL_SETTINGS_RUN_MDOE == localSettings.REMOTE_RUN_MODE:
            self.clsCommon = clsCommon
            if localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd":
                self.autoitDriver = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})      
            elif localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL == "qaKmsFrontEnd2":
                self.autoitDriver2 = webdriver.Remote( command_executor='http://' + localSettings.LOCAL_SETTINGS_AUTOIT_SERVICE_HOST2 + '/wd/hub', desired_capabilities={'browserName':'AutoIt'})
            else:
                writeToLog("INFO","FAIELD to connect to Autoit service on remote host: " + localSettings.LOCAL_SETTINGS_SELENIUM_GRID_POOL)