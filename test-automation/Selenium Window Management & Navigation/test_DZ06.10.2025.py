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

#Создать сценарии, которые перемещают окно на координаты X = 400, Y = 300.
class TestTest1():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.keanrichmond.com/")
        self.driver.set_window_position(x=400, y=300)
        time.sleep(1)

#Разработать тесты с одновременной установкой размера окна (ширина и высота) и его позиции на экране.
class TestTest2():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.keanrichmond.com/")
        self.driver.set_window_rect(x=150, y=100, width=800, height=600)
        time.sleep(1)

class TestTest3():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.keanrichmond.com/")
        self.driver.set_window_size(300, 450)
        self.driver.set_window_position(x=400, y=300)
        time.sleep(1)

#Написать сценарии поиска любых 5 элементов в HTML-документе по их атрибуту.
class TestElement1():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("file:D:testfile.html")
        self.driver.find_element(By.ID, "submit-btn")
        time.sleep(2)


class TestElement2():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("file:D:testfile.html")
        self.driver.find_element(By.ID, "subscribe")
        time.sleep(2)


class TestElement3():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("file:D:testfile.html")
        self.driver.find_element(By.ID, "complex-form")
        time.sleep(2)


class TestElement4():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("file:D:testfile.html")
        self.driver.find_element(By.ID, "bio")
        time.sleep(2)


class TestElement5():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("file:D:testfile.html")
        self.driver.find_element(By.ID, "volume")
        time.sleep(2)

#Создать тесты для клика по элементу и последующего возврата на предыдущую страницу (Back).
class TestBack1():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.ID, "mega-menu-item-7549").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)


class TestBack2():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.ID, "mega-menu-item-4461").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)


class TestBack3():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Sign Up for Free").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)

#Создать тесты для клика по элементу и перехода на следующую страницу (Forward).
class TestForward1():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.ID, "mega-menu-item-7549").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)
        self.driver.forward()
        time.sleep(1)


class TestForward2():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.ID, "mega-menu-item-4461").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)
        self.driver.forward()
        time.sleep(1)


class TestForward3():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Sign Up for Free").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)
        self.driver.forward()
        time.sleep(1)

#Написать сценарии клика по элементу с последующей перезагрузкой страницы (Refresh).
class TestRefresh1():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.ID, "mega-menu-item-7549").click()
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)


class TestRefresh2():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.ID, "mega-menu-item-4461").click()
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)


class TestRefresh3():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_test1(self):
        self.driver.get("https://www.anaconda.com/")
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Sign Up for Free").click()
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)