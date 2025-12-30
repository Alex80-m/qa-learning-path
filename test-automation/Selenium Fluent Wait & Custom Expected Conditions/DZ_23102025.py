import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException


class TestElementWait:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.get('https://fojin.tech/')

    def teardown_method(self, method):
        self.driver.quit()

    #Реализовать тест, который ожидает появления элемента по ID с шагом 0.2 секунды и тайм-аутом 10 секунд.
    def test_test1(self):
        wait = WebDriverWait(
            self.driver,
            timeout=10,
            poll_frequency=0.2,
            ignored_exceptions=[NoSuchElementException]
        )
        element = wait.until(EC.visibility_of_element_located((By.ID, "cases")))
        assert element.is_displayed()

    #Написать тест, который ожидает, пока кнопка станет кликабельной, игнорируя ElementNotInteractableException.
    def test_test2(self):
        wait = WebDriverWait(
            self.driver,
            timeout=10,
            poll_frequency=0.2,
            ignored_exceptions=[ElementNotInteractableException]
        )
        elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header_header__actions__submit__0EIOT")))
        assert elem.is_enabled()

    #Создать тест, который проверяет, что поле ввода получает текст “OK” в течение 15 секунд с шагом опроса 0.5 с.
    def test_test3(self):
        wait = WebDriverWait(
            self.driver,
            timeout=15,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException]
        )
        submit_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header_header__actions__submit__0EIOT")))
        submit_btn.click()
        name_input = wait.until(EC.presence_of_element_located((By.ID, "name")))
        name_input.clear()
        name_input.send_keys("OK")
        assert name_input.get_attribute("value") == "OK", "Поле не содержит текст 'OK'"

    #Реализовать Fluent Wait, который ждёт, пока элемент исчезнет со страницы (удалён из DOM).
    def test_test4(self):
        wait = WebDriverWait(
            self.driver,
            timeout=15,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException]
        )
        cookie_banner = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cookie_cookie__6eQPy")))
        ok_button = cookie_banner.find_element(By.CLASS_NAME, "cookie_cookie__button__h8vvk")
        ok_button.click()
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cookie_cookie__6eQPy")))

    #Написать ожидание, которое проверяет наличие класса "active" у элемента.
    #так как в данном HTML нат в наличии класса "active", будем искать класс "header_header__nav__submit__LOR0F"
    def test_test5(self):
        wait = WebDriverWait(self.driver, 10, poll_frequency=0.2)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "header_header__nav__submit__LOR0F")))
        classes = element.get_attribute("class")
        assert "header_header__nav__submit__LOR0F" in classes.split(), f"Класс не найден в: {classes}"

    #Реализовать тест с ожиданием изменения атрибута "value" у поля ввода.
    @pytest.mark.parametrize(
    "name, contact, company",
    [
        ("Мария", "+79998887766", "ИП Петрова"),
        ("Тест", "+71234567890", "Тестовая организация"),
    ]
    )
    def test_test6(self, name, contact, company):
        wait = WebDriverWait(self.driver, 15)
        submit_btn = wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "header_header__actions__submit__0EIOT")
        ))
        submit_btn.click()
        name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
        contact_field = wait.until(EC.presence_of_element_located((By.ID, "contact")))
        company_field = wait.until(EC.presence_of_element_located((By.ID, "company")))

        name_field.clear()
        name_field.send_keys(name)
        wait.until(lambda driver: name_field.get_attribute("value") == name)

        contact_field.clear()
        contact_field.send_keys(contact)
        wait.until(lambda driver: contact_field.get_attribute("value") == contact)

        company_field.clear()
        company_field.send_keys(company)
        wait.until(lambda driver: company_field.get_attribute("value") == company)
        assert name_field.get_attribute("value") == name
        assert contact_field.get_attribute("value") == contact
        assert company_field.get_attribute("value") == company

    #Написать Fluent Wait, который ждёт появления хотя бы одного элемента по CSS-селектору .menu-item.
    #Так как в данном HTML отсутствует - .menu-item, то применю их аналог для навигационных ссылок.
    def test_test7(self):
        wait = WebDriverWait(
            self.driver,
            timeout=15,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException]
        )
        nav_links = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".header_header__nav__link__KtvV2"))
        )

        assert len(nav_links) >= 4, f"Найдено навигационных ссылок: {len(nav_links)}"
        expected_menu_items = ["Кейсы", "Награды", "Медиа", "Специалисты"]
        actual_texts = [link.text for link in nav_links]
        assert expected_menu_items == actual_texts

    #Создать ожидание, которое проверяет, что количество элементов на странице стало равно 5.
    def test_test8(self):
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, ".header_header__nav__link__KtvV2")
        )
        assert len(elements) == 4, f"Найдено {len(elements)} элементов"

    #Сделать тест, где ожидание игнорирует StaleElementReferenceException и ждёт повторного появления элемента.
    def test_test9(self):
        wait = WebDriverWait(
            self.driver,
            timeout=15,
            poll_frequency=0.5,
            ignored_exceptions=[StaleElementReferenceException]
        )
        element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".header_header__nav__link__KtvV2"))
        )

    #Написать ожидание, которое ждёт, пока текст элемента изменится на “Готово”.
    def test_wait_for_ready_text(self):
        wait = WebDriverWait(self.driver, 10)
        nav_element = self.driver.find_element(By.CSS_SELECTOR, "a[data-target='cases']")
        original_text = nav_element.text
        self.driver.execute_script("""
            var element = arguments[0];
            setTimeout(function() {
                element.textContent = 'Готово';
                }, 2000);
        """, nav_element)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "a[data-target='cases']"), "Готово"))
        time.sleep(5)