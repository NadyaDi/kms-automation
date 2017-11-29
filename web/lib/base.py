import sys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from logger import *

class Base:

    def __init__(self, driver):
        self.driver = driver

    # get elements
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
        else:
            writeToLog("DEBUG",'Function: ' + sys._getframe().f_code.co_name + ': Element not found by: "' + method + '" = "' + value + '"')
            raise Exception('Invalid locator method.')

    # element visible
    def is_visible(self, locator):
        try:
            self.get_element(locator).is_displayed()
            return True
        except NoSuchElementException:
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
        while i != timeout:
            try:
                self.is_visible(locator)
                return self.get_element(locator)
            except NoSuchElementException:
                sleep(1)
                i += 1
        return None

    def wait_for_text(self, locator, text, timeout=10):
        i = 0
        while i != timeout:
            try:
                element = self.get_element(locator)
                element_text = element.text
                if element_text.lower() == text.lower():
                    return True
                else:
                    pass
            except NoSuchElementException:
                pass
            sleep(1)
            i += 1
        return None

    # clicks and taps
    def click(self, locator):
        element = self.wait_visible(locator)
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
        if element == None:
            return False
        else:
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
        self.wait_for_page_readyState()
        
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