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
    
    def navigateToEntryPage(self, entryName):
        self.clsCommon.myMedia.searchEntryMyMedia(entryName)
        self.clsCommon.myMedia.clickEntryAfterSearchInMyMedia(entryName)
        # Wait page load - wait for entry title
        self.wait_visible(self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE, 15)    