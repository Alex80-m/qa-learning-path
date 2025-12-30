import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("file:///D:/testsite.html")
    yield driver
    driver.quit()

# 3. Тест кнопок
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Тестирование кнопок")
class TestButtons:
    @allure.title("Проверка наличия кнопок на странице")
    @allure.description("Параметризованный тест для проверки существования всех основных кнопок")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("buttons", "existence", "parametrized")
    @pytest.mark.parametrize("button_id", [
        "btn-primary",
        "btn-submit",
        "btn-reset",
        "input-button"
    ])
    def test_buttons_existence(self, driver, button_id):
        """Наличие кнопок с `id`: `btn-primary`, `btn-submit`, `btn-reset`, `input-button`"""
        with allure.step(f"Поиск кнопки с ID: {button_id}"):
            button = driver.find_element(By.ID, button_id)
        with allure.step(f"Проверка отображения кнопки {button_id}"):
            assert button.is_displayed(), f"Кнопка с id '{button_id}' не найдена на странице"

    @allure.title("Проверка отключенного состояния кнопки btn-primary")
    @allure.description("Тестирование что кнопка btn-primary имеет состояние disabled")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("buttons", "state", "disabled")
    def test_primary_button_disabled(self, driver):
        """- Что кнопка `btn-primary` отключена (`is_enabled() == False`)"""
        with allure.step("Поиск кнопки btn-primary"):
            primary_button = driver.find_element(By.ID, "btn-primary")
        with allure.step("Проверка что кнопка отключена"):
            assert primary_button.is_enabled() == False, "Кнопка btn-primary должна быть отключена (is_enabled() == False)"

    @allure.title("Проверка свойств кнопки btn-submit")
    @allure.description("Тестирование что кнопка btn-submit включена и имеет правильный тип")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("buttons", "submit", "properties")
    def test_submit_button(self, driver):
        """- Что кнопка `btn-submit` включена и имеет `type="submit"`"""
        with allure.step("Поиск кнопки btn-submit"):
            submit_button = driver.find_element(By.ID, "btn-submit")
        with allure.step("Проверка что кнопка включена"):
            assert submit_button.is_enabled(), "Кнопка btn-submit должна быть включена"
        with allure.step("Проверка type кнопки"):
            assert submit_button.get_attribute("type") == "submit", "Кнопка btn-submit должна иметь type='submit'"

