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
from selenium.webdriver.support import expected_conditions as EC


class TestLocators():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_name(self):
        self.driver.get("file:D:testfile.html")
        locator_name = self.driver.find_element(By.NAME, "bio")
        locator_name.clear()
        locator_name.send_keys("Какой-то текст!")
        print(f"Ввести текст в поле 'name' {locator_name.get_attribute('value')}")
        time.sleep(3)

    def test_class_name(self):
        self.driver.get("https://natalexauto.com/")
        locator_class_name = self.driver.find_element(By.CLASS_NAME, "button_button__tY9TG")
        locator_class_name.click()
        time.sleep(2)

    def test_css_selector(self):
        self.driver.get("https://natalexauto.com/")
        self.driver.find_element(By.CSS_SELECTOR, "button#undefined-\\:r4\\:").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "a.menu_brand__j5EWO:nth-of-type(6)").click()
        time.sleep(2)

    def test_xpath(self):
        self.driver.get("https://natalexauto.com/")
        locator_xpath = self.driver.find_element(By.XPATH, "//button[contains(@class, 'button_button__tY9TG')]")
        locator_xpath.click()
        time.sleep(2)
        ford_element = self.driver.find_element(By.XPATH, "//p[text()='FORD']")
        ford_element.click()
        time.sleep(2)








