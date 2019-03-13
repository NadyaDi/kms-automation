import sys, datetime, re
from time import sleep
import utilityTestFunc
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import InvalidElementStateException
from logger import *
from builtins import str
import pyperclip


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
        

    def get_child_element(self, parent, locator, multipleElements=False):
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
                if multipleElements == True:
                    elements = self.get_child_elements_by_type(parent, method, values)
                    for el in elements:
                        if el.size['width']!=0 and el.size['height']!=0:
                            return el                    
                else:
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
    def is_visible(self, locator, multipleElements=False):
        try:
            if multipleElements == True:
                elements = self.get_elements(locator)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!=0:
                        if el.is_displayed() == True:
                            return True            
            else:
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
           

    def is_present(self, locator, timeout=10):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                self.get_element(locator)
                if wait_until < datetime.datetime.now():
                    #writeToLog('DEBUG','Element not visible')
                    self.setImplicitlyWaitToDefault()
                    return False
                
                self.setImplicitlyWaitToDefault()
                return True   
            except:
                if wait_until < datetime.datetime.now():
                    #writeToLog('DEBUG','Element not visible')
                    self.setImplicitlyWaitToDefault()
                    return False


    # waits for the element to appear (self.is_visible)
    def wait_visible(self, locator, timeout=10, multipleElements=False):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                if self.is_visible(locator, multipleElements) == True:
                    self.setImplicitlyWaitToDefault()
                    if multipleElements == True:
                        elements = self.get_elements(locator)
                        for el in elements:
                            if el.size['width']!=0 and el.size['height']!=0:
                                self.setImplicitlyWaitToDefault()
                                return el
                        return False
                    else:
                        el = self.get_element(locator)
                        self.setImplicitlyWaitToDefault()
                        return el                        
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    return False                
            except:
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    return False                 
                pass
            

    # waits for the element to appear
#     def wait_element1(self, locator, timeout=10, multipleElements=False):
#         wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
#         self.setImplicitlyWait(0)
#         while True:
#             try:
#                 self.setImplicitlyWaitToDefault()
#                 if multipleElements == True:
#                     elements = self.get_elements(locator)
#                     for el in elements:
#                         if el.size['width']!=0 and el.size['height']!=0:
#                             return el
#                     return False
#                 else:
#                     return self.get_element(locator)
#             except:
#                 if wait_until < datetime.datetime.now():
#                     self.setImplicitlyWaitToDefault()
#                     return False                 
#                 pass      
            
            
    # waits for the element to appear
    def wait_element(self, locator, timeout=10, multipleElements=False):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                if multipleElements == True:
                    elements = self.get_elements(locator)
                    for el in elements:
                        if el.size['width']!=0 and el.size['height']!=0:
                            self.setImplicitlyWaitToDefault()
                            return el
                        
                    if wait_until < datetime.datetime.now():
                        self.setImplicitlyWaitToDefault()
                        return False 
                else:
                    el = self.get_element(locator)
                    self.setImplicitlyWaitToDefault()
                    return el
            except:
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    return False                 
                pass   
            

    # waits for the elements to appear (self.is_visible)
    def wait_elements(self, locator, timeout=10):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                if self.is_visible(locator) == True:
                    self.setImplicitlyWaitToDefault()
                    return self.get_elements(locator)
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    return False               
            except:
                self.setImplicitlyWaitToDefault()
                return False
                
                
    # waits for the element child to appear
    def wait_visible_child(self, parent, locator, timeout=10):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                if self.is_visible(locator) == True:
                    self.setImplicitlyWaitToDefault()
                    return self.get_child_element(parent, locator)
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    return False                
            except:
                self.setImplicitlyWaitToDefault()
                return False


    # If you want to verify partial (contains) text set 'contains' True
    def wait_for_text(self, locator, text, timeout=30, contains=False):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        element = None
        while True:
            try:
                element = self.get_element(locator)
#                 if element != None:
                # If element found (no exception), move to the next while
                break
            except:
                if wait_until < datetime.datetime.now():
                    writeToLog('INFO','Element was not found')
                    self.setImplicitlyWaitToDefault()
                    return False                   
                pass
        
        while True:
            try:
                element_text = element.text
                if contains == True:
                    if text.lower() in element_text.lower():
                        self.setImplicitlyWaitToDefault()
                        return True                    
                else:    
                    if str(element_text.lower()) == str(text.lower()):
                        self.setImplicitlyWaitToDefault()
                        return True
                if wait_until < datetime.datetime.now():
                    writeToLog('INFO','Text element not visible')
                    self.setImplicitlyWaitToDefault()
                    return False
                time.sleep(0.5)                 
            except:
                self.setImplicitlyWaitToDefault()
                return False
            
            
    # If you want to verify partial (contains) child text set 'contains' True
    def wait_for_child_text(self, parent, locator, text, timeout=30, contains=False):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        element = None
        while True:
            try:
                element = self.get_child_element(parent, locator)
