import sys, datetime, re
from time import sleep
import utilityTestFunc
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import InvalidElementStateException

from logger import *
from builtins import str


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
                raise NoSuchElementException("FAILED to get element locator value: " + values + "; method: " + method)
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_element_by_type(method, value)
                except NoSuchElementException:
                    pass
            writeToLog("DEBUG","Function: " + sys._getframe().f_code.co_name + ": Element not found by: '" + method + "' = '" + values + '"')
            raise NoSuchElementException("FAILED to get element locator value: " + values + "; method: " + method)
        
        
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
                raise NoSuchElementException("FAILED to get element locator value: " + values + "; method: " + method)
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_child_element_by_type(parent, method, value)
                except NoSuchElementException:
                    pass
            writeToLog("DEBUG","Function: " + sys._getframe().f_code.co_name + ": Element not found by: '" + method + "' = '" + values + '"')
            raise NoSuchElementException("FAILED to get element locator value: " + values + "; method: " + method)
        

    def get_child_elements(self, parent, locator):
        """
        Return elements based on provided locator.
        Locator include the method and locator value in a tuple.
        :param locator:
        :return:
        """

        method = locator[0]
        values = locator[1]
        
        if type(values) is str:
            try:
                return self.get_child_elements_by_type(parent, method, values)
            except NoSuchElementException:
                raise NoSuchElementException("FAILED to get element locator value: " + values + "; method: " + method)
        elif type(values) is list:
            for value in values:
                try:
                    return self.get_child_elements_by_type(parent, method, value)
                except NoSuchElementException:
                    pass
            writeToLog("DEBUG","Function: " + sys._getframe().f_code.co_name + ": Element not found by: '" + method + "' = '" + values + '"')
            raise NoSuchElementException("FAILED to get element locator value: " + values + "; method: " + method)                


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
        
        
    def get_child_elements_by_type(self, parent, method, value):
        if method == 'accessibility_id':
            return parent.find_elements_by_accessibility_id(value)
        elif method == 'android':
            return parent.find_elements_by_android_uiautomator('new UiSelector().%s' % value)
        elif method == 'ios':
            return parent.find_elements_by_ios_uiautomation(value)
        elif method == 'class_name':
            return parent.find_elements_by_class_name(value)
        elif method == 'id':
            return parent.find_elements_by_id(value)
        elif method == 'xpath':
            return parent.find_elements_by_xpath(value)
        elif method == 'name':
            return parent.find_elements_by_name(value)
        elif method == 'tag_name':
            return self.driver.find_elements_by_tag_name(value)        
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
            raise NoSuchElementException("FAILED to get element locator value: " + values + "; method: " + method)


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
        self.setImplicitlyWait(0)
        while True:
            try:
                if self.is_visible(locator) == False:
                    self.setImplicitlyWaitToDefault()
                    return True
                if wait_until < datetime.datetime.now():
                    writeToLog('INFO','Element still visible')
                    self.setImplicitlyWaitToDefault()
                    return False
            except:
                self.setImplicitlyWaitToDefault()
                return True
        self.setImplicitlyWaitToDefault()    
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
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                if self.is_visible(locator) == True:
                    self.setImplicitlyWaitToDefault()
                    return self.get_element(locator)
                if wait_until < datetime.datetime.now():
                    #writeToLog('DEBUG','Element not visible')
                    self.setImplicitlyWaitToDefault()
                    return False                
            except:
                self.setImplicitlyWaitToDefault()
                return False


    # If you want to verify partial (contains) text set 'contains' True
    def wait_for_text(self, locator, text, timeout=10, contains=False):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                element = self.get_element(locator)
                element_text = element.text
                if contains == True:
                    if text.lower() in element_text.lower():
                        self.setImplicitlyWaitToDefault()
                        return True                    
                else:    
                    if element_text.lower() == text.lower():
                        self.setImplicitlyWaitToDefault()
                        return True
                if wait_until < datetime.datetime.now():
                    writeToLog('INFO','Text element not visible')
                    self.setImplicitlyWaitToDefault()
                    return False                  
            except:
                self.setImplicitlyWaitToDefault()
                return False


    # clicks and taps
    # When you have more then one elemnet found with your locator, use multipleElements = True
    # it will search for element from the elements list, and find the one with size not 0
    def click(self, locator, timeout=10, multipleElements=False):
        try:
            if multipleElements == True:
                elements = self.get_elements(locator)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!=0:
                        el.click()
                        return True
                return False
            element = self.wait_visible(locator, timeout)
            if element == False:
                return False
            else:
                element.click()
                return True
            
        except InvalidElementStateException:
            writeToLog("DEBUG","Element was found, but FAILED to click")
            return False        
    
    
    # Click on given element.
    # When you have more then one elemnet (= list of elements) found with your locator, use multipleElements = True
    # it will search for element from the elements list, and find the one with size not 0       
    def clickElement(self, element, multipleElements=False):
            if multipleElements == True:
                for el in element:
                    if el.size['width']!=0 and el.size['height']!=0:
                        el.click()
                        return True
                return False
            if element == None:
                return False
            else:
                element.click()
                return True
     
                    
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
        if element == False:
            return False
        else:
            element.send_keys(text)
            return True 
    
    
    def clear_and_send_keys(self, locator, text):
        element = self.wait_visible(locator)
        if element == False:
            return False
        else:
            element.clear()
            element.send_keys(text)
            return True
            
            
    # key event
    def keyevent(self, locator, event):
        element = self.wait_visible(locator)
        if element == False:
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
        
        
    def get_element_text(self, locator, timeout=30):
        if self.wait_visible(locator, timeout) == False:
            return None
        element = self.get_element(locator)
        return element.text
    
    
    def is_element_checked(self, locator):
        element = self.get_element(locator)
        if element.get_attribute("checked") != "true":
            writeToLog("INFO","element is not checked")
            return False
        
        return True
        
        
    def check_element(self, locator, action):
        if action == True:
            if self.is_element_checked(locator) == True:
                writeToLog("INFO","element is already checked")
                return True
            
        elif action == False:
            if self.is_element_checked(locator) == False:
                writeToLog("INFO","element is already unchecked")
                return True               
        
        if self.click(locator, 30) == False:
            writeToLog("INFO","FAILED to click on element checkbox")
            return False
        
        return True


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
        runningTestNum = os.getenv('RUNNING_TEST_ID',"")
        if (runningTestNum != ""):      
            pngPath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'logs',runningTestNum, scName + '.png')) 
        try:
            self.driver.save_screenshot(pngPath)
            return True
        except:
            writeToLog("INFO","Failed to take a screenshot, bad driver")
            return False
            
           
    # Create a screeshot with a given path
    def takeScreeshot(self, filePath):
        try:
            os.path.abspath(filePath)
            self.driver.save_screenshot(filePath)
            return True
        except:
            writeToLog("INFO","Failed to take a screenshot, bad driver")
            return False

            
    def swith_to_iframe(self, locator, timeout=30):
        elementIframe = self.wait_visible(locator, timeout)
        if elementIframe == False:
            writeToLog("INFO","FAILED to get IFRAME element")
            return False      
        self.driver.switch_to.frame(elementIframe)
        return True         
            
            
    def switch_to_default_content(self):
        localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.DEFAULT
        self.driver.switch_to.default_content()
        
        
    def setImplicitlyWaitToDefault(self):
        self.driver.implicitly_wait(localSettings.LOCAL_SETTINGS_IMPLICITLY_WAIT)
        
        
    def setImplicitlyWait(self, timeout):
        self.driver.implicitly_wait(timeout)        
        
        
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
    
    
    def hover_on_element(self, locator):
        try:
            element = self.get_element(locator)
            ActionChains(self.driver).move_to_element(element).perform()
        except:
            writeToLog("INFO","FAILED to hover on locator: '" + locator[1] + "'")
            return False
        
        return True  
    
    def convertBooleanToYesNo(self, booleanExp):
        strExp = None
        if booleanExp == True:
            strExp = 'Yes'
        elif booleanExp == False:
            strExp = 'No'      
        else:
            raise Exception("Unknown boolean expression")
        return strExp
