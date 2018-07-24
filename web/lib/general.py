from base import *


class General(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #General locators:
    #=============================================================================================================
    KMS_LOADER                                  = ('id', 'loader')#loaderWrap
    ADD_NEW_DROP_DOWN_BUTTON                    = ('id', 'addNewDropDown')
    USER_MENU_TOGGLE_BUTTON                     = ('id', 'userMenuToggleBtn')
    USER_MENU_MY_MEDIA_BUTTON                   = ('xpath', "//a[@href='/my-media' and @role='menuitem']")
    USER_MENU_MY_CHANNELS_BUTTON                = ('xpath', "//a[@href='/my-channels' and @role='menuitem']")
    USER_MENU_MY_PLAYLISTS_BUTTON               = ('xpath', "//a[@href='/my-playlists' and @role='menuitem']")
    USER_MENU_MY_HISTORY_BUTTON                 = ('xpath', "//a[@href='/history' and @role='menuitem']")
    GLOBAL_SEARCH_BUTTON_NEWUI                  = ('xpath', "//span[@class='hidden-tablet' and contains(text(),'search')]")
    GLOBAL_SEARCH_TEXTBOX                       = ('xpath', "//input[@placeholder='Search all media' and @type='text']")
    ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_NEWUI   = ('xpath', "//img[@class='entryThumbnail__img' and @alt='ENTRY_NAME']")
    ENTRY_THUMBNAIL_AFTER_GLOBAL_SEARCH_OLDUI   = ('xpath', "//img[@class='thumb_img' and @alt='Thumbnail for entry ENTRY_NAME']")
    
    #=============================================================================================================

    def waitForLoaderToDisappear(self, timeout=60):
        sleep(1)
        self.wait_while_not_visible(self.KMS_LOADER, timeout)
        sleep(1)
        self.wait_while_not_visible(self.KMS_LOADER, timeout)
        
        
    def SerchInGlobalSearch(self, searchWord):
        if self.clsCommon.isElasticSearchOnPage() == True:
            if self.click(self.GLOBAL_SEARCH_BUTTON_NEWUI, timeout=15) == False:
                writeToLog("INFO","FAILED to click on global search button")
                return False
            
        if self.click(self.GLOBAL_SEARCH_TEXTBOX, timeout=10, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on global search textbox")
            return False
        
        if self.send_keys(self.GLOBAL_SEARCH_TEXTBOX, searchWord, multipleElements=True) == False:
            writeToLog("INFO","FAILED to insert search word to global search textbox")
            return False
            
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
    
    
    def verifySerachAfterGlobalSearch(self, searchWord, searchCount):
        
        return True  