import sys, datetime, re
from time import sleep

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import Select

from logger import *


class Base:
    
    def __init__(self, driver):
        self.driver = driver


    def get_element(self, locator):
        """
        Returns element based on provided locator.
        Locator include the method and locator value in a tuple.
        :param locator:
        :return:
        """

        method = locator[0]
        values = locator[1]
        
        if type(values) is str:
            try:
                return self.get_element_by_type(method, values)
            except NoSuchElementException:
                raise NoSuchElementException
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_element_by_type(method, value)
                except NoSuchElementException:
                    pass
            writeToLog("DEBUG","Function: " + sys._getframe().f_code.co_name + ": Element not found by: '" + method + "' = '" + values + '"')
            raise NoSuchElementException
        
        
    def get_child_element(self, parent, locator):
        """
        Returns element based on provided locator.
        Locator include the method and locator value in a tuple.
        :param locator:
        :return:
        """

        method = locator[0]
        values = locator[1]
        
        if type(values) is str:
            try:
                return self.get_child_element_by_type(parent, method, values)
            except NoSuchElementException:
                raise NoSuchElementException
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_child_element_by_type(parent, method, value)
                except NoSuchElementException:
                    pass
            writeToLog("DEBUG","Function: " + sys._getframe().f_code.co_name + ": Element not found by: '" + method + "' = '" + values + '"')
            raise NoSuchElementException        


    def get_element_by_type(self, method, value):
        if method == 'accessibility_id':
            return self.driver.find_element_by_accessibility_id(value)
        elif method == 'android':
            return self.driver.find_element_by_android_uiautomator('new UiSelector().%s' % value)
        elif method == 'ios':
            return self.driver.find_element_by_ios_uiautomation(value)
        elif method == 'class_name':
            return self.driver.find_element_by_class_name(value)
        elif method == 'id':
            return self.driver.find_element_by_id(value)
        elif method == 'xpath':
            return self.driver.find_element_by_xpath(value)
        elif method == 'name':
            return self.driver.find_element_by_name(value)
        elif method == 'tag_name':
            return self.driver.find_element_by_tag_name(value)        
        else:
            writeToLog("DEBUG",'Function: ' + sys._getframe().f_code.co_name + ': Invalid locator method: "' + method + '" = "' + value + '"')
            raise Exception('Invalid locator method.')
        
        
    def get_child_element_by_type(self, parent, method, value):
        if method == 'accessibility_id':
            return parent.find_element_by_accessibility_id(value)
        elif method == 'android':
            return parent.find_element_by_android_uiautomator('new UiSelector().%s' % value)
        elif method == 'ios':
            return parent.find_element_by_ios_uiautomation(value)
        elif method == 'class_name':
            return parent.find_element_by_class_name(value)
        elif method == 'id':
            return parent.find_element_by_id(value)
        elif method == 'xpath':
            return parent.find_element_by_xpath(value)
        elif method == 'name':
            return parent.find_element_by_name(value)
        elif method == 'tag_name':
            return self.driver.find_element_by_tag_name(value)        
        else:
            writeToLog("DEBUG",'Function: ' + sys._getframe().f_code.co_name + ': Invalid locator method: "' + method + '" = "' + value + '"')
            raise Exception('Invalid locator method.')        


    def get_elements(self, locator):
        """
        Returns element based on provided locator.
        Locator include the method and locator value in a tuple.
        :param locator:
        :return:
        """

        method = locator[0]
        values = locator[1]

        if type(values) is str:
            return self.get_elements_by_type(method, values)
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_elements_by_type(method, value)
                except NoSuchElementException:
                    pass
            raise NoSuchElementException


    def get_elements_by_type(self, method, value):
        if method == 'accessibility_id':
            return self.driver.find_elements_by_accessibility_id(value)
        elif method == 'android':
            return self.driver.find_elements_by_android_uiautomator(value)
        elif method == 'ios':
            return self.driver.find_elements_by_ios_uiautomation(value)
        elif method == 'class_name':
            return self.driver.find_elements_by_class_name(value)
        elif method == 'id':
            return self.driver.find_elements_by_id(value)
        elif method == 'xpath':
            return self.driver.find_elements_by_xpath(value)
        elif method == 'name':
            return self.driver.find_elements_by_name(value)
        elif method == 'tag_name':
            return self.driver.find_elements_by_tag_name(value)        
        else:
            writeToLog("DEBUG",'Function: ' + sys._getframe().f_code.co_name + ': Element not found by: "' + method + '" = "' + value + '"')
            raise Exception('Invalid locator method.')


    # element visible
    def is_visible(self, locator):
        try:
            if self.get_element(locator).is_displayed() == True:
                return True
            else:
                return False
        except NoSuchElementException:
            return False
    
    
    # Wait till element is disappear and return True, elase return False after timeout    
    def wait_while_not_visible(self, locator, timeout=30):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while True:
            try:
                if self.is_visible(locator) == False:
                    return True
                if wait_until < datetime.datetime.now():
                    writeToLog("DEBUG",'Element still visible')
                    break
            except:
                return True
        return False
           
           
    # element present
    def is_present(self, locator):
        try:
            self.get_element(locator)
            return True
        except NoSuchElementException:
            return False


    # waits
    def wait_visible(self, locator, timeout=10):
        i = 0
        self.driver.implicitly_wait(0)
        while i != timeout:
            try:
                if self.is_visible(locator) == True:
                    self.setImplicitlyWaitToDefault()
                    return self.get_element(locator)
                else:
                    sleep(1)
                    i += 1                    
            except NoSuchElementException:
                sleep(1)
                i += 1
        self.setImplicitlyWaitToDefault()                
        return False


    def wait_for_text(self, locator, text, timeout=10):
        i = 0
        self.driver.implicitly_wait(0)
        while i != timeout:
            try:
                element = self.get_element(locator)
                element_text = element.text
                if element_text.lower() == text.lower():
                    self.setImplicitlyWaitToDefault() 
                    return True
                else:
                    pass
            except NoSuchElementException:
                pass
            sleep(1)
            i += 1
        self.setImplicitlyWaitToDefault() 
        return None


    # clicks and taps
    def click(self, locator, timeout=10):
        element = self.wait_visible(locator, timeout)
        if element == None:
            return False
        else:
            element.click()
            
        
    # click with offset
