from base import *
import clsTestService


class EntryPage(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Upload XPATH locators:
    #=============================================================================================================
    ENTRY_PAGE_ENTRY_TITLE                      = ('class_name', 'entryTitle')
    #=============================================================================================================