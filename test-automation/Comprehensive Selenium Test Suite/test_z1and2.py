import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

"""1. Базовая настройка фикстуры"""
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("file:///D:/testsite.html")
    yield driver
    driver.quit()

"""2. Проверка наличия всех уникальных `id`"""
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Проверка уникальности ID")
@allure.title("Проверка уникальности и количества всех ID на странице")
@allure.description("Тест проверяет что все атрибуты ID уникальны и их количество не менее 80")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("id", "validation", "unique")
def test_unique_ids(driver):
    with allure.step("Сбор всех элементов с атрибутом id"):
        elements_with_id = driver.find_elements(By.XPATH, "//*[@id]")
        all_ids = [element.get_attribute("id") for element in elements_with_id]

    with allure.step("Проверка минимального количества элементов"):
        expected_min_count = 80
        assert len(all_ids) >= expected_min_count

    with allure.step("Проверка уникальности всех ID"):
        unique_ids = set(all_ids)
        assert len(all_ids) == len(unique_ids)

    print(f"Найдено {len(all_ids)} элементов с id")
    print(f"Все id уникальны")