#     def click_with_offset(self, locator, x, y):
#         element = self.wait_visible(locator)
#         if element == None:
#             return False
#         else:
#             action = TouchAction(self.driver)
#             action.tap(element, x, y).perform()
#             return True         

        
    # send keys
    def send_keys(self, locator, text):
        element = self.wait_visible(locator)
        if element == None:
            return False
        else:
            element.send_keys(text)
            return True 
    
    
    def clear_and_send_keys(self, locator, text):
        element = self.wait_visible(locator)
        if element == None:
            return False
        else:
            element.clear()
            element.send_keys(text)
            return True
            
            
    # key event
    def keyevent(self, locator, event):
        element = self.wait_visible(locator)
        if element == None:
            return False
        else:
            element.keyevent(event)
            return True     


    def get_element_attributes(self, locator):
        element = self.get_element(locator)
        return {
            'text': element.text,
            'top': element.location['y'],
            'bottom': element.location['y'] + element.size['height'],
            'left': element.location['x'],
            'right': element.location['x'] + element.size['width'],
            'center_x': (element.size['width']/2) + element.location['x'],
            'center_y': (element.size['height']/2) + element.location['y']
        }
        
        
    def get_element_text(self, locator):
        element = self.get_element(locator)
        return element.text


    def navigate(self, url):
        self.driver.get(url)
        if self.wait_for_page_readyState() == False:
            writeToLog("INFO","FAILED to load page: '" + url + "'")
            return False
        else:
            return True
        
        
    # Verify expectedUrl = current URL, if isRegex is True, will verify when expectedUrl is regular expression
    def verifyUrl(self, expectedUrl, isRegex, timeout=30):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while True:        
            currentUrl = self.driver.current_url
            if isRegex == True:
                m = re.search(expectedUrl, currentUrl)
                if m:
                    return True
                else:
                    if wait_until < datetime.datetime.now():
                        return False
            # Compare URL with contains method ('in')
            else:
                # remove the http/https from the current and expected URL and compare
                newCurrentUrl = currentUrl.replace('https://', '')
                newCurrentUrl = newCurrentUrl.replace('http://', '')
                newExpectedUrl = expectedUrl.replace('https://', '')
                newExpectedUrl = newExpectedUrl.replace('http://', '')
                # Compare the URLs
                if newExpectedUrl in newCurrentUrl:
                    return True
                else:
                    if wait_until < datetime.datetime.now():
                        return False
            
    # Verify expectedUrl = current URL, if isRegex is True, will verify when expectedUrl is regular expression
    def verifyUrl_old(self, expectedUrl, isRegex, timeout=30):
        currentUrl = self.driver.current_url
        if isRegex == True:
            m = re.search(expectedUrl, currentUrl)
            if m:
                return True
            else:
                writeToLog("INFO","FAILED, Page loaded with not expected URL, expected: '" + expectedUrl + "'\nbut actual is: '" + currentUrl + "'; isRegex = True")
                return False
        # Compare URL with contains method ('in')
        else:
            # remove the http/https from the current and expected URL and compare
            newCurrentUrl = currentUrl.replace('https://', '')
            newCurrentUrl = newCurrentUrl.replace('http://', '')
            newExpectedUrl = expectedUrl.replace('https://', '')
            newExpectedUrl = newExpectedUrl.replace('http://', '')
            # Compare the URLs
            if newExpectedUrl in newCurrentUrl:
                return True
            else:
                writeToLog("INFO","FAILED, Page loaded with not expected URL, expected: '" + expectedUrl + "'\nbut actual is: '" + currentUrl + "'; isRegex = False")
                return False            
            
            
    def wait_for_page_readyState(self, timeout=30):
        i = 0
        page_state = ''
        while i != timeout and page_state != 'complete':
            page_state = self.driver.execute_script('return document.readyState;')
            sleep(1)
            i += 1
        if page_state == 'complete':
            return True
        else:
            writeToLog("DEBUG","Page readyState was not completed after timeout: '" + timeout + "'")
            return False
       
        
    # Create a screeshot with a given name it the test log folder
    def takeScreeshotGeneric(self, scName):
        LOG_FOLDER_PREFIX = "/"
        if (os.getenv('BUILD_ID',"") != ""):
            LOG_FOLDER_PREFIX = '/' + os.getenv('BUILD_ID',"") + '/'
        runningTestNum = os.getenv('RUNNING_TEST_ID',"")
        if (runningTestNum != ""):            
            pngPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','logs' + LOG_FOLDER_PREFIX,runningTestNum + LOG_FOLDER_PREFIX + scName + '.png'))   
        try:
            self.driver.save_screenshot(pngPath)  
        except:
            writeToLog("INFO","Failed to take a screenshot, bad driver")
            
            
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
        
        
    def setImplicitlyWaitToDefault(self):
        self.driver.implicitly_wait(localSettings.LOCAL_SETTINGS_IMPLICITLY_WAIT)
        
        
    def select_from_combo_by_text(self, locator, optionToSelect):
        try:
            select = Select(self.get_element(locator))
            
            # select by visible text
            select.select_by_visible_text(optionToSelect)
        except:
            writeToLog("INFO","FAILED to select: '" + optionToSelect + "' from locator: '" + locator[1] + "'")
            return False
        
        return True            
        
        
    def select_from_combo_by_value(self, locator, value):
        try:
            select = Select(self.get_element(locator))
            
            # select by value 
            select.select_by_value(value)
        except:
            writeToLog("INFO","FAILED to select: '" + value + "' from locator: '" + locator[1] + "'")
            return False
        
        return True          
