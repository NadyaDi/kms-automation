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
    KMS_LOADER                              = ('id', 'loader')#loaderWrap
    ADD_NEW_DROP_DOWN_BUTTON                = ('id', 'addNewDropDown')
    USER_MENU_TOGGLE_BUTTON                 = ('id', 'userMenuToggleBtn')
    USER_MENU_MY_MEDIA_BUTTON               = ('xpath', "//a[@href='/my-media' and @role='menuitem']")
    #=============================================================================================================

    def waitForLoaderToDisappear(self, timeout=60):
        self.wait_while_not_visible(self.KMS_LOADER, timeout)
