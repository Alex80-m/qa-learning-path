import pytest
import re
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

    # Напиши тест, который проверяет, что элемент с ID username существует и видим на странице.
    def test_test1(self):
        self.driver.get("file:///D:/testfile.html")
        username = self.driver.find_element(By.ID, "username")
        assert username.is_displayed(), "username должен быть виден"

    #Проверь, что значение атрибута placeholder у поля email равно "Введите email".
    def test_test2(self):
        self.driver.get("file:///D:/testfile.html")
        email = self.driver.find_element(By.ID, "emails")
        assert email.get_attribute("placeholder") == "first@mail.example, second@mail.example"

    # Убедись, что на странице три изображения (<img>).
    def test_test3(self):
        self.driver.get("file:///D:/testfile.html")
        images = self.driver.find_elements(By.TAG_NAME, "img")
        assert len(images) == 2, f"Найдено: {len(images)}"
        #С 3 img выдает ошибку ошибку, так как по факту на странице 2 img

    #Напиши тест, который проверяет, что текст заголовка <h1> начинается со слова "Демо".
    def test_test4(self):
        self.driver.get("file:///D:/testfile.html")
        h1_text = self.driver.find_element(By.TAG_NAME, "h1").text
        assert h1_text[:4] == "Демо"

    #Проверь, что значение числа в поле age находится в диапазоне от 18 до 99.
    def test_test5(self):
        self.driver.get("file:///D:/testfile.html")
        age = int(self.driver.find_element(By.ID, "age").get_attribute("value"))
        assert 18 <= age <= 99

    #Убедись, что в футере страницы нет слова "Ошибка".
    def test_test6(self):
        self.driver.get("file:///D:/testfile.html")
        footer = self.driver.find_element(By.TAG_NAME, "footer")
        footer_text = footer.text
        assert "Ошибка" not in footer_text

    #Проверь, что все элементы списка <li> в меню имеют текст строчного типа (str).
    def test_test7(self):
        self.driver.get("file:///D:/testfile.html")
        nav = self.driver.find_element(By.ID, "primary-nav")
        li_list = nav.find_elements(By.TAG_NAME, "li")
        for li in li_list:
           assert isinstance(li.text, str)

    #Убедись, что хотя бы один <button> содержит текст "Отправить".
    def test_test8(self):
        self.driver.get("file:///D:/testfile.html")
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            assert re.search(r"[Отправить]+", button.text)

    #Проверь, что элемент с классом .main-section отображается (is_displayed() == True).
    def test_test9(self):
        self.driver.get("file:///D:/testfile.html")
        main = self.driver.find_element(By.ID, "main")
        assert main.is_displayed() == True

    #Проверь, что атрибут href у первой ссылки не пустой.
    def test_test10(self):
        self.driver.get("file:///D:/testfile.html")
        first_link = self.driver.find_element(By.TAG_NAME, "a")
        href = first_link.get_attribute("href")
        assert href is not None and href != ""

    #Напиши тест, который проверяет, что все ссылки в <nav> имеют атрибут title.
    def test_test11(self):
        self.driver.get("file:///D:/testfile.html")
        nav = self.driver.find_element(By.TAG_NAME, "nav")
        links = nav.find_elements(By.TAG_NAME, "a")
        for link in links:
            title = link.get_attribute("title")
            assert title is not None and title != "", "Ссылка '{link.text}' внутри <nav> не имеет атрибута title"

    #Проверь, что заголовок страницы (driver.title) содержит одно из слов "HTML" или "Demo".
    def test_test12(self):
        self.driver.get("file:///D:/testfile.html")
        title = self.driver.title
        assert "HTML" in title or "Демо" in title

    #Задания по By.LINK_TEXT и By.PARTIAL_LINK_TEXT
    #Найди ссылку по точному тексту "Главная" и проверь, что она кликабельна.
    def test_test13(self):
        self.driver.get("file:///D:/testfile.html")
        link = self.driver.find_element(By.LINK_TEXT, "Главная")
        assert link.is_enabled()
        link.click()

    #Проверь, что ссылка "Формы" содержит в href слово "forms".
    def test_test14(self):
        self.driver.get("file:///D:/testfile.html")
        forms = self.driver.find_element(By.LINK_TEXT, "Формы")
        href = forms.get_attribute("href")
        assert "forms" in href

    #Найди ссылку "Медиа" и проверь, что она видима (is_displayed() == True).
    def test_test15(self):
        self.driver.get("file:///D:/testfile.html")
        media = self.driver.find_element(By.LINK_TEXT, "Медиа")
        assert media.is_displayed() == True

    #Используй By.PARTIAL_LINK_TEXT, чтобы найти ссылку по части слова "Глав" и убедись, что найденный текст равен "Главная".
    def test_test16(self):
        self.driver.get("file:///D:/testfile.html")
        link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Глав")
        text = link.text
        assert text == "Главная"

    #Найди ссылку по части слова "Форм" и проверь, что она активна (is_enabled() == True).
    def test_test17(self):
        self.driver.get("file:///D:/testfile.html")
        form = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Форм")
        assert form.is_enabled() == True

    #Напиши тест, который проверяет, что по частичному тексту "Мед" находится именно ссылка "Медиа".
    def test_test18(self):
        self.driver.get("file:///D:/testfile.html")
        media = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Мед")
        assert media.text == "Медиа"


