from base import *
from selenium.webdriver.common.keys import Keys


class General(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #General locators: 
    #=============================================================================================================
    KMS_LOADER                                          = ('id', 'loader')#loaderWrap
    ADD_NEW_DROP_DOWN_BUTTON                            = ('xpath', "//button[contains(@id, 'addNewDropDown')]")
    USER_MENU_TOGGLE_BUTTON                             = ('id', 'userMenuToggleBtn')
    USER_MENU_MY_MEDIA_BUTTON                           = ('xpath', "//a[contains(@href,'/my-media') and @role='menuitem']")
    USER_MENU_MY_CHANNELS_BUTTON                        = ('xpath', "//a[contains(@href,'/my-channels') and @role='menuitem']")
    USER_MENU_MY_PLAYLISTS_BUTTON                       = ('xpath', "//a[contains(@href,'/my-playlists') and @role='menuitem']")
#     USER_MENU_MY_MEDIA_BUTTON                           = ('xpath', "//a[@href='/my-media' and @role='menuitem']")
#     USER_MENU_MY_CHANNELS_BUTTON                        = ('xpath', "//a[@href='/my-channels' and @role='menuitem']")
#     USER_MENU_MY_CHANNELS_BUTTON                        = ('xpath', "//a[contains(@href,'/my-channels') and @role='menuitem']")
#     USER_MENU_MY_PLAYLISTS_BUTTON                       = ('xpath', "//a[@href='/my-playlists' and @role='menuitem']")
    USER_MENU_MY_HISTORY_BUTTON                         = ('xpath', "//a[@href='/history' and @role='menuitem']")

    
    #=============================================================================================================

    def waitForLoaderToDisappear(self, timeout=60):
        sleep(1)
        self.wait_while_not_visible(self.KMS_LOADER, timeout)
        sleep(1)
        self.wait_while_not_visible(self.KMS_LOADER, timeout)
        
        
    