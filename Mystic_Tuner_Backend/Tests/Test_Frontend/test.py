from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



driver = webdriver.Edge()


driver.get("http://localhost:3000")

button = driver.find_element(By.CLASS_NAME, "bg-sky-blue")

button.click()

input("end script:")