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
    
    #=============================================================================================================

    
