from base import *
from logger import *
import localSettings


class Login(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon    
    #=============================================================================================================
    #Login locators:
    #=============================================================================================================
    LOGIN_USERNAME_FIELD                = ('id', 'Login-username')
    LOGIN_PASSWORD_FIELD                = ('id', 'Login-password')
    LOGIN_SIGN_IN_BTN                   = ('id', 'Login-login')
    USER_MENU_TOGGLE_BTN                = ('id', 'userMenuToggleBtn')
    USER_LOGOUT_BTN                     = ('xpath', "//i[@class='icon-signout']")
    USER_GUEST                          = ('xpath', "//span[@id='userMenuDisplayName' and contains(text(), 'Guest')]")
    USER_NAME                           = ('xpath', "//span[@id='userMenuDisplayName']")
    AUTO_REDIRECT_LOG_IN_BUTTON         = ('xpath', "//a[text()='Click here to login']")
    #============================================================================================================
    def loginToKMS(self, username, password, url=''):
        try:
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            if url != '':
                writeToLog("INFO","URL: " + url)
            # Navigate to login page
            self.navigateToLoginPage(url)
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            self.click(self.LOGIN_SIGN_IN_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            el = self.get_element_text(self.USER_MENU_TOGGLE_BTN)
            if el != 'Guest':
                writeToLog("INFO","Logged in as '" + username + "@" + password + "'")
                # Get the username after login and set the variable. Will need this it some tests
                localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN = el
                return True
            else:
                writeToLog("INFO","FAILED to login as '" + username + "@" + password + "' after 30 seconds.")
                return False
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
        
        
    def navigateToLoginPage(self, url='', verifyUrl=True):
        if url == '':
            self.navigate(localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL)
            if verifyUrl == True:
                return self.clsCommon.myMedia.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL, verifyIn=True, isRegex=False)    
        else:
            self.navigate(url)
            if verifyUrl == True:
                return self.clsCommon.myMedia.verifyUrl(url, False)
           
    
    # If allowAnonymous=False, we will no longer verify if the user is guest because the authentication screen is presented
    def logOutOfKMS(self, allowAnonymous=True):
        # Click on the user menu button
        if self.click(self.USER_MENU_TOGGLE_BTN) == False:
            writeToLog("INFO","FAILED to click on user menu during the first try")
            sleep(15)
            if self.click(self.USER_MENU_TOGGLE_BTN) == False:
                writeToLog("INFO","FAILED to click on user menu during the second try")
                return False
        
        sleep(2)
        # Click on logout button
        if self.clickOnLogOutButton() == False:
            writeToLog("INFO","FAILED to click on logout button")
            return False
        
        sleep(2)
        if allowAnonymous == True:
            # Verify user now is guest
            if self.wait_visible(self.USER_GUEST, 5) == False:
                writeToLog("INFO","FAILED verify user was logout")
                return False
        
        writeToLog("INFO","Success user was logout")   
        return True
    
    
    def clickOnLogOutButton(self):
#         el = self.get_elements(self.USER_LOGOUT_BTN)[1]
#         return el.click()
        if self.click(self.USER_LOGOUT_BTN, multipleElements = True) == False:
            writeToLog("INFO","FAILED to click on logout option")   
            return False            
    
    # This method works for sites with user(userLocator), password(passLocator) and submit(submitLocator) button
    # It verifies any object (objAfterLoginLocator) after login, to make sure login was successful
    def genericLogin(self, username, password, loginUrl, userLocator, passLocator, submitLocator, objAfterLoginLocator):
        # Navigate to Login Page
        if self.navigate(loginUrl) == False:
            writeToLog("INFO","FAILED to navigate to Login Page: " + loginUrl)   
            return False
        
        # Enter username
        if self.send_keys(userLocator, username, True) == False:
            writeToLog("INFO","FAILED to enter username: " + username)
            return False
        
        # Enter password
        if self.send_keys(passLocator, password, True) == False:
            writeToLog("INFO","FAILED to enter password: " + password)
            return False
             
        # Click login/submit
        if self.click(submitLocator, 30, True) == False:
            writeToLog("INFO","FAILED to click login/submit button")
            return False
        
        # Verify login successfully - wait for object which appear only after successful login
        if self.wait_visible(objAfterLoginLocator, 60, True) == False:
            writeToLog("INFO","FAILED to click login/submit button")
            return False         
        return True
    
    
    def getLoginUserName(self):
        try:
            userName = self.get_element_text(self.USER_NAME)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get user name element")
            return False
        return userName
    

    def loginToKMSEmbed(self, username, password):
        try:
            # Going to select the embed iframe            
            if self.wait_element(self.clsCommon.player.PLAYER_EMBED_IFRAME_1, 5) != False:
                self.clsCommon.base.swith_to_iframe(self.clsCommon.player.PLAYER_EMBED_IFRAME_1, 1)
                
            if self.wait_element(self.AUTO_REDIRECT_LOG_IN_BUTTON, 5, True) != False:
                if self.click(self.AUTO_REDIRECT_LOG_IN_BUTTON, 1) == False:
                    writeToLog("INFO", "FAILED to navigate to the log in authentication page while auto redirect was OFF")
                    return False
                sleep(2)
                self.switch_to_default_content()
            
            writeToLog("INFO","Going to login as '" + username + " / " + password + "'")
            # Enter test partner username
            self.send_keys(self.LOGIN_USERNAME_FIELD, username)
            # Enter test partner password
            self.send_keys(self.LOGIN_PASSWORD_FIELD, password)
            # Click Sign In
            self.click(self.LOGIN_SIGN_IN_BTN)
            # Wait page load
            self.wait_for_page_readyState()
            # Verify logged in
            if self.wait_element(self.LOGIN_USERNAME_FIELD, 1, True) != False:
                writeToLog("INFO", "FAILED to load the embed file, the authentication screen is still presented")
                return False
        except Exception as inst:
            writeToLog("INFO","FAILED to login as '" + username + "@" + password + "'")
            self.takeScreeshotGeneric("FAIL_LOGIN_TO_KMS")
            raise Exception(inst)
        
        
    def logOutThenLogInToKMS(self,username, password, url='', allowAnonymous=True):
        # Log Out from the account
        if self.logOutOfKMS(allowAnonymous) == False:
            writeToLog("INFO","FAILED to log out from the current KMS account")  
            return False
        
        # Log In with the desired KMS account
        if self.loginToKMS(username, password, url) == False:
            writeToLog("INFO", "FAILED to authenticate to the " + username + " KMS account " )
            return False
        
        return True