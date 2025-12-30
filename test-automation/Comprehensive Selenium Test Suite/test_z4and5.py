import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("file:///D:/testsite.html")
    yield driver
    driver.quit()

#4. Тест выпадающего меню `<select>`
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Базовая настройка")
class TestDropdownMenu:
    @allure.title("Проверка наличия выпадающего списка fruit-select")
    @allure.description("Тестирование что элемент select с фруктами существует на странице")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("dropdown", "select", "existence")
    def test_fruit_select_exists(self, driver):
        """Проверка наличия элемента с id='fruit-select'"""
        with allure.step("Поиск элемента fruit-selec"):
            select_element = driver.find_element(By.ID, "fruit-select")
        with allure.step("Проверка отображения элемента"):
            assert select_element.is_displayed(), "Элемент fruit-select не найден на странице"

    @allure.title("Проверка выбора по умолчанию в выпадающем списке")
    @allure.description("Тестирование что по умолчанию выбран пустой вариант")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("dropdown", "default", "selection")
    def test_default_selection(self, driver):
        """Что по умолчанию выбран элемент с `id="opt-empty"` (или `value=""`)"""
        with allure.step("Поиск выпадающего списка"):
            select_element = driver.find_element(By.ID, "fruit-select")
        with allure.step("Проверка значения по умолчанию"):
            selected_value = select_element.get_attribute("value")
            assert selected_value == "", f"По умолчанию должен быть выбран value='', но выбран '{selected_value}'"

    @allure.title("Проверка выбора опции 'Яблоко' в выпадающем списке")
    @allure.description("Тестирование возможности выбора значения apple и корректного отображения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("dropdown", "selection", "interaction")
    def test_select_apple(self, driver):
        """- Что можно выбрать "Яблоко" (`value="apple"`) и значение изменится"""
        with allure.step("Поиск и инициализация выпадающего списка"):
            select_element = driver.find_element(By.ID, "fruit-select")
            dropdown = Select(select_element)
        with allure.step("Выбор опции 'Яблоко' по значению apple"):
            dropdown.select_by_value("apple")
        with allure.step("Проверка выбранного значения и текста"):
            selected_value = select_element.get_attribute("value")
            selected_option = dropdown.first_selected_option
            assert selected_value == "apple"
            assert selected_option.text == "Яблоко", f"Должно быть'Яблоко', а отображается '{selected_option.text}'"

#5. Тест `<details>/<summary>`
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Элементы details/summary")
class TestDetailsSummary:
    @allure.title("Проверка наличия элемента details")
    @allure.description("Тестирование что элемент details с меню существует на странице")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("details", "summary", "existence")
    def test_details_element_exists(self, driver):
        """Проверка наличия элемента details с id='details-menu'"""
        with allure.step("Поиск элемента details"):
            details_element = driver.find_element(By.ID, "details-menu")
        with allure.step("Проверка отображения элемента"):
            assert details_element.is_displayed(), "Элемент details-menu не найден"

    @allure.title("Проверка открытого состояния details по умолчанию")
    @allure.description("Тестирование что элемент details изначально открыт")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("details", "state", "default")
    def test_details_default_open(self, driver):
        """- Что по умолчанию он открыт (`open` атрибут присутствует)"""
        with allure.step("Поиск элемента details"):
            details_element = driver.find_element(By.ID, "details-menu")
        with allure.step("Проверка атрибута open"):
            open_attribute = details_element.get_attribute("open")
            assert open_attribute is not None, "Элемент details должен быть открыт по умолчанию (атрибут open)"

    @allure.title("Проверка взаимодействия с details/summary")
    @allure.description("Тестирование открытия/закрытия содержимого при клике на summary")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("details", "summary", "interaction")
    def test_details_content_visible(self, driver):
        """Проверка что при клике на `<summary>` (если бы он был закрыт) содержимое появляется """
        with allure.step("Поиск элементов details, summary и content"):
            details = driver.find_element(By.ID, "details-menu")
            summary = driver.find_element(By.ID, "summary-toggle")
            content = driver.find_element(By.ID, "details-content")

        with allure.step("Закрытие details элемента"):
            driver.execute_script("arguments[0].removeAttribute('open');", details)
        with allure.step("Проверка что содержимое скрыто"):
            assert not content.is_displayed()
        with allure.step("Клик по summary для открытия"):
            summary.click()
        with allure.step("Проверка что содержимое появилось"):
            assert content.is_displayed(), "Содержимое не появилось после клика по summary"