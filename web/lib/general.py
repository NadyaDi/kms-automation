from base import *



class General(Base):
    
    #=============================================================================================================
    #General XPATH locators:
    #=============================================================================================================
    KMS_LOADER                              = ('id', 'loader')#loaderWrap
    ADD_NEW_DROP_DOWN_BUTTON                = ('id', 'addNewDropDown')
    #=============================================================================================================
    
    def waitForLoaderToDisappear(self, timeout=60):
        self.wait_while_not_visible(self.KMS_LOADER, timeout)
#     def loginToKMS(self, username, password):
#         timeout = 30
#         try:
#             writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
#             # Navigate to login page
#             self.navigate(localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL)
#             # Enter test partner username
#             self.send_keys(self.LOGIN_USERNAME_FIELD, username)
#             # Enter test partner password
#             self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
#             # Click Sign In
#             self.click(self.LOGIN_SIGN_IN_BTN)
#             # Wait page load
#             self.wait_for_page_readyState(timeout)
#             # Verify logged in
#             el = self.get_element_text(self.USER_MENU_TOGGLE_BTN)
#             if el != 'Guest':
#                 writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
#                 # Get the username after login and set the variable. Will need this it some tests
#                 localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN = el
#                 return True
#             else:
#                 writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after " + str(timeout) + " seconds.")
#                 return False
#         except Exception as inst:
#             writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
#             self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
#             raise Exception(inst)