#                 if element != None:
                # If element found (no exception), move to the next while
                break
            except:
                if wait_until < datetime.datetime.now():
                    writeToLog('INFO','Element was not found')
                    self.setImplicitlyWaitToDefault()
                    return False                   
                pass
        
        while True:
            try:
                element_text = element.text
                if contains == True:
                    if text.lower() in element_text.lower():
                        self.setImplicitlyWaitToDefault()
                        return True                    
                else:    
                    if str(element_text.lower()) == str(text.lower()):
                        self.setImplicitlyWaitToDefault()
                        return True
                if wait_until < datetime.datetime.now():
                    writeToLog('INFO','Text element not visible')
                    self.setImplicitlyWaitToDefault()
                    return False
                time.sleep(0.5)                 
            except:
                self.setImplicitlyWaitToDefault()
                return False                       
    
    
    # Clicks and taps
    # When you have more then one element found with your locator, use multipleElements = True
    # It will search for element from the elements list, and find the one with size not 0  
    # if passed width and height will use action chain  
    def click(self, locator, timeout=10, multipleElements=False, width=0, height=0):
        try:
            if multipleElements == True:
                element = self.wait_element(locator, timeout, multipleElements=True)
                if element != False:
                    if (width!=0 and height!=0):
                        ActionChains(self.driver).move_to_element_with_offset(element, width, height).click().perform()
                    else:
                        element.click()
                    return True
                return False
            element = self.wait_element(locator, timeout)
            if element == False:
                return False
            else:
                if (width!=0 and height!=0):
                    ActionChains(self.driver).move_to_element_with_offset(element, width, height).click().perform()
                else:
                    element.click()
                return True
            
        except Exception:
            writeToLog("DEBUG","Element was found, but FAILED to click")
            return False
        
        
    # clicks on the child element
    # When you have more then one elemnet found with your locator, use multipleElements = True
    # it will search for element from the elements list, and find the one with size not 0
    def click_child(self, parent, locator, timeout=10, multipleElements=False):
        try:
            if multipleElements == True:
                elements = self.get_child_elements(parent, locator)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!=0:
                        el.click()
                        return True
                return False
            element = self.wait_visible_child(parent, locator, timeout)
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
        try:
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
        except:
            writeToLog("DEBUG","FAILED to click on element")
            return False        
    
    
    # Send keys to given element.
    # When you have more then one elemnet (= list of elements) found with your locator, use multipleElements = True
    # it will search for element from the elements list, and find the one with size not 0       
    def send_keys_to_element(self, element, text, multipleElements=False):
        try:
            if multipleElements == True:
                for el in element:
                    if el.size['width']!=0 and el.size['height']!=0:
                        el.send_keys(text)
                        return True
                return False
            if element == None:
                return False
            else:
                element.send_keys(text)
                return True
        except:
            writeToLog("DEBUG","FAILED to send text to element")
            return False  
        
                
    # send keys
    def send_keys(self, locator, text, multipleElements=False):
        try:
            if multipleElements == True:
                elements = self.get_elements(locator)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!=0:
                        el.send_keys(text)
                        return True
                return False
            else:
                element = self.get_element(locator)
                element.send_keys(text)
                return True 
        except:
            writeToLog("INFO", "FAILED to type text: " + str(text))
            return False


    # send keys to child element
    def send_keys_to_child(self, parent, locator, text, multipleElements=False):
        try:
            if multipleElements == True:
                elements = self.get_child_elements(parent, locator)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!=0:
                        el.send_keys(text)
                        return True
                return False
            else:
                element = self.get_child_element(parent, locator)
                element.send_keys(text)
                return True 
        except:
            writeToLog("INFO", "FAILED to type text: " + str(text))
            return False
        
                  
    # send keys
    def click_and_send_keys(self, locator, text, multipleElements=False):
        try:
            if multipleElements == True:
                elements = self.get_elements(locator)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!=0:
                        if el.click() == False:
                            writeToLog("INFO", "FAILED to click before typing in")
                            return False                        
                        el.send_keys(text)
                        return True
                return False
            else:
                element = self.get_element(locator)
                if element.click() == False:
                    writeToLog("INFO", "FAILED to click before typing in")
                    return False
                element.send_keys(text)
                return True 
        except:
            writeToLog("INFO", "FAILED to type text: " + str(text))
            return False    


    # send keys
    def clear_and_send_keys(self, locator, text, multipleElements=False):
        try:
            if multipleElements == True:
                elements = self.get_elements(locator)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!=0:
                        el.clear()                       
                        el.send_keys(text)
                        return True
                return False
            else:
                element = self.get_element(locator)
                element.clear()
                element.send_keys(text)
                return True 
        except:
            writeToLog("INFO", "FAILED to type text: " + str(text))
            return False 
    
           
    # key event
    def keyevent(self, locator, event):
        element = self.wait_visible(locator)
        if element == False:
            return False
        else:
            element.keyevent(event)
            return True     


    def get_element_attributes(self, locator, multipleElements=False):
        try:
            if multipleElements == True:
                elements = self.get_elements(locator)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!= 0:
                        element = el
                        break
            else:
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
        except:
            writeToLog("INFO", "FAILED to get element")
            return False         
        
    def get_element_text(self, locator, timeout=30):
        if self.wait_visible(locator, timeout) == False:
            return None
        element = self.get_element(locator)
        return element.text
    
    
    def get_element_child_text(self, parent, locator, timeout=30):
        if self.wait_visible_child(parent, locator, timeout) == False:
            return None
        element = self.get_child_element(parent, locator)
        return element.text    
    
    
    def is_element_checked(self, locator):
        element = self.get_element(locator)
        if element.get_attribute("checked") != "true":
            writeToLog("INFO", "'" + locator[1] + "' - element is not checked")
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
    # Set verifyIn = True if you want to verify you url 'in' (not ==) the current url (use it with isRegex=False)
    def verifyUrl(self, expectedUrl, isRegex=False, timeout=30, verifyIn=False):
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
                # Remove the last '/' if exists
                newCurrentUrl = newCurrentUrl.rstrip('/')
                newExpectedUrl = expectedUrl.replace('https://', '')
                newExpectedUrl = newExpectedUrl.replace('http://', '')
                newExpectedUrl = newExpectedUrl.rstrip('/')
                # Compare the URLs
                if verifyIn == False:
                    if newExpectedUrl == newCurrentUrl:
                        return True
                    else:
                        if wait_until < datetime.datetime.now():
                            return False
                else:
                    if newExpectedUrl in newCurrentUrl:
                        return True
                    else:
                        if wait_until < datetime.datetime.now():
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
        elementIframe = self.wait_element(locator, timeout)
        if elementIframe == False:
            writeToLog("INFO","FAILED to get IFRAME element")
            return False      
        self.driver.switch_to.frame(elementIframe)
        return True         
            
            
    def switch_to_default_content(self):
        try:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.DEFAULT
            self.driver.switch_to.default_content()
            return True
        except Exception:
            writeToLog("INFO","FAILED to switch to default content")
            return False        
        
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
    
        
            
    def replaceInLocator(self, locator, replaceWhat, replaceWith):
        return (locator[0], locator[1].replace(replaceWhat, replaceWith))
    
    
    def get_body_element(self):
        return self.get_element(('xpath', '/html/body'))
    
    
    #Copy selected text 
    def copy_to_clipboard(self, textToCopy):
        pyperclip.copy(textToCopy)
    
    
    #Returns string of copy text 
    def paste_from_clipboard(self):
        return str(pyperclip.paste())    

      
    def getAppUnderTest(self):
        return localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST
    
    
    def click_leave_page(self):
        try:
            sleep(2)
            self.driver.switch_to.window(self.driver.current_window_handle)
            self.driver.switch_to.alert.accept()
            if self.wait_for_page_readyState() == False:
                writeToLog("INFO","FAILED to load page after clicking Leave Page")
                return False
            return True
        except Exception:
            return True
        
        
    def click_dialog_accept(self):
        try:
            self.driver.switch_to.alert.accept()
            if self.wait_for_page_readyState() == False:
                writeToLog("INFO","FAILED to click accept")
                return False
            return True
        except Exception:
            writeToLog("INFO","FAILED to click accept")
            return False
        
        
    def click_dialog_dismiss(self):
        try:
            self.driver.switch_to.alert.dismiss()
            if self.wait_for_page_readyState() == False:
                writeToLog("INFO","FAILED to click dismiss")
                return False
            return True
        except Exception:
            writeToLog("INFO","FAILED to click dismiss")
            return False            


    def refresh(self):
        self.driver.refresh()  
