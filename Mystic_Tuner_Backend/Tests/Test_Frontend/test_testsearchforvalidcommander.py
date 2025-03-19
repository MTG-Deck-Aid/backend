# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestTestsearchforvalidcommander():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_testsearchforvalidcommander(self):
    self.driver.implicitly_wait(5)  # Wait up to 10 seconds

    # Test name: test_search_for_valid_commander
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://localhost:3000/")
    # 2 | setWindowSize | 1721x1033 | 
    self.driver.set_window_size(1721, 1033)
    # 3 | click | linkText=Make a Deck! | 
    self.driver.find_element(By.LINK_TEXT, "Make a Deck!").click()
    time.sleep(2)
    # 4 | click | css=.text-xl | 
    self.driver.find_element(By.XPATH, "//button[contains(text(), 'Choose Your Commander')]").click()

    self.driver.find_element(By.XPATH, "//input[@placeholder='Type to search...']").send_keys("Gluntch")
    time.sleep(3)
    self.driver.find_element(By.XPATH, "//input[@placeholder='Type to search...']").send_keys(Keys.ENTER)
    time.sleep(5)
    self.driver.find_element(By.XPATH, "//button[contains(@class, 'bg-success') and contains(@class, 'text-success-700')]").click()

    time.sleep(2)
    # 9 | assertElementPresent | css=.rounded-2xl | 
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".rounded-2xl")
    assert len(elements) > 0
  
