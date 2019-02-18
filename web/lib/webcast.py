from base import *
import clsTestService
from general import General
from logger import writeToLog
from selenium.webdriver.common.keys import Keys


class Webcast(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Webcast locators:
    #==================================================